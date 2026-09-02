# FLS Git + Jira Wiki Catch-Up Implementation Plan (Sep 2026)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Wiki ingest rule override:** Every Phase that creates or substantially rewrites pages MUST discuss top takeaways with Cameron and wait for confirmation before writing that Phase's pages. Do not batch-write an entire Phase unseen.

**Goal:** Bring `cameron-wiki` current through **2026-09-02** by mining local git history + Bitbucket (commits, PRs, messages), enriching with live Jira status/parent trees, and folding in Cameron-provided production context (user counts, adoption, validation status) — without raw dumps.

**Architecture:** **Git-first evidence graph** → Jira enrichment → subsystem synthesis. Immutable extracts land in `raw/fls-work/` (gitignored). Wiki pages stay Tier A/B/C with the same depth model as the July catch-up. Public-repo pages omit ticket keys; join keys live in `raw/` + private tracker.

**Tech Stack / Sources:** Local clones under `CleanDevEnvironment/`, Bitbucket Cloud API (GCM Bearer from `Inventory-Lookup`), Atlassian Jira MCP, Claude project memories, Cameron oral/written context intake.

---

## Global Constraints

- `visibility: fls-internal` for proprietary FLS detail; **omit Jira keys from committed wiki pages** (July precedent) unless Cameron explicitly opts back in for a page
- **NEVER modify `raw/` after initial creation** of each frozen file
- **NEVER answer from memory alone** during later queries — consult wiki pages written here
- Prefer compact indexes + synthesis over dumps; git commit subjects are evidence, not wiki body text
- Neutral factual framing; verify closeability against Confluence/SharePoint when claiming production done
- `wiki/index.md` auto-regenerated — do not hand-edit; append-only `wiki/log.md`
- Flag contradictions with July-2026 wiki explicitly (mobile backlog, ops-health Testing, etc.)
- Career canvases (`fls-career-stats`, `fls-contribution-graph`) refresh at end, not mid-ingest

---

## Gap analysis (evidence, 2026-09-02)

**Wiki last FLS deep ingest:** 2026-07-30 (`wiki/work-log/2026-07-30-four-week-lookback.md`). Overview `updated: 2026-07-21`.

**Window:** 2026-07-31 → 2026-09-02 (~33 days).

