---
title: "Deep Past: Akkadian Translation"
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md]
related: [[wiki/techniques/mbr-decoding.md]], [[wiki/models/byt5.md]], [[wiki/kaggle/arc-agi-benchmarking.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [kaggle, nlp, translation, akkadian, byt5, mbr, low-resource, leakage]
---

# Deep Past: Akkadian Translation

**Competition:** Deep Past Initiative — Translate Akkadian to English
**Prize:** $50,000 | **Deadline:** 2026-03-23 (closed)
**Cameron's best legit score:** 34.7 (top score: 42.9, ~19% gap)
**Notebooks:** 8 iterations

## What it was

Low-resource machine translation from Akkadian cuneiform to English. Akkadian is a dead Semitic language; the training corpus is tiny and domain-specific. Standard transformer approaches fail hard here — no large pretrained models exist for Akkadian, and the character-level nature of cuneiform transliteration makes word-level tokenization lossy.

## Cameron's approach

### Core stack: ByT5 + MBR

**[[wiki/models/byt5.md]]** — a byte-level T5 variant that never tokenizes. Every character/byte is a token. Critical for Akkadian where:
- Cuneiform transliteration uses unusual Unicode characters
- Standard BPE tokenizers destroy morphological structure
- Rare scripts have near-zero vocabulary coverage in standard tokenizers

**[[wiki/techniques/mbr-decoding.md]]** (Minimum Bayes Risk) — instead of taking the single highest-probability output (beam search), generate N candidates and select the one with highest average similarity to all others. On low-resource tasks, this measurably reduces variance and cherry-picks more fluent outputs.

### Iteration history (inferred from notebook sequence)

1. `submission-byt5` — baseline ByT5 submission
2. `score-34-7-byt5-mbr-pipeline` — added MBR, achieved 34.7
3. `score-34-7-byt5-mbr-pipeline-71fdef` — pipeline variant
4. `improved-byt5-mbr` / `byt5-mbr-pipeline-71fdef-v2` — further tuning
5. `akkadianoptimized-mbr` — Akkadian-specific optimization pass
6. `deep-pasta-mbr` — additional experiment

### Data leakage discovery

**Cameron also published:** `first-place-top-1-with-leakage`

He found data leakage in the competition — test set answers were inferable from features that should have been withheld. He documented this in a public notebook, demonstrating both the leakage exploit (achieving first place / top 1%) and responsible disclosure. **This is the more notable finding** from a competition-integrity standpoint.

## Results

| Approach | Score | Notes |
|----------|-------|-------|
| ByT5 + MBR (legitimate) | 34.7 | Best honest score |
| With leakage exploitation | ~Top 1% / 1st | Documented, not the primary submission |
| Top of leaderboard | 42.9 | DataTech Club |

## What Cameron learned

- **ByT5 is the right tool for rare-script / low-resource NLP** — byte-level tokenization sidesteps the OOV problem entirely
- **MBR decoding consistently outperforms greedy/beam on low-resource tasks** — see [[wiki/techniques/mbr-decoding.md]]
- **Leakage detection is a skill** — identifying that test labels were inferable requires understanding the data pipeline end to end
- High score gap (34.7 vs 42.9) likely reflects training data volume limits; the top teams had domain-specific data access or fine-tuned larger models

## Portfolio angle

- Strong NLP systems design story: ByT5 → why byte-level, MBR → why not greedy
- Leakage discovery = data pipeline awareness, not just modeling skill
- 8+ iterations shows methodology, not just a lucky run
- Connects to [[wiki/techniques/mbr-decoding.md]] as a reusable technique page
