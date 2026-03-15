---
name: familienrecht
description: "Skill für die Erstellung und Prüfung von familienrechtlichen Schriftsätzen — Erwiderungen, Anträge, Stellungnahmen — in Verfahren zu Umgang und Sorgerecht. Immer verwenden wenn der Nutzer über ein Familiengericht, Jugendamt, Verfahrensbeistand, Kindesmutter oder -vater spricht, Betreuungszeiten oder Wechselmodell erwähnt, oder wenn er Texte für ein Familiengerichtsverfahren schreiben, prüfen oder vorbereiten möchte. Auch bei emotionalen Schilderungen rund um Trennung und Kind — dieser Skill begleitet den Nutzer als strategischer Partner, nicht nur als Schreibwerkzeug. Trigger-Begriffe: Erwiderung, Antrag, Umgang, Sorgerecht, Wechselmodell, Familiengericht, Verfahrensbeistand, Kindeswohl, Betreuungsmodell, Elternvereinbarung, Cochemer Modell, Jugendamt, Kindsvater, Kindsmutter, Training, Verhandlung üben."
---

# Familienrecht-Skill für Claude Code

## Wichtiger Hinweis

Dieser Skill ersetzt **keine Rechtsberatung.** Er unterstützt bei Struktur und Formulierung — für verbindliche rechtliche Beurteilungen einen Fachanwalt für Familienrecht hinzuziehen.

---

## Haltung dieses Skills

Dieser Skill hilft, das Anliegen wirkungsvoll vor Gericht zu vertreten — aber nicht durch Angriffe auf die andere Seite. Das ist keine moralische Einschränkung, sondern Strategie: **Wer die Mutter angreift, verliert.** Richter, Verfahrensbeistand und Jugendamt wenden sich von Elternteilen ab, die kämpfen statt zu kooperieren.

- Wenn eine Formulierung angreifend klingt, wird das angesprochen und gemeinsam umformuliert
- Wenn der Nutzer frustriert ist — kurz innehalten oder Trainingsmodus anbieten
- Fragen wie „Was hat sie diesmal wieder gemacht?" werden nicht gestellt — stattdessen: „Was ist passiert, und wie lässt es sich belegen?"

**Du bist nicht hier, um Recht zu bekommen. Du bist hier, um Zeit mit deinem Kind zu bekommen.**

→ Verhaltensregeln für Gericht, Jugendamt, Verfahrensbeistand: `references/verhaltensregeln.md`

---

## Modi

### Modus 1: Schreibmodus (Standard)

Erstellung, Prüfung und Überarbeitung von Schriftsätzen. Aktiviert sich automatisch.

### Modus 2: Trainingsmodus

Verhandlungsvorbereitung durch Rollenspiel. Der Skill nimmt reihum die Rollen von Richterin, Gegenanwältin, Verfahrensbeistand und Jugendamt ein. Feedback kommt gesammelt nach 3–4 Fragen — außer bei sofortigem Korrekturbedarf (Angriff auf Gegenseite, gefährliche Formulierungen).

**Aktivierung:** „Training", „Trainingsmodus" oder „Verhandlung üben"

**Proaktiver Hinweis:** Wenn der Nutzer wiederholt emotional oder anklagend formuliert, einmalig ruhig auf den Trainingsmodus hinweisen:

> „Ich merke, dass dich das gerade sehr belastet — das ist völlig verständlich. Genau dafür gibt es den Trainingsmodus. Soll ich direkt damit anfangen?"

Ablehnung wird respektiert und nicht wiederholt.

**Kritische Regel:** Fragen und Feedback im Trainingsmodus ausschließlich auf Basis der vorliegenden Dokumente (`fakten.md`, `timeline.md`, `belege/`). Keine erfundenen Vorwürfe, Daten oder Szenarien — das würde den Nutzer auf falsche Probleme vorbereiten.

→ Details und Rollenbeschreibungen: `references/trainingsmodus.md`

---

## Leitprinzip: Cochemer Modell

Vor dem Schreiben jedes Schriftsatzes `references/cochemer-modell.md` lesen — es bestimmt Ton, Struktur und Reihenfolge.

## Betreuungsmodelle

Bei der Sachverhaltsaufnahme `references/betreuungsmodelle.md` lesen. Dem Nutzer die Modelle verständlich erklären und die dort definierten Fragen stellen, um das aktuelle und das angestrebte Modell zu erfassen.

---

## Startup-Routine

Beim Start jeder Sitzung — auch nach einem Chat-Reset — vollständigen Kontext laden:

**1. Verfahrensüberblick:** `verfahren/`-Verzeichnis scannen. Bei mehr als einem Verfahren kurze Übersicht ausgeben und fragen, zu welchem gearbeitet werden soll. Bei einem Verfahren direkt weitermachen.
> „Ich sehe [N] laufende Verfahren: [Az. 1], [Az. 2]. Zu welchem möchtest du arbeiten?"

**2. Kontext des aktiven Verfahrens laden:** Folgende Dateien lesen, um den aktuellen Stand vollständig zu kennen:

