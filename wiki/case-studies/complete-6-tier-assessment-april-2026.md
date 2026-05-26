---
title: "Complete 6-Tier Assessment: All April 2026 Discoveries"
date: 2026-04-21
type: comparison
status: analysis
visibility: public
related:
  - [[tier-6-external-osint-validation]]
  - [[tier-6-retroactive-ettfemnio]]
  - [[maintainer-response-log]]
created: 2026-04-21
updated: 2026-04-21
tags: [assessment, tier-6, all-findings, comparison, disclosure-readiness]
---

# Complete 6-Tier Assessment: All April 2026 Discoveries

**Evaluating all 7 credential discoveries using the full 6-tier framework to determine disclosure readiness and lessons learned.**

---

## Summary Matrix

| Finding | Repo Stars | Type | Tiers 1-5 | Tier 6 | Total | Status | Disclosure |
|---------|------------|------|-----------|--------|-------|--------|------------|
| **ettfemnio/dbd-server** | 18 | Private Key | 98/110 | **7/30** | 105/140 | ❌ DISMISSED | #23 (archived) |
| **totaljs/superadmin** | 99 | Private Key | 95/110 | **15/30** | 110/140 | ⏳ PENDING | #53 (open) |
| **codename-co/devs** | N/A | Combo (PAT+DB) | 88/110 | **20/30** | 108/140 | ⏳ PENDING | #1 (open) |
| **openworkflow** | ? | PostgreSQL | 82/110 | **12/30** | 94/140 | ⏳ PENDING | #482 (open) |
| **pplcallmesatz** | ? | PostgreSQL | 85/110 | **10/30** | 95/140 | ⏳ PENDING | #1 (open) |
| **atuin** | 29.4k | GitHub PAT | 75/110 | **18/30** | 93/140 | ⏳ PENDING | #3438 (open) |
| **olympus-2.0** | ? | Multiple | ? | ? | ? | ⏳ NOT POSTED | - |

**Tally:**
- DEFINITIVE (130+): 0
- STRONG (110-129): 2
- PROBABLE (90-109): 4
- DISMISSED: 1

---

## Tier-by-Tier Breakdown

### Finding #1: ettfemnio/dbd-server
**Status:** ❌ DISMISSED as "ai-slop"

| Tier | Score | Gaps | Evidence Available |
|------|-------|------|---------------------|
| 1 | 20/20 | None | ✅ High entropy, production path |
| 2 | 25/30 | No CSR match | ✅ OpenSSL valid, 2048-bit |
| 3 | 27/30 | No deployment proof | ✅ Code uses key, but live? |
| 4 | 18/20 | Scope unclear | ✅ 18 stars, active repo |
| 5 | 8/10 | No screenshots | ✅ Code snippets, line numbers |
| **6** | **7/30** | **MISSING CT LOGS** | ❌ No domain, no live proof |
| **TOTAL** | **105/140** | | |

**Tier 6 Gap Analysis:**
- ❌ **No CT logs** - Likely self-signed certificate
- ❌ **No live service** - No public domain documented
- ✅ **Git forensics** - 5 years exposed, owner committed
- ✅ **Organization** - Individual account
- ❌ **No service enumeration** - Unknown deployment scope

**Why Dismissed:** Code showed production use, but **no external proof** of active deployment.

**Lesson:** For private keys, **modulus match + CT logs** are essential.

---

### Finding #2: totaljs/superadmin
**Status:** ⏳ OPEN - Pending maintainer

| Tier | Score | Evidence | Notes |
|------|-------|----------|-------|
| 1 | 20/20 | ✅ `extension:key path:private` | Standard location |
| 2 | 28/30 | ✅ OpenSSL + **CSR Modulus Match** | Better than ettfemnio |
| 3 | 27/30 | ✅ Code shows deployment to `/www/ssl/` | Production path |
| 4 | 19/20 | ✅ 99 stars, 46 forks | Higher impact |
| 5 | 10/10 | ✅ Full evidence package | Line numbers, snippets |
| **6** | **15/30** | ⚠️ Partial | No CT but deployment clearer |
| **TOTAL** | **119/140** | | **STRONG** |

