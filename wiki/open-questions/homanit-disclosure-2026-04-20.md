---
title: Responsible Disclosure — Homanit Lietuva BACnet Exposure (Pagiriai)
type: open-question
status: active
visibility: public
sources: [raw/osint/2026-04-19-scan-enriched.json, raw/osint/2026-04-20-longitudinal.json]
related: [wiki/open-questions/bacnet-bbmd-exposure-2026-04-19.md, wiki/open-questions/walkermedical-disclosure-2026-04-19.md, wiki/open-questions/kipp-mitchell-disclosure-2026-04-20.md, wiki/open-questions/bacnet-fdt-external-tunnels-2026-04-21.md, wiki/techniques/shodan-ics-osint.md]
created: 2026-04-20
updated: 2026-04-21
confidence: high
tags: [bacnet, ics, responsible-disclosure, homanit, wago, mdf, hdf, combustible-dust, nfpa-664, atex, lithuania, manufacturing]
---

# Responsible Disclosure — Homanit Lietuva BACnet Exposure (Pagiriai)

## Summary

An internet-facing BACnet device (`Homanit.VAS_LNS_1`, WAGO controller) at IP `85.206.88.54` in Lithuania bridges the public internet to the building automation systems of **Homanit Lietuva's MDF/HDF wood-fiberboard plant in Pagiriai, Vilnius**. The plant produces ~260,000 m³/yr of medium- and high-density fiberboard; production processes generate large volumes of fine wood dust.

**The wow finding (updated 2026-04-20):** Wood-fiberboard manufacturing is a regulated combustible-dust environment. Loss of integrity in HVAC / dust collection / ventilation control crosses out of "comfort" into the **explosion-hazard regime governed by NFPA 664 (US) and ATEX 2014/34/EU + 1999/92/EC (EU)**. The control of those systems is reachable from any point on the internet with no authentication.

**Stronger than that — we now have evidence of active third-party cloud connectivity, not just theoretical exposure.** Longitudinal Shodan history analysis (126 distinct scan observations since 2026-04-03) shows **two external DigitalOcean IPs** maintaining persistent Foreign Device Table registrations to this BBMD continuously for 17+ days. See "Active external cloud tunnels" section below.

**All data is from Shodan's passive index. No systems were probed, accessed, or interacted with.**

---

## Technical findings

### Device identification

| Field | Value |
|-------|-------|
| Public IP | `85.206.88.54` |
| Country | Lithuania (LT) |
| Device name (BACnet) | `Homanit.VAS_LNS_1` |
| Vendor | WAGO |
| Internal subnets reachable | 2 |
| BACnet port | UDP 47808 |
| Inferred operator | Homanit Lietuva, MDF/HDF plant, Pagiriai (Vilniaus r.) |
| Attribution confidence | High — device name contains operator name |

### Why this attribution is high-confidence

Unlike `Mitchell` (KIPP) which required pattern inference, `Homanit.VAS_LNS_1` carries the operator name in the BACnet device label. The `.VAS_LNS_1` suffix is consistent with a building/system designator (likely a specific production hall or air-handling system, e.g. "VAS" for ventilation/air system, "LNS" for line/zone). The Lithuanian geo on the IP matches Homanit's only Lithuanian site (Pagiriai, near Vilnius).

### Plant context

| Aspect | Value |
|--------|-------|
| Operator | Homanit Lietuva (subsidiary of HOMANIT GmbH & Co. KG, Germany) |
| Site | Pagiriai, Vilniaus rajonas, Lithuania |
| Address | Šiltnamių g. 29, Pagirių k., Vilniaus rajonas |
| Product | MDF (medium-density fiberboard) and HDF (high-density fiberboard), thicknesses up to 22 mm |
| Capacity | ~260,000 m³/yr |
| Investment | ~€175M |
| Operational | Plant operations 2022+, commercial fiberboard production since 2025 |
| Process units on site | Fiber refining, drying, mat forming, hot pressing, sanding, painting, laminating, cutting, milling — full-line finishing |

### Risk in context — why this is "explosion regime" not "comfort regime"

