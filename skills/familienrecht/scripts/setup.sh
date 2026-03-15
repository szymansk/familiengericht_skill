#!/usr/bin/env bash
# setup.sh — Installiert alle Abhängigkeiten des Familienrecht-Skills.
#
# Voraussetzung: macOS mit Homebrew (https://brew.sh)
# Ausführen: bash scripts/setup.sh  (aus dem Arbeitsverzeichnis)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="$(pwd)"

echo "═══════════════════════════════════════════════════"
echo "  Familienrecht-Skill — Setup"
echo "═══════════════════════════════════════════════════"
echo ""

# ── 1. Homebrew ───────────────────────────────────────────────────────────────

if ! command -v brew &>/dev/null; then
  echo "✗ Homebrew nicht gefunden."
  echo "  Bitte installieren: https://brew.sh"
  echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
  exit 1
fi
echo "✓ Homebrew: $(brew --version | head -1)"

# ── 2. Pandoc ─────────────────────────────────────────────────────────────────

if ! command -v pandoc &>/dev/null; then
  echo "→ Installiere Pandoc …"
  brew install pandoc
else
  echo "✓ Pandoc: $(pandoc --version | head -1)"
fi

# ── 3. LaTeX (BasicTeX) ───────────────────────────────────────────────────────

if command -v xelatex &>/dev/null; then
  echo "✓ XeLaTeX: $(xelatex --version | head -1)"
else
  echo "→ Installiere BasicTeX …"
  echo "  (ca. 100 MB — für vollständiges LaTeX alternativ: brew install --cask mactex)"
  brew install --cask basictex
  # PATH aktualisieren
  eval "$(/usr/libexec/path_helper)"
fi

# ── 4. tlmgr-Pakete ───────────────────────────────────────────────────────────

TLMGR="$(command -v tlmgr 2>/dev/null || echo /Library/TeX/texbin/tlmgr)"

if [[ ! -x "$TLMGR" ]]; then
  echo "  ⚠ tlmgr nicht gefunden — LaTeX-Pakete bitte manuell installieren."
else
  echo "→ Aktualisiere tlmgr …"
  sudo "$TLMGR" update --self --quiet || true

  PACKAGES=(
    babel-german
    hyphen-german
    microtype
    parskip
    setspace
    titlesec
    fancyhdr
    booktabs
    longtable
    enumitem
    ulem
    xcolor
    hyperref
    caption
    float
    mdframed
    needspace
    tocloft
    lastpage
  )

  echo "→ Installiere LaTeX-Pakete: ${PACKAGES[*]}"
  sudo "$TLMGR" install "${PACKAGES[@]}" --quiet || true
  echo "✓ LaTeX-Pakete installiert"
fi

# ── 5. Python venv ────────────────────────────────────────────────────────────

VENV="$WORK_DIR/.venv"
if [[ ! -d "$VENV" ]]; then
  echo "→ Erstelle Python venv in .venv …"
  python3 -m venv "$VENV"
fi

echo "→ Installiere Python-Pakete …"
"$VENV/bin/pip" install --upgrade pip --quiet
"$VENV/bin/pip" install markitdown pypdf pillow --quiet
echo "✓ Python: markitdown, pypdf, pillow"

# .venv in .gitignore sicherstellen
if ! grep -qF '.venv/' "$WORK_DIR/.gitignore" 2>/dev/null; then
  printf '\n.venv/\n' >> "$WORK_DIR/.gitignore"
fi

# ── 6. Node / npm ─────────────────────────────────────────────────────────────

if ! command -v node &>/dev/null; then
  echo "→ Installiere Node.js …"
  brew install node
else
  echo "✓ Node.js: $(node --version)"
fi

echo "→ Installiere npm-Pakete (docx) …"
(cd "$SCRIPT_DIR" && npm install --silent)
echo "✓ npm: docx"

# ── Fertig ────────────────────────────────────────────────────────────────────

echo ""
echo "═══════════════════════════════════════════════════"
echo "  Setup abgeschlossen."
echo ""
echo "  Nächster Schritt:"
echo "  Neues Verfahren anlegen:"
echo "  → bash scripts/setup-verfahren.sh \"4 F 42/25\""
echo "═══════════════════════════════════════════════════"
