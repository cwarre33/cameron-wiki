---
title: Responsible Disclosure Letters — All Targets 2026-04-20
type: open-question
status: active
visibility: public
sources: [raw/osint/2026-04-19-scan-enriched.json]
related: [wiki/open-questions/exploitability-assessment-2026-04-20.md, wiki/open-questions/niagara-admin-capabilities-2026-04-20.md, wiki/open-questions/cve-2019-9569-confirmed-hosts-2026-04-20.md, wiki/open-questions/scottsboro-electric-power-board-2026-04-20.md, wiki/open-questions/municipal-ics-cluster-2026-04-20.md, wiki/open-questions/walkermedical-disclosure-2026-04-19.md]
created: 2026-04-20
updated: 2026-04-20
confidence: high
tags: [responsible-disclosure, bacnet, ics, osint]
---

# Responsible Disclosure Letters — All Targets 2026-04-20

All letters follow the same structure: specific findings, no exploitation details, concrete immediate actions, clear offer of technical follow-up. Sender identified as security researcher using only publicly indexed passive data.

---

## LETTER 1 — Lahey Health System (HIGHEST PRIORITY)

**To:** Lahey Health System Security / Compliance  
**Contact:** compliance@lahey.org / +1-781-744-5100  
**Re:** Internet-Exposed Building Automation Controller with Critical Vulnerability — Lahey Medical Market Street  
**Escalation if no response:** CISA ICS-CERT (report@cisa.gov) within **14 days** (healthcare critical infrastructure)

---

Subject: Security Disclosure — Internet-Exposed Building Automation System, Lahey Medical Market Street Facility

Dear Lahey Health System Security Team,

I am an independent security researcher. Using only data already publicly indexed by Shodan (a passive internet scanning service), I have identified a serious security exposure affecting a building automation controller at your Market Street outpatient facility.

**What was found:**

A Tridium Niagara 4 building automation controller (device name `LaheyMedical_MarketStreet_1000`) at IP address `166.148.23.176` is accessible from the public internet. The controller is running Tridium Niagara version **4.4.73.24**.

This firmware version is confirmed vulnerable to **CVE-2017-16748** (CVSS 9.8 Critical — the highest possible severity rating). This vulnerability allows any person on the internet to log into your building management system with full **administrator-level access** by using a disabled account name and a blank password — no valid credentials required.

**What administrator access to Niagara means for your facility:**

Niagara administrator access goes far beyond reading sensor values. It enables:

- **Modification of control logic (Wire Sheet)** — the actual automation programs governing room pressurization, ventilation sequencing, temperature control, and safety interlocks. Logic changes are persistent and are not visible through standard point monitoring.
- **Extraction of all system credentials** — the station configuration file (`config.bog`) contains credentials for all users and all downstream connected systems, including HVAC field controllers.
- **Creation of persistent backdoor accounts** — new administrator accounts can be added that survive password changes and firmware updates.
- **Modification of operator displays** — HMI screens shown to facility staff can be altered to display false values while actual physical conditions differ.

**Why this is critical in a healthcare environment:**

Building automation in a medical facility controls life-safety infrastructure: room pressure differentials for surgical suites (positive pressure, ASHRAE 170) and isolation rooms (negative pressure for airborne infection containment), temperature ranges for medication storage and sterile environments, and ventilation for immunocompromised patient areas.

Wire sheet modification — which administrator access enables — can silently alter pressure control logic so that isolation rooms no longer maintain negative pressure, or surgical suites no longer maintain positive pressure, without any alert appearing on operator monitoring screens. This is an infection control risk with direct patient safety implications.

**I have not accessed, tested, or interacted with your systems in any way.** All data was retrieved from Shodan's passive public index.

**Recommended immediate actions:**

1. Block all inbound internet access to this controller's IP address (`166.148.23.176`) at your perimeter firewall immediately — this isolates the device from remote exploitation within minutes
2. Engage your building automation integrator to audit the Niagara station for unauthorized user accounts, wire sheet modifications, and installed modules
3. Contact Tridium (security@tridium.com) to upgrade to Niagara 4.4 Update 1 (version 4.4.92.2.1) or later, which patches CVE-2017-16748
4. Export and review the full user list in the Niagara station for any unrecognized accounts
5. Review audit logs for any login activity from unexpected IP addresses

