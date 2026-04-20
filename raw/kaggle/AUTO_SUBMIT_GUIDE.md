# Auto-Submit System Documentation

## Hull Tactical — Automated Kaggle Submission Pipeline

### Overview

This system automates the Hull Tactical market prediction competition workflow:
- **Leaderboard monitoring** (live API checks)
- **Model retraining** (LightGBM D+M features)
- **Notebook submission** (Playwright automation)
- **Weekly review cycle** (LLM-powered analysis)

### Files

```
raw/kaggle/
├── hull-tactical-submission.py      # Kaggle notebook (gRPC server)
├── retrain.py                         # Local model retraining
├── model_files/
│   └── hull_dm_model.txt              # Trained LightGBM model (27 features)
├── review/
│   ├── weekly_review.py               # Python leaderboard/submission checker ⭐
│   ├── weekly_review.sh               # Bash wrapper (optional)
│   ├── submit_notebook.py           # Playwright submission automation
│   ├── llm_review.py                  # Claude-powered strategy analysis
│   └── SETUP.md                       # Manual setup instructions
```

### Current Status (2026-04-19)

```
Leaderboard Target: Sharpe = 5.444
Submissions:       None yet (need first submission)
Kernel Status:     Not created on Kaggle yet
Model:             Ready (D+M, 27 features, IC +0.043)
```

### Bearer Token (Working)

Token: `KGAT_4b641e87a3d05d023dc387fc63758ee0`
- Valid for leaderboard API
- 401 errors on old legacy tokens - this one works

### Quick Commands

```bash
# Check leaderboard and submissions
cd raw/kaggle/review
python weekly_review.py

# Expected output:
# 📊 LEADERBOARD (Top 10):
#    1. minglv                     5.444  ← Target
#    2. TeamNari                  5.257
#    ...
#
# 🎯 YOUR SUBMISSIONS:
#   ❌ No submissions yet
```

### First Submission Steps

1. **Create notebook on Kaggle**
   - Go to: https://www.kaggle.com/competitions/hull-tactical-market-prediction
   - Click Code → New Notebook
   - Add dataset `cwarre33/hull-tactical-model` as input
   - Paste content from `hull-tactical-submission.py`
   - Save as `hull-tactical-submission`

2. **Setup Playwright session**
   ```bash
   export KAGGLE_USERNAME=YOUR_EMAIL
   export KAGGLE_PASSWORD=YOUR_PASSWORD
   python submit_notebook.py \
       --kernel cwarre33/hull-tactical-submission \
       --competition hull-tactical-market-prediction \
       --save-session
   ```

3. **Submit**
   ```bash
   python submit_notebook.py \
       --kernel cwarre33/hull-tactical-submission \
       --competition hull-tactical-market-prediction \
       --headless
   ```

### Weekly Cron (After First Submission)

```bash
# Sunday 9 AM run
0 9 * * 0 cd /path/to/cameron-wiki/raw/kaggle/review && python weekly_review.py
```

### Troubleshooting

| Issue | Fix |
|-------|-----|
| 401 on leaderboard | Token expired - get new Bearer from Kaggle Settings |
| 404 on submissions | No submissions yet (normal before first submit) |
| Session invalid | Delete `~/.kaggle/playwright_session.json`, re-run with `--save-session` |
| No "Submit to Competition" button | Kernel isn't saved yet or not attached to competition |

### Model Details

- **Features**: D1-D9 (binary regime flags) + M1-M18 (macro/momentum)
- **Target**: forward_returns
- **Model**: LightGBM Regressor, 300 trees
- **CV**: Walk-forward, 5 folds
- **IC**: +0.044 (D+M only) vs +0.028 (full 94 features)
- **Strategy**: D gates tell model *when* to trust M signal

### Competition Details

- **Deadline**: 2026-06-16
- **Prize**: $100,000
- **Metric**: Annualized Sharpe ratio
- **Evaluation**: gRPC interactive API (walk-forward, no look-ahead)
- **Top Score**: 5.444 (minglv)

