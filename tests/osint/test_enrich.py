import json
import pytest
from scripts.osint.enrich import enrich


def test_enrich_writes_enriched_file(raw_scan, tmp_path):
    out = enrich(raw_scan, tmp_path)
    assert out.exists()
    assert "enriched" in out.name


def test_enrich_output_structure(raw_scan, tmp_path):
    out = enrich(raw_scan, tmp_path)
    data = json.loads(out.read_text())
    assert "scan_date" in data
    assert "protocols" in data
    assert set(data["protocols"].keys()) == {"modbus", "bacnet", "dnp3", "s7"}


def test_enrich_deduplicates_ips(tmp_path):
    """Hosts with duplicate IPs should be collapsed to one."""
    from tests.osint.conftest import SCAN_DATE, SAMPLE_HOST
    raw = {
        "scan_date": SCAN_DATE,
        "shodan_tier": "academic",
        "protocols": {
            "modbus": {
                "query": "port:502",
                "total_results": 2,
                "sampled": 2,
                "hosts": [SAMPLE_HOST, SAMPLE_HOST],  # same IP twice
            }
        },
    }
    raw_path = tmp_path / f"{SCAN_DATE}-scan-raw.json"
    raw_path.write_text(json.dumps(raw))
    out = enrich(raw_path, tmp_path)
    data = json.loads(out.read_text())
    assert len(data["protocols"]["modbus"]["hosts"]) == 1


def test_enrich_host_fields_present(raw_scan, tmp_path):
    out = enrich(raw_scan, tmp_path)
    data = json.loads(out.read_text())
    hosts = data["protocols"]["modbus"]["hosts"]
    assert len(hosts) == 1
    host = hosts[0]
    for field in ("ip", "port", "protocol", "org", "asn", "country", "city", "vulns", "tags", "banner"):
        assert field in host, f"Missing field: {field}"


def test_enrich_none_fields_handled(tmp_path):
    """Hosts with missing optional fields should not raise."""
    from tests.osint.conftest import SCAN_DATE
    raw = {
        "scan_date": SCAN_DATE,
        "shodan_tier": "academic",
        "protocols": {
            "modbus": {
                "query": "port:502",
                "total_results": 1,
                "sampled": 1,
                "hosts": [{"ip": "5.5.5.5", "port": 502}],
            }
        },
    }
    raw_path = tmp_path / f"{SCAN_DATE}-scan-raw.json"
    raw_path.write_text(json.dumps(raw))
    out = enrich(raw_path, tmp_path)
    data = json.loads(out.read_text())
    host = data["protocols"]["modbus"]["hosts"][0]
    assert host["org"] is None
    assert host["vulns"] == []
    assert host["banner"] == ""
