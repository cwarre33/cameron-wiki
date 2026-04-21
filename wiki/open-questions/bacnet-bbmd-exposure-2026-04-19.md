---
title: BACnet BBMD Internet Exposure — 2026-04-19
type: open-question
status: active
visibility: public
sources: [raw/osint/2026-04-19-scan-enriched.json, raw/osint/2026-04-20-scan-enriched.json, raw/osint/2026-04-20-longitudinal.json]
related: [wiki/open-questions/ics-exposure-2026-04-19.md, wiki/techniques/shodan-ics-osint.md, wiki/open-questions/walkermedical-disclosure-2026-04-19.md, wiki/open-questions/homanit-disclosure-2026-04-20.md, wiki/open-questions/kipp-mitchell-disclosure-2026-04-20.md, wiki/open-questions/bacnet-fdt-external-tunnels-2026-04-21.md]
created: 2026-04-19
updated: 2026-04-21
confidence: high
tags: [bacnet, bbmd, ics, osint, building-automation, unauthenticated, shodan, responsible-disclosure]
---

# BACnet BBMD Internet Exposure — 2026-04-19

Derived from [[ics-exposure-2026-04-19]] scan. 1,000 BACnet hosts sampled from 43,629 in Shodan index. All data passive — Shodan indexed responses only, no active probing or interaction with any system.

## Key finding: 84 internet-facing BBMDs

**BBMD (BACnet Broadcast Management Device)** is a protocol router that forwards BACnet broadcasts across subnets. When internet-facing, it bridges the public internet directly into an internal BACnet LAN.

**BACnet has no authentication by default.** WriteProperty is a standard unauthenticated protocol command. Through a BBMD, any BACnet client on the internet can:
- Enumerate all objects on the internal LAN
- Read sensor values, setpoints, schedules
- Write to Analog Output, Binary Output, Multi-State Output, Schedule, and Calendar objects

Writable objects control: HVAC setpoints, airflow, dampers, lighting schedules, chiller/boiler enable states, ventilation rates, alarm thresholds.

## Protocol signal quality

| Protocol | Real ICS signal | Key finding |
|----------|----------------|-------------|
| BACnet | **High** — 299/1,000 hosts with readable device names | 84 BBMDs exposing internal LANs |
| Modbus | Medium — real devices mixed with Aliyun SSH honeypots | 39 CN cloud VMs running SSH on port 502 |
| DNP3 | Low — 603/1,000 hosts responded with HTTP | Real utility SCADA largely absent from public internet |

## Vendor landscape (1,000 BACnet hosts sampled)

| Vendor | Count | Notes |
|--------|-------|-------|
| Tridium (Niagara) | 60 | Most common NA building automation platform |
| Reliable Controls | 38 | MACH-Pro series, default writable outputs |
| Carrier | 26 | i-Vu / Automated Logic subsidiary |
| Obvius (AcquiSuite) | 25 | Monitoring/metering hubs — effectively read-only |
| Automated Logic (ALC) | 24 | WebCTRL, program names visible in banners |
| Delta Controls | 23 | eBMGR/DSM series |
| KMC Controls | 13 | BAC-5051E series |

## Tridium Niagara pre-4.13 firmware exposure

**20+ hosts on pre-4.13 Niagara firmware** with documented auth bypass CVEs. Niagara web UI runs alongside BACnet — auth bypass means full programmatic control of the controller.

| CVE | Impact | Affected versions |
|-----|--------|------------------|
| CVE-2021-22656 | Improper access control on web UI — read all config without credentials | Niagara 4.x < 4.13 |
| CVE-2021-22657 | Remote code execution via Java deserialization — pre-auth | Niagara 4.x < 4.13 |
| CVE-2021-44228 | Log4Shell — Niagara embeds Log4j | Niagara 4.x < 4.13 patch |

Notable pre-4.13 hosts from sample: `Shriners_Oasis_10001` (Charlotte NC, 4.11.2.18), `PAQUIN_FORD`, `PaquetNissanStNicolas`, `Server_505` (Brazil).

## High-priority BBMD hosts

| IP | Country | Vendor | Device name | Internal reach | Notes |
|----|---------|--------|------------|----------------|-------|
| `12.5.26.10` | US | Delta Controls | `Mitchell` | 13 internal subnets (10.X.3.15 pattern) | **KIPP Inspire Academy / KIPP St. Louis network** — 6 schools, ~2,700 students. See [[kipp-mitchell-disclosure-2026-04-20]] |
| `108.252.186.105` | US | Delta Controls | `WalkerMedical` | 192.168.75.x + active FDT 192.168.53.x | **Walker Medical Building, St. Louis** — surgery center, cancer center, DaVita dialysis. See [[walkermedical-disclosure-2026-04-19]] |
| `74.92.76.61` | US | Automated Logic | `300 Building` | 5 internal segments | `PRG:electric_meter` in banner |
| `70.63.96.202` | US | Tridium | `Shriners_Oasis_10001` | `10.0.0.15` | **Oasis Shrine Temple, Charlotte NC** (fraternal lodge / event venue, NOT a hospital — see correction below). Niagara 4.11 |
| `208.105.184.74` | US | Automated Logic | `Seneca HRU` | 6 internal segments | HRU = heat recovery unit |
| `208.181.96.182` | CA | Delta Controls | `CP500_BBMD_PARKADE_FANS` | 4 devices | Casino parking garage mechanical |
| `85.206.88.54` | LT | WAGO | `Homanit.VAS_LNS_1` | 2 internal segments | Homanit = wood panel manufacturer |

## KIPP St. Louis finding (`Mitchell`, 12.5.26.10)

