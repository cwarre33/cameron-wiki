---
title: "ADR: OSINT Pattern Filtering Strategy"
type: decision
status: active
visibility: public
context:
  - GitHub Code Search returns ~85% false positives
  - Test fixtures, documentation examples, placeholder data
  - Need to identify only legitimate production credentials
considered:
  - Keyword filtering only
  - Entropy analysis only  
  - Combined approach with source code verification
  - ML-based classification
decision: Combined keyword + entropy + source verification
consequences:
  - Higher confidence reports
  - Slower verification (10-15 min per finding)
  - Lower false positive rate (~15%)
related:
  - [[github-osint-credential-discovery]]
  - [[credential-exposure-patterns]]
created: 2026-04-21
updated: 2026-04-21
confidence: high
tags: [osint, decision, filtering, false-positives]
---

# ADR: OSINT Pattern Filtering Strategy

## Status
**Accepted** | High Confidence

## Context

When searching GitHub for exposed credentials, the Code Search API returns massive numbers of **test fixtures, documentation examples, and placeholder data**. In initial testing, 85%+ of matches were false positives.

**Examples of false positives found:**
- `postgres://user:password@localhost/testdb` (test fixture)
- `-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA...` (documentation example in README)
- `API_KEY = "your_api_key_here"` (placeholder)

We need a reliable filtering strategy that preserves true positives while eliminating noise.

## Options Considered

### Option 1: Keyword Filtering Only

Filter out matches containing obvious markers:

```python
SKIP_KEYWORDS = ['example', 'test', 'placeholder', 'localhost', 'fake']
```

**Pros:**
- Simple to implement
- Fast execution

**Cons:**
- Easily bypassed (`test_key`, `mytest`)
- May filter real keys in test repositories
- No entropy validation

**Verdict:** Rejected - insufficient filtering

### Option 2: Entropy Analysis Only

Calculate Shannon entropy to detect high-randomness strings:

```python
def entropy(s):
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(s)]
    return -sum(p * math.log(p, 2) for p in prob)

if entropy(content) > 4.5:  # Report
```

**Pros:**
- Catches well-randomized secrets
- Language agnostic

**Cons:**
- Base64 has high entropy but could be test data
- Misses low-entropy patterns (weak passwords)
- False positives on compressed data

**Verdict:** Rejected - incomplete solution

### Option 3: Combined Approach (CHOSEN)

**Layer 1: Entropy Threshold**
```python
if entropy(content) < 3.5:
    return False  # Too predictable
```

**Layer 2: Keyword Filtering**
```python
SKIP_KEYWORDS = [
    'example', 'placeholder', 'your_', 'test',
    'sample', 'localhost', '127.0.0.1', 'fake',
    'dummy', '***', 'xxxx', 'changeme'
]

if any(kw in content.lower() for kw in SKIP_KEYWORDS):
    return False
```

**Layer 3: Format Validation**
```python
# Must match expected pattern
if not re.match(r'ghp_[a-zA-Z0-9]{36}', content):
    return False
```

**Layer 4: Local Verification (CRITICAL)**
```bash
# Clone and check
if key in test/ or docs/:
    return False

if key used in production_code():
    return True
```

**Pros:**
- Multiple defense layers
- High confidence (~85% accuracy)
- Catches both high-entropy keys and contextual usage

**Cons:**
- Slower (requires cloning repos)
- More complex implementation
- Rate limit considerations

**Verdict:** **ACCEPTED** - best balance of precision and coverage

### Option 4: ML-Based Classification

Train classifier on labeled examples of real vs fake credentials.

**Pros:**
- Potentially higher accuracy
- Learns edge cases

**Cons:**
- Requires labeled training data
- Overkill for this use case
- Hard to debug false positives

**Verdict:** Rejected - premature optimization

## Decision

**Use Combined Approach (Option 3):**

1. **Entropy threshold** eliminates predictable strings
2. **Keyword filtering** removes obvious markers
3. **Format validation** ensures pattern match
4. **Local verification** confirms production usage

## Consequences

### Positive
- **Higher confidence reports** - Only report verified findings
- **Professional credibility** - Maintainers take reports seriously
- **Lower noise** - 15% false positive rate vs 85%

### Negative  
- **Slower process** - 10-15 minutes per finding vs instant
- **Rate limit constraints** - Can't mass-process thousands
- **Manual analysis required** - Can't fully automate

## Implementation

```python
# scripts/osint/filters.py

def is_credible_credential(repo, file_path, content):
    """Multi-layer validation"""
    
    # Layer 1: Entropy
    if calculate_entropy(content) < 3.5:
        return False
    
    # Layer 2: Keywords
    if contains_test_markers(content):
        return False
    
    # Layer 3: Pattern
    if not matches_expected_pattern(content):
        return False
    
    # Layer 4: Local verification
    clone_path = shallow_clone(repo)
    if is_in_test_directory(clone_path, file_path):
        return False
    if not used_in_production(clone_path, file_path):
        return False
    
    return True
```

## Validation

From April 2026 hunt results:

| Filter | False Positive Rate |
|--------|---------------------|
| Entropy only | ~60% |
| Keywords only | ~45% |
| Combined (no local) | ~25% |
| **Full 4-layer** | **~15%** |

**Result:** Full filtering caught 2 real private keys in 5 checked files (40% hit rate) with zero false positives reported.

## Lessons

1. **Never skip local verification** - Found test files that passed all other filters
2. **Context matters** - Key in `private/` is different from key in `test/fixtures/`
3. **Entropy is necessary but not sufficient** - Documentation examples have high entropy

## Related Decisions

- [[github-osint-credential-discovery]] - Full methodology
- [[credential-exposure-patterns]] - Pattern analysis
- [[shodan-ics-discovery]] - Similar filtering for ICS

---

*Decision Date: 2026-04-21*
*Last Updated: 2026-04-21*