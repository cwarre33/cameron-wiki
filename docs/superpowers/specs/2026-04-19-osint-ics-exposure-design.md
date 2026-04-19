# OSINT ICS Exposure Mapper — Design Spec

**Date:** 2026-04-19
**Author:** Cameron Warren
**Status:** Approved

## Overview

A modular five-stage CLI pipeline that queries the Shodan API for publicly exposed industrial control system (ICS) protocols, enriches the results with ASN/geo/CVE data, builds a relationship graph, generates a self-contained D3.js visualization, and ingests findings into `cameron-wiki`. Functional repeatability is the primary goal; portfolio polish follows once proven.

## Goals

- **Primary:** A re-runnable research tool that produces fresh ICS exposure data on demand
- **Secondary:** Feeds structured findings into `cameron-wiki` (raw + wiki pages)
- **Tertiary:** Generates a shareable D3.js visualization artifact for portfolio use

## Non-Goals

- Active scanning (all data sourced from Shodan's passive index)
- Real-time monitoring or alerting
- Polished CLI UX (Typer/Click packaging deferred until tool is proven)

## Protocols Covered

| Protocol | Port | Sector |
|----------|------|--------|
| Modbus | 502 | Power, water, manufacturing |
| BACnet | 47808 | Building automation |
| DNP3 | 20000 | Electric utilities, water |
| Siemens S7 | 102 | Industrial PLCs |

Shodan queries: `port:502`, `port:47808`, `port:20000`, `port:102 product:Siemens`

## Architecture

Five independent stages, each reads/writes timestamped JSON files in `raw/osint/`. Stages can be re-run independently — collect once, iterate on viz and wiki ingest without burning API quota.

```
collect.py → enrich.py → graph.py → viz.py → ingest.py
```

A `run_all.sh` convenience script chains all five stages.

## Directory Layout

```
raw/osint/
  YYYY-MM-DD-scan-raw.json        # Shodan API results, one entry per host
  YYYY-MM-DD-scan-enriched.json   # + ASN, geo, CVE enrichment
  YYYY-MM-DD-graph.graphml        # NetworkX graph export
  YYYY-MM-DD-viz.html             # Self-contained D3.js visualization

scripts/osint/
  collect.py                      # Stage 1: Shodan queries
  enrich.py                       # Stage 2: ASN/geo/CVE enrichment
  graph.py                        # Stage 3: NetworkX graph construction
  viz.py                          # Stage 4: D3.js HTML generation
  ingest.py                       # Stage 5: wiki page generation
  run_all.sh                      # Convenience runner (all stages)

wiki/techniques/
  shodan-ics-osint.md             # Methodology page (created once, updated each run)
wiki/open-questions/
  ics-exposure-YYYY-MM-DD.md      # Per-run findings page
```

## Data Model

### Enriched host record
```json
{
  "ip": "x.x.x.x",
  "port": 502,
  "protocol": "modbus",
  "org": "City Water Authority",
  "asn": "AS12345",
  "country": "US",
  "city": "Houston",
  "vulns": ["CVE-2021-1234"],
  "tags": ["ics", "scada"],
  "banner": "..."
}
```

### Scan envelope
```json
{
  "scan_date": "YYYY-MM-DD",
  "shodan_tier": "academic",
  "protocols": {
    "modbus": { "query": "port:502", "total_results": 12453, "sampled": 1000, "hosts": [...] },
    "bacnet":  { "query": "port:47808", ... },
    "dnp3":    { "query": "port:20000", ... },
    "s7":      { "query": "port:102 product:Siemens", ... }
  }
}
```

## Graph Model

**Node types:**

| Type | Color | Size | Attributes |
|------|-------|------|-----------|
| `ip` | Blue | Fixed small | org, city, vuln_count, port, protocol |
| `asn` | Purple | By ip_count | asn_number, org_name, ip_count |
| `country` | Gray | By total_exposed | name, total_exposed |
| `protocol` | Protocol color | By exposure_count | name, port, total_exposed |

**Edge types:**

| Edge | Meaning |
|------|---------|
| `ip → protocol` | exposes |
| `ip → asn` | belongs_to |
| `asn → country` | located_in |

## D3.js Visualization

Self-contained HTML file (no server required). Features:
- Force-directed graph layout
- Protocol filter pills (modbus / bacnet / dnp3 / s7 / all)
- Hover tooltip: org name, ASN, CVE count, city
- Drag nodes to explore clusters
- Saved to `raw/osint/YYYY-MM-DD-viz.html`

D3 template rendered via Jinja2 in `viz.py`.

## Wiki Integration

`ingest.py` generates two wiki artifacts per run:

1. **`wiki/techniques/shodan-ics-osint.md`** — methodology page, created once and updated with each run's metadata. Follows CLAUDE.md frontmatter conventions (`type: technique`, `visibility: public`).

2. **`wiki/open-questions/ics-exposure-YYYY-MM-DD.md`** — per-run findings: top countries by exposure, protocols ranked by count, notable orgs, CVE patterns. Type `open-question`, links to the methodology page via `[[wikilinks]]`.

Both pages appended to `wiki/log.md` and `wiki/index.md` per CLAUDE.md ingest workflow.

## Dependencies

```
shodan          # Shodan API client
networkx        # Graph construction and GraphML export
python-dotenv   # .env loading for SHODAN_API_KEY
jinja2          # D3 HTML templating
```

## Configuration

`SHODAN_API_KEY` loaded from `.env` (gitignored). Shodan account: academic/student tier — full API access, no result cap per query. Default sample: 1000 hosts per protocol for v1; configurable via `--limit` flag.

## Ethical / Legal Scope

- All data sourced from Shodan's passive index — no active scanning
- Read-only, no interaction with target systems
- Methodology documented for reproducibility and auditability
- Findings kept in `visibility: public` wiki pages — no org-specific PII

## Stage Details

### Stage 1: collect.py
- Initializes Shodan client from `.env`
- Runs four queries, pages through results up to `--limit` (default 1000/protocol)
- Writes `YYYY-MM-DD-scan-raw.json`

### Stage 2: enrich.py
- Reads raw JSON; Shodan results already include ASN, geo, org, vulns — no external API needed
- Normalizes fields, deduplicates IPs, writes `YYYY-MM-DD-scan-enriched.json`

### Stage 3: graph.py
- Builds NetworkX directed graph from enriched data
- Deduplicates ASN and country nodes
- Exports `YYYY-MM-DD-graph.graphml`

### Stage 4: viz.py
- Loads GraphML, converts to D3-compatible JSON (nodes + links arrays)
- Renders Jinja2 D3 template → `YYYY-MM-DD-viz.html`

### Stage 5: ingest.py
- Computes summary statistics (top 10 countries, protocol exposure counts, CVE frequency)
- Renders wiki page templates → writes to `wiki/open-questions/` and `wiki/techniques/`
- Appends to `wiki/log.md` and updates `wiki/index.md`

## Success Criteria

1. `run_all.sh` completes end-to-end without manual intervention
2. `raw/osint/` contains all four output files with today's date
3. D3 viz renders in browser with all four protocol filters functional
4. Two wiki pages created/updated and linked in `wiki/index.md`
5. Re-running `enrich.py` through `ingest.py` on cached raw data produces consistent output
