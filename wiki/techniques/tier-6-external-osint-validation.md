---
title: "Tier 6: External OSINT Validation"
date: 2026-04-21
type: technique
status: active
visibility: public
related:
  - [[pre-disclosure-validation-protocol]]
  - [[github-osint-credential-discovery]]
  - [[certificate-transparency-logs]]
  - [[shodan-service-validation]]
  - [[git-history-forensics]]
created: 2026-04-21
updated: 2026-04-21
confidence: high
tags: [osint, validation, external-confirmation, bulletproof, tier-6]
---

# Tier 6: External OSINT Validation

**Beyond the repository: confirming credentials are actively deployed in production environments.**

---

## Purpose

Tier 1-5 validates the credential exists and *should* be active. **Tier 6 confirms it IS active** in the real world.

**Why this matters:**
- Repository code doesn't mean deployment
- Test configs can look like production
- Some repos are abandoned/archived
- External proof = undeniable evidence

**Response to dismissals:**
> "This is probably fake/test data"

**Your response:**
> "Certificate Transparency logs show this key's cert was issued 3 months ago and is still valid. The service is live on Shodan port 443."

---

## Tier 6 Validation Methods

### 6.1: Certificate Transparency (CT) Log Analysis

**Purpose:** Prove private key has issued/valid certificate

**When to use:** Any private key finding (RSA/EC)

**Method:**

```python
# Extract public key from private key
openssl rsa -in privatekey.key -pubout -out public.pem

# Calculate SPKI hash (base64)
openssl rsa -in privatekey.key -pubout -outform DER | openssl dgst -sha256 -binary | openssl base64
# Output: hkfO9q...1dQ=

# Search CT logs for matching certificate
# https://crt.sh/?q=hkfO9q...1dQ
# https://transparencyreport.google.com/https/certificates
```

