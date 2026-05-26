---
title: Credential Exposure Patterns Comparison
type: comparison
status: active
visibility: public
sources:
  - docs/PRODUCTION_IMPACT_ANALYSIS_20260421.md
  - docs/IMPACT_ASSESSMENT_20260421.md
related:
  - [[github-osint-credential-discovery]]
  - [[osint-pattern-filtering]]
  - [[private-key-crypto]]
  - [[database-uri-security]]
  - [[api-token-lifecycle]]
created: 2026-04-21
updated: 2026-04-21
confidence: high
tags: [security, comparison, credentials, exposure, patterns]
---

# Credential Exposure Patterns

**Comparative analysis of different credential types discovered via OSINT, their risk profiles, and detection strategies.**

## Overview

Different credential types exhibit distinct exposure patterns, risk characteristics, and detection difficulty. Understanding these differences enables more effective hunting and triage.

## Pattern Comparison

### 1. Private Keys (RSA/EC/Ed25519)

**Format:**
```
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7sg9glbYg6hX5
[... 40-50 lines ...]
-----END PRIVATE KEY-----
```

**Discovery Pattern:**
- **Search:** `extension:key path:private`, `filename:id_rsa`
- **Entropy:** Very high (5.0+) - Cryptographic randomness
- **File Size:** ~1,700 bytes (RSA-2048)

**Risk Assessment:**

| Factor | Severity | Notes |
|--------|----------|-------|
| **Impact** | 🔴 CRITICAL | Complete cryptographic compromise |
| **Exploitation** | Immediate | Anyone can use exposed private key |
| **Rotation** | Very Hard | Requires replacing certs everywhere |
| **Detection** | Easy | High entropy, distinct format |
| **Recovery** | Weeks | Certificate chain updates |

**Real Examples Found:**
- **ettfemnio/dbd-server:** Production TLS key hardcoded in HTTPS server
- **totaljs/superadmin:** SSL key deployed to managed servers

**Mitigation:**
- Use environment variables: `process.env.SSL_KEY_PATH`
- `gitignore`: `*.key`, `private/`, `id_rsa`
- Hardware security modules (HSM) for production

---

### 2. Database URIs

**Format:**
```
postgresql://user:password@host:5432/database
mongodb+srv://user:pass@cluster.mongodb.net/db
mysql://user:pass@host:3306/db
```

**Discovery Pattern:**
- **Search:** `postgresql://`, `mongodb+srv://`, `DATABASE_URL`
- **Entropy:** Low-Moderate (3.0-4.0) - Contains dictionary words
- **File Size:** Single line

**Risk Assessment:**

| Factor | Severity | Notes |
|--------|----------|-------|
| **Impact** | 🟠 HIGH | Full database access |
| **Exploitation** | Immediate | URI contains everything needed |
| **Rotation** | Medium | One DB user password change |
| **Detection** | Hard | Looks like config, mixed with docs |
| **Recovery** | Hours | Password change + connection reset |