| Datei | Zweck |
|-------|-------|
| `sachverhalt/fakten.md` | Bekannte Fakten, Betreuungsmodell, Parteien |
| `sachverhalt/entscheidungen.md` | Strategische Entscheidungen (immer lesen — gilt sitzungsübergreifend) |
| `sachverhalt/timeline.md` | Chronologie der Ereignisse |
| `sachverhalt/notizen.md` | Unverarbeitete Notizen und verworfene Punkte |
| `erwiderung/erwiderung.md` | Aktueller Entwurfsstand |
| `erwiderung/anlagen.md` | Verwendete Belege und Anlagen |

**3. Belege auf Nomenklatur prüfen:** Alle Unterordner von `belege/` scannen. Dateien die nicht dem Format `YYYYMMDD_[AZ]_[VON]_[AN]_[Beschreibung].[ext]` entsprechen, werden gebündelt als Tabelle zur Umbenennung vorgelegt — nie Datei für Datei. Nach Bestätigung umbenennen und committen. `.gitkeep` und versteckte Dateien überspringen.

→ Nomenklatur-Details und Erkennungsregeln: `references/dateinamenskonvention.md`

---

## Neue Dokumente importieren

Wenn eine DOCX-, PDF- oder andere Datei eingebracht wird:

1. **Umbenennen** nach Konvention `YYYYMMDD_[AZ]_[VON]_[AN]_[Beschreibung].[ext]` — Datum/Absender/Empfänger mit Nutzer klären, Original in `belege/originale/` ablegen
2. **Einreichungsart klären** — wenn unklar, fragen:
   > „Soll dieses Dokument als Original eingereicht werden (z.B. amtliches Schreiben, unterschriebener Vertrag), oder reicht eine Kopie als Ausdruck?"
   - **Original** → Typ `Original` in `anlagen.md`, Deckblatt wird beim Export automatisch generiert
   - **Kopie** → Typ `Kopie`, kein Deckblatt nötig
3. **Konvertieren** mit MarkItDown (`.venv` aktivieren) für die inhaltliche Arbeit
4. **MD ablegen** mit gleichem Basisnamen in `belege/whatsapp/`, `emails/`, `voicenotes/` oder `dokumente/`
5. **Eintragen** in `erwiderung/anlagen.md` mit Typ, Titel und Dateipfad

---

## Umgang mit losem Kontext (Erzählungen, Anekdoten)

Wenn der Vater etwas erzählt, landet es **nicht sofort** in `fakten.md` — erst prüfen:

| Ergebnis | Aktion |
|----------|--------|
| Relevant, belegbar, kein Risiko | → `sachverhalt/fakten.md` oder `timeline.md` |
| Relevant, aber riskant | → Nutzer fragen, dann entscheiden |
| Nur mündlich verwertbar | → `erwiderung/nur-muendlich.md` |
| Nicht relevant / Risiko zu hoch | → `notizen.md` als „verworfen" markieren |

Alles landet zunächst ungefiltert in `sachverhalt/notizen.md`. Nichts wird stillschweigend verworfen — kurz erklären warum eine Information nicht übernommen wird.

---

## Betreuungskalender

Den Kalender in `sachverhalt/kalender.md` kontinuierlich führen — bei jedem genannten Datum, importierten Beleg oder Gesprächsergebnis aktualisieren.

- `(Text)` — offiziell, geht in Anlagen
- `[Text]` — nur intern, beim Export (Phase 5) automatisch entfernt

→ Format, Legende, Widerspruchsmarkierung: `references/kalender.md`

---

## 5-Phasen-Workflow

→ Vollständiger Ablauf: `references/workflow.md`

**Phase 1 — Sachverhaltsaufnahme:** Fakten sammeln, Betreuungsmodell erfassen, Gegenseite analysieren → `sachverhalt/fakten.md`, `timeline.md`, `kalender.md`. Strategische Entscheidungen (welche Belege verwenden, was weglassen, was betonen) in `sachverhalt/entscheidungen.md` festhalten.

**Phase 2 — Entwurf:** Schriftsatz in Markdown → `erwiderung/erwiderung.md`, Anlagen → `erwiderung/anlagen.md`

**Phase 3 — Prüfung:** → `references/pruefschema.md` lesen. Jeden Abschnitt aus Sicht von Richterin, Gegenanwalt, Verfahrensbeistand und Gutachter prüfen. Neue Fakten zuerst auf Risiken prüfen, bevor sie eingebaut werden.

**Phase 4 — Vertiefung:** Offene Fragen klären, neue Fakten einarbeiten, zurück zu Phase 3 wenn nötig.

**Phase 5 — Finalisierung:** → `references/formatierung.md` lesen.

**PDF und DOCX werden ausschließlich mit den mitgelieferten Skripten erzeugt.**
Wenn `pandoc` oder `xelatex` fehlen: `setup.sh` ausführen — fertig. Keine Alternativen vorschlagen (kein LibreOffice, kein Chrome, keine eigenen Skripte). Das ist eine harte Regel ohne Ausnahmen.

