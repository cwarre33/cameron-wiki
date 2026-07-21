# FLS Jira Living-Wiki Catch-Up Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Wiki ingest rule override:** Every Phase that creates pages MUST discuss top takeaways with Cameron and wait for confirmation before writing that Phase's pages. Do not batch-write an entire Phase unseen.

**Goal:** Bring `cameron-wiki` from a May-2026 FLS snapshot to a deep, living record of Cameron's Jira/production work through 2026-07-21 — especially FLSP-103 ClearView, plus every other assignee/reporter cluster that currently has thin or missing wiki coverage.

**Architecture:** Three-tier depth model + initiative-first navigation. Immutable Jira/memory snapshots land in `raw/fls-work/`, then wiki pages synthesize (never dump). One page per *system* or *initiative*, compact epic indexes underneath — never one page per sub-task.

**Tech Stack / Sources:** Atlassian Jira (FLSP/FLSM/FLSI/ITT), Claude project memories under `~/.claude/projects/.../memory/`, local repos under `CleanDevEnvironment/`, existing `wiki/production-systems/*`.

## Global Constraints

- `visibility: fls-internal` for anything with proprietary FLS detail; never publish without sanitization
- **NEVER modify `raw/` after initial creation** of each source file
- **NEVER answer from memory alone** during later queries — consult wiki pages written here
- Prefer compact key/status/assignee/summary indexes over raw Jira dumps (signal-to-noise)
- Neutral factual framing of who-did-what; no implied blame
- Verify closeability claims against Confluence/SharePoint when relevant, not code alone
- `wiki/index.md` is auto-regenerated — do not hand-edit; append `wiki/log.md` only
- Date stamp all new pages `created/updated: 2026-07-21` (or actual write day)
- Flag contradictions with May-2026 wiki pages explicitly (do not silently overwrite)

## Depth model (locked)

| Tier | What goes here | Shape |
|------|----------------|-------|
| **A — Deep synthesis** | Systems Cameron built/owned end-to-end | Full production-system / architecture / ADR pages with stack, decisions, interview angles |
| **B — Compact index** | Initiatives & epics (Jira trees) | One file per initiative or epic: key · status · assignee · one-line summary |
| **C — Catalog row** | Peripheral tickets (ITT, one-off maintenance) | Rows in period work-log tables only |

**Anti-pattern:** 125 wiki pages for FLSP-103. **Do:** 1 initiative index + 4 epic indexes + ~8–12 Tier-A synthesis pages for ClearView subsystems.

## Current gap (evidence, 2026-07-21)

**Wiki last deep FLS ingest:** 2026-05-20 (`wiki/work-log/2026-05-period-summary.md`).

**Assignee footprint (partial Jira pull):** 100+ issues returned with `isLast: false` — FLSP-heavy; also FLSM, FLSI, ITT. FLSP alone has 93 issues updated since 2026-05-20.

**Already in wiki (thin/stale):** ClearView (as FLSP-159 only), pilot DB, dedicated agent, SellSmart Copilot, NS→ZD sync, Zendesk returns, SofaScope.

**Missing or critically stale:**
- FLSP-103 initiative hierarchy + Build Phase reality (AWS/ECS, Entra, RDS delta sync, Approach export)
- FLSP-247 Digital-to-Store / FLS Data Lookup agents
- CRR / Round Robin / views / agent-status Task Server cluster (FLSI deep history)
- Call transcript pipeline (repo memory exists; no production-system page)
- SellSmart analytics / monthly refreshes / Copilot epic FLSM-10
- Calendar app (FLSP-68), agent online bat, OAuth refresh (FLSM-24)
- ~50 ClearView Claude-memory files never promoted to wiki

## Target wiki information architecture

