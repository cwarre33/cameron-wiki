# Responsible Disclosure Report - April 20, 2026

## Executive Summary

During an OSINT security research session on open-source GitHub repositories, I discovered **5 exposed credentials** across multiple projects. These credentials pose security risks including unauthorized access, data exposure, and potential system compromise.

---

## Discovery 1: GitHub PAT in ATUIN Shell History

**Repository:** atuinsh/atuin (20,000+ stars)
**File:** `crates/atuin-client/src/secrets.rs`
**Credential Type:** GitHub Personal Access Token (Classic)
**Redacted Value:** `ghp_R2***2muH`
**Severity:** MEDIUM
**Discovery Method:** Automated regex pattern matching

**Context:** Token appears in source code, likely test/example credential
**Potential Risk:** If active, could allow unauthorized GitHub API access

**Remediation:**
1. Verify if token is active
2. Revoke if active
3. Move token to environment variable or secrets manager
4. Add pre-commit hooks to prevent future exposure

---

## Discovery 2: PostgreSQL Database Credentials

**Repository:** openworkflowdev/openworkflow
**File:** Configuration/documentation file
**Credential Type:** PostgreSQL Database URL
**Severity:** HIGH
**Discovery:** Round 15 of bulk scan

**Context:** Database connection string with embedded credentials
**Potential Risk:** Full database read/write access if production

**Remediation:**
1. Rotate database password immediately
2. Use environment variables for connection strings
3. Review database access logs for unauthorized queries

---

## Discovery 3: PostgreSQL Database Credentials (Second Instance)

**Repository:** pplcallmesatz/svgtofont
**Credential Type:** PostgreSQL Database URL
**Severity:** HIGH
**Discovery:** Round 15 of bulk scan

**Similar to Discovery 2 - Database URL with credentials**

---

## Discovery 4: Database Credentials + Password

**Repository:** ayoubagrebi062-hue/olympus-2.0
**Credentials Found:**
- PostgreSQL URL with embedded credentials
- Plaintext Password
**Severity:** HIGH
**Discovery:** Round 26

**Context:** Multiple secrets in same file
**Risk:** Database compromise, unauthorized access

---

## Discovery 5: GitHub PAT + Database Credentials

**Repository:** codename-co/devs
**Credentials Found:**
- GitHub PAT (classic): `ghp_AB***7890`
- PostgreSQL Database URL
**Severity:** HIGH
**Discovery:** Round 26

**Context:** Repository contains both GitHub access token AND database credentials
**Risk:** Complete system compromise - source code + database access

---

## Impact Assessment

### Severity Distribution
- 🔴 **CRITICAL:** 0
- 🟠 **HIGH:** 4 (Database credentials)
- 🟡 **MEDIUM:** 1 (Test/example tokens)

### Attack Scenarios
1. **Database Compromise:** PostgreSQL URLs could allow data exfiltration, modification, or deletion
2. **Source Code Access:** GitHub PATs could allow malicious code injection
3. **Privilege Escalation:** Combined credentials enable complete system takeover

---

## Timeline

| Date/Time | Event |
|-----------|-------|
| 2026-04-20 21:53 | Discovery #1 (ATUIN) - Automated search |
| 2026-04-20 22:01 | Batch discovery initiated (target: 5 credentials) |
| 2026-04-20 22:03 | Discovery #2 - PostgreSQL URL |
| 2026-04-20 22:03 | Discovery #3 - PostgreSQL URL |
| 2026-04-20 22:04 | Discovery #4 - Multiple credentials |
| 2026-04-20 22:04 | Discovery #5 - Combined GitHub + Database |
| 2026-04-20 22:05 | Disclosure report preparation |
| 2026-04-21 | **Day 0** - Initial outreach to maintainers |
| 2026-04-24 | **Day 3** - Follow-up if no acknowledgment |
| 2026-04-28 | **Day 7** - Public disclosure consideration |

---

## Disclosure Actions Required

### Immediate (Day 0)
- [ ] Create GitHub Security Advisory for each repo
- [ ] Open discussions tagging maintainers
- [ ] Provide exact file locations and line numbers
- [ ] Offer remediation guidance

### Short-term (Days 1-3)
- [ ] Follow up if no acknowledgment
- [ ] Provide additional context if requested
- [ ] Verify fixes when applied

### Long-term (Days 7+)
- [ ] Assess if public disclosure is appropriate
- [ ] Compile into portfolio writeup
- [ ] Share lessons learned (without exposing secrets)

---

## Tools Used

- **Discovery:** `live_credential_hunter.py`, `bulk_credential_hunter.py`
- **Scanning:** GitHub Search API, TruffleHog
- **Analysis:** Custom regex patterns for high-value secrets

---

## Ethical Statement

- ✅ Discovered credentials have NOT been accessed or used
- ✅ Only redacted values are documented (never full credential strings)
- ✅ Responsible disclosure timeline allows maintainers time to remediate
- ✅ Public disclosure will only occur after 7+ days or with maintainer consent

---

## Contact

Cameron Warren
Security Researcher
[GitHub Profile: cwarre33]

---

*This report is for responsible disclosure purposes. Credentials shown are redacted for security.*
