"""
Weekly LLM review pass over Hull Tactical prediction log.

Reads predictions.jsonl (downloaded from Kaggle kernel output),
sends a structured summary to Claude, writes findings to strategy_log.md.

Usage:
    python llm_review.py predictions.jsonl
    python llm_review.py predictions.jsonl --days 14   # extend lookback
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

import anthropic
import numpy as np

LOOKBACK_DAYS = 7


def load_recent(path: Path, n_days: int) -> list[dict]:
    rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    return rows[-n_days:] if len(rows) > n_days else rows


def build_summary(rows: list[dict]) -> str:
    if not rows:
        return "No prediction data available."

    preds = [r['pred'] for r in rows]
    lags = [r['lagged_return'] for r in rows if r.get('lagged_return') is not None]
    attenuated = sum(1 for r in rows if r.get('attenuated'))

    # IC proxy: rank correlation between predictions and next-day lagged returns
    # (lagged_return on day N = return that was realized for day N-1's prediction)
    aligned = [(rows[i]['pred'], rows[i+1]['lagged_return'])
               for i in range(len(rows)-1)
               if rows[i+1].get('lagged_return') is not None]
    ic_proxy = None
    if len(aligned) >= 5:
        from scipy.stats import spearmanr
        ps, ls = zip(*aligned)
        ic_proxy, _ = spearmanr(ps, ls)

    # D-flag regime breakdown
    d_regime_perf: dict[str, list[float]] = defaultdict(list)
    for i, row in enumerate(rows[:-1]):
        next_lag = rows[i+1].get('lagged_return')
        if next_lag is None:
            continue
        for flag, val in row['D'].items():
            key = f"{flag}={val}"
            d_regime_perf[key].append(next_lag * np.sign(row['pred']))

    regime_lines = []
    for key in sorted(d_regime_perf):
        vals = d_regime_perf[key]
        mean = np.mean(vals)
        regime_lines.append(f"  {key:8s}: n={len(vals):3d}  mean_signed_return={mean:+.5f}")

    summary = f"""PREDICTION LOG SUMMARY — last {len(rows)} days
Predictions: mean={np.mean(preds):+.5f}  std={np.std(preds):.5f}
Lagged returns available: {len(lags)} days
IC proxy (pred vs next-day return): {ic_proxy:+.4f if ic_proxy else 'insufficient data'}
Attenuated predictions: {attenuated}/{len(rows)}

D-FLAG REGIME PERFORMANCE (signed return when flag is active):
{chr(10).join(regime_lines) if regime_lines else '  insufficient data'}

TOP M FEATURES (last prediction):
{json.dumps(rows[-1].get('M_top4', {}), indent=2) if rows else 'none'}

RECENT PREDICTIONS (last 5):
{chr(10).join(f"  date_id={r['date_id']}  pred={r['pred']:+.5f}  lag={r.get('lagged_return', 'N/A')}" for r in rows[-5:])}
"""
    return summary


def run_review(summary: str, lookback: int) -> str:
    client = anthropic.Anthropic()
    prompt = f"""You are a quantitative strategy analyst reviewing a systematic trading model.

The model uses 9 binary D-flag regime indicators (D1-D9, values 0/1 except D6 which is -1/0)
and 18 macro/momentum M-features to predict daily forward returns via LightGBM.
It was trained on 9,048 days of data with walk-forward CV IC of +0.043.

Review the last {lookback} days of live prediction data below and answer:

1. Is the model currently generating real signal? (IC proxy vs +0.043 training baseline)
2. Which D-flag regimes are currently working vs. failing? (look at signed return by flag)
3. Any D flags that consistently appear with wrong-sign predictions — candidates to drop?
4. Is the attenuation logic helping or over-firing?
5. One concrete model adjustment to make this week (feature drop, lookback change, or hold).

Be specific and quantitative. Reference the actual numbers. Keep your answer under 400 words.

---
{summary}"""

    msg = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=600,
        messages=[{'role': 'user', 'content': prompt}],
    )
    return msg.content[0].text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('log', type=Path, help='predictions.jsonl path')
    parser.add_argument('--days', type=int, default=LOOKBACK_DAYS)
    parser.add_argument('--output', type=Path, default=Path('strategy_log.md'))
    args = parser.parse_args()

    if not args.log.exists():
        sys.exit(f"Log not found: {args.log}")

    rows = load_recent(args.log, args.days)
    if not rows:
        sys.exit("Log is empty.")

    print(f"Loaded {len(rows)} prediction rows from {args.log}")
    summary = build_summary(rows)
    print(summary)

    print("Running LLM review...")
    review = run_review(summary, args.days)
    print("\n--- LLM REVIEW ---")
    print(review)

    entry = f"\n## [{date.today()}] Weekly review — last {args.days} days\n\n{summary}\n### LLM Analysis\n{review}\n---"
    with args.output.open('a') as f:
        f.write(entry)
    print(f"\nAppended to {args.output}")


if __name__ == '__main__':
    main()
