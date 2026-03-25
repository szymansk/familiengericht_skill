# Architektur — Familienrecht-Skill

## Überblick

Der Skill ist ein Claude-Code-Skill (Markdown-basierte Instruktionsdatei) mit einer agentenbasierten Architektur. Die zentrale Steuerdatei `SKILL.md` definiert 6 Modi und delegiert komplexe Aufgaben an spezialisierte Sub-Agenten. Alle persistenten Daten liegen im Verfahrensordner (`verfahren/{az-kurz}/`), der durch `setup-verfahren.sh` erzeugt wird.

---

## Verzeichnisstruktur Skill

```
skills/familienrecht/
├── SKILL.md                        ← Haupt-Instruktionsdatei (Entry Point)
├── agents/
│   ├── dokument-import.md          ← Agent: Einzeldokument importieren
│   ├── kontext-scan.md             ← Agent: kontext.md neu aufbauen
│   ├── aufraeum.md                 ← Agent: Verfahrensordner bereinigen
│   └── fakten-sammler.md           ← Agent: Fakten aus Belegen extrahieren
├── references/                     ← Fachliche Referenzen (read-only)
│   ├── zitierregeln.md             ← Belegpflicht-Format (KRITISCH)
│   ├── cochemer-modell.md          ← Ton & Strategie für Schriftsätze
│   ├── dateinamenskonvention.md    ← YYYYMMDD_AZ_VON_AN_Beschreibung
│   ├── workflow.md                 ← 5-Phasen-Workflow Detail
│   ├── pruefschema.md              ← Schriftsatz-Prüfcheckliste
│   ├── formatierung.md             ← PDF/DOCX-Formatregeln
│   ├── betreuungsmodelle.md        ← Modelle + Gesprächsfragen
│   ├── trainingsmodus.md           ← Rollenbeschreibungen Training
│   ├── verhaltensregeln.md         ← Do's & Don'ts Gericht/JA/VB
│   ├── verfahrensbeistand.md       ← 20 typische VB-Fragen + Logik
│   ├── kalender.md                 ← Kalender-Format & Legende
│   └── loop-sachverhalt.md         ← Loop-Modus Detail
├── assets/verfahren/               ← Templates (niemals direkt bearbeiten)
│   ├── .claudeprompt/CLAUDE.md     ← Auto-Kontext-Template
│   ├── kontext.md
│   ├── sachverhalt/{6 Templates}
│   ├── erwiderung/{3 Templates}
│   └── vorbereitung/{2 Templates}
└── scripts/
    ├── setup-verfahren.sh          ← Neues Verfahren anlegen
    ├── setup.sh                    ← Pandoc/XeLaTeX/Python installieren
    ├── generate-pdf.py             ← MD → PDF (Pandoc + XeLaTeX)
    ├── generate-docx.js            ← MD → DOCX
    └── combine-pdf.py              ← Alle PDFs → einreichung.pdf
```

---

## Verfahrensordner-Struktur (erzeugt von `setup-verfahren.sh`)

```
verfahren/{az-kurz}/
├── .claudeprompt/
│   └── CLAUDE.md                   ← Auto-Kontext (@ alle Docs außer originale/)
├── kontext.md                      ← Zentrale Übersicht (von kontext-scan.md gepflegt)
├── sachverhalt/
│   ├── fakten.md                   ← Fakten, Parteien, Kernargumente (mit [n]-Zitaten)
│   ├── timeline.md                 ← Chronologie der Ereignisse
│   ├── kalender.md                 ← Betreuungskalender (Monatsübersichten)
│   ├── offene-fragen.md            ← Ungeklärte Punkte, fehlende Belege
│   ├── entscheidungen.md           ← Strategische Entscheidungen
│   └── notizen.md                  ← Unverarbeiteter Rohkontext
├── gegenseite/
│   ├── antrag.md                   ← Antrag der Gegenseite (importiert/transkribiert)
│   └── protokoll-km.md             ← Protokoll Kindesmutter
├── belege/
│   ├── originale/                  ← Rohdokumente (PDF, DOCX, Bilder) — unveränderlich
│   ├── dokumente/                  ← Konvertierte MDs: Gerichtsschreiben, Beschlüsse
│   ├── emails/                     ← Konvertierte MDs: E-Mails
│   ├── whatsapp/                   ← Konvertierte MDs: WhatsApp/SMS
│   └── voicenotes/                 ← Transkribierte MDs: Sprachnachrichten
├── erwiderung/
│   ├── erwiderung.md               ← Hauptschriftsatz (→ Gericht)
│   ├── anlagen.md                  ← Anlagenverzeichnis
│   └── nur-muendlich.md            ← Mündliche Punkte & Redevorschläge
├── vorbereitung/
│   ├── verhandlung.md              ← Verhandlungsvorbereitung
│   └── {name}-gespraech-onepager.md ← Onepager pro Gespräch (max. 1–2 Seiten)
└── output/                         ← Generierte PDFs/DOCX (gitignored)
    └── einreichung.pdf             ← Kombiniertes Einreichungsdokument
```

