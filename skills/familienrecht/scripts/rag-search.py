#!/usr/bin/env python3
"""RAG-Suche: Semantische Suche über alle Verfahrensdokumente.

Aufruf:
  python rag-search.py "Umgang verweigert"
  python rag-search.py "Umgang verweigert" --verfahren 3-f-24-26
  python rag-search.py "Umgang verweigert" --top 10
  python rag-search.py "Umgang verweigert" --doc-type beleg
"""

import argparse
import sqlite3
import struct
import sys
from pathlib import Path

import sqlite_vec
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBEDDING_DIM = 384


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


def search(
    conn: sqlite3.Connection,
    model: SentenceTransformer,
    query: str,
    top_k: int = 5,
    verfahren: str | None = None,
    doc_type: str | None = None,
) -> list[dict]:
    """Führt semantische Suche durch, gibt Treffer mit Metadaten zurück."""
    query_emb = model.encode([query], normalize_embeddings=True)
    query_vec = serialize_f32(query_emb[0].tolist())

    # Erste Phase: Vektor-Suche (breit, da wir danach filtern)
    fetch_k = top_k * 5 if (verfahren or doc_type) else top_k
    rows = conn.execute(
        """SELECT rowid, distance
           FROM vec_chunks
           WHERE embedding MATCH ?
           ORDER BY distance
           LIMIT ?""",
        (query_vec, fetch_k),
    ).fetchall()

    results = []
    for rowid, distance in rows:
        chunk = conn.execute(
            """SELECT verfahren, source_file, line_start, line_end, text, doc_type
               FROM chunks WHERE id = ?""",
            (rowid,),
        ).fetchone()
        if not chunk:
            continue

        v, src, ls, le, txt, dt = chunk

        # Filter anwenden
        if verfahren and v != verfahren:
            continue
        if doc_type and dt != doc_type:
            continue

        score = 1.0 - distance  # Cosine similarity
        results.append(
            {
                "score": score,
                "verfahren": v,
                "source_file": src,
                "line_start": ls,
                "line_end": le,
                "text": txt,
                "doc_type": dt,
            }
        )

        if len(results) >= top_k:
            break

    return results


def main():
    parser = argparse.ArgumentParser(description="RAG-Suche über Verfahrensdokumente")
    parser.add_argument("query", help="Suchanfrage (natürliche Sprache)")
    parser.add_argument("--verfahren", help="Nur in diesem Verfahren suchen")
    parser.add_argument("--doc-type", help="Nur diesen Dokumenttyp (beleg, sachverhalt, …)")
    parser.add_argument("--top", type=int, default=5, help="Anzahl Treffer (default: 5)")
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

    results = search(conn, model, args.query, args.top, args.verfahren, args.doc_type)
    conn.close()

    if not results:
        print("Keine Treffer gefunden.")
        return

    print(f"\n{'─' * 72}")
    print(f"Suche: \"{args.query}\"")
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
        print(f"#{i} [{r['score']:.2f}] {r['verfahren']} | {ref}")
        print(f'   \u201e{snippet}\u201c')
        print()


if __name__ == "__main__":
    main()
