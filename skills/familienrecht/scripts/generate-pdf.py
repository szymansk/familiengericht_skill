#!/usr/bin/env python3
"""
generate-pdf.py — Erzeugt PDFs aus den Markdown-Dateien eines Verfahrens.
Verwendet Pandoc + XeLaTeX (kein eigenes Template).

Verwendung:
  python scripts/generate-pdf.py verfahren/4-f-42-25
  python scripts/generate-pdf.py verfahren/4-f-42-25 --only=erwiderung
  python scripts/generate-pdf.py verfahren/4-f-42-25 --only=kalender
  python scripts/generate-pdf.py verfahren/4-f-42-25 --only=deckblatt

Voraussetzung:
  pandoc, xelatex (via BasicTeX oder MacTeX), setup.sh ausgeführt
"""

import sys
import re
import os
import subprocess
import tempfile
import shutil
from pathlib import Path

# ── Pfade ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent.resolve()
TEMPLATES  = SCRIPT_DIR / 'templates'

# ── Abhängigkeiten prüfen ─────────────────────────────────────────────────────

def check_deps():
    missing = []
    if not shutil.which('pandoc'):
        missing.append('pandoc  → brew install pandoc')
    if not shutil.which('xelatex'):
        missing.append('xelatex → brew install --cask basictex')
    if missing:
        print("Fehlende Abhängigkeiten:")
        for m in missing:
            print(f"  {m}")
        print("\nAlles installieren: bash scripts/setup.sh")
        sys.exit(1)

# ── Markdown-Vorverarbeitung ──────────────────────────────────────────────────

def strip_comments(text: str) -> str:
    """Entfernt HTML-Kommentare (<!-- ... -->)."""
    return re.sub(r'<!--[\s\S]*?-->', '', text)

def strip_internal_notes(text: str) -> str:
    """Entfernt [intern]-Annotationen (eckige Klammern) für den offiziellen Export."""
    return re.sub(r'\s*\[[^\]]*\]', '', text)

def strip_template_hints(text: str) -> str:
    """Entfernt Blockquote-Zeilen (> ...) — werden als Template-Hinweise behandelt."""
    return re.sub(r'^>.*\n?', '', text, flags=re.MULTILINE)

def split_briefkopf(md: str) -> tuple[str, str]:
    """Trennt Briefkopf vom Schriftsatz-Body.

    Unterstützt zwei Formate:
    - Zwei --- (Template-Format): Titel/Hints --- Briefkopf --- Body
    - Ein ---  (einfaches Format): Briefkopf --- Body
    """
    clean = strip_comments(md)
    separators = [m.start() for m in re.finditer(r'\n---\n', clean)]

    if len(separators) >= 2:
        # Briefkopf zwischen erstem und zweitem ---
        bk_start = separators[0] + len('\n---\n')
        bk_end   = separators[1]
        body_start = separators[1] + len('\n---\n')
        return clean[bk_start:bk_end], clean[body_start:]
    elif len(separators) == 1:
        # Briefkopf vor dem einzigen ---
        return clean[:separators[0]], clean[separators[0] + len('\n---\n'):]
    else:
        return '', clean