I am available to provide full technical details to your IT security team, building automation integrator, or Tridium support. I have no intention of accessing or testing your systems further.

Respectfully,  
Cameron Warren  
cwarre33@charlotte.edu

---

## LETTER 2 — City of Cartersville, GA

**To:** Steven Lamar Grier, IT/Network Admin  
**Contact:** sgrier@cartersvillega.gov / +1-770-607-6299  
**Address:** 1 North Erwin St., Cartersville, GA 30120  
**Secondary:** Cartersville-Bartow County CVB (Clarence Brown Conference Center operator)  
**Escalation if no response:** CISA ICS-CERT within **30 days**

---

Subject: Security Disclosure — Critical Vulnerability in City Network Building Automation System, Clarence Brown Conference Center

Dear Mr. Grier,

I am an independent security researcher. Using only publicly indexed data from Shodan (a passive internet scanning service that crawls the public internet), I have identified a critical security vulnerability in a building automation controller on your city network (`CARTERSVILLE-FIBERCOM`, AS64261) serving the Clarence Brown Conference Center.

**What was found:**

A Delta Controls building automation controller (device name `ClarenceBrownAHUs`) at IP address `104.36.136.27` on your city-owned network is accessible from the public internet on UDP port 47808. This device manages the air handling units (HVAC) for the 40,000 sq ft Clarence Brown Conference Center.

The firmware running on this controller (Delta Controls V3.40, build **571848**) is confirmed vulnerable to **CVE-2019-9569** (CVSS 9.8 Critical). This is a buffer overflow vulnerability that allows any person on the internet to execute arbitrary code on the device — full remote takeover — without any credentials, by sending a single specially crafted network packet.

Additionally, the BACnet building automation protocol used by this device has no authentication by design. Before any exploit is needed, any computer on the internet that speaks BACnet can read all sensor values and write to all HVAC control outputs — changing temperature setpoints, disabling fans, modifying schedules, and shutting down climate control for the entire venue — without a username or password.

**What this means for the Clarence Brown Conference Center:**

An attacker can remotely set zone temperatures to extreme values, disable the air handling units entirely, modify the occupancy schedule so HVAC does not run during events, or trigger false alarm conditions — during a conference, wedding, or public event with hundreds of occupants in the building.

The CVE-2019-9569 exploit additionally allows persistent access: once an attacker has code execution on the BBMD gateway, they can reach all downstream HVAC controllers on your internal network at `10.21.175.x`.

**I have not accessed, tested, or interacted with your systems.** All data is from Shodan's public passive index.

**Recommended immediate actions:**

1. Block inbound UDP port 47808 at your perimeter firewall for IP `104.36.136.27` — this prevents internet access to the BACnet controller immediately
2. Contact Delta Controls (deltacontrols.com) to upgrade firmware from build 571848 (V3.40 R5) to build **612850 (V3.40 R6)** — this patches CVE-2019-9569
3. Investigate what device at `10.21.175.238` is maintaining a remote connection through this controller (it appears in the BBMD Foreign Device Table with an unusual 15-minute registration interval)
4. Engage your building automation integrator to audit all BACnet controllers on the `10.21.175.x` network for unauthorized configuration changes
5. Replace any legitimate remote BACnet access with VPN-gated private connectivity

I am available to provide full technical details to your IT team, the Conference Center's facilities staff, or your BAS integrator.

Respectfully,  
Cameron Warren  
cwarre33@charlotte.edu

---

## LETTER 3 — Chicago Boiler Room (RCN / Unknown Property Owner)

**To:** RCN Abuse Team (first contact — for subscriber identification and notification)  
**Contact:** abuse@rcn.com / noc@astound.com  
**Note:** Property owner unknown; ISP is fastest path to subscriber notification. Parallel report to AWS.  
**Also to:** AWS Trust & Safety — trustandsafety@support.aws.com (re: unexplained EC2 instance in FDT)  
**Escalation:** CISA ICS-CERT within **30 days**

---

Subject: Security Disclosure — Internet-Exposed Boiler Control System with Critical Vulnerability and Unexplained Cloud Tunnel, Chicago IL

