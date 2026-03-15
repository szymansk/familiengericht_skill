#!/usr/bin/env node
'use strict';
/**
 * generate-docx.js
 * Generiert DOCX-Ausgaben aus den Markdown-Dateien eines Verfahrens.
 *
 * Verwendung:
 *   node generate-docx.js verfahren/4-f-42-25
 *   node generate-docx.js verfahren/4-f-42-25 --only=erwiderung
 *   node generate-docx.js verfahren/4-f-42-25 --only=kalender
 *
 * Voraussetzung: npm install (im Skill-Verzeichnis)
 */

const {
  Document, Packer, Paragraph, TextRun,
  AlignmentType, UnderlineType,
  convertMillimetersToTwip,
} = require('docx');

const fs   = require('fs');
const path = require('path');

// ── Formatierungskonstanten (references/formatierung.md) ─────────────────────

const FONT             = 'Arial';
const SIZE_BODY        = 22;   // 11 pt  (half-points)
const SIZE_H_CHAPTER   = 26;   // 13 pt
const SIZE_H_SECTION   = 24;   // 12 pt
const MARGIN           = convertMillimetersToTwip(20);   // 2 cm allseitig
const LINE_SPACING     = 276;  // 1.15 × 240
const SPACE_AFTER_BODY = 120;  // 6 pt  (1 pt = 20 twips)
const SPACE_BEFORE_H1  = 300;  // 15 pt
const SPACE_AFTER_H1   = 160;  // 8 pt
const SPACE_BEFORE_H2  = 240;  // 12 pt
const SPACE_AFTER_H2   = 120;  // 6 pt

// ── Inline-Formatting ────────────────────────────────────────────────────────

/**
 * Zerlegt einen Text mit **bold** und *italic* Markierungen
 * in ein Array von TextRun-Objekten.
 */
function parseInline(text, extra = {}) {
  const runs = [];
  const re   = /(\*{1,3})(.*?)\1/gs;
  let last   = 0, m;

  while ((m = re.exec(text)) !== null) {
    if (m.index > last) {
      runs.push(new TextRun({ text: text.slice(last, m.index), font: FONT, size: SIZE_BODY, ...extra }));
    }
    const stars = m[1].length;
    runs.push(new TextRun({
      text: m[2], font: FONT, size: SIZE_BODY,
      bold:    stars >= 2,
      italics: stars === 1 || stars === 3,
      ...extra,
    }));
    last = re.lastIndex;
  }
  if (last < text.length) {
    runs.push(new TextRun({ text: text.slice(last), font: FONT, size: SIZE_BODY, ...extra }));
  }
  return runs.length ? runs : [new TextRun({ text, font: FONT, size: SIZE_BODY, ...extra })];
}

// ── Absatz-Helfer ─────────────────────────────────────────────────────────────

const bodySpacing = { line: LINE_SPACING, lineRule: 'auto', after: SPACE_AFTER_BODY };

function bodyPara(text, opts = {}) {
  return new Paragraph({
    children:  parseInline(text),
    alignment: AlignmentType.JUSTIFIED,
    spacing:   bodySpacing,
    ...opts,
  });
}

function emptyPara() {
  return new Paragraph({ children: [new TextRun('')], spacing: { after: 60 } });
}

function chapterHeading(text) {
  return new Paragraph({
    children:  [new TextRun({ text, font: FONT, size: SIZE_H_CHAPTER, bold: true })],
    spacing:   { before: SPACE_BEFORE_H1, after: SPACE_AFTER_H1 },
    alignment: AlignmentType.LEFT,
  });
}

function sectionHeading(text) {
  return new Paragraph({
    children:  [new TextRun({ text, font: FONT, size: SIZE_H_SECTION, bold: true })],
    spacing:   { before: SPACE_BEFORE_H2, after: SPACE_AFTER_H2 },
    alignment: AlignmentType.LEFT,
  });
}

// ── Markdown-Bereinigung ──────────────────────────────────────────────────────

function stripComments(md) {
  return md.replace(/<!--[\s\S]*?-->/g, '');
}

