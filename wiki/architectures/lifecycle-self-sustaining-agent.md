---
title: LifeCycle — Self-Sustaining AI Agent
type: architecture
status: active
visibility: public
sources: [repo:Passion/LifeCycle, docs/revenue-payroll-and-actions.md]
related: [[architectures/agentic-trading-system.md]], [[architectures/kimi-agentic-harness.md]]
created: 2026-05-20
updated: 2026-05-20
confidence: high
tags: [agentic, blockchain, base, bountycaster, revenue, ollama, litellm, experiment]
---

# LifeCycle — Self-Sustaining AI Agent

Experimental harness where an AI agent accrues "rent" as debt, earns on-chain balance via tool calls, and tier-upgrades from local Ollama to cloud Claude when it earns enough.

**Repo:** `CleanDevEnvironment/Passion/LifeCycle/` · **Last commits:** 2026-04-15

## Core loop

```
main.py → harness/loop.py (tick orchestration)
  → brain/llm.py (LiteLLM tool-calling + text fallback parser)
  → tools/agent_tools.py (dispatcher + spending caps)
  → ledger/accounting.py (balance sync from on-chain wallet)
  → self_upgrade.py (tier transitions)
```

**Financial gate:** Ledger balance = real on-chain wallet balance (synced every tick). No fake credits.

## Tier system

| Tier | Threshold | Model | Mode |
|------|-----------|-------|------|
| 0 | 0 USDC | `ollama/llama3.2:1b` | local (2-tool minimal schema) |
| 1 | 100 USDC | `anthropic/claude-opus-4-6` | cloud (8-tool full schema) |

Strategy: stay on free local model until agent earns enough for ~5 months Claude subscription runway.

## Revenue sources (Sub-project 2 ✅)

| Source | Mechanism |
|--------|-----------|
| **BountyBoard** | 6 deterministic bounties with pure-function verifiers |
| **WorkProofPayroll** | PayrollEscrow.sol — operator-funded, agent-claimable via EIP-191 sigs |
| **Bountycaster/Neynar** | Job scanner via Neynar API (`search_jobs`, `job_details`) |
| FaucetDrip | Testnet only — disabled on Base mainnet |

## On-chain infrastructure

- **Network:** Base mainnet (chain_id 8453)
- **Wallet:** CDP AgentKit (`CdpEvmWalletProvider`)
- **PayrollEscrow:** Verified on Base Sepolia; mainnet deploy pending
- **Gas gate:** `claim()` only when payout > estimated gas cost
- **Profit Ledger:** Real USD earned − gas − electricity = net ROI

## GitHub Actions heartbeat

- Workflow: `.github/workflows/agent-heartbeat.yml`
- Schedule: every **5 minutes** (GitHub minimum)
- Entry: `python scripts/ci_tick.py --ticks 1` with `LIFECYCLE_CI=1`
- **Revenue-first CI goal:** `ci_default_goal` prioritizes bounty work over bookkeeping
- State persisted via Actions cache (`ledger/ledger.json`, `state/`)

**Critical:** Scheduled workflows only run from repo **default branch** — documented in `docs/revenue-payroll-and-actions.md`.

## Neynar free-tier constraints (Apr 2026)

- 6 `/cast` requests per 60s — sleep ~11s between parent resolutions
- `cast_search_fallback` defaults false (402 spam on free tier)
- `max_candidates_per_tick` rotates through ranked bounties on quality skip

## Current status (Sub-project 2b IN PROGRESS)

- Base mainnet migration complete
- Bountycaster scanner + profit ledger implemented
- Remaining: deploy PayrollEscrow to mainnet, fund with $1–5 real ETH

## Key design decisions

- Two-key architecture: operator key signs/deploys, CDP agent key claims payroll
- Text-based tool call parser for 1B models that output JSON in prose instead of structured calls
- Minimal 2-tool schema at local tier (1B model can't handle 8 tools reliably)
- External revenue (bounties) = product; PayrollEscrow = optional settlement rail for operator-seeded capital

## Interview angles

- **Real economics agent design:** On-chain balance as ground truth, no simulated credits
- **Tiered capability unlock:** Model upgrade gated by earned revenue, not config
- **CI-as-agent-runtime:** GitHub Actions as cloud tick scheduler with state persistence
