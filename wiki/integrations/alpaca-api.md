---
title: Alpaca API Integration
type: integration
status: active
visibility: public
sources: [raw/repos/autotrader-readme.md]
related: [wiki/trading/autotrader.md, wiki/trading/rsi-llm-signal-strategy.md, wiki/architectures/agentic-trading-system.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [alpaca, trading, api, paper-trading, stocks, integration]
---

# Alpaca API Integration

Alpaca is a commission-free stock trading API. Offers separate paper trading and live trading environments with identical API interfaces — swap credentials to switch.

## Key capabilities used in AutoTrader

| Capability | API call | Notes |
|-----------|----------|-------|
| Account info | `get_account()` | Equity, buying power, cash |
| Positions | `get_positions()` | Current holdings |
| Price bars | `get_bars(ticker, timeframe)` | OHLCV data for RSI calculation |
| Snapshot | `get_snapshot(ticker)` | Latest quote + trade |
| Buy order | `buy(ticker, qty)` | Market order execution |
| Sell order | `sell(ticker, qty)` | Market order execution |
| News | Alpaca News API | Recent headlines per ticker |

## Paper vs. live trading

Alpaca provides two environments with identical REST interfaces:
- **Paper:** `https://paper-api.alpaca.markets` — simulated execution, no real capital
- **Live:** `https://api.alpaca.markets` — real execution, real capital

The only code change to go live: swap `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` env vars and the base URL. **However:** this surface simplicity masks real risk — full risk management review required before live deployment. See [[wiki/trading/autotrader.md]].

## Auth pattern

```python
import alpaca_trade_api as tradeapi

api = tradeapi.REST(
    key_id=os.environ["ALPACA_API_KEY"],
    secret_key=os.environ["ALPACA_SECRET_KEY"],
    base_url="https://paper-api.alpaca.markets"
)
```

## Retry pattern (AutoTrader shared lib)

AutoTrader's `lib/alpaca_client` wraps all API calls with retries — handles transient 429 (rate limit) and 5xx errors. Pattern: exponential backoff with jitter, max 3 attempts before surfacing the error.

## News API

Alpaca's News API returns recent headlines per ticker — used for LLM sentiment input in AutoTrader. Returns structured JSON with headline, source, published timestamp, and summary. Rate-limited; fetched per-ticker at scan time.

## Rate limits (paper trading tier)

- 200 requests/minute on data APIs
- Order submission: no hard limit, but best practice to batch and avoid bursts

## Used in

- [[wiki/trading/autotrader.md]]