Dear RCN/Astound Security Team,

I am an independent security researcher. I am writing to request subscriber notification for a serious security exposure identified on your network.

**What was found:**

An internet-accessible building control system at IP address `216.80.86.155` on your network (RCN-BLK-23, Chicago) is the HVAC/boiler controller for a multi-building residential or commercial complex. The device manages domestic hot water boilers, vacuum pumps, and temperature monitoring for "Building 6" of the property.

This controller (Delta Controls eBMGR, device name `B6 DHW Boilers_Vac Pumps_Temps`) is running firmware build **571848**, which is confirmed vulnerable to **CVE-2019-9569** (CVSS 9.8 Critical — remote unauthenticated code execution via a single malformed BACnet network packet).

**More critically:** I have identified an **active tunnel from an AWS EC2 cloud instance** into this building's private network. The controller's Foreign Device Table contains an active registration from `54.234.107.205` — an Amazon EC2 instance in Northern Virginia (`ec2-54-234-107-205.compute-1.amazonaws.com`) — with a 60-second refresh cycle. This means a cloud-hosted server is maintaining a live BACnet connection into the building's `192.168.15.x` internal network.

This EC2 instance has an auto-generated hostname with no custom domain, which is inconsistent with any legitimate building automation cloud service. It may represent:
- An unauthorized party who has already established remote access to this building's boiler infrastructure
- A legitimate but severely misconfigured remote management setup that exposes the building to the internet without VPN or authentication

**Physical risk:**

Unauthenticated BACnet access to domestic hot water boiler controls allows setpoint manipulation: water temperatures raised above 140°F (scalding risk) or lowered below 131°F (Legionella growth threshold per CDC guidelines). CVE-2019-9569 allows persistent code execution on the gateway controller and access to all devices on the `192.168.15.x` building network.

**Request:** Please identify and notify the subscriber at `216.80.86.155` of this exposure, and provide them with this report.

I am also notifying AWS Trust & Safety separately regarding the EC2 instance `54.234.107.205`, which is maintaining an active tunnel into a third-party building's private network infrastructure.

I have not accessed, tested, or interacted with any systems. All data is from Shodan's public index.

Respectfully,  
Cameron Warren  
cwarre33@charlotte.edu

---

**Parallel letter to AWS Trust & Safety** (trustandsafety@support.aws.com):

Subject: Potential Unauthorized EC2 Use — Active BACnet Tunnel into Third-Party Building Infrastructure

Dear AWS Trust and Safety Team,

I am reporting a potential misuse of an EC2 instance. EC2 instance at public IP **54.234.107.205** (`ec2-54-234-107-205.compute-1.amazonaws.com`, us-east-1) is maintaining an active Foreign Device Table registration in a Chicago building's BACnet boiler control system (`216.80.86.155`, RCN network).

This creates a live bidirectional BACnet tunnel from this EC2 instance into the building's private `192.168.15.x` LAN. The building controller has no authentication — any BACnet client registered in its FDT can enumerate and write to all building automation objects. The EC2 instance has an auto-generated hostname (no custom domain), which is inconsistent with known building automation cloud platforms.

I have no information on whether this EC2 instance belongs to a legitimate property manager or represents unauthorized third-party access. I am reporting it for your investigation.

The building controller (Delta Controls eBMGR build 571848) is also confirmed vulnerable to CVE-2019-9569 (CVSS 9.8 Critical).

Respectfully,  
Cameron Warren  
cwarre33@charlotte.edu

---

## LETTER 4 — Scottsboro Electric Power Board

**To:** James Alvin Sharp Jr., Network Operations  
**Contact:** sharp@sepb.net / +1-256-574-2680  
**Address:** 404 E Willow St, Scottsboro, AL 35768  
**Note:** ARIN contact unvalidated since Feb 2025 — call the main number if email bounces  
**Escalation:** CISA ICS-CERT within **14 days** (electric utility critical infrastructure; NERC CIP implications)

---

Subject: Security Disclosure — Internet-Exposed Building Automation Controllers on Scottsboro Electric Network, Possible NERC CIP Compliance Concern

Dear Mr. Sharp,

