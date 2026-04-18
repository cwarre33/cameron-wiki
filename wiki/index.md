# Wiki Index
Master catalog of all wiki pages. Updated automatically.

---

## Production Systems
*Cameron's FLS production engineering work.*

| Page | Summary | Status | Visibility | Updated |
|------|---------|--------|------------|---------|
| [SofaScope — AI-Powered Furniture Visual Search](production-systems/sofascope.md) | Live pilot at Furnitureland South (FLS). Dual-modality search over a 200,000-product catalog: fast metadata-weighted text search and CLIP + FAISS i... | active | public | 2026-04-17 |

## Architectures
*Serverless patterns, agent systems, transformer family, retrieval systems.*

| Page | Summary | Updated |
|------|---------|---------|
| [Agentic Trading System Architecture](architectures/agentic-trading-system.md) | Pattern for a containerized, scheduled LLM-driven trading agent with persistent memory and a self-improvement feedback loop. Implemented in wiki/tr... | 2026-04-17 |
| [Provider Adapter Pattern (Multi-LLM)](architectures/provider-adapter-pattern.md) | A strategy pattern for abstracting LLM provider APIs behind a uniform interface. Each provider (OpenAI, Anthropic, Gemini, Grok) gets its own adapt... | 2026-04-17 |

## Techniques
*CLIP+FAISS, Whisper pipelines, routing algorithms, MBR decoding, etc.*

| Page | Summary | Updated |
|------|---------|---------|
| [CLIP + FAISS Visual Search Pipeline](techniques/clip-faiss-visual-search.md) | Pattern for production image similarity search: encode images with CLIP, index embeddings with FAISS, retrieve nearest neighbors. | 2026-04-17 |
| [Hybrid Search Routing (Text + Image)](techniques/hybrid-search-routing.md) | Pattern for multi-modal search: route queries to the optimal search engine based on modality rather than using one unified approach. | 2026-04-17 |
| [LLM Review Pass Before Rotation](techniques/llm-review-pass-before-rotation.md) | A technique for extracting durable signal from time-bounded context before it's purged. Run an LLM over a rolling log or stale document corpus, dis... | 2026-04-17 |
| [MBR Decoding (Minimum Bayes Risk)](techniques/mbr-decoding.md) | A sequence generation decoding strategy that selects the output with highest expected utility across a sample of candidates, rather than the single... | 2026-04-17 |
| [Persistent Model Loading Pattern](techniques/persistent-model-loading.md) | Rule: Load ML models once at service startup. Never reload per request. | 2026-04-17 |

## Integrations
*Zendesk API, NetSuite/SuiteQL, AWS, MiCollab, Groq, Copilot Studio.*

| Page | Summary | Updated |
|------|---------|---------|
| [Alpaca API Integration](integrations/alpaca-api.md) | Alpaca is a commission-free stock trading API. Offers separate paper trading and live trading environments with identical API interfaces — swap cre... | 2026-04-17 |

## Papers
*Formal published research summaries.*

| Page | Summary | Updated |
|------|---------|---------|
| *(none yet)* | | |

## Models

| Page | Summary | Updated |
|------|---------|---------|
| [ByT5 (Byte-Level T5)](models/byt5.md) | Google Research, 2021. A T5 variant that operates directly on raw UTF-8 bytes — no tokenizer, no vocabulary, no BPE. Every byte is a token. | 2026-04-17 |
| [CLIP — Contrastive Language-Image Pretraining](models/clip.md) | OpenAI's vision-language model trained to align image and text embeddings in a shared space via contrastive learning. Enables zero-shot visual simi... | 2026-04-17 |
| [Llama 3.3 70B](models/llama-3-3-70b.md) | Meta's open-weights instruction-tuned LLM. Released late 2024. 70B parameters — large enough for strong reasoning and instruction following, small ... | 2026-04-17 |

## Benchmarks

| Page | Summary | Updated |
|------|---------|---------|
| [ARC-AGI Benchmark](benchmarks/arc-agi.md) | Abstraction and Reasoning Corpus for Artificial General Intelligence. Created by François Chollet. The benchmark that specifically resists LLM memo... | 2026-04-17 |

## Datasets

| Page | Summary | Updated |
|------|---------|---------|
| *(none yet)* | | |

## Tools

