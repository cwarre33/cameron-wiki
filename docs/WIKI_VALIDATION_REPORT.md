---
title: Wiki Schema Validation Report
date: 2026-04-21
status: validation-report
---

# Wiki Structure Validation

## Date: April 21, 2026

---

## ✅ Existing Pages (Follow Schema)

### Wiki Core
- ✅ `wiki/index.md` - Master catalog
- ✅ `wiki/log.md` - Activity log (1905 lines)
- ✅ `wiki/overview.md` - High-level synthesis

### Directories Following CLAUDE.md Schema
- ✅ `wiki/methodology/` - Wiki system meta
- ✅ `wiki/architectures/` - Serverless patterns, agents
- ✅ `wiki/techniques/` - CLIP+FAISS, Whisper, RLHF
- ✅ `wiki/integrations/` - Zendesk, NetSuite, AWS
- ✅ `wiki/tools/` - vLLM, PyTorch, FAISS, Groq
- ✅ `wiki/models/` - GPT, Claude, Llama
- ✅ `wiki/benchmarks/` - MMLU, HumanEval
- ✅ `wiki/decisions/` - ADRs (architectural decisions)
- ✅ `wiki/interview-prep/` - System design, behavioral
- ✅ `wiki/open-questions/` - Gaps, next experiments
- ✅ `wiki/comparisons/` - Synthesis pages

### Content Categories
- ✅ `wiki/kaggle/` - Per-competition writeups (19 competitions)
- ✅ `wiki/trading/` - Strategies, Alpaca patterns
- ✅ `wiki/people/` - Researchers
- ✅ `wiki/labs/` - OpenAI, Anthropic, DeepMind

---

## 📁 Non-Standard Locations

### `docs/` Directory (Disclosure Work)
These are tracking documents, not wiki content per CLAUDE.md rules:

| File | Purpose | Status |
|------|---------|--------|
| `docs/DISCLOSURE_TRACKER.md` | Security disclosure tracking | ✅ Keep in docs/ |
| `docs/portfolio/` | Portfolio documentation | ✅ New category needed? |
| `docs/*_DISCLOSURES_*.md` | Disclosure drafts | ✅ Keep in docs/ |
| `docs/*_ASSESSMENT_*.md` | Impact analysis | ✅ Keep in docs/ |

**Question:** Should security disclosure content migrate to wiki?
- Option A: Keep in docs/ (operational tracking)
- Option B: Move to `wiki/security/` or `wiki/osint/`

### `scripts/` Directory (Tools)
- ✅ `scripts/osint/` - Discovery tools
- ✅ `scripts/osint/README.md` - Tool documentation
- ✅ `scripts/osint/reports/` - Hunt results

**Follows CLAUDE.md:** Tools are code, not wiki content.

### `reports/` Directory
- ✅ `reports/DISCLOSURE_COMPLETION_REPORT.md` - Mission reports

**Question:** Should reports be in wiki/ or reports/?
- Current: reports/
- Wiki schema: wiki/ for knowledge

---

## 🔍 Schema Compliance Issues

### Issue #1: OSINT/Security Content Location
**Current:** `docs/`
**CLAUDE.md says:** `wiki/` is for LLM-generated knowledge

**Migration Path:**
```
docs/IMPACT_ASSESSMENT_20260421.md
→ wiki/techniques/osint-impact-assessment.md

docs/PRODUCTION_IMPACT_ANALYSIS_20260421.md  
→ wiki/techniques/credential-discovery-analysis.md

docs/portfolio/OSINT_CREDENTIAL_DISCOVERY_CASE_STUDY.md
→ wiki/comparisons/osint-security-research-case-study.md

docs/DISCLOSURE_TRACKER.md
→ wiki/open-questions/disclosure-timeline-2026.md
```

### Issue #2: Portfolio Documentation
**New Content Type:** Portfolio/skill demonstration

**Options:**
- A. Create `wiki/portfolio/` (violates CLAUDE.md schema)
- B. Move to `wiki/comparisons/` (synthesis pages)
- C. Keep in `docs/portfolio/` (operational, not wiki knowledge)

**Recommendation:** C - Keep in docs/. Portfolio is presentation layer, not knowledge base.

### Issue #3: Reports Directory
**CLAUDE.md:** `wiki/` for knowledge, `raw/` for sources, `.github/` for automation

**Current:** `reports/` for mission completion docs

**Question:** Where do security research reports belong?
- Option A: Keep in `reports/` (operational)
- Option B: Move to `wiki/osint/` or `wiki/security/`

**Recommendation:** A for operational reports, B for knowledge synthesis

---

## 🎯 Recommendations

### Keep As-Is (Operational)
1. `docs/DISCLOSURE_*.md` - Track disclosures
2. `docs/portfolio/` - Portfolio materials
3. `reports/OPERATIONAL_*.md` - Mission reports
4. `scripts/osint/` - Tools

### Potentially Migrate (Knowledge)
1. Analysis/synthesis content → `wiki/techniques/` or `wiki/comparisons/`
2. Lessons learned → `wiki/decisions/`

### Create New Wiki Pages
The OSINT work should generate knowledge:

- `wiki/techniques/github-osint-credential-discovery.md`
  - Methodology, tools, patterns
  - Techniques: GitHub Code Search, pattern matching
  
- `wiki/decisions/osint-pattern-filtering.md`
  - Why filter X over Y
  - Lessons from false positives

- `wiki/comparisons/credential-exposure-patterns.md`
  - PostgreSQL vs Private Key vs API Token
  - Risk assessment framework

- `wiki/tools/osint-security-toolkit.md`
  - Tool documentation
  - How to run hunts

---

## Next Steps

1. **Decide:** Keep operational docs in docs/ or migrate some to wiki/?
2. **Create:** OSINT technique pages in wiki/techniques/
3. **Update:** wiki/index.md with new pages
4. **Update:** wiki/log.md with latest activity
5. **Commit:** All changes to main

---

*Validator: Automated schema check*
*Source: CLAUDE.md schema definition*
