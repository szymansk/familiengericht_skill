---
name: familienrecht
description: "Skill für die Erstellung und Prüfung von familienrechtlichen Schriftsätzen — Erwiderungen, Anträge, Stellungnahmen — in Verfahren zu Umgang und Sorgerecht. Erstellt auf Anfrage druckbare Gesprächs-Onepager zur Vorbereitung auf Termine mit Verfahrensbeistand, Jugendamt, Anwältin oder Gericht. Immer verwenden wenn der Nutzer über ein Familiengericht, Jugendamt, Verfahrensbeistand, Kindesmutter oder -vater spricht, Betreuungszeiten oder Wechselmodell erwähnt, einen Termin oder ein Gespräch mit Verfahrensbeteiligten erwähnt, oder wenn er Texte für ein Familiengerichtsverfahren schreiben, prüfen oder vorbereiten möchte. Auch bei emotionalen Schilderungen rund um Trennung und Kind — dieser Skill begleitet den Nutzer als strategischer Partner, nicht nur als Schreibwerkzeug. Trigger-Begriffe: Erwiderung, Antrag, Umgang, Sorgerecht, Wechselmodell, Familiengericht, Verfahrensbeistand, Kindeswohl, Betreuungsmodell, Elternvereinbarung, Cochemer Modell, Jugendamt, Kindsvater, Kindsmutter, Training, Verhandlung üben, Onepager, Gespräch vorbereiten, Termin mit."
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

### Modus 3: Kontext-Scan

Scannt das gesamte aktive Verfahren und baut `kontext.md` von Grund auf neu. Läuft als **Subagent im Hintergrund** — der Hauptkontext bleibt sauber, der Nutzer kann währenddessen weiterarbeiten.

**Aktivierung:** „Kontext aufbauen", „Kontext-Scan", „kontext.md neu erstellen"

**Ausführung:** Subagent spawnen mit den Instruktionen aus `agents/kontext-scan.md`. Übergeben:
- Absoluter Pfad zum Verfahrensordner (z.B. `/Users/…/verfahren/3-f-24-26`)

Der Agent liest alle Quelldateien, schreibt `kontext.md` neu und committet. Er meldet am Ende welche Dateien gelesen wurden, was fehlte und welche Lücken aufgefallen sind.

### Modus 4: Gesprächs-Onepager

Erstellt einen druckbaren Vorbereitungszettel für ein konkretes Gespräch — **maximal 1–2 Seiten**, nie mehr. Der Onepager ist kein Duplikat anderer Dokumente, sondern ein eigenständiges Destillat: nur Kernbotschaften, Verhaltens-Do's&Don'ts und Gedächtnisanker. Was auf mehr als zwei Seiten nicht passt, gehört nicht rein.

**Explizite Aktivierung:** „Erstelle einen Onepager für das Gespräch mit [Name]", „Onepager [Name]"

**Proaktiver Hinweis:** Sobald der Nutzer einen bevorstehenden Termin mit Verfahrensbeistand, Jugendamt, Anwältin oder Gericht erwähnt (auch indirekt: „ich treffe morgen den VB", „nächste Woche JA-Gespräch"), einmalig anbieten:
> „Soll ich dir einen Onepager für das Gespräch vorbereiten? Der passt auf eine Seite und enthält deine Kernbotschaften, konkrete Beispiele und die wichtigsten Do's & Don'ts."

Ablehnung wird respektiert und nicht wiederholt.

**Dateiname:** `vorbereitung/[name]-gespraech-onepager.md` — `[name]` = Nachname des Gesprächspartners in Kleinbuchstaben

**Erzeugungsprozess:**
1. Falls nicht bekannt fragen: Gesprächspartner (Name, Rolle), Datum des Termins, Name des Nutzers
2. `sachverhalt/fakten.md` lesen → Kernargumente, Belege-Inventar, Parteien
3. `sachverhalt/entscheidungen.md` lesen → strategische Leitlinie
4. `sachverhalt/timeline.md` lesen → konkrete Ereignisse für Gedächtnisanker
5. `erwiderung/erwiderung.md` lesen → Hauptargumente
6. `erwiderung/nur-muendlich.md` lesen → mündliche Punkte, Redevorschläge
7. **Wenn Gesprächspartner = Verfahrensbeistand oder Jugendamt:** `references/verfahrensbeistand.md` lesen — enthält die 20 typischen Fragen, Bewertungslogik und Do's/Don'ts speziell für diesen Gesprächstyp
8. Template `assets/verfahren/vorbereitung/gespraech-onepager.md` lesen — Struktur und YAML-Header übernehmen, Platzhalter mit Verfahrensdaten befüllen
9. Fertigen Onepager in `vorbereitung/[name]-gespraech-onepager.md` ablegen
10. Committen: `Onepager: [Name]-Gespräch [Datum]`

→ **Format-Template:** `assets/verfahren/vorbereitung/gespraech-onepager.md` (YAML-Frontmatter für Pandoc/XeLaTeX bereits enthalten — 10pt, engere Ränder für Druckoptimierung)