MDF/HDF manufacturing produces fine wood fibers and dust at multiple stations:
- **Refining and drying** — fine fiber suspended in heated air streams
- **Sanding** — submicron wood dust, classified as a **Class II Group G** combustible dust under US NEC; **Group IIIA/IIIB** under EU ATEX zoning
- **Conveying and dust collection** — large baghouses and cyclones carrying high dust loadings
- **Press exhaust** — formaldehyde, VOCs, and fine particulate

The applicable safety regimes:

| Regime | Standard | What it requires |
|--------|----------|-------------------|
| US | **NFPA 664** — Standard for the Prevention of Fires and Explosions in Wood Processing and Woodworking Facilities | Hazard analysis, dust control, ignition source control, explosion venting/suppression |
| EU | **ATEX Directive 2014/34/EU** (equipment) + **1999/92/EC** (workplace) | Zone classification (20/21/22 for dust), zone-rated equipment, explosion protection document |

Building automation controls that BACnet-write can directly affect:
- **Dust collection fan setpoints** — under-ventilating accumulates dust to MEC (minimum explosible concentration); over-ventilating may stir settled dust
- **Process exhaust dampers** — diverting hot/dusty air streams
- **Make-up air handlers** — pressurization that prevents dust migration
- **Inerting / suppression actuators** — if integrated to the BAS
- **Fire-damper schedules and overrides** — life-safety bypass

⚠️ **It cannot be confirmed passively whether the BACnet network behind this BBMD reaches dust-collection, process-exhaust, or fire-safety actuators, or only HVAC/comfort systems.** That distinction determines whether this is a comfort-impact exposure or a process-safety exposure. Either way, the architecture is wrong; the upper bound of the impact is what makes this category of exposure newsworthy.

### Active external cloud tunnels — 17-day evidence (the critical finding)

Longitudinal Shodan history (`api.host(ip, history=True)` → 1,000 observations, 2026-04-03 through 2026-04-20) shows **two external public IPs maintaining persistent Foreign Device Table registrations** to this BBMD:

| Foreign Device IP | Hosting | Scans observed | First seen | Last seen | Source port pattern |
|-------------------|---------|----------------|-----------|-----------|---------------------|
| `157.245.127.71` | DigitalOcean (157.245.0.0/16) | 126 | 2026-04-03 | **2026-04-20 (today)** | Static: port 33371 |
| `104.131.63.228` | DigitalOcean (104.131.0.0/16) | 126 | 2026-04-03 | **2026-04-20 (today)** | **Rotating across 13 distinct ports** (32905, 36930, 37390, 41163, 41164, 44504, 44739, 46308, 47396, 56741, 58750, 59898, 60293) |

**What this means:**

Unlike WalkerMedical's pattern (an *internal* RFC1918 device tunneling out through the BBMD), both of these registrations are from **public internet IPs on DigitalOcean cloud infrastructure tunneling in**. They are not on Homanit's internal network; they are foreign devices on the other side of the internet establishing persistent BACnet reachability.

The rotating-source-port behavior on `104.131.63.228` across 13 distinct ports is consistent with a long-running software client that re-registers on every connection (each TCP/UDP bind gets a new ephemeral port). This is active software, not a stale entry.

**Possible explanations, ranked:**

1. **Cloud-hosted BMS SaaS analytics.** A legitimate third-party monitoring/optimization service phoning home. Even if authorized by Homanit, this architecture (unauthenticated BACnet over public internet from cloud VMs) is unacceptable for an ATEX-regulated facility.
2. **Integrator's remote-management bridge.** A commissioning/service contractor running a tunnel box on cloud infra for their own remote access. Common, architecturally wrong, and often forgotten post-install.
3. **Unauthorized persistent access.** Someone has set up DigitalOcean droplets as BACnet clients to maintain access. Lower probability but non-zero — and distinguishing (1)/(2) from (3) is exactly what Homanit's facilities/IT team needs to do.

All three cases require **immediate action**. Disclosure framing should be: "we are not telling you what this is — we are telling you that two external cloud IPs have had persistent BACnet access to your plant for 17+ days and only your facilities/IT team can distinguish approved from unapproved."

