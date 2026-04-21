---
title: ICS Exposure Findings — 2026-04-19
type: open-question
status: active
visibility: public
sources: [raw/osint/2026-04-19-scan-enriched.json]
related: [wiki/techniques/shodan-ics-osint.md]
created: 2026-04-19
updated: 2026-04-19
confidence: high
tags: [shodan, ics, osint, exposure, 2026-04-19]
---

# ICS Exposure Findings — 2026-04-19

Scan run via [[shodan-ics-osint]] pipeline. 3000 unique hosts across 4 protocols.

## Protocol exposure

| Protocol | Exposed hosts (sampled) | Total in Shodan index |
|----------|------------------------|-----------------------|
| modbus | 1000 | 443205 |
| bacnet | 1000 | 43629 |
| dnp3 | 1000 | 1067695 |
| s7 | 0 | 0 |


## Top countries by exposure

| Rank | Country | Hosts |
|------|---------|-------|
| 1 | US | 1189 |
| 2 | CN | 551 |
| 3 | SG | 279 |
| 4 | GB | 164 |
| 5 | IL | 121 |
| 6 | CA | 107 |
| 7 | JP | 63 |
| 8 | DE | 56 |
| 9 | NL | 46 |
| 10 | HK | 37 |


## CVE patterns


| CVE | Occurrences |
|-----|-------------|
| CVE-2008-3844 | 27 |
| CVE-2016-20012 | 27 |
| CVE-2026-35414 | 27 |
| CVE-2021-36368 | 27 |
| CVE-2023-51767 | 27 |
| CVE-2023-48795 | 27 |
| CVE-2023-38408 | 27 |
| CVE-2007-2768 | 27 |
| CVE-2023-51385 | 27 |
| CVE-2020-15778 | 26 |



## Open questions

- Which ASNs concentrate the most exposed ICS endpoints?
- Are exposed Modbus/DNP3 hosts clustered in specific utility operators?
- How does exposure change week-over-week? ⚠️ (requires longitudinal tracking)

## Next steps

- Re-run with `--limit 5000` for a larger sample
- Cross-reference ASN owners with known utility operators
- Correlate CVE counts with exploit availability in NVD