```
raw/fls-work/jira/2026-07-21/          # immutable snapshots (Tier B sources)
  flsp-103-initiative-index.md
  flsp-104-discovery.md
  flsp-167-design.md
  flsp-159-barcodes.md
  flsp-383-build.md
  cameron-assignee-catalog.md          # Tier C master list (all projects)
  ...

wiki/initiatives/                      # NEW section — Tier B navigation hubs
  flsp-103-inventory-lookup.md
  flsp-247-digital-to-store.md
  zendesk-automation-platform.md       # umbrella for CRR/RR/views/transcripts
  sellsmart-program.md

wiki/production-systems/               # Tier A — expand/update
  inventory-lookup-clearview.md        # REWRITE as hosted product
  clearview-aws-hosting.md             # NEW
  clearview-rds-delta-sync.md          # NEW
  clearview-entra-sso.md               # NEW (or integrations/)
  approach-reporting.md                # NEW
  dedicated-agent-assignment.md        # UPDATE (Done, not Testing)
  crr-round-robin.md                   # NEW
  zendesk-call-transcripts.md          # NEW
  digital-to-store-copilot.md          # NEW
  zendesk-shared-views.md              # NEW (lighter)
  ...

wiki/integrations/
  fls-aws-topology.md                  # NEW (from memory reference)
  netsuite-suitetalk-jwt.md            # NEW
  ...

wiki/decisions/                        # ClearView + Zendesk ADRs
  clearview-approach-export-scope.md
  clearview-location-movement-deferred.md
  clearview-flsp384-umbrella.md
  authjs-v5-authorized-callback.md
  ...

wiki/techniques/
  rds-delta-sync-watermarks.md
  vmpn-serial-snapshot.md
  ...

wiki/interview-prep/
  system-design-clearview.md           # NEW — hosted Next.js + RDS + NetSuite
  behavioral-zendesk-automation.md     # NEW

wiki/work-log/
  2026-05-period-summary.md            # leave; link forward
  2026-06-07-fls-catchup.md            # NEW period synthesis

wiki/methodology/
  neutral-history-framing.md
  verify-against-source-docs.md
```

Exact filenames may shift ±1 during Phase 0 if a better name emerges; keep the *roles* above.

## Source inventory to freeze into `raw/`

Copy (do not move) from Claude memories — treat as first-class sources:

| Source path | Becomes |
|-------------|---------|
| `...Inventory-Lookup/memory/project_flsp103_*.md` + epic files | `raw/fls-work/jira/2026-07-21/flsp-103/*` |
| Other `project_flsp*.md`, `project_*`, `reference_*` ClearView memories | `raw/fls-work/clearview-memory/2026-07-21/*` |
| `...Zendesk-FLSP-247/memory/*` | `raw/fls-work/jira/2026-07-21/flsp-247/*` |
| `...ZendeskCallAutoTranscript/memory/MEMORY.md` | `raw/fls-work/transcripts/2026-07-21-memory.md` |
| `...ZendeskTools/memory/MEMORY.md` | `raw/fls-work/zendesk-tools/2026-07-21-memory.md` |
| Fresh Jira JQL export (assignee=currentUser, all projects) | `raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md` |

Plus live Jira reads during each Phase for status freshness.

---

### Task 0: Freeze sources + schema scaffolding

**Files:**
- Create: `raw/fls-work/jira/2026-07-21/**` (copies + assignee catalog)
- Create: `raw/fls-work/clearview-memory/2026-07-21/**`
- Create: `wiki/initiatives/.gitkeep` (or first initiative page in Task 1)
- Modify: none yet in `wiki/` except later log

**Produces:** Immutable source tree other tasks cite in frontmatter `sources:`.

- [ ] **Step 1: Export full assignee catalog from Jira**

Run Atlassian MCP `searchJiraIssuesUsingJql` with pagination until `isLast: true`:

```
assignee = currentUser() ORDER BY project ASC, updated DESC
```

Fields: `summary, status, issuetype, project, parent, updated, created, assignee`.

Write compact markdown to `raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md` (table: key | project | type | status | updated | summary). Tier C destination.

- [ ] **Step 2: Copy ClearView memory freeze**

Copy the FLSP-103 initiative + 4 epic memory files and all `project_*` / `reference_*` / `feedback_*` ClearView memories into `raw/fls-work/...` as listed above. Do not edit contents after write.

- [ ] **Step 3: Copy non-ClearView memory freezes**

FLSP-247, ZendeskTools, ZendeskCallAutoTranscript, SellSmartTools (if useful), ItemInventoryStory if present.

- [ ] **Step 4: Confirm Tier A/B/C page list with Cameron**

