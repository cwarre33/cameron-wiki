---
title: ClearView Microsoft Clarity Telemetry
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-30/
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[production-systems/clearview-aws-hosting.md]]"
  - "[[work-log/2026-07-30-four-week-lookback.md]]"
created: 2026-07-30
updated: 2026-07-30
confidence: high
tags: [clearview, clarity, telemetry, uat, furnitureland-south]
---

# ClearView Microsoft Clarity Telemetry

Microsoft Clarity on ClearView **prod** for UAT session telemetry — script load, custom events, email/role session tags.

**Status:** Done (2026-07-29)  
**Parent hub:** [[production-systems/inventory-lookup-clearview.md]]

## Work items

| Summary | Status |
|---------|--------|
| Create Clarity project + load script on prod | Done (PR #78; `terraform apply` required for env var) |
| Verify sessions / share with stakeholders | Done (dashboard sharing is Clarity UI) |
| Custom Clarity events for key actions | Done |
| Tag sessions with email and role | Done (anonymous role-leak fixed pre-merge) |

## Ops lesson

**Terraform apply is manual.** CI formats/validates `infra/**` but does not apply. Merged + promoted app deploys do **not** load new ECS env vars until someone runs `terraform apply` in `infra/envs/<env>` (confirmed when Clarity script was absent until prod apply, task-def 3→4).

## Interview angle

Product analytics wired with privacy-conscious session tagging; infra/app deploy split as an operational control surface.
