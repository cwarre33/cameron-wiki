---
title: LLM Review Pass Before Rotation
type: technique
status: active
visibility: public
sources: []
related: [wiki/decisions/autotrader-decisions-log-retention.md, wiki/decisions/wiki-retention-policy.md, wiki/architectures/agentic-trading-system.md, wiki/open-questions/agentic-memory-retention-strategies.md]
created: 2026-04-17
updated: 2026-04-17
confidence: medium
tags: [technique, agentic, memory, retention, distillation, self-improvement, feedback-loop]
---

# LLM Review Pass Before Rotation

A technique for **extracting durable signal from time-bounded context before it's purged.** Run an LLM over a rolling log or stale document corpus, distill regime-independent lessons into a persistent summary, then rotate the raw material.

Addresses the core tension in agentic memory: raw reasoning context staleness quickly, but the lessons embedded in it don't.

## The pattern

```
Raw context (time-bounded)
        ↓
  LLM review pass
        ↓
  Durable lessons (regime-independent) → persistent summary
        ↓
  Raw context purged
```

**Input:** regime-dependent raw material — trading decisions tied to market conditions, working notes tied to a project phase, speculative wiki pages tied to a prior research direction.

**Output:** regime-independent distilled claims — "under high RSI + negative sentiment, skip outperforms execute 73% of the time"; "the key insight from this speculative page was X, now absorbed into Y."

**Then:** rotate the raw input. The signal survives; the noise doesn't.

## Instances in Cameron's systems

### AutoTrader (planned)
- **Raw input:** `logs/decisions.jsonl` — every trade decision with LLM reasoning and market context. Rotates on 90-day window per [[wiki/decisions/autotrader-decisions-log-retention.md]].
- **Review pass:** weekly cron job reads the past 7 days of decisions, asks an LLM to extract durable lessons (signal patterns, regime-specific behaviors, recurring failure modes).
- **Output:** appended to `logs/lessons.md` — persistent, not rotated.
- **Status:** ⚠️ logging infrastructure exists; LLM review pass is a future enhancement per [[wiki/architectures/agentic-trading-system.md]].

### This wiki (quarterly lint)
- **Raw input:** `confidence: speculative` pages with no updates and no inbound wikilinks — working notes that never evolved into real knowledge.
- **Review pass:** LLM reads candidate pages, extracts any claim not already covered elsewhere, appends it to the most relevant existing page.
- **Output:** absorbed into existing pages.
- **Then:** speculative page pruned per [[wiki/decisions/wiki-retention-policy.md]].

## Implementation sketch (AutoTrader)

```python
# weekly_review.py — run before rotation window expires
import json
from pathlib import Path
from datetime import datetime, timedelta

DECISIONS_LOG = Path("logs/decisions.jsonl")
LESSONS_FILE = Path("logs/lessons.md")

def load_recent_decisions(days=7):
    cutoff = datetime.now() - timedelta(days=days)
    decisions = []
    for line in DECISIONS_LOG.read_text().splitlines():
        d = json.loads(line)
        if datetime.fromisoformat(d["timestamp"]) > cutoff:
            decisions.append(d)
    return decisions

def extract_lessons(decisions, llm_client):
    prompt = f"""
You are reviewing {len(decisions)} trading decisions from the past 7 days.
For each decision, you have: ticker, action (execute/skip), RSI value, LLM sentiment, outcome (if available).

Extract 3-5 durable, regime-independent lessons. A durable lesson is a pattern that would
apply in future market conditions, not one tied to this specific week's news.

Format each lesson as a single sentence starting with "When..." or "Under...".
Avoid restating individual decisions. Synthesize patterns.

Decisions:
{json.dumps(decisions, indent=2)}
"""
    return llm_client.complete(prompt)

def append_lessons(lessons_text):
    date = datetime.now().strftime("%Y-%m-%d")
    entry = f"\n## {date}\n{lessons_text}\n"
    with open(LESSONS_FILE, "a") as f:
        f.write(entry)
```

## Why this matters for agentic systems

Without a review pass, rotation is pure loss — you delete context without capturing what it taught. With a review pass, rotation becomes **compression**: the useful signal density of your persistent memory goes up over time, while storage stays bounded.

This is the engineering equivalent of spaced repetition: keep what generalizes, let the specific decay.

## Related patterns

- **AutoTrader's 3-log design** — the separation of `decisions` (rotate), `outcomes` (keep), and `daily_review` (keep) already encodes this principle partially. The review pass completes it.
- **Wiki lint workflow** — the quarterly lint in CLAUDE.md is the manual version of this pattern applied to knowledge management.
- **MemGPT / Letta tiered memory** — a more sophisticated implementation of the same idea: hot context window, warm external storage, cold archival, with automatic promotion/demotion.
