#!/usr/bin/env python3
"""RAG-Index: Verfahrensdokumente → sqlite-vec Vektordatenbank.

Indiziert alle .md-Dateien in verfahren/ rekursiv, außer:
  - belege/originale/  (Binärdateien, Inhalt liegt als .md in Nachbarordnern)
  - output/            (generierte PDFs/TEX/DOCX)
  - .claudeprompt/     (Claude-Konfiguration)

Aufruf:
  python rag-index.py                          # alle Verfahren
  python rag-index.py --verfahren 3-f-24-26    # nur ein Verfahren
  python rag-index.py --reset                  # DB löschen, komplett neu
"""

import argparse
import hashlib
import os
import re
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

# ── Konfiguration ────────────────────────────────────────────────────────────

MODEL_NAME = "mixedbread-ai/deepset-mxbai-embed-de-large-v1"
EMBEDDING_DIM = 1024
MAX_CHUNK_WORDS = 400
OVERLAP_WORDS = 50

_DEFAULT_EXCLUDED_DIRS = {"originale", "output", ".claudeprompt", ".obsidian", ".smart-env",
                          "node_modules", ".venv", "__pycache__", ".git"}
EXCLUDED_FILES = {".gitkeep", ".gitignore", ".DS_Store"}


def _load_ragignore(start: Path) -> set[str]:
    """Lädt Ausschlüsse aus .ragignore, ergänzt Defaults (ersetzt sie nie)."""
    for d in (start, Path(__file__).resolve().parent.parent.parent.parent):
        ragignore = d / ".ragignore"
        if ragignore.is_file():
            entries = set()
            for line in ragignore.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    entries.add(line)
            return entries | _DEFAULT_EXCLUDED_DIRS
    return _DEFAULT_EXCLUDED_DIRS


EXCLUDED_DIRS = _load_ragignore(Path.cwd())

# ── Hilfsfunktionen ─────────────────────────────────────────────────────────


def find_verfahren_root(start: Path) -> Path:
    """Sucht das verfahren/-Verzeichnis ab start aufwärts."""
    cwd = start.resolve()
    for _ in range(10):
        candidate = cwd / "verfahren"
        if candidate.is_dir():
            return candidate
        cwd = cwd.parent
    # Fallback: verfahren/ relativ zum Skript (für Test-Setups)
    script_dir = Path(__file__).resolve().parent
    for _ in range(5):
        candidate = script_dir / "verfahren"
        if candidate.is_dir():
            return candidate
        script_dir = script_dir.parent
    sys.exit("Fehler: verfahren/-Verzeichnis nicht gefunden.")


def db_path_for(verfahren_root: Path) -> Path:
    """DB liegt im Projekt-Root (Eltern von verfahren/)."""
    return verfahren_root.parent / "rag-index.db"


def should_skip(rel_parts: tuple[str, ...]) -> bool:
    """Prüft ob ein Pfad in der Ausschlussliste liegt."""
    return any(part in EXCLUDED_DIRS for part in rel_parts)


def collect_md_files(verfahren_dir: Path) -> list[Path]:
    """Sammelt alle .md-Dateien rekursiv, wendet Ausschlussregeln an."""
    results = []
    for md_file in verfahren_dir.rglob("*.md"):
        if md_file.name in EXCLUDED_FILES:
            continue
        rel = md_file.relative_to(verfahren_dir)
        if should_skip(rel.parts):
            continue
        results.append(md_file)
    return sorted(results)


def strip_frontmatter(text: str) -> tuple[str, int]:
    """Entfernt YAML-Frontmatter, gibt (text, offset_lines) zurück."""
    if not text.startswith("---"):
        return text, 0
    end = text.find("\n---", 3)
    if end == -1:
        return text, 0
    offset = text[: end + 4].count("\n")
    return text[end + 4 :].lstrip("\n"), offset


def classify_doc_type(rel_path: Path) -> str:
    """Leitet doc_type aus dem ersten Verzeichnis im relativen Pfad ab."""
    parts = rel_path.parts
    if len(parts) == 1:
        # Datei im Verfahrens-Root (z.B. kontext.md)
        return "kontext"
    first_dir = parts[0]
    if first_dir == "belege":
        return "beleg"
    return first_dir


LEGAL_SPLIT_PATTERN = re.compile(
    r"(?:"
    r"\n#{1,3}\s"               # Markdown-Überschriften
    r"|\n(?:I{1,3}V?|V)\.\s"   # I. II. III. IV. V.
    r"|\n\d+\.\s"               # 1. 2. 3.
    r"|\n§\s*\d+"               # § 1626 etc.
    r"|\n[a-z]\)\s"             # a) b) c)
    r"|\n\n+"                   # Absatzgrenzen (Fallback)
    r")"
)


