#!/usr/bin/env bash
# push.sh — Patch-Version erhöhen und pushen.
# Immer anstelle von "git push" verwenden.

set -euo pipefail

PLUGIN_JSON=".claude-plugin/plugin.json"
MARKETPLACE_JSON=".claude-plugin/marketplace.json"

# Aktuelle Version lesen
CURRENT=$(grep '"version"' "$PLUGIN_JSON" | head -1 | sed 's/.*"version": *"\([^"]*\)".*/\1/')
MAJOR=$(echo "$CURRENT" | cut -d. -f1)
MINOR=$(echo "$CURRENT" | cut -d. -f2)
PATCH=$(echo "$CURRENT" | cut -d. -f3)

NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"

# Dateien aktualisieren
sed -i '' "s/\"version\": \"$CURRENT\"/\"version\": \"$NEW_VERSION\"/g" "$PLUGIN_JSON"
sed -i '' "s/\"version\": \"$CURRENT\"/\"version\": \"$NEW_VERSION\"/g" "$MARKETPLACE_JSON"

# In letzten lokalen Commit einbauen und pushen
git add "$PLUGIN_JSON" "$MARKETPLACE_JSON"
git commit --amend --no-edit --no-verify
git push --no-verify "$@"

echo "Version: $CURRENT → $NEW_VERSION"
