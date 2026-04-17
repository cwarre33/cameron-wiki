# Wiki Index

Master catalog of all wiki pages. Updated on every ingest.

---

## Production Systems
*Cameron's FLS production engineering work.*

| Page | Summary | Status | Visibility | Updated |
|------|---------|--------|------------|---------|
| [SofaScope](production-systems/sofascope.md) | CLIP+FAISS visual search over 200k furniture products; 16.8s→<500ms via persistent model loading | active | public | 2026-04-17 |

## Architectures
*Serverless patterns, agent systems, transformer family, retrieval systems.*

| Page | Summary | Updated |
|------|---------|---------|
| [Agentic Trading System](architectures/agentic-trading-system.md) | Containerized scheduled LLM agent with persistent JSONL feedback loop; Docker + cron + Gradio | 2026-04-17 |
| [Provider Adapter Pattern](architectures/provider-adapter-pattern.md) | Strategy pattern for multi-provider LLM clients; swap models via config, not code | 2026-04-17 |

## Techniques
*CLIP+FAISS, Whisper pipelines, routing algorithms, MBR decoding, etc.*

| Page | Summary | Updated |
|------|---------|---------|
| [CLIP + FAISS Visual Search Pipeline](techniques/clip-faiss-visual-search.md) | Full pipeline: Base64→CLIP→FAISS→results; IndexFlatIP+L2 norm=cosine similarity | 2026-04-17 |
| [Persistent Model Loading Pattern](techniques/persistent-model-loading.md) | Load ML models once at startup; never per-request. Patterns: subprocess, FastAPI, gunicorn preload | 2026-04-17 |
| [Hybrid Search Routing (Text + Image)](techniques/hybrid-search-routing.md) | Route queries to optimal engine by modality; metadata for structured text, embeddings for images | 2026-04-17 |
| [MBR Decoding](techniques/mbr-decoding.md) | Minimum Bayes Risk: sample N candidates, pick consensus; beats beam search on low-resource NLP | 2026-04-17 |
| [LLM Review Pass Before Rotation](techniques/llm-review-pass-before-rotation.md) | Distill durable lessons from time-bounded logs before purging; completes the agentic self-improvement loop | 2026-04-17 |

## Integrations
*Zendesk API, NetSuite/SuiteQL, AWS, MiCollab, Groq, Copilot Studio.*

| Page | Summary | Updated |
|------|---------|---------|
| [Alpaca API](integrations/alpaca-api.md) | Paper + live trading API; identical interface, swap credentials; News API for sentiment | 2026-04-17 |

## Papers
*Formal published research summaries.*

| Page | Summary | Updated |
|------|---------|---------|
| *(none yet)* | | |

## Models

| Page | Summary | Updated |
|------|---------|---------|
| [CLIP](models/clip.md) | OpenAI vision-language model; clip-vit-large-patch14 (768-dim); zero-shot visual similarity | 2026-04-17 |
| [ByT5](models/byt5.md) | Google byte-level T5; no tokenizer; native rare-script coverage; used for Akkadian translation | 2026-04-17 |

## Benchmarks

| Page | Summary | Updated |
|------|---------|---------|
| [ARC-AGI](benchmarks/arc-agi.md) | Chollet's anti-contamination reasoning benchmark; novel visual grid tasks; ARC-AGI-1 + ARC-AGI-2 | 2026-04-17 |

## Datasets

| Page | Summary | Updated |
|------|---------|---------|
| *(none yet)* | | |

## Tools

| Page | Summary | Updated |
|------|---------|---------|
| [FAISS](tools/faiss.md) | Meta vector similarity search; IndexFlatIP, IVFFlat, HNSW; cosine similarity via L2 norm trick | 2026-04-17 |

## Labs

| Page | Summary | Updated |
|------|---------|---------|
| *(none yet)* | | |

## People

| Page | Summary | Updated |
|------|---------|---------|
| [Andrej Karpathy](people/andrej-karpathy.md) | AI researcher/educator; LLM Wiki pattern, nanoGPT, Neural Networks Zero to Hero | 2026-04-17 |

## Kaggle Competitions

