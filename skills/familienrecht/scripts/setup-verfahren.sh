#!/usr/bin/env bash
# setup-verfahren.sh — Legt ein neues Familienrechtsverfahren mit Ordnerstruktur und Templates an.
#
# Verwendung:
#   ./setup-verfahren.sh "4 F 42/25"
#
# Der Az.-String wird als Ordnername sanitized (Leerzeichen → Bindestriche, Slash → Bindestrich).

set -euo pipefail

# ── Argument prüfen ──────────────────────────────────────────────────────────

if [[ $# -lt 1 ]]; then
  echo "Verwendung: $0 <Aktenzeichen>"
  echo "Beispiel:   $0 \"4 F 42/25\""
  exit 1
fi

AZ="$1"

# Ordnersicherer Kurzname: Leerzeichen → -, Slash → -, Kleinbuchstaben
AZ_DIR=$(echo "$AZ" | tr '[:upper:]' '[:lower:]' | sed 's/[ /]/-/g' | sed 's/--*/-/g')

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES="$SCRIPT_DIR/../assets/verfahren"
TARGET="$(pwd)/verfahren/$AZ_DIR"

# ── Zielordner prüfen ────────────────────────────────────────────────────────

if [[ -d "$TARGET" ]]; then
  echo "Fehler: Verfahren '$AZ_DIR' existiert bereits unter $TARGET"
  exit 1
fi

echo "Lege Verfahren an: $AZ  →  verfahren/$AZ_DIR"

# ── Ordnerstruktur erstellen ─────────────────────────────────────────────────

mkdir -p \
  "$TARGET/sachverhalt" \
  "$TARGET/gegenseite" \
  "$TARGET/belege/originale" \
  "$TARGET/belege/whatsapp" \
  "$TARGET/belege/emails" \
  "$TARGET/belege/voicenotes" \
  "$TARGET/belege/dokumente" \
  "$TARGET/erwiderung" \
  "$TARGET/vorbereitung" \
  "$TARGET/output"

# ── Templates kopieren und Platzhalter ersetzen ──────────────────────────────

replace() {
  # replace <src> <dst>
  # Trennzeichen | statt / damit Aktenzeichen-Slashes kein Problem sind
  local src="$1"
  local dst="$2"
  local az_escaped
  az_escaped=$(printf '%s' "$AZ" | sed 's|[&\]|\\&|g')
  sed \
    -e "s|\[Aktenzeichen\]|$az_escaped|g" \
    -e "s|\[Verfahrensbezeichnung\]|$az_escaped|g" \
    "$src" > "$dst"
}

replace "$TEMPLATES/kontext.md"                      "$TARGET/kontext.md"
replace "$TEMPLATES/sachverhalt/fakten.md"          "$TARGET/sachverhalt/fakten.md"
replace "$TEMPLATES/sachverhalt/kalender.md"         "$TARGET/sachverhalt/kalender.md"
replace "$TEMPLATES/sachverhalt/timeline.md"         "$TARGET/sachverhalt/timeline.md"
replace "$TEMPLATES/sachverhalt/offene-fragen.md"    "$TARGET/sachverhalt/offene-fragen.md"
replace "$TEMPLATES/sachverhalt/notizen.md"          "$TARGET/sachverhalt/notizen.md"
replace "$TEMPLATES/sachverhalt/entscheidungen.md"   "$TARGET/sachverhalt/entscheidungen.md"
replace "$TEMPLATES/erwiderung/erwiderung.md"        "$TARGET/erwiderung/erwiderung.md"
replace "$TEMPLATES/erwiderung/anlagen.md"           "$TARGET/erwiderung/anlagen.md"
replace "$TEMPLATES/erwiderung/nur-muendlich.md"     "$TARGET/erwiderung/nur-muendlich.md"
replace "$TEMPLATES/vorbereitung/verhandlung.md"     "$TARGET/vorbereitung/verhandlung.md"

# ── Gegenseite-Stubs anlegen ─────────────────────────────────────────────────

cat > "$TARGET/gegenseite/antrag.md" <<EOF
# Antrag der Gegenseite — Az. $AZ

> Dieses Dokument wird befüllt, sobald der Antrag importiert wird (z.B. via markitdown).

EOF

cat > "$TARGET/gegenseite/protokoll-km.md" <<EOF
# Protokoll / Anlagen der Gegenseite — Az. $AZ

> Hier werden Protokolle und sonstige Anlagen der Gegenseite gesammelt.

EOF

# ── .gitkeep für leere Belege-Unterordner ────────────────────────────────────

touch \
  "$TARGET/belege/originale/.gitkeep" \
  "$TARGET/belege/whatsapp/.gitkeep" \
  "$TARGET/belege/emails/.gitkeep" \
  "$TARGET/belege/voicenotes/.gitkeep" \
  "$TARGET/belege/dokumente/.gitkeep" \
  "$TARGET/output/.gitkeep"

# ── .gitignore für Output ─────────────────────────────────────────────────────

cat > "$TARGET/output/.gitignore" <<'EOF'
# Generierte DOCX/PDF werden nicht eingecheckt
*.docx
*.pdf
!.gitkeep
EOF

# ── .venv in Root-.gitignore sicherstellen ────────────────────────────────────

ROOT_GITIGNORE="$(pwd)/.gitignore"
if ! grep -qF '.venv/' "$ROOT_GITIGNORE" 2>/dev/null; then
  printf '\n# Python venv\n.venv/\n' >> "$ROOT_GITIGNORE"
  echo ".venv/ zu $ROOT_GITIGNORE hinzugefügt"
fi

# ── Ergebnis ──────────────────────────────────────────────────────────────────

echo ""
echo "Verfahren erfolgreich angelegt:"
echo ""
find "$TARGET" -not -name '.gitkeep' | sort | sed "s|$(pwd)/||"
echo ""
echo "Nächster Schritt: Phase 1 — sachverhalt/fakten.md befüllen."
