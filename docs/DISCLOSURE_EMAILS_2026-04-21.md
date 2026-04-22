# Responsible Disclosure Emails — Ready to Send

Generated: 2026-04-21
Scan data: `raw/osint/2026-04-21-longitudinal-full.json`

---

## 1. Homanit Lietuva (Lithuania) — PRIORITY #1

**Why first:** ATEX-regulated combustible-dust facility + active 17-day DigitalOcean tunnels = highest safety stakes.

**Contacts:**
- **Primary:** info@homanitlietuva.lt (plant)
- **Secondary:** info@homanit.org (German parent)
- **Vendor:** psirt@wago.com (WAGO controller PSIRT)
- **National:** nksc.lt (Lithuanian CERT-LT)

**Send to:** info@homanitlietuva.lt, info@homanit.org
**CC (after 7 days if no response):** nksc.lt, psirt@wago.com

---

### Email: Homanit Lietuva

**To:** info@homanitlietuva.lt, info@homanit.org
**Subject:** URGENT — Active External BACnet Tunnels Detected at Homanit Lietuva (Pagiriai Plant)

```
Dear Homanit Lietuva Facilities and IT Security Teams,

I am a security researcher conducting passive OSINT analysis of internet-exposed 
industrial control systems. Using only data already indexed by Shodan (no active 
scanning, no probing, no interaction with any systems), I identified an exposure 
at your Pagiriai plant that requires immediate attention.

WHAT WAS FOUND:
───────────────
A WAGO BACnet controller (device name "Homanit.VAS_LNS_1") at IP 85.206.88.54 
is reachable from the public internet on UDP port 47808 with no authentication.

MORE CRITICALLY:
Shodan's historical index shows TWO external public IPs on DigitalOcean cloud 
infrastructure have maintained persistent BACnet Foreign Device Table registrations 
to your controller continuously since 2026-04-04 — 17+ days across 130 distinct 
Shodan observations:

  • 157.245.127.71 (DigitalOcean NYC) — static port, 130 scans
  • 104.131.63.228 (DigitalOcean NYC) — rotating ports, 130 scans

These are not stale entries. They represent active software maintaining persistent 
BACnet access to your plant's building automation network.

Whether these are:
  (a) a third-party service contracted by your facilities team,
  (b) your integrator's remote-management setup, or
  (c) unauthorized access

is something only your team can determine. Any of those answers requires 
immediate change. Cases (a) and (b) still represent an architecturally 
unacceptable remote-access path for an ATEX-regulated facility; case (c) is 
an active incident.

WHY THIS MATTERS FOR AN MDF/HDF FACILITY:
─────────────────────────────────────────
Wood-fiberboard manufacturing is a combustible-dust environment governed by 
ATEX 2014/34/EU and 1999/92/EC. Building-automation control over dust-collection 
fans, process-exhaust dampers, make-up air, fire-damper schedules, and ventilation 
setpoints is directly safety-relevant. Loss of integrity in these systems crosses 
out of "comfort" into the explosion-hazard regime.

RECOMMENDED IMMEDIATE ACTIONS:
──────────────────────────────
1. Block UDP port 47808 inbound at your perimeter firewall immediately
   (this removes the exposure in one step)

2. Identify 157.245.127.71 and 104.131.63.228 — are these contracted services, 
   integrator infrastructure, or unknown?

3. If unknown, treat as active intrusion — preserve BBMD state (FDT snapshot, 
   access logs) before remediation

4. Confirm which BACnet objects/controllers are reachable behind Homanit.VAS_LNS_1, 
   and whether dust-collection, process-exhaust, or fire-safety actuators are 
   integrated to this BAS network

5. Contact WAGO PSIRT (psirt@wago.com) for firmware version cross-reference 
   against applicable advisories

6. Replace any legitimate remote BACnet access with VPN-gated private BBMD

TIMELINE:
─────────
I am disclosing this in good faith and have not shared these findings with any 
third party. I request:
  • Acknowledgment within 7 days (by 2026-04-28)
  • Confirmation of remediation timeline within 14 days

If I do not receive a response within 7 days, I will notify:
  • Lithuanian National Cyber Security Centre (NKSC / CERT-LT)
  • WAGO Kontakttechnik PSIRT
  • CISA ICS-CERT (for vendor coordination)

I have no intention of accessing, testing, or interacting with your systems. 
I am available to provide full technical detail to your IT, OT, or facilities 
team — including the specific DigitalOcean IPs and scan history — and to 
coordinate with NKSC and WAGO if you prefer that route.

Respectfully,
Cameron Warren
Security Researcher
[your contact info]
```

---

## 2. Alaska Integrated Services (Integrator) — PRIORITY #2

**Why second:** Shared endpoint = 2 buildings fixed with one email. Attribution is "medium-high confidence" (not confirmed), so framing is softer.

**Contacts:**
- **Primary:** general@akintegrated.com (Alaska Integrated Services)
- **Secondary:** rodger.morrow@akintegrated.com (President, per public records)
- **Building A:** info@cozadgroup.com (12350 Industry Way property manager)
- **Building B:** security@lumen.com (CenturyLink/Lumen PSIRT — 6411 A Street tenant)
- **IP provider:** abuse@acsalaska.net (Alaska Communications)