**Inhaltliche Leitlinien:**
- **Strenge Längenbegrenzung: 1 Seite, maximal 2.** Wer einen Onepager mit 4 Seiten in ein Gespräch mitnimmt, hat keinen Onepager — er hat ein Dokument. Lieber einen Punkt weglassen als die Seite zu sprengen.
- **Kein Kopieren aus anderen Dokumenten** — der Onepager ist kein Auszug aus der Erwiderung, kein Schriftsatz-Duplikat. Er destilliert Haltung und Verhalten, nicht Sachvortrag.
- Konkret und persönlich — echte Namen, echte Ereignisse, echte Daten; keine Allgemeinplätze
- Kernbotschaften sind **Haltungen**, nicht Argumente — was der Nutzer ausstrahlen soll, nicht was er beweisen will
- Do's & Don'ts mit Beispielen aus dem konkreten Verfahren, nicht generisch
- Gedächtnisanker = fertige Sätze, die der Nutzer wörtlich sagen kann, wenn das Thema aufkommt
- Abschlusssatz personalisiert: Kind beim Namen nennen, Kernziel des Verfahrens in einem Satz

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

**2. Kontext laden:** `kontext.md` im Verfahrensordner lesen — gibt sofort den vollständigen Überblick. Existiert sie noch nicht (neues Verfahren oder noch nie ein Kontext-Scan gelaufen), Kontext-Scan automatisch starten.

Danach folgende Dateien für Detailarbeit verfügbar halten (bei Bedarf lesen, nicht alle automatisch laden):

| Datei | Zweck |
|-------|-------|
| `sachverhalt/fakten.md` | Bekannte Fakten, Betreuungsmodell, Parteien (Detail) |
| `sachverhalt/entscheidungen.md` | Strategische Entscheidungen — gilt sitzungsübergreifend |
| `sachverhalt/timeline.md` | Chronologie der Ereignisse (Detail) |
| `sachverhalt/notizen.md` | Unverarbeitete Notizen und verworfene Punkte |
| `erwiderung/erwiderung.md` | Aktueller Entwurfsstand |
| `erwiderung/anlagen.md` | Verwendete Belege und Anlagen |

**3. Belege auf Nomenklatur prüfen:** Alle Unterordner von `belege/` scannen. Dateien die nicht dem Format `YYYYMMDD_[AZ]_[VON]_[AN]_[Beschreibung].[ext]` entsprechen, werden gebündelt als Tabelle zur Umbenennung vorgelegt — nie Datei für Datei. Nach Bestätigung umbenennen und committen. `.gitkeep` und versteckte Dateien überspringen.

→ Nomenklatur-Details und Erkennungsregeln: `references/dateinamenskonvention.md`

---

## Dateistruktur-Regeln

### OCR-Pflicht via LLM-Vision

> ⚠️ **KRITISCHE REGEL — Gerichtsfestigkeit**
>
> Beim Import von bildbasierten Dokumenten (Scans, Fotos, gescannte PDFs) **muss** OCR ausschließlich über die **Vision-Fähigkeit des aktuell aktiven LLM** erfolgen. Das bedeutet: das Read-Tool direkt auf die Bilddatei/PDF anwenden, damit das Modell den Inhalt visuell transkribiert.
>
> **Verboten:** Externe OCR-Tools, MarkItDown auf Scans, automatische Textextraktion aus Bildern ohne LLM-Verifikation.
>
> **Begründung:** OCR-Fehler in Gerichtsdokumenten (falsches Datum, falsch transkribierter Name, fehlendes Wort) können das Verfahren entscheidend beeinflussen. Nur die LLM-Vision gewährleistet, dass Unklarheiten (Handschrift, schlechte Scanqualität, Durchstreichungen) erkannt und dem Nutzer gemeldet werden.
>
> Nach jeder Transkription: auffällige oder unsichere Stellen explizit benennen.

### `belege/` ist unveränderlich

Der Ordner `belege/` und **alle seine Unterordner** (`belege/dokumente/`, `belege/emails/`, `belege/whatsapp/`, `belege/voicenotes/`, `belege/originale/`, …) sind **Single Source of Truth** für importierte Dokumente. Der Skill darf dort **niemals eigenständig etwas verändern** — keine inhaltlichen Anpassungen, keine Ergänzungen, keine Umstrukturierungen, keine neuen Dateien außerhalb des Import-Prozesses.

> **Einzige Ausnahmen:**
> 1. Umbenennung nach Nomenklatur unmittelbar beim Import (Schritt 1 unten) und das initiale Ablegen der konvertierten MD-Datei (Schritt 4).
> 2. Der Nutzer nimmt die Änderung selbst vor — dann ist keine Rückfrage nötig.
> 3. Der Nutzer fordert explizit einen **wiederholten Import** (z.B. „dieses Dokument nochmal importieren", „Import wiederholen") — dann gilt das Verfahren unten.

