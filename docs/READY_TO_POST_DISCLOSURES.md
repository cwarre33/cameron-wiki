# Ready-to-Post GitHub Security Disclosures

## Posting Instructions
1. Sign into GitHub
2. Click each repo URL below
3. Go to Issues → New Issue
4. Copy Title and Body
5. Submit

---

## 1. ATUIN (atuinsh/atuin) - MEDIUM
**URL:** https://github.com/atuinsh/atuin/issues/new

**Title:**
Security Disclosure: Exposed Token Pattern in secrets.rs

**Body:**
Hi @ellie and team,

During a security audit of open-source projects, I identified a potentially 
sensitive credential pattern in your codebase.

**Discovery:**
- File: crates/atuin-client/src/secrets.rs
- Type: GitHub PAT (Classic format)
- Status: Likely test/example credential

**Recommended Actions:**
1. Verify if token is active (revoke if yes)
2. Use environment variables for test credentials
3. Consider secret scanning (TruffleHog/GitHub Advanced Security)

Best regards,
Cameron Warren
Security Researcher

---

## 2. openworkflowdev/openworkflow - HIGH
**URL:** https://github.com/openworkflowdev/openworkflow/issues/new

**Title:**
Security Alert: PostgreSQL Credentials Exposed in Configuration

**Body:**
Hello maintainers,

I discovered PostgreSQL database credentials exposed in this repository.

**Issue:** Database URL with embedded username/password
**Risk:** Unauthorized database access if production credentials

**Required Actions:**
1. Rotate database password immediately
2. Move credentials to environment variables
3. Review database access logs
4. Add .env to .gitignore

Timeline: Following responsible disclosure (7 days before public mention)

Best regards,
Cameron Warren

---

## 3. pplcallmesatz/svgtofont - HIGH  
**URL:** https://github.com/pplcallmesatz/svgtofont/issues/new

**Title:**
Security Disclosure: Database Credentials Exposed

**Body:**
Hi,

PostgreSQL database URL with embedded credentials found in codebase.

**Risk:** Full database read/write access

**Fix:**
1. Rotate database password
2. Use process.env.DATABASE_URL
3. Add .env to .gitignore

Happy to clarify details. Please confirm when credentials rotated.

Best,
Cameron Warren

---

## 4. ayoubagrebi062-hue/olympus-2.0 - HIGH (Multiple)
**URL:** https://github.com/ayoubagrebi062-hue/olympus-2.0/issues/new

**Title:**
CRITICAL: Multiple Exposed Secrets in Repository

**Body:**
Multiple credentials exposed requiring immediate attention:

**Exposed:**
1. PostgreSQL Database URL with password
2. Plaintext password in configuration

**Urgent Actions:**
1. Rotate ALL credentials NOW
2. Move to environment variables
3. Review git history if previously committed
4. Enable secret scanning

Timeline: 7-day disclosure window

Cameron Warren
Security Researcher

---

## 5. codename-co/devs - CRITICAL
**URL:** https://github.com/codename-co/devs/issues/new

**Title:**
🚨 CRITICAL: GitHub Token + Database Credentials Exposed

**Body:**
CRITICAL SECURITY DISCLOSURE - Immediate Action Required

**Critical Findings:**
1. GitHub Personal Access Token (Classic)
2. PostgreSQL Database URL with credentials

**Severity: CRITICAL** - Complete system compromise possible

**IMMEDIATE ACTIONS (Within 24 Hours):**
1. Revoke GitHub token: github.com/settings/tokens
2. Rotate database password
3. Check audit logs for unauthorized access
4. Move credentials to environment variables
5. Add .env to .gitignore

Responsible disclosure timeline: Today (Day 0), follow-up Day 3

Please acknowledge receipt urgently.

Best regards,
Cameron Warren
Security Researcher
GitHub: @cwarre33

---

## Posting Order
1. codename-co/devs (CRITICAL)
2. olympus-2.0 (HIGH - Multiple)
3. openworkflow (HIGH)
4. svgtofont (HIGH)
5. atuin (MEDIUM)

## Follow-up Template
```
Hi team, following up on the security disclosure from [DATE].
Have you had a chance to review? Happy to provide more details.
```

