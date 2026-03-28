---
name: rag-index
description: "RAG-Index aktualisieren | Optionen: --verfahren, --reset"
---

Führe das Skript `skills/familienrecht/scripts/rag-index.py` aus dem `.venv` aus:

```bash
.venv/bin/python skills/familienrecht/scripts/rag-index.py $ARGUMENTS
```

Optionale Argumente (aus $ARGUMENTS):
- `--verfahren 3-f-24-26` — nur ein Verfahren indizieren
- `--reset` — DB löschen und komplett neu aufbauen

Zeige die Zusammenfassung dem Nutzer an.
