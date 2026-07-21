---
title: Verify Against Source Docs Before Closing
type: methodology
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/feedback_verify_against_source_docs.md
  - raw/fls-work/clearview-memory/2026-07-21/reference_approach_report_docs.md
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp508_approach_reporting.md
related:
  - "[[methodology/neutral-history-framing.md]]"
  - "[[production-systems/approach-reporting.md]]"
  - "[[decisions/clearview-approach-export-scope.md]]"
  - "[[interview-prep/behavioral-fls-delivery.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [methodology, jira, requirements, confluence, sharepoint, furnitureland-south]
---

# Verify Against Source Docs Before Closing

Before recommending a ticket be closed, check actual requirement/discovery docs (Confluence, SharePoint, attached PDFs) rather than judging completeness from the code (or ticket description) alone.

## Origin

While closing out FLSP-508 (Approach reporting), an LLM initially recommended closure because the ticket description matched what was built. Cameron pushed back: Approach was documented in Jira/Confluence attachments and a SharePoint discovery doc — check those first. That check surfaced real gaps (PDF export, report-template pivots) that the code-only read had missed.

## Why it matters

Ticket descriptions and code diffs show what was *built*, not what was *required*. When a legacy system or feature being replicated has discovery/requirements documentation somewhere, **that is the actual spec**. Closing based on "the code looks like it covers the description" skips it and risks a premature close.

## How to apply

1. Before recommending closeable: search Confluence (and ask about SharePoint / other doc stores) for real-world requirements or legacy behavior — not just the Jira ticket text.
2. If gaps are found, surface them plainly and let Cameron (or the owner) make the closure call — they may accept the gap as out-of-scope (as with FLSP-508 after Jaylon's "keep it simple" steer) or keep the ticket open.
3. Do not unilaterally decide close vs keep-open when the source docs disagree with the code.

## Worked example — FLSP-508 Approach

| Source of truth | Finding |
|-----------------|---------|
| Ticket + code | CSV/XLSX export + RBAC looked "done" |
| FLSP-109 PDF + SharePoint workshop | PDF export + multi-pivot templates also in legacy Approach |

Outcome: ship core export; explicitly defer PDF/pivots — ADR [[decisions/clearview-approach-export-scope.md]]. Product page: [[production-systems/approach-reporting.md]].

## Pair with

- Tone when writing the closeout/history: [[methodology/neutral-history-framing.md]]
- Interview framing of this habit: [[interview-prep/behavioral-fls-delivery.md]]