| Page | Summary | Competition | Updated |
|------|---------|-------------|---------|
| [ARC-AGI Benchmarking Harness](kaggle/arc-agi-benchmarking.md) | Async multi-provider LLM test harness for ARC-AGI-1 and ARC-AGI-2; provider adapter pattern + cost tracking | ARC Prize | 2026-04-17 |
| [ARC Prize 2025](kaggle/arc-prize-2025.md) | $1M competition; Cameron ran LLM inference loops via harness; grand prize unclaimed | ARC Prize 2025 | 2026-04-17 |
| [Deep Past: Akkadian Translation](kaggle/deep-past-akkadian-translation.md) | ByT5 + MBR pipeline; score 34.7; found + documented data leakage → first place | Deep Past ($50k) | 2026-04-17 |
| [Motion-S: Text-to-Sign](kaggle/motion-s-text-to-sign.md) | Rank 25; TF-IDF + kNN retrieval; 2% below #1; competition still active | Motion-S (Kudos) | 2026-04-17 |
| [Stanford RNA 3D Folding](kaggle/stanford-rna-3d-folding.md) | Pseudo-labeling + multi-GPU embeddings; studied top-1 solution; bioinformatics generalist entry | Stanford RNA ($75k) | 2026-04-17 |
| [UrbanFloodBench](kaggle/urban-flood-modelling.md) | Rank 117; geospatial flood prediction; exploratory entry | Urban Flood ($7k) | 2026-04-17 |
| [Hull Tactical Market Prediction](kaggle/hull-tactical-market-prediction.md) | ACTIVE ($100k, deadline 2026-06-16); quant finance; connects to AutoTrader work | Hull Tactical | 2026-04-17 |

## Trading

| Page | Summary | Updated |
|------|---------|---------|
| [AutoTrader](trading/autotrader.md) | RSI + LLM sentiment paper trading bot; Llama 3.3 70B + Alpaca; self-improvement JSONL loop | 2026-04-17 |
| [RSI + LLM Signal Strategy](trading/rsi-llm-signal-strategy.md) | Dual-signal gate: RSI momentum + LLM news sentiment must both agree; 5% position cap | 2026-04-17 |

## Decisions (ADRs)
*Why Cameron chose approach X over Y. Interview-ready architectural reasoning.*

| Page | Summary | Updated |
|------|---------|---------|
| [Metadata Scoring vs. Embeddings for Text Search](decisions/sofascope-metadata-vs-embeddings.md) | SofaScope: metadata scoring 55× faster, zero cost, 92% accuracy vs embedding-based search | 2026-04-17 |
| [Persistent Service: stdin/stdout vs. HTTP](decisions/sofascope-persistent-service-stdin-stdout.md) | SofaScope: subprocess IPC chosen over HTTP for single-caller pilot simplicity | 2026-04-17 |
| [Open Model vs. Frontier for Trading Sentiment](decisions/autotrader-open-model-vs-frontier.md) | AutoTrader: Llama 3.3 70B 10× cheaper than GPT-4o; task complexity fits open model | 2026-04-17 |
| [90-Day Rotating Retention for Decisions Log](decisions/autotrader-decisions-log-retention.md) | AutoTrader: recency bias intentional; rotate reasoning context, keep outcomes indefinitely | 2026-04-17 |
| [Custom Adapters vs. LiteLLM](decisions/arc-agi-adapters-vs-litellm.md) | ARC-AGI harness: custom adapters chosen for full control over request/response; LiteLLM tradeoffs documented | 2026-04-17 |
| [Wiki Retention Policy](decisions/wiki-retention-policy.md) | Retain ADRs + outcomes forever; prune speculative pages after 90-day staleness + no inbound links; LLM review pass before deletion | 2026-04-17 |

## Interview Prep

| Page | Summary | Updated |
|------|---------|---------|
| [System Design — Visual Search at Scale](interview-prep/system-design-visual-search.md) | SofaScope story: profiling, architecture decisions, scale follow-ups, resume bullet | 2026-04-17 |

## Comparisons

| Page | Summary | Updated |
|------|---------|---------|
| [LLM Wiki vs. RAG](comparisons/llm-wiki-vs-rag.md) | Intelligence at ingest time vs. query time; Cameron has built both; when each wins | 2026-04-17 |

## Open Questions

| Page | Summary | Updated |
|------|---------|---------|
| [Agentic Memory Retention Strategies](open-questions/agentic-memory-retention-strategies.md) | What should agents remember vs. forget? Regime-aware retention, adaptive windows, LLM review passes | 2026-04-17 |

## Methodology
*How this wiki system works.*

| Page | Summary | Updated |
|------|---------|---------|
| [The LLM Wiki Pattern](methodology/llm-wiki-pattern.md) | Karpathy's pattern: compile at ingest, not query time; Memex lineage; three layers + three operations | 2026-04-17 |
| [Cameron's Wiki Setup](methodology/cameron-wiki-setup.md) | How this wiki adapts the pattern: broader taxonomy, decisions/ ADRs, portfolio extraction, visibility model | 2026-04-17 |
