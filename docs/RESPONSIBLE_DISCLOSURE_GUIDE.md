# Responsible Disclosure Templates

## GitHub Discussion Template

### Subject: Security Alert - Exposed Credentials in [REPO_NAME]

\`\`\`
Hi [MAINTAINER_TEAM],

I hope this message finds you well. I'm reaching out as a security researcher 
who discovered exposed credentials in your repository that could pose a security risk.

## Summary
During an automated security audit of open-source projects, I identified 
potentially sensitive credentials exposed in your codebase:

**Repository:** [REPO_URL]
**File:** [FILE_PATH]
**Discovery Date:** [DATE]

## Affected Credentials
- **Type:** [API_KEY / DATABASE_URL / TOKEN]
- **Location:** Line(s) [LINE_NUMBERS]
- **Potential Impact:** [DATA_EXPOSURE / UNAUTHORIZED_ACCESS / etc.]

## Recommended Actions
1. **Immediately rotate/revoke** the exposed credential
2. **Remove** the credential from the repository history
3. **Review access logs** for unauthorized usage
4. **Implement** secret scanning (GitHub Advanced Security or tools like TruffleHog)
5. **Add** \`.env\` files to \`.gitignore\` if not already present

I'm happy to discuss this further via private channels if preferred.

Best regards,
Cameron Warren
[Your Contact Info]
\`\`\`

## Severity Classification

### 🔴 CRITICAL
- **Live AWS keys** with active permissions
- **Production database URLs** with read/write access
- **Private keys** (RSA, EC, SSH)

**Timeline:** Immediate, 24-48 hour response

### 🟠 HIGH
- **Test/Sandbox credentials** but valid
- **Development API keys** that could be escalated

**Timeline:** 7-day disclosure

### 🟡 MEDIUM
- **Example/demo credentials** in documentation
- **Expired/Invalid tokens**

**Timeline:** 14-day disclosure

## Disclosure Process

### Before Reaching Out:
- [ ] Verify credential is live/real (not placeholder)
- [ ] Document exact location and impact
- [ ] Prepare remediation steps

### Contact Methods (in order):
1. GitHub Security Advisory (Private)
2. GitHub Discussion (Public but professional)
3. Repository Issues
4. Direct Email

## Legal/Ethical Guidelines

### ✅ DO:
- Verify credentials before reporting
- Be respectful and professional
- Give reasonable time to fix

### ❌ DON'T:
- Access or use discovered credentials
- Share credentials with others
- Publicly shame maintainers

---
"ENDOFFILE

cat docs/RESPONSIBLE_DISCLOSURE_GUIDE.md
