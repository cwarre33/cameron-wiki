import json
import os
import sys
from datetime import date
from pathlib import Path

import shodan
from dotenv import load_dotenv

PROTOCOLS = {
    "modbus": "port:502",
    "bacnet": "port:47808",
    "dnp3": "port:20000",
    "s7": "port:102 product:Siemens",
}


def _normalize_match(match: dict, protocol: str) -> dict:
    return {
        "ip": match.get("ip_str"),
        "port": match.get("port"),
        "protocol": protocol,
        "org": match.get("org") or None,
        "asn": match.get("asn") or None,
        "country": (match.get("location") or {}).get("country_code") or None,
        "city": (match.get("location") or {}).get("city") or None,
        "vulns": list(match.get("vulns") or {}.keys()),
        "tags": match.get("tags") or [],
        "banner": (match.get("data") or "")[:500],
    }


def collect(limit: int = 1000, out_dir: Path = None) -> Path:
    load_dotenv()
    api_key = os.environ.get("SHODAN_API_KEY")
    if not api_key:
        print("Error: SHODAN_API_KEY not set in environment or .env file", file=sys.stderr)
        sys.exit(1)
    api = shodan.Shodan(api_key)

    if out_dir is None:
        out_dir = Path("raw/osint")
    out_dir.mkdir(parents=True, exist_ok=True)

    scan_date = date.today().isoformat()
    result = {"scan_date": scan_date, "shodan_tier": "academic", "protocols": {}}

    for protocol, query in PROTOCOLS.items():
        hosts = []
        total = 0
        try:
            first = api.search(query, limit=1)
            total = first.get("total", 0)
        except shodan.APIError as e:
            print(f"[{protocol}] Shodan error getting total: {e}", file=sys.stderr)

        try:
            cursor = api.search_cursor(query)
            for match in cursor:
                if len(hosts) >= limit:
                    break
                hosts.append(_normalize_match(match, protocol))
        except shodan.APIError as e:
            print(f"[{protocol}] Shodan error collecting hosts: {e}", file=sys.stderr)

        result["protocols"][protocol] = {
            "query": query,
            "total_results": total,
            "sampled": len(hosts),
            "hosts": hosts,
        }
        print(f"[{protocol}] {len(hosts)} hosts collected")

    out_path = out_dir / f"{scan_date}-scan-raw.json"
    out_path.write_text(json.dumps(result, indent=2))
    print(f"Saved: {out_path}")
    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1000)
    args = parser.parse_args()
    collect(limit=args.limit)