function stripInternalNotes(md) {
  return md.replace(/\s*\[[^\]]*\]/g, '');
}

// ── Briefkopf (alles vor dem ersten "---") ────────────────────────────────────

function parseBriefkopf(md) {
  const clean  = stripComments(md);
  const sepIdx = clean.search(/\n---/);
  if (sepIdx === -1) return [];

  const paras = [];
  const lines = clean.slice(0, sepIdx)
    .split('\n')
    .map(l => l.trim())
    .filter(l => l && !l.startsWith('# ') && !l.startsWith('> '));

  for (const l of lines) {
    const text = l.replace(/\*\*/g, '').replace(/\*/g, '');

    if (/^[A-Za-zÄÖÜäöüß ,]+,\s*den/.test(l) || /^\[Ort\].*den/.test(l)) {
      // Datum — rechtsbündig
      paras.push(new Paragraph({
        children:  [new TextRun({ text, font: FONT, size: SIZE_BODY })],
        alignment: AlignmentType.RIGHT,
        spacing:   { after: 120 },
      }));
    } else if (/^Aktenzeichen:|^\*\*Aktenzeichen:/.test(l)) {
      paras.push(new Paragraph({
        children:  [new TextRun({ text, font: FONT, size: SIZE_BODY, bold: true })],
        spacing:   { after: 120 },
      }));
    } else if (/^Erwiderung|^Antrag/.test(l)) {
      // Betreff — fett und unterstrichen
      paras.push(new Paragraph({
        children:  [new TextRun({ text, font: FONT, size: SIZE_BODY, bold: true,
                                  underline: { type: UnderlineType.SINGLE } })],
        spacing:   { after: 120 },
      }));
    } else if (/^\*\*/.test(l)) {
      // Fetter Block (Name Absender, Gericht)
      paras.push(new Paragraph({
        children:  [new TextRun({ text, font: FONT, size: SIZE_BODY, bold: true })],
        spacing:   { after: 0 },
      }));
    } else {
      paras.push(new Paragraph({
        children:  [new TextRun({ text, font: FONT, size: SIZE_BODY })],
        spacing:   { after: 0 },
      }));
    }
  }

  paras.push(emptyPara());
  return paras;
}

// ── Schriftsatz-Body (nach dem ersten "---") ──────────────────────────────────

