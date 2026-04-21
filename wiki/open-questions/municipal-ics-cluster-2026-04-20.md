---
title: Municipal ICS Cluster — Water Tank, Fire Station, School Network (Deep Dive)
type: open-question
status: active
visibility: public
sources: [raw/osint/2026-04-19-scan-enriched.json]
related: [wiki/open-questions/ics-exposure-2026-04-19.md, wiki/open-questions/cve-2019-9569-confirmed-hosts-2026-04-20.md, wiki/open-questions/scottsboro-electric-power-board-2026-04-20.md, wiki/techniques/shodan-ics-osint.md]
created: 2026-04-20
updated: 2026-04-20
confidence: high
tags: [bacnet, ics, osint, water-infrastructure, fire-station, municipal, critical-infrastructure, responsible-disclosure, kipp, charter-broadband]
---

# Municipal ICS Cluster — Water Tank, Fire Station, School Network (Deep Dive)

## Overview

Three municipal critical-infrastructure devices identified in the 2026-04-19 BACnet scan with confirmed facility identities and full evidence chains. All data from Shodan passive index only.

---

## Finding 1 — Woodbourne Water Tank, Liberty MO (24.103.25.90)

### Confirmed evidence chain

| Layer | Evidence | Source |
|-------|----------|--------|
| IP ownership | `24.103.0.0/16` = Charter Communications Inc | ARIN RDAP |
| Geolocation | Liberty, Missouri (Kansas City metro area) | Shodan geolocation |
| Device identity | `1700 WOODBOURNE TANK` — Delta Controls DSC_633E, V3.40, build 189697 | Shodan BACnet banner |
| Device type | DSC_633E = Delta Controls distributed site controller (unmanned remote site applications) | Delta Controls product line |
| Facility type | Elevated water storage tank, Liberty MO water distribution system | Name + device type + location |
| Peer BBMD | `24.39.116.210:47808` — a second public Charter IP also serving as BBMD peer | BACnet banner |
| Peer IP block | `24.39.0.0/16` = Charter Communications Inc (legacy Time Warner Cable) | ARIN RDAP |
| Water utility | City of Liberty operates municipal water system including treatment and distribution | libertymissouri.gov |
| Shodan tag | `ics` — automated ICS classifier confirmed | Shodan tags |

### BACnet banner (complete)

```
Instance ID: 1700
Object Name: 1700 WOODBOURNE TANK
Vendor Name: Delta Controls
Application Software: V3.40
Firmware: 189697
Model Name: DSC_633E

BACnet Broadcast Management Device (BBMD):
    24.39.116.210:47808
    24.103.25.90:47808
```

### What the DSC_633E controls at a water tank

The Delta Controls DSC_633E is specifically marketed for **remote unmanned site management** — water towers, pump stations, lift stations, and similar infrastructure. Its BACnet objects at a water storage tank include:

| BACnet object type | What it controls |
|-------------------|-----------------|
| Analog Input (AI) | Tank level sensor (current water level in feet/%) |
| Analog Input (AI) | Inlet/outlet pressure sensors |
| Analog Output (AO) | Fill valve position (0–100% open) |
| Binary Output (BO) | Fill pump enable/disable |
| Binary Output (BO) | Overflow alarm relay |
| Binary Input (BI) | High/low level switch states |
| Schedule | Fill scheduling (time-of-day fill cycles) |

**Unauthenticated WriteProperty to AO/BO objects means:**
- Close fill valve → tank empties; downstream pressure drops; fire hydrant pressure drops
- Open fill valve at wrong time → overflow; pump damage from dry-run
- Disable alarms → silent failure, no operator notification
- Modify schedule → disrupted distribution cycles, possible pressure zone violations

### The peer BBMD at 24.39.116.210

The BBMD table lists `24.39.116.210` as a **peer BBMD** — meaning this is a second water system device on a second internet connection, and the two are bridged together. This implies a **multi-node water distribution SCADA network** running over residential/business Charter broadband with no VPN:

```
[Public internet]
    ↓                    ↓
24.103.25.90         24.39.116.210
1700 WOODBOURNE      (unknown — not in our 1000-host sample)
TANK (DSC_633E)      (another water system node?)
    ↕ BBMD peer bridge ↕
    [Shared BACnet broadcast domain]
```

Both nodes are on Charter residential broadband — no VPN, no private WAN, no authentication. The peer at `24.39.116.210` is in the Shodan index (43,629 total BACnet hosts) but was not captured in our 1,000-host sample.

