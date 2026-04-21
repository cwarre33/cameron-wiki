---
title: Security Disclosure Tracker - OSINT Credential Discoveries
date: 2026-04-21
status: active-tracker
updated: 2026-04-21
---

## 📊 DISCLOSURE SUMMARY

| Date | Total Found | Posted | Pending | Avg Response |
|------|-------------|--------|---------|---------------|
| Apr 20 | 5 | 4 | 1 | Awaiting |
| Apr 21 | 2 | 2 | 0 | Just posted |
| **Total** | **7** | **6** | **1** | - |

---

## 🔴 CRITICAL Findings (Priority)

### April 21, 2026 Hunt

#### #1: ettfemnio/dbd-server 🔥 **P1 - JUST POSTED**
- **Issue:** https://github.com/ettfemnio/dbd-server/issues/23
- **Status:** ✅ POSTED (Open)
- **Finding:** Production TLS private key in HTTPS server code
- **Risk:** Complete TLS compromise, MITM attacks, player data exposure
- **Impact:** 18 ⭐, hardcoded production key
- **Key Location:** `private/privatekey.key`
- **Code Location:** `src/server.ts:443`
- **Next Check:** Apr 28 (7 days) for maintainer response

#### #2: totaljs/superadmin 🔥 **P2 - JUST POSTED**
- **Issue:** https://github.com/totaljs/superadmin/issues/53
- **Status:** ✅ POSTED (Open)
- **Finding:** SSL private key with matching CSR for admin panel
- **Risk:** Admin impersonation, SSL forgery, server compromise
- **Impact:** 99 ⭐, 46 forks, ~100 deployments
- **Key Location:** `private/superadmin.key`
- **Code Location:** `definitions/superadmin.js`, `tasks/nginx.js`
- **Next Check:** Apr 28 (7 days) for maintainer response

---

## 🟠 HIGH Findings (Previously Posted)

### April 20, 2026 Hunt - Session 1

#### #3: codename-co/devs 🔴 **CRITICAL - POSTED**
- **Issue:** https://github.com/codename-co/devs/issues/1
- **Status:** ✅ POSTED Apr 20
- **Finding:** GitHub PAT + PostgreSQL combo
- **Risk:** Complete repo access + database compromise
- **Days Since Post:** 1

#### #4: openworkflowdev/openworkflow 🟠 **HIGH - POSTED**
- **Issue:** https://github.com/openworkflowdev/openworkflow/issues/482
- **Status:** ✅ POSTED Apr 20
- **Finding:** PostgreSQL URI in workflow config
- **Risk:** Database access, data breach
- **Days Since Post:** 1

#### #5: pplcallmesatz/svgtofont 🟠 **HIGH - POSTED**
- **Issue:** https://github.com/pplcallmesatz/svgtofont/issues/1
- **Status:** ✅ POSTED Apr 20
- **Finding:** PostgreSQL URI in config
- **Risk:** Database access
- **Days Since Post:** 1

#### #6: atuinsh/atuin 🟡 **MEDIUM - POSTED**
- **Issue:** https://github.com/atuinsh/atuin/issues/3438
- **Status:** ✅ POSTED Apr 20
- **Finding:** GitHub PAT pattern in secrets.rs
- **Impact:** 29.4k ⭐ project
- **Risk:** Potential token exposure
- **Days Since Post:** 1

#### #7: ayoubagrebi062-hue/olympus-2.0 🟠 **HIGH - PENDING**
- **Status:** ⏳ NOT YET POSTED
- **Finding:** Multiple secrets including PostgreSQL
- **Risk:** Database + multiple credentials
- **Action:** Need to post disclosure
- **Priority:** After new hunt results

---

## 📁 File Organization

```
docs/
├── DISCLOSURE_TRACKER.md                     ← This file
├── FRESH_HUNT_DISCLOSURES_20260421.md        ← Apr 21 drafts
├── IMPACT_ASSESSMENT_20260421.md             ← Apr 21 analysis
├── PRODUCTION_IMPACT_ANALYSIS_20260421.md    ← Technical verification
├── READY_TO_POST_DISCLOSURES.md              ← Apr 20 complete postings
├── READY_TO_POST_DISCLOSURES_APR21.md        ← Apr 21 ready-to-post
├── RESPONSIBLE_DISCLOSURE_GUIDE.md           ← Framework
└── DISCUSSION_DRAFTS.md                      ← Apr 20 drafts

reports/
├── DISCLOSURE_COMPLETION_REPORT.md           ← Apr 20 mission report
├── JACKPOT_LIVE_CREDENTIAL_20260420.json     ← First discovery
└── disclosure_timeline/                      ← Weekly tracking

scripts/osint/reports/
├── bulk_discovery_*.json                     ← Batch hunt results
├── fresh_hunt_20260421_184037.json           ← Apr 21 keys
└── hunt2_*.json                              ← Future hunts
```

---

## 📅 Timeline & Follow-ups

```
April 20, 2026 | Hunt 1 Complete - 4 posted
April 21, 2026 | Hunt 2 Complete - 2 posted
April 23, 2026 | Day 3 follow-up check (Apr 20 batch)
April 27, 2026 | Day 7 decision point (Apr 20 batch)
April 28, 2026 | Day 7 decision point (Apr 21 batch)
```

### Follow-up Schedule

| Batch | Post Date | Day 3 Check | Day 7 Decision |
|-------|-----------|-------------|----------------|
| Apr 20 | Apr 20 | Apr 23 | Apr 27 |
| Apr 21 | Apr 21 | Apr 24 | Apr 28 |

---

## 📈 Success Metrics

- **Total Discoveries:** 7 live credentials
- **Disclosures Posted:** 6/7 (86%)
- **Critical Severity:** 3
- **High Severity:** 3
- **Medium Severity:** 1
- **Response Rate:** Awaiting (0-1 days since post)

---

## Next Actions

### Immediate
- [x] Post Apr 21 disclosures (2 done)
- [ ] Post pending: ayoubagrebi062-hue/olympus-2.0
- [ ] Check Day 3 responses (Apr 23)

### This Week
- [ ] Monitor all 6 issues for maintainer responses
- [ ] Run Hunt 3 when rate limits reset
- [ ] Document any maintainer responses

### This Month
- [ ] Complete 7-day follow-ups
- [ ] Assess public disclosure decisions
- [ ] Portfolio writeup on process
