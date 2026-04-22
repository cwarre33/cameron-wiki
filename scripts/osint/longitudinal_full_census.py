"""Stage 6 (auxiliary): Full BACnet census longitudinal pull.

This script:
1. Reads the 2026-04-19-scan-enriched.json to get ALL BACnet hosts
2. Filters to those with BBMD configuration (Foreign Device Table entries)
3. Runs Shodan host(history=True) on each
4. Outputs expanded longitudinal data with scan counts, first/last seen, FDT IPs

Output: raw/osint/2026-04-21-longitudinal-full.json
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
RATE_LIMIT_SECONDS = 1.0  # Shodan free tier: 1 req/sec


def extract_fdt_entries(banner: str) -> list[dict]:
    """Parse Foreign Device Table entries from a BACnet banner."""
    if not banner:
        return []
    return [
        {
            "internal_ip": m[0],
            "source_port": int(m[1]),
            "ttl": int(m[2]),
            "timeout": int(m[3])
        }
        for m in FDT_PATTERN.findall(banner)
    ]


def is_bbmd(banner: str) -> bool:
    """Check if a BACnet banner indicates BBMD configuration."""
    if not banner:
        return False
    # BBMDs show either "Broadcast Management Device" or have FDT entries
    if "Broadcast Management Device" in banner or "BBMD" in banner:
        return True
    # Or if there are FDT entries
    if extract_fdt_entries(banner):
        return True
    return False


def extract_all_bacnet_hosts(enriched_path: Path) -> list[dict]:
    """Extract all BACnet hosts from enriched scan, flagging BBMDs."""
    data = json.loads(Path(enriched_path).read_text())
    bacnet = data.get("protocols", {}).get("bacnet", {})
    hosts = []
    for host in bacnet.get("hosts", []):
        ip = host.get("ip")
        banner = host.get("banner") or ""
        if is_bbmd(banner):
            hosts.append({
                "ip": ip,
                "banner": banner,
                "fdt_entries": extract_fdt_entries(banner),
                "country": host.get("country"),
                "org": host.get("org"),
                "product": host.get("product"),
            })
    return hosts


def fetch_history(api: "shodan.Shodan", ip: str) -> list[dict]:
    """Return the per-observation list from a Shodan host(history=True) call."""
    try:
        record = api.host(ip, history=True)
    except shodan.APIError as e:
        print(f"[{ip}] Shodan error: {e}", file=sys.stderr)
        return []
    return record.get("data") or []


def analyze_host(ip: str, observations: list[dict]) -> dict:
    """Aggregate FDT persistence evidence across all historical observations."""
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

    # Classify tunnel type
    for t in tunnels:
        ip_parts = t["internal_ip"].split(".")
        is_rfc1918 = (
            ip_parts[0] == "10" or
            (ip_parts[0] == "172" and 16 <= int(ip_parts[1]) <= 31) or
            (ip_parts[0] == "192" and ip_parts[1] == "168")
        )
        is_cgnat = ip_parts[0] == "100" and 64 <= int(ip_parts[1]) <= 127
        t["is_internal"] = is_rfc1918 or is_cgnat
        t["is_external_public"] = not is_rfc1918 and not is_cgnat

    return {
        "public_ip": ip,
        "observation_count": len(observations),
        "tunnel_count": len(tunnels),
        "tunnels": tunnels,
        "persistent_tunnels": [t for t in tunnels if t["scan_count"] >= 3],
        "external_fdt_count": sum(1 for t in tunnels if t.get("is_external_public")),
    }


def longitudinal_full_census(
    enriched_path: Path,
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

    # Extract all BACnet BBMD hosts
    print(f"Loading BACnet hosts from {enriched_path}...")
    bbmd_hosts = extract_all_bacnet_hosts(enriched_path)
    print(f"Found {len(bbmd_hosts)} BBMD candidates (hosts with FDT entries)\n")

    if not bbmd_hosts:
        print("No BBMD hosts to process — exiting.", file=sys.stderr)
        sys.exit(1)

    results = []
    for i, host_info in enumerate(bbmd_hosts, 1):
        ip = host_info["ip"]
        print(f"[{i}/{len(bbmd_hosts)}] {ip} ({host_info.get('country', '?')} / {host_info.get('product', 'N/A')})")
        observations = fetch_history(api, ip)
        result = analyze_host(ip, observations)
        result["country"] = host_info.get("country")
        result["org"] = host_info.get("org")
        result["product"] = host_info.get("product")
        results.append(result)

        if i < len(bbmd_hosts):
            time.sleep(sleep_seconds)

    # Compile summary stats
    hosts_with_any_fdt = sum(1 for r in results if r["tunnel_count"] > 0)
    hosts_with_persistent_fdt = sum(1 for r in results if r["persistent_tunnels"])
    hosts_with_external_fdt = sum(1 for r in results if r["external_fdt_count"] > 0)

    # Find shared FDT IPs (integrator pattern)
    fdt_ip_to_bbmds: dict[str, list[str]] = {}
    for r in results:
        for t in r.get("tunnels", []):
            fdt_ip = t["internal_ip"]
            if t.get("is_external_public"):
                fdt_ip_to_bbmds.setdefault(fdt_ip, []).append(r["public_ip"])

    shared_fdt_ips = {ip: bbmds for ip, bbmds in fdt_ip_to_bbmds.items() if len(bbmds) > 1}

    persistent = [
        {"public_ip": r["public_ip"], "tunnels": r["persistent_tunnels"]}
        for r in results if r["persistent_tunnels"]
    ]

    scan_date = date.today().isoformat()
    payload = {
        "scan_date": scan_date,
        "shodan_tier": "academic",
        "source_file": str(enriched_path),
        "summary": {
            "total_bbmd_hosts": len(bbmd_hosts),
            "hosts_with_any_fdt": hosts_with_any_fdt,
            "hosts_with_persistent_fdt": hosts_with_persistent_fdt,
            "hosts_with_external_fdt": hosts_with_external_fdt,
            "shared_fdt_ip_count": len(shared_fdt_ips),
            "shared_fdt_details": shared_fdt_ips,
        },
        "results": results,
        "persistent_summary": persistent,
    }

    out_path = out_dir / f"{scan_date}-longitudinal-full.json"
    out_path.write_text(json.dumps(payload, indent=2))

    print(f"\n{'='*60}")
    print(f"Saved: {out_path}")
    print(f"BBMD hosts checked:     {len(results)}")
    print(f"Hosts with any FDT:     {hosts_with_any_fdt}")
    print(f"Hosts with persistent:  {hosts_with_persistent_fdt}")
    print(f"Hosts with external:    {hosts_with_external_fdt}")

    if shared_fdt_ips:
        print(f"\nShared FDT IPs (integrator pattern): {len(shared_fdt_ips)}")
        for fdt_ip, bbmds in shared_fdt_ips.items():
            print(f"  {fdt_ip} -> {len(bbmds)} BBMDs: {', '.join(bbmds[:5])}{'...' if len(bbmds) > 5 else ''}")

    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--enriched",
        type=Path,
        default=Path("raw/osint/2026-04-19-scan-enriched.json"),
        help="Path to enriched scan JSON"
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=RATE_LIMIT_SECONDS,
        help="Seconds to sleep between Shodan host calls (default 1.0)"
    )
    args = parser.parse_args()

    longitudinal_full_census(
        enriched_path=args.enriched,
        sleep_seconds=args.sleep
    )