**Wiederholter Import — Pflichtablauf:**

Bevor eine bestehende Datei in `belege/` überschrieben oder verändert wird, **muss** der Skill:

1. Den aktuellen Inhalt der Zieldatei lesen
2. Den neuen Inhalt (aus der Quelldatei) ermitteln
3. Die Unterschiede als übersichtliche Tabelle oder Diff darstellen:

   ```
   VORHER  │ NACHHER
   ────────┼────────
   [alter Text / Wert]  │  [neuer Text / Wert]
   ```

4. Explizit fragen:
   > „Die Datei `belege/…` existiert bereits. Ich habe die Unterschiede oben dargestellt. Soll ich sie mit dem neuen Import überschreiben?"

5. Nur bei ausdrücklicher Bestätigung fortfahren — bei Ablehnung nichts verändern.

### Wo neue Dateien abgelegt werden

| Inhalt | Ablageort |
|--------|-----------|
| Importierte Originalbelege (PDF, DOCX, …) | `belege/originale/` |
| Konvertierte MD-Versionen importierter Dokumente | `belege/dokumente/`, `belege/emails/`, … |
| Vom Skill **generierte** Anlage-MDs (Zusammenfassungen, Deckblätter, synthetisierte Dokumente) | **Hauptdokument-Ordner** (`erwiderung/`, `antrag/`, …) |
| Anlagenverzeichnis | `erwiderung/anlagen.md` (oder entsprechender Hauptdokument-Ordner) |

Wenn der Nutzer anweist, eine MD-Datei für einen Anhang zu erzeugen (z. B. Reisekostenübersicht, Aufstellung, Protokollzusammenfassung), wird diese **im selben Ordner wie das Hauptdokument** abgelegt — niemals in `belege/`.

---

## Neue Dokumente importieren

Wenn eine DOCX-, PDF- oder andere Datei eingebracht wird, läuft der Import als **Subagent** — der vollständige Ablauf (Umbenennen, OCR, MD ablegen, anlagen.md, kontext.md, commit) läuft isoliert und meldet am Ende Ergebnis + OCR-Unsicherheiten.

**Ausführung:** Subagent spawnen mit den Instruktionen aus `agents/dokument-import.md`. Übergeben:
- `DATEI`: Absoluter Pfad zur zu importierenden Datei
- `VERFAHREN`: Absoluter Pfad zum Verfahrensordner
- Bekannte Metadaten (Datum, Absender, Empfänger) — wenn vorhanden, mitgeben; wenn nicht, klärt der Agent selbst nach

Der Agent stoppt eigenständig und fragt, wenn Metadaten unklar sind oder die Einreichungsart nicht erkennbar ist. Bei OCR-Unsicherheiten (Handschrift, schlechte Qualität) meldet er diese explizit.

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

## Kontext-Datei pflegen

`kontext.md` im Verfahrensordner ist die **zentrale Übersichtsdatei** — immer als erstes geladen, immer aktuell halten.

**Wann `kontext.md` aktualisieren** (nach Commit der Quelldatei, vor eigenem Commit):

| Auslöser | Betroffene Felder in kontext.md |
|----------|--------------------------------|
| Import neues Dokument | Anlagen-Übersicht, ggf. Behauptungen Gegenseite |
| Änderung an `fakten.md` | Parteien, Betreuungsmodell, Kernargumente, Behauptungen |
| Änderung an `entscheidungen.md` | Strategie-Entscheidungen |
| Änderung an `timeline.md` | Timeline-Highlights |
| Änderung an `erwiderung.md` | Stand Schriftsatz |
| Änderung an `anlagen.md` | Anlagen-Übersicht |
| Neuer Termin / Frist bekannt | Verfahrensdaten → Nächster Termin |

**Format:** Kompakt, keine Fließtexte — nur Tabellen, kurze Stichpunkte, Nummerierungen. `kontext.md` darf nie länger werden als nötig, um vollständig zu sein.

**Zuletzt-aktualisiert-Zeile** im Header (`> Zuletzt aktualisiert: …`) bei jeder Änderung auf aktuelles Datum setzen.

**Commit-Nachricht:** `Kontext: [Veranlassung]` — z.B. `Kontext: Anlage B3 ergänzt`, `Kontext: Strategie-Entscheidung Wechselmodell aktualisiert`

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
11. **`kontext.md` nach jeder inhaltlichen Änderung aktualisieren** — sie muss immer den tatsächlichen Stand widerspiegeln; veraltete kontext.md ist wertlos.
12. **`belege/` niemals eigenständig verändern** — nur bei explizitem wiederholtem Import durch den Nutzer, und nur nach Diff-Anzeige und ausdrücklicher Bestätigung.
13. **Gesprächs-Onepager proaktiv anbieten** — sobald ein Termin mit VB, JA, Anwältin oder Gericht erwähnt wird, einmalig anbieten; nicht wiederholen wenn abgelehnt.