**What you're looking for:**
- ✅ Certificate exists with matching public key
- ✅ Certificate is **valid** (not expired)
- ✅ Certificate issued by real CA (Let's Encrypt, DigiCert, etc.)
- ✅ Multiple certs = key reused (worse!)

**Evidence to capture:**
```
CT Log Entry:
- Serial: 00:ff:3a:4b:...
- Issuer: Let's Encrypt R3
- Validity: 2026-01-15 to 2026-04-15
- Domains: api.example.com, www.example.com
- Status: VALID
```

**Why this works:**
- Impossible to fake (CA-signed)
- Time-stamped (proves when deployed)
- Domain associated (shows scope)
- Maintainers can't dismiss as "test"

---

### 6.2: Live Service Enumeration (Shodan/Censys)

**Purpose:** Confirm service is publicly accessible

**When to use:** Server credentials, API keys, TLS configs

**Method for TLS Keys:**

```bash
# If you extracted domain from CT logs
DOMAIN=api.example.com

# Check if live on port 443
shodan host $DOMAIN
# OR
curl -s https://shodan.io/host/$DOMAIN

# Check SSL certificate
openssl s_client -connect $DOMAIN:443 -servername $DOMAIN < /dev/null | openssl x509 -noout -text

# Compare certificate with your key
openssl x509 -noout -modulus -in server.crt | openssl md5
openssl rsa -noout -modulus -in privatekey.key | openssl md5
# MATCH = Same key in use!
```

**What you're looking for:**
- ✅ Host is **online** and responding
- ✅ Port 443 open with TLS
- ✅ TLS handshake successful
- ✅ **Certificate matches your key**

**Evidence to capture:**
```
Shodan Result:
- Host: 203.0.113.45
- Port: 443 (HTTPS)
- TLS Version: 1.3
- Certificate CN: api.example.com
- Last Seen: 2026-04-21 (hours ago)
- Modulus Match: ✅ Confirmed
```

**Shodan Query Examples:**
```
ssl:"api.example.com"
ssl.cert.serial:00:ff:3a:4b:...
ssl.cert.issuer:"Let's Encrypt"
```

---

### 6.3: Historical Git Forensics

**Purpose:** Understand how/when credential was exposed

**When to use:** All findings - shows negligence pattern

**Deep Dive Commands:**

```bash
# Clone full history (not shallow)
git clone https://github.com/{owner}/{repo}.git
cd {repo}

# When was the file first added?
git log --follow --all --full-history -- "{filepath}" | tail -20

# Who added it?
git log --all --full-history -- "{filepath}" --pretty=format:"%h %an %ae %ad"

# Initial commit containing credential
git log --all --full-history -- "{filepath}" --reverse | head -1

# Was it ever removed?
git log --all --full-history -- "{filepath}" | wc -l
# 1 = never modified after initial commit

# Check commit message
FIRST_COMMIT=$(git log --all --full-history -- "{filepath}" --reverse --pretty=format:"%H" | head -1)
git show $FIRST_COMMIT --stat

# Check for previous security issues
git log --all --grep="security\|credential\|secret\|password\|key" --oneline | head -10
```

**What you're looking for:**
- ✅ **Age of exposure** (days/months since first commit)
- ✅ **Author identity** (core maintainer vs external contributor)
- ✅ **Commit message** (intentional vs accidental)
- ✅ **Previous incidents** (pattern of security issues)
- ✅ **Attempts to remove** (git history shows awareness)

**Evidence to capture:**
```
Git History:
- First Commit: 2021-03-15 (3 years ago)
- Author: John Doe <john@example.com> (Core maintainer, 500+ commits)
- Message: "Initial commit" (not marked as test)
- Last Modified: Never (exposed 3 years)
- Previous Security Issues: None found
```

**Why this works:**
- Shows duration of exposure
- Proves maintainer was author (not external contributor)
- Indicates negligence vs oversight
- Days since exposure = severity

---

### 6.4: Organization Attribution

**Purpose:** Confirm organization is real and active

**When to use:** All findings - shows real-world impact

**Method:**

```python
# WHOIS data
whois example.com
# Look for: Real registrant, not privacy-protected

# LinkedIn OSINT
site:linkedin.com "Example Corp" employees
# Count: 50+ employees = active org

# Business registration
https://opencorporates.com/
# Search: "Example Corp" + location

# GitHub org profile
https://github.com/{org}
# Check: Public profile, other repos, member count

# Website validation
curl -I https://example.com
# HTTP 200 = Active website

# DNS resolution
nslookup api.example.com
# Has A/AAAA records = deployed
```

**What you're looking for:**
- ✅ **Organization exists** (LLC/incorporated)
- ✅ **Has employees** (LinkedIn, Glassdoor)
- ✅ **Active website** (responds to HTTP)
- ✅ **Real domain** (not example.com placeholder)
- ✅ **GitHub presence** (org profile, multiple repos)

**Evidence to capture:**
```
Organization Validation:
- Name: Example Corp
- Status: Active (Delaware C-Corp, 2019)
- Employees: 50+ (LinkedIn)
- Website: example.com (HTTP 200)
- DNS: api.example.com → 203.0.113.45
- GitHub: Active since 2018, 12 repos
```

**Why this works:**
- Can't dismiss as "toy project"
- Shows real business impact
- Employees = potential users affected
- DNS records prove deployment

---

### 6.5: Associated Service Enumeration

**Purpose:** Find where credentials are being used

**When to use:** Database URIs, API tokens, cloud credentials

**Method for Database URIs:**

```bash
# Parse URI components
URI="postgresql://user:pass@prod-db.example.com:5432/app_db"
HOST=$(echo $URI | sed -n 's/.*@\([^:]*\):.*/\1/p')

# DNS lookup
nslookup $HOST
dig +short $HOST

# Port scan (limited, non-intrusive)
nmap -Pn -p 5432 --open $HOST
# OR check Shodan
shodan host $HOST

# Check for web interface (common with DBs)
curl -I http://$HOST:8080
curl -I https://$HOST

# Reverse DNS
host $HOST
```

**Method for AWS Keys:**

```bash
# Extract account info from access key
# AKIA... = AWS Access Key ID

# Check CloudTrail (if you have creds - DON'T)
# Instead, check public resources:

# S3 bucket enumeration (common mistake)
aws s3 ls s3://{bucket-name} --no-sign-request 2>/dev/null
# (only if bucket is public)

# Check for public cloud resources via Shodan
shodan search "X-Amz-Bucket-Owner-Id"
```

**What you're looking for:**
- ✅ **DNS resolves** (shows infrastructure exists)
- ✅ **Port responding** (5432 for PostgreSQL)
- ✅ **Reverse DNS** matches service type
- ✅ **No authentication error** (open port)

**Evidence to capture:**
```
Service Enumeration:
- Host: prod-db.example.com
- DNS: Resolves to 203.0.113.78
- Port 5432: OPEN (PostgreSQL)
- Banner: PostgreSQL 13.2
- Last Activity: Shodan scan 2 days ago
```

**Why this works:**
- Host online = credential usable
- Port open = no firewall blocking
- Banner version = specific target
- Can't claim "not deployed"

---

### 6.6: Threat Intelligence Cross-Reference

**Purpose:** Check if credential has been leaked elsewhere

**When to use:** High-value credentials (production keys)

**Method:**

```bash
# Check Have I Been Pwned for associated email/domain
https://haveibeenpwned.com/domain/example.com

# Check for repository in public breach databases
# (Don't have credentials, just metadata)

# Search for exposed credential on Pastebin/hastebin
google: "api.example.com" site:pastebin.com

# Check Shodan history
shodan host --history 203.0.113.45
# Shows if service has been up consistently

# Certificate transparency history
crt.sh/?q=example.com&output=json&exclude=expired
```

**What you're looking for:**
- ⚠️ **Already leaked** (pastebin, breaches)
- ✅ **Consistent uptime** (legitimate service)
- ✅ **No prior reports** (you're first = bonus points)
- ⚠️ **Multiple CT entries** (cert renewed frequently)

**Evidence to capture:**
```
Threat Intel:
- Past Breaches: None found
- Pastebin: No matches
- CT History: 3 certificates in last year (frequent rotation)
- Shodan Uptime: 99.2% (legitimate production service)
```

---

## Tier 6 Evidence Package Template

```markdown
## Tier 6 External Validation Report

### Credential Summary
- Repository: {owner}/{repo}
- File: {path}
- Type: {private_key/db_uri/api_token}

### 6.1: Certificate Transparency
- CT Log Entry: {YES/NO}
- Serial Number: {sn}
- Issuer: {CA}
- Validity: {start} to {end}  
- Domains: {list}
- Status: {VALID/EXPIRED}

### 6.2: Live Service Enumeration
- Host: {ip/domain}
- Port: {port}
- Shodan Last Seen: {date}
- Modulus Match: {YES/NO}
- Service Confirmed: {YES/NO}

### 6.3: Git History Forensics
- First Commit: {date}
- Exposure Duration: {X years/months}
- Author: {name} ({core maintainer/contributor})
- Previous Security Issues: {count}

### 6.4: Organization Attribution
- Legal Entity: {YES/NO}
- Employees: {count}
- Active Website: {YES/NO}
- DNS Records: {YES/NO}

### 6.5: Associated Service Enumeration
- DNS Resolves: {YES/NO}
- Port Open: {YES/NO}
- Banner Detected: {version}
- Last Activity: {date}

### 6.6: Threat Intelligence
- Prior Breaches: {count}
- Public Exposure: {YES/NO}
- Shodan Uptime: {percent}

### Validation Confidence
- Tier 6 Score: {xx}/30 points
- External Proof: {STRONG/MODERATE/WEAK}
- Recommendation: {PROCEED WITH DISCLOSURE/GATHER MORE}

### Notes
{special considerations}
```

---

## Tier 6 Scoring

Add to Pre-Disclosure Validation Protocol:

| Tier | Max Points | Threshold |
|------|-----------|-----------|
| 1: Automated | 20 | >= 15 |
| 2: Crypto | 30 | >= 25 |
| 3: Context | 30 | >= 25 |
| 4: Impact | 20 | >= 15 |
| 5: Package | 10 | >= 8 |
| **6: External** | **30** | **>= 20** |
| **TOTAL** | **140** | **>= 110 READY** |

### Tier 6 Specific Points

| Method | Points | Required |
|--------|--------|----------|
| CT Log match | 10 | Any key |
| Live service confirmed | 10 | Any server |
| Exposure duration > 6mo | 5 | All |
| Organization verified | 3 | All |
| Threat Intel clean | 2 | All |

**Updated Thresholds:**
- **130-140:** DEFINITIVE - Multiple external proofs
- **110-129:** STRONG - CT logs or live service confirmed  
- **90-109:** PROBABLE - Some external validation
- **75-89:** QUESTIONABLE - Needs more external proof

---

## Real Example: ettfemnio Improved

### Disclosure That Would Survive "ai-slop"

```markdown
## VERIFIED: Production RSA-2048 Private Key with Live TLS Certificate

### Cryptographic Proof
```bash
$ openssl rsa -in privatekey.key -check -noout
RSA key ok

$ openssl rsa -in privatekey.key -text -noout | head -2
Private-Key: (2048 bit, 2 primes)
Modulus: 00:bb:b2:0f:...
```

### Certificate Transparency Evidence
**CT Log Match Found:**
- Search: crt.sh/?id=12345678
- Serial: 00:ff:3a:2c:8b:...
- Issuer: Let's Encrypt R3  
- Valid: 2026-01-15 to 2026-04-15
- **Domain:** dbd-server.example.com
- **Status:** VALID

### Live Service Confirmation
```bash
$ openssl s_client -connect dbd-server.example.com:443 < /dev/null | openssl x509 -noout -modulus | openssl md5
(stdin)= d41d8cd98f00b204e9800998ecf8427e  # MATCHES KEY
```

**Shodan Confirmation:**
- Host: 203.0.113.45
- Port: 443 (HTTPS) - OPEN
- Last Seen: 2 hours ago
- TLS Version: 1.3
- Certificate: VALID (matches above)

### Production Usage (Source Code)
```typescript
// src/server.ts:127
const httpsServer = https.createServer({
    key: fs.readFileSync(path.join('private', 'privatekey.key')),
    cert: fs.readFileSync(path.join('private', 'cert.crt')),
}, app)
httpsServer.listen(443, '0.0.0.0')  // PUBLIC INTERNET
```

### Exposure Duration
**Git History:**
- First Commit: 2021-02-05 (2+ years exposed)
- Author: ettfemnio (repository owner)
- Never Modified: Still exposed in latest commit

### This Is NOT Test Data
- ✅ Certificate issued by Let's Encrypt (real CA)
- ✅ Service is live on public internet
- ✅ TLS handshake succeeds with this exact key
- ✅ Port 443 open on public IP
- ✅ Repository owner committed the key

### Risk
Anyone with this repository can:
1. Decrypt HTTPS traffic to dbd-server.example.com
2. Impersonate the server
3. Perform MITM attacks

**This key MUST be rotated immediately.**
```

**Why This Works:**
1. **Leads with cryptographic proof** - OpenSSL validation
2. **CT log entry** - Independent verification impossible to fake
3. **Live service confirmation** - Not "maybe deployed"
4. **Exact match proof** - Modulus comparison
5. **Exposure duration** - Git history shows negligence
6. **Conclusive statement** - "NOT Test Data" with proof

Impossible to dismiss as "ai-slop" - evidence is external, verifiable, and overwhelming.

---

## Integration with Tier 1-5

**Tier 1-5:** Prove credential exists in repository
**Tier 6:** Prove credential is deployed and active

**When Tier 6 is Essential:**
- 🔴 **Private keys** - Must have CT logs or live confirmation
- 🟠 **Production DBs** - Must resolve DNS, see open ports
- 🟡 **API tokens** - Nice to have (harder to verify without using)

**When Tier 6 is Optional:**
- Dev/test credentials
- Obvious test fixtures
- Archived repos (no active deployment)

---

## Tools Required

| Tool | Purpose | Install |
|------|---------|---------|
| `openssl` | Crypto validation | Built-in |
| `dig`/`nslookup` | DNS validation | Built-in |
| `shodan` | Service enumeration | `pip install shodan` |
| `crt.sh` | CT logs | Web API |
| `whois` | Domain attribution | `apt install whois` |
| `nmap` | Port scanning | Optional (use carefully) |

---

## Related

- [[pre-disclosure-validation-protocol]] - Tiers 1-5
- [[maintainer-response-log]] - Real response patterns
- [[github-osint-credential-discovery]] - Discovery method
- [[certificate-transparency-logs]] - Deep dive on CT

---

*Last Updated: 2026-04-21*
*Tier 6 unlocks: Bulletproof disclosures*