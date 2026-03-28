---
description: "RAG-Index Status — Verfahren, Dateien, Chunks, DB-Größe"
---

Ermittle den Git-Root und führe das Skript aus:

```bash
PROJ=$(git rev-parse --show-toplevel) && "$PROJ/.venv/bin/python" "$PROJ/skills/familienrecht/scripts/rag-status.py"
```

Zeige die Ausgabe dem Nutzer an.
