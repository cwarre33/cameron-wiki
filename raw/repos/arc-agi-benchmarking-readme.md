# arc-agi-benchmarking — LLM Baseline Testing Harness for ARC-AGI
Source: https://github.com/cwarre33/arc-agi-benchmarking
Fetched: 2026-04-17
Note: Fork of arcprizeorg/model_baseline

---

Tests model baselines on ARC-AGI reasoning tasks. Supports OpenAI, Anthropic, Google providers.

## Architecture

- **Batch runner**: `cli/run_all.py` — asyncio concurrency, provider-level rate limiting, tenacity retries
- **Single task**: `main.py` — debug/single-task analysis
- **Provider adapters**: `src/arc_agi_benchmarking/adapters/` — one per provider, implement `ProviderAdapter`
- **Model config**: `src/arc_agi_benchmarking/models.yml` — model name, provider, max_tokens, temperature, pricing
- **Rate limiting**: `provider_config.yml` — per-provider requests/period config
- **Scoring**: `src/scoring/scoring.py` — validates submissions against ground truth

## Key features

- asyncio concurrency — multiple (task, model_config) pairs run simultaneously
- Provider-level rate limiting — configurable requests/period in provider_config.yml
- tenacity exponential backoff retries — handles transient API errors
- Multiple attempts per task — `--num_attempts` parameter
- ARC-AGI-1 and ARC-AGI-2 supported (same task format, different `--data_dir`)
- Metrics collection (disabled by default, `--enable-metrics`)
- HuggingFace upload pipeline for sharing submissions

## Provider adapter interface

```python
class MyProviderAdapter(ProviderAdapter):
    def init_client(self): ...
    def make_prediction(self, prompt: str) -> Attempt: ...
    def chat_completion(self, messages: str) -> str: ...
```

## models.yml structure

```yaml
models:
  - name: "config_name"
    model_name: "actual-model-name"
    provider: "openai|anthropic|gemini"
    max_tokens: 4024
    temperature: 0.0
    pricing:
      date: "YYYY-MM-DD"
      input: 0.00   # per 1M tokens
      output: 0.00
```

## Rate limit config (provider_config.yml)

```yaml
openai:
  rate: 5000
  period: 60
anthropic:
  rate: 1000
  period: 60
gemini:
  rate: 60
  period: 60
```

## Key CLI args (run_all.py)

- `--task_list_file` — .txt with task IDs (one per line)
- `--model_configs` — comma-separated model config names from models.yml
- `--num_attempts` — attempts per task (default: 2)
- `--retry_attempts` — internal retries for failed predictions (default: 2)
- `--log-level` — DEBUG/INFO/WARNING/ERROR/NONE
- `--enable-metrics` — collect performance timing (disabled by default)
- `--overwrite_submission` — overwrite existing results

## Tested providers

OpenAI (o1, gpt-4o), Anthropic (Claude Sonnet, Opus), Google (Gemini), Grok
