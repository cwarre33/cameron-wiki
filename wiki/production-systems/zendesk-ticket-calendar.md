---
title: Zendesk Due Dates Calendar App
type: production-system
status: active
visibility: fls-internal
sources:
  - jira:FLSP-68
  - jira:FLSI-2881
  - raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md
  - repo:Zendesk/ZendeskTicketCalendar
related:
  - "[[initiatives/zendesk-automation-platform.md]]"
  - "[[production-systems/crr-round-robin.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [zendesk, zaf, calendar, due-dates, private-app, furnitureland-south]
---

# Zendesk Due Dates Calendar App

Private Zendesk Support app (ZAF) showing a calendar of the current agent's tickets by **Due Date** (Task tickets).

**Jira:** [FLSP-68](https://furniturelandsouth.atlassian.net/browse/FLSP-68) Due Dates Calendar App (Epic, **Done** live) · child [FLSI-2881](https://furniturelandsouth.atlassian.net/browse/FLSI-2881) Create App for Testing (**Done**).

**Repo:** `CleanDevEnvironment/Zendesk/ZendeskTools/ZendeskTicketCalendar/` · manifest version **1.5.8**, framework 2.0, `nav_bar` location, `private: true`.

Umbrella: [[initiatives/zendesk-automation-platform.md]].

## Behavior

- Calendar UI of tickets assigned to the **current user**
- Events driven by Zendesk system **Due Date** field
- Each event: Ticket ID, subject, due date; click opens the ticket
- Filters by specific **Ticket Status** IDs (e.g. On Hold, Awaiting Response) — not Status Category (avoids “Tasks Completed” leaking in)

## Deployment

- Built with Zendesk Apps Framework + ZCLI; package via `run.ps1 package` → upload ZIP from `tmp/`
- Install as **Private App**; restrict to **Testing** group first for leadership review before wider rollout
- Status IDs configured in `assets/iframe.html` as `INCLUDE_TICKET_STATUS_IDS` (from Admin Center status URL or `GET /api/v2/custom_statuses.json`)

## Acceptance (from epic)

- Loads for Testing-group users only during pilot restriction
- Calendar reflects due dates; links navigate correctly
- No production-wide visibility before approval

## Interview angles

- **ZAF private app + group restriction** as a safe rollout gate
- **Status vs status category** filtering pitfall for custom ticket statuses
