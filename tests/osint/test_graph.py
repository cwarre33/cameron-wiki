import json
import networkx as nx
import pytest
from scripts.osint.graph import build_graph
from tests.osint.conftest import SCAN_DATE, SAMPLE_HOST, SAMPLE_RAW


def test_graph_writes_graphml(enriched_scan, tmp_path):
    out = build_graph(enriched_scan, tmp_path)
    assert out.exists()
    assert out.suffix == ".graphml"


def test_graph_has_ip_node(enriched_scan, tmp_path):
    out = build_graph(enriched_scan, tmp_path)
    G = nx.read_graphml(str(out))
    assert SAMPLE_HOST["ip"] in G.nodes


def test_graph_has_protocol_node(enriched_scan, tmp_path):
    out = build_graph(enriched_scan, tmp_path)
    G = nx.read_graphml(str(out))
    assert "modbus" in G.nodes
    assert G.nodes["modbus"]["node_type"] == "protocol"


def test_graph_has_asn_node(enriched_scan, tmp_path):
    out = build_graph(enriched_scan, tmp_path)
    G = nx.read_graphml(str(out))
    assert SAMPLE_HOST["asn"] in G.nodes
    assert G.nodes[SAMPLE_HOST["asn"]]["node_type"] == "asn"


def test_graph_has_country_node(enriched_scan, tmp_path):
    out = build_graph(enriched_scan, tmp_path)
    G = nx.read_graphml(str(out))
    assert SAMPLE_HOST["country"] in G.nodes
    assert G.nodes[SAMPLE_HOST["country"]]["node_type"] == "country"


def test_graph_edges(enriched_scan, tmp_path):
    out = build_graph(enriched_scan, tmp_path)
    G = nx.read_graphml(str(out))
    ip = SAMPLE_HOST["ip"]
    assert G.has_edge(ip, "modbus")
    assert G.has_edge(ip, SAMPLE_HOST["asn"])
    assert G.has_edge(SAMPLE_HOST["asn"], SAMPLE_HOST["country"])


def test_graph_empty_hosts_ok(tmp_path):
    """Graph builds without error when all protocols have no hosts."""
    raw = {
        "scan_date": SCAN_DATE,
        "shodan_tier": "academic",
        "protocols": {
            "modbus": {"query": "port:502", "total_results": 0, "sampled": 0, "hosts": []},
        },
    }
    path = tmp_path / f"{SCAN_DATE}-scan-enriched.json"
    path.write_text(json.dumps(raw))
    out = build_graph(path, tmp_path)
    G = nx.read_graphml(str(out))
    assert G.number_of_nodes() == 0