def briefkopf_to_latex(text: str) -> str:
    """Konvertiert Briefkopf-Absätze zu LaTeX.

    Parsing-Regeln (absatzbasiert):
    - Fettzeile (**Name**) allein → Adressblock-Beginn; Folgeabsätze (Text)
      werden als Adresszeilen gesammelt. Zwischen zwei Adressblöcken: \\bigskip.
    - Datum (dt. Monatsname)    → rechtsbündig via \\hfill
    - Aktenzeichen:             → fett
    - Erwiderung / Stellungnahme (fett allein) → fett + unterstrichen
    - Alles andere              → linksbündig mit explizitem Zeilenumbruch
    """
    MONTHS  = (r'Januar|Februar|März|April|Mai|Juni|Juli|August|'
               r'September|Oktober|November|Dezember')
    DATE_RE   = re.compile(r'\d{1,2}\.\s*(?:' + MONTHS + r')\s+\d{4}')
    BOLD_ONLY = re.compile(r'^\*\*[^*]+\*\*$')

    def bold_to_tex(s: str) -> str:
        return re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', s)

    def strip_bold(s: str) -> str:
        return re.sub(r'\*\*', '', s)

    paragraphs = [p.strip() for p in re.split(r'\n{2,}', text.strip()) if p.strip()]

    # ── Klassifizierung ───────────────────────────────────────────────────────
    classified = []
    for para in paragraphs:
        lines = [l.strip() for l in para.split('\n') if l.strip()]
        if not lines:
            continue
        first = lines[0]
        if 'Aktenzeichen:' in para:
            classified.append(('az',        lines))
        elif (BOLD_ONLY.match(first) and len(lines) == 1
              and re.match(r'\*\*(Erwiderung|Stellungnahme)\b', first)):
            classified.append(('subject',   lines))
        elif BOLD_ONLY.match(first) and len(lines) == 1:
            classified.append(('addr_start', lines))
        elif DATE_RE.search(para):
            classified.append(('date',      lines))
        else:
            classified.append(('text',      lines))

    # ── Adressblöcke zusammenführen ───────────────────────────────────────────
    items = []
    i = 0
    while i < len(classified):
        kind, lines = classified[i]
        if kind == 'addr_start':
            addr_lines = list(lines)
            j = i + 1
            while j < len(classified) and classified[j][0] == 'text':
                addr_lines.extend(classified[j][1])
                j += 1
            items.append(('addr', addr_lines))
            i = j
        else:
            items.append((kind, lines))
            i += 1

    # ── Parse-Log ────────────────────────────────────────────────────────────
    LABELS = {'addr': 'Adresse', 'date': 'Datum', 'az': 'Aktenzeichen',
              'subject': 'Betreff', 'text': 'Text'}
    for kind, lines in items:
        first = lines[0][:60] + ('…' if len(lines[0]) > 60 else '')
        extra = f' (+{len(lines)-1} Zeilen)' if len(lines) > 1 else ''
        print(f'  [Briefkopf] {LABELS.get(kind, kind):<14} {first}{extra}')

    # ── Rendern ───────────────────────────────────────────────────────────────
    out = []
    prev_addr = False
    for kind, lines in items:
        if kind == 'addr':
            if prev_addr:
                out.append('\\par\\vspace{14pt}')
            tex = ['\\noindent ' + bold_to_tex(l) for l in lines]
            out.append('\\\\[0mm]\n'.join(tex) + '\\par')
            prev_addr = True
        elif kind == 'date':
            prev_addr = False
            for l in lines:
                out.append(f'\\hfill {bold_to_tex(l)}\\\\[1mm]')
        elif kind == 'az':
            prev_addr = False
            for l in lines:
                out.append(f'\\noindent\\textbf{{{strip_bold(l)}}}\\\\[3mm]')
        elif kind == 'subject':
            prev_addr = False
            for l in lines:
                out.append(f'\\noindent\\textbf{{{{{strip_bold(l)}}}}}\\\\[4mm]')
        else:
            prev_addr = False
            for l in lines:
                out.append(f'\\noindent {bold_to_tex(l)}\\\\[0mm]')

    return '\n'.join(out)

# ── Pandoc aufrufen ───────────────────────────────────────────────────────────

# Gemeinsame Basis-Flags für alle Dokumente
PANDOC_BASE = [
    '--pdf-engine', 'xelatex',
    '-V', 'lang=de-DE',
    '-V', 'papersize=a4',
    '-V', 'geometry:margin=2.5cm',
    '-V', 'mainfont=Arial',
    '-V', 'fontsize=12pt',
    '-V', 'linestretch=1.2',
]

def run_pandoc(md_text: str, output: Path, extra_flags: list = None,
               extra_vars: dict = None, template: Path = None):
    """Schreibt MD in Tempfile und ruft Pandoc auf.

    Erzeugt neben der PDF auch eine .tex-Datei im selben Verzeichnis,
    damit Layout-Anpassungen direkt im LaTeX-Code möglich sind.
    """
    with tempfile.NamedTemporaryFile(suffix='.md', mode='w',
                                     encoding='utf-8', delete=False) as f:
        f.write(md_text)
        tmp_md = f.name

    base_cmd = ['pandoc', tmp_md] + PANDOC_BASE
    if template:
        base_cmd += ['--template', str(template)]
    if extra_flags:
        base_cmd += extra_flags
    if extra_vars:
        for k, v in extra_vars.items():
            base_cmd += ['--variable', f'{k}={v}']

    try:
        # PDF erzeugen
        result = subprocess.run(base_cmd + ['--output', str(output)],
                                capture_output=True, text=True)
        if result.returncode != 0:
            print(f"\nPandoc-Fehler:\n{result.stderr}")
            sys.exit(1)

        # .tex-Datei erhalten (gleicher Name, andere Endung)
        tex_output = output.with_suffix('.tex')
        result_tex = subprocess.run(
            base_cmd + ['--output', str(tex_output)],
            capture_output=True, text=True)
        if result_tex.returncode != 0:
            print(f"  [Warnung] .tex konnte nicht gespeichert werden: {result_tex.stderr[:200]}")
    finally:
        os.unlink(tmp_md)

