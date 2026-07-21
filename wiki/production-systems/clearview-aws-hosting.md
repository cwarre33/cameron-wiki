---
title: ClearView AWS Hosting (FLSP-403)
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp403_aws_hosting.md
  - raw/fls-work/clearview-memory/2026-07-21/reference_fls_aws_topology.md
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp383_build_phase.md
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[integrations/fls-aws-topology.md]]"
  - "[[integrations/clearview-entra-sso.md]]"
  - "[[production-systems/clearview-rds-delta-sync.md]]"
  - "[[decisions/authjs-v5-authorized-callback.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [clearview, aws, ecs, fargate, alb, rds, cicd, flsp-403, furnitureland-south]
---

# ClearView AWS Hosting (FLSP-403)

ECS/Fargate hosting for ClearView behind a shared ALB — staging + prod — under Build Phase epic [[initiatives/flsp-103-inventory-lookup.md]].

**Parent hub:** [[production-systems/inventory-lookup-clearview.md]]  
**Jira:** [FLSP-403](https://furniturelandsouth.atlassian.net/browse/FLSP-403) **Testing** (as of 2026-07-21)

## Purpose

Ship ClearView as an internal-only hosted app (VPN/LAN), not SuiteTalk-in-browser alone: containerized Next.js on Fargate, private Postgres RDS, Entra SSO via SSM secrets, Bitbucket OIDC deploy.

## Architecture

| Piece | Choice |
|-------|--------|
| Compute | ECS Fargate services `clearview-staging` / `clearview-prod` (1/1 steady) |
| Ingress | Shared FLS ALB + **estate's first internal ALB** (~$23/mo); listener priority 200 for prod |
| Images | Single ECR repo; digest promotion (`staging-<sha>` → `prod-latest` / `prod-<sha>`) |
| Data | Multi-AZ `db.t4g.small` prod RDS; staging RDS seeded from same lineage — see [[production-systems/clearview-rds-delta-sync.md]] |
| Secrets | SSM Parameter Store (Entra ID/secret/issuer; RDS passwords); Terraform `ignore_changes` on secret values |
| Auth | Entra SSO — [[integrations/clearview-entra-sso.md]] |
| CI/CD | Bitbucket: `verify:ci` → build/push → **auto staging** → **manual** prod promote (OIDC role `fls-inventory-lookup-bitbucket-deploy`) |
| Sync | On-prem task server (not in-cluster) — multi-target delta |

House conventions: [[integrations/fls-aws-topology.md]]. Tasks in data subnets; internal-only access model.

## Locked decisions (do not re-litigate)

- Internal-only (no public internet app surface)
- Sync + migrations stay on-prem task server
- Dev RDS outside Terraform
- Single ECR + digest promotion
- Bitbucket required-approvers is Premium — prod gate is the **manual promote** step (advisory posture, same as FLSP-474)

## Cost

- **Incremental** hosting ~$141/mo (approved 2026-07-13)
- **Total steady-state** ~$171/mo including pre-existing ~$30/mo dev RDS

Keep incremental vs total distinct when discussing spend.

## Status (2026-07-21)

| Item | State |
|------|-------|
| Staging | LIVE — ALB healthy; Entra browser-verified after auth-gate fix |
| Prod | LIVE 2026-07-16 — seeded (~1.96M txns / 11.5M lines); Entra curl/browser verified |
| DNS | CNAMEs live: `clearview` / `clearview-staging` → internal ALB (AD split-horizon; VPN/LAN). External Cloudflare zone is separate — do not conflate |
| Pipeline | Green after YAML-anchor lesson (PR #49); never fold multi-line YAML anchors in Bitbucket `script:` blocks |

**Parent stays Testing** until a final **no-hosts-file** browser check confirms DNS without local overrides.

## Open work

| Key | Notes |
|-----|-------|
| [FLSP-412](https://furniturelandsouth.atlassian.net/browse/FLSP-412) | ECS Auto Scaling — In Progress |
| [FLSP-728](https://furniturelandsouth.atlassian.net/browse/FLSP-728) | Post-launch hardening (load test done; facets cache; staging sync confirmation; RDS RI eval deferred) |
| FLSP-411 | Alarms — deferred standalone |
| Hosts-file cleanup | Admin PowerShell removal of workaround entries |

## Related incidents

- Auth gating regression on wrap of Auth.js middleware — [[decisions/authjs-v5-authorized-callback.md]]
- Staging crash-loop (FLSP-781): RDS password / SSM drift — Done
