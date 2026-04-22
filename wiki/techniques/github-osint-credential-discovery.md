---
title: GitHub OSINT Credential Discovery
type: technique
status: active
visibility: public
sources:
  - raw/osint/2026-04-19-scan-enriched.json
  - docs/PRODUCTION_IMPACT_ANALYSIS_20260421.md
related:
  - [[osint-pattern-filtering]]
  - [[credential-exposure-patterns]]
  - [[responsible-disclosure-process]]
  - [[github-code-search-api]]
created: 2026-04-21
updated: 2026-04-21
confidence: high
tags: [osint, security, github, credentials, discovery]
---

# GitHub OSINT Credential Discovery

**Summary:** Systematic approach to discovering exposed cryptographic credentials in public GitHub repositories using the Code Search API combined with local verification and responsible disclosure.

## Overview

This technique combines [[github-code-search-api]] with pattern matching and entropy analysis to identify live production credentials accidentally committed to public repositories. The approach prioritizes **verification over volume** - each potential finding is cloned locally and analyzed before disclosure.

**Key Insight:** GitHub's Secret Scanning catches common patterns (AWS keys, Slack tokens) but misses custom formats, private keys, and repository-specific credentials. Manual OSINT fills this gap.

## Method

### Phase 1: Pattern Engineering

Effective searches target high-entropy content in sensitive locations:

```
extension:key path:private                    # Private keys
filename:.env.production                      # Production configs
filename:id_rsa OR filename:id_ed25519        # SSH keys
mongodb+srv:// password                       # MongoDB Atlas
postgresql:// user:pass                       # PostgreSQL URIs
AWS_ACCESS_KEY_ID created:>2025-01-01       # Recent AWS keys
```

**Why These Work:**
- `extension:key` files are cryptographic material
- `path:private` suggests sensitive directory structure
- `created:>DATE` filters to recent commits (more likely active)

### Phase 2: Entropy Filtering

Not all matches are secrets. Filter out test/example data:

```python
SKIP_KEYWORD = [
    'example', 'placeholder', 'your_', 'test',
    'sample', 'localhost', 'fake', '***', 'xxxx'
]

def is_likely_real(content):
    # High entropy check
    if entropy(content) < 3.5:
        return False
    # Not documentation
    if any(kw in content.lower() for kw in SKIP_KEYWORDS):
        return False
    return True
```

**Rationale:** Real secrets have high entropy. Test data uses predictable patterns.

### Phase 3: Local Verification

Clone and verify before disclosure:

```bash
# 1. Clone shallow (fast)
git clone --depth 1 https://github.com/{owner}/{repo}.git

# 2. Verify key validity (if applicable)
openssl rsa -in private/key.pem -check -noout

# 3. Check usage in source code
grep -r "private/key" --include="*.js" --include="*.ts"
```

**Critical:** This prevents reporting test fixtures or documentation examples.

### Phase 4: Impact Analysis

Determine **production usage** from source:

| Indicator | Risk Level |
|-----------|------------|
| `fs.readFileSync('private/key')` | 🔴 CRITICAL - Active use |
| Copied to `/etc/ssl/` or `/www/ssl/` | 🔴 CRITICAL - Deployed |
| Hardcoded in HTTPS server | 🔴 CRITICAL - Production |
| Only in `test/` directory | 🟢 LOW - Test fixture |
| Contains "example" or "test" | 🟢 LOW - Documentation |

## Tools

### Custom Scripts

**`fresh_credential_hunter.py`** (Targeted)
- Searches specific file patterns
- Filters by creation date
- Verifies before reporting

**`bulk_credential_hunter.py`** (Broad)
- Multiple patterns in sequence
- JSON report generation
- Designed for collecting multiple discoveries per session

**`live_credential_hunter.py`** (Aggressive)
- Continuous round-based hunting
- Max discovery targets
- Built-in rate limit handling

See [[osint-security-toolkit]] for full documentation.

## Results

### April 2026 Discoveries

**Summary:** 7 live credentials discovered, 6 disclosed (86%)

| Finding | Severity | Status | Repo Stars |
|---------|----------|--------|------------|
| Private key in HTTPS server | 🔴 | Disclosed #23 | 18 |
| SSL key for admin panel | 🔴 | Disclosed #53 | 99 |
| GitHub PAT + PostgreSQL | 🔴 | Disclosed #1 | N/A |
| PostgreSQL URI (x3) | 🟠 | Disclosed (x3) | Various |
| GitHub PAT pattern | 🟡 | Disclosed #3438 | 29.4k |

**Impact:** 29,600+ combined GitHub stars affected

### Key Lessons

1. **`extension:key path:private`** has highest yield (2/5 files = 40%)
2. Local verification essential - 85% of matches are test/documentation
3. Production usage in source code = CRITICAL severity
4. Maintain rate limit awareness (30 searches/hour)

## Limitations

- **Rate limiting:** 30 searches/hour maximum
- **False positives:** Test data, examples, documentation
- **Coverage gaps:** Private repos, deleted commits, alternate VCS
- **Temporal:** Can only find what's currently committed

## Extensions

### Git History Mining

Credentials often exist in deleted commits:

```bash
# Search deleted files in history
git log --diff-filter=D --name-only --pretty=format: | sort -u

# Check for .env deletions
git log --all --full-history -- '*.env'
```

See [[commit-history-analysis]] for techniques.

### Real-Time Monitoring

GitHub Events API provides firehose of public activity:

```
https://api.github.com/events
```

Filter for commits touching sensitive paths.

## Related Techniques

- [[shodan-ics-discovery]] - Industrial control system exposure
- [[credential-entropy-analysis]] - Detecting secrets via entropy
- [[responsible-disclosure-process]] - Disclosure workflow

## References

- **Repository:** https://github.com/cwarre33/cameron-wiki/scripts/osint/
- **Full Case Study:** [[osint-credential-discovery-case-study]]
- **Disclosure Tracker:** [[disclosure-timeline-2026]]

---

*Last Updated: 2026-04-21*
