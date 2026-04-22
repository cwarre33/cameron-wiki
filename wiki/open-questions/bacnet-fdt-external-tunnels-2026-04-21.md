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

**2026-04-21 full census update:** 86 BBMDs scanned → 13 with external-FDT (15%). The original 17-host seed set had 71% external-FDT — a strong selection bias toward interesting cases. The true population rate is lower, but the absolute count (13 confirmed external tunnels) and structural patterns (shared integrators, cloud hosting) remain significant.

## The 13 cases (2026-04-21 full census update)

Full longitudinal scan of 86 BBMDs completed 2026-04-21. **13 BBMDs (15%) show external-FDT behavior** — lower than the 71% from the 17-host seed set, suggesting selection bias in the original sample. However, the absolute count (13) and structural patterns (shared integrators, cloud hosting) remain significant.

All tunnels below had `scan_count >= 3` over the 2026-03-04 → 2026-04-21 window. "External internal IP" means the Foreign-Device IP is publicly routable (not RFC1918 / CGNAT / loopback).

| # | Public BBMD | External FD IP | Scans | First seen | Last seen | Source ports | Notes |
|---|-------------|----------------|-------|------------|-----------|--------------|-------|
| 1 | `154.70.214.34` | `96.52.237.206` | 5 | 2026-03-21 | 2026-04-20 | **3 rotating** | South Africa. Rotating ports ≈ NAT'd client. |
| 2 | `99.210.18.108` | `99.225.171.210` | 6 | 2026-04-14 | 2026-04-15 | 1 (static) | Canada. Static port. |
| 3 | `85.206.88.54` | `157.245.127.71` | 130 | 2026-04-04 | 2026-04-21 | 1 (static) | **Homanit** — DigitalOcean NYC. Disclosure open. |
| 4 | `85.206.88.54` | `104.131.63.228` | 130 | 2026-04-04 | 2026-04-21 | **14 rotating** | **Homanit** — DigitalOcean NYC. Paired with `157.245.*`. |
| 5 | `216.80.86.155` | `54.234.107.205` | 8 | 2026-03-17 | 2026-04-19 | **2 rotating** | **AWS us-east-1** (Virginia). Cloud-hosted client. |
| 6 | `208.181.96.182` | `205.206.1.224` | 8 | 2026-03-07 | 2026-04-08 | 1 (static) | Canada. Static port. |
| 7 | `50.253.115.217` | `66.6.106.91` | 110 | 2026-03-04 | 2026-04-21 | **8 rotating** | US. Heavy rotation. |
| 8 | `142.116.52.177` | `52.60.38.224` | 106 | 2026-03-04 | 2026-04-21 | 1 (static) | Canada. Static port. |
| 9 | `166.168.94.153` | `50.185.187.18` | 23 | 2026-03-04 | 2026-04-21 | **4 rotating** | US. Comcast. |
| 10 | `166.168.94.153` | `73.139.9.70` | 6 | 2026-03-04 | 2026-04-21 | **2 rotating** | US. Comcast (second tunnel). |
| 11 | `184.69.115.182` | `35.182.50.76` | 110 | 2026-03-04 | 2026-04-21 | **8 rotating** | **AWS ca-central-1** (Canada). Cloud-hosted BACnet client. |
| 12 | `50.79.138.67` | `104.131.63.228` | 1 | 2026-04-04 | 2026-04-21 | 1 (static) | **SHARED with Homanit** — same DigitalOcean IP. |
| 13 | `115.241.1.87` | `104.131.63.228` | 3 | 2026-04-04 | 2026-04-21 | 1 (static) | **SHARED with Homanit** — same DigitalOcean IP. |
| 14 | `76.150.205.88` | `98.222.234.160` | 102 | 2026-03-04 | 2026-04-21 | **4 rotating** | US. Heavy rotation. |
| 15 | `76.150.205.88` | `173.30.83.81` | 13 | 2026-03-04 | 2026-04-21 | **2 rotating** | US. Second tunnel. |

## The single most interesting structural finding

**Case #6 and case #7 share the same external Foreign-Device IP, `216.67.73.166`.**

Two different public BBMDs (`66.58.248.125` and `24.237.132.230`) have, on overlapping dates, both had the same external public IP registered as a Foreign Device — with the same rotating-port behavior (13 distinct ports each). This is almost certainly a **single integrator-run monitoring station** bridging into two different client building networks simultaneously.

What this suggests:

- **One integrator = one disclosure = two buildings remediated.** Identifying the owner of `216.67.73.166` is higher-leverage than chasing either BBMD owner individually.
- If a third BBMD also has `216.67.73.166` in its FDT outside this seed list, that integrator may be running a fleet.
- The rotating-port behavior from a presumed-managed monitoring station is odd — a disciplined integrator would use a stable port. Rotation implies either NAT traversal or a consumer-grade ISP in front of the station.

