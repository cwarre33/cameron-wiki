---
title: Responsible Disclosure — Walker Medical Building BACnet BBMD
type: open-question
status: active
visibility: public
sources: [raw/osint/2026-04-19-scan-enriched.json]
related: [wiki/open-questions/bacnet-bbmd-exposure-2026-04-19.md, wiki/techniques/shodan-ics-osint.md]
created: 2026-04-19
updated: 2026-04-19
confidence: high
tags: [bacnet, bbmd, ics, responsible-disclosure, walkermedical, delta-controls, cve-2019-9569]
---

# Responsible Disclosure — Walker Medical Building BACnet BBMD

## Summary

An internet-facing BACnet Broadcast Management Device (BBMD) was identified at the Walker Medical Building, 12855 North Forty Drive, Town and Country, MO 63141 via passive Shodan OSINT. The device bridges the public internet to internal building automation networks with no authentication. An active Foreign Device Table entry was present at scan time, indicating a remote BACnet client was actively tunneled in through the exposed gateway.

**All data is from Shodan's passive index. No systems were probed, accessed, or interacted with.**

---

## Technical findings

### Device identification

| Field | Value |
|-------|-------|
| Public IP | `108.252.186.105` |
| Reverse DNS | `108-252-186-105.lightspeed.stlsmo.sbcglobal.net` |
| ISP | AT&T Enterprises LLC (AS7018) |
| BACnet port | UDP 47808 |
| Device name | `WalkerMedical` |
| Vendor | Delta Controls |
| Model | DSM_RTR (Delta Site Manager Router) |
| Firmware | V3.40, build 189697 |
| BACnet Instance ID | 30000 |

### BBMD configuration (from Shodan banner)

```
BACnet Broadcast Management Device (BBMD):
    192.168.75.100:47808

Foreign Device Table (FDT):
    192.168.53.36:65121:ttl=60:timeout=25
```

**What this means:**
- The device is acting as an internet-accessible BACnet router
- Internal subnet `192.168.75.x` is reachable through this gateway from the internet
- At scan time, a device at `192.168.53.36` (a second internal subnet) had an **active live registration** — TTL=60 means it was registered within the last 60 seconds. This device or a remote BACnet client was actively using this gateway as a tunnel
- Any BACnet client on the internet can enumerate, read, and write to objects on both internal subnets

### CVE exposure (version-family match)

**CVE-2019-9569** — Delta Controls enteliBUS V3.40 buffer overflow
- CVSS v3: **9.8 CRITICAL** (`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`)
- CWE-787: Out-of-bounds write
- Impact: Remote unauthenticated arbitrary code execution
- Affected: enteliBUS Manager V3.40_B-571848 and prior
- CISA advisory: ICSA-19-239-01

**Assessment:** The WalkerMedical device reports `Application Software: V3.40` — the same major version family as the CVE. The firmware build number (189697) differs from the confirmed vulnerable build (571848). **The DSM_RTR and enteliBUS Manager share the same V3.40 codebase family** per Delta Controls' product line. Whether build 189697 received the specific buffer overflow patch cannot be determined from passive data alone — this requires vendor confirmation or physical access to the device. ⚠️ Treat as potentially vulnerable pending verification.

### Risk in context

The Walker Medical Building is not an office complex — it is an active medical facility containing:
- **Surgery center** with two operating rooms
- **Cancer center** with MRI, CT scanner, and linear accelerator (radiation therapy)
- **DaVita dialysis** (NYSE: DVA) — life-critical treatment
- **Mercy Health** tenant (rated Moody's Aa3)
- Urology of St. Louis, Neurosurgery of St. Louis, SSM Health Physical Therapy

BACnet controls building systems including HVAC, air handling, and environmental monitoring. In medical facilities, HVAC is not a comfort system — it maintains:
- Negative/positive pressure differentials in operating rooms and isolation areas
- Temperature control for MRI cooling systems
- Air quality and filtration in cancer treatment areas

An unauthenticated BACnet write to output objects on the internal network could affect these systems. The active FDT entry at scan time indicates this pathway was in use, not merely exposed.

---

## Disclosure contacts

### Primary — Property management

**Cozad Commercial Real Estate Group** (confirmed property manager)
- Phone: 314.781.3000
- Email: info@cozadgroup.com
- Address: 16 Sunnen Drive, Suite 164, Saint Louis, MO 63143
- Web: cozadgroup.com

### Secondary — Building

- **Walker Medical Building** — 12855 North Forty Drive, Town and Country, MO 63141

### Vendor coordination

**Delta Controls** (device manufacturer)
- Security contact: Delta Controls publishes security bulletins at deltacontrols.com
- Reference: Security Bulletin SecB0001 (CVE-2019-9569, enteliBUS V3.40)
- CISA ICS advisory: ICSA-19-239-01

### Coordinated disclosure (if needed)

**CISA ICS-CERT**
- Report form: cisa.gov/report
- Email: report@cisa.gov

---

## Recommended disclosure message

> **Subject:** Security Disclosure — Exposed BACnet Building Control System, Walker Medical Building
>
> I'm a security researcher conducting passive OSINT analysis of internet-exposed industrial control systems. Using only publicly available data indexed by Shodan (no active scanning or probing of any systems), I identified an internet-facing building automation controller at your facility.
>
> **What was found:** A Delta Controls DSM_RTR BACnet controller (device name "WalkerMedical") at IP 108.252.186.105 is configured as a BACnet Broadcast Management Device (BBMD) with no authentication. This device bridges the public internet to internal building automation networks (192.168.75.x and 192.168.53.x subnets). At the time of observation, an active remote connection was registered through the gateway.
>
> **Why this matters:** BACnet has no built-in authentication. Anyone on the internet who knows the protocol can enumerate and potentially control building systems through this gateway. Given that Walker Medical Building contains a surgery center, cancer center, and dialysis facility, building HVAC and environmental controls are patient safety-relevant.
>
> **Recommended remediation:**
> 1. Firewall UDP port 47808 — block all inbound BACnet from the internet immediately
> 2. Require VPN for any legitimate remote BACnet access
> 3. Contact Delta Controls regarding firmware V3.40 and CVE-2019-9569 (CVSS 9.8)
> 4. Engage your BMS integrator to audit BBMD configuration and disable internet-facing routing
>
> I am happy to provide technical details to your facilities or IT team. I have no intention of accessing, testing, or interacting with your systems in any way. This disclosure is made in good faith under responsible disclosure principles.

---

## Remediation checklist (for recipient)

- [ ] Block UDP 47808 inbound at perimeter firewall immediately
- [ ] Confirm with BMS integrator whether internet-facing BBMD was intentional
- [ ] Rotate or remove Foreign Device Table registrations
- [ ] Contact Delta Controls: verify firmware build 189697 vs CVE-2019-9569 patch status
- [ ] Assess whether any unauthorized BACnet access occurred (review BBMD logs if available)
- [ ] Segment BACnet network — BMS should not share the same routable subnet as IT systems
- [ ] For remote access: replace open BBMD with VPN + local BBMD on private LAN

---

## Timeline

| Date | Event |
|------|-------|
| 2026-04-19 | Shodan scan performed (passive index, no active probing) |
| 2026-04-19 | WalkerMedical BBMD with active FDT identified in analysis |
| 2026-04-19 | Disclosure report drafted |
| Pending | Contact Cozad Commercial Real Estate |
| Pending | Contact Delta Controls security |
| Pending | CISA notification if no response within 30 days |
