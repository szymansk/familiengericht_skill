#!/usr/bin/env python3
"""RAG-Status: Übersicht über den RAG-Index."""

import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import sqlite_vec


def find_db(start: Path) -> Path:
    cwd = start.resolve()
    for _ in range(10):
        candidate = cwd / "rag-index.db"
        if candidate.exists():
            return candidate
        cwd = cwd.parent
    sys.exit("rag-index.db nicht gefunden. Zuerst /rag-index ausführen.")


def main():
    db_file = find_db(Path.cwd())
    conn = sqlite3.connect(str(db_file))
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)

    # Statistiken
    total_chunks = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    total_files = conn.execute(
        "SELECT COUNT(DISTINCT verfahren || '/' || source_file) FROM chunks"
    ).fetchone()[0]
    verfahren = conn.execute(
        "SELECT DISTINCT verfahren FROM chunks ORDER BY verfahren"
    ).fetchall()
    db_size = db_file.stat().st_size
    db_mtime = datetime.fromtimestamp(db_file.stat().st_mtime, tz=timezone.utc)

    # Formatieren
    if db_size < 1024 * 1024:
        size_str = f"{db_size / 1024:.1f} KB"
    else:
        size_str = f"{db_size / (1024 * 1024):.1f} MB"

    print(f"RAG-Index: {db_file}")
    print(f"{'─' * 50}")
    print(f"Verfahren:    {len(verfahren)}")
    print(f"Dateien:      {total_files}")
    print(f"Chunks:       {total_chunks}")
    print(f"DB-Größe:     {size_str}")
    print(f"Letztes Update: {db_mtime.strftime('%d.%m.%Y %H:%M')}")

    if verfahren:
        print(f"\n{'─' * 50}")
        print("Details pro Verfahren:\n")
        for (v,) in verfahren:
            v_chunks = conn.execute(
                "SELECT COUNT(*) FROM chunks WHERE verfahren=?", (v,)
            ).fetchone()[0]
            v_files = conn.execute(
                "SELECT COUNT(DISTINCT source_file) FROM chunks WHERE verfahren=?", (v,)
            ).fetchone()[0]
            doc_types = conn.execute(
                "SELECT doc_type, COUNT(*) FROM chunks WHERE verfahren=? GROUP BY doc_type ORDER BY doc_type",
                (v,),
            ).fetchall()
            types_str = ", ".join(f"{dt}:{n}" for dt, n in doc_types)
            print(f"  {v}: {v_files} Dateien, {v_chunks} Chunks ({types_str})")

    conn.close()


if __name__ == "__main__":
    main()
