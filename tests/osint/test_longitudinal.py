import json
from unittest.mock import MagicMock, patch

import pytest


WALKER_BANNER = (
    "BACnet/IP\n"
    "Vendor: Delta Controls\n"
    "BBMD: 192.168.75.100:47808\n"
    "Foreign Device Table:\n"
    "  192.168.53.36:65121:ttl=60:timeout=25\n"
)


def _obs(banner: str, ts: str) -> dict:
    return {"data": banner, "timestamp": ts, "port": 47808}


def test_extract_fdt_entries_parses_walker_format():
    from scripts.osint.longitudinal import extract_fdt_entries
    entries = extract_fdt_entries(WALKER_BANNER)
    assert len(entries) == 1
    assert entries[0] == {
        "internal_ip": "192.168.53.36", "source_port": 65121,
        "ttl": 60, "timeout": 25,
    }


def test_extract_fdt_entries_handles_empty():
    from scripts.osint.longitudinal import extract_fdt_entries
    assert extract_fdt_entries("") == []
    assert extract_fdt_entries(None) == []


def test_extract_fdt_entries_multiple():
    from scripts.osint.longitudinal import extract_fdt_entries
    banner = (
        "FDT:\n"
        "  10.0.0.5:1234:ttl=60:timeout=30\n"
        "  10.0.0.6:5678:ttl=60:timeout=20\n"
    )
    entries = extract_fdt_entries(banner)
    assert len(entries) == 2
    assert {e["internal_ip"] for e in entries} == {"10.0.0.5", "10.0.0.6"}


def test_seed_ips_from_enriched_picks_only_bbmds(tmp_path):
    from scripts.osint.longitudinal import seed_ips_from_enriched
    enriched = tmp_path / "2026-04-19-scan-enriched.json"
    enriched.write_text(json.dumps({
        "scan_date": "2026-04-19",
        "protocols": {
            "bacnet": {"hosts": [
                {"ip": "1.1.1.1", "banner": WALKER_BANNER},  # has FDT
                {"ip": "2.2.2.2", "banner": "no FDT here"},   # no FDT
            ]},
        },
    }))
    seeds = seed_ips_from_enriched(enriched)
    assert seeds == ["1.1.1.1"]


def test_analyze_host_flags_persistent_tunnel():
    from scripts.osint.longitudinal import analyze_host
    obs = [
        _obs(WALKER_BANNER, "2026-03-20T00:00:00"),
        _obs(WALKER_BANNER.replace("65121", "54472"), "2026-03-24T00:00:00"),
        _obs(WALKER_BANNER.replace("65121", "55494"), "2026-04-01T00:00:00"),
        _obs(WALKER_BANNER.replace("65121", "65121"), "2026-04-19T00:00:00"),
    ]
    result = analyze_host("108.252.186.105", obs)
    assert result["public_ip"] == "108.252.186.105"
    assert result["observation_count"] == 4
    assert len(result["persistent_tunnels"]) == 1
    persistent = result["persistent_tunnels"][0]
    assert persistent["internal_ip"] == "192.168.53.36"
    assert persistent["scan_count"] == 4
    assert persistent["rotating_source_ports"] is True


def test_analyze_host_excludes_below_threshold():
    """A tunnel seen only once is not persistent."""
    from scripts.osint.longitudinal import analyze_host
    result = analyze_host("1.2.3.4", [_obs(WALKER_BANNER, "2026-04-19T00:00:00")])
    assert result["tunnel_count"] == 1
    assert result["persistent_tunnels"] == []


def _make_api(host_payload: dict) -> MagicMock:
    api = MagicMock()
    api.host.return_value = host_payload
    return api


def test_longitudinal_writes_output(tmp_path):
    api = _make_api({"data": [_obs(WALKER_BANNER, "2026-04-19T00:00:00")]})
    with patch("scripts.osint.longitudinal.shodan.Shodan", return_value=api), \
         patch.dict("os.environ", {"SHODAN_API_KEY": "test_key"}):
        from scripts.osint.longitudinal import longitudinal
        out = longitudinal(ips=["1.2.3.4"], out_dir=tmp_path, sleep_seconds=0)
    assert out.exists()
    payload = json.loads(out.read_text())
    assert payload["seeds"] == ["1.2.3.4"]
    assert payload["results"][0]["public_ip"] == "1.2.3.4"


def test_longitudinal_persistent_summary_filters(tmp_path):
    persistent_obs = [
        _obs(WALKER_BANNER, "2026-03-20T00:00:00"),
        _obs(WALKER_BANNER.replace("65121", "54472"), "2026-03-24T00:00:00"),
        _obs(WALKER_BANNER.replace("65121", "55494"), "2026-04-01T00:00:00"),
    ]
    api = _make_api({"data": persistent_obs})
    with patch("scripts.osint.longitudinal.shodan.Shodan", return_value=api), \
         patch.dict("os.environ", {"SHODAN_API_KEY": "test_key"}):
        from scripts.osint.longitudinal import longitudinal
        out = longitudinal(ips=["108.252.186.105"], out_dir=tmp_path, sleep_seconds=0)
    payload = json.loads(out.read_text())
    assert len(payload["persistent_summary"]) == 1
    assert payload["persistent_summary"][0]["public_ip"] == "108.252.186.105"


def test_longitudinal_seeds_from_enriched_when_no_ips(tmp_path):
    enriched = tmp_path / "2026-04-19-scan-enriched.json"
    enriched.write_text(json.dumps({
        "scan_date": "2026-04-19",
        "protocols": {"bacnet": {"hosts": [{"ip": "9.9.9.9", "banner": WALKER_BANNER}]}},
    }))
    api = _make_api({"data": []})
    with patch("scripts.osint.longitudinal.shodan.Shodan", return_value=api), \
         patch.dict("os.environ", {"SHODAN_API_KEY": "test_key"}):
        from scripts.osint.longitudinal import longitudinal
        out = longitudinal(enriched_path=enriched, out_dir=tmp_path, sleep_seconds=0)
    payload = json.loads(out.read_text())
    assert payload["seeds"] == ["9.9.9.9"]


def test_longitudinal_handles_shodan_error(tmp_path):
    import shodan
    api = MagicMock()
    api.host.side_effect = shodan.APIError("rate limited")
    with patch("scripts.osint.longitudinal.shodan.Shodan", return_value=api), \
         patch.dict("os.environ", {"SHODAN_API_KEY": "test_key"}):
        from scripts.osint.longitudinal import longitudinal
        out = longitudinal(ips=["1.2.3.4"], out_dir=tmp_path, sleep_seconds=0)
    payload = json.loads(out.read_text())
    assert payload["results"][0]["observation_count"] == 0
    assert payload["results"][0]["tunnel_count"] == 0