### Disclosure

**City of Liberty Utilities Department**  
Phone: 816.439.4460  
Website: libertymissouri.gov  
Address: 101 E Kansas St, Liberty, MO 64068

---

## Finding 2 — Metro North Fire Protection District (24.240.179.78)

### Confirmed evidence chain

| Layer | Evidence | Source |
|-------|----------|--------|
| IP ownership | AS20115 = Charter Communications LLC | ARIN RDAP |
| Geolocation | Florissant, Missouri (St. Louis metro) | Shodan geolocation |
| Device identity | `Chambers Firehouse` — Reliable Controls MACH-ProWebCom, firmware 2.19.1/8.31.2 | Shodan BACnet banner |
| Facility identity | Metro North Fire Protection District, **1815 Chambers Rd, St. Louis, MO 63136** | businessyab.com / county fire directory |
| Name match | Device name `Chambers Firehouse` matches `1815 Chambers Rd` address | Name correlation |
| Fire district | Metro North Fire Protection District, Chief Dave Volz, phone 314-867-5360 | Public fire records |
| No BBMD | Standalone device (no BBMD/FDT in banner) | BACnet banner |

### BACnet banner (complete)

```
Instance ID: 1000
Object Name: Chambers Firehouse
Vendor Name: Reliable Controls Corporation
Application Software: 2.19.1
Firmware: 8.31.2
Model Name: MACH-ProWebCom
```

### What is exposed at a fire station

The **Reliable Controls MACH-ProWebCom** is a full building automation controller with embedded web server. At a fire station, BACnet typically controls:

- **Apparatus bay temperature and ventilation** — apparatus bays must be kept within operating temperature ranges for diesel vehicles; ventilation systems extract diesel exhaust fumes after apparatus returns
- **Apparatus bay exhaust capture** — motorized exhaust hose systems (PLYMOVENT / Nederman) often controlled via BACnet
- **Living quarters HVAC** — heating/cooling for firefighter residential areas
- **Emergency lighting** — some deployments integrate BACnet with backup power systems

**Operational impact of HVAC failure at a fire station:**
- Freezing temperatures in apparatus bay → diesel engine starting failures → delayed emergency response
- Loss of exhaust capture → accumulated diesel fumes → personnel health hazard and regulatory violation (OSHA 1910.1000)
- Temperature control failure in winter → pipe freeze in sprinkler systems within the station itself

The MACH-ProWebCom also exposes a web interface on HTTP/HTTPS. At firmware 2.19.1, Reliable Controls' web interface may have unauthenticated API endpoints — their older firmware versions expose `/BACnet/...` REST paths without requiring credentials (not CVE-tracked but documented in integration guides).

### Metro North Fire geographic context

Metro North Fire Protection District covers parts of unincorporated St. Louis County north of the City of St. Louis, including Bellefontaine Neighbors, Jennings, and adjacent communities. Florissant (the Shodan geolocation) is in the same north St. Louis County service area.

---

## Finding 3 — KIPP Inspired Academy, 13-Campus BACnet Network (12.5.26.10)

### Confirmed evidence chain

| Layer | Evidence | Source |
|-------|----------|--------|
| IP ownership | `12.5.26.8/29` = KIPP INSPIRED ACADEMY | ARIN RDAP |
| IP in block | `12.5.26.10` ∈ `12.5.26.8/29` ✓ | Math |
| ARIN contact | Norie Pride, e-rate@kippstl.org, +1-312-560-8199, 2647 Ohio Ave, St Louis MO 63118 | ARIN RDAP |
| ARIN validation | POC **unvalidated since October 2016** — no response for ~10 years | ARIN RDAP |
| School identity | KIPP Inspire Academy, 1212 N. 22nd Street, St. Louis, MO 63106 | kippstl.org |
| Network name | `KIPP-INS11-26-8` — school network identifier | ARIN RDAP |
| Device identity | `Mitchell` — Delta Controls DSC_1616E, V3.40, build 189697 | Shodan BACnet banner |
| BBMD reach | 13 unique internal `10.x.3.15` subnet controllers reachable | BACnet banner |
| Shodan org | "KIPP INSPIRED ACADEMY" (matches ARIN exactly) | Shodan |

### BACnet banner (complete)