| Signal | Count | Notes |
|--------|------:|-------|
| `inventory-lookup` commits (Cameron, since 7/31) | **508** | Dominant theme: Shop/RMF (~181 commit subjects mention shop/rmf) |
| Unique Jira keys in commit subjects | **70** | Top: FLSP-942 (58), FLSP-949 (24), FLSP-1021 (19), FLSP-860 (18), FLSP-1169 (17) |
| Merged PRs on `inventory-lookup` | **~111→187** | +76 PRs since late July (PR #187 latest sample) |
| Jira assignee `updated >= 2026-07-31` | **224** | **202** Done-category |
| Wiki pages mentioning Shop/RMF | **0** | Major blind spot |

**Largest missing product surface:** Epic **PIE & Shop Replacement** (parent tree under FLSP-856) — NetSuite Shop Request records, RMF tab, duplicate checks, attachments (HEIC), request relationships, VRA handoff (FLSP-782), subscription emails, role permissions (FLSP-1206 in progress).

**July wiki claims likely stale:**
- ClearView = inventory search + hosting only → now **operations platform** (Shop/RMF, orders UX, notifications)
- Mobile camera scan "In Progress" → verify against git/Jira
- Ops-health parent "Testing" → verify closeability
- Build Phase epic Done → new work lives under FLSP-856 + FLSP-217 (VRA)

---

## Depth model (unchanged from July)

| Tier | What | Shape |
|------|------|-------|
| **A** | End-to-end systems Cameron built/owned | Full `production-system` / `decision` pages |
| **B** | Initiatives & epics | One fat initiative page OR compact epic index inline |
| **C** | Peripheral / ITT noise | Work-log table rows only |

**Anti-pattern:** 70 wiki pages for 70 Jira keys. **Do:** ~3–6 new Tier-A Shop/RMF pages + update hub + initiative index + one period work-log.

---

## Source hierarchy (when sources disagree)

1. **Production reality** — Cameron-provided metrics + Confluence/SharePoint validation docs
2. **Merged git on `main`** — what actually shipped
3. **Live Jira status** — closeout truth (Parent Link > rollup fields)
4. **Commit messages** — intent, ADR hints, deferred scope
5. **Claude memory** — gap-fill only; flag if stale vs git/Jira

---

## Phase 0 — Freeze immutable extracts (`raw/fls-work/`)

**No wiki writes.** Build the evidence layer agents will cite.

### 0.1 Local git mining (all FLS repos on machine)

Repos to scan (priority order):

1. `CleanDevEnvironment/NetSuite/Inventory-Lookup` (primary)
2. `CleanDevEnvironment/Zendesk/**` (nested `.git`)
3. `CleanDevEnvironment/SellSmartTools/**`
4. `CleanDevEnvironment/NetSuite/ClearView` (if active)
5. Any repo with `bitbucket.org/furniturelandsouth` remote (discover via shallow scan)

Per repo, freeze to `raw/fls-work/git/2026-09-02/<repo-slug>/`:

| File | Contents |
|------|----------|
| `commits-since-2026-07-31.jsonl` | hash, author, date, subject, body, parents |
| `commit-key-index.md` | FLSP/FLSM/FLSI/ITT keys → commit count, date range, sample subjects |
| `pr-merged-since-2026-07-31.md` | PR id, title, merged date (from git merge commits + Bitbucket API) |
| `theme-clusters.md` | Keyword clusters: shop, rmf, vra, orders, attachment, notification, infra, mobile |

**Git commands (reference):**

```bash
git log --since=2026-07-31 --format='%H|%an|%ae|%ad|%s' --date=iso-strict
git log --since=2026-07-31 --grep='FLSP-' --format='%s'
git shortlog -sn --since=2026-07-31
```

### 0.2 Bitbucket API scrape (GCM Bearer)

Auth: `git credential fill` from `Inventory-Lookup` → Bearer token (discovered Jul 2026).

Freeze to `raw/fls-work/bitbucket/2026-09-02/`:

- `repos-member.json` — workspace `furniturelandsouth`
- `prs-authored-merged.json` — per repo, deduped by PR id
- `career-stats-delta.json` — commits/PRs since last scrape (2026-07-31 baseline)

### 0.3 Jira delta freeze

JQL snapshots → `raw/fls-work/jira/2026-09-02/`:

| File | JQL |
|------|-----|
| `assignee-updated-since-0731.json` | `assignee = currentUser() AND updated >= 2026-07-31` |
| `flsp-856-epic-tree.md` | `"Parent Link" = FLSP-856 OR parent = FLSP-856` (compact index) |
| `flsp-103-open-items.md` | Open ClearView cluster refresh |
| `reporter-since-0731.json` | `reporter = currentUser() AND updated >= 2026-07-31` |

For each **unique key** appearing ≥3 times in git index, fetch summary + status + parent (batch MCP).

### 0.4 Claude memory harvest

Copy (don't move) from `~/.claude/projects/C--Users-cameronwarren-CleanDevEnvironment-NetSuite-Inventory-Lookup/memory/` → `raw/fls-work/clearview-memory/2026-09-02/`

Especially: Shop/RMF plans, VRA, notification design, role permission docs.

### 0.5 Deliverable

`raw/fls-work/git/2026-09-02/AUDIT_REPORT.md` — executive summary:

- Commit/PR totals per repo
- Top 10 subsystem themes by commit volume
- Top 20 Jira keys by commit mentions
- Wiki pages that **must** be created vs updated
- Contradictions vs July wiki

- [x] **Step 0 complete** — AUDIT_REPORT at `raw/fls-work/git/2026-09-02/AUDIT_REPORT.md` (2026-09-02); awaiting Cameron Gate 1

---

## Phase 1 — Cluster map & takeaway gate (no wiki writes yet)

Produce a **single briefing doc** (can live in `.superpowers/sdd/` scratch or chat) with:

### 1.1 Subsystem clusters (proposed Tier A pages)

| Cluster | Evidence | Proposed wiki page |
|---------|----------|-------------------|
| **Shop/RMF requests** | FLSP-856 epic, FLSP-858/860/942/1021, 181 shop commits | `wiki/production-systems/clearview-shop-rmf-requests.md` **NEW** |
| **RMF attachments & preview** | FLSP-1202, HEIC/sanitizer commits | Section in Shop page or `clearview-rmf-attachments.md` |
| **Request relationships** | FLSP-1204, case/RA/RI history | Section in Shop page |
| **Duplicate request guard** | FLSP-869 | `wiki/decisions/clearview-shop-duplicate-guard.md` **NEW** (ADR) |
| **VRA handoff** | FLSP-782, barcode Suitelet intake | `wiki/production-systems/clearview-vra-handoff.md` **NEW** |
| **Orders UX refresh** | FLSP-949 Done | Update `inventory-lookup-clearview` or light `clearview-orders-ux.md` |
| **Notifications / subscriptions** | FLSP-1169, FLSP-862 parent | `wiki/production-systems/clearview-notifications.md` **NEW** |
| **Role permissions (Shop/RMF)** | FLSP-1206 in progress | `wiki/open-questions/clearview-shop-role-permissions.md` until done |
| **Jul carry-forward** | mobile, ops-health, OAuth | Update existing pages + close stale open-work |

### 1.2 Cameron context intake (required before Tier A writes)

Ask Cameron to provide (bullets fine):

| Field | Why wiki needs it |
|-------|-------------------|
| **ClearView active users** (weekly/daily, roles) | Production impact; interview prep |
| **Shop/RMF request volume** (per week, prod vs staging) | Validates "shipped" narrative |
| **PIE sunset / replacement status** | Epic FLSP-856 framing |
| **VRA adoption** | FLSP-782 Post Prod Validation context |
| **Mobile/iPad rollout** | Close FLSP-390 story |
| **Any demos / sign-offs** (dates, stakeholders) | Neutral timeline |
| **What is NOT production yet** | Prevents over-claiming |

Store Cameron answers in `raw/fls-work/context/2026-09-02-cameron-intake.md` (create once; immutable).

### 1.3 Takeaway gate

Present **top 5 takeaways** + proposed page list. **Wait for Cameron confirm/refine.**

- [ ] **Gate 1 passed** — Cameron approved cluster map + page list

---

## Phase 2 — Wiki writes (by cluster, gated per cluster)

Each sub-phase: discuss → confirm → write → log.

### 2.1 Period work-log

- [ ] Create `wiki/work-log/2026-08-09-clearview-shop-rmf-sprint.md`
- [ ] Link from `overview.md` Recent work section
- [ ] Append `wiki/log.md` ingest entry

### 2.2 ClearView hub + initiative refresh

- [ ] Update `wiki/production-systems/inventory-lookup-clearview.md` — Shop/RMF as first-class surface; refresh open-work (no ticket keys in public text)
- [ ] Update `wiki/initiatives/flsp-103-inventory-lookup.md` — add FLSP-856 epic row + topology links (or separate initiative if Cameron prefers)
- [ ] **Decision:** FLSP-856 as inline section on FLSP-103 page vs new `wiki/initiatives/flsp-856-pie-shop-replacement.md` — ask Cameron at Gate 1

### 2.3 Tier A — Shop/RMF (fat page)

`wiki/production-systems/clearview-shop-rmf-requests.md` should cover:

- Problem: PIE replacement, NetSuite Shop Request custom record
- Create/update/close flows from item status/location
- RMF tab, attachments, duplicate guard, request relationships
- NetSuite REST credential wiring (from commits)
- RBAC / role gates (FLSP-1206 if still open — mark ⚠️)
- Cameron intake metrics (user volume)
- Interview angles: custom record + REST + UX for warehouse ops

### 2.4 Tier A — VRA handoff

`wiki/production-systems/clearview-vra-handoff.md` — barcode-based Suitelet intake, PO path, Post Prod Validation status.

### 2.5 Tier A — Notifications

`wiki/production-systems/clearview-notifications.md` — subscription emails for comments/attachments; link to FLSP-862 evaluation story.

### 2.6 ADRs / decisions

- [ ] `wiki/decisions/clearview-shop-duplicate-guard.md`
- [ ] `wiki/decisions/clearview-rmf-attachment-rendering.md` (HEIC, sanitizer, server-side preview)
- [ ] `wiki/decisions/clearview-dev-role-admin-restrict.md` (FLSP-1190 invisible dev role)

### 2.7 July stale pages — delta pass

| Page | Action |
|------|--------|
| `clearview-mobile-ipad.md` | Refresh status from git/Jira |
| `clearview-ops-health.md` | Close or update parent Testing |
| `clearview-aws-hosting.md` | Any infra deltas |
| `zendesk-oauth-refresh-2026-10.md` | Oct deadline still open? |
| `digital-to-store-copilot.md` | Any movement on FLSP-247 |
| `interview-prep/system-design-clearview.md` | Add Shop/RMF + notification paths |

### 2.8 Interview prep refresh

- [ ] Update `wiki/interview-prep/system-design-clearview.md` with Shop/RMF data flow
- [ ] Add behavioral story stub for Shop/RMF delivery if Cameron confirms narrative

- [ ] **Gate 2 passed** — each cluster reviewed before next cluster starts

---

## Phase 3 — Git→Jira linkage methodology (for agents)

When writing any page, agents should build a **claim checklist**:

```
Claim → [commit hash(es)] → [Jira key(s)] → [Cameron intake?] → confidence
```

**Commit message patterns to parse:**

| Pattern | Maps to |
|---------|---------|
| `FLSP-NNN` prefix | Primary Jira link |
| `Merged in worktree-FLSP-NNN-* (pull request #N)` | PR + key |
| `feat(shop):`, `fix(rmf):` | Subsystem tag |
| `docs:`, `plan:` | ADR / open-question candidates |

**Do not** paste 500 commit subjects into wiki. **Do** cite representative PRs and decisions.

Optional helper script (repo-local, not committed to cameron-wiki unless Cameron asks):

`scripts/fls-git-jira-index.py` — reads frozen jsonl, outputs markdown index for `raw/`.

---

## Phase 4 — Career artifacts refresh

After wiki ingest (so dates align):

- [ ] Re-scrape Bitbucket → update `agent-tools/bitbucket-career-stats.json`
- [ ] Regenerate daily series → update `canvases/fls-contribution-graph.canvas.tsx`
- [ ] Update `canvases/fls-career-stats.canvas.tsx` headline stats
- [ ] Optional: `wiki/interview-prep/career-metrics-2026-09.md` (fls-internal, no keys) — Cameron decides

---

## Phase 5 — Lint & closeout

- [ ] Run wiki lint workflow (contradictions, orphans, missing pages, stale content)
- [ ] Fix 🔴 contradictions (July mobile backlog, ops-health, Build Phase scope)
- [ ] Append `wiki/log.md` catch-up complete entry
- [ ] Cameron review of `overview.md` strongest-areas paragraph

---

## Execution schedule (suggested sessions)

| Session | Work | Gate |
|---------|------|------|
| **S1** | Phase 0 freeze (git + Bitbucket + Jira + memory) | AUDIT_REPORT to Cameron |
| **S2** | Phase 1 cluster map + context intake | Gate 1 confirm |
| **S3** | Work-log + hub + initiative | Gate 2a |
| **S4** | Shop/RMF Tier A + ADRs | Gate 2b |
| **S5** | VRA + notifications + July stale pass | Gate 2c |
| **S6** | Interview prep + career canvases + lint | Done |

**Parallelization:** Phase 0 git mining per repo can run in parallel subagents. Phase 2 wiki writes are **sequential per cluster** (takeaway gates).

---

## Success criteria

- [ ] Wiki describes ClearView as of Sep 2026 including **Shop/RMF** (not just inventory search)
- [ ] Every Tier A claim traceable to frozen git or Jira extract
- [ ] Cameron intake metrics on at least Shop/RMF + ClearView adoption pages
- [ ] No silent overwrite of July contradictions
- [ ] Contribution graph + career stats current through 2026-09-02
- [ ] Public wiki pages remain ticket-key-free

---

## Locked decisions (Cameron, 2026-09-02)

1. **FLSP-856 initiative page** — **standalone** `wiki/initiatives/flsp-856-pie-shop-replacement.md` (not inline on FLSP-103)
2. **Ticket keys in wiki** — **keep scrubbed** on all committed wiki pages; keys live in `raw/` + private tracker only
3. **Priority** — **Shop/RMF first**; no major Zendesk / SellSmart / SofaScope pass (light stale checks only if AUDIT flags them)

### Still open at Gate 1 (non-blocking for Phase 0)

4. **Depth on orders UX (FLSP-949)** — fold into hub vs own page?
5. **Commit body mining** — full bodies in `raw/` only, or also mine PR descriptions from Bitbucket?

---

## Related artifacts

- Prior plan: `docs/superpowers/plans/2026-07-21-fls-jira-wiki-catchup.md`
- Last lookback: `wiki/work-log/2026-07-30-four-week-lookback.md`
- Career canvases: `canvases/fls-career-stats.canvas.tsx`, `canvases/fls-contribution-graph.canvas.tsx`
