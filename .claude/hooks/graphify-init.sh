#!/usr/bin/env bash
# Initialize graphify + Claude Code SessionStart hook in a new project.
#
# Usage (run from anywhere, script is self-locating):
#   bash /path/to/cameron-wiki/.claude/hooks/graphify-init.sh <target-project-path>
#
# What it does:
#   1. Copies load-graph.sh into <target>/.claude/hooks/
#   2. Creates <target>/.claude/settings.json with the SessionStart hook
#   3. Prints env var + next-step instructions

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WIKI_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TARGET="${1:-}"

if [ -z "$TARGET" ]; then
    echo "Usage: graphify-init.sh <target-project-path>" >&2
    exit 1
fi

if [ ! -d "$TARGET" ]; then
    echo "Error: '$TARGET' is not a directory." >&2
    exit 1
fi

TARGET="$(cd "$TARGET" && pwd -P)"

# Don't init into cameron-wiki itself
if [ "$TARGET" = "$WIKI_ROOT" ]; then
    echo "Error: target cannot be cameron-wiki itself (it already has the hook)." >&2
    exit 1
fi

echo "Initializing graphify hook in: $TARGET"

# Create .claude/hooks/ in target
mkdir -p "${TARGET}/.claude/hooks"

# Copy hook script
cp "${SCRIPT_DIR}/load-graph.sh" "${TARGET}/.claude/hooks/load-graph.sh"
chmod +x "${TARGET}/.claude/hooks/load-graph.sh"
echo "✓ Copied load-graph.sh → ${TARGET}/.claude/hooks/"

# Create settings.json only if it doesn't exist
SETTINGS="${TARGET}/.claude/settings.json"
if [ ! -f "$SETTINGS" ]; then
    cat > "$SETTINGS" << 'EOF'
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/load-graph.sh",
            "async": false
          }
        ]
      }
    ]
  }
}
EOF
    echo "✓ Created ${TARGET}/.claude/settings.json"
else
    echo "ℹ  ${TARGET}/.claude/settings.json already exists — add the SessionStart hook manually if needed"
fi

echo ""
echo "────────────────────────────────────────────────────"
echo "Next steps:"
echo ""
echo "  1. Add CAMERON_WIKI_PATH to ~/.zshrc (once per machine):"
echo "       export CAMERON_WIKI_PATH=\"${WIKI_ROOT}\""
echo "     Then: source ~/.zshrc"
echo ""
echo "  2. In the new project, install graphify and build its graph:"
echo "       cd \"${TARGET}\""
echo "       npx add-skill safishamsi/graphify"
echo "       # Open Claude Code and run /graphify"
echo ""
echo "  3. Commit the generated files to git:"
echo "       git add .claude/hooks/load-graph.sh .claude/settings.json"
echo "       git commit -m 'feat: add graphify SessionStart hook'"
echo ""
echo "Each Claude Code session in this project will then inject:"
echo "  • This project's own graph  (~4k tokens)"
echo "  • cameron-wiki master graph (~4k tokens)"
echo "────────────────────────────────────────────────────"
