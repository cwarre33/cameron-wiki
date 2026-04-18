---
title: Open Question — Agentic Memory Retention Strategies
type: open-question
status: active
visibility: public
sources: [raw/repos/autotrader-readme.md]
related: [wiki/trading/autotrader.md, wiki/decisions/autotrader-decisions-log-retention.md, wiki/architectures/agentic-trading-system.md]
created: 2026-04-17
updated: 2026-04-17
confidence: speculative
tags: [open-question, agentic, memory, retention, feedback-loop]
---

# Open Question — Agentic Memory Retention Strategies

Surfaced from AutoTrader's 90-day rotating `decisions.jsonl`. The general problem: **what should an agentic system remember vs. forget, and for how long?**

## The core tension

More memory → better context, more learning signal, higher storage + retrieval cost, risk of overfitting to stale regimes.

Less memory → lower cost, more adaptable, loses hard-won lessons, misses rare-but-important patterns.

## Domain-specific retention windows

Different domains have different regime change frequencies, which should drive retention horizon:

| Domain | Natural regime boundary | Suggested retention |
|--------|------------------------|---------------------|
| Stock trading signals | ~1 quarter (90 days) | 90 days (AutoTrader's choice) |
| News sentiment context | Days to weeks | 7–30 days |
| Career/interview knowledge | Years | Indefinite |
| Production system decisions | Until superseded | Indefinite + `status: superseded` |
| Kaggle competition approaches | Per-competition | Indefinite (limited volume) |

## What to retain indefinitely vs. rotate

**Retain indefinitely:**
- Outcomes (P&L, task results) — the ground truth signal
- Architectural decisions (ADRs) — document with `status: superseded` rather than deleting
- Rare events — market crashes, production incidents; low frequency, high learning value

**Rotate on a window:**
- Reasoning context tied to a specific regime or time period
- Intermediate working notes that led to a conclusion (keep the conclusion, rotate the path)

## Open sub-questions

1. **Can a LLM review pass extract durable lessons before rotation?** AutoTrader logs get purged at 90 days. A weekly LLM pass could distill `decisions.jsonl` into a shorter "lessons learned" file that persists indefinitely — capturing the signal before the raw data is rotated out.

2. **Should retention be adaptive?** Keep decisions from high-performance periods longer; prune losing-streak decisions faster. This is regime-aware forgetting.

3. **How does this generalize to the LLM Wiki itself?** This wiki uses `status: archived | superseded` instead of deletion. Is that sufficient, or should old `speculative` pages eventually be pruned?

## Related decisions and proposals

- [[wiki/decisions/wiki-retention-policy.md]] — applies this question to the wiki itself
- [[wiki/decisions/consensus-based-memory-distillation.md]] — proposes multi-model consensus to reduce drift before retention

## Next steps to explore

- Implement the weekly LLM review pass in AutoTrader before 90-day rotation
- Study how MemGPT / Letta handles tiered memory (in-context, external, archival)
- Look at how human memory research (spacing effect, consolidation) maps to agentic retention design