# ── Dokumente generieren ──────────────────────────────────────────────────────

def protect_signature_block(body: str) -> str:
    """Verhindert Seitenumbruch im Unterschriftsblock via \\needspace.

    Fügt \\needspace{7cm} vor 'Weiterer Sachvortrag' (Standard-Schlussformel)
    oder als Fallback vor der Unterschriftszeile (___) ein. Anders als
    \\begin{samepage} umschließt \\needspace keinen Inhalt, sodass Pandoc
    das Markdown im Block normal verarbeitet.
    """
    anchor = re.search(r'\nWeiterer Sachvortrag\b', body)
    if not anchor:
        anchor = re.search(r'\n_{5,}', body)
    if not anchor:
        return body
    pos = anchor.start()
    body = body[:pos] + '\n\\vspace{12pt}\n\\needspace{7cm}' + body[pos:]

    # Zusätzlicher Abstand vor der Orts-Datums-Zeile im Unterschriftsblock
    MONTHS = (r'Januar|Februar|März|April|Mai|Juni|Juli|August|'
              r'September|Oktober|November|Dezember')
    sig_date = re.search(r'\n(?=\S[^\n]*\d{1,2}\.\s*(?:' + MONTHS + r')\s+\d{4})',
                         body[pos:])
    if sig_date:
        p = pos + sig_date.start()
        body = body[:p] + '\n\\vspace{10pt}' + body[p:]
    return body


def build_erwiderung(md_path: Path, output: Path):
    md = md_path.read_text(encoding='utf-8')
    briefkopf_raw, body = split_briefkopf(md)
    bk_lines = briefkopf_raw.count('\n') if briefkopf_raw else 0
    body_lines = body.count('\n')
    print(f'  [Split]     Briefkopf {bk_lines} Zeilen, Body {body_lines} Zeilen')
    body = protect_signature_block(body)
    briefkopf_tex = briefkopf_to_latex(briefkopf_raw) if briefkopf_raw else ''
    run_pandoc(
        md_text    = body,
        output     = output,
        template   = TEMPLATES / 'schriftsatz.latex',
        extra_vars = {'briefkopf': briefkopf_tex} if briefkopf_tex else {},
    )


# ── Kalender-Rendering (matplotlib) ──────────────────────────────────────────

MONTH_DE_TO_NUM = {
    'Januar': 1, 'Februar': 2, 'März': 3, 'April': 4,
    'Mai': 5, 'Juni': 6, 'Juli': 7, 'August': 8,
    'September': 9, 'Oktober': 10, 'November': 11, 'Dezember': 12,
}

CELL_COLORS = {'V': '#BDD7EE', 'M': '#FCE4D6', '—': '#E8E8E8', '': '#FFFFFF'}
FLAG_COLORS = {'F': '#C00000', 'K': '#E07000', '!': '#C00000', '~': '#888888'}


