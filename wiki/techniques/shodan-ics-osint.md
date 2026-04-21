---
title: Shodan ICS OSINT — Methodology
type: technique
status: active
visibility: public
sources: [raw/osint/2026-04-19-scan-raw.json]
related: [wiki/open-questions/ics-exposure-2026-04-19.md]
created: 2026-04-19
updated: 2026-04-19
confidence: high
tags: [shodan, ics, osint, modbus, bacnet, dnp3, s7, scada]
---

# Shodan ICS OSINT — Methodology

**Purpose:** Systematically enumerate publicly exposed industrial control system (ICS) endpoints via Shodan's passive index. No active scanning — read-only.

## Pipeline stages

```
collect.py → enrich.py → graph.py → viz.py → ingest.py
```

| Stage | Script | Output |
|-------|--------|--------|
| 1. Collect | `scripts/osint/collect.py` | `YYYY-MM-DD-scan-raw.json` |
| 2. Enrich | `scripts/osint/enrich.py` | `YYYY-MM-DD-scan-enriched.json` |
| 3. Graph | `scripts/osint/graph.py` | `YYYY-MM-DD-graph.graphml` |
| 4. Viz | `scripts/osint/viz.py` | `YYYY-MM-DD-viz.html` |
| 5. Ingest | `scripts/osint/ingest.py` | Wiki pages |

## Protocols queried

| Protocol | Shodan query | Sector |
|----------|-------------|--------|
| Modbus | `port:502` | Power, water, manufacturing |
| BACnet | `port:47808` | Building automation |
| DNP3 | `port:20000` | Electric utilities, water |
| Siemens S7 | `port:102 product:Siemens` | Industrial PLCs |

## Graph model

**Node types:** `ip` (blue) · `asn` (purple) · `country` (gray) · `protocol` (protocol color)

**Edge types:** `ip → protocol` (exposes) · `ip → asn` (belongs_to) · `asn → country` (located_in)

## Ethical scope

- All data from Shodan passive index — no active scanning or interaction with target systems
- Findings kept in `visibility: public` wiki pages — no org-specific PII
- Methodology documented for reproducibility and auditability

## Run history


- **2026-04-19** — 3000 hosts across 4 protocols
