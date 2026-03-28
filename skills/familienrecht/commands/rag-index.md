---
description: "RAG-Index aktualisieren | Optionen: --verfahren, --reset"
---

Ermittle den Git-Root und führe das Skript aus:

```bash
PROJ=$(git rev-parse --show-toplevel) && "$PROJ/.venv/bin/python" "$PROJ/skills/familienrecht/scripts/rag-index.py" $ARGUMENTS
```

Optionale Argumente (aus $ARGUMENTS):
- `--verfahren 3-f-24-26` — nur ein Verfahren indizieren
- `--reset` — DB löschen und komplett neu aufbauen

Zeige die Zusammenfassung dem Nutzer an.
