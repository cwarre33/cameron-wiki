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