def parse_kalender_md(md: str) -> list:
    """Parst kalender.md → Liste von Monatsdicts."""
    clean = strip_internal_notes(strip_template_hints(strip_comments(md)))
    sections = re.split(r'\n---\n', clean)
    MONTH_RE = re.compile(
        r'^(Januar|Februar|März|April|Mai|Juni|Juli|August|'
        r'September|Oktober|November|Dezember)\s+(\d{4})'
        r'(?:\s+\(([^)]*)\))?', re.MULTILINE
    )
    CELL_RE = re.compile(r'^\s*(\d+)\s*([!~]?)([VM\u2014]?)([FK]*)\s*$')

    months = []
    for section in sections:
        section = section.strip()
        m = MONTH_RE.search(section)
        if not m:
            continue
        month_name = m.group(1)
        year       = int(m.group(2))
        hint       = (m.group(3) or '').strip()

        # Zellen aus ASCII-Grid lesen
        raw_cells = []
        for line in section.splitlines():
            if '│' not in line or 'Mo' in line or '─' in line:
                continue
            for field in line.split('│')[1:-1]:
                cm = CELL_RE.match(field)
                if cm and cm.group(1):
                    raw_cells.append({
                        'day':      int(cm.group(1)),
                        'modifier': cm.group(2),
                        'betreuer': cm.group(3),
                        'flags':    set(cm.group(4)),
                    })
                else:
                    raw_cells.append(None)  # leeres Feld im Grid

        # Ereignisse lesen (interne Anmerkungen schon entfernt)
        ereignisse = []
        in_erg = False
        for line in section.splitlines():
            if re.match(r'Ereignisse:', line.strip()):
                in_erg = True
                continue
            if in_erg and line.strip().startswith('-'):
                ereignisse.append(line.strip()[1:].strip())

        months.append({
            'title':      f'{month_name} {year}',
            'month_num':  MONTH_DE_TO_NUM[month_name],
            'year':       year,
            'hint':       hint,
            'raw_cells':  raw_cells,
            'ereignisse': ereignisse,
        })
    return months


def _axes_rect(col: int, row: int) -> tuple:
    """Gibt (x, y, w, h) in Figure-Koordinaten zurück. 4 Spalten, 2 Reihen."""
    ML, MR, MT, MB = 0.02, 0.02, 0.04, 0.02
    HG, VG = 0.010, 0.025
    col_w = (1 - ML - MR - 3 * HG) / 4
    row_h = (1 - MT - MB - VG) / 2
    x = ML + col * (col_w + HG)
    y = 1 - MT - (row + 1) * row_h - row * VG
    return x, y, col_w, row_h


def _draw_month(ax, mdata: dict):
    """Zeichnet einen Monat in die übergebene Axes."""
    import calendar as cal_mod
    import matplotlib.patches as patches

    month_num = mdata['month_num']
    year      = mdata['year']
    first_wd, n_days = cal_mod.monthrange(year, month_num)  # 0=Mo

    ax.set_xlim(0, 7)
    ax.set_ylim(0, 8)   # 1 Titel + 1 Header + 6 Wochen
    ax.set_aspect('auto')
    ax.axis('off')

    WEEKDAYS = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']

    # Titel
    title_y = 7.6
    ax.text(3.5, title_y, mdata['title'],
            ha='center', va='center', fontsize=7.5, fontweight='bold',
            color='#1F3864')
    if mdata['hint']:
        hint = mdata['hint'] if len(mdata['hint']) <= 55 else mdata['hint'][:52] + '…'
        ax.text(3.5, 7.15, hint,
                ha='center', va='center', fontsize=4.5, color='#555555')

    # Wochentag-Header
    for c, wd in enumerate(WEEKDAYS):
        fc = '#2F5496' if c < 5 else '#5B7EC9'
        ax.add_patch(patches.Rectangle(
            (c, 6), 1, 0.9, facecolor=fc, edgecolor='white', lw=0.4))
        ax.text(c + 0.5, 6.45, wd,
                ha='center', va='center', fontsize=5.5,
                color='white', fontweight='bold')

    # Datumszellen
    for day in range(1, n_days + 1):
        idx = first_wd + day - 1
        c   = idx % 7
        r   = idx // 7          # Woche (0 = erste)
        y0  = 5 - r             # y-Unterkante (von oben nach unten)

        # Zell-Daten aus raw_cells suchen
        cell = next((x for x in mdata['raw_cells']
                     if x and x['day'] == day), None)
        betreuer = cell['betreuer'] if cell else ''
        modifier = cell['modifier'] if cell else ''
        flags    = cell['flags']    if cell else set()

        bg = CELL_COLORS.get(betreuer, '#FFFFFF')
        ax.add_patch(patches.Rectangle(
            (c, y0), 1, 1, facecolor=bg, edgecolor='#CCCCCC', lw=0.35))

        # Tageszahl
        day_color = FLAG_COLORS['F'] if 'F' in flags else '#222222'
        ax.text(c + 0.12, y0 + 0.72, str(day),
                fontsize=5, va='center', color=day_color)

        # Betreuer-Kürzel
        if betreuer and betreuer != '—':
            tc = '#1A4F8A' if betreuer == 'V' else '#B22222'
            ax.text(c + 0.5, y0 + 0.32, betreuer,
                    ha='center', va='center', fontsize=6.5,
                    fontweight='bold', color=tc)

        # Flags / Modifier (oben rechts)
        extra = modifier + ''.join(sorted(flags - {'F'}))
        if extra:
            ec = FLAG_COLORS.get(extra[0], '#888888')
            ax.text(c + 0.90, y0 + 0.72, extra,
                    ha='right', va='center', fontsize=4, color=ec)

    # Leere Zellen (vor erstem Tag)
    for c in range(first_wd):
        ax.add_patch(patches.Rectangle(
            (c, 5), 1, 1, facecolor='#F5F5F5', edgecolor='#E0E0E0', lw=0.25))

    # Leere Zellen (nach letztem Tag)
    last_idx = first_wd + n_days - 1
    last_c   = last_idx % 7
    last_r   = last_idx // 7
    for c in range(last_c + 1, 7):
        ax.add_patch(patches.Rectangle(
            (c, 5 - last_r), 1, 1, facecolor='#F5F5F5',
            edgecolor='#E0E0E0', lw=0.25))


