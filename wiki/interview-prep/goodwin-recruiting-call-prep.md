---
title: Goodwin Recruiting — Backend Engineer Call Prep
type: interview-note
status: active
visibility: private
sources: [raw/job-search/goodwin-recruiting-backend-engineer-2026-07-11.md]
related: [[production-systems/inventory-lookup-clearview.md]], [[production-systems/sofascope.md]], [[production-systems/sellsmart-copilot.md]], [[production-systems/pilot-database-migration.md]], [[decisions/disclosure-communication-humanization.md]]
created: 2026-07-11
updated: 2026-07-11
confidence: medium
tags: [job-search, interview-prep, backend-engineer, goodwin-recruiting, llm, recruiting-tech]
---

# Goodwin Recruiting — Backend Engineer Call Prep

Inbound outreach from "Hunter," a virtual recruiter at Goodwin Recruiting, for a remote **Backend Engineer** role building LLM-powered recruiting automation (prompt-engineered pipelines, email/calendar/ATS integrations, reliability/security-focused backend). Full JD and email in [[raw/job-search/goodwin-recruiting-backend-engineer-2026-07-11.md]].

## Legitimacy assessment

**Verdict: likely legitimate, worth taking the call.** No fee requests, no bank/SSN ask, no wire/crypto pressure — the classic job-scam-for-money markers are absent. Goodwin Recruiting is a real, established agency (hospitality-founded, Forbes recruiting-firm recognition), and the JD is too technically specific (async Python, idempotency, per-firm data isolation, OAuth/webhooks, MCP, SOC 2/ISO 27001) to be a generic phishing template — reads like a genuine client spec funneled through a third-party recruiter.

**Before/at the start of the call:**
- Confirm sender domain matches `goodwinrecruiting.com` (not a lookalike).
- Ask directly who the actual hiring company is — Goodwin is the staffing agency, not necessarily the employer.
- Ask whether "virtual recruiter" means a live person or an automated intake bot.
- Do not give SSN, bank details, or pay anything — not needed for an intake call.

## Role fit — why this maps to Cameron's background

| JD requirement | Cameron's evidence |
|---|---|
| LLM pipelines, heavy prompt engineering, eval of non-deterministic systems | [[production-systems/sofascope.md]] (CLIP+FAISS hybrid search), [[production-systems/sellsmart-copilot.md]] (Copilot Studio prompt/tool design) |
| Python backend: API design, data modeling, async, Postgres | [[production-systems/inventory-lookup-clearview.md]] (SuiteQL/SuiteTalk API surface), [[production-systems/pilot-database-migration.md]] (Postgres ETL, entity mapping) |
| Reliability & data security: queuing, retries, idempotency, per-tenant isolation, review-before-send | [[production-systems/inventory-lookup-clearview.md]] scale/security profile (Entra ID gating, internal-network-only exposure); [[decisions/disclosure-communication-humanization.md]] for careful, review-gated external communication |
| Integrations: OAuth, webhooks, proprietary APIs, MCP | ClearView's NetSuite OAuth 2.0 JWT (PS256) integration pattern; SellSmart's NetSuite REST tool for Copilot Studio; this very session is MCP-based tooling |
| Previous work integrating calendar/email/CRM/ATS/TRM platforms | ClearView reframed as **CRM foundation over NetSuite ERP** — serial-level customer/product lifecycle tracking (see below) |
| Data modeling / ER experience | ClearView + pilot migration entity mapping (Customer → Accounts/contacts, Transaction → line items, dual NetSuite/app IDs) |

## Headline story: ClearView as a CRM foundation

Lead with this instead of "it's a barcode lookup tool":

> "I built and operate the backend for a system that's effectively the customer/product-relationship layer sitting on top of our NetSuite ERP. Every one of ~1.3 million tracked serial numbers across 200,000+ distinct products carries its full lifecycle — receipts, sales orders, returns, transfers, service activity — and that's synced out of NetSuite every 15 minutes so the app can serve high-volume lookups fast and cheap instead of hitting SuiteQL live on every request. It's hosted on AWS, gated behind Microsoft Entra ID, and deliberately kept off the public internet — internal network only. That's the same shape of problem as this role: high-reliability sync, per-record data isolation, and integrations against a proprietary system of record."

This directly answers "previous work integrating with calendar/email/CRM/ATS/TRM platforms" and "per-firm data isolation" — NetSuite is FLS's ERP of record, and ClearView's serial-tracking is the CRM-equivalent relationship layer over it.

## Questions to ask them

- Who is the actual end client (name of the company/product, not just Goodwin as the agency)?
- Stage/size: funded startup vs. bootstrapped, team size, how many engineers on backend?
- What does "prompt engineering across a wide variety of recruiter use cases" look like operationally — is there an eval harness, or is quality judged ad hoc?
- What's the actual comp number, not just "six figure"? Equity: what stage/vesting?
- What's the current architecture for the "review-before-send approval flow" — human-in-the-loop UI, Slack approval, email confirm?

## Open items

- [ ] Confirm call happened and outcome
- [ ] Get actual employer name once revealed
- [ ] Decide whether to pursue past the intake call
