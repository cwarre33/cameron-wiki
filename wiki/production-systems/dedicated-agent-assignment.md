---
title: Dedicated Agent Assignment — Zendesk CCS Automation
type: production-system
status: active
visibility: fls-internal
sources:
  - jira:FLSP-163
  - jira:FLSP-162
  - jira:FLSI-2965
  - jira:FLSI-2066
  - raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md
  - repo:Zendesk/DedicatedAgentAssignment
related:
  - "[[initiatives/zendesk-automation-platform.md]]"
  - "[[production-systems/crr-round-robin.md]]"
  - "[[integrations/netsuite-zendesk-customer-sync.md]]"
  - "[[work-log/2026-05-period-summary.md]]"
created: 2026-05-20
updated: 2026-07-30
confidence: high
tags: [zendesk, aws-lambda, ccs, automation, webhook, furnitureland-south]
---

# Dedicated Agent Assignment — Zendesk CCS Automation

Automatically assigns incoming **CCS** and **Vendor Care** tickets to the dedicated agent stored on the requester's user field (`dedicated_agent`), using AWS Lambda triggered by Zendesk webhooks — with CRR round-robin as fallback when empty.

⚠️ **Contradiction (resolved 2026-07-21):** May-2026 wiki listed dedicated-agent implementation as **Testing**. Live tracker shows **Done**.

**Status:** Dedicated-agent organization field + CRR logic **Done** · launch parent **Done** · post-launch follow-up **Ready for Deployment** · exclude supervisors from CCS dedicated-agent assignment **Post Prod Validation** · shared exclusion module **Done**.

**Repo:** `CleanDevEnvironment/Zendesk/ZendeskTools/DedicatedAgentAssignment/`

Umbrella: [[initiatives/zendesk-automation-platform.md]]. CRR: [[production-systems/crr-round-robin.md]].

## Late-July note — supervisor exclusion

Supervisors must be excluded from CCS dedicated-agent assignment in **both** the nightly sync path and CRR — shared exclusion module keeps the two paths consistent.

## Problem

Lookup-style dedicated-agent fields on Zendesk users cannot drive assignment actions purely from native triggers. The Lambda workaround reads the requester's field via API and assigns programmatically. CRR also consults the **organization** dedicated-agent field (FLSP-163).

## Flow

```
Ticket created in CCS/Vendor Care group
  → Zendesk trigger fires
  → Webhook → AWS Lambda
  → Lambda reads requester user_fields.dedicated_agent
  → If set: assign ticket, tag dedicated_agent_assigned, status Open (or Untouched per later rules)
  → If empty: tag ccs_rr_no_dedicated_agent, continue round-robin
```

## Components

| File | Purpose |
|------|---------|
| `lambda_function.mjs` | Node.js Lambda handler (primary) |
| `org_dedicated_agent_sync.py` | Library: org → user field propagation |
| `04_bulk_assign_ccs_agents.py` | Bulk set org `dedicated_agent` from CSV |
| `05_sync_org_dedicated_agent_to_users.py` | Reconcile org field → end-user fields |
| `AWS_LAMBDA_SETUP.md` / SAM templates | Deployment guide |

## Data model

- **Organization field:** `organization_fields.dedicated_agent` — set via bulk CSV / FLSP-162
- **User field:** `user_fields.dedicated_agent` — what Lambda reads at ticket time
- **Propagation:** `--propagate-to-users` on bulk script copies org value to all end-users in org
- Optional fallback env vars: `ORG_DEDICATED_AGENT_FALLBACK` when user field empty

## Post-launch (FLSI-2965)

Parent still **Ready for Deployment** (live 2026-07-21). Notable children:

| Key | Work | Status |
|-----|------|--------|
| FLSI-3007 | ALL customers export | Done |
| FLSI-3008 | Automate setting Dedicated Agent field | Done |
| FLSI-3058 | Dedicated Agent Nightly Sync | Done |
| FLSI-3048 | Dedicated Agent Backfill Repair | Done |
| FLSI-3011 | Tag Inactive Employees | Ready for Deployment |
| FLSI-3013 / FLSI-3018 | Round Robin Set Due Date (+ docs) | Done |
| FLSI-3009 / FLSI-3016 | Agent status 4:30 PM offline (+ docs) | Done |
| FLSI-3010 | Daily supervisor activity email | Done |

Intent from story: autopopulate dedicated agent from customers with open tickets; clear when all tickets closed (plus TBD follow-ons).

## Operations

- **Cost:** $0/year class load on AWS Free Tier (~100–200 invocations/month historically)
- **Rollback:** Deactivate Zendesk trigger → immediate revert to round-robin
- **Monitoring:** CloudWatch logs + `dedicated_agent_assigned` tag rate in Zendesk

## Deployment status (updated 2026-07-21)

- Organization field created (FLSP-162 **Done**)
- Org dedicated-agent logic in CRR (FLSP-163 **Done** — was incorrectly wiki-tagged Testing)
- Launch feature FLSI-2066 **Done**; Lambda + webhook + triggers in production path
- Post-launch FLSI-2965 still **Ready for Deployment** (nightly sync / backfill Done; inactive-employee tag pending deploy)

## Interview angles

- **Serverless integration pattern:** Webhook → Lambda → REST API upsert
- **Data propagation problem:** Org-level config must flow to user-level fields triggers/Lambda can read
- **Safe rollout:** Pilot org → metrics → expand; instant rollback via trigger deactivation
- **Status hygiene:** wiki “Testing” vs Jira “Done” — always re-check live Jira on catch-up
