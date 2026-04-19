# OSINT ICS Exposure Mapper — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a five-stage modular CLI pipeline that queries Shodan for exposed ICS protocols, builds a relationship graph, generates a D3.js visualization, and ingests findings into cameron-wiki.

**Architecture:** Five independent Python scripts in `scripts/osint/` each read/write timestamped JSON files in `raw/osint/`. Stages chain via file convention (today's date prefix) and can be re-run independently. Jinja2 renders the D3 HTML and wiki markdown. All config via `.env`.

**Tech Stack:** Python 3.10+, shodan, networkx, jinja2, python-dotenv, pytest, D3.js v7 (CDN)

---

## File Map

| File | Responsibility |
|------|---------------|
| `scripts/osint/__init__.py` | Package marker |
| `scripts/osint/collect.py` | Stage 1: query Shodan API, write raw JSON |
| `scripts/osint/enrich.py` | Stage 2: normalize fields, deduplicate hosts |
| `scripts/osint/graph.py` | Stage 3: build NetworkX graph, export GraphML |
| `scripts/osint/viz.py` | Stage 4: load GraphML, render D3 HTML via Jinja2 |
| `scripts/osint/ingest.py` | Stage 5: compute stats, write wiki pages, append log |
| `scripts/osint/templates/d3_graph.html.j2` | D3.js force-directed graph template |
| `scripts/osint/templates/wiki_findings.md.j2` | Per-run findings page template |
| `scripts/osint/templates/wiki_methodology.md.j2` | Methodology page template (written once) |
| `scripts/osint/run_all.sh` | Chains all five stages |
| `requirements-osint.txt` | Python dependencies |
| `tests/osint/__init__.py` | Package marker |
| `tests/osint/conftest.py` | Shared fixtures (tmp scan data) |
| `tests/osint/test_collect.py` | Tests for collect.py |
| `tests/osint/test_enrich.py` | Tests for enrich.py |
| `tests/osint/test_graph.py` | Tests for graph.py |
| `tests/osint/test_viz.py` | Tests for viz.py |
| `tests/osint/test_ingest.py` | Tests for ingest.py |

---

## Task 1: Project Scaffold

**Files:**
- Create: `scripts/osint/__init__.py`
- Create: `tests/osint/__init__.py`
- Create: `tests/osint/conftest.py`
- Create: `requirements-osint.txt`
- Modify: `.gitignore`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p scripts/osint/templates
mkdir -p tests/osint
mkdir -p raw/osint
```

- [ ] **Step 2: Create package markers**

`scripts/osint/__init__.py` — empty file.
`tests/osint/__init__.py` — empty file.

- [ ] **Step 3: Write requirements-osint.txt**

```
shodan>=1.31.0
networkx>=3.3
python-dotenv>=1.0.0
jinja2>=3.1.4
pytest>=8.2.0
```

- [ ] **Step 4: Write tests/osint/conftest.py**

```python
import json
import pytest
from pathlib import Path
from datetime import date


SCAN_DATE = "2026-04-19"

SAMPLE_HOST = {
    "ip": "1.2.3.4",
    "port": 502,
    "protocol": "modbus",
    "org": "City Water Authority",
    "asn": "AS12345",
    "country": "US",
    "city": "Houston",
    "vulns": ["CVE-2021-1234"],
    "tags": ["ics"],
    "banner": "Modbus banner data",
}

SAMPLE_RAW = {
    "scan_date": SCAN_DATE,
    "shodan_tier": "academic",
    "protocols": {
        "modbus": {
            "query": "port:502",
            "total_results": 1,
            "sampled": 1,
            "hosts": [SAMPLE_HOST],
        },
        "bacnet": {
            "query": "port:47808",
            "total_results": 0,
            "sampled": 0,
            "hosts": [],
        },
        "dnp3": {
            "query": "port:20000",
            "total_results": 0,
            "sampled": 0,
            "hosts": [],
        },
        "s7": {
            "query": "port:102 product:Siemens",
            "total_results": 0,
            "sampled": 0,
            "hosts": [],
        },
    },
}


@pytest.fixture
def raw_scan(tmp_path):
    """Write sample raw scan JSON to tmp_path, return its Path."""
    p = tmp_path / f"{SCAN_DATE}-scan-raw.json"
    p.write_text(json.dumps(SAMPLE_RAW))
    return p


@pytest.fixture
def enriched_scan(tmp_path):
    """Write sample enriched scan JSON to tmp_path, return its Path."""
    p = tmp_path / f"{SCAN_DATE}-scan-enriched.json"
    p.write_text(json.dumps(SAMPLE_RAW))
    return p
```

- [ ] **Step 5: Update .gitignore**

Add these lines to `.gitignore`:

```
raw/osint/*.json
raw/osint/*.graphml
```

(Keep `raw/osint/*.html` unignored — the D3 viz is the portfolio artifact.)

- [ ] **Step 6: Install dependencies**

```bash
pip install -r requirements-osint.txt
```

Expected: all packages install without error.

- [ ] **Step 7: Commit scaffold**

```bash
git add scripts/osint/__init__.py tests/osint/__init__.py tests/osint/conftest.py requirements-osint.txt .gitignore
git commit -m "feat(osint): project scaffold — directories, deps, test fixtures"
```

---

## Task 2: collect.py

**Files:**
- Create: `scripts/osint/collect.py`
- Create: `tests/osint/test_collect.py`

- [ ] **Step 1: Write failing tests**

`tests/osint/test_collect.py`:

```python
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


MOCK_MATCH = {
    "ip_str": "1.2.3.4",
    "port": 502,
    "org": "City Water Authority",
    "asn": "AS12345",
    "location": {"country_code": "US", "city": "Houston"},
    "vulns": {"CVE-2021-1234": {}},
    "tags": ["ics"],
    "data": "Modbus banner",
}


def make_mock_api(match=MOCK_MATCH, total=1):
    api = MagicMock()
    api.search_cursor.return_value = iter([match])
    api.search.return_value = {"matches": [match], "total": total}
    return api


def test_collect_writes_output_file(tmp_path):
    with patch("scripts.osint.collect.shodan.Shodan", return_value=make_mock_api()), \
         patch("scripts.osint.collect.Path", wraps=Path), \
         patch.dict("os.environ", {"SHODAN_API_KEY": "test_key"}):
        from scripts.osint.collect import collect
        out = collect(limit=1, out_dir=tmp_path)
    assert out.exists()


def test_collect_output_has_all_protocols(tmp_path):
    with patch("scripts.osint.collect.shodan.Shodan", return_value=make_mock_api()), \
         patch.dict("os.environ", {"SHODAN_API_KEY": "test_key"}):
        from scripts.osint.collect import collect
        out = collect(limit=1, out_dir=tmp_path)
    data = json.loads(out.read_text())
    assert set(data["protocols"].keys()) == {"modbus", "bacnet", "dnp3", "s7"}


def test_collect_host_fields(tmp_path):
    with patch("scripts.osint.collect.shodan.Shodan", return_value=make_mock_api()), \
         patch.dict("os.environ", {"SHODAN_API_KEY": "test_key"}):
        from scripts.osint.collect import collect
        out = collect(limit=1, out_dir=tmp_path)
    hosts = json.loads(out.read_text())["protocols"]["modbus"]["hosts"]
    assert hosts[0]["ip"] == "1.2.3.4"
    assert hosts[0]["asn"] == "AS12345"
    assert hosts[0]["vulns"] == ["CVE-2021-1234"]


def test_collect_banner_truncated(tmp_path):
    long_match = dict(MOCK_MATCH, data="x" * 1000)
    with patch("scripts.osint.collect.shodan.Shodan", return_value=make_mock_api(long_match)), \
         patch.dict("os.environ", {"SHODAN_API_KEY": "test_key"}):
        from scripts.osint.collect import collect
        out = collect(limit=1, out_dir=tmp_path)
    host = json.loads(out.read_text())["protocols"]["modbus"]["hosts"][0]
    assert len(host["banner"]) <= 500
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
pytest tests/osint/test_collect.py -v
```

Expected: `ImportError: cannot import name 'collect'`

- [ ] **Step 3: Write scripts/osint/collect.py**

```python
import json
import os
import sys
from datetime import date
from pathlib import Path

import shodan
from dotenv import load_dotenv

PROTOCOLS = {
    "modbus": "port:502",
    "bacnet": "port:47808",
    "dnp3": "port:20000",
    "s7": "port:102 product:Siemens",
}


def _normalize_match(match: dict, protocol: str) -> dict:
    return {
        "ip": match.get("ip_str"),
        "port": match.get("port"),
        "protocol": protocol,
        "org": match.get("org") or None,
        "asn": match.get("asn") or None,
        "country": (match.get("location") or {}).get("country_code") or None,
        "city": (match.get("location") or {}).get("city") or None,
        "vulns": list(match.get("vulns") or {}.keys()),
        "tags": match.get("tags") or [],
        "banner": (match.get("data") or "")[:500],
    }


def collect(limit: int = 1000, out_dir: Path = None) -> Path:
    load_dotenv()
    api = shodan.Shodan(os.environ["SHODAN_API_KEY"])

    if out_dir is None:
        out_dir = Path("raw/osint")
    out_dir.mkdir(parents=True, exist_ok=True)

    scan_date = date.today().isoformat()
    result = {"scan_date": scan_date, "shodan_tier": "academic", "protocols": {}}

    for protocol, query in PROTOCOLS.items():
        hosts = []
        total = 0
        try:
            cursor = api.search_cursor(query)
            for match in cursor:
                if len(hosts) >= limit:
                    break
                hosts.append(_normalize_match(match, protocol))
            # total from first page search for reporting
            first = api.search(query, limit=1)
            total = first.get("total", len(hosts))
        except shodan.APIError as e:
            print(f"[{protocol}] Shodan error: {e}", file=sys.stderr)

        result["protocols"][protocol] = {
            "query": query,
            "total_results": total,
            "sampled": len(hosts),
            "hosts": hosts,
        }
        print(f"[{protocol}] {len(hosts)} hosts collected")

    out_path = out_dir / f"{scan_date}-scan-raw.json"
    out_path.write_text(json.dumps(result, indent=2))
    print(f"Saved → {out_path}")
    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1000)
    args = parser.parse_args()
    collect(limit=args.limit)
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
pytest tests/osint/test_collect.py -v
```

Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/osint/collect.py tests/osint/test_collect.py
git commit -m "feat(osint): Stage 1 collect.py — Shodan multi-protocol query"
```

---

## Task 3: enrich.py

**Files:**
- Create: `scripts/osint/enrich.py`
- Create: `tests/osint/test_enrich.py`

- [ ] **Step 1: Write failing tests**

`tests/osint/test_enrich.py`:

```python
import json
import pytest


def test_enrich_writes_output_file(raw_scan, tmp_path):
    from scripts.osint.enrich import enrich
    out = enrich(raw_path=raw_scan, out_dir=tmp_path)
    assert out.exists()


def test_enrich_deduplicates_by_ip_port(tmp_path):
    import json
    from scripts.osint.enrich import enrich

    # two identical hosts
    dup_host = {
        "ip": "1.2.3.4", "port": 502, "protocol": "modbus",
        "org": "Test", "asn": "AS1", "country": "US", "city": "Dallas",
        "vulns": [], "tags": [], "banner": "",
    }
    data = {
        "scan_date": "2026-04-19", "shodan_tier": "academic",
        "protocols": {
            "modbus": {"query": "port:502", "total_results": 2, "sampled": 2,
                       "hosts": [dup_host, dup_host]},
        },
    }
    raw = tmp_path / "2026-04-19-scan-raw.json"
    raw.write_text(json.dumps(data))

    out = enrich(raw_path=raw, out_dir=tmp_path)
    result = json.loads(out.read_text())
    assert result["protocols"]["modbus"]["sampled"] == 1


def test_enrich_empty_string_becomes_none(raw_scan, tmp_path):
    import json
    from scripts.osint.enrich import enrich

    data = json.loads(raw_scan.read_text())
    data["protocols"]["modbus"]["hosts"][0]["org"] = ""
    raw_scan.write_text(json.dumps(data))

    out = enrich(raw_path=raw_scan, out_dir=tmp_path)
    result = json.loads(out.read_text())
    assert result["protocols"]["modbus"]["hosts"][0]["org"] is None


def test_enrich_output_filename(raw_scan, tmp_path):
    from scripts.osint.enrich import enrich
    out = enrich(raw_path=raw_scan, out_dir=tmp_path)
    assert "enriched" in out.name
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
pytest tests/osint/test_enrich.py -v
```

Expected: `ImportError`

- [ ] **Step 3: Write scripts/osint/enrich.py**

```python
import json
from datetime import date
from pathlib import Path


def enrich(raw_path: Path = None, out_dir: Path = None) -> Path:
    if raw_path is None:
        scan_date = date.today().isoformat()
        raw_path = Path("raw/osint") / f"{scan_date}-scan-raw.json"
    raw_path = Path(raw_path)

    if out_dir is None:
        out_dir = raw_path.parent
    out_dir = Path(out_dir)

    data = json.loads(raw_path.read_text())
    seen: set[tuple] = set()

    for protocol, pdata in data["protocols"].items():
        deduped = []
        for host in pdata["hosts"]:
            key = (host.get("ip"), host.get("port"))
            if key in seen:
                continue
            seen.add(key)
            # normalize empty strings to None
            host = {k: (v if v != "" else None) for k, v in host.items()}
            deduped.append(host)
        pdata["hosts"] = deduped
        pdata["sampled"] = len(deduped)

    out_name = raw_path.name.replace("scan-raw", "scan-enriched")
    out_path = out_dir / out_name
    out_path.write_text(json.dumps(data, indent=2))
    print(f"Saved → {out_path}")
    return out_path


if __name__ == "__main__":
    enrich()
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
pytest tests/osint/test_enrich.py -v
```

Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/osint/enrich.py tests/osint/test_enrich.py
git commit -m "feat(osint): Stage 2 enrich.py — normalize and deduplicate hosts"
```

---

## Task 4: graph.py

**Files:**
- Create: `scripts/osint/graph.py`
- Create: `tests/osint/test_graph.py`

- [ ] **Step 1: Write failing tests**

`tests/osint/test_graph.py`:

```python
import json
import networkx as nx
import pytest


def test_graph_writes_graphml(enriched_scan, tmp_path):
    from scripts.osint.graph import build_graph
    out = build_graph(enriched_path=enriched_scan, out_dir=tmp_path)
    assert out.exists()
    assert out.suffix == ".graphml"


def test_graph_has_protocol_nodes(enriched_scan, tmp_path):
    from scripts.osint.graph import build_graph
    out = build_graph(enriched_path=enriched_scan, out_dir=tmp_path)
    G = nx.read_graphml(str(out))
    types = [d["type"] for _, d in G.nodes(data=True)]
    assert "protocol" in types


def test_graph_has_ip_node(enriched_scan, tmp_path):
    from scripts.osint.graph import build_graph
    out = build_graph(enriched_path=enriched_scan, out_dir=tmp_path)
    G = nx.read_graphml(str(out))
    assert "ip:1.2.3.4" in G.nodes


def test_graph_has_country_node(enriched_scan, tmp_path):
    from scripts.osint.graph import build_graph
    out = build_graph(enriched_path=enriched_scan, out_dir=tmp_path)
    G = nx.read_graphml(str(out))
    assert "country:US" in G.nodes


def test_graph_exposes_edge(enriched_scan, tmp_path):
    from scripts.osint.graph import build_graph
    out = build_graph(enriched_path=enriched_scan, out_dir=tmp_path)
    G = nx.read_graphml(str(out))
    assert G.has_edge("ip:1.2.3.4", "protocol:modbus")
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
pytest tests/osint/test_graph.py -v
```

Expected: `ImportError`

- [ ] **Step 3: Write scripts/osint/graph.py**

```python
import json
from datetime import date
from pathlib import Path

import networkx as nx

PROTOCOL_COLORS = {
    "modbus": "#2563eb",
    "bacnet": "#dc2626",
    "dnp3": "#059669",
    "s7": "#d97706",
}


def build_graph(enriched_path: Path = None, out_dir: Path = None) -> Path:
    if enriched_path is None:
        scan_date = date.today().isoformat()
        enriched_path = Path("raw/osint") / f"{scan_date}-scan-enriched.json"
    enriched_path = Path(enriched_path)

    if out_dir is None:
        out_dir = enriched_path.parent
    out_dir = Path(out_dir)

    data = json.loads(enriched_path.read_text())
    G = nx.DiGraph()

    # Protocol nodes
    for protocol, pdata in data["protocols"].items():
        G.add_node(
            f"protocol:{protocol}",
            type="protocol",
            label=protocol,
            color=PROTOCOL_COLORS[protocol],
            exposure_count=pdata["sampled"],
        )

    for protocol, pdata in data["protocols"].items():
        for host in pdata["hosts"]:
            ip = host["ip"]
            if not ip:
                continue

            G.add_node(
                f"ip:{ip}",
                type="ip",
                label=ip,
                color="#60a5fa",
                org=host.get("org") or "",
                city=host.get("city") or "",
                vuln_count=len(host.get("vulns") or []),
            )
            G.add_edge(f"ip:{ip}", f"protocol:{protocol}", relation="exposes")

            asn = host.get("asn")
            if asn:
                asn_id = f"asn:{asn}"
                if not G.has_node(asn_id):
                    G.add_node(
                        asn_id,
                        type="asn",
                        label=asn,
                        color="#a78bfa",
                        org_name=host.get("org") or "",
                        ip_count=0,
                    )
                G.nodes[asn_id]["ip_count"] = G.nodes[asn_id].get("ip_count", 0) + 1
                G.add_edge(f"ip:{ip}", asn_id, relation="belongs_to")

            country = host.get("country")
            if country:
                country_id = f"country:{country}"
                if not G.has_node(country_id):
                    G.add_node(
                        country_id,
                        type="country",
                        label=country,
                        color="#6b7280",
                        total_exposed=0,
                    )
                G.nodes[country_id]["total_exposed"] = G.nodes[country_id].get("total_exposed", 0) + 1
                if asn:
                    asn_id = f"asn:{asn}"
                    if not G.has_edge(asn_id, country_id):
                        G.add_edge(asn_id, country_id, relation="located_in")

    out_name = enriched_path.name.replace("scan-enriched.json", "graph.graphml")
    out_path = out_dir / out_name
    nx.write_graphml(G, str(out_path))
    print(f"Saved → {out_path}  ({G.number_of_nodes()} nodes, {G.number_of_edges()} edges)")
    return out_path


if __name__ == "__main__":
    build_graph()
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
pytest tests/osint/test_graph.py -v
```

Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add scripts/osint/graph.py tests/osint/test_graph.py
git commit -m "feat(osint): Stage 3 graph.py — NetworkX directed graph + GraphML export"
```

---

## Task 5: D3 Template + viz.py

**Files:**
- Create: `scripts/osint/templates/d3_graph.html.j2`
- Create: `scripts/osint/viz.py`
- Create: `tests/osint/test_viz.py`

- [ ] **Step 1: Write failing tests**

`tests/osint/test_viz.py`:

```python
import networkx as nx
import pytest


def _make_graphml(tmp_path):
    """Build a minimal GraphML fixture and return its path."""
    import json
    from scripts.osint.graph import build_graph
    from tests.osint.conftest import SCAN_DATE, SAMPLE_RAW

    enriched = tmp_path / f"{SCAN_DATE}-scan-enriched.json"
    enriched.write_text(json.dumps(SAMPLE_RAW))
    return build_graph(enriched_path=enriched, out_dir=tmp_path)


def test_viz_writes_html(tmp_path):
    from scripts.osint.viz import build_viz
    graph_path = _make_graphml(tmp_path)
    out = build_viz(graph_path=graph_path, out_dir=tmp_path)
    assert out.exists()
    assert out.suffix == ".html"


def test_viz_html_contains_d3(tmp_path):
    from scripts.osint.viz import build_viz
    graph_path = _make_graphml(tmp_path)
    out = build_viz(graph_path=graph_path, out_dir=tmp_path)
    html = out.read_text()
    assert "d3js.org" in html


def test_viz_html_contains_filter_pills(tmp_path):
    from scripts.osint.viz import build_viz
    graph_path = _make_graphml(tmp_path)
    out = build_viz(graph_path=graph_path, out_dir=tmp_path)
    html = out.read_text()
    for proto in ["modbus", "bacnet", "dnp3", "s7"]:
        assert proto in html


def test_viz_html_contains_graph_data(tmp_path):
    from scripts.osint.viz import build_viz
    graph_path = _make_graphml(tmp_path)
    out = build_viz(graph_path=graph_path, out_dir=tmp_path)
    html = out.read_text()
    assert "1.2.3.4" in html  # the sample IP appears in graph data JSON
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
pytest tests/osint/test_viz.py -v
```

Expected: `ImportError`

- [ ] **Step 3: Write scripts/osint/templates/d3_graph.html.j2**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>ICS Exposure Map — {{ scan_date }}</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; background: #0f172a; font-family: system-ui, sans-serif; color: #e2e8f0; }
  h1 { padding: 16px 20px 2px; font-size: 16px; margin: 0; }
  .sub { padding: 2px 20px 10px; font-size: 12px; color: #64748b; margin: 0; }
  #filters { padding: 6px 20px; display: flex; gap: 8px; }
  .pill { border: none; border-radius: 10px; padding: 3px 12px; font-size: 11px; cursor: pointer; color: white; opacity: 0.45; transition: opacity 0.15s; }
  .pill.active { opacity: 1; }
  .pill-all { background: #334155; }
  svg { display: block; }
  .tooltip {
    position: absolute; background: #1e293b; border: 1px solid #334155;
    border-radius: 6px; padding: 8px 12px; font-size: 11px;
    pointer-events: none; display: none; max-width: 200px;
  }
  .tooltip strong { display: block; font-size: 12px; margin-bottom: 3px; }
  .tooltip .dim { color: #64748b; }
</style>
</head>
<body>
<h1>ICS Protocol Exposure Map</h1>
<p class="sub">{{ scan_date }} &nbsp;·&nbsp; Shodan passive index &nbsp;·&nbsp; Legitimate OSINT (read-only)</p>
<div id="filters">
  <button class="pill pill-all active" onclick="setFilter('all',this)">all</button>
  <button class="pill" style="background:#2563eb" onclick="setFilter('modbus',this)">modbus</button>
  <button class="pill" style="background:#dc2626" onclick="setFilter('bacnet',this)">bacnet</button>
  <button class="pill" style="background:#059669" onclick="setFilter('dnp3',this)">dnp3</button>
  <button class="pill" style="background:#d97706" onclick="setFilter('s7',this)">s7</button>
</div>
<svg id="graph"></svg>
<div class="tooltip" id="tip"></div>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const data = {{ graph_data | safe }};
let activeFilter = 'all';

const W = window.innerWidth, H = window.innerHeight - 80;
const svg = d3.select('#graph').attr('width', W).attr('height', H);
const g = svg.append('g');

svg.call(d3.zoom().scaleExtent([0.05, 10]).on('zoom', e => g.attr('transform', e.transform)));

function radius(d) {
  if (d.type === 'protocol') return 18;
  if (d.type === 'country') return 8 + Math.min((d.total_exposed || 0) / 60, 16);
  if (d.type === 'asn') return 5 + Math.min((d.ip_count || 0) / 12, 10);
  return 3.5;
}

function visible(d) {
  if (activeFilter === 'all') return true;
  if (d.type === 'protocol') return d.label === activeFilter;
  if (d.type === 'ip') {
    return data.links.some(l => {
      const s = l.source.id ?? l.source;
      const t = l.target.id ?? l.target;
      return s === d.id && t === `protocol:${activeFilter}`;
    });
  }
  return true;
}

function linkVisible(l) {
  if (activeFilter === 'all') return true;
  const t = l.target.id ?? l.target;
  return t === `protocol:${activeFilter}`;
}

const sim = d3.forceSimulation(data.nodes)
  .force('link', d3.forceLink(data.links).id(d => d.id).distance(70).strength(0.4))
  .force('charge', d3.forceManyBody().strength(-90))
  .force('center', d3.forceCenter(W / 2, H / 2))
  .force('collide', d3.forceCollide().radius(d => radius(d) + 3));

const link = g.append('g').selectAll('line')
  .data(data.links).join('line')
  .attr('stroke', '#334155').attr('stroke-width', 0.7);

const node = g.append('g').selectAll('circle')
  .data(data.nodes).join('circle')
  .attr('r', d => radius(d))
  .attr('fill', d => d.color)
  .attr('stroke', '#0f172a').attr('stroke-width', 1)
  .call(d3.drag()
    .on('start', (e,d) => { if (!e.active) sim.alphaTarget(0.3).restart(); d.fx=d.x; d.fy=d.y; })
    .on('drag',  (e,d) => { d.fx=e.x; d.fy=e.y; })
    .on('end',   (e,d) => { if (!e.active) sim.alphaTarget(0); d.fx=null; d.fy=null; }));

const label = g.append('g').selectAll('text')
  .data(data.nodes.filter(d => d.type === 'protocol' || d.type === 'country')).join('text')
  .text(d => d.label)
  .attr('fill', '#94a3b8').attr('font-size', d => d.type === 'protocol' ? 11 : 9)
  .attr('text-anchor', 'middle').attr('pointer-events', 'none');

const tip = d3.select('#tip');
node.on('mouseover', (e,d) => {
  let h = `<strong>${d.label}</strong>`;
  if (d.org) h += `<div>${d.org}</div>`;
  if (d.city) h += `<div class="dim">${d.city}</div>`;
  if (d.vuln_count) h += `<div class="dim">CVEs: ${d.vuln_count}</div>`;
  if (d.exposure_count) h += `<div class="dim">Exposed: ${d.exposure_count}</div>`;
  if (d.ip_count) h += `<div class="dim">IPs in ASN: ${d.ip_count}</div>`;
  if (d.total_exposed) h += `<div class="dim">Country total: ${d.total_exposed}</div>`;
  tip.html(h).style('display','block')
    .style('left',(e.pageX+14)+'px').style('top',(e.pageY-8)+'px');
})
.on('mousemove', e => tip.style('left',(e.pageX+14)+'px').style('top',(e.pageY-8)+'px'))
.on('mouseout',  () => tip.style('display','none'));

sim.on('tick', () => {
  link.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y)
      .attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);
  node.attr('cx',d=>d.x).attr('cy',d=>d.y);
  label.attr('x',d=>d.x).attr('y',d=>d.y - radius(d) - 4);
});

function setFilter(f, btn) {
  activeFilter = f;
  document.querySelectorAll('.pill').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  node.attr('opacity', d => visible(d) ? 1 : 0.08);
  link.attr('opacity', l => linkVisible(l) ? 0.6 : 0.04);
  label.attr('opacity', d => visible(d) ? 1 : 0.08);
}
</script>
</body>
</html>
```

- [ ] **Step 4: Write scripts/osint/viz.py**

```python
import json
from datetime import date
from pathlib import Path

import networkx as nx
from jinja2 import Environment, FileSystemLoader


def build_viz(graph_path: Path = None, out_dir: Path = None) -> Path:
    if graph_path is None:
        scan_date = date.today().isoformat()
        graph_path = Path("raw/osint") / f"{scan_date}-graph.graphml"
    graph_path = Path(graph_path)

    if out_dir is None:
        out_dir = graph_path.parent
    out_dir = Path(out_dir)

    G = nx.read_graphml(str(graph_path))
    scan_date = graph_path.name.split("-graph.graphml")[0]

    nodes = [
        {
            "id": nid,
            "label": attrs.get("label", nid),
            "type": attrs.get("type", "ip"),
            "color": attrs.get("color", "#60a5fa"),
            "org": attrs.get("org", ""),
            "city": attrs.get("city", ""),
            "vuln_count": int(attrs.get("vuln_count", 0)),
            "exposure_count": int(attrs.get("exposure_count", 0)),
            "ip_count": int(attrs.get("ip_count", 0)),
            "total_exposed": int(attrs.get("total_exposed", 0)),
        }
        for nid, attrs in G.nodes(data=True)
    ]
    links = [
        {"source": src, "target": dst, "relation": attrs.get("relation", "")}
        for src, dst, attrs in G.edges(data=True)
    ]

    graph_data = json.dumps({"nodes": nodes, "links": links})
    template_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    html = env.get_template("d3_graph.html.j2").render(
        graph_data=graph_data,
        scan_date=scan_date,
    )

    out_name = graph_path.name.replace("graph.graphml", "viz.html")
    out_path = out_dir / out_name
    out_path.write_text(html, encoding="utf-8")
    print(f"Saved → {out_path}")
    return out_path


if __name__ == "__main__":
    build_viz()
```

- [ ] **Step 5: Run tests to confirm they pass**

```bash
pytest tests/osint/test_viz.py -v
```

Expected: 4 passed.

- [ ] **Step 6: Commit**

```bash
git add scripts/osint/viz.py scripts/osint/templates/d3_graph.html.j2 tests/osint/test_viz.py
git commit -m "feat(osint): Stage 4 viz.py + D3 template — force-directed graph HTML"
```

---

## Task 6: Wiki Templates + ingest.py

**Files:**
- Create: `scripts/osint/templates/wiki_findings.md.j2`
- Create: `scripts/osint/templates/wiki_methodology.md.j2`
- Create: `scripts/osint/ingest.py`
- Create: `tests/osint/test_ingest.py`

- [ ] **Step 1: Write failing tests**

`tests/osint/test_ingest.py`:

```python
import json
import pytest
from pathlib import Path
from tests.osint.conftest import SCAN_DATE, SAMPLE_RAW


def _setup_wiki(tmp_path):
    """Create minimal wiki structure expected by ingest.py."""
    (tmp_path / "wiki" / "open-questions").mkdir(parents=True)
    (tmp_path / "wiki" / "techniques").mkdir(parents=True)
    log = tmp_path / "wiki" / "log.md"
    log.write_text("# Activity Log\n\n---\n")
    return log


def test_ingest_creates_findings_page(tmp_path):
    from scripts.osint.ingest import ingest
    enriched = tmp_path / f"{SCAN_DATE}-scan-enriched.json"
    enriched.write_text(json.dumps(SAMPLE_RAW))
    _setup_wiki(tmp_path)
    findings = ingest(enriched_path=enriched, wiki_dir=tmp_path / "wiki")
    assert findings.exists()


def test_ingest_findings_has_frontmatter(tmp_path):
    from scripts.osint.ingest import ingest
    enriched = tmp_path / f"{SCAN_DATE}-scan-enriched.json"
    enriched.write_text(json.dumps(SAMPLE_RAW))
    _setup_wiki(tmp_path)
    findings = ingest(enriched_path=enriched, wiki_dir=tmp_path / "wiki")
    text = findings.read_text()
    assert "---" in text
    assert "type: open-question" in text
    assert "visibility: public" in text


def test_ingest_creates_methodology_page(tmp_path):
    from scripts.osint.ingest import ingest
    enriched = tmp_path / f"{SCAN_DATE}-scan-enriched.json"
    enriched.write_text(json.dumps(SAMPLE_RAW))
    _setup_wiki(tmp_path)
    ingest(enriched_path=enriched, wiki_dir=tmp_path / "wiki")
    methodology = tmp_path / "wiki" / "techniques" / "shodan-ics-osint.md"
    assert methodology.exists()


def test_ingest_appends_to_log(tmp_path):
    from scripts.osint.ingest import ingest
    enriched = tmp_path / f"{SCAN_DATE}-scan-enriched.json"
    enriched.write_text(json.dumps(SAMPLE_RAW))
    log = _setup_wiki(tmp_path)
    ingest(enriched_path=enriched, wiki_dir=tmp_path / "wiki")
    assert SCAN_DATE in log.read_text()


def test_ingest_methodology_not_overwritten(tmp_path):
    from scripts.osint.ingest import ingest
    enriched = tmp_path / f"{SCAN_DATE}-scan-enriched.json"
    enriched.write_text(json.dumps(SAMPLE_RAW))
    _setup_wiki(tmp_path)
    methodology = tmp_path / "wiki" / "techniques" / "shodan-ics-osint.md"
    methodology.write_text("existing content")
    ingest(enriched_path=enriched, wiki_dir=tmp_path / "wiki")
    assert methodology.read_text() == "existing content"
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
pytest tests/osint/test_ingest.py -v
```

Expected: `ImportError`

- [ ] **Step 3: Write scripts/osint/templates/wiki_findings.md.j2**

```markdown
---
title: "ICS Protocol Exposure — {{ scan_date }}"
type: open-question
status: active
visibility: public
sources: ["raw/osint/{{ scan_date }}-scan-enriched.json"]
related: ["[[wiki/techniques/shodan-ics-osint.md]]"]
created: {{ scan_date }}
updated: {{ scan_date }}
confidence: high
tags: [osint, ics, scada, shodan, modbus, bacnet, dnp3, s7, critical-infrastructure]
---

# ICS Protocol Exposure — {{ scan_date }}

**{{ total_hosts }} publicly exposed ICS hosts** across 4 protocols via Shodan passive index.

## Protocol Exposure

| Protocol | Port | Exposed Hosts |
|----------|------|--------------|
| modbus | 502 | {{ protocol_counts.modbus }} |
| bacnet | 47808 | {{ protocol_counts.bacnet }} |
| dnp3 | 20000 | {{ protocol_counts.dnp3 }} |
| s7 | 102 | {{ protocol_counts.s7 }} |

## Top Countries by Exposure

| Rank | Country | Hosts |
|------|---------|-------|
{% for country, count in top_countries %}| {{ loop.index }} | {{ country }} | {{ count }} |
{% endfor %}

## Notable Findings

- **{{ total_with_vulns }}** of {{ total_hosts }} hosts have known CVEs mapped by Shodan
- See [[wiki/techniques/shodan-ics-osint.md]] for pipeline methodology

## Open Questions

- Which ASNs appear across multiple protocols?
- Are CVE-flagged hosts concentrated in specific countries or sectors?
- How does exposure compare to the previous scan?
```

- [ ] **Step 4: Write scripts/osint/templates/wiki_methodology.md.j2**

```markdown
---
title: Shodan ICS/SCADA OSINT — Methodology
type: technique
status: active
visibility: public
sources: []
related: []
created: {{ created_date }}
updated: {{ created_date }}
confidence: high
tags: [osint, shodan, ics, scada, methodology, critical-infrastructure, network-mapping]
---

# Shodan ICS/SCADA OSINT — Methodology

Five-stage passive OSINT pipeline mapping publicly exposed ICS protocols. All data from Shodan's internet-wide scan index — read-only, no active scanning, no interaction with target systems.

## Pipeline

`collect.py` → `enrich.py` → `graph.py` → `viz.py` → `ingest.py`

| Stage | Script | Output |
|-------|--------|--------|
| Collect | `scripts/osint/collect.py` | `YYYY-MM-DD-scan-raw.json` |
| Enrich | `scripts/osint/enrich.py` | `YYYY-MM-DD-scan-enriched.json` |
| Graph | `scripts/osint/graph.py` | `YYYY-MM-DD-graph.graphml` |
| Viz | `scripts/osint/viz.py` | `YYYY-MM-DD-viz.html` |
| Ingest | `scripts/osint/ingest.py` | wiki pages |

## Protocols

| Protocol | Shodan Query | Sector |
|----------|-------------|--------|
| Modbus | `port:502` | Power, water, manufacturing |
| BACnet | `port:47808` | Building automation |
| DNP3 | `port:20000` | Electric utilities, water |
| Siemens S7 | `port:102 product:Siemens` | Industrial PLCs |

## Ethical Scope

- Shodan academic/student API key — passive index only
- No active scanning, no interaction with discovered hosts
- Findings documented for defensive research and public awareness
- Run: `bash scripts/osint/run_all.sh` from project root
```

- [ ] **Step 5: Write scripts/osint/ingest.py**

```python
import json
from collections import Counter
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def ingest(enriched_path: Path = None, wiki_dir: Path = None) -> Path:
    if enriched_path is None:
        scan_date = date.today().isoformat()
        enriched_path = Path("raw/osint") / f"{scan_date}-scan-enriched.json"
    enriched_path = Path(enriched_path)

    if wiki_dir is None:
        wiki_dir = Path("wiki")
    wiki_dir = Path(wiki_dir)

    data = json.loads(enriched_path.read_text())
    scan_date = data["scan_date"]

    all_hosts = [
        h for pdata in data["protocols"].values() for h in pdata["hosts"]
    ]
    protocol_counts = {
        p: data["protocols"][p]["sampled"] for p in data["protocols"]
    }
    country_counter = Counter(h["country"] for h in all_hosts if h.get("country"))
    top_countries = country_counter.most_common(10)
    total_with_vulns = sum(1 for h in all_hosts if h.get("vulns"))

    template_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))

    # Per-run findings page
    findings_md = env.get_template("wiki_findings.md.j2").render(
        scan_date=scan_date,
        protocol_counts=protocol_counts,
        top_countries=top_countries,
        total_hosts=len(all_hosts),
        total_with_vulns=total_with_vulns,
    )
    findings_path = wiki_dir / "open-questions" / f"ics-exposure-{scan_date}.md"
    findings_path.write_text(findings_md)

    # Methodology page — only write once
    methodology_path = wiki_dir / "techniques" / "shodan-ics-osint.md"
    if not methodology_path.exists():
        methodology_md = env.get_template("wiki_methodology.md.j2").render(
            created_date=scan_date,
        )
        methodology_path.write_text(methodology_md)

    # Append to wiki/log.md
    log_path = wiki_dir / "log.md"
    log_entry = (
        f"\n## [{scan_date}] ingest | ICS Protocol Exposure Scan\n\n"
        f"Source: raw/osint/{scan_date}-scan-enriched.json\n"
        f"Pages created: wiki/open-questions/ics-exposure-{scan_date}.md\n"
        f"Pages updated: wiki/techniques/shodan-ics-osint.md\n"
        f"Contradictions: none\n"
        f"Key findings:\n"
        f"  - Total exposed hosts: {len(all_hosts)}\n"
        f"  - Hosts with CVEs: {total_with_vulns}\n"
        f"  - Protocol counts: {protocol_counts}\n"
        f"  - Top country: {top_countries[0] if top_countries else 'N/A'}\n\n"
        f"---\n"
    )
    with open(log_path, "a") as f:
        f.write(log_entry)

    print(f"Saved → {findings_path}")
    print(f"Updated → {log_path}")
    return findings_path


if __name__ == "__main__":
    ingest()
```

- [ ] **Step 6: Run tests to confirm they pass**

```bash
pytest tests/osint/test_ingest.py -v
```

Expected: 5 passed.

- [ ] **Step 7: Commit**

```bash
git add scripts/osint/ingest.py scripts/osint/templates/wiki_findings.md.j2 scripts/osint/templates/wiki_methodology.md.j2 tests/osint/test_ingest.py
git commit -m "feat(osint): Stage 5 ingest.py + wiki templates — findings and methodology pages"
```

---

## Task 7: run_all.sh + Full Test Suite

**Files:**
- Create: `scripts/osint/run_all.sh`

- [ ] **Step 1: Write run_all.sh**

`scripts/osint/run_all.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

LIMIT=${1:-1000}

echo "=== OSINT ICS Exposure Mapper ==="
echo "Limit: $LIMIT hosts per protocol"
echo ""

echo "[1/5] Collecting from Shodan..."
python scripts/osint/collect.py --limit "$LIMIT"

echo ""
echo "[2/5] Enriching (normalize + deduplicate)..."
python scripts/osint/enrich.py

echo ""
echo "[3/5] Building graph..."
python scripts/osint/graph.py

echo ""
echo "[4/5] Generating D3 visualization..."
python scripts/osint/viz.py

echo ""
echo "[5/5] Ingesting into wiki..."
python scripts/osint/ingest.py

echo ""
echo "=== Done. Check raw/osint/ for output files. ==="
```

- [ ] **Step 2: Make executable**

```bash
chmod +x scripts/osint/run_all.sh
```

- [ ] **Step 3: Run full test suite**

```bash
pytest tests/osint/ -v
```

Expected: all tests pass. Count: 4 (collect) + 4 (enrich) + 5 (graph) + 4 (viz) + 5 (ingest) = **22 passed**.

- [ ] **Step 4: Run smoke test with real Shodan API**

```bash
# Run with small limit first to verify API key and output format
bash scripts/osint/run_all.sh 50
```

Expected: five `Saved →` lines, four files in `raw/osint/` with today's date, `wiki/open-questions/ics-exposure-YYYY-MM-DD.md` created.

- [ ] **Step 5: Open the D3 visualization**

```bash
# Windows
start raw/osint/*-viz.html
```

Verify: page loads, four protocol filter pills visible, nodes draggable, hover tooltips show org/city/CVE count.

- [ ] **Step 6: Commit**

```bash
git add scripts/osint/run_all.sh
git commit -m "feat(osint): run_all.sh convenience runner — chains all five pipeline stages"
```

- [ ] **Step 7: Run at full limit and commit wiki artifacts**

```bash
bash scripts/osint/run_all.sh 1000
git add wiki/open-questions/ics-exposure-*.md wiki/techniques/shodan-ics-osint.md wiki/log.md
git add raw/osint/*-viz.html
git commit -m "data(osint): first full ICS exposure scan — $(date +%Y-%m-%d)"
```

---

## Self-Review

**Spec coverage:**
- ✅ Five stages: collect, enrich, graph, viz, ingest
- ✅ Four protocols: Modbus, BACnet, DNP3, S7
- ✅ Shodan academic key via .env
- ✅ NetworkX graph with 4 node types, 3 edge types
- ✅ D3 force-directed viz with filter pills and hover tooltip
- ✅ Wiki findings + methodology pages with correct frontmatter
- ✅ `wiki/log.md` append
- ✅ `run_all.sh` convenience runner
- ✅ Configurable `--limit` flag in collect.py

**Placeholder scan:** None found.

**Type consistency:**
- `collect()` returns `Path` → `enrich(raw_path=Path)` ✅
- `enrich()` returns `Path` → `graph.build_graph(enriched_path=Path)` ✅
- `build_graph()` returns `Path` → `build_viz(graph_path=Path)` ✅
- `build_viz()` returns `Path` → `ingest(enriched_path=Path)` ✅ (ingest takes enriched, not viz)
- `wiki_dir` param consistent across `ingest()` and tests ✅
- `out_dir` param consistent across all stages and tests ✅
