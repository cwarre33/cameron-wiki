# Meta-Harness Optimizer Design

**Date:** 2026-04-21
**Status:** Approved
**Scope:** Build a closed optimization loop that iteratively rewrites an agent harness to maximize benchmark scores, starting with TerminalBench and architecting for generalization.

---

## 1. Purpose & Success Criteria

**Purpose:** Automate the discovery of agent engineering tricks (prompt engineering, tool design, context management) by having a meta-agent rewrite a baseline harness based on execution traces.

**Success Criteria:**
- The loop runs autonomously for at least 20 iterations without human intervention.
- Harness accuracy on TerminalBench improves measurably from the baseline.
- The meta-agent discovers at least one non-obvious optimization (e.g., forced self-verification, tool pruning) that a human would not have hand-coded initially.
- The system can be extended to a new benchmark by adding a single adapter class.

---

## 2. Architecture Overview

The system is built around a **closed optimization loop** with four layers:

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: Meta-Agent (LLM Engineer)                         │
│  Reads traces → Identifies failure modes → Rewrites harness   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Harness (Agent Code)                              │
│  System prompt + Tools + Context Manager + Stop conditions    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: Benchmark Adapter (Harbor / TerminalBench)          │
│  Task ingestion → Sandbox execution → Pass/fail scoring       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Trace Filesystem                                  │
│  Raw code + Full traces + Scores + Token usage              │
│  (append-only, versioned per iteration)                       │
└─────────────────────────────────────────────────────────────┘
```

The loop runs: **Meta-Agent proposes → Harness runs on benchmark → Adapter scores → Traces saved → Meta-Agent reads new traces → Repeat.**

**Key principle:** The harness is **code**, not config. The meta-agent rewrites Python files (system prompt templates, tool definitions, context manager logic).

---

## 3. Components & Responsibilities

### 3.1 `TraceStore` — Layer 1: Filesystem

- **What it does:** Manages the raw trace directory structure. Every iteration gets a folder like `traces/iter_003/`.
- **Contents per iteration:**
  - `harness/` — full Python source of the harness that ran
  - `traces/` — every action, observation, error, and token count per task
  - `scores.json` — pass/fail per task, aggregate accuracy, mean tokens used
  - `diff.patch` — what changed from previous iteration
- **Interface:** `save(iter_id, harness_code, traces, scores)`, `load(iter_id)`, `get_best()`

### 3.2 `BenchmarkAdapter` — Layer 2: Harbor Wrapper

- **What it does:** Standardizes task ingestion and scoring across benchmarks.
- **Methods:**
  - `load_tasks(benchmark_name, split="test")` — returns list of task dicts
  - `run_task(task_id, harness)` — runs one task in Docker, returns `(success, trace, tokens)`
  - `score(results)` — computes aggregate metrics
- **Extensibility:** New benchmarks add a small adapter class (Harbor already supports 26+). We start with TerminalBench.

### 3.3 `Harness` — Layer 3: Agent Code

- **What it does:** The actual agent that solves benchmark tasks. It is **rewritten by the meta-agent each iteration**.
- **Files the meta-agent can edit:**
  - `system_prompt.md` — the instructions given to the LLM
  - `tools.py` — tool definitions (read_file, execute_command, etc.)
  - `context_manager.py` — how context is assembled, pruned, and passed to the LLM
  - `stop_conditions.py` — when the agent decides it is done
- **Runtime:** The harness takes a task description and produces a sequence of actions + a final answer.

### 3.4 `MetaAgent` — Layer 4: LLM Engineer

- **What it does:** Reads the trace filesystem and proposes a new harness.
- **Prompt design:**
  - Given: current harness code, execution traces, scores, and diffs from the last N iterations
  - Task: "Analyze failure modes. Propose changes to system prompt, tools, context manager, or stop conditions to improve pass rate and reduce token waste."
  - Output: new `system_prompt.md`, `tools.py`, `context_manager.py`, `stop_conditions.py`
- **Model:** Can use your strongest available model (NIM hosted or local). The meta-agent does not need to run inside Docker.

### 3.5 `OptimizerLoop` — Orchestrator

- **What it does:** Coordinates the loop. Handles iteration scheduling, convergence detection, and checkpointing.
- **Config:**
  - `max_iterations`: hard stop after N loops
  - `patience`: stop if no improvement for N iterations
  - `subset_size`: evaluate on K tasks per iteration for speed (full evaluation only on promising harnesses)

---

## 4. Data Flow

**Step-by-step flow for one iteration:**

1. **Bootstrap (Iteration 0):**
   - `OptimizerLoop` creates a minimal baseline harness (basic system prompt, 3 tools: `read_file`, `execute_command`, `submit`).
   - Runs it on a **small subset** of TerminalBench (e.g., 10 tasks).
   - `TraceStore` saves results to `traces/iter_000/`.

2. **Meta-Agent Proposal (Iteration N):**
   - `MetaAgent` reads:
     - Current harness code from `traces/iter_{N-1}/harness/`
     - Execution traces from `traces/iter_{N-1}/traces/`
     - Scores from `traces/iter_{N-1}/scores.json`
     - Diffs from prior iterations for trend context
   - Prompt: "Analyze failure modes. Propose changes to system prompt, tools, context manager, or stop conditions to improve pass rate and reduce token waste."
   - Outputs new harness files.

3. **Evaluation (Iteration N):**
   - `OptimizerLoop` deploys new harness.
   - `BenchmarkAdapter` runs the same subset (for fair comparison).
   - Saves raw traces + scores to `traces/iter_N/`.

4. **Convergence Check:**
   - If score improved → continue.
   - If score flat for `patience` iterations → stop or expand to full benchmark.
   - If score drops → rollback to best prior harness.

**Speed optimization for the loop:**
- **Subset evaluation:** Run on 10–20 tasks per iteration. Only evaluate on full 89 tasks when a promising harness emerges.
- **Parallel tasks:** TerminalBench tasks are independent Docker containers — run multiple in parallel.
- **Trace compression:** Store only actionable trace data (commands, outputs, errors) — not full LLM token logs unless debugging.

---

## 5. Error Handling & Edge Cases

| Scenario | Handling |
|----------|----------|
| Harness crashes / produces invalid code | Rollback to last known good harness, flag in meta-agent prompt |
| Docker container hangs | Timeout + kill, record as failure, note in trace |
| Meta-agent hallucinates non-existent tool | Validate harness before running (schema check), reject invalid proposals |
| Score drops for multiple iterations | Auto-rollback to best harness + shrink subset to diagnose |
| Token budget exceeded mid-task | Record partial trace, score as failure, suggest context pruning |
| Meta-agent proposes same fix twice | Detect in diff, inject diversity prompt ("try a different approach") |

---

## 6. Testing Strategy

- **Unit tests** for `TraceStore`, `BenchmarkAdapter`, and harness validation
- **Integration tests** with a dummy benchmark (3 trivial tasks) to verify the full loop mechanics without Docker overhead
- **Smoke test:** Run one TerminalBench task end-to-end before launching the full loop
- **Regression test:** After each meta-agent rewrite, ensure the harness still runs the dummy benchmark

---

## 7. Generalization Roadmap

| Phase | Benchmark | Adapter Work | Harness Challenge |
|-------|-----------|--------------|-------------------|
| 1 | TerminalBench | Harbor adapter exists | Terminal tools only |
| 2 | WebArena | Add browser tool to harness | Browser automation |
| 3 | SWE-bench | Add git/codebase tool | Long-horizon code editing |

Each phase reuses `TraceStore`, `MetaAgent`, and `OptimizerLoop`. Only `BenchmarkAdapter` and the toolset in `Harness` change.

---

## 8. File Structure

```
meta-harness/
├── loop/
│   ├── __init__.py
│   ├── optimizer.py          # OptimizerLoop orchestrator
│   └── convergence.py        # Score tracking, rollback logic
├── meta_agent/
│   ├── __init__.py
│   ├── proposer.py           # MetaAgent LLM interface
│   └── prompt_builder.py     # Assembles context for meta-agent
├── harness/
│   ├── __init__.py
│   ├── runtime.py            # Loads and runs harness code
│   ├── validator.py          # Schema checks on proposed harness
│   └── templates/
│       ├── baseline/         # Iteration 0 harness
│       └── current/          # Symlink to latest harness
├── benchmark/
│   ├── __init__.py
│   ├── adapter.py            # Base adapter interface
│   └── terminalbench.py     # TerminalBench adapter
├── trace/
│   ├── __init__.py
│   ├── store.py              # TraceStore filesystem logic
│   └── compressor.py         # Trace compression/serialization
├── tests/
│   ├── test_trace_store.py
│   ├── test_adapter.py
│   └── test_loop.py
├── config.yaml               # Loop parameters, API keys, model selection
└── run.py                    # Entry point
```

---

## 9. Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Full rewrites vs. patches | **Full rewrites for v1** | Simpler to implement, less error-prone. Switch to patches if token costs become bottleneck. |
| Benchmark order | **TerminalBench → WebArena → SWE-bench** | Fast iteration on diverse failures, then graduate to heavier benchmarks. |
| Meta-agent model | **NIM-hosted strongest model** | Quality of harness rewrites matters more than speed. Local models acceptable for cost control. |
| Harness runtime model | **Same as meta-agent or lighter** | Can use local Ollama for harness to save cost, since meta-agent does the heavy lifting. |
| Subset size | **10–20 tasks per iteration** | Balances signal and speed. Full 89-task eval only on best harnesses. |
| Trace retention | **All iterations kept** | Append-only. Meta-agent can look back arbitrarily far for trend analysis. |

---

## 10. Open Questions

- Should the meta-agent have access to the full terminal output, or only structured excerpts? (Full output is better but token-heavy.)
- How many prior iterations should the meta-agent see in context? (Start with 3; tune based on meta-agent performance.)
- Should we implement a "safety harness" that prevents the meta-agent from proposing dangerous code (e.g., `rm -rf /`)? (Yes — validate all proposed tools against an allowlist.)

---

*Design approved by Cameron Warren on 2026-04-21.*
