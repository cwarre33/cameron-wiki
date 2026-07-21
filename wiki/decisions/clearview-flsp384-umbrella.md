---
title: "ADR: Keep FLSP-384 Open as Umbrella"
type: decision
status: superseded
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp383_build_phase.md
  - raw/fls-work/jira/2026-07-21/flsp-103/project_flsp383_build_phase.md
  - jira:FLSP-384
related:
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[production-systems/inventory-lookup-clearview.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [adr, clearview, jira, flsp-384, umbrella, furnitureland-south]
---

# ADR: Keep FLSP-384 Open as Umbrella

## Decision (historical process intent)

**Originally:** keep [FLSP-384](https://furniturelandsouth.atlassian.net/browse/FLSP-384) ("Search and lookup core") **In Progress** as a deliberate umbrella story — do not flag it closeable from wiki synthesis or sub-task completion alone.

## Live status supersession (Task 10 lint, 2026-07-21)

⚠️ **Critical contradiction fixed:** Catch-up pages claimed FLSP-384 was still **In Progress** and must stay open. **Live Jira status is Done** (updated 2026-07-02). Workflow truth = **Done**. Do not list FLSP-384 on open-work tables.

This ADR remains as the *process rationale* for why the story was once kept open as an umbrella; it does **not** override current Jira. Frontmatter `status: superseded` marks the keep-open instruction as obsolete.

## Context

FLSP-384's only sub-task (FLSP-393 synonym/normalization research) is Done. Results/display work largely lives under FLSP-386 (also Done). The keep-open intent was to preserve a parent thread for search/lookup core overlapping browse/perf work under FLSP-391.

Frozen build-phase memory listed FLSP-384 as "Done" on the tree line while a deliberate-decision paragraph said keep **In Progress**. Early catch-up pages followed the deliberate decision and incorrectly asserted live Jira was still In Progress — that assertion was wrong as of 2026-07-02.

## Options considered

| Option | Outcome |
|--------|---------|
| Close FLSP-384 because only sub-task Done | Loses umbrella for overlapping search/results thread |
| Keep In Progress as umbrella | Matches earlier process intent; was the catch-up default |
| Match live Jira (**Done**) | Correct for status queries; process intent preserved in this ADR only |

## Decision rationale (why umbrella existed)

1. Umbrella stories are process tools, not only DoD checklists
2. Overlap with FLSP-386 results work was intentional, not incomplete hygiene
3. Agents/audits must not auto-recommend close from "sub-tasks complete" alone — but once Jira is Done, wiki status must follow Jira

## Outcome (current)

- Live Jira: **Done** (2026-07-02)
- Initiative / ClearView hub / overview open lists: FLSP-384 removed from open work (Task 10)
- Historical umbrella rationale retained on this page only
