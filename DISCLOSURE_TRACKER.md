# Credential Disclosure Tracker

## Mission Status: READY FOR OUTREACH

**Date:** April 20, 2026
**Discoveries:** 5 live credentials
**Status:** Disclosure framework complete

---

## Outcome Summary

| Repo | Maintainers | Severity | Credential Types | Status |
|------|-------------|----------|------------------|--------|
| atuinsh/atuin | @ellie, team | MEDIUM | GitHub PAT (test) | **BLOCKED — hostile response, AI-slop detected** |
| openworkflowdev/openworkflow | Unknown | HIGH | PostgreSQL URL | READY |
| pplcallmesatz/svgtofont | Unknown | HIGH | PostgreSQL URL | READY |
| ayoubagrebi062-hue/olympus-2.0 | Unknown | HIGH | PostgreSQL + Password | READY |
| codename-co/devs | Unknown | HIGH | GitHub PAT + PostgreSQL | READY |

**Total Critical:** 1 (Combined GitHub + Database)
**Total High:** 3 (Database credentials)
**Total Medium:** 1 (Test token in popular project)

---

## Ready to Execute

### Discussion Templates: ✅ Ready in `docs/DISCUSSION_DRAFTS.md`
- Pre-written 5 GitHub discussions
- Response templates
- Follow-up timelines

### Responsible Disclosure Guide: ✅ Ready in `docs/RESPONSIBLE_DISCLOSURE_GUIDE.md`
- Severity framework
- Disclosure timelines
- Ethical guidelines
- Contact methods

### Full Report: ✅ Ready in `reports/RESPONSIBLE_DISCLOSURE_REPORT_20260420.md`
- Discovery details
- Impact assessment
- Remediation steps
- Timeline

---

## Recommended Next Actions

1. **Priority Order (by severity):**
   - codename-co/devs → CRITICAL (combined threat)
   - ayoubagrebi062-hue/olympus-2.0 → HIGH (multiple secrets)
   - openworkflowdev/openworkflow → HIGH
   - pplcallmesatz/svgtofont → HIGH
   - atuinsh/atuin → MEDIUM (but popular, good PR)

2. **Create GitHub Discussions:**
   - Create one per repo
   - Use templates from `docs/DISCUSSION_DRAFTS.md`
   - Tag maintainers when possible
   - Set appropriate severity tags

3. **Track Responses:**
   - Day 0: Initial post
   - Day 3: Follow-up if no ack
   - Day 7: Consider escalation

4. **Tools Available:**
   - `live_credential_hunter.py` - Single discovery
   - `bulk_credential_hunter.py` - Multiple discoveries
   - `wow_continuous_discovery.py` - Continuous scanning

---

## Hunt Statistics

- **Rounds completed:** 26
- **Files analyzed:** 33
- **Success rate:** 15% (5/33)
- **Time to 5 discoveries:** ~3 minutes

---

## All Committed to GitHub

```
docs/
  ├── RESPONSIBLE_DISCLOSURE_GUIDE.md    # Framework
  └── DISCUSSION_DRAFTS.md                # Templates

reports/
  ├── RESPONSIBLE_DISCLOSURE_REPORT_20260420.md
  └── JACKPOT_LIVE_CREDENTIAL_20260420.json

scripts/osint/
  ├── bulk_credential_hunter.py
  ├── live_credential_hunter.py
  ├── wow_continuous_discovery.py
  └── (4 other scanners)
```

---

## Lessons Learned (2026-04-21)

### atuinsh/atuin — BLOCKED

**What happened:** Issue #3438 submitted with templated "security researcher" disclosure format. Maintainer Ellie Huxtable responded with hostility ("lol what?", "just no dude", "tell your claude to stand down") and blocked from the atuinsh organization.

**Why it failed:**
1. The finding was likely a **test token** in a test file — not a production leak
2. The disclosure was **immediately recognizable as AI-generated** (structured template, formal sign-off, severity labels)
3. The maintainer perceived it as **spam/self-promotion** rather than a good-faith report
4. The "security researcher" framing for a minor finding came across as self-important

**Decision:** See [[wiki/decisions/disclosure-communication-humanization.md]] for full analysis and new rules:
- No bulk templates for repos >1k stars
- Human rewrite required for every disclosure to a popular repo
- Test/fixture findings get a "should I even send this?" gate
- Max 3 sentences for GitHub issue disclosures unless genuinely critical
- First-name-only sign-off — no "security researcher" title
- 5-minute cooling-off period before posting any disclosure

**Cost:** Blocked from atuinsh/atuin (20k+ stars). Public block record visible to other maintainers. Future disclosures must be significantly more careful.

---

*Ready to reach out!*
