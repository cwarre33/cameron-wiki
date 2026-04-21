---
title: Responsible Disclosure — KIPP St. Louis BACnet BBMD ("Mitchell")
type: open-question
status: active
visibility: public
sources: [raw/osint/2026-04-19-scan-enriched.json, raw/osint/2026-04-20-longitudinal.json]
related: [wiki/open-questions/bacnet-bbmd-exposure-2026-04-19.md, wiki/open-questions/walkermedical-disclosure-2026-04-19.md, wiki/techniques/shodan-ics-osint.md]
created: 2026-04-20
updated: 2026-04-20
confidence: high
tags: [bacnet, bbmd, ics, responsible-disclosure, kipp, k12-schools, charter-school, delta-controls, single-point-of-failure]
---

# Responsible Disclosure — KIPP St. Louis BACnet BBMD ("Mitchell")

## Summary

An internet-facing BACnet Broadcast Management Device (BBMD) was identified at IP `12.5.26.10` (device name `Mitchell`) via passive Shodan OSINT. The device routes BACnet traffic to **13 internal subnets** following a regular `10.X.3.15:47808` pattern — strongly indicative of a multi-campus building automation deployment for **KIPP St. Louis**, a charter school network operating 6 schools serving approximately 2,700 students (Pre-K through 12).

**The wow finding:** A single internet-facing, unauthenticated device is the routing nexus for the building automation of an entire K–12 school network. Loss of integrity at this one IP cascades to **temperature, ventilation, scheduling, and life-safety control** across every KIPP St. Louis campus simultaneously. This is the textbook definition of a single point of failure in critical infrastructure terms.

**All data is from Shodan's passive index. No systems were probed, accessed, or interacted with.**

**Update 2026-04-20 (longitudinal):** Shodan history (133 observations over the past ~6 weeks) confirms **four distinct internal controllers have registered as Foreign Devices through this BBMD** across 2026-03-04 → 2026-04-20. The registration is continuous, not a one-time scan artifact. A clean device handoff from `10.20.80.181` → `10.20.80.175` occurred on 2026-04-07, consistent with a controller replacement or DHCP rebind. This confirms the BBMD has been reachable — and actively used — for at least 47 days.

---

## Technical findings

### Device identification

| Field | Value |
|-------|-------|
| Public IP | `12.5.26.10` |
| ISP | AT&T Business Services (AS7018) |
| BACnet port | UDP 47808 |
| Device name | `Mitchell` |
| Vendor | Delta Controls |
| Model | DSC-1616E site controller (per BACnet banner) |
| Internal subnets reachable | 13 (all `10.X.3.15:47808` pattern) |
| Inferred operator | KIPP St. Louis (charter school network) |
| Attribution confidence | Medium-high — pending owner confirmation |

### Why we attribute this to KIPP St. Louis

The attribution is inferential, not banner-confirmed:

1. **Geo-ISP fit.** AT&T Business Services range; St. Louis is KIPP's metro.
2. **Subnet structure.** 13 BACnet subnets sharing a uniform `10.X.3.15` pattern is consistent with a centrally-administered multi-site organization, not a single building.
3. **Subnet count.** KIPP St. Louis operates 6 campuses; 13 subnets is consistent with multiple HVAC zones / controllers per campus (typical in K–12 BAS rollouts).
4. **Adjacency.** The same Shodan scan surfaced two other named ICS devices on AT&T infrastructure in the St. Louis metro (`WalkerMedical`, `PowerHouse_1`).

⚠️ **Attribution caveat:** "KIPP St. Louis" is a strong working hypothesis from infrastructure pattern + locale, not a direct banner confirmation. Disclosure should be sent to KIPP St. Louis with explicit framing that we are seeking confirmation that this IP belongs to them and offering technical detail in support.

### Foreign Device Table history (2026-03-04 → 2026-04-20)

Shodan's 133 scans of `12.5.26.10` over this window captured the Foreign Device Table on each scan. Four distinct internal controllers in the `10.20.80.0/24` subnet registered through this BBMD:

| Internal IP | Scans seen | First seen | Last seen | Source port | TTL | Status |
|-------------|-----------|------------|-----------|-------------|-----|--------|
| `10.20.80.181` | 39 | 2026-03-12 | 2026-04-06 | 47808 (static) | 60 | Retired 2026-04-07 |
| `10.20.80.175` | 33 | 2026-04-07 | 2026-04-20 | 47808 (static) | 60 | **Currently active** |
| `10.20.80.98`  | 5  | 2026-03-31 | 2026-04-01 | 47808 (static) | 60 | Brief registration |
| `10.20.80.210` | 3  | 2026-03-06 | 2026-03-07 | 47808 (static) | 60 | Brief registration |
| `10.20.80.125` | 1  | 2026-03-04 | 2026-03-04 | 47808 (static) | 60 | Single observation |

**Two operationally significant patterns:**