**Send to:** general@akintegrated.com
**CC:** (hold — only loop in buildings if AIS confirms they operate the endpoint)

---

### Email: Alaska Integrated Services

**To:** general@akintegrated.com
**Subject:** Responsible Disclosure — Internet-Reachable BACnet Monitoring Endpoint (216.67.73.166)

```
Dear Alaska Integrated Services Security Team,

I am a security researcher conducting passive OSINT analysis of internet-exposed 
building automation systems. Using only data already indexed by Shodan (no active 
scanning, no probing, no interaction with any systems), I identified a pattern 
that points to your infrastructure.

WHAT WAS OBSERVED:
──────────────────
Two internet-facing Delta Controls BBMDs in Anchorage both have 216.67.73.166 
as a persistent Foreign Device Table entry:

  • 24.237.132.230 — "Huffman Plaza 12350 Industry Way", Anchorage AK
  • 66.58.248.125  — "6411 A Street", Anchorage AK (100% leased to CenturyLink/Lumen)

Across Shodan's history, both registrations have been continuous since 2026-03-04 
(47+ days) with rotating source ports consistent with a long-running client process.

216.67.73.166 resolves as 216-67-73-166.static.acsalaska.net — an ACS static 
commercial assignment in Anchorage, which is the profile of an integrator's 
remote-monitoring station.

I am writing to ask:
  1. Is 216.67.73.166 an endpoint you operate (monitoring station, gateway, etc.)?
  2. Is the remote-access architecture into both client buildings intentional?
  3. Is the BACnet Foreign Device registration authenticated or VPN-gated at 
     some layer other than BACnet itself? (BACnet has no authentication.)
  4. Are the two building BBMDs intended to be reachable from the public 
     internet on UDP 47808? (I believe this is unintentional — the current 
     configuration lets any BACnet client on the internet enumerate and write 
     to both buildings.)

RECOMMENDED IMMEDIATE ACTIONS:
──────────────────────────────
1. Block UDP 47808 inbound at the perimeter firewall for both client sites
   (this removes the internet exposure immediately)

2. Move all remote monitoring behind a VPN (site-to-site IPsec or WireGuard) 
   between your monitoring station and each client's BBMD

3. Audit Foreign Device registrations at both client sites and confirm only 
   your managed endpoint(s) are present

4. Provide each client with a brief describing the architectural fix and any 
   evidence of unauthorized BACnet reads or writes in their controller logs

BUILDING STAKEHOLDERS:
──────────────────────
I have not yet contacted the building operators directly. If you confirm this 
is your infrastructure, I recommend you notify:
  • 12350 Industry Way: Cange Group Commercial Real Estate / Paragon Properties
  • 6411 A Street: CenturyLink/Lumen PSIRT (security@lumen.com) — major telecom tenant

TIMELINE:
─────────
I request acknowledgment within 7 days (by 2026-04-28). If I do not hear from 
you, or if you indicate this is not your infrastructure, I will notify:
  • Both building operators directly
  • Alaska Communications Systems (abuse@acsalaska.net)
  • CISA ICS-CERT (for cross-stakeholder coordination, given the CenturyLink tenancy)

I have no intention of accessing, testing, or interacting with any of these 
systems. I am available to provide technical detail to your engineering team 
and to coordinate with CISA and the building tenants if you prefer.

Respectfully,
Cameron Warren
Security Researcher
[your contact info]
```

---

## 3. DigitalOcean Abuse — `104.131.63.228` — PRIORITY #3

**Why third:** One IP bridges 3 buildings across 3 countries. DigitalOcean can identify the customer.

**Contact:**
- **Abuse:** abuse@digitalocean.com
- **Web form:** https://www.digitalocean.com/company/contact/

**Send to:** abuse@digitalocean.com

---

### Email: DigitalOcean Abuse

**To:** abuse@digitalocean.com
**Subject:** Security Disclosure — BACnet ICS Tunneling from Droplet 104.131.63.228