def chunk_text(
    text: str, line_offset: int
) -> list[dict]:
    """Splittet Text an juristischen Strukturgrenzen in Chunks mit Zeilennummern."""
    paragraphs = LEGAL_SPLIT_PATTERN.split(text)
    chunks = []
    current_words: list[str] = []
    current_line_start = line_offset + 1
    current_line = line_offset

    for para in paragraphs:
        para = para.strip()
        if not para:
            current_line += 2
            continue

        para_lines = para.count("\n") + 1
        para_words = para.split()

        # Reine Überschriften überspringen
        if re.match(r"^#{1,6}\s+", para) and len(para_words) < 8:
            current_line += para_lines + 1
            continue

        if len(current_words) + len(para_words) > MAX_CHUNK_WORDS and current_words:
            chunk_text_str = " ".join(current_words)
            if len(chunk_text_str.strip()) > 20:
                chunks.append(
                    {
                        "text": chunk_text_str,
                        "line_start": current_line_start,
                        "line_end": current_line,
                    }
                )

            # Overlap: letzte OVERLAP_WORDS Wörter behalten
            if len(current_words) > OVERLAP_WORDS:
                current_words = current_words[-OVERLAP_WORDS:]
            current_line_start = max(current_line_start, current_line - 3)

        if not current_words:
            current_line_start = current_line + 1

        current_words.extend(para_words)
        current_line += para_lines + 1  # +1 für die Leerzeile danach

    # Letzter Chunk
    if current_words:
        chunk_text_str = " ".join(current_words)
        if len(chunk_text_str.strip()) > 20:
            chunks.append(
                {
                    "text": chunk_text_str,
                    "line_start": current_line_start,
                    "line_end": current_line,
                }
            )

    return chunks


def serialize_f32(vec: list[float]) -> bytes:
    """Serialisiert float-Vektor für sqlite-vec."""
    return struct.pack(f"{len(vec)}f", *vec)


# ── Datenbank ────────────────────────────────────────────────────────────────


def init_db(db: Path) -> sqlite3.Connection:
    """Erstellt DB und Tabellen falls nötig."""
    conn = sqlite3.connect(str(db))
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS chunks (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            verfahren     TEXT NOT NULL,
            source_file   TEXT NOT NULL,
            line_start    INTEGER NOT NULL,
            line_end      INTEGER NOT NULL,
            text          TEXT NOT NULL,
            doc_type      TEXT NOT NULL,
            mtime         REAL NOT NULL,
            content_hash  TEXT NOT NULL DEFAULT ''
        )"""
    )
    conn.execute(
        """CREATE INDEX IF NOT EXISTS idx_chunks_verfahren
           ON chunks(verfahren)"""
    )
    conn.execute(
        """CREATE INDEX IF NOT EXISTS idx_chunks_source
           ON chunks(verfahren, source_file)"""
    )
    # sqlite-vec virtual table
    conn.execute(
        f"""CREATE VIRTUAL TABLE IF NOT EXISTS vec_chunks
            USING vec0(embedding float[{EMBEDDING_DIM}])"""
    )
    # FTS5 für Keyword-Suche (Hybrid-Suche)
    conn.execute(
        """CREATE VIRTUAL TABLE IF NOT EXISTS fts_chunks
           USING fts5(text, tokenize='unicode61 remove_diacritics 1')"""
    )
    conn.commit()
    return conn


def file_needs_update(
    conn: sqlite3.Connection, verfahren: str, rel_path: str, content_hash: str
) -> bool:
    """Prüft ob die Datei seit dem letzten Index geändert wurde (Hash-basiert)."""
    row = conn.execute(
        "SELECT content_hash FROM chunks WHERE verfahren=? AND source_file=? LIMIT 1",
        (verfahren, rel_path),
    ).fetchone()
    if row is None:
        return True
    return row[0] != content_hash


def delete_file_chunks(
    conn: sqlite3.Connection, verfahren: str, rel_path: str
) -> int:
    """Löscht alle Chunks einer Datei (für Re-Index)."""
    ids = [
        r[0]
        for r in conn.execute(
            "SELECT id FROM chunks WHERE verfahren=? AND source_file=?",
            (verfahren, rel_path),
        ).fetchall()
    ]
    if ids:
        placeholders = ",".join("?" * len(ids))
        conn.execute(f"DELETE FROM vec_chunks WHERE rowid IN ({placeholders})", ids)
        conn.execute(f"DELETE FROM fts_chunks WHERE rowid IN ({placeholders})", ids)
        conn.execute(
            f"DELETE FROM chunks WHERE id IN ({placeholders})", ids
        )
    return len(ids)


# ── Hauptlogik ───────────────────────────────────────────────────────────────


def index_verfahren(
    conn: sqlite3.Connection,
    model: SentenceTransformer,
    verfahren_dir: Path,
    verfahren_name: str,
) -> dict:
    """Indiziert ein einzelnes Verfahren. Gibt Statistiken zurück."""
    stats = {"files": 0, "chunks": 0, "skipped": 0}
    md_files = collect_md_files(verfahren_dir)

    for md_file in md_files:
        rel_path = str(md_file.relative_to(verfahren_dir))

        # Datei lesen und Hash berechnen
        raw_text = md_file.read_text(encoding="utf-8", errors="replace")
        content_hash = hashlib.sha256(raw_text.encode()).hexdigest()
        mtime = os.path.getmtime(md_file)

        if not file_needs_update(conn, verfahren_name, rel_path, content_hash):
            stats["skipped"] += 1
            continue

        # Alte Chunks löschen (Re-Index)
        delete_file_chunks(conn, verfahren_name, rel_path)

        text = raw_text
        text, line_offset = strip_frontmatter(text)
        chunks = chunk_text(text, line_offset)

        if not chunks:
            stats["skipped"] += 1
            continue

        doc_type = classify_doc_type(Path(rel_path))

        # Embeddings berechnen (Batch)
        prefixed_texts = [
            f"[{verfahren_name} | {rel_path}]\n{c['text']}" for c in chunks
        ]
        embeddings = model.encode(prefixed_texts, normalize_embeddings=True)

        # In DB speichern
        for chunk, emb in zip(chunks, embeddings):
            cur = conn.execute(
                """INSERT INTO chunks
                   (verfahren, source_file, line_start, line_end, text, doc_type, mtime, content_hash)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    verfahren_name,
                    rel_path,
                    chunk["line_start"],
                    chunk["line_end"],
                    chunk["text"],
                    doc_type,
                    mtime,
                    content_hash,
                ),
            )
            conn.execute(
                "INSERT INTO vec_chunks (rowid, embedding) VALUES (?, ?)",
                (cur.lastrowid, serialize_f32(emb.tolist())),
            )
            conn.execute(
                "INSERT INTO fts_chunks(rowid, text) VALUES (?, ?)",
                (cur.lastrowid, chunk["text"]),
            )
            stats["chunks"] += 1

        stats["files"] += 1

    conn.commit()
    return stats


