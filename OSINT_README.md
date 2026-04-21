# 🔍 OSINT Secret Monitoring Suite

Complete automated monitoring system for exposed credentials across GitHub and industrial control systems.

---

## 📦 Components

### 1. GitHub Secret Monitor (`.github/workflows/secret-monitor.yml`)

**Daily GitHub Action** that scans for exposed secrets in public code.

**Scans for:**
- AWS Access Keys
- Google API Keys  
- Database passwords (MySQL, MongoDB, PostgreSQL)
- Private Keys (RSA, OpenSSH, EC, PGP)
- API Keys & Secrets
- Slack & Discord tokens
- Stripe keys (live & test)
- Firebase URLs
- Generic bearer tokens

**Runs:** Daily at 09:00 UTC

**Outputs:**
- `reports/README.md` - Latest report
- `reports/history/YYYY-MM-DD-report.md` - Historical reports

**Setup:**
1. Set `GITHUB_PAT` secret in repo settings
2. Action runs automatically
3. Reports auto-committed to repo

---

### 2. TruffleHog Config (`trufflehog-config.yml`)

Configuration for [TruffleHog OSS](https://github.com/trufflesecurity/trufflehog) with custom detectors for:
- High-entropy secrets
- Cloud provider keys
- Database connection strings
- Private keys
- CI/CD tokens

**Usage:**
```bash
# Install TruffleHog
brew install trufflesecurity/trufflehog/trufflehog

# Scan current directory
trufflehog filesystem . --config trufflehog-config.yml

# Scan specific repo
trufflehog git https://github.com/user/repo --config trufflehog-config.yml
```

---

### 3. TruffleHog + GitHub Scanner (`scripts/osint/trufflehog_scanner.py`)

**One-shot scanner** that:
1. Searches GitHub for repos with potential secrets
2. Clones repos (shallow clone, depth=20)
3. Runs TruffleHog DeepScan
4. Generates JSON report

**Usage:**
```bash
export GITHUB_PAT="github_pat_11..."
python scripts/osint/trufflehog_scanner.py
```

**Target Patterns:**
- AWS keys (`AKIA`)
- Google API (`AIzaS`)
- MongoDB URIs
- Stripe keys
- Slack tokens
- GitHub tokens

---

### 4. Shodan ICS Scanner (`scripts/osint/collect.py`)

**Industrial Control System reconnaissance** - scans for SCADA/PLC devices on public internet.

**Protocols:**
| Protocol | Port | Use Case |
|----------|------|----------|
| Modbus | 502 | Factory automation |
| BACnet | 47808 | Building control |
| DNP3 | 20000 | Power grid/utility |
| S7 | 102 | Siemens PLCs |

**⚠️ These should NEVER be on public internet!**

**Usage:**
```bash
export SHODAN_API_KEY="your_shodan_api_key_here"  # or put it in .env (gitignored)
python -m scripts.osint.collect --limit 1000
```

**Full Pipeline:**
```bash
cd scripts/osint
./run_all.sh
```

---

## 🚀 Quick Start

### GitHub Secret Monitoring (Automated)
```bash
# Set secret in repo settings
echo "GITHUB_PAT=github_pat_11..." >> .env

# Push to trigger workflow
git push origin main
```

### TruffleHog Scan (One-time)
```bash
# Install
curl -sSfL https://install.trufflehog.org | sh

# Run
trufflehog filesystem . --config trufflehog-config.yml
```

### Shodan ICS Scan (Monthly)
```bash
export SHODAN_API_KEY="your_key"
python -m scripts.osint.collect
```

---

## 📊 Report Examples

### GitHub Secret Report
```markdown
# 🔒 Secret Monitoring Report

**Total Findings:** 1,373,184

| Pattern | Count | Severity |
|---------|-------|----------|
| API Keys | 1,024,512 | 🔴 CRITICAL |
| Database Passwords | 182,528 | 🔴 CRITICAL |
| AWS Access Keys | 166,144 | 🔴 CRITICAL |
```

### TruffleHog Report
```json
{
  "scan_time": "2026-04-20T12:00:00",
  "tool": "trufflehog",
  "total_findings": 47,
  "findings": [...]
}
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Required For | Description |
|----------|--------------|-------------|
| `GITHUB_PAT` | GitHub Monitor, TruffleHog Scanner | GitHub Personal Access Token |
| `SHODAN_API_KEY` | ICS Scanner | Shodan API key |

### GitHub PAT Permissions

Required scopes:
- `public_repo` or `repo` (for private repos)
- `read:org` (optional)

---

## 📈 Historical Tracking

All reports are timestamped and stored:

```
reports/
├── README.md                    # Latest report
├── history/
│   ├── 2026-04-19-report.md
│   ├── 2026-04-18-report.md
│   └── ...
```

Track trends over time and spot new exposures as they appear.

---

## ⚠️ Legal & Ethics

These tools search **publicly accessible** data only:
- Public GitHub repos
- Public Shodan results
- Certificate transparency logs

**Do NOT:**
- Scan private repos without authorization
- Exploit found credentials
- Violate Terms of Service
- Use findings for malicious purposes

**Purpose:** Security awareness and hardening your own infrastructure.

---

## 🛠️ Troubleshooting

### GitHub API Rate Limits
- Search API: 30 req/min (authenticated)
- Wait for reset or use multiple tokens

### Shodan Insufficient Credits
- Free tier: 100 credits/month
- Resets on 1st of month
- Upgrade to paid for more

### TruffleHog Not Found
```bash
# Install via Homebrew
brew install trufflesecurity/trufflehog/trufflehog

# Or use the binary
curl -sSfL https://install.trufflehog.org | sh
```

---

## 📚 References

- [GitHub Code Search API](https://docs.github.com/en/rest/search)
- [Shodan API](https://developer.shodan.io/api)
- [TruffleHog OSS](https://github.com/trufflesecurity/trufflehog)
- [Certificate Transparency](https://certificate.transparency.dev/)

---

## 📝 License

MIT - For educational and authorized security testing purposes only.
