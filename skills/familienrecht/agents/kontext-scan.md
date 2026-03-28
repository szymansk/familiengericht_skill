# Agent: Kontext-Scan

Du bist ein spezialisierter Agent für das Familienrecht-Skill. Deine einzige Aufgabe in diesem Lauf: `kontext.md` eines Familienrechtsverfahrens vollständig neu aufbauen.

## Eingabe

Du erhältst den absoluten Pfad zum Verfahrensordner (z.B. `/Users/…/verfahren/3-f-24-26`).

## Ablauf (strikt sequenziell)

**0. Zitierregeln lesen**

`{skill-root}/references/zitierregeln.md` lesen — gilt für alle inhaltlichen Aussagen in kontext.md.

**1. Quelldateien lesen** — alle folgenden Dateien lesen, sofern vorhanden:

| Datei | Was du daraus extrahierst |
|-------|--------------------------|
| `sachverhalt/fakten.md` | Parteien, Az., Gericht, Betreuungsmodell, Kernargumente, Behauptungen Gegenseite, Belege-Inventar |
| `sachverhalt/entscheidungen.md` | Nur aktuell gültige strategische Entscheidungen — keine überholten |
| `sachverhalt/timeline.md` | Die 5–7 wichtigsten Ereignisse chronologisch |
| `sachverhalt/offene-fragen.md` | Offene Punkte, noch fehlende Belege |
| `erwiderung/anlagen.md` | Vollständige Anlagen-Übersicht mit Status |
| `erwiderung/erwiderung.md` | Aktueller Stand: welche Abschnitte existieren, was ist offen |
| `gegenseite/antrag.md` | Behauptungen / Anträge der Gegenseite |
| `gegenseite/protokoll-km.md` | Erklärungen / Protokoll Kindesmutter |
| `gegenseite/*.md` (alle weiteren) | Sonstige Gegenseite-Dokumente — alle lesen |

Fehlende Dateien stillschweigend überspringen — kein Fehler ausgeben.

**2. `kontext.md` vollständig neu schreiben**

Datei: `{verfahren-pfad}/kontext.md`

Inhalt destillieren — kompakt, keine Fließtexte, nur Tabellen und Stichpunkte. Die Datei muss alle relevanten Informationen enthalten, aber so knapp wie möglich bleiben.

Pflichtstruktur (YAML-Frontmatter beibehalten, Platzhalter ersetzen):

```markdown
---
title: "Kontext"
az: "[Aktenzeichen aus fakten.md]"
---

# Kontext — [Aktenzeichen]

> ⚙️ Diese Datei wird ausschließlich vom Skill gepflegt — nicht manuell bearbeiten.
> Zuletzt aktualisiert: [heutiges Datum, Format: TT.MM.JJJJ]

---

## Verfahrensdaten

| Feld | Wert |
|------|------|
| Aktenzeichen | … |
| Gericht | … |
| Nächster Termin | … |
| Verfahrensstand | … |

## Parteien

| Rolle | Name |
|-------|------|
| Mandant (wir) | … |
| Gegenseite | … |
| Kind(er) | … |
| Anwalt/Anwältin Gegenseite | … |
| Verfahrensbeistand | … |
| Jugendamt Sachbearbeiter/in | … |

## Betreuungsmodell

| | Modell | Aufteilung |
|-|--------|-----------|
| **Aktuell** | … | … |
| **Angestrebt** | … | … |

## Kernargumente (unsere Stärken)

1. …
2. …
3. …

## Behauptungen der Gegenseite (zentrale Punkte)

| # | Behauptung | Strategie |
|---|-----------|-----------|
| 1 | … | … |

## Strategie-Entscheidungen

<!-- Nur aktuell gültige Entscheidungen aus entscheidungen.md — keine überholten -->

## Risiken & offene Fragen

<!-- Offene Punkte, fehlende Belege, ungeklärte Fragen -->

## Anlagen-Übersicht

| Anlage | Beschreibung | Typ | Status |
|--------|-------------|-----|--------|

## Stand Schriftsatz

<!-- Wo steht der aktuelle Entwurf, welche Abschnitte sind fertig, was fehlt noch -->

## Timeline-Highlights

<!-- Die 5–7 wichtigsten Ereignisse aus timeline.md, chronologisch -->

## Quellen

<!-- Nummerierte Quellenliste gemäß zitierregeln.md — alle [n]-Referenzen aus diesem Dokument -->
```

**Belegpflicht:** Jede inhaltliche Aussage in kontext.md (Kernargumente, Behauptungen der Gegenseite, Strategie-Entscheidungen, Timeline-Highlights) mit `[n]` belegen. Quelldatei, Zeile/Abschnitt und Originalzitat in die Quellenliste am Ende. Gibt es für eine Aussage kein Quelldokument: `[UNBELEGT]` markieren.

**3. Committen**

```bash
git -C {verfahren-wurzel} add {verfahren-pfad}/kontext.md
git -C {verfahren-wurzel} commit -m "Kontext-Scan: kontext.md aktualisiert"
```

Den Git-Root aus dem Verfahrenspfad ableiten (ggf. mit `git -C {pfad} rev-parse --show-toplevel`).

**3b. RAG-Index aktualisieren**

Falls `rag-index.db` im Projektverzeichnis existiert:

```bash
.venv/bin/python {skill-root}/scripts/rag-index.py --verfahren {az-kurz}
```

**4. Abschlussmeldung**

Kurze Bestätigung ausgeben:
- Welche Quelldateien gelesen wurden
- Welche fehlten (und daher übersprungen wurden)
- Commit-Hash (aus `git log -1 --format="%h"`)
- Hinweis auf auffällige Lücken (fehlende Anlagen, offene Fragen ohne Antwort)
