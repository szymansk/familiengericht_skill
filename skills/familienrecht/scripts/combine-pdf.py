#!/usr/bin/env python3
"""
combine-pdf.py — Führt alle Verfahrensdokumente zu einer einzigen PDF-Datei zusammen.

Reihenfolge:
  1. erwiderung.docx  → erwiderung.pdf  (via LibreOffice)
  2. kalender.docx    → kalender.pdf    (via LibreOffice)
  3. Für jede Original-Anlage in anlagen.md:
       deckblatt-{X}.docx → deckblatt-{X}.pdf  (via LibreOffice)
       + das Original selbst (PDF/JPG/PNG wird ggf. konvertiert)
  4. Alles zusammenführen → output/einreichung.pdf

Voraussetzung:
  pip install pypdf pillow
  LibreOffice installiert (soffice im PATH)

Verwendung:
  python scripts/combine-pdf.py verfahren/4-f-42-25
"""

import sys
import os
import re
import subprocess
import shutil
from pathlib import Path

# ── Abhängigkeiten prüfen ─────────────────────────────────────────────────────

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    print("Fehler: pypdf nicht installiert. Bitte ausführen: pip install pypdf")
    sys.exit(1)

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

SOFFICE = shutil.which('soffice') or shutil.which('libreoffice')

# ── Hilfsfunktionen ───────────────────────────────────────────────────────────

def docx_to_pdf(docx_path: Path, output_dir: Path) -> Path:
    """Konvertiert eine DOCX-Datei zu PDF via LibreOffice."""
    if not SOFFICE:
        raise RuntimeError(
            "LibreOffice nicht gefunden. Bitte installieren: https://www.libreoffice.org\n"
            "Danach erneut versuchen."
        )
    subprocess.run(
        [SOFFICE, '--headless', '--convert-to', 'pdf', '--outdir', str(output_dir), str(docx_path)],
        check=True, capture_output=True
    )
    return output_dir / (docx_path.stem + '.pdf')


def image_to_pdf(img_path: Path, output_dir: Path) -> Path:
    """Konvertiert JPG/PNG zu PDF via Pillow."""
    if not PILLOW_AVAILABLE:
        raise RuntimeError(
            f"Pillow nicht installiert — kann {img_path.name} nicht konvertieren.\n"
            "Bitte ausführen: pip install pillow"
        )
    out = output_dir / (img_path.stem + '.pdf')
    img = Image.open(img_path).convert('RGB')
    img.save(out, 'PDF', resolution=150)
    return out


def to_pdf(src: Path, output_dir: Path) -> Path:
    """Konvertiert beliebige Datei zu PDF."""
    suffix = src.suffix.lower()
    if suffix == '.pdf':
        return src
    elif suffix == '.docx':
        return docx_to_pdf(src, output_dir)
    elif suffix in ('.jpg', '.jpeg', '.png', '.tiff', '.bmp'):
        return image_to_pdf(src, output_dir)
    else:
        raise ValueError(f"Nicht unterstütztes Format: {src.name}")


def parse_originale(anlagen_md: Path):
    """Liest Original-Anlagen aus anlagen.md. Gibt Liste von (anlage, titel, datei) zurück."""
    if not anlagen_md.exists():
        return []
    result = []
    for line in anlagen_md.read_text(encoding='utf-8').splitlines():
        if not line.startswith('|'):
            continue
        cols = [c.strip() for c in line.split('|') if c.strip()]
        if len(cols) >= 3 and re.match(r'^[A-Z]', cols[0]) and 'original' in cols[3].lower() if len(cols) > 3 else False:
            result.append((cols[0], cols[1], cols[2]))
    return result


def merge_pdfs(pdf_paths: list, output: Path):
    writer = PdfWriter()
    for p in pdf_paths:
        if not p.exists():
            print(f"  ⚠ Datei nicht gefunden, übersprungen: {p}")
            continue
        reader = PdfReader(str(p))
        for page in reader.pages:
            writer.add_page(page)
    with open(output, 'wb') as f:
        writer.write(f)

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Verwendung: python scripts/combine-pdf.py <verfahren-pfad>")
        sys.exit(1)

    verfahren = Path(sys.argv[1])
    if not verfahren.exists():
        print(f"Fehler: Verfahren nicht gefunden: {verfahren}")
        sys.exit(1)

    output_dir   = verfahren / 'output'
    anlagen_md   = verfahren / 'erwiderung' / 'anlagen.md'
    output_pdf   = output_dir / 'einreichung.pdf'
    output_dir.mkdir(exist_ok=True)

    to_merge = []

    # 1. Erwiderung
    erwiderung_docx = output_dir / 'erwiderung.docx'
    if erwiderung_docx.exists():
        print("Konvertiere erwiderung.docx …")
        to_merge.append(docx_to_pdf(erwiderung_docx, output_dir))
    else:
        print("  ⚠ erwiderung.docx nicht gefunden — zuerst generate-docx.js ausführen")

    # 2. Kalender
    kalender_docx = output_dir / 'kalender.docx'
    if kalender_docx.exists():
        print("Konvertiere kalender.docx …")
        to_merge.append(docx_to_pdf(kalender_docx, output_dir))

    # 3. Originale mit Deckblättern
    for anlage, titel, datei in parse_originale(anlagen_md):
        deckblatt_docx = output_dir / f'deckblatt-{anlage}.docx'
        if deckblatt_docx.exists():
            print(f"Konvertiere deckblatt-{anlage}.docx …")
            to_merge.append(docx_to_pdf(deckblatt_docx, output_dir))
        else:
            print(f"  ⚠ deckblatt-{anlage}.docx fehlt — zuerst generate-docx.js --only=deckblatt ausführen")

        # Original-Datei suchen (in belege/originale/ oder angegebener Pfad)
        kandidaten = [
            verfahren / datei if datei else None,
            verfahren / 'belege' / 'originale' / datei if datei else None,
        ]
        original_path = next((p for p in kandidaten if p and p.exists()), None)
        if original_path:
            print(f"Füge Original hinzu: {original_path.name} …")
            to_merge.append(to_pdf(original_path, output_dir))
        else:
            print(f"  ⚠ Original für Anlage {anlage} nicht gefunden: {datei}")

    if not to_merge:
        print("\nKeine Dokumente zum Zusammenführen gefunden.")
        sys.exit(1)

    print(f"\nFühre {len(to_merge)} Dokument(e) zusammen → {output_pdf.name} …")
    merge_pdfs(to_merge, output_pdf)
    print(f"✓  {output_pdf}")


if __name__ == '__main__':
    main()
