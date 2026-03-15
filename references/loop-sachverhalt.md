# Loop-Workflow: Iterative Sachverhaltsaufnahme

Dieser Workflow wird mit dem `/loop`-Skill von Claude Code ausgeführt.
Er ersetzt das manuelle Frage-Antwort-Gespräch durch einen strukturierten
Iterationsprozess: Claude fragt, du antwortest in einer Datei, Claude wertet aus.

---

## Aktivierung

```
/loop 10m Führe eine Iteration des Familienrecht-Sachverhalts-Loops durch für verfahren/{az-kurz}
```

Empfohlenes Intervall: **10–15 Minuten** — genug Zeit, um die Fragen in Ruhe zu beantworten.

---

## Was Claude in jeder Iteration tut

### Schritt 1 — Dateien lesen
- `sachverhalt/fakten.md` — aktueller Wissensstand
- `sachverhalt/offene-fragen.md` — Fragen aus der letzten Iteration mit deinen Antworten

### Schritt 2 — Antworten auswerten
- Beantworte Fragen in `fakten.md` einarbeiten
- Neue Erkenntnisse in `sachverhalt/timeline.md` ergänzen
- Git-Commit nach jeder Aktualisierung

### Schritt 3 — Neue Fragen generieren
- Lücken im Sachverhalt identifizieren
- Widersprüche oder Unklarheiten benennen
- Maximal **5 Fragen pro Iteration** — nicht mehr

### Schritt 4 — `offene-fragen.md` aktualisieren
- Beantwortete Fragen als `[x]` markieren
- Neue Fragen anhängen
- Iterationszähler hochzählen

### Schritt 5 — Abbruchbedingung prüfen
Nach **3 Iterationen ohne neue offene Fragen** stoppt der Loop automatisch:
- Zusammenfassung des Sachverhalts ausgeben
- `sachverhalt/fakten.md` als vollständig markieren
- Hinweis: „Sachverhaltsaufnahme abgeschlossen — bereit für Phase 2 (Entwurf)"

---

## Format von `offene-fragen.md`

Claude schreibt und liest dieses Format:

```markdown
# Offene Fragen — Az. [Aktenzeichen]

<!-- Iteration: N | Letzte Aktualisierung: YYYY-MM-DD HH:MM -->

## Iteration 1

- [x] Seit wann gilt das aktuelle Betreuungsmodell?
      → Antwort: Seit März 2024, nach mündlicher Absprache beim Mediationsgespräch.

- [ ] Gibt es eine schriftliche Vereinbarung zum Betreuungsmodell?
      → Antwort: _hier eintragen_

- [ ] Wie viele Nächte pro Monat ist das Kind aktuell bei dir?
      → Antwort: _hier eintragen_

## Iteration 2

- [ ] [Neue Frage von Claude]
      → Antwort: _hier eintragen_
```

**Deine Aufgabe:** Nur die `→ Antwort:` Zeilen ausfüllen. Nichts anderes ändern.

---

## Starten des Loops

```bash
# 1. Verfahren muss angelegt sein (setup-verfahren.sh)
# 2. offene-fragen.md wird beim ersten Loop-Aufruf automatisch erstellt
# 3. Loop starten:

/loop 10m Führe eine Iteration des Familienrecht-Sachverhalts-Loops durch für verfahren/3-f-24-26
```

## Loop manuell stoppen

```
/loop stop
```

Oder: Wenn Claude nach 3 Iterationen ohne neue Fragen die Abschlussmeldung ausgibt,
läuft der Loop zwar weiter — tut aber nichts mehr Sinnvolles. Dann manuell stoppen.
