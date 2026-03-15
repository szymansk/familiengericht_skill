# Familienrecht-Skill für Claude Code

Skill zur Erstellung von Schriftsätzen im Familienrecht (Umgang, Sorgerecht) nach dem Cochemer Modell — mit integriertem Trainingsmodus zur Verhandlungsvorbereitung.

> **Hinweis:** Dieser Skill ersetzt keine Rechtsberatung. Für verbindliche rechtliche Beurteilungen einen Fachanwalt für Familienrecht hinzuziehen.

---

## Installation

### Marketplace (empfohlen)

In Claude Code:

```
/plugin marketplace add szymansk/familiengericht_skill
/plugin install familienrecht@familienrecht-marketplace
```

### Manuell

```bash
git clone https://github.com/szymansk/familiengericht_skill.git
```

Nach dem Klonen in Claude Code als Plugin einbinden (`/plugin`).

---

## Verwendung

Der Skill aktiviert sich automatisch sobald familienrechtliche Begriffe fallen — kein Befehl nötig. Einfach natürlich schreiben.

---

## Funktionen & Beispiel-Prompts

### Neues Verfahren anlegen

Der Skill legt die vollständige Ordnerstruktur mit allen Templates an.

> „Ich habe ein neues Verfahren, Aktenzeichen 4 F 42/25."

---

### Sachverhaltsaufnahme

Der Skill stellt gezielte Fragen zum Betreuungsmodell, erfasst Fakten, Zeitachse und Kalender — und hilft, relevante von riskanten Informationen zu trennen.

> „Erzähl mir was passiert ist: Die Mutter hat die letzten drei Übergaben verweigert, zuletzt am 3. März."

> „Ich bin Vater von Bruno, 4 Jahre. Wir haben seit November ein Wechselmodell, aber die Mutter hält sich nicht daran."

---

### Schriftsatz verfassen

Der Skill schreibt Erwiderungen, Anträge und Stellungnahmen nach dem Cochemer Modell — kooperativ statt konfrontativ.

> „Schreib eine Erwiderung auf den Antrag der Mutter. Sie behauptet, ich sei unzuverlässig bei Übergaben."

> „Ich möchte einen Antrag auf Ausweitung meiner Umgangszeiten stellen."

---

### Schriftsatz prüfen

Der Skill prüft den Text aus vier Perspektiven: Richterin, Gegenanwalt, Verfahrensbeistand, Gutachter.

> „Prüfe die Erwiderung. Was könnte die Gegenseite daraus machen?"

> „Lies den Entwurf durch — gibt es Formulierungen, die uns schaden könnten?"

---

### Dokument importieren

DOCX, PDF oder andere Dokumente werden umbenannt, konvertiert und in die Ablage eingeordnet.

> „Hier ist der Schriftsatz der Gegenseite vom 10. März. Bitte einlesen."

> „Importiere das Protokoll vom Jugendamt."

---

### Betreuungskalender führen

Der Skill pflegt den Kalender automatisch bei jedem genannten Datum. Abweichungen vom Standard werden separat markiert.

> „Bruno war letzte Woche Montag und Dienstag bei mir, Mittwoch hat die Mutter kurzfristig übernommen."

> „Trag ein: Am 15. März war die Übergabe erst um 18 Uhr statt wie üblich um 8 Uhr."

---

### DOCX exportieren

Der Skill erzeugt druckfertige DOCX-Dateien — Erwiderung und Kalender ohne interne Notizen.

> „Exportiere die Erwiderung als DOCX."

> „Erstelle den offiziellen Betreuungskalender für die Anlage."

---

### Trainingsmodus — Verhandlung üben

Der Skill spielt reihum die Rollen von Richterin, Gegenanwältin, Verfahrensbeistand und Jugendamt. Feedback kommt gesammelt nach mehreren Fragen.

> „Ich möchte die Verhandlung üben."

> „Training — spiel die Richterin und frag mich zum Betreuungsmodell."

Der Skill schlägt den Trainingsmodus auch von sich aus vor, wenn er merkt dass Frustration oder Unsicherheit im Gespräch zunehmen.

---

### Mehrere Verfahren

Der Skill erkennt beim Start alle laufenden Verfahren im Arbeitsverzeichnis und gibt einen Überblick.

> „Welche Verfahren haben wir gerade?"

> „Wechsle zu Verfahren 3 F 18/25."

---

## 5-Phasen-Workflow

| Phase | Inhalt |
|-------|--------|
| **1. Sachverhaltsaufnahme** | Fakten, Betreuungsmodell, Gegenseite, Kalender |
| **2. Entwurf** | Schriftsatz in Markdown nach Cochemer-Prinzip |
| **3. Prüfung** | Aus Sicht aller Verfahrensbeteiligten |
| **4. Vertiefung** | Offene Fragen klären, neue Fakten einarbeiten |
| **5. Finalisierung** | DOCX exportieren, Verhandlung vorbereiten |
