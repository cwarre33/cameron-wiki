---
title: NetSuite → Zendesk Customer Sync (Task Server)
type: integration
status: planned
visibility: fls-internal
sources: [jira:FLSM-20]
related: [[production-systems/dedicated-agent-assignment.md]], [[work-log/2026-05-period-summary.md]]
created: 2026-05-20
updated: 2026-05-20
confidence: high
tags: [netsuite, zendesk, smartconnect, task-server, integration, sync]
---

# NetSuite → Zendesk Customer Sync (Task Server)

Spec for replacing SmartConnect **"NS CUSTOMER TO ZENDESK USERS"** with a Task Server job, standardizing alongside existing vendor sync, case creation, and comment processing.

**Jira:** [FLSM-20 Replace SmartConnect Customer Sync](https://furniturelandsouth.atlassian.net/browse/FLSM-20) (Backlog, spec authored 2026-05-20)

## Objective

- Reduce SmartConnect dependency
- Single integration pattern for all syncs
- Improved maintainability and processing visibility

## Job design

**Job type:** `netsuite.customer.sync.zendesk.users`

**Source:** NetSuite Customers (saved search 6091 equivalent), grouped by `internalId`

**Target:** Zendesk Users API (create/update)

## ID mapping (critical)

| System | Field | Role |
|--------|-------|------|
| NetSuite | `internalId` | Source primary key |
| Zendesk | `external_id` | Upsert match key |
| NetSuite | `custentity_zendesk_user_id_eone` | Writeback target for Zendesk `id` |

**Rule:** Always upsert on `external_id`. Never match on email alone (duplicate risk).

## Field mapping (baseline from SmartConnect)

| Zendesk | NetSuite source |
|---------|-----------------|
| `external_id` | `internalId` |
| `email` | `email` |
| `name` | ORGNAME calc (companyName or first + last) |
| `phone` | PHONECALCULATION |
| `role` | ENDUSERTYPE constant |
| `shared` | TRUE |
| `suspended` | FALSE |

**Custom user fields:** Shipping State, Historical Order Total (`custentity_fls_hist_ord_total_ns`), NetSuite Customer ID (`entityid`), Customer Portal Link (`custentity_customer_portal_link`)

## Upsert logic

1. Pull customers from NetSuite (consider incremental via `lastModifiedDate`)
2. Normalize name (person vs company), phone formatting, null-safe required fields
3. If Zendesk user exists (`external_id` match) → update; else → create
4. Write Zendesk `id` back to `custentity_zendesk_user_id_eone`
5. Per-record failure: log payload + error, retry via task server — do not block batch

## Edge cases to resolve

- **Missing emails:** Skip vs create-without-email (needs product decision)
- **Person vs company:** `isPerson`, `companyName`, `firstName`, `lastName` name construction
- **Performance:** Pagination + incremental sync for large customer base
- **Field drift:** Only sync required columns, avoid over-syncing SmartConnect legacy columns

## Out of scope (v1)

- Organization syncing
- Ticket linking changes
- Historical backfill optimization

## Acceptance criteria

- Task server job deployable
- Create + update via `external_id` working
- NetSuite writeback confirmed
- No duplicate users
- Logging with created/updated/failure counts
- Validated against SmartConnect preview sample

## Interview angles

- **Legacy migration:** Documenting SmartConnect config as executable spec before cutting over
- **Bidirectional ID linking:** External ID upsert + writeback enables future incremental sync
- **Integration standardization:** One task-server pattern reduces operational surface area