**Why the FDT entries look like public IPs:** Foreign Device registration under BACnet/IP lets any device that can reach the BBMD register itself. The BBMD doesn't distinguish between a legitimate RFC1918 internal device joining across subnets and a public-IP device joining from across the internet — both are just entries in the FDT. A correctly-firewalled BBMD should never see public-IP FDT entries. The fact that Homanit's BBMD has two is itself the finding.

**Homanit is not unique — 2026-04-21 update.** A broader longitudinal sweep of 17 BBMDs surfaced **12 cases** of this external-public-IP FDT pattern. See [[bacnet-fdt-external-tunnels-2026-04-21]] for the full catalogue (AWS-hosted, Azure-hosted, and a shared integrator endpoint that bridges two different buildings). What keeps Homanit at the top of the disclosure queue is **the combination**: ATEX/NFPA-664 combustible-dust context + two cloud tunnels active for 17 days + rotating-port behavior on one tunnel indicating active software, not a stale entry.

### CVE / firmware exposure

WAGO controllers (PFC100, PFC200, 750-series) have been the subject of multiple CISA advisories in recent years (CVE-2019-5079, CVE-2021-21001, CVE-2022-45138 family, others). A specific firmware version was not captured in the available banner. ⚠️ Treat as version-unknown pending vendor verification.

The bigger architectural issue is the same as Walker Medical and KIPP: **internet-facing BACnet does not need a CVE to be unsafe** — protocol-standard unauthenticated WriteProperty is sufficient.

---

## Disclosure contacts

### Primary — operator (Lithuanian subsidiary)

