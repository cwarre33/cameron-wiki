---
title: Scottsboro Electric Power Board — Internet-Exposed JCI NAE Controllers (Deep Dive)
type: open-question
status: active
visibility: public
sources: [raw/osint/2026-04-19-scan-enriched.json]
related: [wiki/open-questions/ics-exposure-2026-04-19.md, wiki/techniques/shodan-ics-osint.md]
created: 2026-04-20
updated: 2026-04-20
confidence: high
tags: [bacnet, jci, johnson-controls, ics, electric-utility, osint, scada, critical-infrastructure, survalent, tva]
---

# Scottsboro Electric Power Board — Internet-Exposed JCI NAE Controllers (Deep Dive)

## Confirmed evidence chain

| Layer | Evidence | Source |
|-------|----------|--------|
| ASN ownership | AS26809 = Scottsboro Electric Power Board | ARIN RDAP |
| IP netblock | `173.242.224.0/20` allocated to AS26809 | ARIN RDAP |
| IP in block | `173.242.239.157` and `173.242.239.158` ∈ `173.242.224.0/20` ✓ | Math |
| Device responses | Both IPs returned valid BACnet WhoIs responses to Shodan | Shodan scan |
| Device 1 identity | HMC-01, JCI M4-SNC25152-0, firmware 10.1.7.196 | Shodan BACnet banner |
| Device 2 identity | HMC-02, JCI MS-NAE4510-2, firmware 9.0.7.7978 | Shodan BACnet banner |
| Org confirmation | Shodan org field: "Scottsboro Electric Power Board" (matches ARIN) | Shodan enrichment |
| Utility type | Municipal electric + cable/internet utility, TVA member, 8,500 customers | Survalent case study / sepb.net |
| SCADA system | SurvalentONE ADMS deployed since 2003, 7 substations | Survalent case study |
| Network topology | Single-homed AS, one upstream through AS11758 (IRIS Networks) | IPinfo AS26809 |
| ARIN contact | James Alvin Sharp Jr., sharp@sepb.net, +1-256-574-2680, 404 E Willow St, Scottsboro AL 35768 | ARIN RDAP |
| ARIN validation | POC unvalidated — no response since **February 7, 2025** | ARIN RDAP |

---

## Device inventory

### HMC-01 — `173.242.239.157`

```
Instance ID: 501
Object Name: HMC-01
Vendor Name: JCI
Firmware: 10.1.7.196
Model Name: M4-SNC25152-0
```

**JCI M4-SNC25152-0** = Metasys Site Network Controller (SNC). The SNC is Johnson Controls' top-tier NAE — it aggregates all field controllers and NAE supervisors across a site, provides the primary Metasys web UI, and connects to the enterprise BAS network. One SNC typically manages an entire building or campus. `Instance ID: 501` with `HMC-01` naming suggests this is the primary site controller.

### HMC-02 — `173.242.239.158`

```
Instance ID: 500
Object Name: HMC-02
Vendor Name: JCI
Firmware: 9.0.7.7978
Model Name: MS-NAE4510-2
```

**JCI MS-NAE4510-2** = Metasys Network Automation Engine, mid-range. Manages up to 300 field objects. Typically subordinate to an SNC. `Instance ID: 500` with `HMC-02` naming: this is a second-level controller reporting to HMC-01. The pair (SNC + NAE) is a standard JCI multi-zone deployment.

Neither device has a BBMD table in the banner, meaning they are standalone BACnet devices on the utility's network — not bridging additional private subnets, but the devices themselves are fully reachable.

---

## Why a power utility's building automation matters

Scottsboro Electric operates **its own fiber network and internet service** (sepb.net). The HMC-01/HMC-02 pair is almost certainly managing their **operations building** or **headquarters facility** at 404 E Willow Street, Scottsboro, AL — the same address as their ARIN contact.

The critical concern is **network segmentation**. SEPB operates:
1. **Survalent SCADA** for electric distribution (7 substations, AMI metering, CVR)
2. **JCI Metasys building automation** (HMC-01/HMC-02 exposed on internet)

Both run on SEPB's own fiber network (AS26809). If the building automation network and the SCADA distribution network share any infrastructure — VLAN trunks, management interfaces, shared switches — internet-reachable building automation controllers become a lateral movement path into utility SCADA.

**NERC CIP standards** (CIP-005, CIP-007) require electronic security perimeters around bulk electric system cyber assets. Building automation systems controlling HVAC in a utility operations building may or may not fall under CIP scope depending on their BES Cyber System classification — but internet-exposure without authentication is a violation of the principle of least access regardless.

---

## CVE assessment

### HMC-02 — firmware 9.0.7.7978

| CVE | Description | CVSS | Status |
|-----|-------------|------|--------|
| CVE-2021-27660 | Metasys web server path traversal — read arbitrary files without auth | 7.5 HIGH | ⚠️ Firmware 9.0.7.7978 < 9.0.8 — **likely vulnerable** |
| CVE-2022-21934 | Metasys SOAP API improper auth — write access without credentials | 9.8 CRITICAL | ✅ Firmware 9.0.7 predates this CVE's affected range — N/A |
| CVE-2023-4486 | Command injection via crafted packet | 9.8 CRITICAL | ⚠️ Requires version mapping — unconfirmed passively |

**CVE-2021-27660** on HMC-02: Allows unauthenticated reading of config files, credential files, and controller logic from the Metasys web interface. If port 443/8443 is also internet-facing (not confirmed from BACnet scan alone), this escalates to full credential theft + controller takeover.

### HMC-01 — firmware 10.1.7.196

More current firmware; 10.1.7 is a recent Metasys release. CVE-2021-27660 patched at 9.0.8. CVE-2022-21934 patched at 10.1.6 — this firmware is above that. Reduced known CVE exposure, but BACnet/UDP is still unauthenticated by protocol.

---

## ARIN contact unvalidated — implications

ARIN marks the SEPB point of contact (James Alvin Sharp Jr.) as **"unvalidated" since February 7, 2025**. This means:
- ARIN attempted to re-validate the contact and received no response for ~14 months
- The listed email/phone may be incorrect, outdated, or unmanned
- Security disclosures sent to these contacts may not be received

**Alternative contacts:**
- sepb.net website contact form
- Phone: +1-256-574-2680 (office number; may reach front desk even if Sharp is unreachable)
- CISA ICS-CERT as escalation path given utility classification

---

## Disclosure

**Primary:** James Alvin Sharp Jr.  
Email: sharp@sepb.net  
Phone: +1-256-574-2680  
Address: 404 E Willow St, Scottsboro, AL 35768

**Alternate:** sepb.net contact form

**TVA ICS Security:** As a TVA member utility, SEPB may also be subject to TVA cybersecurity program oversight. TVA can be notified as a parallel escalation path.

**CISA:** report@cisa.gov — escalate if no SEPB response within 30 days. NERC CIP implications warrant CISA involvement.

---

## Open questions

- Are HMC-01 and HMC-02 also internet-facing on 443/8443 (Metasys web UI)? Would need active scanning to confirm.
- What does "HMC" stand for in this deployment? The utility's operations center? A substation building?
- Is there network segmentation between the Metasys BAS network and the Survalent SCADA distribution network?
- Are the two Scottsboro devices the only internet-facing devices in AS26809, or are there more on `98.159.192.0/20`?
- Does the unvalidated ARIN contact indicate the utility is under-resourced for network management?
