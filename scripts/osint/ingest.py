import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent / "templates"
WIKI_ROOT = Path(__file__).parent.parent.parent / "wiki"


def _compute_stats(enriched: dict) -> dict:
    country_counter: Counter = Counter()
    vuln_counter: Counter = Counter()
    protocols = []
    total_hosts = 0

    for proto_name, proto_data in enriched["protocols"].items():
        hosts = proto_data["hosts"]
        total_hosts += len(hosts)
        protocols.append({
            "name": proto_name,
            "sampled": proto_data["sampled"],
            "total_results": proto_data["total_results"],
        })
        for host in hosts:
            if host.get("country"):
                country_counter[host["country"]] += 1
            for cve in host.get("vulns") or []:
                vuln_counter[cve] += 1

    top_countries = [{"country": c, "count": n} for c, n in country_counter.most_common(10)]
    top_vulns = [{"cve": v, "count": n} for v, n in vuln_counter.most_common(10)]

    return {
        "total_hosts": total_hosts,
        "protocol_count": len(protocols),
        "protocols": protocols,
        "top_countries": top_countries,
        "top_vulns": top_vulns,
    }


def _load_run_history(technique_path: Path, scan_date: str, stats: dict) -> list:
    runs = []
    if technique_path.exists():
        text = technique_path.read_text(encoding="utf-8")
        for m in re.finditer(r"\*\*(\d{4}-\d{2}-\d{2})\*\* — (\d+) hosts", text):
            if m.group(1) != scan_date:
                runs.append({"date": m.group(1), "total_hosts": int(m.group(2)), "protocol_count": 4})
    runs.append({"date": scan_date, "total_hosts": stats["total_hosts"], "protocol_count": stats["protocol_count"]})
    runs.sort(key=lambda r: r["date"])
    return runs


def ingest(enriched_path: Path, wiki_root: Path = None) -> tuple[Path, Path]:
    """
    Generate wiki pages from enriched scan JSON.
    Returns (technique_path, findings_path).
    """
    enriched = json.loads(enriched_path.read_text(encoding="utf-8"))
    scan_date = enriched["scan_date"]
    today = date.today().isoformat()

    if wiki_root is None:
        wiki_root = WIKI_ROOT

    technique_path = wiki_root / "techniques" / "shodan-ics-osint.md"
    findings_path = wiki_root / "open-questions" / f"ics-exposure-{scan_date}.md"

    technique_path.parent.mkdir(parents=True, exist_ok=True)
    findings_path.parent.mkdir(parents=True, exist_ok=True)

    stats = _compute_stats(enriched)
    runs = _load_run_history(technique_path, scan_date, stats)

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)

    # Write technique page (methodology, created once — updated each run)
    t_tmpl = env.get_template("technique.md.j2")
    created = today if not technique_path.exists() else _frontmatter_field(technique_path, "created") or today
    technique_path.write_text(
        t_tmpl.render(scan_date=scan_date, created=created, runs=runs),
        encoding="utf-8",
    )

    # Write per-run findings page
    f_tmpl = env.get_template("findings.md.j2")
    findings_path.write_text(
        f_tmpl.render(scan_date=scan_date, **stats),
        encoding="utf-8",
    )

    _append_log(wiki_root, scan_date, technique_path, findings_path)
    _update_index(wiki_root, scan_date, technique_path, findings_path)

    print(f"Technique: {technique_path}")
    print(f"Findings:  {findings_path}")
    return technique_path, findings_path


def _frontmatter_field(path: Path, field: str) -> str | None:
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"^{field}:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def _append_log(wiki_root: Path, scan_date: str, technique_path: Path, findings_path: Path) -> None:
    log_path = wiki_root / "log.md"
    if not log_path.exists():
        return
    entry = (
        f"\n## [{scan_date}] ingest | Shodan ICS Exposure Scan\n"
        f"Source: raw/osint/{scan_date}-scan-enriched.json\n"
        f"Pages created: [{findings_path.name}]\n"
        f"Pages updated: [{technique_path.name}]\n"
        f"Contradictions: none\n"
    )
    with log_path.open("a", encoding="utf-8") as f:
        f.write(entry)


def _update_index(wiki_root: Path, scan_date: str, technique_path: Path, findings_path: Path) -> None:
    index_path = wiki_root / "index.md"
    if not index_path.exists():
        return
    text = index_path.read_text(encoding="utf-8")

    findings_line = f"- [[ics-exposure-{scan_date}]] — ICS exposure findings {scan_date}"
    technique_line = "- [[shodan-ics-osint]] — Shodan ICS OSINT methodology"

    if findings_line not in text:
        text += f"\n{findings_line}\n"
    if technique_line not in text:
        text += f"{technique_line}\n"

    index_path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("enriched_path", type=Path)
    parser.add_argument("--wiki-root", type=Path, default=None)
    args = parser.parse_args()
    ingest(args.enriched_path, args.wiki_root)
