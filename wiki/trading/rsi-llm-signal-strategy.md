---
title: RSI + LLM Sentiment — Dual-Signal Trading Strategy
type: trading-strategy
status: active
visibility: public
sources: [raw/repos/autotrader-readme.md]
related: [wiki/trading/autotrader.md, wiki/integrations/alpaca-api.md]
created: 2026-04-17
updated: 2026-04-17
confidence: medium
tags: [trading, rsi, sentiment-analysis, llm, signal, strategy, technical-analysis]
---

# RSI + LLM Sentiment — Dual-Signal Trading Strategy

Hybrid strategy combining a backward-looking momentum indicator (RSI) with a forward-looking LLM news sentiment signal. Both must agree before a trade executes — neither alone is sufficient.

## Why dual-signal

Single indicators generate false positives. RSI can flag oversold conditions in a stock whose fundamentals are deteriorating (news not yet priced in). LLM sentiment on headlines can be noisy or manipulable without confirming price momentum. Requiring both to agree reduces false positive rate at the cost of missing some valid signals.

This is the same pattern as ensemble models in ML: independent weak signals combined are more reliable than either alone.

## RSI component

**Relative Strength Index, 14-period, Wilder's smoothing.**

```
RSI = 100 - (100 / (1 + RS))
RS  = Average Gain / Average Loss  (Wilder's exponential smoothing)
```

- RSI < 30 → oversold signal (potential buy)
- RSI > 70 → overbought signal (potential sell)
- Wilder's smoothing (vs. simple moving average) gives more weight to recent price action

## LLM sentiment component

- Fetch recent headlines per ticker via Alpaca News API
- Pass headlines + price context to Llama 3.3 70B
- LLM returns: sentiment direction (bullish/bearish/neutral) + confidence score + reasoning
- Confidence threshold gates execution — low-confidence LLM outputs skip the trade

**Why Llama 3.3 70B?** See [[wiki/decisions/autotrader-open-model-vs-frontier.md]].

## Signal combination logic

```
if rsi_signal == "oversold" and llm_sentiment == "bullish" and confidence > threshold:
    execute_buy(ticker, position_size=0.05 * account_equity)

if rsi_signal == "overbought" and llm_sentiment == "bearish" and confidence > threshold:
    execute_sell(ticker)

else:
    skip  # log to decisions.jsonl with reasoning
```

## Scan universe

Top 50 stocks by volume at scan time. Volume filter ensures sufficient liquidity and active price discovery — thin stocks have unreliable RSI and noisy news signals.

## Limitations and open questions

- ⚠️ **No backtesting documented** — strategy is deployed to paper trading without published historical performance baseline. Should backtest RSI + sentiment on historical data before drawing conclusions.
- ⚠️ **LLM sentiment on headlines is manipulable** — headline sentiment doesn't always reflect actual price movement; earnings surprises, Fed announcements, and macro events can override both signals.
- ⚠️ **15-minute scan cadence** — misses intraday momentum; best suited for multi-hour or multi-day holding periods.
- **Open question:** Does LLM sentiment add alpha over RSI alone? The outcomes.jsonl log exists to answer this — a future analysis pass could split trades by "RSI-only would have agreed" vs. "LLM was the deciding factor."

## Related

- [[wiki/trading/autotrader.md]] — the system that implements this strategy
- [[wiki/integrations/alpaca-api.md]] — broker integration
