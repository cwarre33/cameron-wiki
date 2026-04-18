#!/usr/bin/env bash
# Hull Tactical — weekly review + model update pipeline
# Run every Sunday: crontab -e → 0 9 * * 0 cd /path/to/review && ./weekly_review.sh
#
# Uses Kaggle Bearer token (KGAT_...) via REST API — works with the newer token format.
# Set KAGGLE_TOKEN in your shell or .zshrc:
#   export KAGGLE_TOKEN=KGAT_611b4fa3b193ea606d631a8d10ac45ed

set -euo pipefail

COMPETITION="hull-tactical-market-prediction"
KERNEL_USER="cwarre33"
KERNEL_SLUG="hull-tactical-submission"
DATASET_SLUG="cwarre33/hull-tactical-model"
MODEL_DIR="../model_files"
REVIEW_DIR="."
PYTHON="/Applications/anaconda3/bin/python3"

KAGGLE_TOKEN="${KAGGLE_TOKEN:-KGAT_611b4fa3b193ea606d631a8d10ac45ed}"
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
teams = data.get('submissions', data.get('leaderboard', []))[:10]
for i, t in enumerate(teams, 1):
    score = t.get('score', t.get('publicScore', '?'))
    name = t.get('teamName', t.get('displayName', '?'))
    print(f'  {i:2d}. {name:<30} {score}')
" 2>/dev/null || echo "  (leaderboard parse error — check manually)"

# 4. Check our submission history
echo "[4/5] Our submissions..."
curl -s -L -H "$AUTH_HEADER" \
    "https://www.kaggle.com/api/v1/competitions/submissions/${COMPETITION}" \
    | python3 -c "
import json, sys
subs = json.load(sys.stdin)
if isinstance(subs, list):
    for s in subs[:5]:
        print(f'  {s.get(\"date\",\"?\")}  score={s.get(\"publicScore\",\"?\")}  status={s.get(\"status\",\"?\")}')
" 2>/dev/null || echo "  (submissions parse error)"

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