1. **The `.181 → .175` handoff on 2026-04-07.** `.181` stopped appearing at `2026-04-06 23:23 UTC`; `.175` first appeared at `2026-04-07 11:56 UTC` — a ~13-hour window. Same subnet, same port (47808), same TTL (60). This reads as either a controller swap, a DHCP-driven IP change, or a zone relocation. Either way, the BBMD kept routing without interruption.
2. **Static port 47808 on all registrations.** No rotating ephemeral ports (the WalkerMedical pattern). This is standard BACnet/IP behavior from an in-building controller using the canonical 0xBAC0 port — i.e., these look like legitimate internal devices, not NAT-ed clients calling home.

**FDT vs. BDT — important distinction.** The 13 internal subnets in the BDT (`10.X.3.15` pattern, from the existing wiki) describe **outbound broadcast routing** — where this BBMD forwards BACnet broadcasts it receives. The FDT entries above describe **inbound Foreign Device registrations** — devices that have explicitly registered with this BBMD to receive broadcasts. Both columns of the routing table are internet-reachable, but the FDT is the direct-message surface: write attempts from the internet can be delivered to any Foreign Device the BBMD knows about.

### BBMD blast radius

| Aspect | Value |
|--------|-------|
| Externally reachable | UDP 47808 from any internet client |
| Authentication | None (BACnet/IP standard) |
| Internal subnets behind BBMD | 13 |
| Controllers visible | At minimum 13 (one per subnet via `.X.3.15` pattern) |
| KIPP campuses likely affected | All 6 (~2,700 students) |
| Writable BACnet objects | Analog Output, Binary Output, Multi-State Output, Schedule, Calendar |

What this means in classroom terms:
- **HVAC setpoints** — temperature, humidity, ventilation rates per classroom
- **Schedules** — daily/weekly run times for unit ventilators, RTUs, AHUs
- **Outdoor air dampers** — fresh air supply (post-COVID a regulated parameter in schools)
- **Boiler / chiller enable** — building-wide heat/cool availability
- **Lighting / occupancy** — depending on integration depth

### CVE exposure

The Delta Controls DSC-1616E is a long-lived product line. A specific firmware version was not captured in the available banner. The device family has been the subject of multiple CISA advisories over the years; firmware-level CVE exposure cannot be confirmed passively. ⚠️ Treat as version-unknown pending vendor verification.

The BBMD itself does not need a CVE to be a problem — **unauthenticated BACnet WriteProperty is a standard protocol behavior, not a vulnerability**. The exposure is the architecture, not a bug.

### Risk in context — why a school is not "lower stakes"

Building automation in K–12 facilities is patient-safety adjacent in ways that often go unacknowledged:

- **Asthma and respiratory conditions** — disabled or misconfigured ventilation in occupied classrooms triggers attacks. ~1 in 12 US children has asthma.
- **Heat exposure** — disabled cooling during late spring or early fall in St. Louis summers (95°F+ heat indexes) creates rapid hyperthermia risk in young children.
- **Carbon dioxide buildup** — defeated outdoor-air dampers cause cognitive impairment within hours; long-known to degrade test performance and trigger headaches/nausea in classrooms.
- **Schedule manipulation** — disabling night setback (intentional energy waste) or running boilers in summer (equipment damage + fire risk) are both reachable from a writable Schedule object.
- **Cascading effect** — unlike a single-building exposure, **one action against this BBMD propagates to every KIPP campus simultaneously**. There is no isolation between sites.

The combination of (a) life-safety relevance, (b) child population, and (c) 6-site simultaneous exposure is the wow.

---

## Disclosure contacts

### Primary — KIPP St. Louis network