Present the proposed page list (from IA section) as a checklist. Wait for add/drop before Phase 1 writes.

- [ ] **Step 5: Append log entry for source freeze only**

```
## [2026-07-21] ingest | FLS Jira catch-up — raw source freeze
Source: Claude memories + Jira assignee export
Pages created: [none — raw only]
Pages updated: [none]
Contradictions: [none]
```

---

### Task 1: FLSP-103 initiative + epic indexes (Tier B)

**Files:**
- Create: `wiki/initiatives/flsp-103-inventory-lookup.md`
- Create: `wiki/initiatives/flsp-103-discovery.md` (or fold Discovery/Design into parent if Cameron prefers fewer pages — default: parent + 4 epic sections OR 1 parent + link to build detail)
- Prefer **1 initiative page with 4 epic sections** if page count is a concern; otherwise 1 + 4 files matching memory layout
- Modify: `wiki/overview.md` (pointer only, after pages exist)

**Cameron decisions (2026-07-21):**
- One fat FLSP-103 initiative page (all 4 epics inline)
- ClearView Session 2: **full subsystem split**
- Transcripts / Shared Views / Calendar: **Tier A** pages
- Hubs use `type: production-system` + tags `[initiative, jira-index]` (no schema extension)
- Execution: **subagent-driven**
- **Full Jira activity audit** required before/during build (not memory-only)

- [ ] **Step 1: Discuss takeaways (gate)**

Present:
1. FLSP-103 is the true parent (not FLSP-159)
2. Rollup field unreliable — Parent Link tree is source of truth
3. Open items list as of freeze date
4. FLSP-384 umbrella decision

Wait for confirm.

- [ ] **Step 2: Write initiative page**

Use `type: production-system` with tags `[initiative, jira-index]`.

- [ ] **Step 3: Cross-link** from future ClearView production page and work-log

- [ ] **Step 4: Log append**

---

### Task 2: Rewrite ClearView production-system page (Tier A hub)

**Files:**
- Modify: `wiki/production-systems/inventory-lookup-clearview.md` (full rewrite)
- Related updates: `pilot-database-migration.md` (status + links)

**Contradiction to flag in page:**
- Old: FLSP-159 Epic status Testing; New: Post Prod Validation; parent initiative FLSP-103 In Progress
- Old: suitelet replacement narrative; New: hosted ClearView product (ECS/Fargate, Entra, RDS ~5GB, delta sync)

- [ ] **Step 1: Discuss takeaways (gate)** — hosted product story, stack table, open threads
- [ ] **Step 2: Rewrite page** — sections: Purpose, Initiative link, Stack, Surfaces (routes), Data plane (NetSuite + RDS), Auth, Ops (CI/CD), Open work, Interview angles
- [ ] **Step 3: Update pilot-database page** related links + note full-scale parity complete (2026-06-22) vs original windowed pilot framing — flag if contradiction
- [ ] **Step 4: Log append**

---

### Task 3: ClearView subsystem deep pages (Tier A cluster)

**Files to create (from memory → wiki synthesis):**

| Wiki page | Primary sources |
|-----------|-----------------|
| `wiki/production-systems/clearview-aws-hosting.md` | `project_flsp403_aws_hosting.md`, `reference_fls_aws_topology.md` |
| `wiki/production-systems/clearview-rds-delta-sync.md` | `project_shared_rds_dev_db.md`, `project_rds_delta_runner.md`, `project_delta_sync_build.md`, `project_full_scale_parity.md`, FLSP-547/548 |
| `wiki/integrations/clearview-entra-sso.md` | FLSP-414 tree, `project_auth_gating_regression.md`, `reference_minted_session_jwt.md` |
| `wiki/production-systems/approach-reporting.md` | `project_flsp508_*`, `reference_approach_report_docs.md` |
| `wiki/techniques/vmpn-serial-snapshot.md` | `project_flsp646_serial_snapshot.md` |
| `wiki/techniques/rds-delta-sync-watermarks.md` | `project_flsp547_txn_lane_drain.md` |
| `wiki/integrations/fls-aws-topology.md` | `reference_fls_aws_topology.md` |
| `wiki/integrations/netsuite-suitetalk-jwt.md` | `project_netsuite_auth.md` + ja-utility-shed pattern |

