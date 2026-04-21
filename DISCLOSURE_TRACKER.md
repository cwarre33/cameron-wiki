# Credential Disclosure Tracker

## Mission Status: READY FOR OUTREACH

**Date:** April 20, 2026
**Discoveries:** 5 live credentials
**Status:** Disclosure framework complete

---

## Outcome Summary

| Repo | Maintainers | Severity | Credential Types | Status |
|------|-------------|----------|------------------|--------|
| atuinsh/atuin | @ellie, team | MEDIUM | GitHub PAT (test) | READY |
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

*Ready to reach out!*