KIPP St. Louis (charter school network — 6 schools, ~2,700 students) on AT&T Business (AS7018). Delta Controls DSC-1616E site controller. 13 internal BACnet subnets following `10.X.3.15:47808`. The 6 KIPP campuses likely correlate to multiple BACnet controllers each — every campus's temperature control, ventilation, and scheduling routes through this single internet-facing BBMD. Single point of failure for the entire network's environmental control. On the same AT&T block: `WalkerMedical` and `PowerHouse_1` (Tridium) — three internet-exposed ICS devices on adjacent IPs in a shared business district. Full disclosure analysis: [[kipp-mitchell-disclosure-2026-04-20]].

> **Correction note (2026-04-20):** The original entry stated "KIPP Inspired Academy" and "13-campus school HVAC." KIPP St. Louis is "KIPP **Inspire** Academy" (the flagship campus name) and the network has **6 schools**, not 13. The 13 subnets visible via BACnet correspond to BACnet network segments, not necessarily 1:1 with campuses (multiple controllers per campus is common in BAS deployments). Source: [kippstl.org](https://www.kippstl.org/).

## Oasis Shrine Temple, Charlotte NC (`Shriners_Oasis_10001`, 70.63.96.202)

> **Correction note (2026-04-20):** The original entry identified this device as "Shriners Children's Hospital Charlotte." This identification was **incorrect**. "Oasis" is the name of the **Oasis Shriners** fraternal organization in Charlotte NC (temple at 604 Doug Mayes Pl, Charlotte NC 28262 — [oasisshriners.org](https://oasisshriners.org/)). Shriners Children's operates **no hospital in Charlotte**; the nearest is Shriners Children's Greenville, SC ([locations](https://www.shrinerschildrens.org/en/locations)). The patient-safety framing originally attached to this finding does not apply.

Tridium Niagara 4.11.2.18 confirmed from BACnet banner — exposure is real and CVEs still apply (CVE-2021-22656, CVE-2021-22657, CVE-2021-44228 ⚠️ vendor confirmation recommended). Sitting on Charter residential broadband (AS11426). BBMD bridges to single internal controller at `10.0.0.15`. The Oasis Shrine Temple is a fraternal lodge / event venue (~80,000 sq ft) — building automation exposure is real but the stakes are crowd-safety / event continuity, not ICU isolation. Worth disclosing on technical merit; not promoted to a separate disclosure page given the lower severity profile.

## Automated Logic program names (control loop evidence)

ALC banners expose the loaded program name — direct evidence of what the controller manages:

| Banner program | Meaning |
|----------------|---------|
| `PRG:electric_meter` | Electricity metering |
| `PRG:seneca_hru_control` | Heat recovery unit control loop |
| `PRG:aaon_vcmx_bacnet_n60_oa_dpm_reset` | Rooftop HVAC unit (AAON VCMX) |
| `PRG:worc_perf_rtu-1` | Remote terminal unit |
| `PRG:c_4813_aaon_...` | Chiller/air handler |

## `Trinity_1` misconfiguration note (66.61.221.204, Raleigh NC)

Vendor: Tridium, but Application Software: `Cylon Controls 2.3.0`. BBMD table points back at its own public IP — self-referential misconfiguration indicating the device was set up without understanding BBMD routing. Cylon Controls 2.3.0 is a very old firmware version. On Charter residential broadband.

## Country distribution (BACnet, 1,000 hosts)

US dominates at 741/1,000 — consistent with BACnet being a North American standard (ASHRAE 135). Canada 62, Japan 25, GB 21.

## 2026-04-21 update — longitudinal history answers the first open question

A follow-up longitudinal Shodan pull (`raw/osint/2026-04-20-longitudinal.json`) seeded 17 of the 84 BBMDs that had any FDT entry at scan time and pulled the per-host history for each.

- **16 of 17 seeded BBMDs (94%)** had at least one *persistent* Foreign Device entry (scan_count ≥ 3 across the 2026-03-04 → 2026-04-20 window).
- **12 of 17 (71%)** have a Foreign Device entry whose IP is **publicly routable**, not RFC1918 — the external-FDT pattern first flagged at [[homanit-disclosure-2026-04-20]].
- Two different public BBMDs (`66.58.248.125` and `24.237.132.230`) share the same external FD IP `216.67.73.166` — almost certainly a single integrator-run monitoring station bridging two client buildings.
- Cloud-hosted BACnet clients now include DigitalOcean (Homanit, 2 IPs), AWS ca-central-1 (`35.182.50.76`), and Azure East US (`40.76.12.72`).

Full catalogue at [[bacnet-fdt-external-tunnels-2026-04-21]].

The implication for this survey: the original "84 BBMDs internet-exposed" count almost certainly understates the problem. BBMDs are not just exposed — they are **actively bridging to external public endpoints on cloud infrastructure** in a majority of the sampled cases. This is the direction that warrants the next scan cycle and the next round of per-target disclosures.

## Open questions

- ~~How many of the 84 BBMDs have active Foreign Device Table entries at any given time?~~ Answered 2026-04-21: ≥94% of seeded BBMDs have persistent FDT entries.
- Is the 12/17 external-FDT ratio representative if run against the full 1,000-host BACnet enriched census? Possible ~700+ external-tunnel cases if ratio holds.
- Are Tridium pre-4.13 hosts also internet-facing on port 443/8443 (Niagara web UI)?
- What is the responsible disclosure contact chain for building automation vendors vs. property managers vs. **integrators operating shared monitoring stations** (new category surfaced 2026-04-21)?
- How does exposure change week-over-week? Requires longitudinal tracking. ⚠️

## Ethical scope

All findings from Shodan passive index. No active probing, no connections to target systems, no BACnet packets sent, no interaction with any objects. Data used for security research and responsible disclosure only.
