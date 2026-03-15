---
name: familienrecht
description: "Skill für die Erstellung von Schriftsätzen im Familienrecht (Umgang, Sorgerecht). Verwende diesen Skill immer, wenn der Nutzer Anträge, Erwiderungen, Stellungnahmen oder Vorbereitungen für Verhandlungen im Familienrecht erstellen, prüfen oder überarbeiten möchte. Trigger-Begriffe: Erwiderung, Antrag, Umgang, Sorgerecht, Wechselmodell, Familiengericht, Verfahrensbeistand, Kindeswohl, Betreuungsmodell, Elternvereinbarung, Cochemer Modell. Auch bei allgemeinen Fragen zu familienrechtlichen Schriftsätzen, Verhandlungsvorbereitung oder Anlagengestaltung diesen Skill verwenden."
---

# Familienrecht-Skill für Claude Code

## Leitprinzip: Cochemer Modell

Alle Schriftsätze folgen dem Geist des Cochemer Modells nach Jürgen Rudolph:
→ Lies `references/cochemer-modell.md` vor dem Schreiben jedes Schriftsatzes.

## Betreuungsmodelle

→ Lies `references/betreuungsmodelle.md` bei der Sachverhaltsaufnahme (Phase 1).
Erkläre dem Nutzer die Modelle verständlich und stelle die dort definierten Fragen,
um das aktuelle und das angestrebte Modell zu erfassen.

## Setup (einmalig)

Beim ersten Aufruf prüfen und ausführen:

```bash
pip install markitdown --quiet
python -c "from markitdown import MarkItDown; print('✅ MarkItDown bereit')"
```

## Neues Verfahren anlegen

```bash
./setup-verfahren.sh "2 F 67/68"
```

Das Script legt `verfahren/2-f-67-68/` mit der vollständigen Ordnerstruktur an und befüllt alle Templates mit dem Aktenzeichen. Danach direkt mit Phase 1 beginnen.

## Projektstruktur

Jedes Verfahren liegt in einem eigenen Ordner:

```
verfahren/{az-kurz}/
├── sachverhalt/
│   ├── fakten.md           # Gesammelte Fakten (wird iterativ ergänzt)
│   └── timeline.md         # Chronologie der Ereignisse
├── gegenseite/
│   ├── antrag.md           # Antrag der Gegenseite (Markdown)
│   └── protokoll-km.md     # Protokoll/Anlagen der Gegenseite
├── belege/
│   ├── whatsapp/           # Chat-Exports als .md
│   ├── emails/             # E-Mails als .md
│   ├── voicenotes/         # Transkripte von Sprachnachrichten
│   └── dokumente/          # Sonstige Belege als .md
├── erwiderung/
│   ├── erwiderung.md       # Haupttext der Erwiderung
│   ├── anlagen.md          # Anlagenverzeichnis mit Beschreibung
│   └── nur-muendlich.md    # Punkte nur für die mündliche Verhandlung
├── vorbereitung/
│   └── verhandlung.md      # Persönliche Vorbereitung + Redevorschläge
└── output/                 # Generierte DOCX/PDF (git-ignored)
```

## Neue Dokumente importieren

Wenn der Nutzer eine DOCX-, PDF- oder andere Datei einbringt:

```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("datei.docx")
# result.text_content enthält den Markdown-Text
```

Speichere das Ergebnis im passenden Unterordner als `.md`.

## 5-Phasen-Workflow

→ Lies `references/workflow.md` für den vollständigen Ablauf.

### Kurzübersicht:

**Phase 1 — Sachverhaltsaufnahme**
- Fragen stellen, Fakten sammeln
- Bei Erwiderungen: Antrag der Gegenseite analysieren
- `sachverhalt/fakten.md` und `sachverhalt/timeline.md` befüllen

**Phase 2 — Entwurf**
- Erwiderung/Antrag in Markdown schreiben
- `erwiderung/erwiderung.md` erstellen
- Anlagen in `erwiderung/anlagen.md` verzeichnen

**Phase 3 — Prüfung**
→ Lies `references/pruefschema.md`
- Jeden Abschnitt aus Sicht aller Verfahrensbeteiligten prüfen
- Prüfergebnis dem Nutzer als Übersicht vorlegen
- **Neue Anekdoten/Fakten immer zuerst auf Risiken prüfen, bevor sie eingebaut werden**

**Phase 4 — Vertiefung**
- Offene Fragen an den Nutzer
- Neue Fakten einarbeiten
- Zurück zu Phase 3 wenn nötig

**Phase 5 — Finalisierung**
→ Lies `references/formatierung.md`
- DOCX/PDF generieren → `output/`
- `vorbereitung/verhandlung.md` erstellen
- Anlagen als DOCX generieren

## Arbeitsformat: Markdown-First

- **Schreibe immer zuerst in Markdown** — der Nutzer arbeitet in VS Code mit Preview
- **DOCX nur als Output** — generiert in Phase 5 oder auf Anfrage
- **Versionierung über Git** — der Skill committed nach jeder Dateiänderung, der Nutzer committed nicht selbst
- Vermeide es, bei jeder kleinen Änderung ein neues DOCX zu generieren

## Git-Versionierung (automatisch)

Nach **jeder Änderung an Verfahrensdateien** (Sachverhalt, Erwiderung, Anlagen, Belege usw.)
führt der Skill automatisch einen Commit durch. Der Nutzer muss das nicht selbst tun.

### Setup-Prüfung beim ersten Aufruf eines Verfahrens:

```bash
# 1. Git installiert?
if ! command -v git &>/dev/null; then
  brew install git        # macOS
  # alternativ: apt install git / winget install git
fi

# 2. Lokales Repo vorhanden?
if [ ! -d ".git" ]; then
  git init
  git add .
  git commit -m "Initial: Verfahren angelegt"
fi
```

### Commit-Regeln:

- **Wann:** nach jeder gespeicherten Änderung an einer Verfahrensdatei
- **Nachricht:** kurz und beschreibend, z.B.:
  - `Sachverhalt: Betreuungsrealität ergänzt`
  - `Erwiderung: Abschnitt III überarbeitet`
  - `Belege: WhatsApp-Export importiert`
  - `Anlagen: B4 hinzugefügt`
- **Nie committen:** `output/*.docx`, `output/*.pdf` (via `.gitignore` ausgeschlossen)

## Wichtige Regeln

1. **Immer den Skill lesen** bevor du schreibst: `references/cochemer-modell.md`
2. **Neue Fakten zuerst prüfen** — Risiken besprechen, erst nach Freigabe einbauen
3. **Punkte nur für die mündliche Verhandlung** in `nur-muendlich.md` — nicht im Schriftsatz
4. **Querverweise** bei Strukturänderungen immer aktualisieren
5. **Eidesstattliche Versicherung** nie in Schriftsätze aufnehmen — unüblich am Familiengericht
6. **Kostenantrag** nur wenn vom Nutzer ausdrücklich gewünscht — wirkt konfrontativ
7. **„Weiterer Sachvortrag bleibt vorbehalten"** immer vor der Unterschrift
8. **Nach jeder Dateiänderung committen** — der Nutzer committed nie selbst
