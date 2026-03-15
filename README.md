# Familienrecht-Skill für Claude Code

Skill zur Erstellung von Schriftsätzen im Familienrecht (Umgang, Sorgerecht) nach dem Cochemer Modell.

## Schnellstart

### 1. Installation
```bash
pip install markitdown
```

### 2. Neues Verfahren anlegen
```bash
cp -r templates/verfahren verfahren/3f2426-gabriel-szymanski
```

### 3. Dokumente importieren
Wirf DOCX/PDF-Dateien in den passenden Unterordner und lasse Claude Code sie konvertieren:
```
# Claude Code konvertiert automatisch mit MarkItDown
```

### 4. Arbeiten
Bearbeite die Markdown-Dateien in VS Code mit Preview. Claude Code kennt den 5-Phasen-Workflow und führt dich durch.

## Struktur

```
familienrecht-skill/
├── SKILL.md                    # Hauptskill (Claude Code liest das zuerst)
├── references/
│   ├── cochemer-modell.md      # Ton und Haltung
│   ├── workflow.md             # 5-Phasen-Prozess
│   ├── pruefschema.md          # Prüfung aus Sicht aller Beteiligten
│   └── formatierung.md         # DOCX-Standards
├── templates/
│   └── verfahren/              # Kopiervorlage für neue Verfahren
└── verfahren/
    └── [az-kurz]/              # Jedes Verfahren als eigener Ordner
```

## Workflow

1. **Sachverhaltsaufnahme** — Fakten sammeln, Gegenseite analysieren
2. **Entwurf** — Schriftsatz in Markdown
3. **Prüfung** — Aus Sicht aller Verfahrensbeteiligten
4. **Vertiefung** — Offene Fragen, neue Fakten
5. **Finalisierung** — DOCX generieren, Vorbereitung Verhandlung