**Real Examples Found:**
- Multiple repositories with PostgreSQL URIs in `.env` or config files
- Often accompanied by `sslmode=require` (won't save you if exposed)

**Mitigation:**
- Connection string builders (not hardcoded strings)
- Secret management: AWS Secrets Manager, HashiCorp Vault
- Network-level: IP allowlists (not password-only)

---

### 3. API Tokens

**Format (Examples):**
```
GitHub: ghp_xxxxxxxx...xxxxxxxx
Anthropic: sk-ant-xxxxxxxx...xxxxxxxx
Stripe: sk_live_xxxxxxxx...xxxxxxxx  
Google: AIzaSyxxxxxxxx...xxxxxxxx
```

**Discovery Pattern:**
- **Search:** `ghp_`, `sk_live_`, `AIzaSy`, `^sk-ant`
- **Entropy:** Very high (4.5+) - Random token generation
- **Prefix Detection:** Distinct prefixes make easy targets

**Risk Assessment:**

| Factor | Severity | Notes |
|--------|----------|-------|
| **Impact** | 🟠-🔴 VARIES | Depends on token scope |
| **Exploitation** | Immediate | Bearer tokens work anywhere |
| **Rotation** | Easy | Single revoke/regenerate |
| **Detection** | Very Easy | Fixed prefixes = grep targets |
| **Recovery** | Minutes | Revoke via API |

**Real Examples Found:**
- GitHub PATs in test fixtures (false positive: atuin #3438)
- GitHub PAT + PostgreSQL combo (codename-co/devs - critical)

**Mitigation:**
- **Short-lived tokens** - Expire automatically
- **Scope restriction** - Least-privilege access
- **GitHub Secret Scanning** - Automatic detection (but not all providers)
- **Pre-commit hooks** - gitleaks, detect-secrets

---

## Comparative Analysis

### Detection Difficulty

```
Easiest to Detect                     Hardest to Detect
─────────────────────────────────────────────────────────
API Tokens (fixed prefixes)    →    Database URIs
        ↓                              ↓
Private Keys (high entropy)    →    Config files
        ↓                              ↓
AWS Keys (AKIA prefix)       →    Custom secrets
```

**Reasoning:**
- **API tokens:** Fixed prefixes = instant regex hits
- **Private keys:** High entropy flags in search, but need verification
- **DB URIs:** Look like config, easy to miss
- **Custom secrets:** No patterns = nearly impossible

### Risk vs Exploitability

```
High Risk, Easy Exploit (CRITICAL)
├── Private keys          [ Production TLS, SSH keys ]
├── Scoped admin tokens   [ GitHub PAT + DB combo ]
└── Root database URIs    [ Production DB with write access ]

Medium Risk, Easy Exploit (HIGH)
├── API tokens (limited scope)  [ Single service access ]
├── Read-only DB URIs           [ Data exfiltration ]
└── Development credentials    [ Lateral movement ]

Low Risk, Hard Exploit (LOW)
├── Test fixture tokens       [ Valid format, fake data ]
├── Example documentation     [ Clearly marked ]
└── Expired/Revoked tokens    [ Already invalid ]
```

### Hunter Priority

**Tier 1 (Immediate Disclosure):**
1. Private keys in `private/` directories
2. Production API tokens with admin scope
3. Cloud provider keys (AWS, GCP, Azure)

**Tier 2 (High Priority):**
4. Database URIs with write access
5. TLS certificates with private keys
6. CI/CD tokens (GitHub Actions, GitLab CI)

**Tier 3 (Low Priority):**
7. Read-only database URIs
8. Development tokens
9. Test fixture secrets (verify first!)

## Pattern-Specific Detection

### Private Keys

**What to Look For:**
```bash
# File patterns
*.key, *.pem, id_rsa, id_ed25519

# Content markers
-----BEGIN PRIVATE KEY-----
-----BEGIN RSA PRIVATE KEY-----
-----BEGIN OPENSSH PRIVATE KEY-----

# Locations
private/, secrets/, .ssh/, /etc/ssl/
```

**Verification Steps:**
1. `openssl rsa -in file.key -check -noout`
2. Check if used in `https.createServer()` or SSH auth
3. Verify key length (2048+ bits for RSA)

### Database URIs

**What to Look For:**
```bash
# Connection strings
postgresql://, mysql://, mongodb+srv://
redis://, amqps://, smtp://

# Environment patterns
DATABASE_URL=, DB_URI=, MONGO_URI=
```

**Verification Steps:**
1. Check if host is `localhost` or remote
2. Look for `sslmode=require` or similar
3. Check if credentials work (careful!)

### API Tokens

**What to Look For:**
```bash
# Fixed prefixes
github_pat_, ghp_, github_token_
sk_live_, sk_test_ (Stripe)
AIzaSy (Google)
hf_ (Hugging Face)
```

**Verification Steps:**
1. Check token format (length, charset)
2. Verify against provider documentation
3. **NEVER** test in production (rate limits, detection)

## Lessons from April 2026 Hunt

### What Worked

**Highest Yield:** `extension:key path:private`
- 2 real private keys in 5 checked files (40% hit rate)
- Zero false positives after verification

**Moderate Yield:** `DATABASE_URL postgres`
- Multiple hits, but 60% false positive rate
- Filter by `created:>date` for recent commits

**Low Yield:** `ghp_ created:>2025-04-01`
- Mostly test fixtures
- Need additional context filtering

### What Didn't Work

- **Broad searches** without date filtering (too much noise)
- **Single-layer filtering** (keywords-only or entropy-only)
- **Skipping local verification** (reported test data)

## Recommendations for Hunters

### For New OSINT Practitioners

1. **Start with private keys** - High impact, easy detection
2. **Always verify before reporting** - Clone and check usage
3. **Document your methodology** - Reproducible results
4. **Follow responsible disclosure** - 7-day standard timeline

### For Security Teams

1. **Monitor your own repos** - Weekly scans for internal code
2. **Implement pre-commit hooks** - gitleaks, detect-secrets
3. **Use secret management** - Vault, AWS Secrets Manager
4. **Regular rotation** - Even "safe" creds should rotate

## Related Patterns

- [[private-key-crypto]] - Deep dive on key management
- [[database-uri-security]] - Securing connection strings
- [[api-token-lifecycle]] - Token generation and revocation

## References

- **Case Study:** [[osint-credential-discovery-case-study]]
- **Filtering Strategy:** [[osint-pattern-filtering]]
- **Tool Documentation:** [[osint-security-toolkit]]

---

*Last Updated: 2026-04-21*
