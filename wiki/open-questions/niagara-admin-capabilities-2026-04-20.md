---
title: Niagara Admin Access — What CVE-2017-16748 Actually Gives (Lahey Medical)
type: open-question
status: active
visibility: public
sources: [raw/osint/2026-04-19-scan-enriched.json]
related: [wiki/open-questions/exploitability-assessment-2026-04-20.md, wiki/open-questions/ics-exposure-2026-04-19.md]
created: 2026-04-20
updated: 2026-04-20
confidence: high
tags: [tridium, niagara, cve-2017-16748, healthcare, ics, admin-access, building-automation, lahey-medical]
---

# Niagara Admin Access — What CVE-2017-16748 Actually Gives (Lahey Medical)

## The Vulnerability

**CVE-2017-16748** — Tridium Niagara 4 Improper Authentication  
CVSS v3: **9.8 Critical** (`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`)  
CWE-287: Improper Authentication

> "An attacker can log into the local Niagara platform using a disabled account name and a blank password, granting the attacker administrator access to the Niagara system."

**Affected:** Niagara 4 Framework versions **4.4 and prior**. Patched in **4.4 Update 1 (4.4.92.2.1)**.

**Lahey Medical Market Street** (`166.148.23.176`) runs **Tridium 4.4.73.24** — below the 4.4.92.2.1 patch threshold. **Confirmed vulnerable.**

The attack: send an HTTP login request to the Niagara web interface using a known disabled account name (common defaults: `guestoperator`, `guest`, `operator-old`, `disabled`) with an empty password string. The authentication logic fails to reject disabled accounts before checking credentials, granting full admin session.

---

## What Niagara Admin Access Actually Controls

Niagara 4 is not just a BACnet gateway. It is a **full building automation supervisory platform** — the authoritative control layer above all field devices. Admin access is qualitatively different from unauthenticated BACnet WriteProperty. Here is exactly what it enables:

### 1. Wire Sheet — The Control Logic Layer

> "The wiresheet and web wiresheet require Admin permissions level of a given component."

The **Wire Sheet** is Niagara's visual programming environment — it is where the actual automation logic lives. Control loops, PID algorithms, setpoint schedules, alarm conditions, interlocks, and failsafe sequences are all implemented as wire sheet programs.

**What admin can do in Wire Sheet:**
- **Modify PID control parameters** — change the gain, integral, and derivative settings of any control loop. A subtle change to pressurization control PID (e.g., reversing sign on error calculation) can invert a room's pressure differential while appearing to work normally on the operator display.
- **Break control interlocks** — remove the wire connections between safety interlock logic and the actuator outputs. For example: disconnect the high-temperature alarm from the cooling enable output, so the system never responds to overtemperature.
- **Add hidden logic branches** — insert new wire sheet components that run in background: a timed schedule that overrides setpoints at 3 AM, a component that suppresses alarms during specific time windows, a setpoint bias that causes actual conditions to differ from displayed values.
- **Change output limits** — every Analog Output has High/Low limit properties that constrain how far WriteProperty can push a value. Admin can widen these limits to allow extreme setpoints that the default BACnet-only path would reject.

### 2. config.bog — The Credential Vault

The Niagara **station database** (`config.bog`) contains:
- All local user credentials (username + password hash for all Niagara accounts)
- Network configuration (IP bindings, port assignments)
- **All downstream controller connection credentials** — if this Niagara station connects to downstream JACE controllers, other Niagara supervisors, or third-party systems (DALI lighting, access control, fire alarm gateways), those connection credentials are stored in config.bog
- BACnet network configuration and device bindings
- Historical trend data references

Admin can **download config.bog** via the Niagara file browser. Once in hand, the attacker has every password for every system this controller touches — not just the current building, but any other buildings connected through the same Niagara supervisor hierarchy.

**A known companion vulnerability:** CVE-2012-4701 (Tridium Niagara AX directory traversal, CVSS 9.3) allowed unauthenticated download of config.bog via HTTP path traversal. The combination of CVE-2017-16748 (auth bypass to get admin) + config.bog download gives the full credential picture without needing directory traversal.

### 3. File System Write — Module Installation and Persistence

> "By default only admin users are permitted to write to your file system."

Admin can **install new Niagara modules** (JAR files). Niagara's extensible component model allows third-party modules to add arbitrary functionality. A malicious module can:
- Add a new user account that persists across password changes
- Implement a covert communication channel (phone-home beacon)
- Log all operator actions and exfiltrate them
- Create a hidden override that activates on schedule

Module installation survives controller reboots and firmware updates if installed into the station's persistent module directory.

### 4. User Account Control — Persistence via Legitimate Credentials

Admin can:
- Create new admin-level accounts with attacker-controlled passwords
- Modify or disable existing operator accounts (lock out legitimate users)
- Change the passwords of all existing users

