---
title: ClearView AWS Hosting
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/
  - raw/fls-work/clearview-memory/2026-07-30/
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[integrations/fls-aws-topology.md]]"
  - "[[integrations/clearview-entra-sso.md]]"
  - "[[production-systems/clearview-rds-delta-sync.md]]"
  - "[[production-systems/clearview-public-alb-waf.md]]"
  - "[[production-systems/clearview-ops-health.md]]"
  - "[[decisions/authjs-v5-authorized-callback.md]]"
  - "[[work-log/2026-07-30-four-week-lookback.md]]"
created: 2026-07-21
updated: 2026-07-30
confidence: high
tags: [clearview, aws, ecs, fargate, alb, rds, cicd, furnitureland-south]
---

# ClearView AWS Hosting

ECS/Fargate hosting for ClearView — staging + prod — under Build Phase epic [[initiatives/flsp-103-inventory-lookup.md]].

**Parent hub:** [[production-systems/inventory-lookup-clearview.md]]  
**Status:** **Post Prod Validation** (as of 2026-07-24)

## Purpose

Ship ClearView as a hosted Next.js app on Fargate with private Postgres RDS, Entra SSO via SSM secrets, and Bitbucket OIDC deploy. Originally **internal-ALB only**; late July added a **public ALB + WAF** path ([[production-systems/clearview-public-alb-waf.md]]) while keeping Entra as the auth gate.

## Architecture

| Piece | Choice |
|-------|--------|
| Compute | ECS Fargate `clearview-staging` / `clearview-prod` |
| Ingress | Internal ALB **+** public ALB; host-header routing |
| Images | Single ECR; digest promotion staging → prod |
| Data | Multi-AZ `db.t4g.small` prod RDS; staging seeded from same lineage — [[production-systems/clearview-rds-delta-sync.md]] |
| Secrets | SSM Parameter Store; Terraform `ignore_changes` on secret values; **manual `terraform apply`** after infra merge |
| Auth | Entra SSO — [[integrations/clearview-entra-sso.md]] |
| CI/CD | Bitbucket: `verify:ci` → build/push → auto staging → **manual** prod promote |
| Sync | On-prem task server (not in-cluster) — multi-target delta |

House conventions: [[integrations/fls-aws-topology.md]].

## Contradiction — access model

| Claim | When | Status |
|-------|------|--------|
| Internal-only (no public internet app surface) | July 21 wiki / early hosting story | **Superseded** by public ALB + WAF; Entra still required |
| Sync + migrations on-prem task server | Ongoing | Still true |
| Single ECR + digest promotion | Ongoing | Still true |
| Prod gate = manual Bitbucket promote | Ongoing | Still true |

## Cost

- Early estimate: incremental ~$141/mo; total ~$171/mo incl. dev RDS
- Late-July ops health: **~$159/mo** steady-state (under prior ~$201–216 with public add-on) — [[production-systems/clearview-ops-health.md]]

## Status (2026-07-30)

| Item | State |
|------|-------|
| Staging / prod ECS | LIVE |
| DNS | Internal CNAMEs + public Cloudflare CNAMEs (`clearview` / `clearview-staging`) |
| Parent story | **Post Prod Validation** |
| Public path | Done — [[production-systems/clearview-public-alb-waf.md]] |

## Open work

| Item | Notes |
|------|-------|
| ECS Auto Scaling | In Progress |
| Post-launch hardening | In Progress |
| Ops health parent | Still Testing; sub-tasks Done — [[production-systems/clearview-ops-health.md]] |

## Related incidents

- Auth gating regression — [[decisions/authjs-v5-authorized-callback.md]]
- Staging crash-loop (RDS password / SSM drift) — Done