---

## Agenten-Übersicht

| Agent | Datei | Aktivierung | Schreibt in |
|-------|-------|-------------|-------------|
| Dokument-Import | `agents/dokument-import.md` | Neues Dokument übergeben | `belege/`, `anlagen.md`, `kontext.md` |
| Kontext-Scan | `agents/kontext-scan.md` | Modus 3, Auto-Start, Ende Aufräumen | `kontext.md` |
| Verfahren-Aufräumen | `agents/aufraeum.md` | Modus 5 | `belege/`, `sachverhalt/`, `anlagen.md`, spawnt kontext-scan |
| Fakten-Sammler | `agents/fakten-sammler.md` | Modus 6, `/fakten-sammler` | `sachverhalt/fakten.md` |

---

## Aufrufreihenfolge und Abhängigkeiten

### Graph 1 — Modi und Agent-Aufrufe

```mermaid
flowchart TD
    USER([Nutzer]) --> SKILL[SKILL.md\nEntry Point]

    SKILL -->|"Modus 1 (Standard)"| M1[Schreiben & Prüfen\nintern, kein Agent]
    SKILL -->|"Modus 2 — Training"| M2[Trainingsmodus\nintern, kein Agent]
    SKILL -->|"Modus 3 — Kontext-Scan\nauch: Auto-Start ohne kontext.md"| KONTEXT
    SKILL -->|"Dokument-Import\nautomatisch bei Datei-Übergabe"| IMPORT
    SKILL -->|"Modus 4 — Onepager"| M4[Onepager erstellen\nintern, kein Agent]
    SKILL -->|"Modus 5 — Aufräumen"| AUFRAEUMEN
    SKILL -->|"Modus 6 — /fakten-sammler"| FAKTEN

    AUFRAEUMEN -->|"Schritt 11\nSub-Subagent"| KONTEXT

    subgraph Agenten
        IMPORT[dokument-import.md]
        KONTEXT[kontext-scan.md]
        AUFRAEUMEN[aufraeum.md]
        FAKTEN[fakten-sammler.md]
    end
```

### Graph 2 — Datenfluss (Lesen → Schreiben)

