# Formatierungsstandards für Schriftsätze

## Markdown-Arbeitsdokument

Im Arbeitsalltag wird in Markdown geschrieben und in VS Code mit Preview bearbeitet. Das Markdown-Format folgt diesen Konventionen:

### Überschriften
```markdown
# Erwiderung — Az. 4 F 42/25         (Dokumenttitel, nicht im Text)

## Begründung:                         (Hauptüberschrift)
## I. Vorbemerkung                     (Kapitel)
## II. Zur Vorgeschichte               (Kapitel)
### 1. Wohnsituation                   (Unterkapitel)
### 2. Betreuungsrealität              (Unterkapitel)
```

### Querverweise
Im Markdown-Text: `(vgl. oben IV.)` oder `(dazu unten V.)`

### Zitate
Direkte Zitate kursiv in Anführungszeichen:
```markdown
Die Erzieherin äußerte sinngemäß: *„Ganz ehrlich, es gibt nicht viele Unterschiede."*
```

### Anlagen-Referenzen
Im Text: `(Anlage B4)` — immer in Klammern.

---

## DOCX-Generierung (Phase 5)

Für die Endausgabe als DOCX gelten diese Standards:

### Seitenformat
- **Papier:** A4
- **Ränder:** 2 cm allseitig (1134 DXA)
- **Schrift:** Arial
- **Schriftgröße:** 11 pt (22 half-points)
- **Zeilenabstand:** 1,15 (276 twips)
- **Absatzabstand nach:** 6 pt (120 twips)
- **Ausrichtung:** Blocksatz (Justified)

### Überschriften
- **Kapitel (I., II., ...):** Arial 13 pt fett, Abstand vor 15 pt, nach 8 pt
- **Unterkapitel (1., 2., ...):** Arial 12 pt fett, Abstand vor 12 pt, nach 6 pt
- **„Begründung:" und „Schlussbemerkung":** wie Kapitel

### Briefkopf
```
Thomas Beispiel          [fett]
Friedrichstraße 61
76229 Karlsruhe
Tel.: 0151 00000000
E-Mail: thomas.beispiel@example.com

Amtsgericht Karlsruhe-Durlach    [fett]
– Familiengericht –
Pfinztalstraße 2
76227 Karlsruhe

                                  Karlsruhe, den [Datum]  [rechtsbündig]

Aktenzeichen: [Az.]              [fett]

Erwiderung auf den Antrag...      [fett, unterstrichen]
```

### Anträge
- „Der Antragsgegner beantragt:" — fett
- Antragspunkte mit Einrückung (480 DXA)
- „Es wird weiter beantragt:" — fett
- „Hilfsweise:" — eingerückt, normal

### Unterschriftsblock
```
Weiterer Sachvortrag bleibt vorbehalten.

                                  Karlsruhe, den [Datum]


_______________________________
Thomas Beispiel           [fett]
(Antragsgegner)
```

### Anlagen-Dokumente
- Jede Anlage als eigenes DOCX
- Deckblatt mit: Anlage-Nummer, Titel, Aktenzeichen, Kurzbeschreibung
- Tabellarische Anlagen: Zebra-Striping, Header farbig (2B579A weiß)

---

## DOCX-Generierung mit docx-js (Node.js)

Bevorzugtes Tool: `docx` npm-Paket.

```bash
npm install -g docx
```

### Wichtige Regeln:
- Seitengröße explizit setzen (A4: 11906 x 16838 DXA)
- Nie `\n` verwenden — immer separate Paragraph-Objekte
- Tabellen: immer `columnWidths` UND `width` auf Zellen setzen
- `ShadingType.CLEAR` verwenden, nie `SOLID` (schwarze Hintergründe)
- Smart Quotes: `\u201E` (öffnend), `\u201C` (schließend), `\u2013` (Gedankenstrich)