**ADRs to create:**

| ADR | Decision |
|-----|----------|
| `wiki/decisions/clearview-approach-export-scope.md` | Close FLSP-508 without PDF/pivots |
| `wiki/decisions/clearview-location-movement-deferred.md` | Revert building-level movement; Oracle DW later |
| `wiki/decisions/clearview-flsp384-umbrella.md` | Keep FLSP-384 open as umbrella |
| `wiki/decisions/authjs-v5-authorized-callback.md` | Auth.js v5 trap + fix |

- [ ] **Step 1: Discuss takeaways for this cluster (gate)** — propose which of the 8+4 pages to keep vs fold into hub
- [ ] **Step 2: Write approved pages** one batch after approval
- [ ] **Step 3: Wire `[[wikilinks]]` among hub, subsystems, ADRs, initiative index
- [ ] **Step 4: Log append**

---

### Task 4: Zendesk automation platform (Tier A + B)

**Scope from Jira/memory (non-exhaustive):** Dedicated Agent (Done), Round Robin CCS/VCS, Shared Views cleanup, agent-status Task Server jobs, FLSP-160 Weimer vendor routing, FLSM-20 customer sync, FLSM-33/34/35 CRR tweaks, FLSP-138 Set Agents Online retry, FLSP-68 calendar app, call transcripts.

**Files:**
- Create: `wiki/initiatives/zendesk-automation-platform.md` (Tier B umbrella index)
- Update: `wiki/production-systems/dedicated-agent-assignment.md` (status Done; expand post-launch FLSI-2965 etc.)
- Create: `wiki/production-systems/crr-round-robin.md`
- Create: `wiki/production-systems/zendesk-call-transcripts.md`
- Create: `wiki/production-systems/zendesk-shared-views.md` (lighter Tier A)
- Update: `wiki/integrations/netsuite-zendesk-customer-sync.md` (FLSM-20 now Post Prod Validation)
- Create: `wiki/production-systems/zendesk-ticket-calendar.md` (Tier A — Cameron decision 2026-07-21)

- [ ] **Step 1: Jira + repo pass** — pull FLSP-163/160/68 trees; read DedicatedAgentAssignment + ZendeskCallAutoTranscript + ZendeskSharedViews repos enough to ground claims
- [ ] **Step 2: Discuss takeaways (gate)**
- [ ] **Step 3: Write/update pages**
- [ ] **Step 4: Log append**

**Note:** Overview currently says "CRR deep-dive — still deferred" — this task retires that gap.

---

### Task 5: Copilot / SellSmart / Digital-to-Store (Tier A)

**Files:**
- Create: `wiki/production-systems/digital-to-store-copilot.md` (FLSP-247; from frontier memory + Jira 248–251)
- Create: `wiki/initiatives/sellsmart-program.md` (FLSI-2333 / FLSM-10 / DC Furniture Discovery FLSP-85–89)
- Update: `wiki/production-systems/sellsmart-copilot.md`
- Update: `wiki/integrations/sellsmart-netsuite-rest-tool.md`
- Optional ADR: perf acceptance for SuiteQL ~23s browse (from FLSP-247 frontier)

- [ ] **Step 1: Discuss takeaways (gate)**
- [ ] **Step 2: Write/update**
- [ ] **Step 3: Log append**

---

### Task 6: SofaScope + older FLSI catch-up (Tier A refresh + Tier C)

**Files:**
- Update: `wiki/production-systems/sofascope.md` (FLSI-2593 tweaks, training video FLSI-2826, Copilot tool backlog FLSI-3004)
- Add Tier C rows to period work-log for Deployed testing tasks / Stella bot / KB gaps unless they deserve their own pages

- [ ] **Step 1: Diff SofaScope wiki vs Jira FLSI-2103 epic children Cameron touched**
- [ ] **Step 2: Discuss whether Stella/KB/case-dashboard get pages or catalog rows only**
- [ ] **Step 3: Write approved updates**
- [ ] **Step 4: Log append**

---

### Task 7: Maintenance / FLSM odds + ends (Tier B/C)