def _render_ereignisse(pdf, months: list):
    """Rendert eine oder mehrere Ereignisse-Seiten."""
    import matplotlib.pyplot as plt

    COLOR_HEAD = '#1F3864'
    lines = []
    for m in months:
        if not m['ereignisse']:
            continue
        lines.append(('h', m['title']))
        for e in m['ereignisse']:
            lines.append(('e', e))
        lines.append(('s', ''))

    if not lines:
        return

    def new_page():
        fig = plt.figure(figsize=(29.7 / 2.54, 21.0 / 2.54))
        ax  = fig.add_axes([0.05, 0.04, 0.90, 0.92])
        ax.axis('off')
        ax.text(0.0, 1.01, 'Ereignisse', transform=ax.transAxes,
                fontsize=11, fontweight='bold', va='bottom', color=COLOR_HEAD)
        return fig, ax, 0.97

    fig, ax, y = new_page()
    for kind, text in lines:
        if kind == 'h':
            if y < 0.12:
                pdf.savefig(fig, bbox_inches='tight')
                plt.close(fig)
                fig, ax, y = new_page()
            ax.text(0.0, y, text, transform=ax.transAxes,
                    fontsize=8.5, fontweight='bold', va='top', color=COLOR_HEAD)
            y -= 0.028
        elif kind == 'e':
            if y < 0.05:
                pdf.savefig(fig, bbox_inches='tight')
                plt.close(fig)
                fig, ax, y = new_page()
            ax.text(0.015, y, f'– {text}', transform=ax.transAxes,
                    fontsize=7, va='top')
            y -= 0.020
        else:
            y -= 0.010
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)


