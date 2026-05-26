---
title: Dedicated Agent Assignment — Zendesk CCS Automation
type: production-system
status: active
visibility: fls-internal
sources: [jira:FLSP-163, jira:FLSP-162, repo:Zendesk/DedicatedAgentAssignment]
related: [[integrations/netsuite-zendesk-customer-sync.md]], [[work-log/2026-05-period-summary.md]]
created: 2026-05-20
updated: 2026-05-20
confidence: high
tags: [zendesk, aws-lambda, ccs, automation, webhook, furnitureland-south]
---

# Dedicated Agent Assignment — Zendesk CCS Automation

Automatically assigns incoming **CCS** and **Vendor Care** tickets to the dedicated agent stored on the requester's user field (`dedicated_agent`), using AWS Lambda triggered by Zendesk webhooks.

**Jira:** [FLSP-163 Implement Organization Dedicated Agent Logic in CRR](https://furniturelandsouth.atlassian.net/browse/FLSP-163) (Testing) · prerequisite [FLSP-162](https://furniturelandsouth.atlassian.net/browse/FLSP-162) (Done)

**Repo:** `CleanDevEnvironment/Zendesk/ZendeskTools/DedicatedAgentAssignment/`

## Problem

Lookup-style dedicated-agent fields on Zendesk users cannot drive assignment actions purely from native triggers. The Lambda workaround reads the requester's field via API and assigns programmatically.

## Flow

```
Ticket created in CCS/Vendor Care group
  → Zendesk trigger fires
  → Webhook → AWS Lambda
  → Lambda reads requester user_fields.dedicated_agent
  → If set: assign ticket, tag dedicated_agent_assigned, status Open
  → If empty: tag ccs_rr_no_dedicated_agent, continue round-robin
```

## Components

| File | Purpose |
|------|---------|
| `lambda_function.mjs` | Node.js Lambda handler (primary) |
| `org_dedicated_agent_sync.py` | Library: org → user field propagation |
| `04_bulk_assign_ccs_agents.py` | Bulk set org `dedicated_agent` from CSV |
| `05_sync_org_dedicated_agent_to_users.py` | Reconcile org field → end-user fields |
| `AWS_LAMBDA_SETUP.md` | Full deployment guide |

## Data model

- **Organization field:** `organization_fields.dedicated_agent` — set via bulk CSV
- **User field:** `user_fields.dedicated_agent` — what Lambda reads at ticket time
- **Propagation:** `--propagate-to-users` on bulk script copies org value to all end-users in org

Optional fallback env vars: `ORG_DEDICATED_AGENT_FALLBACK` when user field empty.

## Operations

- **Cost:** $0/year (AWS Free Tier — ~100–200 invocations/month)
- **Rollback:** Deactivate Zendesk trigger → immediate revert to round-robin
- **Monitoring:** CloudWatch logs + `dedicated_agent_assigned` tag rate in Zendesk

## Deployment status (May 2026)

- Organization field created (FLSP-162 Done)
- Lambda + webhook infrastructure documented
- Testing phase — pilot org validation before full CCS rollout
- Local scripts updated May 2026 (`lambda_function.mjs`, sync utilities)

## Interview angles

- **Serverless integration pattern:** Webhook → Lambda → REST API upsert
- **Data propagation problem:** Org-level config must flow to user-level fields triggers can read
- **Safe rollout:** Pilot org → metrics week → expand; instant rollback via trigger deactivation
