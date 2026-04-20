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

An internet-facing BACnet Broadcast Management Device (BBMD) was identified at the Walker Medical Building, 12855 North Forty Drive, Town and Country, MO 63141 via passive Shodan OSINT. The device bridges the public internet to internal building automation networks with no authentication.

**Critical finding:** Historical Shodan data confirms a persistent, active BACnet tunnel from an internal device (`192.168.53.36`) through this public gateway — observed continuously across four independent scans spanning 30 days. This is not accidental misconfiguration. Something on the internal network has been actively maintaining an internet-facing BACnet connection since at least March 20, 2026.

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
| Last Shodan observation | 2026-04-20T00:14:51 UTC |

### BBMD configuration

```
BACnet Broadcast Management Device (BBMD):
    192.168.75.100:47808        ← primary internal subnet

Foreign Device Table (FDT):
    192.168.53.36:65121:ttl=60:timeout=25   ← persistent tunnel, second internal subnet
```

**What this means:**
- The device is an internet-accessible BACnet router with no authentication
- Internal subnet `192.168.75.x` is permanently reachable through this gateway
- A device at `192.168.53.36` on a second internal subnet is actively maintaining a registration tunnel
- Any BACnet client on the internet can enumerate, read, and write to objects on both subnets

### Persistent FDT tunnel — 30-day evidence

Shodan independently observed the same internal device (`192.168.53.36`) registered in the Foreign Device Table across all four scans in its history. The source port rotates (ephemeral UDP), confirming the device is continuously re-registering — not a stale entry:

| Shodan scan date | FDT source port | TTL | Timeout |
|-----------------|----------------|-----|---------|
| 2026-03-20 | 60066 | 60s | 36s remaining |
| 2026-03-24 | 54472 | 60s | 46s remaining |
| 2026-04-01 | 55494 | 60s | 26s remaining |
| 2026-04-19 | 65121 | 60s | 25s remaining |

**TTL=60 with rotating ports means `192.168.53.36` re-announces itself every ~60 seconds.** This is a deliberate persistent tunnel that has been running for at minimum 30 days, not an idle misconfiguration. The internal device at `.53.36` is actively seeking to maintain reachability from the internet.

### Protocol confirmation — device is live and responsive

The raw BACnet packet Shodan captured (`810a0017010030010c0c023fffff194b3ec4020075303f`) is a complete `ReadProperty-ACK` response — the device received Shodan's query and responded correctly with a fully valid BACnet protocol exchange:

```
BVLC: type=0x81 (BACnet/IP), function=0x0a (Original-Unicast-NPDU)
NPDU: version=1, control=0x00 (no special routing)
APDU: ComplexACK, invoke-id=1, service=ReadProperty (0x0c)
  Object-Identifier: Device #30000
  Property: object-list (75)
  Value: Device #30000 (self-confirmed identity)
```

The device is fully functional, protocol-compliant, and answering BACnet queries from the internet with no authentication challenge.

### CVE exposure (version-family match)

**CVE-2019-9569** — Delta Controls enteliBUS V3.40 buffer overflow
- CVSS v3: **9.8 CRITICAL** (`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`)
- CWE-787: Out-of-bounds write
- Impact: Remote unauthenticated arbitrary code execution via crafted BACnet packet
- Affected: enteliBUS Manager V3.40_B-571848 and prior
- CISA advisory: ICSA-19-239-01

**Assessment:** WalkerMedical reports `Application Software: V3.40` — same major version family as the CVE. Firmware build 189697 differs from confirmed-vulnerable build 571848. The DSM_RTR and enteliBUS Manager share the V3.40 codebase. Whether build 189697 received the buffer overflow patch cannot be confirmed passively — requires vendor verification. ⚠️ Treat as potentially vulnerable pending Delta Controls confirmation.

### Risk in context

Walker Medical Building is not a general office complex. It is an active medical facility containing:
- **Surgery center** — two operating rooms
- **Cancer center** — MRI, CT scanner, linear accelerator (radiation therapy)
- **DaVita dialysis** — life-critical renal treatment (NYSE: DVA)
- **Mercy Health** — rated Moody's Aa3
- Urology of St. Louis, Neurosurgery of St. Louis, SSM Health Physical Therapy

BACnet in a medical facility controls safety-critical infrastructure:
- **Operating room pressure differentials** — positive pressure prevents pathogen ingress; incorrect setpoints create infection risk
- **MRI suite HVAC** — temperature excursions can damage superconducting magnets
- **Cancer center air handling** — filtration and pressure control for immunocompromised patients
- **Dialysis environment** — temperature and air quality for treatment areas

