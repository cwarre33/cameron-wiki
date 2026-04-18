# Hull Tactical — Submission & Weekly Review Setup

## One-time setup

### 1. Kaggle credentials
Your `~/.kaggle/kaggle.json` needs username + key (not just token):
```json
{"username": "cwarre33", "key": "KGAT_611b4fa3b193ea606d631a8d10ac45ed"}
```

### 2. Install dependencies
```bash
pip install kaggle anthropic playwright lightgbm scipy
playwright install chromium
```

Set your Anthropic API key (for LLM review):
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Upload model to Kaggle as a dataset

```bash
mkdir -p model_files
cp /tmp/hull_dm_model.txt model_files/

# Create dataset metadata
cat > model_files/dataset-metadata.json << 'EOF'
{
  "title": "hull-tactical-model",
  "id": "cwarre33/hull-tactical-model",
  "licenses": [{"name": "CC0-1.0"}]
}
EOF

kaggle datasets create -p model_files
```

On updates (after retraining):
```bash
kaggle datasets version -p model_files -m "weekly update $(date +%Y-%m-%d)"
```

### 4. Create the Kaggle notebook

1. Go to kaggle.com/competitions/hull-tactical-market-prediction → Code → New Notebook
2. Paste contents of `hull-tactical-submission.py`
3. Add dataset `cwarre33/hull-tactical-model` as input
4. Name the notebook `hull-tactical-submission`
5. Set accelerator: None, Internet: Off (competition requirement)
6. Save the notebook (don't run yet)

### 5. Save Playwright session (avoids re-login every week)
```bash
KAGGLE_USERNAME=cwarre33 KAGGLE_PASSWORD=your_password \
  python submit_notebook.py \
    --kernel cwarre33/hull-tactical-submission \
    --competition hull-tactical-market-prediction \
    --save-session
```
This saves cookies to `~/.kaggle/playwright_session.json`. Subsequent runs skip login.

---

## First submission

```bash
python submit_notebook.py \
  --kernel cwarre33/hull-tactical-submission \
  --competition hull-tactical-market-prediction
```

Or headlessly (for cron):
```bash
python submit_notebook.py \
  --kernel cwarre33/hull-tactical-submission \
  --competition hull-tactical-market-prediction \
  --headless
```

---

## Weekly review cycle (every Sunday)

```bash
cd raw/kaggle/review
./weekly_review.sh
```

This:
1. Downloads `predictions.jsonl` from your kernel output
2. Runs LLM review → appends to `strategy_log.md`
3. Shows leaderboard + submission history
4. Prompts you if retraining is needed

### If retraining:
```bash
python ../retrain.py              # generates new hull_dm_model.txt
kaggle datasets version -p ../model_files -m "weekly update $(date +%Y-%m-%d)"
python submit_notebook.py \
  --kernel cwarre33/hull-tactical-submission \
  --competition hull-tactical-market-prediction \
  --headless
```

---

## Reusing submit_notebook.py for other competitions

```bash
python submit_notebook.py \
  --kernel cwarre33/<your-kernel-slug> \
  --competition <competition-slug>
```

The script is competition-agnostic — it just finds the "Submit to Competition" button in any Kaggle notebook editor.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Session invalid` | Delete `~/.kaggle/playwright_session.json`, re-run with `--save-session` |
| Button not found | Run without `--headless`, check screenshot at `/tmp/kaggle_submit_debug.png` |
| `401 Unauthorized` on CLI | Update `~/.kaggle/kaggle.json` with `{"username": "cwarre33", "key": "..."}` |
| `predictions.jsonl` not in kernel output | Notebook may not have submitted yet; check kernel status on Kaggle |
