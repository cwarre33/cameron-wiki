---
title: BACnet FDT External-Cloud Tunnel Pattern — 12 Cases Observed
type: open-question
status: active
visibility: public
sources: [raw/osint/2026-04-20-longitudinal.json, raw/osint/2026-04-20-scan-enriched.json]
related: [wiki/open-questions/bacnet-bbmd-exposure-2026-04-19.md, wiki/open-questions/walkermedical-disclosure-2026-04-19.md, wiki/open-questions/homanit-disclosure-2026-04-20.md, wiki/open-questions/kipp-mitchell-disclosure-2026-04-20.md, wiki/techniques/shodan-ics-osint.md]
created: 2026-04-21
updated: 2026-04-21
confidence: high
tags: [bacnet, bbmd, fdt, ics, cloud, digitalocean, azure, aws, shared-infrastructure, integrator, responsible-disclosure, survey]
---

# BACnet FDT External-Cloud Tunnel Pattern — 12 Cases Observed

## What this page is

An aggregate finding from the 2026-04-20 longitudinal Shodan pull over 17 seeded BBMDs. It surfaces a population-level pattern that was first spotted at [[homanit-disclosure-2026-04-20]] but is clearly not unique to Homanit: **BACnet Broadcast Management Devices on the public internet are routinely maintaining long-lived Foreign Device registrations with other public-internet IPs** — not just with their own internal RFC1918 networks (the [[walkermedical-disclosure-2026-04-19]] pattern).

This page lists every such case, ranks the most interesting, and queues them for per-target investigation and disclosure.

## Why this is a distinct class from WalkerMedical / KIPP

| Pattern | Description | Example | Disclosure target |
|---------|-------------|---------|-------------------|
| **Internal-FDT (Walker / KIPP)** | BBMD routes to RFC1918 hosts in its own building network. Standard if misconfigured. | `12.5.26.10 → 10.20.80.175` (KIPP) | Building operator |
| **External-FDT (Homanit and this population)** | BBMD has a Foreign Device entry whose IP is a **public, routable, non-RFC1918** address — often a cloud provider or a second ISP block | `85.206.88.54 → 157.245.127.71` (Homanit → DigitalOcean) | Building operator **and** the owner of the public endpoint |

The external-FDT pattern cannot be explained by normal BBMD operation. Possible explanations, each remediable:

1. **Legitimate SaaS / cloud monitoring** — a third-party BAS platform bridges into the building network through the FDT. The building operator usually knows this exists, but often not that it is internet-reachable with no auth.
2. **Integrator remote-access** — a BMS integrator's monitoring station (on its own public IP) registers as a Foreign Device to keep the operator-facing broadcast channel open. Shows up as a single static-port registration.
3. **Unauthorized bridge** — an attacker has registered their own Foreign Device with the BBMD to receive broadcasts and issue writes, possibly proxying from a cloud VPS to avoid attribution.

At this survey level we cannot distinguish (1)/(2)/(3). All three warrant remediation.

## The 12 cases

All tunnels below had `scan_count >= 3` over the 2026-03-04 → 2026-04-20 window. "External internal IP" means the Foreign-Device IP is publicly routable (not RFC1918 / CGNAT / loopback).

| # | Public BBMD | External FD IP | Scans | First seen | Last seen | Source ports | Notes |
|---|-------------|----------------|-------|------------|-----------|--------------|-------|
| 1 | `166.144.189.152` | `108.190.193.44` | 275 | 2026-03-05 | 2026-04-20 | **37 rotating** | Highest scan count with rotation. Almost certainly a NAT'd client repeatedly calling home. |
| 2 | `24.199.212.139` | `174.99.186.214` | 182 | 2026-03-04 | 2026-04-18 | 1 (static) | Static single-port ≈ direct/managed endpoint, not NAT. |
| 3 | `75.112.176.136` | `24.227.56.226` | 146 | 2026-03-11 | 2026-04-20 | 18 rotating | Second case of heavy rotation. Same-ISP block (`24.x`) — could be across-building integrator. |
| 4 | `85.206.88.54` | `157.245.127.71` | 126 | 2026-04-03 | 2026-04-20 | 1 (static) | **Homanit** — DigitalOcean NYC. Disclosure open. |
| 4 | `85.206.88.54` | `104.131.63.228` | 126 | 2026-04-03 | 2026-04-20 | 13 rotating | **Homanit** — DigitalOcean NYC. Paired with `157.245.*`. |
| 5 | `63.41.64.84` | `208.161.229.62` | 108 | 2026-03-04 | 2026-04-20 | 16 rotating | TTL mix (30/60) is unusual. Possibly two devices behind same NAT. |
| 6 | `66.58.248.125` | `216.67.73.166` | 108 | 2026-03-04 | 2026-04-20 | 13 rotating | **Shared with case #7** below. |
| 7 | `24.237.132.230` | `216.67.73.166` | 104 | 2026-03-04 | 2026-04-19 | 13 rotating | **Same internal IP as case #6.** |
| 8 | `184.69.115.182` | `35.182.50.76` | 107 | 2026-03-04 | 2026-04-19 | 8 rotating | **AWS ca-central-1** (Canada). Cloud-hosted BACnet client. |
| 9 | `208.104.56.247` | `40.76.12.72` | 11 | 2026-03-05 | 2026-04-20 | 1 (static) | **Azure East US.** Long interval between scans — stable endpoint. |
| 10 | `72.174.109.126` | `72.174.229.106` | 8 | 2026-04-14 | 2026-04-19 | 1 (static) | Same /16 ISP block as BBMD. Local-ish. |
| 11 | `142.176.198.154` | `142.68.5.130` | 6 | 2026-03-08 | 2026-04-20 | 4 rotating | Eastlink (Canadian ISP). |
| 12 | `76.125.152.123` | `64.58.243.130` | 4 | 2026-03-17 | 2026-04-20 | 4 rotating | Comcast ↔ ATT. Cross-ISP. |
| 13 | `75.112.176.136` | `108.188.161.116` | 4 | 2026-03-29 | 2026-03-30 | 1 (static) | Transient secondary FD for case #3. |