**Homanit Lietuva, UAB**
- Address: Šiltnamių g. 29, Pagirių k., Vilniaus rajonas, Lithuania
- Phone: +370 669 61 909
- Email: info@homanit.lt
- Web: [homanitlietuva.lt/kontaktai](https://www.homanitlietuva.lt/kontaktai/)

Ask for: site facilities/maintenance manager AND IT/OT security contact. Plant operations and IT may be split across the German parent and the Lithuanian site.

### Parent company — Germany

**HOMANIT GmbH & Co. KG**
- Web: [homanit.org](https://www.homanit.org/en/)
- Headquarters: Losheim am See, Saarland, Germany

The German parent likely owns IT/OT architecture decisions across all four group factories (Germany, Poland ×2, Lithuania). Disclosure should reach both Lithuanian operations and German corporate IT.

### Vendor coordination

**WAGO Kontakttechnik GmbH & Co. KG** (Germany)
- Security: WAGO PSIRT — psirt@wago.com (verify current address on wago.com/security)
- WAGO maintains a published security advisory program for their controllers.

### National coordination

**NKSC — Lithuanian National Cyber Security Centre** (CERT-LT)
- Web: nksc.lt
- The competent national CSIRT for Lithuanian critical-infrastructure exposures. Forestry/wood processing is a notable Lithuanian industrial sector.

### Coordinated disclosure escalation

If primary contacts are unresponsive within 30 days:
- **CISA ICS-CERT** — cisa.gov/report (US, but accepts cross-border reports for vendor coordination with WAGO)
- **CERT-EU** — for EU-wide coordination given the parent company is German

---

## Recommended disclosure message

> **Subject:** URGENT — Active External BACnet Tunnels Detected at Homanit Lietuva (Pagiriai Plant)
>
> I am a security researcher conducting passive OSINT analysis of internet-exposed industrial control systems. Using only data already indexed by Shodan (no active scanning, no probing, no interaction with any systems), I identified an exposure at your Pagiriai plant that requires immediate attention.
>
> **What was found:**
> A WAGO BACnet controller (device name `Homanit.VAS_LNS_1`) at IP `85.206.88.54` is reachable from the public internet on UDP port 47808 with no authentication.
>
> **More importantly:** Shodan's historical index shows **two external public IPs on DigitalOcean cloud infrastructure** (`157.245.127.71` and `104.131.63.228`) have maintained persistent BACnet Foreign Device Table registrations to your controller **continuously since 2026-04-03 — 17+ days as of today, across 126 distinct Shodan observations.** One of them rotates across 13 different source ports, indicating active software that re-registers on every connection. These are not stale entries and they are not on your internal network.
>
> Whether these are (a) a third-party service contracted by your facilities team, (b) your integrator's remote-management setup, or (c) unauthorized access is something only your team can determine. Any of those answers requires immediate change. Cases (a) and (b) still represent an architecturally unacceptable remote-access path for an ATEX-regulated facility; case (c) is an active incident.
>
> **Why this matters for an MDF/HDF facility specifically:**
> Wood-fiberboard manufacturing is a combustible-dust environment governed by ATEX 2014/34/EU and 1999/92/EC. Building-automation control over dust-collection fans, process-exhaust dampers, make-up air, fire-damper schedules, and ventilation setpoints is directly safety-relevant. Even if this specific BACnet network reaches only HVAC/comfort systems and not process-safety actuators, that architectural separation should be confirmed and documented — and the perimeter exposure should be removed regardless.
>
> **Recommended immediate actions:**
> 1. Block UDP port 47808 inbound at your perimeter firewall right now
> 2. Confirm what process and life-safety systems are reachable via the BACnet network behind this controller
> 3. Engage WAGO support to verify firmware version and applicable advisories
> 4. Engage your BAS/integrator to audit BBMD and Foreign Device Table configuration
> 5. Replace any legitimate remote BACnet access with VPN-gated private BBMD
>
> I have no intention of accessing, testing, or interacting with your systems. I am disclosing this in good faith and am available to provide full technical detail to your IT, OT, or facilities team — and to coordinate with NKSC (CERT-LT) and WAGO if you prefer that route.

---

## Remediation checklist

- [ ] **URGENT:** Identify `157.245.127.71` and `104.131.63.228` — are these contracted services, integrator infrastructure, or unknown?
- [ ] **URGENT:** If unknown, treat as active intrusion — preserve BBMD state (FDT snapshot, access logs) before remediation
- [ ] Block UDP 47808 inbound at perimeter firewall immediately (this kills the tunnels and removes the exposure in one step)
- [ ] Identify and document which BACnet objects/controllers are reachable behind `Homanit.VAS_LNS_1`
- [ ] Confirm whether dust-collection, process-exhaust, or fire-safety actuators are integrated to this BAS network
- [ ] If yes: treat exposure as ATEX/explosion-protection-relevant and trigger relevant change-control + insurer notification
- [ ] Contact WAGO PSIRT for firmware version cross-reference against advisories
- [ ] Audit BBMD Foreign Device Table for unauthorized registrations (the two DigitalOcean IPs are the first place to look)
- [ ] Audit BAS access logs for evidence of enumeration or write attempts from either DigitalOcean IP
- [ ] Segment BAS from any routable internet-reachable subnet
- [ ] Replicate audit at sister Homanit plants (Losheim, Poland ×2) — same parent IT may have replicated the architecture, and if these tunnels are a shared service the pattern will exist there too

---

## Timeline

| Date | Event |
|------|-------|
| 2026-04-03 | Earliest DigitalOcean tunnel observation (both external IPs registered simultaneously) |
| 2026-04-19 | Passive OSINT scan identified `Homanit.VAS_LNS_1` BACnet exposure |
| 2026-04-20 | Operator attribution confirmed via banner; initial disclosure draft written |
| 2026-04-20 | Longitudinal Shodan history analysis surfaced 126-scan active DigitalOcean tunnels — disclosure escalated from "exposure" to "active external connectivity, 17-day-old" |
| Pending | Contact Homanit Lietuva (info@homanit.lt) and German parent corporate IT |
| Pending | Pre-notify NKSC (CERT-LT) given potential ATEX relevance |
| T+7 days | Escalate to NKSC if no response (shortened window vs standard 30 days given active-tunnel evidence) |

---

## Open questions

- What does `VAS_LNS_1` mean? Likely a system designator (ventilation/air system, line/zone 1) — operator confirmation would clarify scope.
- Is the same architecture replicated at the German and Polish Homanit plants? If yes, disclosure scope expands to multi-country.
- Does Homanit have a published security.txt or PSIRT? If not, this is a useful structural recommendation.
- Are NKSC and CERT-LT the right first-contact in Lithuania, or should the report go via the German parent's CSIRT relationships?

## Ethical scope

All findings derived from Shodan's passive index. No active probing, no connections to target systems, no BACnet packets sent, no interaction with any objects. Data used for security research and responsible disclosure only.
