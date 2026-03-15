#!/usr/bin/env python3
"""
combine-pdf.py — Führt alle Verfahrensdokumente zu einer einzigen PDF zusammen.

Reihenfolge:
  1. erwiderung.pdf  (via generate-pdf.py falls noch nicht vorhanden/aktuell)
  2. kalender.pdf
  3. Für jede Original-Anlage: deckblatt-{X}.pdf + Original-Datei
  4. Zusammenführen → output/einreichung.pdf

Voraussetzung:
  bash scripts/setup.sh ausgeführt (installiert pypdf, pillow, pandoc, xelatex)

Verwendung:
  python scripts/combine-pdf.py verfahren/4-f-42-25
"""

import sys
import re
import os
import subprocess
from pathlib import Path

# ── Venv auto-detect: pypdf/pillow im .venv aktivieren ───────────────────────

def _find_venv_python() -> str | None:
    candidates = [
        Path(os.getcwd()) / '.venv' / 'bin' / 'python',
        Path(__file__).parents[3] / '.venv' / 'bin' / 'python',
    ]
    return next((str(p) for p in candidates if p.exists()), None)

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    venv_py = _find_venv_python()
    if venv_py and venv_py != sys.executable:
        os.execv(venv_py, [venv_py] + sys.argv)
    print("Fehler: pypdf nicht installiert. Bitte ausführen: bash scripts/setup.sh")
    sys.exit(1)

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

SCRIPT_DIR = Path(__file__).parent.resolve()

# ── Hilfsfunktionen ───────────────────────────────────────────────────────────

def is_outdated(pdf: Path, src: Path) -> bool:
    """Gibt True zurück wenn PDF fehlt oder älter als die Quelldatei."""
    return not pdf.exists() or (src.exists() and src.stat().st_mtime > pdf.stat().st_mtime)


def generate_pdf(verfahren: Path, only: str):
    """Ruft generate-pdf.py auf."""
    script = SCRIPT_DIR / 'generate-pdf.py'
    result = subprocess.run(
        [sys.executable, str(script), str(verfahren), f'--only={only}'],
        capture_output=False
    )
    if result.returncode != 0:
        print(f"  ✗ Fehler bei generate-pdf.py --only={only}")
        sys.exit(1)


def image_to_pdf(img_path: Path, output_dir: Path) -> Path:
    if not PILLOW_AVAILABLE:
        raise RuntimeError(
            f"Pillow nicht installiert — {img_path.name} kann nicht konvertiert werden.\n"
            "Bitte ausführen: bash scripts/setup.sh"
        )
    out = output_dir / (img_path.stem + '_orig.pdf')
    img = Image.open(img_path).convert('RGB')
    img.save(out, 'PDF', resolution=150)
    return out


def to_pdf(src: Path, output_dir: Path) -> Path:
    suffix = src.suffix.lower()
    if suffix == '.pdf':
        return src
    elif suffix in ('.jpg', '.jpeg', '.png', '.tiff', '.bmp'):
        return image_to_pdf(src, output_dir)
    else:
        raise ValueError(f"Nicht unterstütztes Format für Zusammenführung: {src.name}")


def parse_originale(anlagen_md: Path) -> list:
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


def merge_pdfs(pdf_paths: list, output: Path):
    writer = PdfWriter()
    for p in pdf_paths:
        if not p.exists():
            print(f"  ⚠ Nicht gefunden, übersprungen: {p}")
            continue
        for page in PdfReader(str(p)).pages:
            writer.add_page(page)
    with open(output, 'wb') as f:
        writer.write(f)

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Verwendung: python scripts/combine-pdf.py <verfahren-pfad>")
        sys.exit(1)

    verfahren  = Path(sys.argv[1])
    output_dir = verfahren / 'output'
    anlagen_md = verfahren / 'erwiderung' / 'anlagen.md'
    output_dir.mkdir(exist_ok=True)

    to_merge = []

    # 1. Erwiderung
    erwiderung_md  = verfahren / 'erwiderung' / 'erwiderung.md'
    erwiderung_pdf = output_dir / 'erwiderung.pdf'
    if erwiderung_md.exists():
        if is_outdated(erwiderung_pdf, erwiderung_md):
            generate_pdf(verfahren, 'erwiderung')
        to_merge.append(erwiderung_pdf)
    else:
        print("  ⚠ erwiderung.md nicht gefunden — übersprungen")

    # 2. Kalender
    kalender_md  = verfahren / 'sachverhalt' / 'kalender.md'
    kalender_pdf = output_dir / 'kalender.pdf'
    if kalender_md.exists():
        if is_outdated(kalender_pdf, kalender_md):
            generate_pdf(verfahren, 'kalender')
        to_merge.append(kalender_pdf)

    # 3. Originale mit Deckblättern
    for anlage, titel, datei in parse_originale(anlagen_md):
        deckblatt_pdf = output_dir / f'deckblatt-{anlage}.pdf'
        if not deckblatt_pdf.exists():
            generate_pdf(verfahren, 'deckblatt')

        if deckblatt_pdf.exists():
            to_merge.append(deckblatt_pdf)

        kandidaten = [
            verfahren / datei if datei else None,
            verfahren / 'belege' / 'originale' / datei if datei else None,
        ]
        original_path = next((p for p in kandidaten if p and p.exists()), None)
        if original_path:
            print(f"  Füge Original hinzu: {original_path.name}")
            to_merge.append(to_pdf(original_path, output_dir))
        else:
            print(f"  ⚠ Original für Anlage {anlage} nicht gefunden: {datei}")

    if not to_merge:
        print("Keine Dokumente zum Zusammenführen gefunden.")
        sys.exit(1)

    output_pdf = output_dir / 'einreichung.pdf'
    print(f"\nFühre {len(to_merge)} Dokument(e) zusammen …")
    merge_pdfs(to_merge, output_pdf)
    print(f"✓  {output_pdf}")


if __name__ == '__main__':
    main()