**Tier 6 Evidence:**
- ❌ **CT Logs** - Not checked yet
- ⚠️ **Deployment context** `/www/ssl/superadmin.key` suggests production install
- ✅ **Git forensics** - Multi-year exposure, core maintainer
- ✅ **Organization** - totaljs organization (legitimate)
- ⚠️ **No live confirmation** - But deployment path clear

**Advantages over ettfemnio:**
1. **CSR exists** - `superadmin.csr` - proves key was actually used
2. **Modulus match** - We verified key matches CSR
3. **Higher profile** - 99 stars = more maintainer attention
4. **Organization** - totaljs is established project

**Expected Outcome:** Better response than ettfemnio due to clearer production context.

---

### Finding #3: codename-co/devs
**Status:** ⏳ OPEN - Combo exposure (PAT + PostgreSQL)

| Tier | Score | Evidence | Notes |
|------|-------|----------|-------|
| 1 | 20/20 | ✅ Pattern matches | `ghp_` + `postgres://` |
| 2 | 25/30 | ✅ Token format valid | No OpenSSL needed |
| 3 | 28/30 | ✅ Code uses both | Dev/prod environment |
| 4 | 15/20 | ⚠️ Low visibility repo | But CRITICAL severity |
| 5 | 10/10 | ✅ Full package | Both credentials documented |
| **6** | **20/30** | ⚠️ Good but incomplete | |
| **TOTAL** | **118/140** | | **STRONG** |

