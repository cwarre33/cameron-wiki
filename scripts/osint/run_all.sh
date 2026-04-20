#!/usr/bin/env bash
# Run the full OSINT ICS pipeline: collect → enrich → graph → viz → ingest
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LIMIT="${LIMIT:-1000}"
TODAY="$(date +%F)"
OUT="$REPO_ROOT/raw/osint"

echo "=== ICS OSINT pipeline — $TODAY ==="
echo "Limit: $LIMIT hosts/protocol | Output: $OUT"
echo

cd "$REPO_ROOT"

echo "[1/5] collect.py"
python -m scripts.osint.collect --limit "$LIMIT"

RAW="$OUT/${TODAY}-scan-raw.json"
ENRICHED="$OUT/${TODAY}-scan-enriched.json"
GML="$OUT/${TODAY}-graph.graphml"

echo
echo "[2/5] enrich.py"
python -m scripts.osint.enrich "$RAW"

echo
echo "[3/5] graph.py"
python -m scripts.osint.graph "$ENRICHED"

echo
echo "[4/5] viz.py"
python -m scripts.osint.viz "$GML" "$ENRICHED"

echo
echo "[5/5] ingest.py"
python -m scripts.osint.ingest "$ENRICHED"

echo
echo "=== Done. Files in $OUT ==="
ls -lh "$OUT/${TODAY}-"*
