---
title: CRR — CCS/VCS Custom Round Robin
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md
  - raw/fls-work/jira/2026-07-21/cluster-map.md
  - jira:FLSI-2066
  - jira:FLSI-3032
  - jira:FLSM-33
  - repo:Zendesk/DedicatedAgentAssignment
related:
  - "[[initiatives/zendesk-automation-platform.md]]"
  - "[[production-systems/dedicated-agent-assignment.md]]"
  - "[[integrations/netsuite-zendesk-customer-sync.md]]"
created: 2026-07-21
updated: 2026-07-30
confidence: high
tags: [zendesk, crr, round-robin, ccs, vcs, task-server, furnitureland-south]
---

# CRR — CCS/VCS Custom Round Robin

**Custom Round Robin (CRR)** is the Task Server–backed ticket assignment stack for **CCS** and **VCS**, with dedicated-agent preference before fair-share fallback.

**Anchor status:** Custom Round Robin R&D **Done** · vendor RR toward daily cap **Done** · post-launch follow-up **Ready for Deployment** · exclude supervisors **Post Prod Validation** · shared exclusion module **Done**.

Umbrella: [[initiatives/zendesk-automation-platform.md]]. Dedicated-agent Lambda: [[production-systems/dedicated-agent-assignment.md]].

## Late-July — supervisor exclusion

Supervisors excluded from CCS dedicated-agent assignment in sync **and** CRR via a shared exclusion module so the two paths cannot drift.

## Assignment flow

```
Ticket enters CCS / VCS group
  → Prefer dedicated agent (org/user field) if set and eligible
  → Else CRR skill/capacity queue (ccs-skill-queue + custom RR)
  → Capacity / daily-cap rules gate who is eligible
  → agent-status jobs keep online/offline aligned with business hours
  → Fallback tags (e.g. ccs_rr_no_dedicated_agent) when no dedicated agent
```

**Dedicated-agent fallback:** if requester has no `dedicated_agent`, ticket continues through round-robin rather than stalling. Org-field logic in CRR landed via [FLSP-163](https://furniturelandsouth.atlassian.net/browse/FLSP-163) (**Done**).

## Capacity & business rules (synthesized)

| Concern | Evidence in Jira tree | Outcome |
|---------|----------------------|---------|
| Per-agent capacity | FLSI-2963 Denita Baker capacity rule | Done |
| After-hours pickup | FLSI-2964 automation outside business hours | Done |
| Untouched status | FLSI-2962 set ticket to ⚠️ Untouched | Done |
| VCS supervisor flag | FLSI-2982 “VCS Supervisor Review” checkbox | Done |
| Group rename | FLSI-2980 Client Relations → After Hours Chat | Done |
| Vendor tickets toward daily cap | FLSM-33 (+ FLSM-34 logs, FLSM-35 Huffman limit 30) | Done |
| Due date on RR assign | FLSI-3013 Round Robin Set Due Date | Done |

## Task Server jobs

Scheduled Node jobs (not native Zendesk RR alone) drive eligibility and presence:

| Job / artifact | Role | Jira |
|----------------|------|------|
| `ccs-skill-queue.js` | CCS skill queue scheduling | FLSI-2983 |
| `agent-status.js` | Auto set agents online / offline | FLSI-2985, FLSI-2986, FLSI-2987, FLSI-3009, FLSI-3016 |
| Custom RR research deploy | FLSI-3032 → task server schedule | FLSI-3035 |
| Dedicated agent nightly sync | Keep fields reconciled | FLSI-3058 |
| Supervisor activity email | Daily agent activity | FLSI-3010 |
| Logging on all tasks | Ops visibility | FLSI-3022 |

Related ops fix: [FLSP-138](https://furniturelandsouth.atlassian.net/browse/FLSP-138) retry logic for `Set Agents Online.bat` (**Done**).

Wait-time / webhook Lambda siblings live under `ZendeskWaitTimeServer/` (business-hours checker + webhook receiver) — adjacent to presence/routing, not the full CRR queue.

## Evolution

1. **FLSI-2066** — Dedicated agent field + RR fallback; triggers, Lambda, docs, mass field update.
2. **FLSI-3032** — Custom RR R&D across VCS/CCS/CI (outlines, native-logic map, chat/messaging investigation, dedicated-agent migration to prod).
3. **FLSI-2965 [POST LAUNCH]** — Autopopulate dedicated agent from open tickets, inactive-employee tagging, view cleanup, nightly sync, due-date automation. Parent still **Ready for Deployment**; most children Done, FLSI-3011 Tag Inactive Employees still Ready for Deployment.
4. **FLSM-33** — Vendor RR assignments count toward agent daily cap (maintenance follow-on).

## Interview angles

- **Preference then fairness:** dedicated agent when present; capacity-aware RR otherwise
- **Task Server as control plane:** presence + skill queue + custom RR scheduled outside Zendesk native limits
- **Safe post-launch backlog:** FLSI-2965 keeps production stable while residual deploy items stay explicit
