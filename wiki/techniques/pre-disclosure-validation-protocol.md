---
title: "Pre-Disclosure Validation Protocol"
date: 2026-04-21
type: technique
status: active
visibility: public
related:
  - [[github-osint-credential-discovery]]
  - [[osint-pattern-filtering]]
  - [[maintainer-response-log]]
  - [[credential-exposure-patterns]]
created: 2026-04-21
updated: 2026-04-21
confidence: high
tags: [security, validation, disclosure, quality-assurance, osint]
---

# Pre-Disclosure Validation Protocol

**Preventing "ai-slop" dismissals through rigorous evidence collection.**

Created in response to the ettfemnio/dbd-server maintainer dismissal (Issue #23), this protocol establishes minimum requirements before contacting any maintainer.

---

## The Problem

**What Happened:**
- ettfemnio dismissed finding as "ai-slop 🤮"
- Archived repo (acknowledged) but no key rotation (incomplete)
- Finding was **legitimate** - verified with OpenSSL + source code

**Root Cause:** Maintainer fatigue from AI-generated spam reports

**Solution:** Evidence so overwhelming that dismissal is impossible

---

## Validation Tiers

### Tier 1: Automated Screening (Required)

**Purpose:** Eliminate obvious false positives

| Check | Tool/Method | Threshold | Fail Action |
|-------|-------------|-----------|-------------|
| **Entropy** | `math.entropy()` | > 3.5 | Discard |
| **Keyword Filter** | Skip list | 0 matches | Proceed |
| **Pattern Match** | Regex | Full match required | Discard |
| **File Extension** | Name patterns | Listed extensions | Proceed |

**Example Skip List:**
```python
SKIP_KEYWORDS = [
    'example', 'placeholder', 'your_', 'test', 'sample',
    'localhost', '127.0.0.1', 'fake', 'dummy', 'changeme',
    'todo', 'fixme', 'xxx', '***'
]
```

**Evidence to Capture:**
- [ ] Entropy calculation
- [ ] Pattern match confirmation
- [ ] File path screenshot

---

### Tier 2: Cryptographic Verification (CRITICAL)

**Purpose:** Prove the credential is real, not a placeholder

#### For Private Keys

```bash
# 1. Validate key format
openssl rsa -in privatekey.key -check -noout
# Expected: "RSA key ok"

# 2. Check key size (should be 2048+ bits)
openssl rsa -in privatekey.key -text -noout | head -1
# Expected: "Private-Key: (2048 bit)"

# 3. Calculate modulus (for CSR matching)
openssl rsa -in privatekey.key -modulus -noout
# Save: Modulus=ABC123...

# 4. Check associated certificate/CSR
openssl req -in cert.csr -modulus -noout
# Compare: Must match key modulus
```

**Evidence to Capture:**
- [ ] OpenSSL validation output (screenshot/text)
- [ ] Key size confirmation
- [ ] Modulus match with CSR (if applicable)

#### For Database URIs

```bash
# Parse components
echo "$DB_URI" | grep -E '^postgresql://[^:]+:[^@]+@[^:]+:\d+/[^?]+'
# Must match: postgres://user:pass@host:port/db

# Check if localhost vs remote
echo "$DB_URI" | grep -vE 'localhost|127\.0\.0\.1'
# Should NOT match localhost

# Verify password strength
PASSWORD=$(echo "$DB_URI" | sed 's/.*:\/\/[^:]+:\([^@]*\)@.*/\1/')
if [ ${#PASSWORD} -lt 12 ]; then echo "WEAK_PASSWORD"; fi
```

**Evidence to Capture:**
- [ ] URI components (redacted password)
- [ ] Host (localhost vs remote)
- [ ] SSL mode (sslmode=require?)

#### For API Tokens

```bash
# Verify format against provider documentation
# GitHub: ghp_[36 chars of alnum]
echo "$TOKEN" | grep -E '^ghp_[a-zA-Z0-9]{36}$'

# Stripe: sk_live_[24+ chars]
echo "$TOKEN" | grep -E '^sk_live_[a-zA-Z0-9]{24,}$'

# Check prefix validity
if [[ "$TOKEN" =~ ^ghp_ ]]; then ...
elif [[ "$TOKEN" =~ ^sk_live_ ]]; then ...
else echo "UNKNOWN_PREFIX"; fi
```

**Evidence to Capture:**
- [ ] Format validation (regex match)
- [ ] Prefix verification
- [ ] Length check

---

### Tier 3: Contextual Analysis (CRITICAL)

**Purpose:** Prove production usage, not test fixture

#### Repository Context

**Clone and analyze:**

```bash
# 1. Clone repository (shallow = fast)
git clone --depth 1 https://github.com/{owner}/{repo}.git

# 2. Check file location
find . -path "*/test/*" -o -path "*/tests/*" -o -path "*/fixture/*"
# File NOT in test directories? PROCEED

# 3. Check .gitignore
if grep -E "\.key|private/" .gitignore; then
    echo "EXCLUDED_IN_GITIGNORE"
fi

# 4. Check for documentation markers
if grep -i "example\|test\|demo" "$FILE_PATH"; then
    echo "POSSIBLE_TEST_FIXTURE"
fi
```

**Evidence to Capture:**
- [ ] File path (not in test/)
- [ ] .gitignore status
- [ ] No "example"/"test" markers

#### Source Code Context

**Find how the credential is used:**

```bash
# Search for references to the credential file
grep -r "privatekey.key\|superadmin.key" --include="*.js" --include="*.ts" --include="*.py"

# Look for HTTPS/SSH/Auth configuration
grep -rE "https\\.createServer|createServer.*key|fs\\.readFileSync.*key"

# Check for production environment checks
grep -rE "process\\.env\\.NODE_ENV|if.*production|NODE_ENV.*production"
```

**Red Flags (Test Data):**
- ❌ In `test/` directory
- ❌ In `__tests__/` or `spec/`
- ❌ Referenced in `.test.js` file
- ❌ Contains "example", "fixture", "mock"

**Green Flags (Production):**
- ✅ Used in `server.js` or `app.js`
- ✅ Deployed with HTTPS configuration
- ✅ Environment variable path construction
- ✅ README mentions production deployment

**Evidence to Capture:**
- [ ] Source code showing usage (screenshot/snippet)
- [ ] Line numbers
- [ ] Production configuration context

---

### Tier 4: Impact Assessment (Required for Severity)

**Purpose:** Quantify the actual risk

#### Deployment Impact

```bash
# GitHub stars (wider usage = higher impact)
curl -s https://api.github.com/repos/{owner}/{repo} | jq '.stargazers_count'

# Forks (more copies = harder to fix)
curl -s https://api.github.com/repos/{owner}/{repo} | jq '.forks_count'

# Last updated (active project?)
curl -s https://api.github.com/repos/{owner}/{repo} | jq '.updated_at'
```

#### Technical Impact

| Credential Type | Direct Impact | Exploit Difficulty |
|-----------------|---------------|-------------------|
| Private Key + HTTPS | MITM, Impersonation | Copy + Use |
| Database URI | Data breach, RCE | Connect |
| API Token | Service abuse | HTTP Request |
| SSH Key | Server access | SSH Connect |

**Evidence to Capture:**
- [ ] GitHub stars/forks
- [ ] Last commit date
- [ ] Deployment scope (single vs multi-tenant)

---

### Tier 5: Evidence Package (Required for Disclosure)

**Purpose:** Create undeniable proof bundle

#### Required Documentation

| Item | Format | Description |
|------|--------|-------------|
| **Finding Location URL** | Link | Direct GitHub URL to file |
| **OpenSSL Validation** | Screenshot | `RSA key ok` output |
| **Key Modulus** | Text | Full modulus or truncated |
| **CSR Modulus** | Text | For comparison (if exists) |
| **Source Code Usage** | Snippet | 5-10 lines showing usage |
| **File Path** | Text | Relative to repo root |
| **Repository Stats** | Screenshot | Stars, forks, last updated |
| **Risk Assessment** | Text | Specific technical risks |

#### Optional Enhancements

| Enhancement | Purpose |
|-------------|---------|
| **Diff with similar keys** | Show this is real, not test |
| **Deployment evidence** | Actual users vs template |
| **Associated services** | SSL cert transparency logs |

---

## Confidence Scoring

### Calculate Disclosure Readiness

```python
def calculate_confidence(findings):
    score = 0
    
    # Tier 1: Automated (20 points)
    if findings['entropy'] > 3.5: score += 5
    if findings['pattern_match']: score += 5
    if findings['no_skip_keywords']: score += 5
    if findings['valid_extension']: score += 5
    
    # Tier 2: Crypto Verification (30 points)
    if findings['openssl_valid']: score += 10
    if findings['key_size_2048_plus']: score += 5
    if findings['modulus_match']: score += 10
    if findings['associated_cert']: score += 5
    
    # Tier 3: Context (30 points)
    if findings['not_in_test_dir']: score += 10
    if findings['production_usage']: score += 15
    if findings['real_deployment']: score += 5
    
    # Tier 4: Impact (20 points)
    if findings['stars'] > 10: score += 5
    if findings['active_repo']: score += 5
    if findings['clear_impact']: score += 10
    
    return score

# Thresholds
if score >= 90:  return "READY - Post immediately"
if score >= 75:  return "PROBABLE - Gather more evidence"
if score >= 60:  return "QUESTIONABLE - Needs verification"
return "REJECT - Insufficient evidence"
```

### Minimum Viable Disclosure (MVD)

**Must have (100% required):**
- ✅ OpenSSL validation OR pattern match confirmation
- ✅ Source code showing production usage
- ✅ Line numbers
- ✅ Risk assessment

**Should have (strongly preferred):**
- ✅ Modulus match (for keys)
- ✅ Repository context (stars, activity)
- ✅ Screenshot of file location

**Nice to have (increases confidence):**
- Associated certificate
- Deployment documentation
- Multiple instances

---

## Template: Evidence Collection Checklist

```markdown
## Disclosure Evidence Package

### Finding Summary
- **Repository:** {owner}/{repo}
- **File:** {path}
- **Type:** {private_key/database/api_token}
- **Discovery Date:** YYYY-MM-DD

### Tier 1: Automated Screening
- [ ] Entropy > 3.5: {value}
- [ ] No skip keywords: confirmed
- [ ] Pattern matches: {regex_used}

### Tier 2: Cryptographic Verification
- [ ] OpenSSL validation: {screenshot/text}
- [ ] Key size: {bits} (2048+ required)
- [ ] Modulus: {value} (truncated acceptable)
- [ ] CSR Match: {yes/no/NA}

### Tier 3: Contextual Analysis
- [ ] Local clone: {yes}
- [ ] File location: {not_in_test}
- [ ] Source usage: {snippet_lines}
- [ ] Production context: {yes/no}

### Tier 4: Impact Assessment
- [ ] Stars: {count}
- [ ] Forks: {count}
- [ ] Last updated: {date}
- [ ] Risk level: {critical/high/medium}

### Tier 5: Evidence Package
- [ ] File URL captured
- [ ] OpenSSL output recorded
- [ ] Source snippet documented
- [ ] Risk assessment written

**Confidence Score:** {xx}/100
**Recommendation:** {POST / GATHER / REJECT}

**Notes:** {any_special_considerations}
```

---

## Real Examples

### Good Disclosure (High Confidence): ettfemnio/dbd-server

**What We Had:**
```
✅ OpenSSL: RSA key ok (verified)
✅ Key size: 2048 bits (standard)
✅ Source: src/server.ts line 127
✅ Usage: https.createServer({key:...}).listen(443)
✅ Not in test directory
✅ Stars: 18 (low but real)

Score: 95/100 → READY
```

**Why Dismissed Anyway:**
- Maintainer assumed "ai-slop" without reading
- Evidence was strong but not presented as "proof"
- No associated cert verification shown in disclosure

**Lesson:** Lead with cryptographic verification, not search method

### Better Presentation

**Instead of:**
```
I found a private key using GitHub search: extension:key path:private
```

**Lead with:**
```
## VERIFIED: Production RSA-2048 Private Key Exposed

OpenSSL validation:
$ openssl rsa -in privatekey.key -check -noout
→ RSA key ok

Production usage (src/server.ts:127):
const httpsServer = https.createServer({
    key: fs.readFileSync('private/privatekey.key'),
    cert: fs.readFileSync('private/cert.crt'),
}, app)
httpsServer.listen(443, '0.0.0.0')  // PUBLIC HTTPS

This is NOT a test fixture. Key is deployed on port 443.
```

---

## Related

- [[maintainer-response-log]] - Real-world responses
- [[osint-pattern-filtering]] - Why we filter
- [[github-osint-credential-discovery]] - Full method

---

*Last Updated: 2026-04-21*
*Response to: ettfemnio Issue #23 "ai-slop" dismissal*
