---
title: ClearView Public ALB + WAF
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-30/
related:
  - "[[production-systems/clearview-aws-hosting.md]]"
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[integrations/clearview-entra-sso.md]]"
  - "[[integrations/fls-aws-topology.md]]"
  - "[[work-log/2026-07-30-four-week-lookback.md]]"
created: 2026-07-30
updated: 2026-07-30
confidence: high
tags: [clearview, aws, alb, waf, cloudflare, furnitureland-south]
---

# ClearView Public ALB + WAF

Make ClearView reachable on the **public internet** (still behind Entra ID), using a second internet-facing ALB + dedicated WAF — rather than remaining VPN/LAN-only behind the internal ALB.

**Status:** Done (2026-07-24 verified)  
**Parent:** [[production-systems/clearview-aws-hosting.md]]

## Why

Some on-site users could not reach the **internal** ALB (ping + TCP timeout to node IPs) despite campus presence. Team chose a public path over chasing the per-device network root cause. Entra SSO remains the auth gate.

## What shipped (2026-07-23 → 24)

- New Terraform modules: `infra/modules/waf` (AWS Common + Known-Bad-Inputs + SQLi managed rules + 2000 req/5 min per-IP rate limit) and `infra/modules/alb-public`
- ECS service supports **two** target groups (`internal` + `public`) via map/`for_each` with `moved` blocks to avoid destroy/recreate
- Applied `shared` → `staging` → `production`; both target groups healthy
- Cloudflare public CNAMEs (Mark): `clearview.furniturelandsouth.com` and `clearview-staging.furniturelandsouth.com` → public ALB
- Verified from public internet (desktop + phone): Entra sign-in HTTP 200

**PR:** #68 (`clearview-public-waf`)

## Cost

Estimated incremental **~$30–45/mo** for public ALB + dedicated WAF. Combined ClearView steady-state later measured ~**$159/mo** under ops health ([[production-systems/clearview-ops-health.md]]) — under prior budget expectations.

## Related CI detours (pre-existing on main)

- Bumped `next` for high-severity audit findings; Trivy HIGH findings on intentional public ALB + SSE-S3 log bucket suppressed with rationale in `.trivyignore`

## Contradiction

July 21 wiki framed ClearView hosting as **internal-only**. That framing is **superseded** for end-user access — internal ALB remains; public ALB is the internet path.