def main():
    parser = argparse.ArgumentParser(description="RAG-Index für Verfahrensdokumente")
    parser.add_argument(
        "--verfahren", help="Nur dieses Verfahren indizieren (z.B. 3-f-24-26)"
    )
    parser.add_argument(
        "--reset", action="store_true", help="DB löschen und komplett neu aufbauen"
    )
    args = parser.parse_args()

    verfahren_root = find_verfahren_root(Path.cwd())
    db = db_path_for(verfahren_root)

    if args.reset and db.exists():
        db.unlink()
        print("✓ DB gelöscht")

    print(f"→ Lade Embedding-Modell {MODEL_NAME} …")
    model = SentenceTransformer(MODEL_NAME)

    conn = init_db(db)

    # Prüfe ob FTS5-Tabelle vorhanden (ältere DBs ohne Hybrid-Suche)
    has_fts = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='fts_chunks'"
    ).fetchone()
    if not has_fts and not args.reset:
        print("⚠ FTS5-Index fehlt. Mit --reset neu aufbauen für Hybrid-Suche.")


    # Verfahren ermitteln
    if args.verfahren:
        dirs = [verfahren_root / args.verfahren]
        if not dirs[0].is_dir():
            sys.exit(f"Fehler: {dirs[0]} existiert nicht.")
    else:
        dirs = sorted(
            [d for d in verfahren_root.iterdir() if d.is_dir() and not d.name.startswith(".")]
        )

    total = {"files": 0, "chunks": 0, "skipped": 0, "verfahren": 0}

    for vdir in dirs:
        name = vdir.name
        print(f"→ Indiziere {name} …")
        stats = index_verfahren(conn, model, vdir, name)
        print(
            f"  {stats['files']} Dateien, {stats['chunks']} Chunks"
            f" ({stats['skipped']} unverändert)"
        )
        total["files"] += stats["files"]
        total["chunks"] += stats["chunks"]
        total["skipped"] += stats["skipped"]
        total["verfahren"] += 1

    conn.close()
    print(
        f"\n✓ Indiziert: {total['files']} Dateien, {total['chunks']} Chunks"
        f" in {total['verfahren']} Verfahren"
        f" ({total['skipped']} übersprungen)"
    )
    print(f"  DB: {db}")


if __name__ == "__main__":
    main()
