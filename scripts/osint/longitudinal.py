"""Stage 6 (auxiliary): Longitudinal Shodan history pull for BBMD persistence detection.

For a curated list of BACnet BBMD IPs, fetches Shodan host history and identifies
internal devices that have been re-registering through the public BBMD across
multiple scans (the "persistent FDT tunnel" pattern surfaced in WalkerMedical).

Input options:
  - default: read most-recent enriched scan JSON, extract BACnet hosts with FDT
             entries in their banner, use as seed list
  - --ips:   comma-separated IP list overrides

Output: raw/osint/YYYY-MM-DD-longitudinal.json
"""
import json
import os
import re
import sys
import time
from datetime import date
from pathlib import Path

import shodan
from dotenv import load_dotenv

FDT_PATTERN = re.compile(
    r'(\d+\.\d+\.\d+\.\d+):(\d+):ttl=(\d+):timeout=(\d+)'
)
RATE_LIMIT_SECONDS = 1.0


def extract_fdt_entries(banner: str) -> list[dict]:
    """Parse Foreign Device Table entries from a BACnet banner."""
    if not banner:
        return []
    return [
        {"internal_ip": m[0], "source_port": int(m[1]), "ttl": int(m[2]), "timeout": int(m[3])}
        for m in FDT_PATTERN.findall(banner)
    ]


def seed_ips_from_enriched(enriched_path: Path) -> list[str]:
    """Find BACnet hosts whose banner shows any FDT entry — those are BBMDs worth tracking."""
    data = json.loads(Path(enriched_path).read_text())
    bacnet = data.get("protocols", {}).get("bacnet", {})
    seeds = []
    for host in bacnet.get("hosts", []):
        if extract_fdt_entries(host.get("banner") or ""):
            seeds.append(host["ip"])
    return seeds


def _latest_enriched(out_dir: Path) -> Path | None:
    candidates = sorted(out_dir.glob("*-scan-enriched.json"))
    return candidates[-1] if candidates else None


def fetch_history(api: "shodan.Shodan", ip: str) -> list[dict]:
    """Return the per-observation list from a Shodan host(history=True) call."""
    try:
        record = api.host(ip, history=True)
    except shodan.APIError as e:
        print(f"[{ip}] Shodan error: {e}", file=sys.stderr)
        return []
    return record.get("data") or []


def analyze_host(ip: str, observations: list[dict]) -> dict:
    """Aggregate FDT persistence evidence across all historical observations of one BBMD."""
    by_internal: dict[str, list[dict]] = {}
    for obs in observations:
        for fdt in extract_fdt_entries(obs.get("data") or ""):
            entry = {
                "timestamp": obs.get("timestamp"),
                "source_port": fdt["source_port"],
                "ttl": fdt["ttl"],
                "timeout": fdt["timeout"],
            }
            by_internal.setdefault(fdt["internal_ip"], []).append(entry)

    tunnels = []
    for internal_ip, entries in by_internal.items():
        scans = sorted({e["timestamp"] for e in entries if e["timestamp"]})
        ports = sorted({e["source_port"] for e in entries})
        tunnels.append({
            "internal_ip": internal_ip,
            "scan_count": len(scans),
            "first_seen": scans[0] if scans else None,
            "last_seen": scans[-1] if scans else None,
            "rotating_source_ports": len(ports) > 1,
            "distinct_source_ports": ports,
            "ttl_values": sorted({e["ttl"] for e in entries}),
        })
    tunnels.sort(key=lambda t: t["scan_count"], reverse=True)

    return {
        "public_ip": ip,
        "observation_count": len(observations),
        "tunnel_count": len(tunnels),
        "tunnels": tunnels,
        "persistent_tunnels": [t for t in tunnels if t["scan_count"] >= 3],
    }


def longitudinal(
    enriched_path: Path = None,
    ips: list[str] = None,
    out_dir: Path = None,
    sleep_seconds: float = RATE_LIMIT_SECONDS,
) -> Path:
    load_dotenv()
    api_key = os.environ.get("SHODAN_API_KEY")
    if not api_key:
        print("Error: SHODAN_API_KEY not set in environment or .env file", file=sys.stderr)
        sys.exit(1)
    api = shodan.Shodan(api_key)

    if out_dir is None:
        out_dir = Path("raw/osint")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if ips is None:
        if enriched_path is None:
            enriched_path = _latest_enriched(out_dir)
        if enriched_path is None:
            print("Error: no enriched scan found and no --ips given", file=sys.stderr)
            sys.exit(1)
        ips = seed_ips_from_enriched(Path(enriched_path))
        print(f"Seeded {len(ips)} BBMD candidates from {enriched_path}")

    if not ips:
        print("No IPs to process — exiting.")
        sys.exit(0)

    results = []
    for i, ip in enumerate(ips, 1):
        print(f"[{i}/{len(ips)}] {ip}")
        observations = fetch_history(api, ip)
        results.append(analyze_host(ip, observations))
        if i < len(ips):
            time.sleep(sleep_seconds)

    persistent = [
        {"public_ip": r["public_ip"], "tunnels": r["persistent_tunnels"]}
        for r in results if r["persistent_tunnels"]
    ]

    scan_date = date.today().isoformat()
    payload = {
        "scan_date": scan_date,
        "shodan_tier": "academic",
        "seeds": ips,
        "results": results,
        "persistent_summary": persistent,
    }
    out_path = out_dir / f"{scan_date}-longitudinal.json"
    out_path.write_text(json.dumps(payload, indent=2))

    print(f"\nSaved: {out_path}")
    print(f"Hosts checked:        {len(results)}")
    print(f"Hosts with any FDT:   {sum(1 for r in results if r['tunnel_count'])}")
    print(f"Hosts with persistent FDT (>=3 scans): {len(persistent)}")
    if persistent:
        print("\nPersistent tunnels (the WalkerMedical pattern):")
        for entry in persistent:
            for t in entry["tunnels"]:
                print(
                    f"  {entry['public_ip']} -> {t['internal_ip']}  "
                    f"({t['scan_count']} scans, "
                    f"{'rotating' if t['rotating_source_ports'] else 'static'} ports)"
                )
    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--enriched", type=Path, default=None,
                        help="Path to enriched scan JSON (defaults to latest in raw/osint/)")
    parser.add_argument("--ips", type=str, default=None,
                        help="Comma-separated IP list (overrides --enriched seeding)")
    parser.add_argument("--sleep", type=float, default=RATE_LIMIT_SECONDS,
                        help="Seconds to sleep between Shodan host calls (default 1.0)")
    args = parser.parse_args()

    ip_list = [ip.strip() for ip in args.ips.split(",")] if args.ips else None
    longitudinal(enriched_path=args.enriched, ips=ip_list, sleep_seconds=args.sleep)
