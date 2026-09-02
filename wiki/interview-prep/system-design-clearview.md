---
title: System Design — ClearView (Hosted Inventory Lookup)
type: interview-note
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-07-21/flsp-103/project_flsp103_initiative_index.md
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp403_aws_hosting.md
  - raw/fls-work/clearview-memory/2026-07-21/project_shared_rds_dev_db.md
  - raw/fls-work/clearview-memory/2026-09-02/
  - raw/fls-work/git/2026-09-02/AUDIT_REPORT.md
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[initiatives/pie-shop-replacement.md]]"
  - "[[production-systems/clearview-shop-rmf-requests.md]]"
  - "[[production-systems/clearview-notifications.md]]"
  - "[[production-systems/clearview-vra-handoff.md]]"
  - "[[production-systems/clearview-aws-hosting.md]]"
  - "[[production-systems/clearview-rds-delta-sync.md]]"
  - "[[integrations/clearview-entra-sso.md]]"
  - "[[integrations/fls-aws-topology.md]]"
  - "[[production-systems/approach-reporting.md]]"
  - "[[decisions/authjs-v5-authorized-callback.md]]"
  - "[[decisions/clearview-approach-export-scope.md]]"
  - "[[decisions/clearview-shop-live-netsuite-read.md]]"
  - "[[decisions/clearview-shop-duplicate-guard.md]]"
  - "[[decisions/clearview-rmf-attachment-rendering.md]]"
  - "[[decisions/clearview-dev-role-admin-restrict.md]]"
  - "[[interview-prep/behavioral-fls-delivery.md]]"
  - "[[interview-prep/system-design-visual-search.md]]"
created: 2026-07-21
updated: 2026-09-02
confidence: high
tags: [interview, system-design, clearview, aws, rds, entra, netsuite, next.js, shop, rmf]
---

# System Design — ClearView (Hosted Inventory Lookup)

Interview preparation grounded in real ClearView production work at Furnitureland South. Hub page: [[production-systems/inventory-lookup-clearview.md]]. Initiative: [[initiatives/flsp-103-inventory-lookup.md]] · Shop/RMF: [[initiatives/pie-shop-replacement.md]].

**Visibility:** fls-internal — sanitize before public resume/portfolio use (see sanitized bullet at bottom).

## The story (behavioral framing)

"I own Furnitureland South's ClearView product — a Next.js app that replaced a NetSuite suitelet for floor staff and is now the ops UI for Shop/RMF (PIE replacement). We host on ECS/Fargate behind internal + public ALBs, sync full ~23-year inventory history into Postgres RDS via SuiteQL delta lanes, gate pricing with Microsoft Entra SSO, and ship Approach-style CSV/XLSX export. For shop ops we keep NetSuite as live system of record (no RDS lag on the queue), write a transitional iSeries sync until Blue Yonder owns create, archive closed comment history to Oracle NSAW, and layer department view/create RBAC behind a rollout flag."

## Architecture sketch (talking points)

```
Floor / shop staff
    → ALB (internal + public/WAF)
        → ECS Fargate (clearview-staging / clearview-prod)
            → Next.js App Router
                ← Entra SSO (Auth.js v5) + session roles / RBAC
                ← Postgres RDS  (browse / detail / orders read plane)
                ← Live SuiteTalk  (Shop/RMF queue + write-back)
On-prem task server
    → multi-lane delta sync → RDS
    → transitional Shop sync (iSeries → NetSuite) + optional NSAW archive
Bitbucket OIDC → ECR digest promote (auto staging / manual prod)
```

Deep pages: [[production-systems/clearview-aws-hosting.md]] · [[production-systems/clearview-rds-delta-sync.md]] · [[production-systems/clearview-shop-rmf-requests.md]] · [[integrations/clearview-entra-sso.md]] · [[decisions/clearview-shop-live-netsuite-read.md]]

## Key technical talking points

### 1. Two freshness SLAs in one product
Catalog/history tolerate ~15 min RDS lag. Shop/RMF does **not** — live NetSuite reads for the operational queue ([[decisions/clearview-shop-live-netsuite-read.md]]). Same app, intentional split.

### 2. Hosting choices that matter in interviews
- Estate's first internal ALB; later public ALB + WAF + Cloudflare CNAMEs
- Single ECR + digest promotion; manual prod gate
- Sync + migrations stay on-prem task server (not in-cluster)
- Cost: keep incremental hosting vs total steady-state distinct

### 3. Auth / RBAC evolution
Entra OIDC via Auth.js v5; pricing/export gates; Shop pilot `canAccessShop` plus department **view vs create** tiers; Zendesk stays on the stricter gate (PII). Feature-flagged department rollout. Middleware must check `req.auth` explicitly — [[decisions/authjs-v5-authorized-callback.md]].

### 4. Shop/RMF as PIE replacement
One custom record, two surfaces (Shop + RMF filter/nav). Duplicate open-request guard. Attachments rendered server-side (HEIC/docs/email) with XSS-hardened sanitizer. Closed comments in NSAW, not 2M NetSuite notes. Notifications: SES subscribe + sync-path notify (SMTP PLACEHOLDER lesson).

### 5. Knowing what not to build
Shop sub-location: closed as WMS/Blue Yonder–owned; typed web edit is a claim, not a scan. Avoid a ClearView-only field that drifts from Items page truth.

### 6. Approach export scope discipline
CSV/XLSX + shared RBAC; defer PDF + multi-pivot — [[decisions/clearview-approach-export-scope.md]].

### 7. Ops incidents as design feedback
- Staging crash-loop from RDS password / SSM drift → secrets + Terraform `ignore_changes` discipline
- NSAW archive resume on barcode max missed 13 days of closures → watermark on last_change_date
- SMTP PLACEHOLDER + dual-block env → length-check + SES-anchored extract
- ECS rolling promote ChunkLoadError window is normal mid-rollout

## Follow-up questions to anticipate

**"Why not query NetSuite live for everything?"**
→ Latency and SuiteQL concurrency on floor browse; RDS absorbs catalog/history. Shop queue is the exception where lag breaks ops.

**"How do you keep RDS fresh?"**
→ Multi-lane SuiteQL delta sync with watermarks from on-prem runners; hang class = unguarded network calls.

**"How would you cut over from PIE?"**
→ NetSuite SoR + transitional iSeries write sync; retire sync when BY/WMS creates/closes; NSAW for closed history; dual-run metrics still TBD.

**"What would you do differently?"**
→ Treat discovery docs as close criteria early. Profile auth middleware wrapping before staging sign-off. Populate real secrets before ECS task roll. Feature-flag department RBAC from day one of permission design.

**"Public vs internal tradeoffs?"**
→ Public path exists with WAF + Entra; pricing and PII still role-gated.

## Resume bullet (sanitized)

> Designed and shipped an internal/public Next.js inventory + shop-ops app on ECS/Fargate with Entra SSO, Postgres RDS read plane synced from ERP, live NetSuite custom-record Shop/RMF workflows, role-gated export, and SES subscription notifications — staging and production live for floor and shop staff

## Pair with

Behavioral delivery stories: [[interview-prep/behavioral-fls-delivery.md]]. Contrast ML-serving design: [[interview-prep/system-design-visual-search.md]].
