---
title: LiteLLM
type: tool
status: active
visibility: public
sources: [raw/repos/arc-agi-benchmarking-readme.md]
related: [[wiki/decisions/arc-agi-adapters-vs-litellm.md]], [[wiki/architectures/provider-adapter-pattern.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [tool, llm, sdk, multi-provider, openai-format, abstraction]
---

# LiteLLM

A Python library that provides a **unified interface for 100+ LLM providers** (OpenAI, Anthropic, Gemini, Azure, Bedrock, HuggingFace, etc.) using the OpenAI `chat/completions` format.

## Key features

- **Unified SDK** — call any model with the same `completion()` function
- **OpenAI-compatible output** — returns standard OpenAI-style response objects regardless of the provider
- **Streaming support** — consistent streaming interface across all models
- **Retry & fallback logic** — built-in support for model fallbacks and exponential backoff
- **Cost tracking** — automatic token counting and cost calculation per provider
- **LiteLLM Proxy** — a server that acts as an OpenAI-compatible gateway to any model

## Usage pattern

```python
from litellm import completion

# OpenAI
response = completion(model="gpt-4o", messages=[{"role": "user", "content": "hello"}])

# Anthropic
response = completion(model="claude-3-5-sonnet", messages=[{"role": "user", "content": "hello"}])

# Gemini
response = completion(model="gemini/gemini-pro", messages=[{"role": "user", "content": "hello"}])
```

## Role in Cameron's Wiki

LiteLLM is the primary **architectural alternative** to the custom [[wiki/architectures/provider-adapter-pattern.md]] used in the ARC-AGI benchmarking harness.

While LiteLLM reduces boilerplate and handles the complexity of multiple provider SDKs, Cameron chose **custom adapters** for the ARC-AGI project to maintain absolute control over request construction and response parsing, which is critical for benchmarking accuracy.

See [[wiki/decisions/arc-agi-adapters-vs-litellm.md]] for the detailed decision rationale.

## Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [GitHub Repository](https://github.com/BerriAI/litellm)
