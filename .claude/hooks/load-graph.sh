#!/usr/bin/env bash
# SessionStart hook: injects graphify knowledge graph into Claude Code context.
# Auto-fires when this project opens in Claude Code.
# Committed to git — syncs across all machines via the repo.
#
# Master wiki graph: set CAMERON_WIKI_PATH in ~/.zshrc to also inject the
# master cameron-wiki graph alongside this project's graph:
#   export CAMERON_WIKI_PATH="/path/to/cameron-wiki"

set -euo pipefail

GRAPH_REPORT="graphify-out/GRAPH_REPORT.md"
GRAPH_JSON="graphify-out/graph.json"

escape_for_json() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    s="${s//$'\t'/\\t}"
    printf '%s' "$s"
}

emit_context() {
    local ctx
    ctx=$(escape_for_json "$1")
    printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' "$ctx"
}

# No graph built yet
if [ ! -f "$GRAPH_REPORT" ]; then
    emit_context "<graph-status>No knowledge graph found. Run /graphify to build it.</graph-status>"
    exit 0
fi

# Staleness check: any .md file (outside graphify-out/) newer than graph.json?
stale_warning=""
if [ -f "$GRAPH_JSON" ]; then
    newer_file=$(find . -name "*.md" \
        -not -path './.git/*' \
        -not -path './graphify-out/*' \
        -not -path './node_modules/*' \
        -newer "$GRAPH_JSON" 2>/dev/null | head -1)
    if [ -n "$newer_file" ]; then
        stale_warning="\n\n⚠️ GRAPH IS STALE: Files modified since last /graphify run (e.g. ${newer_file}). Run /graphify to update."
    fi
fi

project_report=$(cat "$GRAPH_REPORT")
context="<project-graph>${project_report}${stale_warning}</project-graph>"

# Master wiki graph injection — skip if CAMERON_WIKI_PATH points to this repo
CURRENT_DIR="$(pwd -P)"
MASTER_PATH="${CAMERON_WIKI_PATH:-}"

if [ -n "$MASTER_PATH" ]; then
    MASTER_REAL="$(cd "$MASTER_PATH" 2>/dev/null && pwd -P || echo "")"
    if [ -n "$MASTER_REAL" ] && [ "$MASTER_REAL" != "$CURRENT_DIR" ]; then
        master_report="${MASTER_REAL}/graphify-out/GRAPH_REPORT.md"
        if [ -f "$master_report" ]; then
            master_content=$(cat "$master_report")
            context="${context}\n\n<master-wiki-graph>${master_content}</master-wiki-graph>"
        else
            context="${context}\n\n<master-wiki-graph-status>Master graph not found at ${MASTER_PATH}/graphify-out/. Run /graphify there first.</master-wiki-graph-status>"
        fi
    fi
fi

emit_context "$context"