def _render_legende(pdf):
    """Rendert eine Legendenseite als erste Seite des Kalender-PDFs."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    COLOR_HEAD = '#1F3864'
    fig = plt.figure(figsize=(29.7 / 2.54, 21.0 / 2.54), facecolor='white')
    ax  = fig.add_axes([0.05, 0.05, 0.90, 0.90])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Titel
    ax.text(5, 6.65, 'Betreuungskalender — Legende',
            ha='center', va='center', fontsize=14, fontweight='bold',
            color=COLOR_HEAD)

    # ── Spalte 1: Betreuung ─────────────────────────────────────────────────
    ax.text(0.1, 6.1, 'Betreuung', fontsize=10, fontweight='bold',
            va='center', color=COLOR_HEAD)

    betreuung = [
        ('#BDD7EE', '#1A4F8A', 'V', 'Vater'),
        ('#FCE4D6', '#B22222', 'M', 'Mutter'),
        ('#E8E8E8', '#444444', '—', 'Kein WM-Eintrag (vor Wechselmodell-Start)'),
        ('#FFFFFF', '#444444', '',  'Keine Angabe'),
    ]
    for i, (bg, tc, kuerzel, label) in enumerate(betreuung):
        y = 5.5 - i * 0.75
        # Beispielzelle
        ax.add_patch(patches.Rectangle(
            (0.1, y - 0.28), 0.7, 0.56,
            facecolor=bg, edgecolor='#AAAAAA', lw=0.8))
        if kuerzel:
            ax.text(0.45, y, kuerzel, ha='center', va='center',
                    fontsize=9, fontweight='bold', color=tc)
        ax.text(1.0, y, label, va='center', fontsize=8.5)

    # ── Spalte 2: Zellenaufbau ──────────────────────────────────────────────
    ax.text(5.0, 6.1, 'Aufbau einer Tageszelle', fontsize=10,
            fontweight='bold', va='center', color=COLOR_HEAD)

    # Beispielzelle groß gezeichnet
    cw, ch = 1.8, 1.4
    cx, cy = 5.0, 4.55
    ax.add_patch(patches.Rectangle(
        (cx, cy), cw, ch, facecolor='#BDD7EE', edgecolor='#888888', lw=1.0))
    # Tageszahl oben links
    ax.text(cx + 0.12, cy + ch - 0.22, '15',
            fontsize=10, va='center', color='#222222')
    # Betreuer-Kürzel mittig
    ax.text(cx + cw/2, cy + ch/2 - 0.1, 'V',
            ha='center', va='center', fontsize=13, fontweight='bold',
            color='#1A4F8A')
    # Flag oben rechts
    ax.text(cx + cw - 0.10, cy + ch - 0.22, 'F',
            ha='right', va='center', fontsize=8, color='#C00000')

    # Pfeile und Beschriftungen
    arrow = dict(arrowstyle='->', color='#333333', lw=0.8)
    ax.annotate('Tageszahl', xy=(cx + 0.18, cy + ch - 0.22),
                xytext=(cx - 0.8, cy + ch + 0.05),
                fontsize=7.5, arrowprops=arrow, va='center')
    ax.annotate('Betreuer (V / M)', xy=(cx + cw/2, cy + ch/2 - 0.1),
                xytext=(cx + cw + 0.15, cy + ch/2 + 0.15),
                fontsize=7.5, arrowprops=arrow, va='center')
    ax.annotate('Markierung', xy=(cx + cw - 0.12, cy + ch - 0.22),
                xytext=(cx + cw + 0.15, cy + ch - 0.05),
                fontsize=7.5, arrowprops=arrow, va='center')

    # ── Spalte 2: Markierungen ──────────────────────────────────────────────
    ax.text(5.0, 3.35, 'Markierungen', fontsize=10, fontweight='bold',
            va='center', color=COLOR_HEAD)

    markierungen = [
        ('#C00000', 'F',  'Feiertag (Tageszahl ebenfalls rot)'),
        ('#E07000', 'K',  'Kind krank'),
        ('#C00000', '!',  'Widerspruch zu Beleg (abweichend von Plan)'),
        ('#888888', '~',  'Datum unsicher'),
        ('#444444', 'FK', 'Kombination möglich (z. B. Feiertag + krank)'),
    ]
    for i, (color, kuerzel, label) in enumerate(markierungen):
        y = 2.85 - i * 0.55
        ax.text(5.1, y, kuerzel, va='center', fontsize=8.5,
                fontweight='bold', color=color)
        ax.text(5.6, y, label, va='center', fontsize=8.5)

    # ── Spalte 2: Sonderzeichen ─────────────────────────────────────────────
    ax.text(5.0, 0.55, 'Sonderzeichen in Ereignissen', fontsize=10,
            fontweight='bold', va='center', color=COLOR_HEAD)
    sonder = [
        ('(Text)', 'Offizieller Eintrag — erscheint in Anlagen'),
        ('[Text]', 'Nur interner Hinweis — wird beim PDF-Export entfernt'),
    ]
    for i, (kuerzel, label) in enumerate(sonder):
        y = 0.08 - i * 0.40 + 0.35
        ax.text(5.1, y, kuerzel, va='center', fontsize=8, color='#333333',
                fontstyle='italic')
        ax.text(6.5, y, label, va='center', fontsize=8)

    # Trennlinien zwischen Spalten
    ax.axvline(x=4.7, ymin=0.01, ymax=0.97, color='#CCCCCC', lw=0.8)

    pdf.savefig(fig, bbox_inches='tight', dpi=150)
    plt.close(fig)


def _build_kalender_matplotlib(md: str, output: Path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    months = parse_kalender_md(md)
    if not months:
        raise ValueError('Keine Monatsblöcke gefunden')

    with PdfPages(str(output)) as pdf:
        _render_legende(pdf)
        for page_start in range(0, len(months), 8):
            page_months = months[page_start:page_start + 8]
            fig = plt.figure(figsize=(29.7 / 2.54, 21.0 / 2.54),
                             facecolor='white')
            for slot, mdata in enumerate(page_months):
                col, row = slot % 4, slot // 4
                ax = fig.add_axes(_axes_rect(col, row))
                _draw_month(ax, mdata)
            for slot in range(len(page_months), 8):
                col, row = slot % 4, slot // 4
                ax = fig.add_axes(_axes_rect(col, row))
                ax.axis('off')
            pdf.savefig(fig, bbox_inches='tight', dpi=150)
            plt.close(fig)

        _render_ereignisse(pdf, months)

    print(f'  [matplotlib] {len(months)} Monate gerendert')


def build_kalender(md_path: Path, output: Path):
    md = md_path.read_text(encoding='utf-8')
    try:
        _build_kalender_matplotlib(md, output)
    except Exception as exc:
        print(f'  [Warnung] matplotlib fehlgeschlagen ({exc}) — Pandoc-Fallback')
        clean = strip_internal_notes(strip_template_hints(strip_comments(md)))
        clean = re.sub(
            r'((?:^[┌├└│].*\n)+)',
            lambda m: '```\n' + m.group(0) + '```\n',
            clean, flags=re.MULTILINE
        )
        run_pandoc(clean, output, extra_flags=[
            '--from', 'markdown-yaml_metadata_block',
            '-V', 'geometry:margin=1.5cm,landscape',
        ])


def build_deckblatt(anlage: str, titel: str, datei: str, az: str, output: Path):
    md = f"""# Anlage {anlage}

