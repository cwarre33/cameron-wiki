# Responsible Disclosure Report - April 20, 2026

## Executive Summary

During OSINT security research, I discovered **5 exposed credentials** across 
multiple open-source GitHub repositories.

## Discoveries

### #1: ATUIN Shell History (atuinsh/atuin)
- **File:** crates/atuin-client/src/secrets.rs
- **Type:** GitHub PAT (Classic)
- **Severity:** MEDIUM
- **Status:** Test/example credential in popular project (20k+ stars)

### #2: openworkflowdev/openworkflow  
- **Type:** PostgreSQL Database URL
- **Severity:** HIGH
- **Risk:** Database compromise if production

### #3: pplcallmesatz/svgtofont
- **Type:** PostgreSQL Database URL
- **Severity:** HIGH

### #4: ayoubagrebi062-hue/olympus-2.0
- **Types:** PostgreSQL URL + Plaintext Password
- **Severity:** HIGH

### #5: codename-co/devs
- **Types:** GitHub PAT + PostgreSQL URL
- **Severity:** HIGH
- **Risk:** Complete system compromise (code + database)

## Disclosure Timeline

- **Day 0 (Today):** Initial outreach to maintainers
- **Day 3:** Follow-up if no acknowledgment
- **Day 7:** Public disclosure consideration

## Tools Used

- live_credential_hunter.py
- bulk_credential_hunter.py
- GitHub Search API

## Ethical Statement

- ✅ Credentials NOT accessed or used
- ✅ Only redacted values documented
- ✅ 7-day responsible disclosure timeline
- ✅ Public disclosure only if necessary

Cameron Warren | Security Researcher