## The single most interesting structural finding

**Case #6 and case #7 share the same external Foreign-Device IP, `216.67.73.166`.**

Two different public BBMDs (`66.58.248.125` and `24.237.132.230`) have, on overlapping dates, both had the same external public IP registered as a Foreign Device — with the same rotating-port behavior (13 distinct ports each). This is almost certainly a **single integrator-run monitoring station** bridging into two different client building networks simultaneously.

What this suggests:

- **One integrator = one disclosure = two buildings remediated.** Identifying the owner of `216.67.73.166` is higher-leverage than chasing either BBMD owner individually.
- If a third BBMD also has `216.67.73.166` in its FDT outside this seed list, that integrator may be running a fleet.
- The rotating-port behavior from a presumed-managed monitoring station is odd — a disciplined integrator would use a stable port. Rotation implies either NAT traversal or a consumer-grade ISP in front of the station.

## Also notable

- **Cloud-hosted BACnet clients exist (3 confirmed):** Homanit → DigitalOcean (×2), `208.104.56.247` → Azure East US, `184.69.115.182` → AWS ca-central-1. This is an emerging pattern: BACnet reach is being exposed to commodity public clouds where compromising one VM yields building-level ICS access.
- **`104.36.136.27 → 10.21.175.238` (930 scans, static single port)** — not in the list above because the internal IP is RFC1918, but the persistence is extreme: **930 Shodan observations in 47 days**, single-port, steady TTL. This is the single most-scanned BBMD in the seed set and a strong candidate for a Walker-pattern disclosure.
- **Of the 17 seeded BBMDs, 12 (71%) show external-FDT behavior.** If this ratio holds against the full 1000-host BACnet census, there may be **~700+ similar external-tunnel cases in the dataset** — a population worth a separate open-question / methodology page before we try to disclose at scale.

## Candidate targets ranked for per-target disclosure

Ranked by a combination of (a) wow-value, (b) feasibility of attribution, (c) public-interest impact:

1. **`216.67.73.166` (integrator)** — identify the owner of this shared endpoint; disclosure reaches ≥2 buildings.
2. **`166.144.189.152 → 108.190.193.44`** — 275 scans, 37 rotating ports. The most persistent case. Unknown owner of either IP.
3. **`184.69.115.182 → 35.182.50.76` (AWS)** — cloud-hosted BACnet. Novel pattern; probable SaaS or bad actor.
4. **`208.104.56.247 → 40.76.12.72` (Azure)** — same cloud pattern, different provider.
5. **`104.36.136.27` (internal-FDT extreme persistence)** — candidate Walker-pattern disclosure.

## Open questions for Cameron

- Which of the 5 candidate targets above should we try to attribute and file a per-target disclosure for?
- Should we rerun the longitudinal against the full 1000-host BACnet enriched list to characterize the population more precisely, or is 17/12 representative enough to act on?
- Do we want a generic "this is happening to you" template disclosure that the building operators can receive even when their integrator / cloud tenant is the primary remediation party?

## Scope and ethics

All findings derive from Shodan's passive index. No active probing, no connections to target systems, no BACnet packets sent, no interaction with any objects. The Foreign Device Table is a broadcast-routing table that Shodan captures as part of its normal BACnet banner fingerprinting. Where a Foreign Device IP is a cloud provider or second-party network, that organization is a stakeholder in the exposure and will be notified alongside the building operator.
