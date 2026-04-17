---
title: MBR Decoding (Minimum Bayes Risk)
type: technique
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md]
related: [[wiki/kaggle/deep-past-akkadian-translation.md]], [[wiki/models/byt5.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [nlp, decoding, mbr, sequence-generation, translation, low-resource]
---

# MBR Decoding (Minimum Bayes Risk)

A sequence generation decoding strategy that selects the output with **highest expected utility across a sample of candidates**, rather than the single highest-probability output.

## The problem with greedy/beam search

Standard decoding (greedy or beam search) maximizes sequence probability under the model. This has two failure modes:

1. **Exposure bias** — model is trained on gold prefixes, generates on its own outputs; errors compound
2. **Mode collapse** — the highest-probability output is often generic/safe, not the best by downstream metrics (BLEU, chrF, etc.)

On low-resource tasks, these problems are worse: the model is uncertain, and the highest-probability beam is often wrong.

## How MBR works

```
1. Sample N candidate outputs from the model (N = 50–200 typical)
2. For each candidate c_i, compute its average similarity to all other candidates
   score(c_i) = mean(sim(c_i, c_j) for j ≠ i)
3. Return the candidate with highest average similarity
```

The similarity function is usually chrF, BLEU, or a learned metric. The winner is the "consensus" candidate — the one most other candidates agree with.

## Why it works

MBR is finding the **Bayes-optimal output under the empirical distribution**. The sample of N candidates approximates the model's full distribution. The consensus candidate has low expected loss even if the model is uncertain.

On low-resource translation:
- The model generates a diverse sample
- Fluent, accurate translations cluster together
- MBR identifies the cluster center
- Greedy/beam would pick the single highest-probability sequence, which may be an outlier

## Implementation sketch

```python
from sacrebleu.metrics import CHRF

chrf = CHRF()

def mbr_decode(candidates: list[str]) -> str:
    scores = []
    for i, hyp in enumerate(candidates):
        refs = candidates[:i] + candidates[i+1:]
        score = sum(chrf.sentence_score(hyp, [r]).score for r in refs)
        scores.append(score / len(refs))
    return candidates[scores.index(max(scores))]
```

## Where Cameron uses this

- [[wiki/kaggle/deep-past-akkadian-translation.md]] — ByT5 + MBR pipeline for Akkadian translation; achieved 34.7 (vs greedy baseline lower). Multiple notebook iterations refining the pipeline.

## Tradeoffs

| Factor | MBR | Beam Search |
|--------|-----|------------|
| Compute cost | N × forward passes | 1 beam search |
| Quality (low-resource) | Better | Worse |
| Quality (high-resource) | Marginal gain | Usually sufficient |
| Latency | High | Low |

## Key papers

- Eikema & Aziz (2020) — "Is MAP Decoding All You Need?" — foundational MBR for NMT
- Freitag et al. (2022) — MBR with quality-aware metrics; showed MBR+COMET beats beam across WMT

## Related techniques

- **Self-consistency** (Wei et al. 2022) — same idea applied to reasoning: sample N chain-of-thought paths, take majority vote answer. MBR is the continuous-output analog.
- **Ensemble decoding** — averaging logits across models; related but different — MBR works with a single model