\\vspace{{3cm}}

**{titel or datei or 'Originaldokument'}**

Aktenzeichen: {az}

\\vspace{{2cm}}

*Das Original dieses Dokuments wird separat eingereicht.*
"""
    run_pandoc(md, output, template=TEMPLATES / 'schriftsatz.latex')


def parse_originale(anlagen_md: Path) -> list:
    """Liest Original-Anlagen aus anlagen.md."""
    if not anlagen_md.exists():
        return []
    result = []
    for line in anlagen_md.read_text(encoding='utf-8').splitlines():
        if not line.startswith('|'):
            continue
        cols = [c.strip() for c in line.split('|') if c.strip()]
        if (len(cols) >= 4
                and re.match(r'^[A-Z]\d*$', cols[0])
                and 'original' in cols[3].lower()):
            result.append((cols[0], cols[1], cols[2]))
    return result

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    check_deps()

    args          = sys.argv[1:]
    verfahren_arg = next((a for a in args if not a.startswith('--')), None)
    only          = next((a.replace('--only=', '') for a in args
                          if a.startswith('--only=')), 'all')

    if not verfahren_arg:
        print("Verwendung: python scripts/generate-pdf.py <verfahren-pfad> [--only=erwiderung|kalender|deckblatt]")
        sys.exit(1)

    verfahren  = Path(verfahren_arg)
    az         = verfahren.name.upper().replace('-', ' ')
    output_dir = verfahren / 'output'
    output_dir.mkdir(exist_ok=True)

    if only in ('all', 'erwiderung'):
        src = verfahren / 'erwiderung' / 'erwiderung.md'
        if src.exists():
            dst = output_dir / 'erwiderung.pdf'
            print(f"Generiere erwiderung.pdf …", end=' ', flush=True)
            build_erwiderung(src, dst)
            print(f"✓  {dst}")
        else:
            print("  erwiderung.md nicht gefunden — übersprungen.")

    if only in ('all', 'kalender'):
        src = verfahren / 'sachverhalt' / 'kalender.md'
        if src.exists():
            dst = output_dir / 'kalender.pdf'
            print(f"Generiere kalender.pdf …", end=' ', flush=True)
            build_kalender(src, dst)
            print(f"✓  {dst}")
        else:
            print("  kalender.md nicht gefunden — übersprungen.")

    if only in ('all', 'deckblatt'):
        anlagen_src = verfahren / 'erwiderung' / 'anlagen.md'
        for anlage, titel, datei in parse_originale(anlagen_src):
            dst = output_dir / f'deckblatt-{anlage}.pdf'
            print(f"Generiere deckblatt-{anlage}.pdf …", end=' ', flush=True)
            build_deckblatt(anlage, titel, datei, az, dst)
            print(f"✓  {dst}")

    print(f"\nFertig. PDFs liegen in: {output_dir}")


if __name__ == '__main__':
    main()
