---
description: Semantische Suche über alle Verfahrens-Dokumente
---

Führe `skills/familienrecht/scripts/rag-search.py` aus dem `.venv` aus:

```bash
.venv/bin/python skills/familienrecht/scripts/rag-search.py $ARGUMENTS
```

$ARGUMENTS enthält die Suchanfrage und optionale Filter:
- `"Suchanfrage"` — natürlichsprachliche Suche
- `--verfahren 3-f-24-26` — nur in einem Verfahren suchen
- `--doc-type beleg` — nur Belege durchsuchen (beleg, sachverhalt, gegenseite, erwiderung, vorbereitung, kontext)
- `--top 10` — mehr Treffer anzeigen (default: 5)

Zeige die Ergebnisse dem Nutzer formatiert an.
