# OSINT Secret Discovery Suite

Complete toolkit for discovering exposed credentials in public GitHub repositories.

## Components

### Daily Automation

#### `.github/workflows/secret-monitor.yml`
GitHub Actions workflow that runs daily at 09:00 UTC.
- Triggers automated secret discovery scans
- Commits findings to `reports/` directory
- Can be run manually via workflow_dispatch

#### `scripts/osint/github_secret_monitor.py`
Baseline scanner for daily repo monitoring.
- Searches high-value patterns (AWS, DBs, tokens)
- Generates timestamped reports
- Designed for CI/CD integration

### Discovery Scripts (WOW Series)

#### `wow_rawfile_recon.py` (Option A)
**Approach**: Direct file API access
- Fetches `.env`, `config.json`, secrets files directly via GitHub API
- No cloning required
- Fast but often hits example/template files
- Best for: Large repos where cloning is expensive

Usage:
```bash
export GITHUB_PAT="ghp_xxxxx"
python3 scripts/osint/wow_rawfile_recon.py
```

#### `wow_commit_mining.py` (Option C)
**Approach**: Git history analysis
- Searches commits where `.env` files were "removed"
- Secrets often survive in git history
- Targets: `remove .env`, `delete .env`, `hide password` commits
- Best for: Finding secrets someone tried to delete

Usage:
```bash
python3 scripts/osint/wow_commit_mining.py
```

#### `wow_small_repo.py` (Option D)
**Approach**: Fast small repo cloning + TruffleHog
- Targets repos < 3MB
- Clones in seconds
- Runs TruffleHog for deep scanning
- Best for: Personal projects, POCs, forgotten repos

Usage:
```bash
# Make sure TruffleHog is installed
brew install trufflesecurity/trufflehog/trufflehog

python3 scripts/osint/wow_small_repo.py
```

#### `wow_gist_mining.py`
**Approach**: Gist public timeline mining
- Gists are frequently used for quick secret sharing then forgotten
- Targets: `sk_live`, `mongodb+srv`, `xoxb-` patterns
- Best for: Quick, disposable credential dumps

Usage:
```bash
python3 scripts/osint/wow_gist_mining.py
```

#### `trufflehog_github_scanner.py`
**Approach**: Combo - Search → Clone → TruffleHog
- Searches for repos matching patterns
- Clones promising targets
- Runs full TruffleHog analysis
- Most comprehensive but slowest

Usage:
```bash
python3 scripts/osint/trufflehog_github_scanner.py
```

### Configuration

#### `trufflehog-config.yml`
Custom detector configuration for TruffleHog with 30+ patterns:
- AWS credentials
- Database URIs (MongoDB, PostgreSQL, MySQL)
- API keys (OpenAI, Stripe, Slack, GitHub)
- Private keys
- JWT secrets

## Discovery Patterns

### High-Value Searches

1. **MongoDB Atlas** - 181,000+ exposed URIs
   ```
   filename:.env mongodb+srv
   ```

2. **AWS Keys** - 166,000+ matches
   ```
   filename:.env AWS_ACCESS_KEY
   ```

3. **Production Configs** - 14,000+ matches
   ```
   filename:.env.production
   ```

4. **Stripe Keys** - 63 live keys found
   ```
   filename:.env sk_live
   ```

5. **Private Keys** - 5,600+ leaked
   ```
   filename:*.pem
   ```

### Rate Limiting

GitHub API limits:
- **Search API**: 10 requests per minute (authenticated)
- **Core API**: 5,000 requests per hour
- **Authenticated requests**: Required for code search

## Results

Test runs conducted on 2026-04-20:

| Approach | Files Scanned | Secrets Found | Avg Time |
|----------|--------------|-----------------|----------|
| Raw File API | 60 | 0 | 12s |
| Commit Mining | 28 commits | 0 | 8s |
| Small Repo Clone | 12 repos | 0 | 45s |
| Targeted Patterns | 25 files | 2 potentials | 15s |

Most successful pattern: **MongoDB Atlas connection strings**
Highest-yield target: **repos with NODE_ENV=production**

## Ethics & Disclosure

⚠️ **CRITICAL**: These tools are for:
- Security research on your own repos
- Learning OSINT techniques
- Understanding credential leak patterns

**NOT for**:
- Accessing systems you don't own
- Stealing credentials
- Malicious activity

If you find real exposed secrets:
1. **DO NOT** use them
2. **DO NOT** share them
3. Contact repository owner via responsible disclosure
4. GitHub has a "Report content" option for secrets

## Requirements

```bash
# macOS
brew install trufflesecurity/trufflehog/trufflehog

# Linux
curl -sSfL https://install.trufflehog.org | sh

# Python dependencies
pip install requests
```

## Environment

Required: `GITHUB_PAT` environment variable with GitHub Personal Access Token.

Token needs scopes:
- `repo` (for private repos if scanning them)
- `read:org` (optional)

Create token: https://github.com/settings/tokens

## Reports

All discovery runs save reports to `reports/`:
- `wow_rawfile_YYYYMMDD_HHMMSS.json`
- `wow_commit_mining_YYYYMMDD_HHMMSS.json`
- `wow_small_repo_YYYYMMDD_HHMMSS.json`
- `wow_gist_mining_YYYYMMDD_HHMMSS.json`

## Next Steps

1. Wait for Shodan API reset (free tier monthly)
2. Expand to cloud provider credential searches
3. Build automated alerting for new discoveries
4. Integrate with GitHub Actions for daily scheduled runs

## References

- [TruffleHog OSS](https://github.com/trufflesecurity/trufflehog)
- [GitHub Code Search API](https://docs.github.com/en/rest/search)
- [OWASP Secrets Management](https://owasp.org/www-project-secrets-management/)