function parseBody(md) {
  const clean = stripComments(md);
  const sep   = clean.search(/\n---/);
  const body  = sep !== -1 ? clean.slice(sep + 4) : clean;
  const lines = body.split('\n');
  const paras = [];

  for (const line of lines) {
    const t = line.trim();
    if (!t)                              { continue; }
    if (t.startsWith('>'))               { continue; }  // Blockquotes (Arbeitshinweise)
    if (/^---+$/.test(t))                { continue; }  // Trennlinien

    if (/^## /.test(t)) {
      paras.push(chapterHeading(t.replace(/^## /, '')));
    } else if (/^### /.test(t)) {
      paras.push(sectionHeading(t.replace(/^### /, '')));
    } else if (/^# /.test(t)) {
      // H1 = Dokumenttitel — überspringen
    } else if (t === 'Der Antragsgegner beantragt:' || t === 'Es wird weiter beantragt:') {
      paras.push(new Paragraph({
        children:  [new TextRun({ text: t, font: FONT, size: SIZE_BODY, bold: true })],
        spacing:   bodySpacing,
      }));
    } else if (/^\d+\.\s/.test(t) || t.startsWith('Hilfsweise:')) {
      paras.push(bodyPara(t, {
        indent:    { left: convertMillimetersToTwip(12) },
        alignment: AlignmentType.LEFT,
      }));
    } else if (/^Anlage [A-Z]\d+:/.test(t)) {
      paras.push(bodyPara(t, { indent: { left: convertMillimetersToTwip(6) } }));
    } else if (t.startsWith('Weiterer Sachvortrag')) {
      paras.push(emptyPara());
      paras.push(bodyPara(t));
    } else if (/^_{3,}$/.test(t)) {
      paras.push(new Paragraph({
        children:  [new TextRun({ text: '________________________', font: FONT, size: SIZE_BODY })],
        alignment: AlignmentType.RIGHT,
        spacing:   { after: 0 },
      }));
    } else {
      paras.push(bodyPara(t));
    }
  }

  return paras;
}

// ── Erwiderung generieren ────────────────────────────────────────────────────

async function buildErwiderung(mdPath) {
  const md = fs.readFileSync(mdPath, 'utf8');

  const doc = new Document({
    sections: [{
      properties: {
        page: {
          size:   { width: convertMillimetersToTwip(210), height: convertMillimetersToTwip(297) },
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
        },
      },
      children: [
        ...parseBriefkopf(md),
        ...parseBody(md),
      ],
    }],
  });

  return Packer.toBuffer(doc);
}

// ── Kalender generieren (ohne interne Notizen) ───────────────────────────────

async function buildKalender(mdPath) {
  const raw    = fs.readFileSync(mdPath, 'utf8');
  const clean  = stripInternalNotes(stripComments(raw));
  const paras  = [];

  for (const line of clean.split('\n')) {
    const t = line.trim();
    if (!t || t === '---') continue;

    if (/^[A-Za-zÄÖÜäöü]+ \d{4}/.test(t)) {
      // Monatsüberschrift
      paras.push(new Paragraph({
        children:  [new TextRun({ text: t, font: FONT, size: SIZE_H_SECTION, bold: true })],
        spacing:   { before: 240, after: 120 },
      }));
    } else {
      // Kalenderzeilen in Monospace
      paras.push(new Paragraph({
        children:  [new TextRun({ text: t, font: 'Courier New', size: 18 })],
        spacing:   { after: 0, line: 240, lineRule: 'exact' },
      }));
    }
  }

  if (!paras.length) paras.push(emptyPara());

  const doc = new Document({
    sections: [{
      properties: {
        page: {
          // Querformat für den Kalender
          size:   { width: convertMillimetersToTwip(297), height: convertMillimetersToTwip(210) },
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
        },
      },
      children: paras,
    }],
  });

  return Packer.toBuffer(doc);
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args          = process.argv.slice(2);
  const verfahrenPath = args.find(a => !a.startsWith('--'));
  const only          = (args.find(a => a.startsWith('--only=')) || '').replace('--only=', '') || 'all';

  if (!verfahrenPath) {
    console.error('Verwendung: node generate-docx.js <verfahren-pfad> [--only=erwiderung|kalender]');
    process.exit(1);
  }
  if (!fs.existsSync(verfahrenPath)) {
    console.error(`Fehler: Verfahren nicht gefunden: ${verfahrenPath}`);
    process.exit(1);
  }

  const outputDir = path.join(verfahrenPath, 'output');
  fs.mkdirSync(outputDir, { recursive: true });

  if (only === 'all' || only === 'erwiderung') {
    const src = path.join(verfahrenPath, 'erwiderung', 'erwiderung.md');
    if (fs.existsSync(src)) {
      process.stdout.write('Generiere erwiderung.docx … ');
      const buf = await buildErwiderung(src);
      const dst = path.join(outputDir, 'erwiderung.docx');
      fs.writeFileSync(dst, buf);
      console.log(`✓  ${dst}`);
    } else {
      console.warn('  erwiderung.md nicht gefunden — übersprungen.');
    }
  }

  if (only === 'all' || only === 'kalender') {
    const src = path.join(verfahrenPath, 'sachverhalt', 'kalender.md');
    if (fs.existsSync(src)) {
      process.stdout.write('Generiere kalender.docx (ohne interne Notizen) … ');
      const buf = await buildKalender(src);
      const dst = path.join(outputDir, 'kalender.docx');
      fs.writeFileSync(dst, buf);
      console.log(`✓  ${dst}`);
    } else {
      console.warn('  kalender.md nicht gefunden — übersprungen.');
    }
  }

  console.log('\nFertig. Dateien liegen in:', outputDir);
}

main().catch(err => { console.error('\nFehler:', err.message); process.exit(1); });
