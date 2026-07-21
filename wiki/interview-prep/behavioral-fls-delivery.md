---
title: Behavioral Stories — FLS Delivery
type: interview-note
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/feedback_neutral_history_framing.md
  - raw/fls-work/clearview-memory/2026-07-21/feedback_verify_against_source_docs.md
  - raw/fls-work/jira/2026-07-21/cluster-map.md
related:
  - "[[methodology/neutral-history-framing.md]]"
  - "[[methodology/verify-against-source-docs.md]]"
  - "[[interview-prep/system-design-clearview.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[production-systems/clearview-aws-hosting.md]]"
  - "[[production-systems/approach-reporting.md]]"
  - "[[decisions/clearview-approach-export-scope.md]]"
  - "[[initiatives/zendesk-automation-platform.md]]"
  - "[[production-systems/dedicated-agent-assignment.md]]"
  - "[[production-systems/crr-round-robin.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [interview, behavioral, star, jira, clearview, zendesk, furnitureland-south]
---

# Behavioral Stories — FLS Delivery

STAR-ready stories from Furnitureland South delivery: spec-driven Jira, stakeholder loops, production incidents, Zendesk automation. Technical depth for ClearView: [[interview-prep/system-design-clearview.md]].

**Visibility:** fls-internal — strip colleague names / ticket IDs for public interviews if needed.

## 1. Spec-driven Jira (don't close on code alone)

**Prompt fit:** "Tell me about a time you caught a requirements gap" / "How do you know something is done?"

| | |
|--|--|
| **Situation** | Closing Approach reporting (FLSP-508) on ClearView — ticket text matched the CSV/XLSX + RBAC build. |
| **Task** | Decide whether the story was truly closeable vs still short of legacy Approach. |
| **Action** | Verified Confluence/SharePoint discovery docs (FLSP-109 PDF + workshop), not just code/ticket. Surfaced PDF export + multi-pivot templates as real gaps; aligned with stakeholder "keep it simple" steer; wrote explicit deferrals into an ADR. |
| **Result** | Shipped core export as Done; deferred list documented so future work doesn't re-discover. Habit captured: [[methodology/verify-against-source-docs.md]] · [[decisions/clearview-approach-export-scope.md]] · [[production-systems/approach-reporting.md]] |

**Sound bite:** "Built ≠ required. Discovery docs are the spec."

## 2. Stakeholder loops (Sales / Merch → scoped delivery)

**Prompt fit:** "Working with non-engineering stakeholders" / "Managing scope"

| | |
|--|--|
| **Situation** | Inventory Lookup initiative needed floor + merchandising buy-in before build (FLSP-106/107 discovery under FLSP-103). |
| **Task** | Translate workshop needs into a shippable Approach successor without boiling the ocean. |
| **Action** | Discovery meetings → design → build; when Approach parity gaps appeared at closeout, used stakeholder "keep it simple" guidance to ship CSV/XLSX + RBAC and defer pivots/PDF rather than silently over-building or silently under-shipping. |
| **Result** | ClearView Approach export live under FLSP-508 Done; deferred templates cited for follow-on. Initiative map: [[initiatives/flsp-103-inventory-lookup.md]] |

**Communication habit:** When writing timelines/closeouts that touch others' work, use neutral facts — no "since nobody commented" framing. [[methodology/neutral-history-framing.md]]

## 3. Production incidents (FLSP-781 / FLSP-784)

**Prompt fit:** "Tell me about a production incident" / "Debugging under pressure"

### FLSP-781 — Staging crash-loop (Done)

| | |
|--|--|
| **Situation** | `clearview-staging` crash-looped after hosting/auth work. |
| **Task** | Restore staging without breaking prod promote discipline. |
| **Action** | Traced to RDS password / SSM Parameter Store drift (secrets outside Terraform-applied values; `ignore_changes` on secret values). Fixed secret alignment; confirmed ALB healthy + Entra path. |
| **Result** | Bug Done; reinforced SSM/Terraform ops lesson on [[production-systems/clearview-aws-hosting.md]]. |

### FLSP-784 — Akeneo 503 + sign-in video (In Progress as of 2026-07-21)

| | |
|--|--|
| **Situation** | Hosted ClearView: product images 503 via Akeneo path; missing sign-in video asset. |
| **Task** | Restore image path + login UX without regressing SSO. |
| **Action** | Treating as SSM/asset hosting follow-on separate from Entra core (FLSP-414 Done). |
| **Result** | Still In Progress — honest "open follow-up" story; don't claim Done. |

**Sound bite:** "Separate auth correctness from asset/CDN/SSM path failures — different blast radii."

## 4. Zendesk automation platform (breadth of ownership)

**Prompt fit:** "Tell me about a system you owned end-to-end" / "Impact across a team"

| | |
|--|--|
| **Situation** | Contact-center tooling sprawl — routing, views, transcripts, calendar, returns, NS↔Zendesk sync. |
| **Task** | Ship durable automations agents actually use; keep post-launch fixes honest. |
| **Action** | Built/owned cluster: CRR round robin, dedicated-agent org logic, shared views cleanup, call transcript pipeline, due-dates calendar app, returns reporting, customer sync replacement. Indexed as [[initiatives/zendesk-automation-platform.md]] (~108 assignee issues in cluster). |
| **Result** | Most stories Done / post-prod validation; residual open items called out (e.g. FLSI-2965 Ready for Deployment, FLSM-20 Post Prod Validation, OAuth refresh open question). Deep links: [[production-systems/crr-round-robin.md]], [[production-systems/dedicated-agent-assignment.md]], [[production-systems/zendesk-call-transcripts.md]]. |

**Sound bite:** "Not one Lambda — a platform of routing, reporting, and sync jobs with post-launch ownership."

## Quick prompt → story map

| Interview prompt | Lead with |
|------------------|-----------|
| Ambiguity / requirements | Story 1 (source docs) |
| Stakeholders / scope | Story 2 |
| Incident / debugging | Story 3 (781 primary; 784 as open follow-up) |
| Ownership / impact | Story 4 (Zendesk) |
| System design deep-dive | Hand off to [[interview-prep/system-design-clearview.md]] |