I am an independent security researcher. Using only data from Shodan's public internet index, I have identified two building automation system controllers that are accessible from the public internet on your organization's own network (AS26809, `173.242.224.0/20`).

**What was found:**

Two Johnson Controls (JCI) Metasys Network Automation Engines are internet-accessible on BACnet UDP port 47808:

| IP Address | Device Name | Model | Firmware |
|------------|------------|-------|----------|
| `173.242.239.157` | HMC-01 | JCI M4-SNC25152-0 (Site Network Controller) | 10.1.7.196 |
| `173.242.239.158` | HMC-02 | JCI MS-NAE4510-2 (Network Automation Engine) | 9.0.7.7978 |

These devices appear to manage the building automation system for your operations facility. The BACnet protocol used by these controllers has no authentication by design — any computer on the internet that speaks BACnet can read sensor values and write to control outputs (temperature setpoints, fan enables, damper positions, equipment schedules) for your facility without credentials.

**Why this is especially concerning for an electric utility:**

Your organization operates both JCI Metasys building automation and Survalent SCADA for electric distribution — both running on AS26809, your own fiber network. NERC CIP standards (CIP-005 Electronic Security Perimeters) require isolation of bulk electric system cyber assets from internet-accessible paths. If your building automation network and your Survalent SCADA distribution network share any network infrastructure — which is possible on a converged utility fiber network — internet-accessible building automation controllers represent a potential lateral movement path toward your distribution SCADA.

Even if the networks are fully segmented, internet-facing building automation at a utility operations center is a security risk and likely warrants review under your CIP compliance program.

HMC-02 (firmware 9.0.7.7978) also falls below the 9.0.8 patch threshold for **CVE-2021-27660** (Metasys web server path traversal, CVSS 7.5 High), which allows unauthenticated reading of controller configuration files if the Metasys web interface is also internet-accessible.

**I have not accessed, tested, or interacted with your systems.** All data is from Shodan's passive public index.

**Recommended immediate actions:**

1. Block inbound UDP 47808 to `173.242.239.157` and `173.242.239.158` at your perimeter firewall immediately
2. Verify network segmentation between Metasys BAS network and Survalent SCADA distribution network
3. Upgrade HMC-02 firmware to 9.0.8 or later to patch CVE-2021-27660
4. Contact your JCI Metasys integrator to audit both controllers for any unauthorized configuration changes
5. Review your CIP-005 Electronic Security Perimeter documentation for these assets

Given your role as a TVA member utility, I would also recommend notifying TVA's cybersecurity team as a precaution.

Respectfully,  
Cameron Warren  
cwarre33@charlotte.edu

---

## LETTER 5 — Metro North Fire Protection District (Chambers Firehouse)

**To:** Chief Dave Volz, Metro North Fire Protection District  
**Contact:** +1-314-867-5360  
**Address:** 1815 Chambers Rd, St. Louis, MO 63136  
**Secondary:** St. Louis County IT/Network or Fire District IT support  
**Escalation:** CISA ICS-CERT within **30 days**

---

Subject: Security Disclosure — Internet-Exposed Building Automation System at 1815 Chambers Road Fire Station

Dear Chief Volz,

I am an independent security researcher. Using publicly indexed data from Shodan (a passive internet scanning service), I have identified a building automation controller at your fire station that is accessible from the public internet.

**What was found:**

A Reliable Controls building automation controller (device name `Chambers Firehouse`) at IP address `24.240.179.78` is internet-accessible on UDP port 47808. This device manages your fire station's building automation system, including HVAC for the apparatus bay and station facilities.

The BACnet building automation protocol has no authentication by design — any computer that reaches this device can read all building sensor values and write to all HVAC control outputs without a password or login of any kind. This includes control of apparatus bay temperature and ventilation systems.

**Why this matters for emergency response readiness:**

Your apparatus bay heating system is critical to maintaining your fleet's operational readiness. In winter conditions (St. Louis January average lows: 22°F), if apparatus bay temperatures drop due to HVAC control being disabled or setpoints being forced to minimum, diesel engine blocks can cold-soak to the point where reliable cold starting is impaired. This can delay response to emergency calls for the duration of the failure — which could span hours depending on how the fault is diagnosed.

