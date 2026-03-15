# Dateinamenskonvention für Belege und importierte Dokumente

## Format

```
YYYYMMDD_[AZ]_[VON]_[AN]_[Beschreibung].[ext]
```

Alle Segmente mit Unterstrich `_` getrennt. Innerhalb der Beschreibung Bindestriche `-`.
Keine Leerzeichen, keine Sonderzeichen außer `-` und `_`.

---

## Segmente

### 1. Datum `YYYYMMDD`
- Erstellungsdatum des Dokuments, wenn bekannt
- Andernfalls: Datum des Hinzufügens zum Verfahren
- Beispiel: `20240315`

### 2. Aktenzeichen-Kürzel `[AZ]`
- Aus dem Ordnernamen des Verfahrens abgeleitet
- Beispiel: `verfahren/3-f-24-26/` → `3f2426`
- Kann entfallen wenn das Dokument keinem Verfahren eindeutig zugeordnet ist

### 3. Absender `[VON]`

| Kürzel | Bedeutung |
|--------|-----------|
| `KV`   | Kindsvater |
| `KM`   | Kindsmutter |
| `RA`   | Rechtsanwalt (eigener) |
| `RAG`  | Rechtsanwalt Gegenseite |
| `R`    | Richter / Gericht |
| `VB`   | Verfahrensbeistand |
| `JA`   | Jugendamt |
| `KB`   | Kinderbetreuung (KiTa, Schule, Tagesmutter) |
| `EB`   | Erziehungsberatung / Beratungsstelle |
| `GA`   | Gutachter |
| `SB`   | Sonstiger Beteiligter |

### 4. Empfänger `[AN]`
Gleiche Kürzel wie Absender.
Bei Dokumenten ohne eindeutigen Empfänger (z.B. interner Vermerk): `INT`.

### 5. Beschreibung `[Beschreibung]`
- Kurz, eindeutig, auf Deutsch
- Bindestriche statt Leerzeichen
- Beispiele: `Antrag-Umgangsregelung`, `WhatsApp-Export-Juli`, `Entwicklungsgespraech-KiTa`, `Protokoll-Termin`

### 6. Erweiterung `[ext]`
Original-Erweiterung beibehalten: `.pdf`, `.docx`, `.png`, `.jpg`, `.mp3` usw.
Konvertierte Markdown-Version: gleicher Basisname, Erweiterung `.md`.

---

## Beispiele

| Original | Bedeutung |
|----------|-----------|
| `20240315_3f2426_KM_R_Antrag-Umgangsregelung.pdf` | Antrag der Kindsmutter ans Gericht vom 15.03.2024 |
| `20240315_3f2426_KM_R_Antrag-Umgangsregelung.md` | Konvertierte Version desselben Dokuments |
| `20240401_3f2426_R_KV_Ladung-Termin-12Mai.pdf` | Ladung vom Gericht an den Kindsvater |
| `20240210_3f2426_KV_KM_WhatsApp-Export-Jan-Feb.md` | WhatsApp-Export KV → KM |
| `20240318_3f2426_KB_INT_Entwicklungsgespraech-KiTa.md` | Gesprächsnotiz KiTa, intern |
| `20240120_3f2426_EB_INT_Beratungsprotokoll-Erstgespraech.pdf` | Protokoll Beratungsstelle |
| `20240501_3f2426_GA_R_Gutachten-Bindungsanalyse.pdf` | Gutachten an Gericht |

---

## Verzeichnisstruktur für Belege

```
belege/
├── originale/          ← Originaldateien (PDF, DOCX, Bilder, Audio)
│   └── YYYYMMDD_AZ_VON_AN_Beschreibung.ext
├── whatsapp/           ← Konvertierte WhatsApp-Exporte (.md)
├── emails/             ← Konvertierte E-Mails (.md)
├── voicenotes/         ← Transkripte von Sprachnachrichten (.md)
└── dokumente/          ← Sonstige konvertierte Dokumente (.md)
```

Konvertierte Markdown-Dateien landen im thematischen Unterordner,
behalten aber denselben Basisnamen wie das Original in `originale/`.
So ist jederzeit nachvollziehbar, welche MD-Datei aus welchem Original stammt.

---

## Umbenennung beim Import

Wenn der Nutzer eine Datei einbringt, benennt der Skill sie vor dem Speichern um:

1. Datum ermitteln (Metadaten → Dateiname → heute)
2. Absender und Empfänger erfragen falls nicht eindeutig
3. Beschreibung aus Inhalt oder Dateiname ableiten, mit Nutzer abstimmen
4. Original unter neuem Namen in `belege/originale/` speichern
5. Konvertierung starten, MD-Datei mit gleichem Basisnamen im Unterordner ablegen
6. Beide Pfade in `erwiderung/anlagen.md` eintragen

---

## Wenn das Erstellungsdatum unbekannt ist

Präfix `ca` vor dem Datum: `ca20240301_...`
Oder Datum des Hinzufügens ohne Präfix, mit Notiz in `anlagen.md`.

---

## Erkennung nicht-konformer Dateinamen (Startup-Prüfung)

Eine Datei gilt als **nicht konform**, wenn sie **nicht** diesem Muster entspricht:

```
^\d{8}_[a-z0-9]+-[a-z0-9-]+_[A-Z]+_[A-Z]+_.+\.[a-z0-9]+$
```

Konkret: beginnt nicht mit 8 Ziffern, enthält keine Unterstriche als Trennzeichen,
oder fehlt ein VON/AN-Kürzel aus der Kürzel-Tabelle.

**Ausnahmen — diese Dateien überspringen:**
- `.gitkeep`
- Dateien die mit `.` beginnen
- Dateien in `output/`
- Bereits umbenannte Dateien (Muster erfüllt)

**Datum-Extraktion (Priorität):**
1. Datei-Metadaten (`mtime` / EXIF bei Bildern)
2. Datum im bestehenden Dateinamen (verschiedene Formate erkennen)
3. Heutiges Datum als Fallback

**VON/AN-Erschließung:**
- Aus Verzeichnis: `whatsapp/` → wahrscheinlich KV↔KM
- Aus Dateiname: „Antrag" → KM oder RAG als VON, R als AN
- Aus Inhalt (wenn bereits als .md vorhanden): Briefkopf auswerten
- Sonst: Nutzer fragen
