"""Simple certificate transparency lookup for 216.67.73.166 attribution.

No API keys required - uses crt.sh only.
"""
import json
import socket
import sys
from datetime import date
from pathlib import Path

import requests

TARGET_IP = "216.67.73.166"
TARGET_ORGS = ["Alaska Integrated Services", "akintegrated", "Alaska Integrated"]
CRTSH_BASE = "https://crt.sh/"


def get_reverse_dns(ip: str) -> str | None:
    """Get reverse DNS for an IP."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None


def crtsh_search(query: str) -> list[dict]:
    """Query crt.sh with a search term."""
    url = f"{CRTSH_BASE}?q={query}&output=json"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            return resp.json() if isinstance(resp.json(), list) else []
    except Exception as e:
        print(f"Error searching '{query}': {e}", file=sys.stderr)
    return []


def main():
    print(f"=== Certificate Transparency Lookup: {TARGET_IP} ===\n")

    # 1. Reverse DNS lookup
    print("[1/4] Getting reverse DNS...")
    reverse_dns = get_reverse_dns(TARGET_IP)
    if reverse_dns:
        print(f"  Reverse DNS: {reverse_dns}")
    else:
        print(f"  No reverse DNS found for {TARGET_IP}")
    print()

    # 2. Search by reverse DNS domain
    certs = []
    if reverse_dns:
        print(f"[2/4] Searching crt.sh for %{reverse_dns}...")
        domain = ".".join(reverse_dns.split(".")[-2:])  # Get base domain
        cert_results = crtsh_search(f"%.{domain}")
        certs.extend(cert_results)
        print(f"  Found {len(cert_results)} certificates")
    print()

    # 3. Search by organization names
    print("[3/4] Searching crt.sh for organization names...")
    for org in TARGET_ORGS:
        results = crtsh_search(f"%{org}%")
        print(f"  '{org}': {len(results)} certificates")
        certs.extend(results)
    print()

    # 4. Dedupe and analyze
    print("[4/4] Analyzing certificates...")
    seen_ids = set()
    unique_certs = []
    for c in certs:
        cid = c.get("id")
        if cid and cid not in seen_ids:
            seen_ids.add(cid)
            unique_certs.append(c)

    print(f"  Unique certificates: {len(unique_certs)}")

    # Extract useful info
    cert_summary = []
    for c in unique_certs[:20]:  # Limit to 20
        cert_summary.append({
            "id": c.get("id"),
            "common_name": c.get("common_name"),
            "name_value": c.get("name_value", "")[:200],
            "issuer_name": c.get("issuer_name"),
            "not_before": c.get("not_before"),
            "not_after": c.get("not_after"),
        })
        print(f"    - {c.get('common_name')} (issued: {c.get('not_before', '?')[:10]})")

    # Save results
    scan_date = date.today().isoformat()
    payload = {
        "scan_date": scan_date,
        "target_ip": TARGET_IP,
        "reverse_dns": reverse_dns,
        "certificates_found": len(unique_certs),
        "certificate_details": cert_summary,
        "search_terms_used": [f"%.{reverse_dns}"] + [f"%{o}%" for o in TARGET_ORGS],
    }

    out_dir = Path("raw/osint")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"cert-lookup-{TARGET_IP.replace('.', '-')}-{scan_date}.json"
    out_path.write_text(json.dumps(payload, indent=2))

    print(f"\nOutput: {out_path}")

    # Attribution assessment
    print("\n=== Attribution Assessment ===")
    attribution_signals = []

    for c in cert_summary:
        cn = (c.get("common_name") or "").lower()
        nv = (c.get("name_value") or "").lower()

        for org in ["alaska integrated", "akintegrated", "alaskaintegrated"]:
            if org in cn or org in nv:
                attribution_signals.append(f"Certificate CN/NAM contains '{org}'")

    if attribution_signals:
        print("POSITIVE SIGNALS:")
        for s in attribution_signals:
            print(f"  - {s}")
    else:
        print("No direct certificate attribution signals found.")
        print("This is EXPECTED - integrators rarely have TLS certs on BMS monitoring stations.")
        print("Next step: manual web search for AIS case studies at target addresses.")


if __name__ == "__main__":
    main()
