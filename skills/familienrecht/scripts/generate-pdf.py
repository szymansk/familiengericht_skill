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
    """Trennt Briefkopf (vor erstem ---) vom Schriftsatz-Body."""
    clean = strip_comments(md)
    m = re.search(r'\n---\n', clean)
    if not m:
        return '', clean
    return clean[:m.start()], clean[m.end():]

def briefkopf_to_latex(text: str) -> str:
    """Konvertiert Briefkopf-Zeilen zu LaTeX:
    - Leerzeilen          → \\medskip (Abstand zwischen Adressblöcken)
    - Datum (den \\d)     → rechtsbündig via \\hfill
    - Aktenzeichen:       → fett
    - Erwiderung / Antrag / Stellungnahme → fett + unterstrichen
    - Alle anderen Zeilen → linksbündig mit explizitem Zeilenumbruch
    """
    lines = [l.rstrip() for l in text.split('\n')]
    out = []
    for line in lines:
        if line.startswith('#') or line.startswith('>'):
            continue
        if not line.strip():
            out.append('\\medskip')
            continue
        # Markdown Bold → LaTeX
        line = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', line)
        if re.search(r'\d{1,2}\.\s*(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s+\d{4}', line):
            out.append(f'\\hfill {line}\\\\[1mm]')
        elif 'Aktenzeichen:' in line:
            out.append(f'\\noindent\\textbf{{{line}}}\\\\[3mm]')
        elif re.match(r'(Erwiderung|Antrag|Stellungnahme)', line):
            out.append(f'\\noindent\\textbf{{\\underline{{{line}}}}}\\\\[4mm]')
        else:
            out.append(f'\\noindent {line}\\\\[0mm]')
    return '\n'.join(out)

# ── Pandoc aufrufen ───────────────────────────────────────────────────────────

# Gemeinsame Basis-Flags für alle Dokumente
PANDOC_BASE = [
    '--pdf-engine', 'xelatex',
    '-V', 'lang=de-DE',
    '-V', 'papersize=a4',
    '-V', 'geometry:margin=2.5cm',
    '-V', 'mainfont=Arial',
    '-V', 'fontsize=11pt',
    '-V', 'linestretch=1.2',
]

def run_pandoc(md_text: str, output: Path, extra_flags: list = None,
               extra_vars: dict = None, template: Path = None):
    """Schreibt MD in Tempfile und ruft Pandoc auf."""
    with tempfile.NamedTemporaryFile(suffix='.md', mode='w',
                                     encoding='utf-8', delete=False) as f:
        f.write(md_text)
        tmp_md = f.name

    cmd = ['pandoc', tmp_md, '--output', str(output)] + PANDOC_BASE
    if template:
        cmd += ['--template', str(template)]
    if extra_flags:
        cmd += extra_flags
    if extra_vars:
        for k, v in extra_vars.items():
            cmd += ['--variable', f'{k}={v}']

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"\nPandoc-Fehler:\n{result.stderr}")
            sys.exit(1)
    finally:
        os.unlink(tmp_md)

# ── Dokumente generieren ──────────────────────────────────────────────────────

def build_erwiderung(md_path: Path, output: Path):
    md = md_path.read_text(encoding='utf-8')
    briefkopf_raw, body = split_briefkopf(md)
    briefkopf_tex = briefkopf_to_latex(briefkopf_raw) if briefkopf_raw else ''
    run_pandoc(
        md_text    = body,
        output     = output,
        template   = TEMPLATES / 'schriftsatz.latex',
        extra_vars = {'briefkopf': briefkopf_tex} if briefkopf_tex else {},
    )


def build_kalender(md_path: Path, output: Path):
    md = md_path.read_text(encoding='utf-8')
    clean = strip_internal_notes(strip_comments(md))
    # Kalender-ASCII-Tabellen in Verbatim-Block für LaTeX wrappen
    clean = re.sub(
        r'((?:^[┌├└│].*\n)+)',
        lambda m: '```\n' + m.group(0) + '```\n',
        clean, flags=re.MULTILINE
    )
    run_pandoc(clean, output, extra_flags=[
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
