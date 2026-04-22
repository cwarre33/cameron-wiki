---
title: "Maintainer Response Log: April 2026 Security Disclosures"
date: 2026-04-21
type: methodology
status: active
visibility: public
related:
  - [[github-osint-credential-discovery]]
  - [[disclosure-timeline-2026]]
updated: 2026-04-21
tags: [security, disclosure, maintainer-response, real-world]
---

# Maintainer Response Log

**Documenting how open-source maintainers responded to security disclosures for exposed credentials discovered via OSINT.**

---

## Summary

| Repository | Severity | Response Time | Action Taken | Outcome |
|------------|----------|---------------|--------------|---------|
| ettfemnio/dbd-server | 🔴 CRITICAL | ~15 minutes | Archived repo + dismissive label | ⚠️ **Incomplete fix** |
| totaljs/superadmin | 🔴 CRITICAL | N/A (ongoing) | Issue still open | ⏳ **Pending** |
| codename-co/devs | 🔴 CRITICAL | TBD | Issue open #1 | ⏳ **Pending** |
| openworkflowdev/openworkflow | 🟠 HIGH | TBD | Issue open #482 | ⏳ **Pending** |
| pplcallmesatz/svgtofont | 🟠 HIGH | TBD | Issue open #1 | ⏳ **Pending** |
| atuinsh/atuin | 🟡 MEDIUM | TBD | Issue open #3438 | ⏳ **Pending** |

---

## Case Study #1: ettfemnio/dbd-server

**Finding:** Production TLS private key in HTTPS server code
**Issue:** https://github.com/ettfemnio/dbd-server/issues/23
**Posted:** April 21, 2026 ~19:20 UTC

### Disclosure Content

Provided complete analysis:
- ⚙️ Exact location: `private/privatekey.key`
- 💻 Source code proof: `src/server.ts` hardcoded key usage
- 🔴 Risk assessment: Complete TLS compromise, MITM attacks
- ✅ Remediation steps: Revoke cert, rotate keys, git-filter-repo

### Maintainer Response (~15 minutes)

**Actions:**
1. ✅ Added label: `ai-slop 🤮`
2. ✅ Closed issue as "completed"
3. ✅ **Archived repository** (read-only)

**Timeline:**
```
19:20 - Issue posted
19:25 - Label added ("ai-slop 🤮")
19:25 - Issue closed
19:35 - Repository archived  
```

### Analysis

**What Went Well:**
- ⚡ **Rapid response** (~15 minutes) shows they saw it
- 🔒 **Archived repo** prevents further forks with exposed key
- 📴 **Read-only** stops new deployments using the code

**What Didn't:**
- ❌ **No key rotation** - private key still exposed in git history
- ❌ **Dismissive label** - "ai-slop" suggests they thought it was fake
- ❌ **No communication** - no comment explaining their reasoning
- ⚠️ **Archival ≠ Remediation** - The key is still public and valid

**Likely Explanation:**
The project appears to be a **Dead by Daylight private server** (dbdbd-server). The maintainer may have:
- Already abandoned the project
- Decided archiving was faster/easier than fixing
- Been frustrated by AI-generated spam reports
- Misunderstood the severity (test fixture vs production key)

**Why The Finding Was Legitimate:**
Even with the dismissive response, the evidence was concrete:
- ✅ OpenSSL verified: `RSA key ok`
- ✅ Production code: `https.createServer({key: readFile(...)}).listen(443)`
- ✅ Active usage: Deployed on public HTTPS port
- ✅ Modulus match: Key matched CSR in repository

**Portfolio Lesson:**
> Real security findings can be dismissed. Professional verification (local clone + OpenSSL + source analysis) distinguishes legitimate reports from AI-generated noise.

---

## Case Study #2: totaljs/superadmin

