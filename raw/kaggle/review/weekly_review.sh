#!/usr/bin/env bash
# Hull Tactical — weekly review + model update pipeline
# Run every Sunday: crontab -e → 0 9 * * 0 cd /path/to/review && ./weekly_review.sh

set -euo pipefail

COMPETITION="hull-tactical-market-prediction"
KERNEL_SLUG="cwarre33/hull-tactical-submission"
DATASET_SLUG="cwarre33/hull-tactical-model"
MODEL_DIR="../model_files"
REVIEW_DIR="."
PYTHON="/Applications/anaconda3/bin/python3"

echo "=== Hull Tactical weekly review — $(date) ==="

# 1. Pull latest kernel output (prediction log)
echo "[1/5] Pulling kernel output..."
kaggle kernels output "$KERNEL_SLUG" -p "$REVIEW_DIR"
if [ ! -f "$REVIEW_DIR/predictions.jsonl" ]; then
    echo "  WARNING: predictions.jsonl not found in output. Kernel may not have run yet."
    exit 1
fi
echo "  predictions.jsonl downloaded."

# 2. Run LLM review
echo "[2/5] Running LLM review..."
"$PYTHON" llm_review.py predictions.jsonl --output strategy_log.md
echo "  Review appended to strategy_log.md"

# 3. Check leaderboard position
echo "[3/5] Leaderboard..."
kaggle competitions leaderboard "$COMPETITION" --show 2>/dev/null | head -20 || true

# 4. Check our submission history
echo "[4/5] Submission history..."
kaggle competitions submissions "$COMPETITION" 2>/dev/null | head -5 || true

# 5. Prompt for model update decision
echo ""
echo "[5/5] Model update?"
echo "  If retraining is needed:"
echo "    a) Retrain: $PYTHON ../retrain.py"
echo "    b) Upload:  kaggle datasets version -p $MODEL_DIR -m 'weekly update YYYY-MM-DD'"
echo "    c) Submit:  python submit_notebook.py --kernel $KERNEL_SLUG --competition $COMPETITION"
echo ""
echo "=== Done. Review strategy_log.md for LLM recommendations ==="
