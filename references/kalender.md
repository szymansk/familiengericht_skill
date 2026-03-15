# Betreuungskalender — Führung und Format

## Zweck

Der Kalender ist das zentrale Gedächtnis des Verfahrens für alle zeitbezogenen Fakten.
Er erfasst das gelebte Betreuungsmodell, Ereignisse und interne Notizen in einem Dokument —
und erlaubt gleichzeitig den Export eines bereinigten, offiziellen Betreuungskalenders.

---

## Datei

`sachverhalt/kalender.md` — wird monatweise geführt, älteste Monate oben.

---

## Legende

### Betreuung (Wer hat das Kind?)

| Kürzel | Bedeutung |
|--------|-----------|
| `Y`    | Kindsvater |
| `M`    | Kindsmutter |
| `—`    | unbekannt / nicht erfasst |

### Zusatzkürzel (werden angehängt)

| Kürzel | Bedeutung |
|--------|-----------|
| `F`    | Gesetzlicher Feiertag |
| `U`    | Urlaub (Elternteil oder Kind) |
| `K`    | Kind krank |
| `KU`   | Kind krank, Urlaub genommen |

Beispiele: `YF` = Kindsvater, Feiertag · `MK` = Kindsmutter, Kind krank

### Annotationen

| Format | Sichtbarkeit | Bedeutung |
|--------|--------------|-----------|
| `(Text)` | offiziell | Ereignis, das in offizielle Dokumente darf |
| `[Text]` | nur intern | Notiz für interne Vorbereitung — wird beim Export entfernt |

---

## Kalender-Format

Ein Monat pro Block, getrennt durch `---`. Monatszeile mit relevanten Ereignissen.
ASCII-Tabelle mit Boxzeichen (Copy-Paste-fähig). Zellen werden breiter wenn nötig.

```
---
[Monatsname Jahr] ([optionaler Hinweis])

┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│  Mo  │  Di  │  Mi  │  Do  │  Fr  │  Sa  │  So  │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ TT X │ TT X │ ...  │      │      │      │      │
└──────┴──────┴──────┴──────┴──────┴──────┴──────┘
---
```

Leere Tage am Monatsanfang/-ende bleiben leer. Zellbreite wird pro Monat einheitlich
gewählt — breiter wenn Annotationen es erfordern.

---

## Aktualisierung durch den Skill

### Wann wird der Kalender aktualisiert?

1. **Beim Sachverhaltsgespräch** — wenn ein Datum oder Zeitraum genannt wird
2. **Beim Importieren von Belegen** — wenn Datumsangaben im Dokument erscheinen
3. **Beim Ausfüllen von offene-fragen.md** — wenn Antworten Daten enthalten
4. **Auf explizite Nennung** — „Bruno war letzte Woche bei mir krank"

### Regeln:

- Bekannte Betreuung eintragen — nie raten, immer mit Quelle (Beleg oder Gespräch)
- Intern-Notizen `[...]` für: eigene Einschätzungen, Risiken, emotionale Hintergründe,
  Dinge die nur mündlich relevant sind
- Offizielle Annotationen `(...)` für: Feiertage, Arztbesuche, KiTa-Events,
  Urlaube, Übergaben, Gerichtstermine
- Wenn ein Datum unsicher ist: Kürzel `~` voranstellen, z.B. `~Y`
- Widersprüche (Kalender vs. Beleg) sofort markieren: `!` voranstellen, z.B. `!M`
  und in `sachverhalt/notizen.md` als offene Frage erfassen

### Nach jeder Aktualisierung: Git-Commit

```
Kalender: [Monat] aktualisiert — [Kurzbeschreibung]
```

---

## Offizieller Export (für Anlagen)

Beim Export als Anlage (z.B. Anlage B2: Betreuungskalender) werden alle `[...]`-Inhalte
automatisch entfernt. Der Skill erzeugt eine bereinigte Kopie in `output/`.

Exportbefehl (Phase 5):
> „Erstelle den offiziellen Betreuungskalender als DOCX ohne interne Notizen."

