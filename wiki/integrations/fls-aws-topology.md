---
title: FLS AWS Topology Conventions
type: integration
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/reference_fls_aws_topology.md
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[production-systems/clearview-aws-hosting.md]]"
  - "[[production-systems/clearview-rds-delta-sync.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [aws, fls, vpc, ecs, rds, alb, topology, furnitureland-south, clearview]
---

# FLS AWS Topology Conventions

House patterns for Furnitureland South's AWS estate — match these when designing new infra; do not invent parallel networks or auth styles.

**Used by ClearView:** [[production-systems/clearview-aws-hosting.md]], [[production-systems/clearview-rds-delta-sync.md]]

## Account & region

- Single primary account · default region **us-east-1**
- CLI login via wrapper (`aws login`, not vanilla `aws sso login`); sessions expire

## VPCs (parallel layout)

| VPC | CIDR pattern | Role |
|-----|--------------|------|
| FLS (prod) | `10.0.0.0/16` | Production public / data / build subnets across AZs; NAT present |
| FLS-STAGING | `10.3.0.0/16` | Staging mirror of same tier layout; NAT present |

Also: brand-specific and backup VPCs (out of ClearView scope). **Databases live in `*-data-subnet` tiers** (private).

## RDS conventions

| Pattern | House default |
|---------|---------------|
| Prod | Multi-AZ, private, encrypted |
| Staging | Single-AZ, private, encrypted |
| Engine (legacy) | SQL Server dominant historically |
| Auth | Username/password — **IAM DB auth off everywhere** |
| Proxy / Aurora | Not used |

ClearView introduced the estate's **first Postgres RDS**. ClearView as-built placed shared/dev DBs in the **prod VPC** because STAGING site-to-site VPN was down and peering is non-transitive — see [[production-systems/clearview-rds-delta-sync.md]].

## DB access security groups

Prefer CIDR allowlists (VPN + LAN ranges), not SG-referencing. Devs reach private DBs via FLS VPN/Direct Connect — **no bastion**. Do not copy legacy public `/32` exceptions.

## Compute

- **ECS Fargate microservices** behind shared ALBs (clusters for production, staging, AI product-finder, data services)
- New app = add ECS service + ALB target-group rule; reuse cluster/ALB/NAT
- No App Runner
- Common pattern elsewhere: Fargate in **public** subnets with public IP (avoid NAT data charges). ClearView internal-only tasks can use **data subnets** (NAT + VPN routes present)

## Load balancers & DNS

- Estate LBs historically internet-facing; ClearView added the **first internal ALB**
- ACM: issued `*.furniturelandsouth.com` wildcard — reuse for hostnames
- Corporate DNS: AD **split-horizon** for `furniturelandsouth.com` (VPN clients resolve internal CNAMEs → ALB). Route53 private zones unnecessary for on-prem users. External Cloudflare zone is separate.

## Secrets

Secrets Manager barely used for DBs — prefer **SSM Parameter Store** / ECS task-def secrets.

## Cost framing for new apps

Reuse shared ALB/NAT/cluster → incremental cost is mostly RDS + new internal ALB + Fargate tasks. ClearView hosting page tracks approved incremental vs total steady-state.