Similarly, your exhaust capture systems (if BACnet-controlled) protect your personnel from diesel fume exposure. Disabling these systems creates an OSHA 1910.1000 exposure concern.

**This device is connected through Charter Communications residential broadband** — a consumer-grade internet connection with no indication of firewall protection on UDP port 47808. This is likely an unintended internet exposure.

**I have not accessed, tested, or interacted with your systems.** All data is from Shodan's passive public index.

**Recommended immediate actions:**

1. Contact your internet service provider (Charter/Spectrum) and ask them to block inbound UDP port 47808 on your connection, or connect a firewall/router that blocks this port
2. Contact your building automation service contractor and ask them whether this device needs internet connectivity — if not, disconnect it from the internet-facing network entirely
3. If remote access is needed for service, ask your contractor to configure VPN-based access instead of direct internet exposure

This fix requires no equipment purchase — simply blocking the port at your router or requesting it from Charter is sufficient. I am happy to explain the technical steps to whoever manages your building systems.

Respectfully,  
Cameron Warren  
cwarre33@charlotte.edu

---

## LETTER 6 — City of Liberty MO (Woodbourne Water Tank)

**To:** City of Liberty Utilities Department  
**Contact:** +1-816-439-4460  
**Address:** 101 E Kansas St, Liberty, MO 64068  
**Website:** libertymissouri.gov  
**Secondary:** Missouri Public Service Commission (if City of Liberty routes through Liberty Utilities LLC)  
**Escalation:** CISA ICS-CERT + EPA WaterISAC within **14 days** (water infrastructure critical infrastructure)

---

Subject: Security Disclosure — Internet-Exposed Water Distribution Tank Controller, Liberty Missouri

Dear City of Liberty Utilities Director,

I am an independent security researcher. Using only publicly indexed data from Shodan, I have identified what appears to be a water distribution system control device that is accessible from the public internet without any authentication.

**What was found:**

A Delta Controls building/site controller (device name `1700 WOODBOURNE TANK`) at IP address `24.103.25.90` is accessible from the public internet on UDP port 47808. The device type (Delta Controls DSC_633E) is specifically designed for remote unmanned infrastructure sites including water storage tanks, pump stations, and similar distribution system equipment.

The BACnet protocol used by this controller has no authentication requirement — any computer on the internet can read all sensor values and write to all control outputs. For a water storage tank, those outputs typically include the fill valve and transfer pump.

**What unauthorized access means for water distribution:**

Unauthenticated write access to a water tank controller allows: forcing the fill valve closed (tank drains; downstream pressure drops; fire hydrant flow is reduced when the zone needs it most), or forcing the fill valve fully open at the wrong time (tank overflow; pump damage). Alarm thresholds can also be modified so operators receive no notification of abnormal conditions.

**More concerning:** The controller's configuration shows it is peered with a second internet-facing device at `24.39.116.210` — both on Charter Communications broadband addresses. This suggests at least two water system nodes are connected to the public internet over consumer broadband with no authentication, forming a small distribution network operating without any VPN or access control.

**I have not accessed, tested, or interacted with your systems.** All data is from Shodan's passive public index.

**Recommended immediate actions:**

1. Block inbound UDP 47808 at the network connection for `24.103.25.90` immediately — this is the highest priority action
2. Identify and investigate `24.39.116.210` — this appears to be a peer device in the same water distribution network and may have the same exposure
3. Contact your SCADA/automation integrator about replacing consumer broadband + direct internet exposure with a cellular private network (AT&T FirstNet, Verizon Private) or VPN-based architecture
4. Report this to your state drinking water program contact (Missouri DNR) for awareness

Given this involves water infrastructure, I will be notifying CISA's ICS-CERT (report@cisa.gov) and the WaterISAC simultaneously with this letter, per standard responsible disclosure practice for water sector critical infrastructure.

Respectfully,  
Cameron Warren  
cwarre33@charlotte.edu

---

## LETTER 7 — KIPP Inspired Academy (KIPP St. Louis)

