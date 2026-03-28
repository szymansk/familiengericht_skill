#!/usr/bin/env python3
"""RAG-Suche: Semantische Suche über alle Verfahrensdokumente.

Aufruf:
  python rag-search.py "Umgang verweigert"
  python rag-search.py "Umgang verweigert" --verfahren 3-f-24-26
  python rag-search.py "Umgang verweigert" --top 10
  python rag-search.py "Umgang verweigert" --doc-type beleg
"""

import argparse
import os
import sqlite3
import struct
import sys
from pathlib import Path

# ── .env laden (HF_TOKEN für HuggingFace-Auth) ──────────────────────────────
def _load_dotenv():
    """Lädt KEY='value'-Paare aus .env ins Environment."""
    for d in (Path.cwd(), Path(__file__).resolve().parent.parent.parent.parent):
        env_file = d / ".env"
        if env_file.is_file():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip().strip("'\""))
            break

_load_dotenv()

import sqlite_vec
from sentence_transformers import SentenceTransformer

MODEL_NAME = "mixedbread-ai/deepset-mxbai-embed-de-large-v1"
EMBEDDING_DIM = 1024


def find_db(start: Path) -> Path:
    """Sucht rag-index.db im Projektverzeichnis."""
    cwd = start.resolve()
    for _ in range(10):
        candidate = cwd / "rag-index.db"
        if candidate.exists():
            return candidate
        cwd = cwd.parent
    sys.exit("Fehler: rag-index.db nicht gefunden. Zuerst rag-index.py ausführen.")


def serialize_f32(vec: list[float]) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)


def _vector_search_raw(
    conn: sqlite3.Connection,
    model: SentenceTransformer,
    query: str,
    fetch_k: int,
) -> list[tuple[int, float]]:
    """Vektor-Suche, gibt (rowid, distance) zurück."""
    query_emb = model.encode([query], normalize_embeddings=True)
    query_vec = serialize_f32(query_emb[0].tolist())
    return conn.execute(
        """SELECT rowid, distance FROM vec_chunks
           WHERE embedding MATCH ? ORDER BY distance LIMIT ?""",
        (query_vec, fetch_k),
    ).fetchall()


def _fts_search_raw(
    conn: sqlite3.Connection,
    query: str,
    fetch_k: int,
) -> list[tuple[int, float]]:
    """FTS5-Keyword-Suche, gibt (rowid, rank) zurück. Leere Liste wenn kein FTS5."""
    has_fts = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='fts_chunks'"
    ).fetchone()
    if not has_fts:
        return []
    words = [w for w in query.split() if len(w) > 2]
    if not words:
        return []
    fts_query = " OR ".join(f'"{w}"' for w in words)
    try:
        return conn.execute(
            "SELECT rowid, rank FROM fts_chunks WHERE text MATCH ? ORDER BY rank LIMIT ?",
            (fts_query, fetch_k),
        ).fetchall()
    except sqlite3.OperationalError:
        return []


def _load_chunk(conn: sqlite3.Connection, rowid: int) -> dict | None:
    """Lädt Chunk-Metadaten anhand der rowid."""
    row = conn.execute(
        "SELECT verfahren, source_file, line_start, line_end, text, doc_type FROM chunks WHERE id = ?",
        (rowid,),
    ).fetchone()
    if not row:
        return None
    v, src, ls, le, txt, dt = row
    return {"verfahren": v, "source_file": src, "line_start": ls,
            "line_end": le, "text": txt, "doc_type": dt}


def search(
    conn: sqlite3.Connection,
    model: SentenceTransformer,
    query: str,
    top_k: int = 5,
    verfahren: str | None = None,
    doc_type: str | None = None,
    mode: str = "hybrid",
) -> list[dict]:
    """Hybrid-Suche (Vector + FTS5 mit RRF), oder reine Vektor-/Keyword-Suche."""
    K = 60  # RRF-Konstante
    fetch_k = top_k * 6

    # Vektor-Suche
    vec_rows = _vector_search_raw(conn, model, query, fetch_k) if mode != "keyword" else []
    # FTS5-Suche
    fts_rows = _fts_search_raw(conn, query, fetch_k) if mode != "vector" else []

    vec_rank = {rowid: rank for rank, (rowid, _) in enumerate(vec_rows)}
    fts_rank = {rowid: rank for rank, (rowid, _) in enumerate(fts_rows)}

    # RRF-Score berechnen
    all_ids = set(vec_rank) | set(fts_rank)
    rrf_scores = {
        rowid: (
            (1 / (K + vec_rank[rowid]) if rowid in vec_rank else 0) +
            (1 / (K + fts_rank[rowid]) if rowid in fts_rank else 0)
        )
        for rowid in all_ids
    }

    # Nach Score sortieren, Filter anwenden
    results = []
    for rowid, score in sorted(rrf_scores.items(), key=lambda x: -x[1]):
        chunk = _load_chunk(conn, rowid)
        if not chunk:
            continue
        if verfahren and chunk["verfahren"] != verfahren:
            continue
        if doc_type and chunk["doc_type"] != doc_type:
            continue

        # Herkunft kennzeichnen
        in_vec = rowid in vec_rank
        in_fts = rowid in fts_rank
        source = "[V+K]" if (in_vec and in_fts) else ("[K]" if in_fts else "[V]")

        results.append({**chunk, "score": score, "source": source})
        if len(results) >= top_k:
            break

    return results


def main():
    parser = argparse.ArgumentParser(description="RAG-Suche über Verfahrensdokumente")
    parser.add_argument("query", help="Suchanfrage (natürliche Sprache)")
    parser.add_argument("--verfahren", help="Nur in diesem Verfahren suchen")
    parser.add_argument("--doc-type", help="Nur diesen Dokumenttyp (beleg, sachverhalt, …)")
    parser.add_argument("--top", type=int, default=5, help="Anzahl Treffer (default: 5)")
    parser.add_argument(
        "--mode", choices=["hybrid", "vector", "keyword"], default="hybrid",
        help="Suchmodus: hybrid (default), vector, keyword"
    )
    args = parser.parse_args()

    db_file = find_db(Path.cwd())
    conn = sqlite3.connect(str(db_file))
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)

    # Prüfen ob Index leer ist
    count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    if count == 0:
        sys.exit("Index ist leer. Zuerst rag-index.py ausführen.")

    print(f"→ Lade Embedding-Modell …", file=sys.stderr)
    model = SentenceTransformer(MODEL_NAME)

    results = search(conn, model, args.query, args.top, args.verfahren, args.doc_type, args.mode)
    conn.close()

    if not results:
        print("Keine Treffer gefunden.")
        return

    print(f"\n{'─' * 72}")
    print(f"Suche: \"{args.query}\"")
    if args.mode != "hybrid":
        print(f"Modus: {args.mode}")
    if args.verfahren:
        print(f"Filter: Verfahren={args.verfahren}")
    if args.doc_type:
        print(f"Filter: Typ={args.doc_type}")
    print(f"{'─' * 72}\n")

    for i, r in enumerate(results, 1):
        snippet = r["text"][:200].replace("\n", " ")
        if len(r["text"]) > 200:
            snippet += " …"
        ref = f"{r['source_file']}:Z. {r['line_start']}-{r['line_end']}"
        print(f"#{i} {r['source']} [{r['score']:.4f}] {r['verfahren']} | {ref}")
        print(f'   \u201e{snippet}\u201c')
        print()


if __name__ == "__main__":
    main()
