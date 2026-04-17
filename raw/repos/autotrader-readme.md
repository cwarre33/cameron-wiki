# AutoTrader - Autonomous Paper Trading Bot
Source: https://github.com/cwarre33/AutoTrader
Fetched: 2026-04-17

---

AI-powered paper trading bot that scans high-volume stocks, analyzes them with RSI and news sentiment via LLM reasoning, and executes paper trades on Alpaca.

## Features

- **Stock Scanner**: Identifies top 50 most active stocks by volume
- **Technical Analysis**: RSI (14-period) using Wilder's smoothing
- **News Sentiment**: Fetches recent headlines via Alpaca News API
- **LLM Reasoning**: Uses Llama 3.3 70B via HF Inference API for analysis
- **Paper Trading**: Executes trades on Alpaca paper trading
- **Risk Management**: 5% max position size, confidence threshold
- **Dashboard**: Real-time Gradio UI with account summary, positions, and trade history
- **Scheduling**: Automatic scans every 15 minutes during market hours

## Architecture (refactor)

- **Single scan entrypoint**: `workspace/scan_autotrader.py` — used by cron and HEARTBEAT; uses shared lib (in-process Alpaca client, retries, logging)
- **Shared lib** (`workspace/lib/`): `config` (watchlist, env validation), `alpaca_client` (get_account, get_positions, get_bars, get_snapshot, buy, sell with retries), `rsi`, `decisions` (log, retention, outcomes, daily review)
- **Watchlist**: `workspace/config/watchlist.json` — single source of ticker groups
- **Self-improvement**: Each scan appends to `logs/outcomes.jsonl` and `logs/daily_review.jsonl`; `logs/decisions.jsonl` is rotated (90-day retention). See `workspace/SELF_IMPROVEMENT.md`
- **Health**: `GET /api/health` checks Alpaca connectivity
- **Discord**: Discord bot integration via `DISCORD_BOT_TOKEN`
- Deployed as Docker container with OpenClaw gateway

## Required Secrets

- ALPACA_API_KEY / ALPACA_SECRET_KEY — Alpaca paper trading
- HF_TOKEN — Hugging Face Inference API (Llama 3.3 70B)
- DISCORD_BOT_TOKEN — optional Discord alerts

## Risk Management

- 5% max position size per trade
- Confidence threshold before execution
- RSI + LLM sentiment must align for signal

## Self-improvement loop

- `logs/outcomes.jsonl` — per-trade outcomes appended each scan
- `logs/daily_review.jsonl` — daily summary
- `logs/decisions.jsonl` — 90-day rotating log of trading decisions
- `SELF_IMPROVEMENT.md` documents the feedback loop design

## Deployment

- Docker-based, app_port 7860 (Gradio UI)
- Hugging Face Spaces compatible (docker SDK)
- Health check: GET /api/health
- 15-minute scan interval during market hours
