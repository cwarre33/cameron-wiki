---
title: BACnet BBMD Internet Exposure — 2026-04-19
type: open-question
status: active
visibility: public
sources: [raw/osint/2026-04-19-scan-enriched.json]
related: [wiki/open-questions/ics-exposure-2026-04-19.md, wiki/techniques/shodan-ics-osint.md, wiki/open-questions/walkermedical-disclosure-2026-04-19.md]
created: 2026-04-19
updated: 2026-04-19
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
| `12.5.26.10` | US | Delta Controls | `Mitchell` | 13 internal subnets (10.X.3.15 pattern) | **KIPP Inspired Academy** — 13-campus school HVAC |
| `108.252.186.105` | US | Delta Controls | `WalkerMedical` | 192.168.75.x + active FDT 192.168.53.x | **Walker Medical Building, St. Louis** — surgery center, cancer center, DaVita dialysis. See [[walkermedical-disclosure-2026-04-19]] |
| `74.92.76.61` | US | Automated Logic | `300 Building` | 5 internal segments | `PRG:electric_meter` in banner |
| `70.63.96.202` | US | Tridium | `Shriners_Oasis_10001` | `10.0.0.15` | Shriners Children's Hospital Charlotte, Niagara 4.11 |
| `208.105.184.74` | US | Automated Logic | `Seneca HRU` | 6 internal segments | HRU = heat recovery unit |
| `208.181.96.182` | CA | Delta Controls | `CP500_BBMD_PARKADE_FANS` | 4 devices | Casino parking garage mechanical |
| `85.206.88.54` | LT | WAGO | `Homanit.VAS_LNS_1` | 2 internal segments | Homanit = wood panel manufacturer |

## KIPP Academy finding (`Mitchell`, 12.5.26.10)

KIPP Inspired Academy (charter school network), St. Louis, on AT&T Business (AS7018). Delta Controls DSC-1616E site controller. 13 internal subnets all following `10.X.3.15:47808` — one BACnet controller per school campus, all routing through this single internet-facing BBMD. Every campus's temperature control, ventilation, and scheduling reachable through one exposed device. On the same AT&T block: `WalkerMedical` and `PowerHouse_1` (Tridium) — three internet-exposed ICS devices on adjacent IPs in a shared business district.

## Shriners Children's Hospital Charlotte (`Shriners_Oasis_10001`, 70.63.96.202)

Tridium Niagara 4.11.2.18 confirmed from BACnet banner. Three CVEs apply by version: CVE-2021-22656, CVE-2021-22657, CVE-2021-44228. Sitting on Charter residential broadband (AS11426). BBMD bridges to single internal controller at `10.0.0.15`. Healthcare HVAC with air pressure differentials in isolation rooms is patient safety-critical infrastructure.

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

## Open questions

- How many of the 84 BBMDs have active Foreign Device Table entries at any given time?
- Are Tridium pre-4.13 hosts also internet-facing on port 443/8443 (Niagara web UI)?
- What is the responsible disclosure contact chain for building automation vendors vs. property managers?
- How does exposure change week-over-week? Requires longitudinal tracking. ⚠️

## Ethical scope

All findings from Shodan passive index. No active probing, no connections to target systems, no BACnet packets sent, no interaction with any objects. Data used for security research and responsible disclosure only.