**To:** KIPP St. Louis School Leadership  
**Contact:** +1-314-296-3502 (KIPP Inspire Academy)  
**Address:** 1212 N. 22nd Street, St. Louis, MO 63106  
**Also contact:** kippstl.org contact form; e-rate@kippstl.org (from ARIN records, may be active)  
**Escalation:** CISA ICS-CERT within **30 days**

---

Subject: Security Disclosure — Internet-Exposed HVAC Control System Covering All KIPP St. Louis School Campuses

Dear KIPP St. Louis Leadership,

I am an independent security researcher. Using only publicly indexed data from Shodan (a passive internet scanning service), I have identified a building automation controller that is accessible from the public internet and appears to manage HVAC systems across all of your school campuses.

**What was found:**

A Delta Controls building automation system controller (device name `Mitchell`) at IP address `12.5.26.10` — on a network registered in ARIN's database to "KIPP INSPIRED ACADEMY" — is accessible from the public internet on UDP port 47808.

What is particularly significant about this device is its network configuration: it acts as a central gateway (BBMD — BACnet Broadcast Management Device) that bridges the public internet to **13 separate internal school building networks**, spanning subnets `10.2.x`, `10.43.x`, `10.50.x`, `10.51.x`, `10.68.x`, `10.72.x`, `10.107.x`, `10.116.x`, `10.132.x`, `10.136.x`, `10.144.x`, `10.171.x`, and `10.10.70.x`.

Each of these subnets has at least one HVAC controller. Through this single internet-facing gateway, all of them are simultaneously reachable from the public internet without any authentication.

**What BACnet unauthenticated access means in a school:**

The BACnet protocol used by these controllers has no login or password requirement by design. Any computer that reaches this device can read all HVAC sensor values and write to all control outputs across all 13 campus zones. This includes classroom ventilation (CO₂ levels and fresh air supply are ASHRAE 62.1 regulated), gymnasium and auditorium air handling for assemblies, building heating and cooling schedules, and boiler enable states.

In winter, disabling heating across all campuses simultaneously could force school closures for 2,700+ students and staff. Disrupting CO₂ ventilation in occupied classrooms creates a measurable impact on student health and cognitive performance well below NIOSH complaint thresholds.

**Additional concern:** Your network's IP registration with ARIN has not been validated since **October 2016** — nearly 10 years. This strongly suggests your network infrastructure team may not be aware of this exposure, as it appears to predate current IT management.

**I have not accessed, tested, or interacted with your systems.** All data is from Shodan's passive public index.

**Recommended immediate actions:**

1. Contact your internet service provider and request that UDP port 47808 be blocked inbound at your internet connection for IP `12.5.26.10`
2. Contact your building automation service contractor to assess whether this device needs internet connectivity — if not, disconnect it from the internet-facing network
3. Ask your contractor to audit all 13 campus HVAC zones accessible through this gateway for any unexpected configuration changes
4. If remote HVAC management is needed for service, ask your contractor to switch to VPN-based access

I am happy to provide technical details to your IT team or building automation contractor. Student safety and building readiness for the coming school year should be the priority here.

Respectfully,  
Cameron Warren  
cwarre33@charlotte.edu

---

## Disclosure tracking

| Target | Letter | Priority | Sent | Response | Escalation deadline |
|--------|--------|----------|------|----------|-------------------|
| Lahey Health System | Letter 1 | 🔴 CRITICAL | ☐ | — | 14 days → CISA |
| City of Cartersville | Letter 2 | 🔴 CRITICAL | ☐ | — | 30 days → CISA |
| Chicago Boiler / RCN + AWS | Letter 3 | 🔴 CRITICAL | ☐ | — | 30 days → CISA |
| Scottsboro Electric | Letter 4 | 🔴 CRITICAL | ☐ | — | 14 days → CISA |
| Metro North Fire | Letter 5 | 🟡 HIGH | ☐ | — | 30 days → CISA |
| City of Liberty (Water Tank) | Letter 6 | 🔴 CRITICAL | ☐ | — | 14 days → CISA + WaterISAC |
| KIPP St. Louis | Letter 7 | 🟡 HIGH | ☐ | — | 30 days → CISA |
| WalkerMedical (Cozad Group) | See [[walkermedical-disclosure-2026-04-19]] | 🔴 CRITICAL | ☐ | — | 30 days → CISA |