**KIPP St. Louis (regional organization)**
- Address: 1310 Papin Street, Suite 203, St. Louis, MO 63103
- Phone: (314) 349-1388
- Web: [kippstl.org/contact](https://www.kippstl.org/apps/contact/)
- Principal officer: Kelly Garrett

Ask for: IT director, facilities director, or operations lead. Do not give technical detail to the front-desk receptionist; request a written intake channel.

### Secondary — KIPP national support

**KIPP Foundation (national)**
- Web: [kipp.org/contact](https://www.kipp.org/contact/)

KIPP National has a regional support function and may have a security contact who can route the report internally.

### Vendor coordination

**Delta Controls**
- Security bulletins: deltacontrols.com
- For BACnet/BBMD exposure pattern (not a CVE), Delta's role is integrator-education, not patching.

### Coordinated disclosure escalation

**CISA K–12 Cybersecurity** — cisa.gov/K12Cybersecurity / report@cisa.gov
**CISA ICS-CERT** — cisa.gov/report

Escalate to CISA if no KIPP response within 30 days. CISA has a specific K-12 cybersecurity team given the surge in school-targeted incidents.

**Missouri Department of Elementary and Secondary Education (DESE)** — Charter Schools Office. Tertiary path if KIPP and CISA are non-responsive.

---

## Recommended disclosure message

> **Subject:** Security Disclosure — Internet-Exposed Building Control System Likely Belonging to KIPP St. Louis
>
> I am a security researcher conducting passive OSINT analysis of internet-exposed industrial control systems. Using only data already indexed by Shodan (no active scanning, no probing, no interaction with any systems), I identified what I believe is a serious exposure on infrastructure operated by KIPP St. Louis. I am writing to confirm attribution and to share technical detail in good faith.
>
> **What was found:**
> A Delta Controls DSC-1616E BACnet site controller (device name "Mitchell") at IP `12.5.26.10` on AT&T Business is configured as an internet-facing BACnet Broadcast Management Device (BBMD) with no authentication. It bridges the public internet to **13 internal building automation subnets** in a regular pattern strongly consistent with a multi-campus K–12 deployment. Geographic and infrastructure context point to KIPP St. Louis.
>
> **Why this matters:**
> Unlike a single-building exposure, a BBMD configured this way means **a single action from any internet host can affect every campus reachable through this device simultaneously.** BACnet has no authentication — any BACnet client on the internet can enumerate, read, and potentially write to building automation objects (HVAC setpoints, ventilation schedules, outdoor-air dampers, boiler enables) across the network.
>
> In a school setting, the practical concerns are:
> - **Asthma triggers** from disabled or misconfigured ventilation
> - **Heat exposure** if cooling is disabled in summer
> - **CO₂ buildup** from defeated outdoor-air dampers (degrades cognition, triggers headaches)
> - **Equipment damage** from out-of-season boiler/chiller operation
>
> **Recommended immediate actions:**
> 1. Block UDP port 47808 inbound at your perimeter firewall right now
> 2. Confirm that `12.5.26.10` belongs to KIPP St. Louis
> 3. If yes, engage your BMS integrator (likely the firm that installed the Delta Controls system) to audit BBMD configuration
> 4. Replace any legitimate remote BACnet access with VPN + private BBMD
> 5. Audit the Foreign Device Table for any unauthorized registrations
>
> I have no intention of accessing, testing, or interacting with your systems. I am disclosing this in good faith. I am available to provide full technical details — including the specific subnet pattern observed — to your IT, facilities, or BMS integration team.

---

## Remediation checklist

- [ ] Confirm IP attribution (`12.5.26.10` belongs to KIPP St. Louis network)
- [ ] Block UDP 47808 inbound at perimeter firewall immediately
- [ ] Audit Foreign Device Table for unauthorized registrations
- [ ] Engage BMS integrator for end-to-end BBMD configuration review
- [ ] Determine why all 13 BACnet subnets route through one internet-facing device (likely a remote-access shortcut for the integrator that was never replaced with VPN)
- [ ] Segment BACnet network from routable IT subnets
- [ ] Replace internet-facing BBMD with VPN-gated private BBMD for any legitimate remote access
- [ ] Audit access logs for evidence of BACnet enumeration or write attempts
- [ ] Roll the same audit across any sister KIPP regions using the same integrator

---

## Timeline

| Date | Event |
|------|-------|
| 2026-03-04 | First Shodan observation of a Foreign Device (`10.20.80.125`) registering through this BBMD |
| 2026-03-12 | `10.20.80.181` begins persistent registration (39 scans over next 25 days) |
| 2026-04-06 | `10.20.80.181` last observed |
| 2026-04-07 | `10.20.80.175` first observed — clean handoff, same subnet/port/TTL (now 33 scans and counting) |
| 2026-04-19 | Passive OSINT scan identified `Mitchell` BBMD at `12.5.26.10` |
| 2026-04-20 | KIPP St. Louis attribution hypothesis formed; disclosure draft written |
| 2026-04-20 | Longitudinal history pulled — four internal controllers registered through BBMD across 47-day window |
| Pending | Contact KIPP St. Louis IT/facilities |
| Pending | Confirm attribution before sharing full technical detail |
| T+30 days | Escalate to CISA K-12 Cybersecurity if no response |

---

## Open questions

- Is `Mitchell` named after the integrator (a person), the building, or a campus? "Mitchell" is not a KIPP St. Louis school name (their schools include KIPP Inspire, KIPP Wonder, KIPP Triumph, KIPP Wisdom, KIPP Victory, KIPP St. Louis High).
- Are the 13 subnets the full KIPP footprint, or do they represent a subset (e.g., only campuses on a single integrator's contract)?
- Does the same integrator serve other KIPP regions? If yes, this is potentially a multi-region disclosure.
- Did the integrator configure this BBMD, or was it set up by KIPP IT in-house?
- What prompted the `10.20.80.181 → .175` handoff on 2026-04-07? Controller replacement, zone relocation, or just a DHCP lease expiry? A controller swap suggests an active maintenance relationship with an integrator who could be the first remediation contact.
- Why does only the `10.20.80.0/24` subnet appear in the FDT while the BDT advertises 13 `10.X.3.15` subnets? Are controllers in the other 12 subnets not configured to register as Foreign Devices (i.e., they rely on broadcast routing only), or are they segmented off from the BBMD but still reachable via broadcast relay?

## Ethical scope

All findings derived from Shodan's passive index. No active probing, no connections to target systems, no BACnet packets sent, no interaction with any objects. The internal subnet structure was inferred from BACnet broadcast routing tables that Shodan captured passively. Data used for security research and responsible disclosure only.
