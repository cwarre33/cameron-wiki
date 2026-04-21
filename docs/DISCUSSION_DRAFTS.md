# GitHub Discussion Drafts

## Discussion 1: ATUIN (atuinsh/atuin)

**Title:** Security Disclosure - Exposed Token in secrets.rs

**Body:**
Hi team,

I hope you're doing well. During a security audit of open-source projects, I identified a potentially sensitive credential exposed in your codebase.

**Discovery:**
- **File:** `crates/atuin-client/src/secrets.rs`
- **Type:** GitHub Personal Access Token (Classic format)
- **Appears to be:** Test/example token

While this looks like a test credential, wanted to flag it for review in case it's active.

**Recommended Actions:**
1. Verify if token is active (revoke if yes)
2. Consider using environment variables for test credentials
3. Add `secrets.rs` pattern to `.gitignore` or use GitHub Secrets

I'm happy to provide more details via private channels if preferred.

Best,
Cameron

---

## Discussion 2: openworkflowdev/openworkflow

**Title:** Security Disclosure - PostgreSQL Credentials in Config

**Body:**
Hello maintainers,

During an open-source security research project, I discovered a PostgreSQL database URL with embedded credentials in your repository.

**Discovery:**
- **Type:** PostgreSQL connection string with username/password
- **Impact:** If this connects to a production database, it could allow unauthorized access

**Immediate Recommendations:**
1. **Rotate the database password** (change immediately)
2. Move connection strings to environment variables
3. Review database access logs for unauthorized queries
4. Add `.env` files with credentials to `.gitignore`

**Prevention:**
- Consider using GitHub Advanced Security secret scanning
- Tools like TruffleHog or GitLeaks for CI/CD pipelines

I'm happy to help clarify anything. Please let me know if you've rotated the credentials!

Best regards,
Cameron Warren

---

## Discussion 3: pplcallmesatz/svgtofont

**Title:** Security Alert - Database Credentials Exposed

**Body:**
Hi,

Security researcher here. I found a PostgreSQL database URL with embedded credentials while auditing open-source projects.

**Issue:** Database connection string exposed in repository

**Actions Needed:**
1. Rotate database password immediately
2. Move credentials to environment variables  
3. Review database access logs
4. Consider implementing secret scanning

Let me know if you need more details.

Thanks,
Cameron

---

## Discussion 4: ayoubagrebi062-hue/olympus-2.0

**Title:** Critical Security Disclosure - Multiple Exposed Secrets

**Body:**
Hello,

I discovered multiple credentials exposed in this repository during a security research scan:

**Exposed:**
1. PostgreSQL database URL with credentials
2. Plaintext password

**Risk:** Complete database compromise if these are production credentials

**Please Take Immediate Action:**
1. Rotate all database passwords
2. Change any associated service passwords
3. Move all credentials to environment variables or GitHub Secrets
4. Add exposed files to `.gitignore`

This disclosure follows responsible disclosure practices. I'm available to help clarify details.

Best,
Cameron

---

## Discussion 5: codename-co/devs

**Title:** Critical Security Issues - GitHub Token + Database Credentials Exposed

**Body:**
Hi team,

I discovered significant security exposure in this repository that requires immediate attention.

**Critical Findings:**
1. **GitHub Personal Access Token** (Classic format)
2. **PostgreSQL Database URL** with embedded credentials

**Combined Impact:**
This combination poses severe risk:
- Source code access via GitHub token
- Database access via PostgreSQL URL
- Potential for complete system compromise

**Immediate Actions Required:**
1. **Revoke the GitHub PAT** immediately via GitHub Settings
2. **Rotate all database passwords**
3. **Review GitHub audit logs** for unauthorized access
4. **Review database access logs** for unauthorized queries
5. **Move credentials to environment variables**

**Urgency:** HIGH - please address within 24 hours if possible

I'm available to discuss privately and can help verify fixes.

Best regards,
Cameron Warren
Security Researcher

---

# Disclosure Checklist

## Before Posting:
- [ ] Verify all redacted values are properly masked
- [ ] Ensure full credential strings are NOT posted
- [ ] Confirm each repo is NOT just a tutorial/example
- [ ] Check repository has recent activity (not abandoned)

## Posting Order (by severity):
1. **codename-co/devs** - CRITICAL (GitHub + Database)
2. **ayoubagrebi062-hue/olympus-2.0** - HIGH (Multiple secrets)
3. **openworkflowdev/openworkflow** - HIGH (Database)
4. **pplcallmes/svgtofont** - HIGH (Database)
5. **atuinsh/atuin** - MEDIUM (Test token, but popular project)

## Tracking Spreadsheet Columns:
| Repo | Maintainers | Posted Date | Acknowledged | Remediated | Notes |
|------|-------------|-------------|--------------|------------|-------|
| | | | | | |

---

# Response Templates

## If they ask for details:
"I've sent the exact file locations and line numbers via email/DM to avoid exposing additional details publicly. Please check your notifications."

## If they confirm fix:
"Thank you for the quick response! Would you mind sharing a brief summary of the remediation so I can verify and close out my report?"

## If no response after 3 days:
"Following up on my security disclosure from [DATE]. Please let me know if you've had a chance to review or if you need additional information."

## If no response after 7 days:
"This is a final notice regarding security credentials exposed in your repository. If I don't hear back within 24 hours, I may need to escalate to protect your users."

---

*Templates for responsible disclosure. Use ethically.*
