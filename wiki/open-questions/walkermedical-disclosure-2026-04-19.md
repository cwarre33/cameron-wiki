---
title: Responsible Disclosure — Walker Medical Building BACnet BBMD
type: open-question
status: active
visibility: public
sources: [raw/osint/2026-04-19-scan-enriched.json]
related: [wiki/open-questions/bacnet-bbmd-exposure-2026-04-19.md, wiki/techniques/shodan-ics-osint.md]
created: 2026-04-19
updated: 2026-04-20
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
| 2026-04-20 | Follow-up investigation plan added (see below) |
| Pending | Contact Cozad Commercial Real Estate Group |
| Pending | Contact Delta Controls security team |
| T+30 days | CISA ICS-CERT notification if no response |

---

## Follow-up investigation plan (2026-04-20)

Open questions worth pursuing before — and during — the disclosure exchange. Each is a discrete research thread that strengthens the disclosure or seeds new findings.

### 1. Identify `192.168.53.36` (the persistent tunneler)

The internal device that has been re-registering through the BBMD every ~60 seconds for 30+ days is the most interesting actor in this story. Hypotheses:

| Hypothesis | Evidence-for | How to test (passively) |
|-----------|--------------|--------------------------|
| Remote-access workstation owned by the BMS integrator | Most common reason for a persistent FDT registration | Look for a parallel Niagara/WebCTRL/Delta enteliWEB exposure on the same /24 |
| Cloud-hosted analytics/optimization service phoning home | "Smart building" SaaS often uses BACnet over BBMD | Banner-search for `Coppertree`, `Switch Automation`, `BuildingOS`, `Kaiterra`, etc. |
| A second on-prem controller (auxiliary BBMD) | Multi-tenant medical buildings sometimes have per-tenant BAS | Check whether `108.252.186.105` neighbors expose BACnet |
| Misconfigured user device (laptop with BACnet client open) | Possible but unlikely — TTL=60 with rotating ports suggests software, not human | Source-port jitter analysis — software clients have characteristic patterns |

**Action:** Banner-search Shodan for known building-analytics SaaS products active in St. Louis healthcare.

### 2. The AT&T-block adjacency claim — verify or retract

The BACnet survey page says: *"On the same AT&T block: WalkerMedical and PowerHouse_1 (Tridium) — three internet-exposed ICS devices on adjacent IPs in a shared business district."*

This needs scrutiny:
- WalkerMedical: `108.252.186.105` (lightspeed.stlsmo.sbcglobal.net — St. Louis Lightspeed/U-verse range)
- KIPP `Mitchell`: `12.5.26.10` (legacy AT&T 12.0.0.0/8 allocation — different address space entirely)
- `PowerHouse_1`: IP not specified in current notes

⚠️ "Same AT&T block" is misleading if it just means `AS7018` (which covers tens of millions of IPs). True /24 adjacency is a much stronger claim. **Action:** pull `PowerHouse_1`'s IP from raw data and verify the actual /24 / /22 relationships. If "adjacent" is wrong, soften the claim in the survey page.

### 3. Delta Controls firmware build cross-reference

WalkerMedical reports `V3.40, build 189697`. Confirmed-vulnerable to CVE-2019-9569 is `V3.40 build 571848 and prior`. Build numbers don't form a simple ordering across product variants (DSM_RTR vs enteliBUS Manager use different build streams).

**Action:**
- Pull all Delta Controls release notes for V3.40 family (deltacontrols.com support portal — may require integrator access)
- Cross-reference build 189697 against the documented patch series
- Frame disclosure as: "we have not confirmed your firmware is vulnerable; we are asking you to confirm it is patched"

### 4. Shodan history pivot (longitudinal evidence is the strongest part of this disclosure)

The 4-scan history (2026-03-20 / 03-24 / 04-01 / 04-19) is what makes WalkerMedical unique among the 84 BBMDs surveyed. Worth doing the same longitudinal analysis on:

- The other 83 BBMDs in the survey — how many also show persistent FDT entries across multiple Shodan scans?
- The 20+ Niagara pre-4.13 hosts — has any host been observed dropping in/out of the index (indicating intermittent fixes)?
- Any host that appears in three or more scans is a candidate for "this is a stable misconfiguration, not transient" framing.

**Action:** Add `--longitudinal` mode to `scripts/osint/collect.py` that pulls Shodan host history (`api.host(ip, history=True)`) for each high-priority IP rather than relying on the live snapshot.

### 5. Wayback Machine pivot for Walker Medical Building tenants

Cozad Commercial Real Estate Group manages the building. Wayback may have:
- Historical tenant lists (DaVita, Mercy, SSM Health, etc. all have long-running address records)
- Construction/renovation news that mentions the BMS integrator by name (the integrator is the likely root cause and a more useful disclosure recipient than the property manager)
- Old leasing materials that name the building engineer / facilities contact

**Action:** Pull Wayback snapshots of cozadgroup.com and walkermedicalbuilding.com for the last 5 years.

### 6. BMS integrator identification

Across all three disclosure cases (WalkerMedical, KIPP, Homanit), the practical fix lives with the BMS integrator, not the building owner. The integrator is also the entity most likely to have a single architecture replicated across many sites.

**Action:** For each Delta Controls install in the survey, look for integrator names embedded in BACnet program identifiers (pattern observed in Automated Logic banners — e.g., `PRG:c_4813_aaon_...` may encode integrator job numbers). If a single integrator name recurs, **the integrator is the highest-leverage disclosure target in the entire dataset.**

---

## Cross-reference

Related disclosures filed in the same scan:
- [[kipp-mitchell-disclosure-2026-04-20]] — KIPP St. Louis, BBMD blast-radius case
- [[homanit-disclosure-2026-04-20]] — Homanit Lietuva MDF plant, combustible-dust regime
- [[bacnet-bbmd-exposure-2026-04-19]] — survey page (84 BBMDs, vendor breakdown)