The persistent FDT tunnel means the internal BACnet network has been continuously reachable from the internet for at least 30 days. The BBMD at `192.168.75.100` and the tunneling device at `192.168.53.36` are downstream controllers — their Analog Output, Binary Output, and Schedule objects are the actual writable endpoints for the systems above.

---

## Disclosure contacts

### Primary — Property management

**Cozad Commercial Real Estate Group** (confirmed property manager)
- Phone: 314.781.3000
- Email: info@cozadgroup.com
- Address: 16 Sunnen Drive, Suite 164, Saint Louis, MO 63143

### Secondary — Building address

Walker Medical Building — 12855 North Forty Drive, Town and Country, MO 63141

### Vendor coordination

**Delta Controls**
- Security bulletins: deltacontrols.com
- Reference: Security Bulletin SecB0001 / CVE-2019-9569 / CISA ICSA-19-239-01

### Coordinated disclosure escalation

**CISA ICS-CERT** — report@cisa.gov / cisa.gov/report
Escalate if no property manager response within 30 days.

---

## Recommended disclosure message

> **Subject:** Security Disclosure — Exposed BACnet Building Control System, Walker Medical Building
>
> I am a security researcher conducting passive OSINT analysis of internet-exposed industrial control systems. Using only data already indexed by Shodan (no active scanning, no probing, no interaction with any systems), I identified a serious exposure at your facility.
>
> **What was found:**
> A Delta Controls DSM_RTR BACnet controller (device name "WalkerMedical") at IP `108.252.186.105` is configured as an internet-facing BACnet Broadcast Management Device with no authentication. It bridges the public internet to your internal building automation networks on subnets `192.168.75.x` and `192.168.53.x`.
>
> More critically: historical Shodan data shows an internal device at `192.168.53.36` has been actively maintaining a live tunnel through this public gateway every 60 seconds, continuously, across four independent observations spanning March 20 to April 19, 2026 — at minimum 30 days. This is an ongoing condition, not a one-time snapshot.
>
> BACnet has no built-in authentication. Any BACnet client on the internet can enumerate, read, and potentially write to building automation objects reachable through this gateway. Given that Walker Medical Building contains a surgery center, cancer center with a linear accelerator, and active DaVita dialysis — building HVAC and environmental controls are directly patient safety-relevant.
>
> The device firmware (Delta Controls V3.40) also falls within the version family affected by CVE-2019-9569 (CVSS 9.8 Critical — remote unauthenticated code execution via BACnet packet). This requires confirmation with Delta Controls.
>
> **Recommended immediate actions:**
> 1. Block UDP port 47808 inbound at your perimeter firewall right now
> 2. Investigate what `192.168.53.36` is and why it is maintaining an internet-facing BACnet tunnel
> 3. Contact Delta Controls to verify your firmware's patch status against CVE-2019-9569
> 4. Engage your BMS integrator to audit BBMD configuration
> 5. Replace any legitimate remote BACnet access with VPN + private BBMD
>
> I have no intention of accessing, testing, or interacting with your systems. I am disclosing this in good faith. I am available to provide full technical details to your facilities team, IT security team, or BMS integrator.

---

## Remediation checklist

- [ ] Block UDP 47808 inbound at perimeter firewall immediately
- [ ] Identify `192.168.53.36` — determine what it is and why it is tunneling through a public BBMD
- [ ] Audit the Foreign Device Table for unauthorized registrations
- [ ] Contact Delta Controls: verify build 189697 vs CVE-2019-9569 patch status
- [ ] Review BBMD access logs for evidence of unauthorized enumeration or write attempts
- [ ] Segment BACnet network from routable IT subnets
- [ ] Replace internet-facing BBMD with VPN-gated private BBMD for any legitimate remote access

---

## Timeline

| Date | Event |
|------|-------|
| 2026-03-20 | Earliest Shodan observation of active FDT tunnel (192.168.53.36:60066) |
| 2026-03-24 | Second Shodan observation confirms persistence (192.168.53.36:54472) |
| 2026-04-01 | Third observation (192.168.53.36:55494) |
| 2026-04-19 | Passive OSINT scan performed — fourth FDT observation (192.168.53.36:65121) |
| 2026-04-19 | Raw BACnet packet decoded — device confirmed live and protocol-responsive |
| 2026-04-19 | Disclosure report finalized |
| Pending | Contact Cozad Commercial Real Estate Group |
| Pending | Contact Delta Controls security team |
| T+30 days | CISA ICS-CERT notification if no response |
