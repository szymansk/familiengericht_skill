# Familienrecht-Skill für Claude Code

Skill zur Erstellung von Schriftsätzen im Familienrecht (Umgang, Sorgerecht) nach dem Cochemer Modell — mit integriertem Trainingsmodus zur Verhandlungsvorbereitung.

---

## Installation in Claude Code

Es gibt zwei Wege, den Skill zu installieren: über den **Marketplace** (empfohlen, kein `git clone` nötig) oder **manuell** per Symlink.

---

### Option A: Über den Marketplace (empfohlen)

#### Schritt 1: Marketplace hinzufügen

In Claude Code:

```
/plugin marketplace add szymansk/familiengericht_skill
```

#### Schritt 2: Plugin installieren

```
/plugin install familienrecht@familienrecht-marketplace
```

Oder interaktiv:
1. `/plugin` aufrufen
2. Tab **Discover** öffnen
3. `familienrecht` auswählen und Installationsbereich wählen (user / project)

#### Schritt 3: Abhängigkeiten installieren

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install markitdown --quiet
```

---

### Option B: Manuell per Symlink

### Schritt 1: Repository klonen

```bash
git clone https://github.com/szymansk/familiengericht_skill.git
cd familiengericht_skill
```

### Schritt 2: Skill in Claude Code registrieren

Claude Code lädt Skills aus dem Verzeichnis `~/.claude/skills/`. Den Skill-Ordner dort verlinken oder kopieren:

```bash
# Option A: Symlink (empfohlen — bleibt automatisch aktuell)
mkdir -p ~/.claude/skills
ln -s "$(pwd)" ~/.claude/skills/familienrecht

# Option B: Kopieren
cp -r . ~/.claude/skills/familienrecht
```

### Schritt 3: Abhängigkeiten installieren

```bash
# MarkItDown für den DOCX/PDF-Import
pip install markitdown --quiet

# Test
python -c "from markitdown import MarkItDown; print('MarkItDown bereit')"
```

### Schritt 4: Skill in Claude Code verwenden

Starte Claude Code in dem Verzeichnis, in dem du deine Verfahren ablegen möchtest:

```bash
cd ~/Dokumente/familienrecht   # oder ein anderer Arbeitsordner
claude
```

Claude Code erkennt den Skill automatisch anhand der Trigger-Begriffe in `SKILL.md`:
**Erwiderung, Antrag, Umgang, Sorgerecht, Wechselmodell, Familiengericht, Kindeswohl** u.a.

---

## Erstes Verfahren anlegen

```bash
# Setup-Script aus dem Skill-Verzeichnis ausführen:
~/.claude/skills/familienrecht/setup-verfahren.sh "4 F 42/25"
```

Oder wenn du direkt im Skill-Verzeichnis arbeitest:

```bash
./setup-verfahren.sh "4 F 42/25"
```

Das Script legt `verfahren/4-f-42-25/` mit der vollständigen Ordnerstruktur an
und befüllt alle Templates mit dem Aktenzeichen.

---

## Skill aktualisieren

```bash
cd ~/.claude/skills/familienrecht
git pull
```

---

## Modi

| Modus | Aktivierung | Zweck |
|-------|-------------|-------|
| **Schreibmodus** | automatisch | Anträge, Erwiderungen, Stellungnahmen erstellen und prüfen |
| **Trainingsmodus** | „Training" eingeben | Verhandlung üben — Skill spielt Richterin, Gegenanwältin, Verfahrensbeistand und Jugendamt |

---

## Struktur

```
familienrecht-skill/
├── SKILL.md                        # Skill-Definition (von Claude Code gelesen)
├── setup-verfahren.sh              # Script für neue Verfahren
├── references/
│   ├── cochemer-modell.md          # Ton und Haltung
│   ├── workflow.md                 # 5-Phasen-Prozess
│   ├── pruefschema.md              # Prüfung aus Sicht aller Beteiligten
│   ├── formatierung.md             # DOCX-Standards
│   ├── betreuungsmodelle.md        # Erklärung aller Betreuungsmodelle
│   ├── verhaltensregeln.md         # Dos/Don'ts für Gericht, Jugendamt, Verfahrensbeistand
│   └── trainingsmodus.md           # Regeln und Rollen für den Trainingsmodus
├── templates/
│   └── verfahren/                  # Vorlage für neue Verfahren
└── verfahren/
    └── {az-kurz}/                  # Jedes Verfahren als eigener Ordner
```

---

## 5-Phasen-Workflow

1. **Sachverhaltsaufnahme** — Fakten sammeln, Betreuungsmodell erfassen, Gegenseite analysieren
2. **Entwurf** — Schriftsatz in Markdown nach dem Cochemer-Prinzip
3. **Prüfung** — Aus Sicht von Richterin, Gegenanwalt, Verfahrensbeistand und Gutachter
4. **Vertiefung** — Offene Fragen klären, neue Fakten einarbeiten
5. **Finalisierung** — DOCX exportieren, Verhandlung vorbereiten
