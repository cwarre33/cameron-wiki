---
title: ClearView Shop Notifications
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-09-02/flsp-856-story-descriptions.md
  - raw/fls-work/clearview-memory/2026-09-02/project_flsp1169_subscribers_field.md
  - raw/fls-work/clearview-memory/2026-09-02/project_flsp1187_sync_change_notifications.md
  - raw/fls-work/clearview-memory/2026-09-02/project_flsp1207_subscribe_confirmation.md
  - raw/fls-work/inventory-lookup-docs/2026-09-02/
  - raw/fls-work/git/2026-09-02/inventory-lookup/adr-signals.json
related:
  - "[[production-systems/clearview-shop-rmf-requests.md]]"
  - "[[initiatives/pie-shop-replacement.md]]"
  - "[[work-log/2026-08-09-clearview-shop-rmf-sprint.md]]"
created: 2026-09-02
updated: 2026-09-02
confidence: high
tags: [clearview, shop, notifications, email, ses, furnitureland-south]
---

# ClearView Shop Notifications

Subscription email notifications for Shop/RMF request activity — ClearView-originated comments/attachments first, then sync-driven changes from the transitional iSeries → NetSuite writer.

**Parent evaluation story:** still In Progress (PIE follow-up / Notify Me / task-lite needs). **Subscription emails:** Done and live-verified. **Sync-change notify:** Done and live-verified (SMTP fixed 2026-09-02; Cameron confirmed sync-triggered email landed and working).

## What shipped

- NetSuite field: subscriber email JSON list on the Shop Request custom record (SB1 + production)
- Subscribe / unsubscribe from request detail Actions menu (Shop + RMF routes)
- SES send via nodemailer; actor excluded from their own notification (app path)
- Post-demo UX: banner + bell subscribe confirmation
- Never-throws notify path — failed SMTP logs; request POST still succeeds
- Sync path: `notifySyncedShopRequestChange` built from per-target sync diff (does **not** re-fetch via the wrong account flag); null actor → notify all subscribers

## Deliberate early gap (found in prod)

Legacy iSeries → Shop sync wrote comments **without** calling the app notify path. Subscribers only got mail for ClearView POSTs. Confirmed via records with all-caps iSeries authors + zero CloudWatch notify lines. Follow-up story wired sync diffs into notify.

## Ops: SMTP was the real outage (2026-09-02)

After sync-notify code merged, still no mail — root cause was credentials, not code:

- Terraform seeded SSM SMTP params as literal `PLACEHOLDER` with `ignore_changes`
- Task-server `.env.local` lacked real values
- `ja-utility-shed` has **two** SMTP blocks (Outlook + SES); naive first-match / PowerShell array-join produced wrong concatenated secrets
- Fix: take the SES pair **after** `SMTP_HOST=email-smtp…`; SSM path segment is `prod` not `production`
- Live smoke: direct `sendEmail()` delivered to Cameron — SES path confirmed
- **Sync-triggered email confirmed working** (Cameron, 2026-09-02) after ECS/task-server picked up fixed values

## Decisions

- **Shared To: header (not Bcc)** — Cameron: OK for internal FLS employees; seeing other subscribers is useful context
- Subscribe stays on stricter Shop access gate (not widened view-only roles) until a later ticket

## Ops / CI notes

- Use the SES SMTP credential set in utility-shed env (not the Outlook pair)
- nodemailer peer vs advisory: pin ^8 + allowlist unreachable `raw` option in audit + Trivy gates
- Audit CI must **fail closed** when npm audit JSON lacks a `vulnerabilities` key

## Open

- Legacy reconciliation field sync (related backfill deferred for prod)
- Full "lightweight task management" decision from the evaluation story
