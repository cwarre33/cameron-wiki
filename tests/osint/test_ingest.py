import json
import pytest
from pathlib import Path
from scripts.osint.ingest import ingest, _compute_stats
from tests.osint.conftest import SCAN_DATE, SAMPLE_RAW


def _wiki_root(tmp_path):
    root = tmp_path / "wiki"
    (root / "techniques").mkdir(parents=True)
    (root / "open-questions").mkdir(parents=True)
    (root / "log.md").write_text("# Log\n", encoding="utf-8")
    (root / "index.md").write_text("# Index\n", encoding="utf-8")
    return root


def test_ingest_creates_technique_page(enriched_scan, tmp_path):
    wiki = _wiki_root(tmp_path)
    tech, _ = ingest(enriched_scan, wiki)
    assert tech.exists()
    assert "shodan-ics-osint" in tech.name


def test_ingest_creates_findings_page(enriched_scan, tmp_path):
    wiki = _wiki_root(tmp_path)
    _, findings = ingest(enriched_scan, wiki)
    assert findings.exists()
    assert SCAN_DATE in findings.name


def test_ingest_technique_has_frontmatter(enriched_scan, tmp_path):
    wiki = _wiki_root(tmp_path)
    tech, _ = ingest(enriched_scan, wiki)
    text = tech.read_text(encoding="utf-8")
    assert "type: technique" in text
    assert "visibility: public" in text


def test_ingest_findings_has_frontmatter(enriched_scan, tmp_path):
    wiki = _wiki_root(tmp_path)
    _, findings = ingest(enriched_scan, wiki)
    text = findings.read_text(encoding="utf-8")
    assert "type: open-question" in text
    assert SCAN_DATE in text


def test_ingest_appends_log(enriched_scan, tmp_path):
    wiki = _wiki_root(tmp_path)
    ingest(enriched_scan, wiki)
    log = (wiki / "log.md").read_text(encoding="utf-8")
    assert SCAN_DATE in log
    assert "Shodan ICS" in log


def test_ingest_updates_index(enriched_scan, tmp_path):
    wiki = _wiki_root(tmp_path)
    ingest(enriched_scan, wiki)
    index = (wiki / "index.md").read_text(encoding="utf-8")
    assert "ics-exposure" in index
    assert "shodan-ics-osint" in index


def test_compute_stats_counts_hosts():
    stats = _compute_stats(SAMPLE_RAW)
    assert stats["total_hosts"] == 1
    assert stats["protocol_count"] == 4


def test_compute_stats_top_countries():
    stats = _compute_stats(SAMPLE_RAW)
    countries = [c["country"] for c in stats["top_countries"]]
    assert "US" in countries


def test_ingest_idempotent_index(enriched_scan, tmp_path):
    """Running ingest twice should not duplicate index entries."""
    wiki = _wiki_root(tmp_path)
    ingest(enriched_scan, wiki)
    ingest(enriched_scan, wiki)
    index = (wiki / "index.md").read_text(encoding="utf-8")
    assert index.count("shodan-ics-osint") == 1
