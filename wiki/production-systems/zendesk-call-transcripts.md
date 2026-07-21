---
title: Zendesk Call Auto-Transcript Pipeline
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/transcripts/2026-07-21-memory.md
  - raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md
  - raw/fls-work/jira/2026-07-21/cluster-map.md
  - repo:Zendesk/ZendeskCallAutoTranscript
related:
  - "[[initiatives/zendesk-automation-platform.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [zendesk, transcripts, whisper, groq, micollab, pii, task-server, furnitureland-south]
---

# Zendesk Call Auto-Transcript Pipeline

Production pipeline that attaches call transcripts (and summaries) to Zendesk tickets: download MiCollab recordings, preprocess audio, transcribe, correct names, summarize, redact PII, upload.

**Repo:** `CleanDevEnvironment/Zendesk/ZendeskTools/ZendeskCallAutoTranscript/`

**Jira footprint:** Thin on early assignee stories ([FLSI-2761](https://furniturelandsouth.atlassian.net/browse/FLSI-2761) local Whisper backfill, [FLSI-2762](https://furniturelandsouth.atlassian.net/browse/FLSI-2762) model eval — both **Done**) but the system is durable. Follow-on AWS / Task Server work in the same parent tree (FLSI-2763–2765, FLSI-2973, FLSI-2990–2994) is also **Done**. Separate cluster-map “Transcripts” bucket lists only FLSI-2761/2762; Zendesk automation cluster absorbs the AWS/Task Server siblings.

Umbrella: [[initiatives/zendesk-automation-platform.md]].

## Pipeline

```
Zendesk fetch (ticket ↔ recording refs)
  → MiCollab download
  → FFmpeg preprocess
  → Whisper / Groq Whisper transcribe
  → RapidFuzz name correction
  → LLM summarize / reflow
  → PII redact (CC, SSN, email, phone)
  → Zendesk upload
```

**Stereo convention:** left = agent (ch1), right = customer (ch2).

**Entry point:** `run.py` (`--model`, `--limit`, `--skip-upload`, `--engine`).

## Engines

| Engine | Module | Notes |
|--------|--------|-------|
| v1 legacy | `transcriber.py` | Older path |
| v2 optimized (default) | `transcriber_v2.py` | Channel detection, name detection, merge |
| Groq (Lambda-ready) | `groq_transcriber.py` | Stereo WAV → mono MP3 @64kbps (25MB limit) → parallel Groq Whisper; avoids torch imports |
| Groq LLM | `groq_llm.py` | `llama-3.1-8b-instant` for summarize/reflow (replaces Ollama when engine=groq) |
| PII | `redactor.py` | Shared across engines before upload |
| Orchestration | `pipeline.py` | Enrichment, download, idempotency |

Branch note (memory): `feature/groq-migration` holds Groq engine work.

## Ops artifacts

- `output/transcripts/` — cached transcripts (delete to re-run)
- `output/run_log.json` — last-run metrics
- Task Server path: create job → refactor → test → docs → Zendesk upload check (FLSI-2973 / 2992 / 2990 / 2991 / 2994)

## Hard-won fixes (2026-02)

From frozen transcript memory — keep these as regression watchlist:

- **"this is" name bug** — IGNORECASE regex treated “this is” as a name
- **Channel swap on outbound** — generic intro phrases overweight; agent-name + call_type awareness
- **Duplicate agent/customer name** — when requester_id == assignee_id, clear customer_name
- **Whisper hallucination loops** — “Bye. Bye…” end loops → `_deduplicate_repetitions`
- **Zero metrics on cache hit** — idempotent path must still count words
- **Aggressive segment merge** — 0.5s → 0.3s gap; simplified polished formatter

## Interview angles

- **Multi-engine transcription:** local Whisper vs Groq for Lambda size/cost constraints
- **PII before upload:** redaction as a hard gate, not a nicety
- **Jira lag vs system maturity:** durable production system with sparse early ticket surface