**Candidates:**
- FLSM-24 / FLSM-27 Zendesk OAuth refresh deadline (Oct 27, 2026) — worth a short `wiki/open-questions/` or maintenance page
- FLSM-5 / FLSM-25 / FLSM-36 SellSmart monthly refreshes — catalog under SellSmart program
- ITT tickets — catalog only unless investigation produced durable technique

- [ ] **Step 1: Discuss which get pages vs catalog**
- [ ] **Step 2: Write**
- [ ] **Step 3: Log append**

---

### Task 8: Methodology + interview layer

**Files:**
- Create: `wiki/methodology/neutral-history-framing.md`
- Create: `wiki/methodology/verify-against-source-docs.md`
- Create: `wiki/interview-prep/system-design-clearview.md`
- Create: `wiki/interview-prep/behavioral-fls-delivery.md` (spec-driven Jira, stakeholder loops, prod incidents 781/784)

- [ ] **Step 1: Discuss interview angles to emphasize**
- [ ] **Step 2: Write**
- [ ] **Step 3: Log append**

---

### Task 9: Period work-log + overview synthesis

**Files:**
- Create: `wiki/work-log/2026-06-07-fls-catchup.md` (covers May 21 → Jul 21)
- Modify: `wiki/overview.md` — strongest areas, recent work, retire stale gaps
- Modify: `wiki/work-log/2026-05-period-summary.md` — add "Superseded for ClearView status by …" note at top (do not rewrite history)

- [ ] **Step 1: Draft period summary structure for Cameron review**
- [ ] **Step 2: Write after approval**
- [ ] **Step 3: Log append for synthesis**

---

### Task 10: Lint + open questions

Run wiki lint workflow:

1. Contradictions (especially ClearView status, dedicated-agent status, pilot DB "windowed" vs full-scale)
2. Orphans among new initiative pages
3. Missing pages mentioned 3+ times
4. Stale May claims
5. Weak sourcing
6. Missing cross-refs
7. Suggest 5 next questions + 3 next sources

- [ ] **Step 1: Produce lint report for Cameron**
- [ ] **Step 2: Fix 🔴 items immediately**
- [ ] **Step 3: Final log entry for catch-up complete**

---

## Execution order & session sizing

| Session | Tasks | Est. pages touched |
|---------|-------|--------------------|
| 1 | 0 + 1 + 2 | sources + initiative + ClearView hub rewrite |
| 2 | 3 | ClearView subsystems + ADRs |
| 3 | 4 | Zendesk platform |
| 4 | 5 + 6 | Copilot/SellSmart + SofaScope |
| 5 | 7 + 8 + 9 + 10 | maintenance, interview, synthesis, lint |

Do not start Session N+1 until Cameron has confirmed Session N takeaways/pages.

## Out of scope (unless Cameron expands)

- Personal Passion/Kaggle/AutoTrader refreshes (separate catch-up)
- OSINT/disclosure corpus (already dense)
- Rewriting `wiki/index.md` by hand
- Importing full Jira comment threads / attachments into wiki (link out; Approach PDF stays referenced via FLSP-109)

## Success criteria

1. Asking "What have I done on ClearView?" yields FLSP-103-rooted answer with AWS/SSO/RDS/Approach depth and `[[wikilinks]]`
2. Asking "What Zendesk systems did I ship?" covers Dedicated Agent, Round Robin, views, transcripts, returns — not just one Lambda
3. Every Cameron assignee story since May 2026 appears at least as a Tier C catalog row
4. May-2026 contradictions are flagged, not papered over
5. Interview prep pages cite real production pages

## Self-review (plan vs request)

| Request | Covered by |
|---------|------------|
| Capture max depth for FLSP-103 | Tasks 1–3 |
| Anything worked on in Jira | Tasks 0 catalog + 4–7 |
| Living wiki for reference | Tier A systems + Tier B hubs + work-log |
| Massive update after long gap | Phased sessions 1–5 + lint |
| Signal-to-noise | Depth model; no per-subtask pages |

No TBD placeholders for required structure; exact prose of each wiki page is produced at execution time after takeaway gates (required by wiki ingest rules).