**This is the persistent access path.** Rather than relying on CVE-2017-16748 repeatedly (which may be patched), the attacker creates a new admin account with a normal-looking name on first access, then uses that account for all future sessions — undetectable unless administrators audit the user list.

### 5. Downstream Controller Access — The Full Building Network

Niagara supervisors aggregate dozens to hundreds of field controllers. From Niagara admin:
- Every BACnet device in the station's device database is accessible at the programming level — not just WriteProperty to current values, but modification of all properties including high/low limits, out-of-service flags, and alarm parameters
- JACE (Java Application Control Engine) field controllers connected via N4 links can be fully reprogrammed
- Third-party protocol adapters (LonWorks, Modbus, KNX, DALI, RS-485) connected through the supervisor are accessible as BACnet proxies — admin access propagates through to all of them

### 6. Px Page Modification — Hiding Attacks from Operators

Niagara serves graphical operator interface pages (Px pages) to building operators through a web browser. Admin can:
- **Modify Px pages to show false values** while actual physical values differ — an operator monitoring temperature on a screen sees 72°F while the actual zone is at 95°F because the display binding was changed to show a different point
- Remove alarms from operator view
- Change color coding (e.g., make "fault" show as "normal" green)

This is a **deception layer** — it allows an attacker to make physically unsafe conditions look normal to the humans monitoring the system.

---

## Specifically at Lahey Medical — Healthcare Impact

Lahey Hospital & Medical Center's building automation at `LaheyMedical_MarketStreet_1000` controls:

**Room pressure differentials (critical):**
- **Surgery suites/procedure rooms:** Positive pressure (+0.03" WC minimum, ASHRAE 170) — prevents contaminated corridor air from entering sterile space. An attacker modifying pressure control logic to negative or zero could increase surgical site infection risk.
- **Isolation rooms (airborne infection):** Negative pressure (-0.03" WC minimum) — prevents infectious aerosols from leaving isolation room. Reversing or disabling this control is an **infection control failure** that can expose other patients and staff to airborne pathogens (TB, measles, COVID, etc.)
- **Pharmacy compounding areas:** Positive pressure — sterile drug compounding requires controlled air quality.

**Temperature and humidity:**
- Medication storage (per USP 797/800): strict temperature bands for IV medications, biologics, chemotherapy agents. Wire sheet modification to disable temperature alarms or widen setpoint limits can cause drug degradation — which is not immediately visible.
- Surgical supply sterile storage.

**The unique danger of wire sheet modification vs. BACnet WriteProperty:**
- A BACnet WriteProperty attack changes a current value — it is immediately visible to any technician monitoring the point, and the control system may override it on the next control cycle.
- A **wire sheet modification** changes the logic — it persists, it survives override attempts, and it can be designed to look correct in all normal monitoring tools while producing dangerous physical conditions.

An attacker with Niagara admin at Lahey Medical Market Street can modify the pressure differential control PID for isolation rooms so that they maintain slightly positive rather than slightly negative pressure — infectious patients no longer contained — without this being visible on any standard operator screen unless someone specifically inspects the wire sheet configuration.

---

## Attack Sequence (CVE-2017-16748 on 166.148.23.176)

1. Connect to Niagara web UI — the controller is internet-facing on BACnet/UDP port 47808; if port 443 or 8443 is also open (standard Niagara web server), the UI is directly accessible
2. Submit login request with a disabled account name + blank password via HTTP POST
3. Receive admin session token
4. Access Wire Sheet browser → modify any control loop
5. Access User Manager → create new persistent admin account
6. Access File Browser → download config.bog (contains all system credentials)
7. Access Module Manager → install persistent module for long-term access
8. Modify Px display pages → conceal changes from operators

Steps 1–4 require no special tools beyond a web browser.

---

## Why This Is Worse Than Protocol-Level BACnet Access

| Attack type | Persistence | Detectability | Scope |
|-------------|-------------|---------------|-------|
| BACnet WriteProperty | None (resets on next scan cycle) | Immediate (point monitoring) | Single object |
| Niagara admin (CVE-2017-16748) | Permanent (wire sheet + new accounts) | Very low (requires wire sheet audit) | All objects + all logic + all downstream devices + full credential extraction |

BACnet WriteProperty is a one-time physical disruption. Niagara admin access is **persistent, stealthy, full-system compromise** — closer to an APT foothold than a denial-of-service.

---

## Disclosure contacts

**Lahey Health System (Burlington, MA)**  
- Lahey Hospital & Medical Center: +1-781-744-5100  
- Privacy/Security reporting: compliance@lahey.org (general)  
- The Market Street outpatient facility is managed under Lahey Health System

**Tridium (vendor)**  
- security@tridium.com  
- Reference: CVE-2017-16748, CISA ICSA-17-094-02 (or equivalent Tridium security bulletin)

**CISA ICS-CERT escalation:** report@cisa.gov (healthcare critical infrastructure; escalate if no Lahey response in 14 days — healthcare sector warrants shorter window)
