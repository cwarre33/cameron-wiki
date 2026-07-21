---
title: Neutral History Framing
type: methodology
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/feedback_neutral_history_framing.md
related:
  - "[[methodology/verify-against-source-docs.md]]"
  - "[[production-systems/approach-reporting.md]]"
  - "[[interview-prep/behavioral-fls-delivery.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [methodology, jira, communication, handoff, furnitureland-south]
---

# Neutral History Framing

When documenting who-did-what history (Jira comments, timelines, closeout notes, PR descriptions, handoffs), keep it **factual and neutral** — never frame around a colleague's gap or imply blame.

## Origin

While drafting an FLSP-508 closeout comment, an LLM draft opened with "Quick history since ticket had no comments" before listing what Jaylon and Filadelfo had (and hadn't) done. Cameron corrected: don't frame it as "history since no comments" — don't throw shade; just track everything.

## Why it matters

The goal of documenting history is complete, accurate tracking for the team record — not implicitly criticizing a colleague for an absent comment, a quiet status transition, or reassigned work. Even true, neutral-sounding framing like "since the ticket had no comments" reads as pointed once followed by a list of what someone didn't do.

## How to apply

- State the timeline as plain facts (who opened it, who did what work, when it moved status) without a framing sentence that calls out an absence or gap as the reason for writing it up.
- Don't justify *why* a history is being written — just write it.
- Applies to any Jira comment, PR description, or handoff note that touches other people's work — not only ClearView / FLSP-508.

## Anti-pattern → rewrite

| Avoid | Prefer |
|-------|--------|
| "Quick history since nobody left comments…" | "Timeline: opened by X on DATE; Y shipped Z on DATE; status → Done on DATE." |
| "X never finished Y so I…" | "Y remained open after DATE; completed under Z on DATE." |
| Listing what someone *didn't* do as the narrative spine | Listing what *did* happen, chronologically |

## Related

- Spec completeness before close: [[methodology/verify-against-source-docs.md]]
- FLSP-508 context: [[production-systems/approach-reporting.md]]
- Behavioral stories that need this tone: [[interview-prep/behavioral-fls-delivery.md]]
