---
title: System Design — ClearView (Hosted Inventory Lookup)
type: interview-note
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-07-21/flsp-103/project_flsp103_initiative_index.md
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp403_aws_hosting.md
  - raw/fls-work/clearview-memory/2026-07-21/project_shared_rds_dev_db.md
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[production-systems/clearview-aws-hosting.md]]"
  - "[[production-systems/clearview-rds-delta-sync.md]]"
  - "[[integrations/clearview-entra-sso.md]]"
  - "[[integrations/fls-aws-topology.md]]"
  - "[[production-systems/approach-reporting.md]]"
  - "[[decisions/authjs-v5-authorized-callback.md]]"
  - "[[decisions/clearview-approach-export-scope.md]]"
  - "[[interview-prep/behavioral-fls-delivery.md]]"
  - "[[interview-prep/system-design-visual-search.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [interview, system-design, clearview, aws, rds, entra, netsuite, next.js]
---

# System Design — ClearView (Hosted Inventory Lookup)

Interview preparation grounded in real ClearView production work at Furnitureland South. Hub page: [[production-systems/inventory-lookup-clearview.md]]. Initiative: [[initiatives/flsp-103-inventory-lookup.md]].

**Visibility:** fls-internal — sanitize before public resume/portfolio use (see sanitized bullet at bottom).

## The story (behavioral framing)

"I own Furnitureland South's ClearView inventory product — a Next.js app that replaced a NetSuite suitelet for floor staff. We host it on ECS/Fargate behind an internal ALB, sync full ~23-year inventory history into Postgres RDS via SuiteQL delta lanes, gate pricing with Microsoft Entra SSO (Auth.js v5), and ship Approach-style CSV/XLSX export with role-gated columns. Staging and prod are live; I'm still driving post-launch hardening and open bugs."

## Architecture sketch (talking points)

```
Floor staff (VPN/LAN)
    → Internal ALB
        → ECS Fargate (clearview-staging / clearview-prod)
            → Next.js App Router
                ← Entra SSO (Auth.js v5) + session roles / RBAC
                ← Postgres RDS read plane (~5GB, full history)
            ← SuiteTalk / SuiteQL (live NetSuite for some paths)
On-prem task server → multi-lane delta sync → RDS
Bitbucket OIDC → ECR digest promote (auto staging / manual prod)
```

Deep pages: [[production-systems/clearview-aws-hosting.md]] · [[production-systems/clearview-rds-delta-sync.md]] · [[integrations/clearview-entra-sso.md]] · [[integrations/fls-aws-topology.md]] · [[production-systems/approach-reporting.md]]

## Key technical talking points

### 1. Read plane vs source of truth
NetSuite remains SoT; RDS is the browse/detail/orders read plane. Don't live-SuiteQL every grid. Full-scale parity (~23 years) superseded an earlier windowed pilot — [[production-systems/clearview-rds-delta-sync.md]], [[production-systems/pilot-database-migration.md]].

### 2. Hosting choices that matter in interviews
- Internal-only (no public app surface); estate's first internal ALB
- Single ECR + digest promotion; manual prod gate (Bitbucket Premium approvers unavailable)
- Sync + migrations stay on-prem task server (not in-cluster)
- Incremental hosting ~$141/mo vs total steady-state ~$171/mo — keep distinct when discussing cost

### 3. Auth / RBAC
Entra OIDC via Auth.js v5; session roles gate wholesale/cost/MSRP and export columns. Middleware must check `req.auth` explicitly when wrapping `auth((req) => …)` — regression ADR [[decisions/authjs-v5-authorized-callback.md]].

### 4. Approach export scope discipline
Ship CSV/XLSX + shared RBAC; explicitly defer PDF + multi-pivot templates after verifying discovery docs — [[decisions/clearview-approach-export-scope.md]], [[methodology/verify-against-source-docs.md]].

### 5. Ops incidents as design feedback
- FLSP-781: staging crash-loop from RDS password / SSM drift → secrets + Terraform `ignore_changes` discipline
- FLSP-784: Akeneo images 503 + missing sign-in video → asset/SSM path still open

## Follow-up questions to anticipate

**"Why not query NetSuite live for everything?"**
→ Latency and SuiteQL concurrency on floor browse; RDS absorbs catalog/history traffic; delta lanes close freshness. Live SuiteTalk remains for paths that need SoT immediacy.

**"How do you keep RDS fresh?"**
→ Multi-lane SuiteQL delta sync with watermarks from on-prem runners; fixed wedged txn lane (FLSP-547) and non-serial parity (FLSP-548). Technique pages: [[techniques/rds-delta-sync-watermarks.md]], [[techniques/vmpn-serial-snapshot.md]].

**"How would you scale?"**
→ ECS Auto Scaling (FLSP-412 In Progress); facets/cache hardening (FLSP-728); evaluate RDS RI later; discuss read replicas if browse load grows.

**"What would you do differently?"**
→ Treat discovery docs as the close criteria from day one on Approach parity. Profile auth middleware wrapping before staging "works in browser" sign-off. Keep SSM secret drift runbooks next to Terraform from the first hosting PR.

**"Public vs internal tradeoffs?"**
→ Inventory + pricing are internal-only by design; VPN/LAN + Entra beats public internet + WAF complexity for this workforce.

## Resume bullet (sanitized)

> Designed and shipped an internal Next.js inventory app on ECS/Fargate with Entra SSO, Postgres RDS read plane synced from ERP via scheduled SuiteQL deltas, and role-gated CSV/XLSX export — staging and production live for floor staff

## Pair with

Behavioral delivery stories (stakeholders, incidents, Zendesk): [[interview-prep/behavioral-fls-delivery.md]]. Contrast ML-serving design: [[interview-prep/system-design-visual-search.md]].
