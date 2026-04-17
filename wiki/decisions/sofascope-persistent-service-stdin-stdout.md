---
title: "ADR: Persistent Python Service via stdin/stdout vs. HTTP (SofaScope)"
type: decision
status: active
visibility: public
sources: [raw/repos/sofascope-ai-powered-product-match-finder.md]
related: [wiki/production-systems/sofascope.md, wiki/techniques/persistent-model-loading.md, wiki/techniques/clip-faiss-visual-search.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [adr, architecture, python, subprocess, ipc, ml-serving, furnitureland-south]
---

# ADR: Persistent Python Service via stdin/stdout vs. HTTP (SofaScope)

## Decision

Run the persistent CLIP/FAISS Python service as a long-lived subprocess communicating with the Next.js host via stdin/stdout JSON, rather than as a separate HTTP server.

## Context

CLIP model loading takes ~2.5 seconds per request when instantiated inside a serverless/per-request handler. The fix requires keeping the model loaded between requests. Two primary patterns exist: subprocess IPC or a separate HTTP server.

The deployment target is a single-machine pilot environment (not a Kubernetes cluster or auto-scaling setup).

## Options considered

| Option | Complexity | Port management | Health checks | Independent scaling | Overhead |
|--------|-----------|-----------------|---------------|--------------------| ---------|
| **Subprocess stdin/stdout** | **Low** | **None** | **Via stdout signal** | **No** | **Minimal** |
| FastAPI/Flask HTTP server | Medium | Required | HTTP /health | Yes | HTTP stack |
| Model server (Triton, TorchServe) | High | Required | Full HTTP | Yes | Significant |

## Decision rationale

1. **No port management** — no need to assign, expose, or secure a port; the subprocess is owned by the Next.js process
2. **Single deployment unit** — Next.js + Python service start and stop together; no separate process management
3. **Minimal overhead** — stdin/stdout JSON adds ~0ms vs HTTP which adds TCP stack overhead
4. **Sufficient for pilot** — single-caller (one Next.js process) with fallback to standard search if service crashes

## Startup handshake

```python
# Service prints this when ready
print("SERVICE_READY", flush=True)
```

Next.js waits for `SERVICE_READY` before routing requests. If the line never arrives (startup failure), it falls back to the standard (per-request) image search endpoint.

## Tradeoffs accepted

- **Single caller only** — stdin/stdout is 1:1; if multiple Next.js workers need CLIP, this pattern breaks (need HTTP or a message queue)
- **No independent scaling** — can't scale the Python service separately from the web server
- **Harder to monitor** — no HTTP health endpoint; requires log parsing or stdout signals for observability
- **Process coupling** — if Next.js crashes and restarts, the Python subprocess must also restart

## When this pattern breaks down

Move to HTTP (FastAPI) when:
- Multiple callers need the model simultaneously
- Independent horizontal scaling is needed
- A dedicated model server with batching (Triton) would improve throughput

## Outcome

- Zero port conflicts in pilot deployment
- Automatic fallback if service fails to start
- ~0ms IPC overhead vs model inference time
