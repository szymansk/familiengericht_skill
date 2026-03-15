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
| `V`    | Kindsvater |
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

### Abweichungen vom Standard

Der Kalender definiert einmal den **Standard** (Übergabezeit, -ort). Nur Abweichungen davon werden annotiert — alles was der Regel entspricht, bleibt ohne Zusatz.

**Vertretung (anderer Elternteil übernimmt):**

| Notation | Bedeutung | Sichtbarkeit |
|----------|-----------|--------------|
| `M[V]`   | Mutter hat Kind, war Vaters geplanter Tag | intern |
| `V[M]`   | Vater hat Kind, war Mutters geplanter Tag | intern |

Das Basiszeichen zeigt immer, wer das Kind **tatsächlich** hatte. Das Ziel einer Übergabe ist am nächsten Tag ablesbar.

**Übergabe-Abweichungen:**

| Notation | Bedeutung | Sichtbarkeit |
|----------|-----------|--------------|
| `(Ü1800)` | Übergabe um 18:00 Uhr (abweichend vom Standard) | offiziell |
| `(ÜKT)`   | Übergabe in der KiTa (wenn nicht Standard) | offiziell |
| `(ÜHV)`   | Übergabe beim Vater (wenn nicht Standard) | offiziell |
| `(ÜHM)`   | Übergabe bei der Mutter (wenn nicht Standard) | offiziell |
| `[Ü1800]` | wie oben, aber nur intern relevant | intern |

Kombinationen möglich: `VK(Ü1800)` = Vaters Tag, Kind krank, Übergabe um 18:00.

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
- Wenn ein Datum unsicher ist: Kürzel `~` voranstellen, z.B. `~V`
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
│ 10 — │ 11 V │ 12 V │ 13 V │ 14 M │ 15 M │ 16 M │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ 17 V │ 18 V │ 19 M │ 20 M │ 21 V │ 22 V │ 23 V │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ 24 M │ 25 M │ 26 V │ 27 V │ 28 M │ 29 M │ 30 M │
└──────┴──────┴──────┴──────┴──────┴──────┴──────┘

---
Dezember 2025

┌──────┬──────┬────────────────────┬─────────────────────┬─────────────────────┬──────┬──────┐
│  Mo  │  Di  │         Mi         │         Do          │         Fr          │  Sa  │  So  │
├──────┼──────┼────────────────────┼─────────────────────┼─────────────────────┼──────┼──────┤
│ 1 V  │ 2 V  │ 3 M                │ 4 M                 │ 5 V                 │ 6 V  │ 7 V  │
├──────┼──────┼────────────────────┼─────────────────────┼─────────────────────┼──────┼──────┤
│ 8 M  │ 9 M  │ 10 V               │ 11 V                │ 12 M                │ 13 M │ 14 M │
├──────┼──────┼────────────────────┼─────────────────────┼─────────────────────┼──────┼──────┤
│ 15 V │ 16 V │ 17 M               │ 18 M                │ 19 V                │ 20 V │ 21 V │
├──────┼──────┼────────────────────┼─────────────────────┼─────────────────────┼──────┼──────┤
│ 22 M │ 23 M │ 24 V (Heiligabend) │ 25 VF (1.Weihnacht) │ 26 MF (2.Weihnacht) │ 27 M │ 28 M │
├──────┼──────┼────────────────────┼─────────────────────┼─────────────────────┼──────┼──────┤
│ 29 V │ 30 V │ 31 M (Silvester)   │                     │                     │      │      │
└──────┴──────┴────────────────────┴─────────────────────┴─────────────────────┴──────┴──────┘

---
März 2026
Standard: Übergabe 08:00 Uhr KiTa (Wochentags) / 17:00 Uhr jeweils zuhause (Wochenende)

┌────────────────┬──────┬──────────────────────────────────┬──────┬──────┬──────┬───────────────────┐
│       Mo       │  Di  │                Mi                │  Do  │  Fr  │  Sa  │        So         │
├────────────────┼──────┼──────────────────────────────────┼──────┼──────┼──────┼───────────────────┤
│ 2 M            │ 3 M  │ 4 V                              │ 5 V  │ 6 M  │ 7 M  │ 1 V               │
├────────────────┼──────┼──────────────────────────────────┼──────┼──────┼──────┼───────────────────┤
│ 9 V(Ü1400)     │ 10 V │ 11 MK (KiTa-Gespräch) [!Konflikt]│ 12 M │ 13 V │ 14 V │ 8 M[V]            │
├────────────────┼──────┼──────────────────────────────────┼──────┼──────┼──────┼───────────────────┤
│ 16 M           │ 17 M │ 18 V                             │ 19 V │ 20 M │ 21 M │ 15 V (heute)      │
├────────────────┼──────┼──────────────────────────────────┼──────┼──────┼──────┼───────────────────┤
│ 23 V           │ 24 V │ 25 M                             │ 26 M │ 27 V │ 28 V │ 22 M              │
├────────────────┼──────┼──────────────────────────────────┼──────┼──────┼──────┼───────────────────┤
│ 30 M           │ 31 M │                                  │      │      │      │ 29 V (Sommerzeit) │
└────────────────┴──────┴──────────────────────────────────┴──────┴──────┴──────┴───────────────────┘

Lesebeispiele:
- 9 V(Ü1400): Vaters Tag, Übergabe abweichend um 14:00 (Ziel: Mutter, sichtbar am 10 V → nein, also intern geblieben)
- 8 M[V]: Vaters geplanter Tag, Mutter hat übernommen (intern, geht nicht ins Dokument)
---
```