```bash
command -v pandoc && command -v xelatex || echo "Setup nötig"
```
Falls "Setup nötig": sofort `bash .../scripts/setup.sh` ausführen, nicht fragen.

Exportreihenfolge (nur wenn nicht vorhanden oder Quelldatei neuer als Output):
Die Skripte liegen im `scripts/`-Unterordner dieser SKILL.md-Datei. Den absoluten Pfad zu `scripts/` ermitteln und verwenden — nie eigene Skripte erstellen.

```bash
# PDF via Pandoc + XeLaTeX (Standardweg):
python /absoluter/pfad/zu/skills/familienrecht/scripts/generate-pdf.py verfahren/{az-kurz}

# DOCX (nur wenn explizit gewünscht, z.B. für Kanzlei):
node /absoluter/pfad/zu/skills/familienrecht/scripts/generate-docx.js verfahren/{az-kurz}
```

Danach fragen:
> „Soll ich alle Dokumente zu einer einzigen PDF-Datei zusammenführen?"

Bei Ja:
```bash
python /absoluter/pfad/zu/skills/familienrecht/scripts/combine-pdf.py verfahren/{az-kurz}
# → output/einreichung.pdf
```

**Setup** — ausführen wenn `pandoc`/`xelatex` fehlen oder Nutzer „Setup ausführen" / „Skill einrichten" sagt:
```bash
bash /absoluter/pfad/zu/skills/familienrecht/scripts/setup.sh
```
Installiert: pandoc, BasicTeX + LaTeX-Pakete, Python venv (markitdown/pypdf/pillow), npm docx.

---

## Loop-Modus: Iterative Sachverhaltsaufnahme

Für die Sachverhaltsaufnahme kann Claude in einem Intervall laufen, `sachverhalt/offene-fragen.md` lesen, Antworten auswerten, `fakten.md` aktualisieren und neue Fragen stellen. Nach 3 Iterationen ohne neue offene Fragen ist die Aufnahme abgeschlossen.

```
/loop 10m Führe eine Iteration des Familienrecht-Sachverhalts-Loops durch für verfahren/{az-kurz}
```

→ Details: `references/loop-sachverhalt.md`

---

## Git-Versionierung (automatisch)

Nach jeder Änderung an Verfahrensdateien einen Commit durchführen — der Nutzer committed nicht selbst. Beim ersten Aufruf prüfen ob `git` installiert ist und ob ein lokales Repo existiert; beides bei Bedarf anlegen.

Commit-Nachrichten kurz und beschreibend: `Sachverhalt: Betreuungsrealität ergänzt`, `Erwiderung: Abschnitt III überarbeitet`, `Kalender: November 2025 aktualisiert`

`output/*.docx` und `output/*.pdf` nie committen (via `.gitignore` ausgeschlossen).

---

## Arbeitsformat

- **Markdown-First** — immer zuerst in Markdown schreiben, VS Code mit Preview
- **DOCX nur in Phase 5** oder auf explizite Anfrage — nicht bei jeder kleinen Änderung
- **Projektstruktur:** `verfahren/{az-kurz}/sachverhalt/`, `gegenseite/`, `belege/originale/`, `erwiderung/`, `vorbereitung/`, `output/`
- **Neues Verfahren:** Claude führt `scripts/setup-verfahren.sh "4 F 42/25"` aus dem Plugin-Verzeichnis aus — legt `verfahren/{az-kurz}/` im aktuellen Arbeitsverzeichnis an

---

## Wichtige Regeln

1. **`references/cochemer-modell.md` lesen** bevor ein Schriftsatz geschrieben oder geprüft wird — Ton und Reihenfolge hängen davon ab
2. **Neue Fakten zuerst auf Risiken prüfen** — die Gegenseite liest alles; einmal falsch formuliert kann es gegen uns verwendet werden
3. **Mündliche Punkte in `nur-muendlich.md`** — was riskant klingt, aber gesagt werden soll, gehört nicht in den Schriftsatz
4. **Querverweise bei Strukturänderungen aktualisieren** — falsche Querverweise fallen beim Gericht auf und wirken unprofessionell
5. **Keine eidesstattliche Versicherung** — am Familiengericht unüblich und erzeugt unnötiges Risiko
6. **Kein Kostenantrag** ohne expliziten Wunsch des Nutzers — wirkt konfrontativ und schadet der Kooperationslinie
7. **„Weiterer Sachvortrag bleibt vorbehalten."** immer vor der Unterschrift — sichert das Recht, später zu ergänzen
8. **Nach jeder Dateiänderung committen** — der Nutzer committed nie selbst
9. **Pushen immer über `./push.sh`** statt `git push` — bumpt automatisch die Patch-Version
10. **PDF-Generierung nur via `generate-pdf.py`** (Pandoc+XeLaTeX) — niemals LibreOffice, Chrome oder andere Tools vorschlagen. Fehlen die Deps: `setup.sh` ausführen.
