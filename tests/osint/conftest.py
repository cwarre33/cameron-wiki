import json
import pytest


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