```mermaid
flowchart LR
    subgraph Belege ["belege/ (Single Source of Truth)"]
        ORIG[originale/\nPDF, DOCX, Bilder]
        DOCS[dokumente/ emails/\nwhatsapp/ voicenotes/\n.md-Dateien]
    end

    subgraph Sachverhalt ["sachverhalt/"]
        FAKTEN_MD[fakten.md]
        TIMELINE[timeline.md]
        OFFENE[offene-fragen.md]
        ENT[entscheidungen.md]
    end

    subgraph Erwiderung ["erwiderung/"]
        ERWIDE[erwiderung.md\n→ Gericht]
        ANLAGEN[anlagen.md]
        MUENDLICH[nur-muendlich.md]
    end

    KONTEXT_MD[kontext.md]
    VORBEREITUNG[vorbereitung/\nverhandlung.md\nonepager.md]

    %% Import-Agent
    IMPORT_AG[dokument-import.md] -->|"ablegen"| ORIG
    IMPORT_AG -->|"OCR / konvertieren"| DOCS
    IMPORT_AG -->|"eintragen"| ANLAGEN
    IMPORT_AG -->|"aktualisieren"| KONTEXT_MD

    %% Kontext-Scan
    FAKTEN_MD -->|liest| KONTEXT_AG[kontext-scan.md]
    TIMELINE -->|liest| KONTEXT_AG
    ENT -->|liest| KONTEXT_AG
    OFFENE -->|liest| KONTEXT_AG
    ANLAGEN -->|liest| KONTEXT_AG
    KONTEXT_AG -->|"neu schreiben"| KONTEXT_MD

    %% Fakten-Sammler
    DOCS -->|liest| FAKTEN_AG[fakten-sammler.md]
    FAKTEN_AG -->|"extrahiert Fakten\n[n]-Zitate"| FAKTEN_MD

    %% Aufräumen
    AUFRAEUMEN_AG[aufraeum.md] -->|"umbenennen"| ORIG
    AUFRAEUMEN_AG -->|"umbenennen"| DOCS
    AUFRAEUMEN_AG -->|"abgleichen"| ANLAGEN
    AUFRAEUMEN_AG -->|"aktualisieren"| FAKTEN_MD
    AUFRAEUMEN_AG -->|"aktualisieren"| TIMELINE
    AUFRAEUMEN_AG -->|"unbelegte Aussagen melden"| OFFENE
    AUFRAEUMEN_AG -->|"spawnt"| KONTEXT_AG

    %% Schreiben (intern)
    FAKTEN_MD -->|liest| ERWIDE
    ANLAGEN -->|liest| ERWIDE
    MUENDLICH -.->|"nur mündlich\nnie in Schriftsatz"| ERWIDE
```

### Graph 3 — Zitierregeln-Abhängigkeiten

```mermaid
flowchart LR
    ZITIER[references/zitierregeln.md\nKRITISCHE REGEL]

    ZITIER -->|"liest zuerst"| KONTEXT_AG[kontext-scan.md]
    ZITIER -->|"liest zuerst"| IMPORT_AG[dokument-import.md]
    ZITIER -->|"liest zuerst"| FAKTEN_AG[fakten-sammler.md]
    ZITIER -->|"gilt implizit"| SKILL[SKILL.md\nalle Modi]

    subgraph Interne Docs ["Interne Docs — Belegpflicht [n]"]
        direction LR
        A[fakten.md]
        B[timeline.md]
        C[kontext.md]
        D[verhandlung.md]
        E[onepager.md]
        F[nur-muendlich.md]
    end

    subgraph Externe Schreiben ["Externe Schreiben — kein Inline-Zitat"]
        direction LR
        X[erwiderung.md]
        Y[Anträge]
    end

    KONTEXT_AG --> C
    IMPORT_AG --> C
    FAKTEN_AG --> A
```

---

## Kritische Regeln (höchste Priorität)

| Regel | Gilt für | Details |
|-------|---------|---------|
| **Belegpflicht** | Alle internen Docs | `[n]` im Text + Quellenliste am Ende; kein Zitat → `[UNBELEGT]` |
| **OCR via LLM-Vision** | Alle Scans/Bilder | Externes OCR verboten — Read-Tool direkt auf Bilddatei |
| **belege/ unveränderlich** | Alle Modi | Nur Import-Agent und Aufräum-Agent dürfen umbenennen |
| **Kein Redevorschlag in fakten.md** | Modus 1, Fakten-Sammler | Redevorschläge → nur-muendlich.md |
| **Externe Schreiben nur aus belegten Fakten** | Modus 1 | Alles was in erwiderung.md steht, muss in einem internen Doc mit `[n]` stehen |

---

## Startup-Sequenz

```mermaid
sequenceDiagram
    participant N as Nutzer
    participant S as SKILL.md
    participant K as kontext-scan.md

    N->>S: Sitzung starten
    S->>S: verfahren/ scannen
    alt Mehrere Verfahren
        S->>N: Übersicht + Frage welches Verfahren
    end
    S->>S: kontext.md lesen
    alt kontext.md fehlt
        S->>K: Kontext-Scan starten (auto)
        K->>S: kontext.md erzeugt
    end
    S->>S: belege/ auf Nomenklatur prüfen
    alt Nicht-konforme Dateien gefunden
        S->>N: Umbenenntabelle vorlegen
        N->>S: Bestätigung
        S->>S: Umbenennen + Commit
    end
    S->>N: Bereit
```