---

## Vollständiges Beispiel

```
---
November 2025 (Wechselmodell-Start: 11.11.)

┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│  Mo  │  Di  │  Mi  │  Do  │  Fr  │  Sa  │  So  │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ —    │ —    │ —    │ —    │ —    │ 1 —  │ 2 —  │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ 3 —  │ 4 —  │ 5 —  │ 6 —  │ 7 —  │ 8 —  │ 9 —  │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ 10 — │ 11 Y │ 12 Y │ 13 Y │ 14 M │ 15 M │ 16 M │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ 17 Y │ 18 Y │ 19 M │ 20 M │ 21 Y │ 22 Y │ 23 Y │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ 24 M │ 25 M │ 26 Y │ 27 Y │ 28 M │ 29 M │ 30 M │
└──────┴──────┴──────┴──────┴──────┴──────┴──────┘

---
Dezember 2025

┌──────┬──────┬────────────────────┬─────────────────────┬─────────────────────┬──────┬──────┐
│  Mo  │  Di  │         Mi         │         Do          │         Fr          │  Sa  │  So  │
├──────┼──────┼────────────────────┼─────────────────────┼─────────────────────┼──────┼──────┤
│ 1 Y  │ 2 Y  │ 3 M                │ 4 M                 │ 5 Y                 │ 6 Y  │ 7 Y  │
├──────┼──────┼────────────────────┼─────────────────────┼─────────────────────┼──────┼──────┤
│ 8 M  │ 9 M  │ 10 Y               │ 11 Y                │ 12 M                │ 13 M │ 14 M │
├──────┼──────┼────────────────────┼─────────────────────┼─────────────────────┼──────┼──────┤
│ 15 Y │ 16 Y │ 17 M               │ 18 M                │ 19 Y                │ 20 Y │ 21 Y │
├──────┼──────┼────────────────────┼─────────────────────┼─────────────────────┼──────┼──────┤
│ 22 M │ 23 M │ 24 Y (Heiligabend) │ 25 YF (1.Weihnacht) │ 26 MF (2.Weihnacht) │ 27 M │ 28 M │
├──────┼──────┼────────────────────┼─────────────────────┼─────────────────────┼──────┼──────┤
│ 29 Y │ 30 Y │ 31 M (Silvester)   │                     │                     │      │      │
└──────┴──────┴────────────────────┴─────────────────────┴─────────────────────┴──────┴──────┘

---
März 2026

┌──────┬──────┬──────────────────────────────────┬──────┬──────┬──────┬───────────────────┐
│  Mo  │  Di  │                Mi                │  Do  │  Fr  │  Sa  │        So         │
├──────┼──────┼──────────────────────────────────┼──────┼──────┼──────┼───────────────────┤
│ 2 M  │ 3 M  │ 4 Y                              │ 5 Y  │ 6 M  │ 7 M  │ 1 Y               │
├──────┼──────┼──────────────────────────────────┼──────┼──────┼──────┼───────────────────┤
│ 9 Y  │ 10 Y │ 11 MK (KiTa-Gespräch) [!Konflikt]│ 12 M │ 13 Y │ 14 Y │ 8 M               │
├──────┼──────┼──────────────────────────────────┼──────┼──────┼──────┼───────────────────┤
│ 16 M │ 17 M │ 18 Y                             │ 19 Y │ 20 M │ 21 M │ 15 Y (heute)      │
├──────┼──────┼──────────────────────────────────┼──────┼──────┼──────┼───────────────────┤
│ 23 Y │ 24 Y │ 25 M                             │ 26 M │ 27 Y │ 28 Y │ 22 M              │
├──────┼──────┼──────────────────────────────────┼──────┼──────┼──────┼───────────────────┤
│ 30 M │ 31 M │                                  │      │      │      │ 29 Y (Sommerzeit) │
└──────┴──────┴──────────────────────────────────┴──────┴──────┴──────┴───────────────────┘
---
```
