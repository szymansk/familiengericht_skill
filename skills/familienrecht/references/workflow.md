# 5-Phasen-Workflow für familienrechtliche Schriftsätze

## Phase 1 — Sachverhaltsaufnahme

### Bei neuen Verfahren:
1. Verfahrensdaten aufnehmen: Aktenzeichen, Gericht, Parteien, Kind(er), Anwälte
2. Grundsituation klären: Wer hat den Antrag gestellt? Was wird beantragt?
3. Chronologie erstellen: Trennung, Auszug, Vereinbarungen, Beratungsstellen
4. Betreuungsrealität erfragen: Wer macht was? Wie sieht ein typischer Tag aus?
5. Belege sammeln: E-Mails, WhatsApp, Fotos, Kalender, Bescheinigungen

### Bei Erwiderungen zusätzlich:
6. Antrag der Gegenseite importieren und analysieren
7. Jede Behauptung einzeln erfassen mit Bewertung:
   - Schwere: Hoch / Mittel / Niedrig
   - Belegbar: Ja / Nein / Teilweise
   - Antwort-Strategie: Widerlegen / Einordnen / Ignorieren
8. Protokolle/Anlagen der Gegenseite analysieren
9. Widersprüche innerhalb des Antrags identifizieren

### Output Phase 1:
- `sachverhalt/fakten.md` — alle gesammelten Fakten
- `sachverhalt/timeline.md` — Chronologie
- Bei Erwiderungen: Analyse-Tabelle der gegnerischen Behauptungen

---

## Phase 2 — Entwurf

### Struktur eines Schriftsatzes:

```markdown
# [Antrag/Erwiderung] — [Az.]

## Briefkopf
[Name, Adresse, Gericht, Datum, Az., Rubrum]

## Antrag
1. Hauptantrag (Zurückweisung / eigener Antrag)

Es wird weiter beantragt:
2. Konkrete Regelung
   Hilfsweise: Alternative
3. Weitere Anträge (z.B. Ferienregelung)

## Begründung

### I. Vorbemerkung
[Zusammenfassung der Position, Verweis auf stärkste Argumente]

### II. Zur Vorgeschichte
[Sachverhalt aus eigener Sicht]

### III.–VI. [Thematische Abschnitte]
[Je nach Verfahren: Betreuungsrealität, Kooperation, Fachliche Einschätzungen, Widerlegungen]

### [Vorletzter Abschnitt] Zum Protokoll / Zu den Anlagen der Gegenseite
[Nur wenn relevant]

### Schlussbemerkung
[Zusammenfassende Position zum Kindeswohl]

### [Letzter Abschnitt] Glaubhaftmachung
[Anlagenverzeichnis]

Weiterer Sachvortrag bleibt vorbehalten.

[Datum, Unterschrift]
```

### Reihenfolge-Prinzip:
1. **Positiv führen** — eigene Stärken, Kooperation, fachliche Bestätigung
2. **Defensiv abschließen** — Widerlegungen kompakt, nicht dominant
3. **Protokollkritik separat** — in eigenem Abschnitt
4. **Schlussbemerkung** — Kernposition zum Kindeswohl

### Output Phase 2:
- `erwiderung/erwiderung.md` — Haupttext
- `erwiderung/anlagen.md` — Anlagenverzeichnis mit Beschreibungen

---

## Phase 3 — Prüfung

→ Siehe `references/pruefschema.md` für das vollständige Prüfschema.

### Prüfung in drei Schritten:

**Schritt 1: Perspektiv-Prüfung**
Jeden Abschnitt aus der Sicht lesen von:
- Richterin/Richter
- Gegenanwältin/Gegenanwalt
- Verfahrensbeistand
- (falls bestellt) Gutachter

**Schritt 2: Konsistenz-Prüfung**
- Stimmen alle Querverweise?
- Widerspricht sich der Schriftsatz intern?
- Sind alle erwähnten Anlagen tatsächlich beigefügt?
- Stimmen Datumsangaben?

**Schritt 3: Risiko-Prüfung**
- Kann die Gegenseite einen Absatz umdrehen?
- Gibt es Formulierungen, die arrogant oder abwertend wirken?
- Sind Behauptungen belegbar oder nur Wort gegen Wort?

### Output Phase 3:
- Prüfbericht als Übersicht an den Nutzer
- Liste offener Fragen für Phase 4

---

## Phase 4 — Vertiefung

1. Offene Fragen aus Phase 3 dem Nutzer vorlegen
2. Neue Anekdoten oder Fakten aufnehmen
3. **Jede neue Information zuerst auf Risiken prüfen:**
   - Kann die Gegenseite es umdrehen?
   - Stützt es die eigene Linie oder schwächt es sie?
   - Ist es relevant oder nur emotional befriedigend?
4. Nach Freigabe durch den Nutzer einarbeiten
5. Bei wesentlichen Änderungen: zurück zu Phase 3

### Abschluss Phase 4:
Der Nutzer bestätigt: „Nichts mehr offen" → weiter zu Phase 5.

---

## Phase 5 — Finalisierung

### 5a: DOCX-Generierung
- Erwiderung als DOCX mit einheitlicher Formatierung
- Alle Anlagen als separate DOCX
- Deckblätter für Anlagen wo nötig
- Alles in `output/` ablegen

### 5b: Vorbereitung Verhandlung
`vorbereitung/verhandlung.md` erstellen mit:
- Alle Punkte aus dem Schriftsatz (Kurzfassung)
- **NUR MÜNDLICH**-Punkte mit Redevorschlägen
- Erwartbare Fragen der Richterin mit Antwortvorschlägen
- Erwartbare Argumente der Gegenseite mit Reaktionen
- Dos and Don'ts für die Verhandlung

### 5c: Checkliste Einreichung
- [ ] Datum im Briefkopf und Unterschrift auf Einreichungsdatum
- [ ] Alle Anlagen vollständig und nummeriert
- [ ] Kopien für alle Verfahrensbeteiligten
- [ ] Versand per Fax/beA oder persönliche Einreichung

### Formatierungsstandards:
→ Siehe `references/formatierung.md`