**Tier 6 Evidence:**
- ⚠️ **GitHub API** - Can check if token is still valid (don't use!)
- ✅ **Repository activity** - Recent commits
- ✅ **Organization** - Real GitHub org
- ✅ **PAT scope** - Can see permissions in token format
- ⚠️ **PostgreSQL host** - Could be localhost vs remote

**Unique Factors:**
- **Combo exposure** = higher severity
- **GitHub PAT** - GitHub may have already revoked via Secret Scanning
- **PostgreSQL** - If remote, immediate data breach risk

**Missing Tier 6:**
- Token revocation status (check GitHub)
- PostgreSQL host connectivity (local vs remote)
- Associated GitHub account activity

---

### Finding #4: openworkflowdev/openworkflow
**Status:** ⏳ OPEN - PostgreSQL URI

| Tier | Score | Evidence | Notes |
|------|-------|----------|-------|
| 1 | 18/20 | ⚠️ Some keywords | `sample` in nearby code? |
| 2 | 20/30 | ⚠️ URI parsing only | No crypto validation |
| 3 | 20/30 | ⚠️ Config file | Unclear if production |
| 4 | 14/20 | ✅ Active project | Recent updates |
| 5 | 10/10 | ✅ Documented | Full disclosure |
| **6** | **12/30** | ⚠️ Weak external | |
| **TOTAL** | **94/140** | | **PROBABLE** |

**Tier 6 Evidence:**
- ⚠️ **No CT logs** - Database credentials don't have certs
- ⚠️ **Host validation** - Could be localhost
- ✅ **Project activity** - Active development
- ⚠️ **Scope unclear** - Single dev or org tool?

**Challenges:**
- Database URIs **harder to Tier 6 validate** than keys
- No certificate path
- Connection string could be placeholder
- Need **actual connection proof** (risky!)

---

### Finding #5: pplcallmesatz/svgtofont
**Status:** ⏳ OPEN - PostgreSQL URI

| Tier | Score | Evidence | Notes |
|------|-------|----------|-------|
| 1 | 20/20 | ✅ Clean pattern | No skip keywords |
| 2 | 20/30 | ⚠️ URI only | No crypto (normal) |
| 3 | 25/30 | ✅ Production code | Used in build pipeline |
| 4 | 15/20 | ⚠️ Lower stars | Still active |
| 5 | 10/10 | ✅ Documented | |
| **6** | **10/30** | ❌ Weak | |
| **TOTAL** | **100/140** | | **PROBABLE** |

**Similar to openworkflow** - Database URI, harder to externally validate.

---

### Finding #6: atuinsh/atuin
**Status:** ⏳ OPEN - GitHub PAT pattern

| Tier | Score | Evidence | Notes |
|------|-------|----------|-------|
| 1 | 15/20 | ⚠️ Pattern in test code | `secrets.rs` test |
| 2 | 22/30 | ⚠️ Valid format | Can't verify without using |
| 3 | 10/30 | ❌ **Test file** | `src/secrets.rs` test data |
| 4 | 8/20 | ✅ 29.4k stars | But false positive risk |
| 5 | 10/10 | ✅ Documented | Proper disclosure |
| **6** | **18/30** | ⚠️ Mixed | |
| **TOTAL** | **93/140** | | **PROBABLE/QUESTIONABLE** |

**CRITICAL: Test File**
- Located in `src/secrets.rs` - test fixture
- Pattern: `ghp_****test****` (test data format)
- Project: **29.4k stars** = very careful here

**Tier 6 Evidence:**
- ✅ **High visibility** - Major project (shell history tool)
- ✅ **Test context** - Clearly test fixture
- ✅ **Pattern** - Contains "test" in placeholder

**Verdict:** **LIKELY FALSE POSITIVE** despite disclosure
- Pattern in test file
- Format suggests test data
- Major project likely careful

**Lesson:** For major projects (10k+ stars), require **higher Tier 3 threshold**

---

## Tier 6 Difficulty by Credential Type

| Credential Type | Tier 6 Ease | Best Methods | Example |
|----------------|------------|--------------|---------|
| **Private Keys** | ⭐⭐⭐ Easy | CT logs, Shodan TLS, modulus match | ettfemnio, superadmin |
| **Database URIs** | ⭐⭐ Medium | DNS resolve, port check, banner grab | openworkflow, pplcallmesatz |
| **API Tokens** | ⭐ Hard | Token introspection (risky), usage logs | codename-co, atuin |

**Why Private Keys Are Easiest:**
- Have associated certificates (CT logs)
- Used in TLS (Shodan can see)
- Modulus match (mathematical proof)
- Standard formats (easy to verify)

**Why API Tokens Are Hardest:**
- No external certificate
- Usage requires authentication
- Could be test tokens
- Format varies by provider

---

## Red Flags (Would Have Prevented Disclosures)

### atuin - Should Not Have Been Disclosed

**Red Flags Present:**
- ❌ Found in **test file** (`src/secrets.rs`)
- ❌ Contains **"test"** in placeholder
- ❌ **29.4k stars** - major project
- ⚠️ No usage in production code

**Should have required:**
- Source code review FIRST
- Higher confidence threshold
- Or just **marked as false positive**

### What to Check Before Disclosing Major Projects

```markdown
## Major Project (10k+ stars) Prechecklist

- [ ] Is it in test/ directory?
- [ ] Does it contain "test", "example", "fake"?
- [ ] Is it used in production code?
- [ ] Is it imported by main entry points?
- [ ] Is it exported from library?
- [ ] Would the failure be catastrophic?

If ANY check fails → Likely false positive
```

---

## Success Patterns: What Worked

### codename-co/devs - Strong Finding

**Why Strong:**
- ✅ Combo exposure (PAT + DB)
- ✅ Both in production code
- ✅ Real organization
- ✅ Recent activity
- ✅ High impact (complete takeover)

**Tier 6 Potential:**
- Could validate PAT scope
- Could check DB connectivity
- Real deployment likely

### totaljs/superadmin - Strong Finding

**Why Strong:**
- ✅ CSR modulus match
- ✅ Code shows production deployment
- ✅ 99 stars = legitimate usage
- ✅ Established organization
- ✅ Clear deployment path

---

## Recommended Actions by Finding

### Immediate Priority

**1. totaljs/superadmin #53**
- ⏰ **Day 3 Check:** Apr 24
- 🔍 **Next Step:** Wait for maintainer response
- 💡 **Expected:** Better than ettfemnio (clearer context)

**2. codename-co/devs #1**
- ⏰ **Day 3 Check:** Apr 24
- 🔍 **Next Step:** Check if GitHub auto-revoked PAT
- 🔥 **Priority:** HIGH (combo exposure)

### Reassessment Needed

**3. atuinsh/atuin #3438**
- 🤔 **Reassess:** Likely false positive
- 🔍 **Action:** Close disclosure or add note
- 📝 **Lesson:** Test files should be filtered harder

**4. openworkflow #482, pplcallmesatz #1**
- ⏰ **Wait:** Day 7 for responses
- 🔍 **Tier 6:** Harder for DB URIs, need patience

### Not Posted

**5. olympus-2.0**
- 📝 **Action:** Apply full Tier 6 before posting
- 🔍 **Research:** Gather more external evidence

---

## Updated Protocol: When to Disclose

### Private Keys (ettfemnio, superadmin)

**Minimum for disclosure:**
- ✅ OpenSSL validation
- ✅ Source code showing production use
- ⭐ **NEW:** Check for associated certificate
- ⭐ **NEW:** Verify modulus match (key ↔ cert)
- ⭐ **NEW:** Search CT logs (if cert found)

**STRONG (110+):** Modulus match, production context clear
**DEFINITIVE (130+):** CT log entry + live service confirmation

### Database URIs (openworkflow, pplcallmesatz)

**Minimum for disclosure:**
- ✅ URI parsing (valid format)
- ✅ Not in test/ directory
- ✅ Used in production code
- ⭐ **NEW:** Host is remote (not localhost)
- ⭐ **NEW:** Port open on remote host

**STRONG (110+):** Remote host, production code
**DEFINITIVE (130+):** Actual connection proof (careful!)

### API Tokens (codename-co, atuin)

**Minimum for disclosure:**
- ✅ Valid format
- ✅ Production usage
- ⭐ **NEW:** Token not in test/ or mock data
- ⭐ **NEW:** High-confidence source code
- ⭐ **NEW:** Major project = extra scrutiny

**STRONG (110+):** Production code, real org
**DEFINITIVE (130+):** Token introspection proof (rare)

---

## Lessons Summary

### 1. Tier 6 is Essential for Private Keys

Without CT logs or live service proof:
- Dismissal as "not deployed" possible
- Maintainer assumes test data
- Archival instead of rotation

**Fix:** Always search CT logs, check for modulus match.

### 2. Major Projects (10k+ stars) Need Extra Scrutiny

atuin finding:
- Should have been filtered as test data
- 29.4k stars means careful maintainers
- Test file = probably intentional test fixture

**Fix:** Higher threshold for major projects.

### 3. Different Credential Types, Different Tier 6

- **Keys:** Easy (CT logs, Shodan)
- **DBs:** Medium (DNS, port scan)
- **Tokens:** Hard (introspection, usage)

**Fix:** Adjust Tier 6 expectations by credential type.

### 4. Combo Exposures = Higher Priority

codename-co/devs:
- PAT + DB = complete takeover
- Even without full Tier 6, severity warrants disclosure

**Fix:** Combo credentials get priority even with lower scores.

---

## Related

- [[tier-6-retroactive-ettfemnio]] - Detailed case study
- [[tier-6-external-osint-validation]] - Full methodology
- [[maintainer-response-log]] - Response patterns
- [[pre-disclosure-validation-protocol]] - Original framework

---

*Analysis Date: 2026-04-21*
*Framework: 6-Tier Pre-Disclosure Validation*
*Findings: 7 discoveries, 6 posted, 1 dismissed*
