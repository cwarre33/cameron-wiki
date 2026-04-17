---
title: LiteLLM
type: tool
status: stable
visibility: public
sources: [https://github.com/BerriAI/litellm]
related: [[wiki/decisions/arc-agi-adapters-vs-litellm.md]], [[wiki/architectures/provider-adapter-pattern.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [tool, llm, sdk, abstraction, proxy, python]
---

# LiteLLM

**LiteLLM** is a Python library that provides a unified interface for calling 100+ LLM APIs (OpenAI, Anthropic, Gemini, HuggingFace, etc.) using the OpenAI completion/embedding format.

## Key Features

- **Standardized Input/Output**: Call any provider using `completion(model="gpt-3.5-turbo", messages=...)`.
- **Authentication Handling**: Manages API keys and environment variables across providers.
- **Cost Tracking**: Built-in support for calculating token usage and cost per request.
- **Streaming Support**: Unified streaming interface for all supported models.
- **Proxy Server**: Optional proxy to provide a centralized endpoint for team-wide LLM access.

## Usage in Cameron's Projects

LiteLLM is frequently considered when building multi-provider systems, though it is sometimes passed over in favor of the [[wiki/architectures/provider-adapter-pattern.md|Provider Adapter Pattern]] for specific reasons.

### ARC-AGI Benchmarking
In the [[wiki/kaggle/arc-agi-benchmarking.md|ARC-AGI project]], LiteLLM was evaluated but ultimately **not used**. 

**Reasons for rejection:**
- **Control**: Need for precise control over request shapes and provider-specific parameters (e.g., temperature ranges, system prompt handling).
- **Transparency**: Benchmarking requires visibility into the raw response to debug parsing errors; LiteLLM's abstraction layer can occasionally mask these.
- **Dependencies**: Preference for native SDKs to minimize the dependency tree for the runner harness.

See the full decision log: [[wiki/decisions/arc-agi-adapters-vs-litellm.md|ADR: Custom Provider Adapters vs. LiteLLM]].

## Comparison: LiteLLM vs. Custom Adapters

| Feature | LiteLLM | Custom Adapters |
|---------|---------|-----------------|
| **Boilerplate** | Low (Unified call) | High (One class per provider) |
| **Control** | Mediated by abstraction | Full access to native SDK |
| **Maintenance** | Handled by LiteLLM maintainers | Manual updates for SDK changes |
| **Debugging** | Indirect (Check LiteLLM issues) | Direct (Check provider SDK/docs) |

## Related
- [[wiki/architectures/provider-adapter-pattern.md]]
- [[wiki/decisions/arc-agi-adapters-vs-litellm.md]]
