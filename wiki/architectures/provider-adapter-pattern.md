---
title: Provider Adapter Pattern (Multi-LLM)
type: architecture
status: active
visibility: public
sources: [raw/repos/arc-agi-benchmarking-readme.md]
related: [[wiki/kaggle/arc-agi-benchmarking.md]], [[wiki/decisions/arc-agi-adapters-vs-litellm.md]], [[wiki/architectures/agentic-trading-system.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [architecture, strategy-pattern, multi-provider, llm, adapter, abstraction]
---

# Provider Adapter Pattern (Multi-LLM)

A **strategy pattern** for abstracting LLM provider APIs behind a uniform interface. Each provider (OpenAI, Anthropic, Gemini, Grok) gets its own adapter class; calling code never touches provider SDKs directly.

## Interface

```python
class ProviderAdapter:
    def init_client(self): ...
    def make_prediction(self, prompt: str) -> Attempt: ...
    def chat_completion(self, messages: str) -> str: ...
```

Adding a new provider = implement these three methods. **No changes to the runner or scoring logic.**

## Structure

```
adapters/
  openai_adapter.py
  anthropic_adapter.py
  gemini_adapter.py
  grok_adapter.py
  base.py             ← ProviderAdapter ABC
```

Model selection is config-driven via `models.yml` — the runner instantiates the right adapter based on the `provider` field.

## Why this works

- **Swap models with config changes, not code changes** — the key value proposition
- **Testability** — each adapter can be unit-tested in isolation; mock adapters work at the interface level
- **Rate limiting and retry logic live in the runner**, not the adapters — clean separation of concerns
- **Pricing stays with the model config**, not the adapter — cost tracking doesn't couple to provider logic

## Tradeoffs vs. unified SDKs (LiteLLM)

See [[wiki/decisions/arc-agi-adapters-vs-litellm.md]] for the full ADR. Short version: custom adapters give full control at the cost of more boilerplate; unified SDKs reduce boilerplate at the cost of abstraction leakage.

## Where Cameron uses this

- [[wiki/kaggle/arc-agi-benchmarking.md]] — multi-provider ARC-AGI evaluation harness

## Related patterns

- [[wiki/architectures/agentic-trading-system.md]] — uses a single provider (Groq/Llama) with no need for the adapter layer; simpler when provider is fixed
