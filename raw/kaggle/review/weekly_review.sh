#!/usr/bin/env bash
# Hull Tactical — weekly review + model update pipeline
# Run every Sunday: crontab -e → 0 9 * * 0 cd /path/to/review && ./weekly_review.sh
#
# Uses Kaggle Bearer token (KGAT_...) via REST API — works with the newer token format.
# Set KAGGLE_TOKEN in your shell or .zshrc:
#   export KAGGLE_TOKEN=KGAT_6...45ed

set -euo pipefail

COMPETITION="hull-tactical-market-prediction"
KERNEL_USER="cwarre33"
KERNEL_SLUG="hull-tactical-submission"
DATASET_SLUG="cwarre33/hull-tactical-model"
MODEL_DIR="../model_files"
REVIEW_DIR="."
PYTHON="/usr/bin/env python3"

# Get token from ~/.kaggle/kaggle.json if KAGGLE_TOKEN not set
KAGGLE_TOKEN="${KAGGLE_TOKEN:-KGAT_4b641e87a3d05d023dc387fc63758ee0}"
AUTH_HEADER="Authorization: Bearer $KAGGLE_TOKEN"

echo "=== Hull Tactical weekly review — $(date) ==="

# 1. Pull latest kernel output (prediction log)
echo "[1/5] Pulling kernel output..."
OUTPUT_URL="https://www.kaggle.com/api/v1/kernels/output/${KERNEL_USER}/${KERNEL_SLUG}?datasetDatasetType=all"
curl -s -L -H "$AUTH_HEADER" "$OUTPUT_URL" -o /tmp/kernel_output.zip

if [ ! -s /tmp/kernel_output.zip ]; then
    echo "  WARNING: kernel output empty. Kernel may not have run yet."
    exit 1
fi

mkdir -p /tmp/kernel_output
unzip -o /tmp/kernel_output.zip -d /tmp/kernel_output >/dev/null 2>&1

if [ -f /tmp/kernel_output/predictions.jsonl ]; then
    cp /tmp/kernel_output/predictions.jsonl "$REVIEW_DIR/predictions.jsonl"
    echo "  predictions.jsonl downloaded ($(wc -l < "$REVIEW_DIR/predictions.jsonl") rows)"
else
    echo "  WARNING: predictions.jsonl not found in kernel output."
    ls /tmp/kernel_output/ 2>/dev/null || true
    exit 1
fi

# 2. Run LLM review
echo "[2/5] Running LLM review..."
"$PYTHON" llm_review.py "$REVIEW_DIR/predictions.jsonl" --output "$REVIEW_DIR/strategy_log.md"
echo "  Review appended to strategy_log.md"

# 3. Check leaderboard (top 10)
echo "[3/5] Leaderboard (top 10)..."
curl -s -L -H "$AUTH_HEADER" \
    "https://www.kaggle.com/api/v1/competitions/${COMPETITION}/leaderboard/view" \
    | python3 -c "
import json, sys
data = json.load(sys.stdin)
teams = data.get('submissions', [])[:10]
for i, t in enumerate(teams, 1):
    score = t.get('score', '?')
    name = t.get('teamName', '?')
    print(f'  {i:2d}. {name:<30} {score}')
" 2>/dev/null || echo "  (leaderboard unavailable)"

# 4. Check our submission history
echo "[4/5] Our submissions..."
SUBS_BODY=$(curl -s -L -H "$AUTH_HEADER" \
    "https://www.kaggle.com/api/v1/competitions/submissions/${COMPETITION}")
if [ -z "$SUBS_BODY" ] || [ "$SUBS_BODY" = "null" ]; then
    echo "  No submissions yet."
else
    echo "$SUBS_BODY" | python3 -c "
import json, sys
body = sys.stdin.read().strip()
if not body or body in ('null','[]',''):
    print('  No submissions yet.')
    sys.exit()
subs = json.loads(body)
if isinstance(subs, list):
    for s in subs[:5]:
        print(f'  {s.get(\"date\",\"?\")[:10]}  score={s.get(\"publicScore\",\"?\")}  status={s.get(\"status\",\"?\")}')
elif isinstance(subs, dict):
    print('  Response:', list(subs.keys()))
" 2>/dev/null || echo "  (parse error — no submissions or unexpected format)"
fi

# 5. Dataset version bump (if model was retrained)
echo "[5/5] Model update?"
echo ""
echo "  If retrain is needed based on LLM review:"
echo "    1. python3 ../retrain.py [--drop D4] [--features D M]"
echo "    2. Upload new model:"

# Try kaggle CLI first, fall back to curl instructions
if command -v kaggle &>/dev/null && kaggle datasets list 2>/dev/null | grep -q "$DATASET_SLUG"; then
    echo "    3. kaggle datasets version -p $MODEL_DIR -m 'weekly update $(date +%Y-%m-%d)'"
else
    echo "    3. curl -X POST -H '$AUTH_HEADER' \\"
    echo "         -F 'versionNotes=weekly update $(date +%Y-%m-%d)' \\"
    echo "         -F 'files=@$MODEL_DIR/hull_dm_model.txt' \\"
    echo "         'https://www.kaggle.com/api/v1/datasets/$DATASET_SLUG/versions'"
fi

echo "    4. python3 submit_notebook.py \\"
echo "         --kernel ${KERNEL_USER}/${KERNEL_SLUG} \\"
echo "         --competition ${COMPETITION} --headless"
echo ""
echo "=== Done. See strategy_log.md for LLM recommendations ==="
