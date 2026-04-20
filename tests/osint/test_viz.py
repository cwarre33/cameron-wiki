import json
import pytest
from pathlib import Path
from scripts.osint.graph import build_graph
from scripts.osint.viz import build_viz
from tests.osint.conftest import SCAN_DATE


def _make_graphml(enriched_scan, tmp_path):
    return build_graph(enriched_scan, tmp_path)


def test_viz_writes_html(enriched_scan, tmp_path):
    gml = _make_graphml(enriched_scan, tmp_path)
    out = build_viz(gml, enriched_scan, tmp_path)
    assert out.exists()
    assert out.suffix == ".html"


def test_viz_contains_d3(enriched_scan, tmp_path):
    gml = _make_graphml(enriched_scan, tmp_path)
    out = build_viz(gml, enriched_scan, tmp_path)
    html = out.read_text(encoding="utf-8")
    assert "d3" in html


def test_viz_contains_scan_date(enriched_scan, tmp_path):
    gml = _make_graphml(enriched_scan, tmp_path)
    out = build_viz(gml, enriched_scan, tmp_path)
    html = out.read_text(encoding="utf-8")
    assert SCAN_DATE in html


def test_viz_filter_pills_present(enriched_scan, tmp_path):
    gml = _make_graphml(enriched_scan, tmp_path)
    out = build_viz(gml, enriched_scan, tmp_path)
    html = out.read_text(encoding="utf-8")
    for proto in ("modbus", "bacnet", "dnp3", "s7"):
        assert proto in html


def test_viz_graph_json_embedded(enriched_scan, tmp_path):
    gml = _make_graphml(enriched_scan, tmp_path)
    out = build_viz(gml, enriched_scan, tmp_path)
    html = out.read_text(encoding="utf-8")
    assert "GRAPH" in html
    assert "nodes" in html
    assert "links" in html
