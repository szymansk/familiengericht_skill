# Zitierregeln — Belegpflicht im Familienrecht-Skill

> Diese Regeln haben **höchste Priorität** und gelten für den gesamten Skill sowie alle Sub-Agenten.

---

## Grundsatz

Jede Behauptung, Argumentation oder sachliche Aussage in einem intern generierten Dokument muss durch ein exaktes Zitat aus einem vorhandenen Quelldokument belegt sein. Es gibt keine unbelegten Behauptungen — nur belegte Aussagen oder explizit markierte Lücken.

**Ziel:** Keine Halluzinationen. Jeder Inhalt ist auf eine konkrete Textstelle in einem importierten Dokument zurückführbar.

---

## Welche Dokumente unterliegen der Belegpflicht?

### Belegpflichtig (interne Dokumente):

| Dokument | Hinweis |
|---------|---------|
| `sachverhalt/fakten.md` | Jede Faktenaussage |
| `sachverhalt/timeline.md` | Jedes Ereignis |
| `sachverhalt/offene-fragen.md` | Jede Aussage über den Sachverhalt |
| `sachverhalt/entscheidungen.md` | Jede strategische Einschätzung die auf Fakten beruht |
| `sachverhalt/notizen.md` | Jede übernommene Aussage |
| `erwiderung/nur-muendlich.md` | Jeder mündliche Punkt der auf einem Dokument basiert |
| `vorbereitung/verhandlung.md` | Jede inhaltliche Aussage |
| `vorbereitung/*-gespraech-onepager.md` | Gedächtnisanker und Kernbotschaften |
| `kontext.md` | Alle inhaltlichen Felder |

**Nicht belegpflichtig** (reine Strukturelemente): Überschriften, Aktenzeichen, Datum, Tabellenspalten-Bezeichnungen, Platzhaltertext.

### Nicht belegpflichtig (externe Schreiben):

`erwiderung/erwiderung.md`, Anträge und alle Schreiben an Gericht, Gegenseite, VB, JA oder andere Institutionen enthalten **kein Inline-Zitierformat**.

**Aber:** In diesen Schreiben dürfen nur Argumente und Fakten verwendet werden, die in einem internen Dokument bereits mit `[n]` belegt sind. Belege erscheinen dort gesammelt als Anlagen in der **Glaubhaftmachung** — nicht als Einzelzitate im Fließtext.

---

## Zitierformat

### Nummerierte Referenzen

Inline im Text: `[1]`, `[2]`, … direkt nach der belegten Aussage.

Quellenliste am **Ende des Dokuments** (eigener Abschnitt):

```markdown
---

## Quellen

[1] belege/emails/20260210_3f2426_KB_KV_KiTa-Email.md, Z. 8:
    „Herr Berger erscheint stets pünktlich und gut vorbereitet zur Übergabe."

[2] belege/dokumente/20250901_3f2426_KV_KM_Elternvereinbarung.md, Abschnitt 3:
    „Die Betreuungszeiten werden paritätisch aufgeteilt."
```

### Pflichtfelder je Zitat

| Feld | Format | Beispiel |
|------|--------|---------|
| Datei | Relativer Pfad ab Verfahrensordner | `belege/emails/20260210_3f2426_KB_KV_KiTa-Email.md` |
| Textstelle | Zeilennummer (`Z. n`) oder Abschnitt (`Abschnitt X`) | `Z. 8` oder `Abschnitt 3` |
| Originalzitat | Wörtlich, in Anführungszeichen | `„Herr Berger erscheint stets pünktlich."` |

### Sonderfall Onepager

Da der Onepager platzkritisch ist (max. 1–2 Seiten), erscheinen die `[n]`-Marker am Ende der jeweiligen Zeile/des Bullet-Points. Die Quellenliste kommt in einen eigenen kompakten Abschnitt am Ende:

```markdown
- Stets pünktlich und verlässlich bei Übergaben. [1]
- KiTa bestätigt aktive Einbindung in Entwicklungsgespräche. [2]

---
**Quellen:** [1] belege/emails/20260210_…md, Z. 8 | [2] belege/emails/20260210_…md, Z. 15
```

---

## Wenn kein Beleg vorhanden ist

Aussage **nicht weglassen** und **nicht erfinden**. Stattdessen:

```
Die Übergaben verlaufen konfliktfrei. [UNBELEGT]
```

Der `[UNBELEGT]`-Marker:
- Erscheint inline, direkt nach der Aussage
- Bedeutet: Diese Aussage kommt aus dem Gedächtnis des Nutzers, ist aber noch nicht durch ein importiertes Dokument gedeckt
- Wird vom Aufräum-Agent als offene Frage in `offene-fragen.md` eingetragen
- Soll so schnell wie möglich durch einen Beleg ersetzt werden

---

## Wie Zitate ermittelt werden

1. Quelldokument in `belege/` lesen (Read-Tool)
2. Relevante Textstelle identifizieren
3. Exaktes Originalzitat übernehmen — **nicht paraphrasieren**, nicht kürzen ohne Kennzeichnung (`[…]`)
4. Bei OCR-Unsicherheiten (Scan, Handschrift): Unsicherheit explizit vermerken: `„[Lesart unsicher: Herr Berger …]"`

---

## Prüfreihenfolge beim Schreiben

1. Quelldokument lesen
2. Exaktes Zitat extrahieren
3. Aussage formulieren + `[n]` anhängen
4. Quellenliste am Ende aktualisieren
5. Gibt es für eine Aussage kein Quelldokument → `[UNBELEGT]` setzen, nicht weglassen
