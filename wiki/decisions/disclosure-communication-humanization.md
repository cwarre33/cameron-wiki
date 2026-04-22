---
title: Disclosure Communication Humanization — The atuinsh/atuin Incident
type: decision
status: active
visibility: public
sources: [reports/JACKPOT_LIVE_CREDENTIAL_20260420.json, raw/osint/live_credential_hunter.py]
related: [wiki/techniques/shodan-ics-osint.md, wiki/open-questions/disclosure-letters-2026-04-20.md]
created: 2026-04-22
updated: 2026-04-22
confidence: high
tags: [responsible-disclosure, ai-communication, reputation, open-source, lesson-learned]
---

# Disclosure Communication Humanization — The atuinsh/atuin Incident

## What happened

On 2026-04-21, a disclosure was submitted to `atuinsh/atuin` (20k+ stars) via GitHub Issue #3438:

> **Title:** Security Disclosure: Exposed Token Pattern in secrets.rs  
> **Finding:** `ghp_R2***2muH` in `crates/atuin-client/src/secrets.rs`  
> **Format:** Templated "security researcher" disclosure with structured body, severity labeling, and remediation checklist

**Maintainer response (Ellie Huxtable):**

- "lol what?"
- "just no dude"
- "tell your claude to stand down"

**Consequence:** Blocked from the `atuinsh` organization on GitHub.

## Why the response was hostile

The finding itself — a test/example token in a test file — was likely not a genuine vulnerability. But the **delivery format** made it worse:

| Signal detected | How it read to the maintainer |
|-----------------|------------------------------|
| Over-structured template (bullet lists, severity labels, numbered actions) | "This is a form letter" |
| Formal "security researcher" sign-off | "This person is role-playing authority over my project" |
| Long remediation checklist for a one-line test token | "This person doesn't understand what they're looking at" |
| No uncertainty or humility | "They think they found something when they haven't" |
| The pattern matched a known AI disclosure template | "This was written by an LLM, not a person" |

The maintainer's "tell your claude to stand down" confirms the disclosure was **immediately recognized as AI-generated**. The block was the consequence.

## Root cause analysis

**Finding quality:** The token `ghp_R2***2muH` was likely a **test/example credential** — a common pattern in `secrets.rs` test files. GitHub PATs with `ghp_` prefix in `*_test.go`, `*_test.rs`, `test_*.py`, or `secrets.rs` in a shell-history project are overwhelmingly test fixtures, not production leaks.

**Delivery quality:** The disclosure was long, templated, and treated a probable test token as a production security incident. It did not acknowledge uncertainty. It did not show that the finder understood the codebase context.

**Process quality:** The disclosure was generated from a template batch without per-finding human review of whether the finding was worth reporting at all.

## What to do differently

### Tier 1: Don't disclose at all

If any of these are true, **do not open a security issue** — open a regular discussion or say nothing:

- The file name contains `test`, `spec`, `mock`, `fixture`, `example`, or `sample`
- The token is in a `secrets.rs` file in a shell-history/crypto project (where test tokens are expected)
- The token format matches known test patterns (`ghp_` with `test`, `example`, `demo`, or short/random-looking value)
- The repository has 10k+ stars and active maintainers (they have secret scanning enabled; GitHub would have flagged a real leak)
- The finding is a single credential with no evidence of production use

### Tier 2: If disclosure is warranted, humanize first

**Before sending:** Rewrite the message as if speaking to a person, not filing a ticket.

| Instead of | Use |
|------------|-----|
| "I am a security researcher conducting an audit..." | "Hey — noticed something that might be worth a look:" |
| "Severity: MEDIUM" | (delete entirely) |
| "Recommended immediate actions:" | "Not sure if this matters, but figured I'd flag it:" |
| Numbered remediation checklist | One or two sentences max |
| Formal sign-off with title | First name only, no "security researcher" |

**Example of a humanized version for the same finding:**

> Hey — noticed a `ghp_` token in `crates/atuin-client/src/secrets.rs`. Looks like it might be a test fixture, but wanted to flag it just in case it's not. No worries if it's intentional.

That's it. One sentence of context, one sentence of uncertainty, done.

### Tier 3: Post-incident reputation repair

- Do not attempt to contact the maintainer again from another account
- Do not argue the finding was valid
- Do not post about the incident publicly in a way that names the maintainer
- Accept the block as a lesson and move on
- If the block prevents future legitimate contributions, consider a polite, brief appeal after 6+ months

## The cost

Being blocked from `atuinsh/atuin` means:

- Cannot open issues or PRs
- Cannot participate in discussions
- Cannot report future legitimate bugs
- Public block record is visible to other maintainers
- The incident is searchable in GitHub's public issue history

This is a **reputation event** that other maintainers may reference. Future disclosures must be significantly more careful to avoid being perceived as the same pattern.

## Decision

- **Bulk disclosure templates are banned** for findings in repositories with >1k stars or active maintainers
- **Every disclosure to a popular repo gets a human rewrite** — no exceptions
- **Test/fixture/context-aware findings get a "should I even send this?" gate** before any draft is written
- **Disclosure sign-off is first name only** — no "security researcher", no university affiliation, no formal title
- **Max disclosure length for GitHub issues: 3 sentences** unless the finding is genuinely critical and complex
- **All future disclosures get a 5-minute cooling-off period** before posting

## Open questions

- Should the live credential hunter be modified to flag test-file patterns and auto-skip them?
- Should there be a separate "low-confidence ping" workflow (e.g., tweet/DM) vs. "formal disclosure" workflow?
- How do we repair reputation with the Rust/open-source community after a visible block?
