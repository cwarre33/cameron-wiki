---
title: Agentic Trading System Architecture
type: architecture
status: active
visibility: public
sources: [raw/repos/autotrader-readme.md]
related: [wiki/trading/autotrader.md, wiki/trading/rsi-llm-signal-strategy.md, wiki/integrations/alpaca-api.md, wiki/decisions/autotrader-open-model-vs-frontier.md, wiki/decisions/autotrader-decisions-log-retention.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [architecture, agentic, trading, docker, gradio, cron, feedback-loop, self-improvement]
---

# Agentic Trading System Architecture

Pattern for a containerized, scheduled LLM-driven trading agent with persistent memory and a self-improvement feedback loop. Implemented in [[wiki/trading/autotrader.md]].

## System diagram

```
┌─────────────────────────────────────────────────────┐
│  Docker Container                                    │
│                                                      │
│  cron (15min, market hours)                          │
│       ↓                                              │
│  scan_autotrader.py          ← single entrypoint     │
│       ↓                                              │
│  lib/alpaca_client           ← market data + orders  │
│  lib/rsi                     ← technical analysis    │
│  lib/decisions               ← log + execute/skip    │
│       ↓                                              │
│  HF Inference API (Llama 3.3 70B)  ← LLM reasoning  │
│       ↓                                              │
│  Alpaca Paper Trading API    ← order execution       │
│       ↓                                              │
│  logs/                       ← persistent JSONL      │
│    outcomes.jsonl                                    │
│    decisions.jsonl (90-day)                          │
│    daily_review.jsonl                                │
│                                                      │
│  Gradio UI (port 7860)       ← dashboard             │
│  GET /api/health             ← health check          │
│  Discord bot                 ← alerts                │
└─────────────────────────────────────────────────────┘
```

## Key architectural properties

**Single scan entrypoint.** `scan_autotrader.py` is the only file the cron job and health check call. All logic flows through shared lib — no duplicated Alpaca client, no duplicated logging. Changes to retry logic, risk parameters, or watchlist happen in one place.

**Persistent feedback loop.** Every scan appends to JSONL logs regardless of whether a trade executes. This creates a complete audit trail and the raw material for strategy improvement. The logs are mounted as a Docker volume — survive container restarts.

**HF Spaces-compatible deployment.** The Docker config (`sdk: docker`, `app_port: 7860`) matches HuggingFace Spaces conventions. Can be deployed to HF Spaces for free-tier hosting or run locally — same container, same behavior.

**Health check endpoint.** `GET /api/health` verifies Alpaca connectivity and returns account equity. Enables external monitoring (UptimeRobot, Discord webhook, etc.) without accessing trading logic directly.

## Watchlist management

Single source of truth: `workspace/config/watchlist.json`. Ticker groups (e.g., large cap, tech, ETFs) defined once, consumed by scan logic. No hardcoded tickers in scan code.

## Self-improvement loop design

```
Scan → Decision → Log → (future) LLM review pass
                             ↓
                    Strategy parameter updates
                             ↓
                    Updated watchlist.json / thresholds
```

The loop is partially implemented — logging infrastructure exists, but the automated LLM review pass that *acts* on the logs is a future enhancement. Currently: logs are available for manual analysis.

## Deployment checklist

1. Copy `.env.example` → `.env`, fill API keys
2. `docker compose up` — starts container with Gradio UI + cron
3. `curl http://localhost:5050/api/health` — verify Alpaca connectivity
4. Scan dry run: `docker compose exec openclaw-gateway python scan_autotrader.py`
5. Monitor Discord for trade alerts

## Patterns applicable elsewhere

- **Single entrypoint + shared lib** — apply to any scheduled agentic task (transcript pipelines, data ingestion, monitoring)
- **JSONL feedback logs** — lightweight, appendable, grep-able; better than a DB for early-stage agent memory
- **HF Spaces Docker deployment** — zero-cost hosting for demos and pilots
- **Health check as first-class concern** — build `GET /health` into every service, not as an afterthought
