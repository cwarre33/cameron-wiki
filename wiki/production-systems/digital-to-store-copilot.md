---
title: Digital-to-Store Copilot Agents (FLSP-247)
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-07-21/flsp-247/flsp-247-frontier.md
  - raw/fls-work/jira/2026-07-21/flsp-247/flsp-247-environment.md
  - raw/fls-work/jira/2026-07-21/flsp-247/MEMORY.md
  - raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md
  - raw/fls-work/jira/2026-07-21/cluster-map.md
  - raw/fls-work/jira/2026-07-21/AUDIT_REPORT.md
related:
  - "[[initiatives/sellsmart-program.md]]"
  - "[[production-systems/sellsmart-copilot.md]]"
  - "[[integrations/sellsmart-netsuite-rest-tool.md]]"
  - "[[integrations/netsuite-suitetalk-jwt.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [digital-to-store, copilot-studio, popdock, suiteql, netsuite, fls, production]
---

# Digital-to-Store Copilot Agents (FLSP-247)

[FLSP-247](https://furniturelandsouth.atlassian.net/browse/FLSP-247) is the epic for Furnitureland South's **Digital-to-Store Guided Shopping Experience** — two Microsoft Copilot Studio agents backed by **Popdock → NetSuite SuiteQL**.

**Epic status (live 2026-07-21):** **Testing**. Stories FLSP-248–251 are **Ready for Deployment**; sub-task FLSP-255 remains **In Progress**.

**Workspace:** `CleanDevEnvironment/Zendesk/FLSP-247/` (docs/SQL workspace, not a code repo). Structure: `agents/`, `suiteql/`, `testing/`, `reference/`, `topics/`. Folder consolidated 2026-06-19 — old per-version drafts were deleted and the folder is **not git-tracked**.

Related DC-facing Copilot program: [[initiatives/sellsmart-program.md]] / [[production-systems/sellsmart-copilot.md]] (different audience; shared Copilot Studio + SuiteQL patterns).

## Two agents

| Agent | Audience | Artifact | Frontier |
|-------|----------|----------|----------|
| **FLS Data Lookup Agent** | Internal staff | `agents/fls-data-lookup.md` | FLSP-248/249/250 largely complete earlier; staff lookup path |
| **Digital-To-Store Guided Experience** | Customer shoppers | `agents/digital-to-store.md` | Active product frontier through June 2026 sign-off |

**Customer agent tools:** `LookupProductBySku`, `LookupByProductClass`, `LookupByVendor`, `LookupByDisplayLocation`.

## Architecture

```
Customer / staff chat (Copilot Studio)
  → Knowledge sources (Zendesk HC primary)
  → Popdock lists (SuiteQL-backed)
  → NetSuite (item / inventory / classification)
```

- **Popdock** holds deployed SuiteQL lists; Cameron pastes validated `.sql` from the FLSP-247 workspace into Popdock and runs the Testing tab.
- **Live SuiteQL validation** (before Popdock paste) uses sibling `NetSuite/ja-utlity-shed` (`ns.postQuery`, prod JWT/PS256, role 1109). See [[integrations/netsuite-suitetalk-jwt.md]].
- ODBC role 1070 available for note/narrative tables via `nsodbc.js`.

## Story index (FLSP-247 tree)

| Key | Summary | Status (live 2026-07-21) |
|-----|---------|--------------------------|
| [FLSP-247](https://furniturelandsouth.atlassian.net/browse/FLSP-247) | Digital-to-Store Guided Shopping Experience (epic) | **Testing** |
| [FLSP-248](https://furniturelandsouth.atlassian.net/browse/FLSP-248) | Customer can ask questions about store and policies | **Ready for Deployment** |
| [FLSP-249](https://furniturelandsouth.atlassian.net/browse/FLSP-249) | Customer can check if a product is on display | **Ready for Deployment** |
| [FLSP-250](https://furniturelandsouth.atlassian.net/browse/FLSP-250) | Customer receives guided prompts for QA and product checks | **Ready for Deployment** |
| [FLSP-251](https://furniturelandsouth.atlassian.net/browse/FLSP-251) | Copilot Agent is created and configured | **Ready for Deployment** |
| [FLSP-255](https://furniturelandsouth.atlassian.net/browse/FLSP-255) | Design guided entry experience (no empty chat) | **In Progress** |

Cluster map (2026-07-21): 6 assignee issues; Done-ish / Open-ish ≈ **4 / 2**.

## June 2026 acceptance (frontier memory)

Jaylon review (2026-06-18) mapped to Jira; Cameron posted sign-off comments 2026-06-19 (FLSP-251/249/248 comments 59176–59178). Acceptance record: `testing/jira-signoff-2026-06-19.md`.

Key product decisions landed then:

- **Instructions (FLSP-251):** customer tone, Zendesk-primary, room→class, colloquial→strict. Bed strict class is **`Bed`** (singular). Location mapping: **M=Mart, S=Showroom, O=Outlet** (location 75).
- **SuiteQL (FLSP-249):** cap + vendor-interleave + display-first on browse queries; inventory-driven restructure trimmed class browse **34s → ~23s**. Verified live + in Popdock. **Cameron accepted ~23s** — cached-rollup perf follow-up **dropped**.
- **KB priority (FLSP-248):** Zendesk primary; Core 10 = 10/10. Website (`furniturelandsouth.com`) knowledge source **removed** so citations stay Zendesk-only.
- **LookupByDisplayLocation:** query pasted, tool enabled, instructions published, D-block tests passed 2026-06-19.

⚠️ Frontier memory labels stories “DONE”; **live Jira still shows Ready for Deployment** for FLSP-248–251 and epic **Testing**. Treat Jira as workflow truth; memory as technical acceptance.

## Open residual

1. **FLSP-247 epic** still **Testing** — stories Ready for Deployment but epic not closed.
2. **FLSP-255** — guided entry (no empty chat) still **In Progress**.
3. **Fallback topic** — out-of-scope declines still use Copilot's generic Fallback ("not sure how to help"); instruction edits cannot override it. Needs a customized **Fallback system topic** for Guest Services redirect. Safe as-is (declines, no leak).

## Interview angles

- **Popdock as SuiteQL deploy surface:** validate in utility shed → paste to Popdock → Copilot tools
- **Perf acceptance:** ~23s browse accepted deliberately; document facts, don't chase vanity latency
- **KB hygiene:** remove competing website source so Zendesk HC citations win