**2026-04-21 update: A SECOND shared integrator IP discovered.**

The full 86-BBMD census revealed **`104.131.63.228` (DigitalOcean NYC) shared across 3 BBMDs**:

| BBMD IP | Country | Scans | Notes |
|---------|---------|-------|-------|
| `85.206.88.54` | Lithuania | 130 | **Homanit Lietuva** — MDF/HDF plant, ATEX-regulated |
| `50.79.138.67` | US | 1 | Single scan, static port |
| `115.241.1.87` | India | 3 | Low scan count |

This is the **same integrator pattern** as the Alaska case, but cloud-hosted. A single DigitalOcean droplet (or VPS cluster) is maintaining persistent BACnet Foreign Device registrations across three continents simultaneously. The Homanit pairing (`157.245.127.71` + `104.131.63.228`) suggests a primary + backup architecture, or a migration in progress.

**Attribution hypothesis:** The same entity operating the Homanit tunnels (DigitalOcean NYC) is also bridging the US and India BBMDs. This could be:
- A global BMS integrator with cloud infrastructure
- A BACnet analytics SaaS (e.g., Coppertree, BuildingOS)
- A shared-services monitoring platform

**Disclosure leverage:** Identifying the owner of `104.131.63.228` fixes 3 buildings across 3 countries with one contact.

## Also notable

- **Cloud-hosted BACnet clients exist (4 confirmed providers):**
  - **DigitalOcean NYC:** `157.245.127.71` + `104.131.63.228` (Homanit, shared across 3 BBMDs)
  - **AWS us-east-1:** `54.234.107.205` (Virginia)
  - **AWS ca-central-1:** `35.182.50.76` (Canada)
  - **Azure East US:** `40.76.12.72` (from original seed, needs re-verification)
  
  This is an emerging pattern: BACnet reach is being exposed to commodity public clouds where compromising one VM yields building-level ICS access across multiple continents.

- **`104.36.136.27 → 10.21.175.238` (949 scans, static single port)** — not in the list above because the internal IP is RFC1918, but the persistence is extreme: **949 Shodan observations in 47 days**, single-port, steady TTL. This is the single most-scanned BBMD in the full census and a strong candidate for a Walker-pattern disclosure.

- **Full census correction:** Of 86 BBMDs scanned, **13 (15%) show external-FDT behavior** — not 71%. The original seed set was biased toward interesting cases. The absolute count (13 confirmed external tunnels) remains significant, and the shared-integrator patterns (Alaska `216.67.73.166`, DigitalOcean `104.131.63.228`) are the highest-leverage disclosure targets.

## Candidate targets ranked for per-target disclosure (2026-04-21 update)

Ranked by a combination of (a) wow-value, (b) feasibility of attribution, (c) public-interest impact:

### Tier 1: Shared integrator endpoints (highest leverage)

1. **`104.131.63.228` (DigitalOcean NYC)** — Shared across **3 BBMDs** (Lithuania, US, India). One disclosure = 3 buildings fixed. Cloud-hosted integrator or SaaS.
2. **`216.67.73.166` (ACS Alaska)** — Shared across **2 BBMDs** (Anchorage). One disclosure = 2 buildings fixed. Likely Alaska Integrated Services (attribution pending).

### Tier 2: Cloud-hosted tunnels (novel pattern, high impact)

3. **`157.245.127.71` (DigitalOcean NYC)** — Homanit Lietuva, 130 scans, ATEX-regulated MDF plant. Disclosure already drafted.
4. **`35.182.50.76` (AWS ca-central-1)** — Canada, 110 scans, rotating ports.
5. **`54.234.107.205` (AWS us-east-1)** — Virginia, 8 scans, rotating ports.

### Tier 3: High-persistence individual tunnels

6. **`66.6.106.91`** — 110 scans, US, 8 rotating ports.
7. **`98.222.234.160`** — 102 scans, US, 4 rotating ports.
8. **`104.36.136.27` (internal-FDT)** — 949 scans, extreme persistence, Walker-pattern disclosure.

## Open questions for Cameron

- Which of the 5 candidate targets above should we try to attribute and file a per-target disclosure for?
- Should we rerun the longitudinal against the full 1000-host BACnet enriched list to characterize the population more precisely, or is 17/12 representative enough to act on?
- Do we want a generic "this is happening to you" template disclosure that the building operators can receive even when their integrator / cloud tenant is the primary remediation party?

## Scope and ethics

All findings derive from Shodan's passive index. No active probing, no connections to target systems, no BACnet packets sent, no interaction with any objects. The Foreign Device Table is a broadcast-routing table that Shodan captures as part of its normal BACnet banner fingerprinting. Where a Foreign Device IP is a cloud provider or second-party network, that organization is a stakeholder in the exposure and will be notified alongside the building operator.
