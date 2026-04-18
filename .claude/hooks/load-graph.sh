#!/usr/bin/env bash
# SessionStart hook: injects graphify knowledge graph into Claude Code context.
# Fires automatically when this project is opened. Committed to git — syncs
# across all machines via the repo.

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
    emit_context "<wiki-graph-status>No knowledge graph found. Run /graphify to build it before querying the wiki.</wiki-graph-status>"
    exit 0
fi

# Staleness check: any wiki/ or raw/ .md newer than graph.json?
stale_warning=""
if [ -f "$GRAPH_JSON" ]; then
    newer_file=$(find wiki/ raw/ -name "*.md" -newer "$GRAPH_JSON" 2>/dev/null | head -1)
    if [ -n "$newer_file" ]; then
        stale_warning="\n\n⚠️ GRAPH IS STALE: Files modified since last /graphify run (e.g. ${newer_file}). Run /graphify to update before querying."
    fi
fi

report=$(cat "$GRAPH_REPORT")
emit_context "<wiki-graph>${report}${stale_warning}</wiki-graph>"