```
Dear DigitalOcean Abuse Team,

I am a security researcher conducting passive OSINT analysis of internet-exposed 
industrial control systems. Using only data already indexed by Shodan (no active 
scanning, no probing, no interaction with any systems), I identified a DigitalOcean 
droplet maintaining persistent connections to building automation systems across 
three countries.

WHAT WAS OBSERVED:
──────────────────
IP 104.131.63.228 (DigitalOcean NYC, 104.131.0.0/16) appears as a registered 
BACnet Foreign Device in the Foreign Device Tables of three internet-facing 
BBMDs (BACnet Broadcast Management Devices):

  • 85.206.88.54  — Lithuania (Homanit Lietuva, MDF/HDF manufacturing plant)
  • 50.79.138.67  — United States
  • 115.241.1.87  — India

Shodan history shows continuous registration since 2026-04-04 (17+ days) with 
130 distinct observations per BBMD. One BBMD (Homanit) shows rotating source 
ports across 14 distinct ephemeral ports, consistent with active software 
re-registering on every connection.

BACnet/IP is an industrial control protocol used for building automation (HVAC, 
lighting, access control, fire safety). A Foreign Device registration means the 
droplet is receiving BACnet broadcasts from and potentially issuing writes to 
the internal building networks of all three facilities.

This architecture — a cloud VPS bridging directly into industrial control networks 
over the public internet with no authentication — is a significant safety concern, 
particularly for the Lithuania facility which is an ATEX-regulated combustible-dust 
environment.

REQUEST:
────────
I request that DigitalOcean:
  1. Identify the customer/account operating 104.131.63.228
  2. Determine whether this is:
     (a) A legitimate building-management SaaS or integrator monitoring platform
     (b) A compromised droplet being used for unauthorized ICS access
  3. If (a): Ensure the customer is aware their architecture exposes three 
     buildings to unauthenticated internet access, and recommend immediate 
     migration to VPN-gated private BACnet
  4. If (b) or unknown: Treat as a compromised droplet and follow your 
     incident-response procedures

I have not yet contacted the building operators at any of the three facilities. 
I am disclosing this in good faith and am available to provide full technical 
detail (including specific BBMD IPs, scan timestamps, and FDT entry data) to 
your security team.

Respectfully,
Cameron Warren
Security Researcher
[your contact info]
```

---

## 4. AWS Tunnel Cases — PRIORITY #4

Two AWS-hosted external FDT tunnels discovered:
- `35.182.50.76` → AWS ca-central-1 (Canada), 110 scans
- `54.234.107.205` → AWS us-east-1 (Virginia), 8 scans

**Contact:**
- **AWS Security:** aws-security@amazon.com
- **Abuse:** abuse@amazonaws.com

---

### Email: AWS Security

**To:** aws-security@amazon.com, abuse@amazonaws.com
**Subject:** Security Disclosure — BACnet ICS Tunneling from AWS IPs (ca-central-1, us-east-1)

```
Dear AWS Security Team,

I am a security researcher conducting passive OSINT analysis of internet-exposed 
industrial control systems. Using only data already indexed by Shodan (no active 
scanning, no probing, no interaction with any systems), I identified two AWS IPs 
maintaining persistent BACnet Foreign Device registrations with building automation 
systems.

WHAT WAS OBSERVED:
──────────────────
IP 35.182.50.76 (AWS ca-central-1, Canada):
  • Registered as BACnet Foreign Device with BBMD at 184.69.115.182 (Canada)
  • 110 Shodan observations, 2026-03-04 through 2026-04-21
  • 8 rotating source ports (active software)

IP 54.234.107.205 (AWS us-east-1, Virginia):
  • Registered as BACnet Foreign Device with BBMD at 216.80.86.155 (US)
  • 8 Shodan observations, 2026-03-17 through 2026-04-19
  • 2 rotating source ports

BACnet/IP is an industrial control protocol used for building automation (HVAC, 
lighting, access control, fire safety). A Foreign Device registration means the 
EC2 instance is receiving BACnet broadcasts from and potentially issuing writes 
to the internal building networks.

REQUEST:
────────
I request that AWS:
  1. Identify the customer/account(s) operating these IPs
  2. Determine whether this is:
     (a) A legitimate building-management SaaS or integrator monitoring platform
     (b) A compromised instance being used for unauthorized ICS access
  3. If (a): Ensure the customer is aware their architecture exposes buildings 
     to unauthenticated internet access, and recommend immediate migration to 
     VPN-gated private BACnet
  4. If (b) or unknown: Treat as compromised instances

I am disclosing this in good faith and am available to provide full technical 
detail to your security team.

Respectfully,
Cameron Warren
Security Researcher
[your contact info]
```

---

## Sending Checklist

| Target | Email sent? | Date sent | Ack deadline | Response? | Remediation confirmed? |
|--------|-------------|-----------|--------------|-----------|------------------------|
| Homanit Lietuva | ☐ | ___ | 2026-04-28 | ☐ | ☐ |
| Alaska Integrated | ☐ | ___ | 2026-04-28 | ☐ | ☐ |
| DigitalOcean abuse | ☐ | ___ | 2026-04-28 | ☐ | ☐ |
| AWS Security | ☐ | ___ | 2026-04-28 | ☐ | ☐ |

**Escalation dates (if no acknowledgment):**
- 2026-04-28: CC national CERTs (NKSC, CISA) and vendors (WAGO)
- 2026-05-05: Public disclosure (GitHub, Twitter, ICS mailing lists)

---

## Notes

- All emails use a **7-day acknowledgment window** (shorter than the standard 30 days) due to active-tunnel evidence and safety-critical contexts (ATEX, telecom).
- Framing is **collaborative, not accusatory** — "we don't know what this is, only you can tell us" — which reduces defensiveness.
- Each email explicitly states **no active probing occurred** — important for legal safe harbor.
- Escalation path is clear but not threatening — "if no response, we notify X" gives recipients agency.
