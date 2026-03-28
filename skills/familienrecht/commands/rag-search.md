---
description: "Semantische Suche | Optionen: --verfahren, --doc-type, --top"
---

Ermittle den Git-Root und führe das Skript aus:

```bash
PROJ=$(git rev-parse --show-toplevel) && "$PROJ/.venv/bin/python" "$PROJ/skills/familienrecht/scripts/rag-search.py" $ARGUMENTS
```

$ARGUMENTS enthält die Suchanfrage und optionale Filter:
- `"Suchanfrage"` — natürlichsprachliche Suche
- `--verfahren 3-f-24-26` — nur in einem Verfahren suchen
- `--doc-type beleg` — nur Belege durchsuchen (beleg, sachverhalt, gegenseite, erwiderung, vorbereitung, kontext)
- `--top 10` — mehr Treffer anzeigen (default: 5)

Zeige die Ergebnisse dem Nutzer formatiert an.