| Page | Summary | Updated |
|------|---------|---------|
| [FAISS — Facebook AI Similarity Search](tools/faiss.md) | Meta's library for efficient similarity search and clustering of dense vectors. Core infrastructure for any embedding-based retrieval system. | 2026-04-17 |
| [Groq — LLM Inference API](tools/groq.md) | Groq provides ultra-low-latency inference for open-source LLMs via custom LPU (Language Processing Unit) hardware. Primary value proposition: signi... | 2026-04-17 |
| [LiteLLM](tools/litellm.md) | LiteLLM is a Python library that provides a unified interface for calling 100+ LLM APIs (OpenAI, Anthropic, Gemini, HuggingFace, etc.) using the Op... | 2026-04-17 |

## Labs

| Page | Summary | Updated |
|------|---------|---------|
| *(none yet)* | | |

## People

| Page | Summary | Updated |
|------|---------|---------|
| [Andrej Karpathy](people/andrej-karpathy.md) | AI researcher, educator, and former OpenAI/Tesla engineer. One of the most influential technical communicators in deep learning. | 2026-04-17 |

## Kaggle Competitions

| Page | Summary | Competition | Updated |
|------|---------|-------------|---------|
| ["Deep Past: Akkadian Translation"](kaggle/deep-past-akkadian-translation.md) | Competition: Deep Past Initiative — Translate Akkadian to English | "Deep Past: Akkadian Translation" | 2026-04-17 |
| ["Motion-S: Text-to-Sign Motion Generation"](kaggle/motion-s-text-to-sign.md) | Competition: Motion-S: Hierarchical Text-to-Motion Generation for Sign Language (Signvrse) | "Motion-S: Text-to-Sign Motion Generation" | 2026-04-17 |
| [AI Mathematical Olympiad — Progress Prize 3](kaggle/aimo-progress-prize-3.md) | Competition: AI Mathematical Olympiad - Progress Prize 3 | AI Mathematical Olympiad — Progress Prize 3 | 2026-04-17 |
| [ARC Prize 2025](kaggle/arc-prize-2025.md) | Competition: ARC Prize 2025 | ARC Prize 2025 | 2026-04-17 |
| [ARC-AGI Benchmarking Harness](kaggle/arc-agi-benchmarking.md) | Cameron's fork of [arcprizeorg/model_baseline](https://github.com/arcprizeorg/model_baseline). A production-grade async test harness for running fr... | ARC-AGI Benchmarking Harness | 2026-04-17 |
| [CSIRO — Image2Biomass Prediction](kaggle/csiro-image2biomass.md) | Competition: CSIRO - Image2Biomass Prediction | CSIRO — Image2Biomass Prediction | 2026-04-17 |
| [Cameron's Kaggle Portfolio — Overview](kaggle/portfolio-overview.md) | 14 competitions entered across NLP, bioinformatics, CV, mathematical reasoning, quantitative finance, sports analytics, and wildlife ID. Total priz... | Cameron's Kaggle Portfolio — Overview | 2026-04-17 |
| [Google Tunix Hackathon](kaggle/google-tunix-hackathon.md) | Competition: Google Tunix Hack - Train a model to show its work | Google Tunix Hackathon | 2026-04-17 |
| [House Prices — Advanced Regression Techniques](kaggle/house-prices-regression.md) | Competition: House Prices - Advanced Regression Techniques | House Prices — Advanced Regression Techniques | 2026-04-17 |
| [Hull Tactical — Market Prediction](kaggle/hull-tactical-market-prediction.md) | Competition: Hull Tactical - Market Prediction | Hull Tactical — Market Prediction | 2026-04-17 |
| [Jaguar Re-Identification Challenge](kaggle/jaguar-re-identification.md) | Competition: Jaguar Re-Identification Challenge | Jaguar Re-Identification Challenge | 2026-04-17 |
| [MABe — Social Action Recognition in Mice](kaggle/mabe-mouse-behavior.md) | Competition: MABe Challenge - Social Action Recognition in Mice | MABe — Social Action Recognition in Mice | 2026-04-17 |
| [March Machine Learning Mania 2026](kaggle/march-machine-learning-mania-2026.md) | Competition: March Machine Learning Mania 2026 | March Machine Learning Mania 2026 | 2026-04-17 |
| [Predicting Heart Disease (Playground S6E2)](kaggle/playground-s6e2-heart-disease.md) | Competition: Predicting Heart Disease (Playground Series Season 6, Episode 2) | Predicting Heart Disease (Playground S6E2) | 2026-04-17 |
| [Stanford RNA 3D Folding (Part 2)](kaggle/stanford-rna-3d-folding.md) | Competition: Stanford RNA 3D Folding Part 2 | Stanford RNA 3D Folding (Part 2) | 2026-04-17 |
| [UrbanFloodBench — Flood Modelling](kaggle/urban-flood-modelling.md) | Competition: UrbanFloodBench: Flood Modelling | UrbanFloodBench — Flood Modelling | 2026-04-17 |

## Trading

| Page | Summary | Updated |
|------|---------|---------|
| [AutoTrader — Autonomous Paper Trading Bot](trading/autotrader.md) | AI-powered paper trading bot. Scans top 50 most-active stocks every 15 minutes, applies RSI + LLM news sentiment as dual signal gates, and executes... | 2026-04-17 |
| [RSI + LLM Sentiment — Dual-Signal Trading Strategy](trading/rsi-llm-signal-strategy.md) | Hybrid strategy combining a backward-looking momentum indicator (RSI) with a forward-looking LLM news sentiment signal. Both must agree before a tr... | 2026-04-17 |

## Decisions (ADRs)
*Why Cameron chose approach X over Y.*

| Page | Summary | Updated |
|------|---------|---------|
| ["ADR: 90-Day Rotating Retention for Trading Decisions Log"](decisions/autotrader-decisions-log-retention.md) | Rotate `logs/decisions.jsonl` on a 90-day window. Keep `logs/outcomes.jsonl` and `logs/daily_review.jsonl` indefinitely. | 2026-04-17 |
| ["ADR: Consensus-Based Memory Distillation"](decisions/consensus-based-memory-distillation.md) | Current agentic systems (e.g., wiki/trading/autotrader.md|AutoTrader) rely on a single-pass wiki/techniques/llm-review-pass-before-rotation.md|LLM ... | 2026-04-17 |
| ["ADR: Custom Provider Adapters vs. LiteLLM for ARC-AGI Harness"](decisions/arc-agi-adapters-vs-litellm.md) | The ARC-AGI benchmarking harness needs to run tasks against models from OpenAI, Anthropic, Google, and Grok. Two obvious approaches: | 2026-04-17 |
| ["ADR: Metadata Scoring vs. Embeddings for Text Search (SofaScope)"](decisions/sofascope-metadata-vs-embeddings.md) | Use custom field-weighted metadata scoring for text search instead of embedding-based semantic search. | 2026-04-17 |
| ["ADR: Open Model (Llama 3.3 70B) vs. Frontier Model for Trading Sentiment"](decisions/autotrader-open-model-vs-frontier.md) | Use Llama 3.3 70B via HuggingFace Inference API for news sentiment analysis rather than a frontier model (GPT-4o, Claude Sonnet). | 2026-04-17 |
| ["ADR: Persistent Python Service via stdin/stdout vs. HTTP (SofaScope)"](decisions/sofascope-persistent-service-stdin-stdout.md) | Run the persistent CLIP/FAISS Python service as a long-lived subprocess communicating with the Next.js host via stdin/stdout JSON, rather than as a... | 2026-04-17 |
| ["ADR: Wiki Retention Policy — When to Archive vs. Prune Speculative Pages"](decisions/wiki-retention-policy.md) | Apply the same retain-outcomes-rotate-reasoning principle from wiki/decisions/autotrader-decisions-log-retention.md to this wiki itself: | 2026-04-17 |

## Interview Prep

| Page | Summary | Updated |
|------|---------|---------|
| [System Design — Visual Search at Scale (SofaScope)](interview-prep/system-design-visual-search.md) | Interview preparation grounded in real production work at FLS. | 2026-04-17 |

## Comparisons

| Page | Summary | Updated |
|------|---------|---------|
| [LLM Wiki vs. RAG — Architectural Comparison](comparisons/llm-wiki-vs-rag.md) | Two fundamentally different approaches to LLM + documents. Cameron has built production systems using both. | 2026-04-17 |

## Open Questions

| Page | Summary | Updated |
|------|---------|---------|
| [Open Question — Agentic Memory Retention Strategies](open-questions/agentic-memory-retention-strategies.md) | Surfaced from AutoTrader's 90-day rotating `decisions.jsonl`. The general problem: what should an agentic system remember vs. forget, and for how l... | 2026-04-17 |

## Methodology
*How this wiki system works.*

| Page | Summary | Updated |
|------|---------|---------|
| [Cameron's Wiki — Setup and Adaptations](methodology/cameron-wiki-setup.md) | How this wiki instantiates Karpathy's LLM Wiki pattern, and what was adapted for Cameron's broader context. | 2026-04-17 |
| [The LLM Wiki Pattern (Karpathy, April 2026)](methodology/llm-wiki-pattern.md) | A pattern for building persistent, compounding personal knowledge bases using LLMs. Published April 4, 2026 as a GitHub gist by Andrej Karpathy. 5,... | 2026-04-17 |
