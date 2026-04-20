import json
import sys
from pathlib import Path


def enrich(raw_path: Path, out_dir: Path = None) -> Path:
    """
    Read raw scan JSON, deduplicate IPs, normalize fields, write enriched JSON.
    Returns the path of the written enriched file.
    """
    data = json.loads(raw_path.read_text())

    if out_dir is None:
        out_dir = raw_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    scan_date = data["scan_date"]
    enriched = {
        "scan_date": scan_date,
        "shodan_tier": data.get("shodan_tier", "unknown"),
        "protocols": {},
    }

    for protocol, proto_data in data["protocols"].items():
        seen_ips = set()
        unique_hosts = []
        for host in proto_data["hosts"]:
            ip = host.get("ip")
            if ip and ip not in seen_ips:
                seen_ips.add(ip)
                unique_hosts.append(_normalize_host(host, protocol))

        enriched["protocols"][protocol] = {
            "query": proto_data["query"],
            "total_results": proto_data["total_results"],
            "sampled": proto_data["sampled"],
            "hosts": unique_hosts,
        }
        print(f"[{protocol}] {len(unique_hosts)} unique hosts (was {len(proto_data['hosts'])})")

    out_path = out_dir / f"{scan_date}-scan-enriched.json"
    out_path.write_text(json.dumps(enriched, indent=2))
    print(f"Saved: {out_path}")
    return out_path


def _normalize_host(host: dict, protocol: str) -> dict:
    """Ensure all required fields are present with consistent types."""
    return {
        "ip": host.get("ip") or "",
        "port": host.get("port") or 0,
        "protocol": protocol,
        "org": host.get("org") or None,
        "asn": host.get("asn") or None,
        "country": host.get("country") or None,
        "city": host.get("city") or None,
        "vulns": list(host.get("vulns") or []),
        "tags": list(host.get("tags") or []),
        "banner": str(host.get("banner") or "")[:500],
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_path", type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()
    enrich(args.raw_path, args.out_dir)