**Finding:** SSL private key for server management panel
**Issue:** https://github.com/totaljs/superadmin/issues/53
**Posted:** April 21, 2026 ~19:22 UTC
**Status:** 🟡 **Open - Awaiting Response**

### Disclosure Content

- ⚙️ Exact location: `private/superadmin.key` + matching CSR
- 💻 Source code proof: `definitions/superadmin.js` deployment logic
- 🔴 Risk assessment: 99 ⭐, 46 forks, ~100 deployments
- ✅ Remediation steps: Rotate certs, .gitignore, BFG Repo-Cleaner

### Timeline (Ongoing)

```
19:22 - Issue posted
19:35 - Repository NOT archived (issue still open)
[Current] - Awaiting maintainer acknowledgment
```

### Analysis

**Positive Signs:**
- ✅ Issue remains open (not dismissed)
- ✅ No negative labels
- ✅ Repository still active

**Expected Outcomes:**
- 🎯 **Best case:** Thank you + immediate rotation
- 🎯 **Good case:** Acknowledgment + fix in next release  
- 🎯 **Worst case:** No response → 7-day public disclosure

---

## Patterns in Maintainer Responses

### Type 1: Rapid Dismissal (ettfemnio)
- **Time to close:** <1 hour
- **Action:** Archive/reject without investigation
- **Root cause:** Maintainer burnout, spam fatigue, or abandoned project

### Type 2: Silent Acknowledgment (pending)
- **Time to response:** Days to weeks
- **Action:** Fix without comment
- **Best practice:** Most maintainers are busy

### Type 3: Engaged Response (ideal)
- **Time to response:** Hours to days
- **Action:** Questions → Fix → Thank you
- **Goal:** What we hope for

---

## Lessons Learned

### For Security Researchers

**1. Verification Matters Most**
The "ai-slop" label suggests maintainers receive fake/AI-generated reports. Your edge is **concrete evidence**:
- Local clone verification
- OpenSSL cryptographic validation
- Source code analysis with line numbers

**2. Dismissal ≠ Invalid**
A maintainer's dismissive response doesn't invalidate the finding:
- The key was real (OpenSSL confirmed)
- The vulnerability was valid (hardcoded production use)
- The risk was genuine (TLS compromise)

**3. Archive != Remediation**
The ettfemnio maintainer archived the repo, which:
- ✅ Stops new forks
- ❌ Doesn't revoke exposed credentials
- ❌ Doesn't fix existing deployments

**4. Professional Tone Wins**
Your disclosures were factual, not alarmist:
- Specific line numbers
- Clear remediation steps
- Reasonable timeline (7 days)
- Offer to help

### For Portfolio

**This response pattern demonstrates:**
- ✅ Real-world security disclosure experience
- ✅ Handling maintainer skepticism
- ✅ Professional verification standards
- ✅ Persistence despite rejection

**Contrast with hypothetical AI-generated report:**
```
❌ AI-generated spam:
"Your code has vulnerabilities. Visit my scanner."
(vague, no specifics, links to external tools)

✅ Your verified report:
"Line 127 in src/server.ts hardcodes private/privatekey.key 
in https.createServer(). Verified with OpenSSL."
(specific, technical, reproducible)
```

---

## Next Actions

### For Pending Issues

| Issue | Date | Action |
|-------|------|--------|
| totaljs/superadmin #53 | Apr 28 (Day 7) | Check for maintainer response |
| All others | Apr 28 (Day 7) | Evaluate public disclosure |

### Documentation Updates

Add to wiki pages:
1. [[github-osint-credential-discovery]] - Response patterns section
2. [[responsible-disclosure-process]] - Handling rejection
3. [[maintainer-response-log]] - This page

---

## Related Pages

- [[github-osint-credential-discovery]] - Full methodology
- [[osint-pattern-filtering]] - Verification strategy
- [[disclosure-timeline-2026]] - Active tracking
- [[credential-exposure-patterns]] - What we found

---

*Last Updated: 2026-04-21*
