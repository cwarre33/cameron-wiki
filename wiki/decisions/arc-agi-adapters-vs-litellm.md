---
title: "ADR: Custom Provider Adapters vs. LiteLLM for ARC-AGI Harness"
type: decision
status: active
visibility: public
sources: [raw/repos/arc-agi-benchmarking-readme.md]
related: [[wiki/kaggle/arc-agi-benchmarking.md]], [[wiki/architectures/provider-adapter-pattern.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: medium
tags: [adr, arc-agi, litellm, multi-provider, abstraction, strategy-pattern]
---

# ADR: Custom Provider Adapters vs. LiteLLM

## Context

The ARC-AGI benchmarking harness needs to run tasks against models from OpenAI, Anthropic, Google, and Grok. Two obvious approaches:

1. **Custom adapter per provider** — implement `ProviderAdapter` interface for each
2. **[[wiki/tools/litellm.md|LiteLLM]]** — unified SDK that wraps 100+ providers behind one interface

## Decision

**Custom adapters** — one Python class per provider implementing a 3-method interface (`init_client`, `make_prediction`, `chat_completion`).

## Rationale

| Factor | Custom Adapters | LiteLLM |
|--------|----------------|---------|
| Control over request shape | Full | LiteLLM mediates |
| Provider-specific features | Easy to access | May be abstracted away |
| Boilerplate | More per provider | Less |
| Dependency | None (native SDKs) | LiteLLM + its deps |
| Debugging | Transparent | Extra indirection layer |
| ARC-AGI-specific response parsing | Own logic | LiteLLM's generic parsing |

For a **benchmarking harness**, precise control over request construction and response parsing matters more than reducing boilerplate. ARC-AGI tasks require exact output format validation — you want to own that logic, not inherit it from a third-party unification layer.

⚠️ This is a judgment call. LiteLLM would have been a reasonable choice, especially if the provider list grew large. The fork started from arcprizeorg/model_baseline which already used this pattern — path dependence is a factor.

## Consequences

- Adding a new provider requires implementing three methods — low but non-zero friction
- Rate limiting and retry logic live in the runner (`run_all.py`), not the adapters — this is correct; the adapter is thin
- Testing each adapter independently is straightforward
- If LiteLLM adds ARC-AGI-specific support, switching has nonzero migration cost

## Related

- [[wiki/architectures/provider-adapter-pattern.md]] — the pattern itself
- [[wiki/decisions/autotrader-open-model-vs-frontier.md]] — different trade-off: single provider chosen for cost reasons