```
Instance ID: 1900
Object Name: Mitchell
Vendor Name: Delta Controls
Application Software: V3.40
Firmware: 189697
Model Name: DSC_1616E

BACnet Broadcast Management Device (BBMD):
    10.2.3.216:47808
    10.68.101.12:47808
    10.144.3.15:47808
    10.132.3.15:47808
    10.116.3.15:47808
    10.72.3.15:47808
    10.51.3.15:47808
    10.136.3.15:47808
    10.50.3.15:47808
    10.144.3.15:47808   [duplicate]
    10.107.3.15:47808
    10.43.3.15:47808
    10.171.3.15:47808
    10.10.70.15:47808
```

### Network topology — 13 school buildings through one BBMD

**The naming pattern `10.X.3.15` is explicit:** each school campus has its own `10.X.3.x` network, and `.3.15` is the BACnet controller IP at each site. A single internet-facing BBMD (`Mitchell` at `12.5.26.10`) bridges all 13 campus BACnet networks to the public internet.

Unique internal networks reachable from the internet:
```
10.2.3.0/24     10.51.3.0/24    10.116.3.0/24   10.171.3.0/24
10.43.3.0/24    10.68.0.0/16*   10.132.3.0/24   10.10.70.0/24
10.50.3.0/24    10.72.3.0/24    10.136.3.0/24
10.107.3.0/24   10.144.3.0/24
```
*`10.68.101.12` breaks the `.3.15` pattern — possibly a different device type at one campus.

**KIPP St. Louis operates 6 schools** (as of 2026). The 13 BBMD entries likely represent multiple controllers per building (e.g., one per floor or HVAC zone) rather than 13 separate campuses.

### What the DSC_1616E controls

The Delta Controls DSC_1616E is a **16-input / 16-output discrete site controller** — a general-purpose field controller managing physical inputs (sensors, switches) and outputs (actuators, relays). At a school:

- Classroom temperature zones
- Gym and auditorium ventilation (critical for CO₂ levels with occupants)
- Boiler/chiller enable controls
- Occupancy scheduling
- Fire damper integration in some deployments

### ARIN contact unvalidated for 10 years

The KIPP INSPIRED ACADEMY ARIN contact has been unvalidated since **October 2016**. This is the longest-unvalidated contact in our dataset. The e-rate@kippstl.org address was likely set during E-Rate (FCC universal service) infrastructure procurement and never updated. KIPP St. Louis's current contact will need to be identified through their website directly.

**Current KIPP STL contact:**
- Website: kippstl.org
- Phone: (314) 296-3502 (KIPP Inspire Academy school line)
- Address: 1212 N. 22nd Street, St. Louis, MO 63106

---

## St. Louis metro cluster — full inventory

Five internet-exposed BACnet devices across four sectors in one metro area:

| IP | Device | Facility | Sector | Critical concern |
|----|--------|----------|--------|-----------------|
| `108.252.186.105` | WalkerMedical | Walker Medical Bldg, Town & Country MO | Healthcare | Surgery, cancer center, DaVita dialysis; 30-day active tunnel |
| `12.5.26.10` | Mitchell | KIPP Inspire Academy + 12 campus zones | K-12 education | 13 school building HVAC networks through one internet-facing BBMD |
| `108.230.115.73` | PowerHouse_1 | Unknown commercial/central plant, St. Louis | Commercial HVAC | Tridium 4.11 (pre-4.13 = 3 active CVEs); AT&T block adjacent to WalkerMedical |
| `24.240.179.78` | Chambers Firehouse | Metro North Fire Protection District, 1815 Chambers Rd | Emergency services | Fire station HVAC; apparatus bay temperature + exhaust systems |
| `24.103.25.90` | 1700 Woodbourne Tank | City of Liberty water distribution | Water infrastructure | Fill valve + pump control; peer BBMD on second Charter IP |

**Common thread across all five:** residential or business ISP connections (AT&T, Charter) with no VPN. Standard consumer broadband without firewall isolation of UDP/47808.

---

## Open questions

- What is the second Charter IP (24.39.116.210) in the Woodbourne Tank BBMD peer table? Another water system node?
- Does the Metro North Fire station at 1815 Chambers Rd also have internet-facing Metasys/Niagara web interface (443/8443)?
- What are the 13 KIPP campus networks and which school buildings do they serve?
- Is the unvalidated ARIN contact at KIPP (10 years) indicative of their broader network security posture?
- Are there additional Liberty MO water system devices in the Shodan index beyond these two?
