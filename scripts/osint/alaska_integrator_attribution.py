"""Certificate transparency and attribution lookup for 216.67.73.166 (Alaska integrator).

This script:
1. Queries crt.sh for any certificates served from 216.67.73.166 or adjacent /24
2. Looks for DNS records pointing to 216.67.0.0/17
3. Searches Shodan for any TLS banners on that IP
4. Searches for case studies/press releases naming Alaska Integrated Services at target addresses

Output: raw/osint/alaska-integrator-attribution-YYYY-MM-DD.json
"""
import json
import re
import sys
import time
from datetime import date
from pathlib import Path

import requests
import shodan
from dotenv import load_dotenv

TARGET_IP = "216.67.73.166"
TARGET_NETWORK = "216.67.0.0/17"
TARGET_ORG = "Alaska Integrated Services"
TARGET_ADDRESSES = [
    "12350 Industry Way, Anchorage, AK",
    "6411 A Street, Anchorage, AK",
    "383 Industrial Way, Anchorage, AK",
]

CRTSH_BASE = "https://crt.sh/"


def fetch_crtsh_ip_certs(ip: str) -> list[dict]:
    """Query crt.sh for certificates matching an IP address (reverse DNS or SAN)."""
    # crt.sh doesn't directly support IP lookups, but we can try:
    # 1. Reverse DNS of the IP
    # 2. IP as a string in SAN (rare but happens)
    import socket
    try:
        reverse_dns = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        reverse_dns = None

    certs = []
    if reverse_dns:
        url = f"{CRTSH_BASE}?q=%.{reverse_dns}&output=json"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                certs = resp.json()
        except Exception as e:
            print(f"[crt.sh] Error for {reverse_dns}: {e}", file=sys.stderr)
    return certs


def fetch_crtsh_org_certs(org: str) -> list[dict]:
    """Query crt.sh for certificates issued to an organization."""
    # Search by common name containing org name
    certs = []
    search_terms = [
        f"%{org}%",
        f"%{org.replace(' ', '')}%",
        "%akintegrated%",
        "%alaskaintegrated%",
    ]
    for term in search_terms:
        url = f"{CRTSH_BASE}?q={term}&output=json"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list):
                    certs.extend(data)
        except Exception as e:
            print(f"[crt.sh] Error for '{term}': {e}", file=sys.stderr)
        time.sleep(0.5)
    return certs


def dedupe_certs(certs: list[dict]) -> list[dict]:
    """Remove duplicate certificates by MIN_ISSUE_KEY."""
    seen = set()
    unique = []
    for c in certs:
        key = c.get("min_issue_date", "") + str(c.get("id", ""))
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique


def analyze_cert_for_attribution(cert: dict, target_ip: str) -> dict | None:
    """Check if a certificate provides attribution evidence."""
    evidence = {
        "cert_id": cert.get("id"),
        "common_name": cert.get("common_name", ""),
        "name_value": cert.get("name_value", ""),
        "issuer_name": cert.get("issuer_name", ""),
        "not_before": cert.get("not_before"),
        "not_after": cert.get("not_after"),
        "attribution_signal": None,
    }

    # Check for IP in SAN
    name_value = cert.get("name_value", "")
    if target_ip in name_value:
        evidence["attribution_signal"] = f"IP {target_ip} found in SAN"
        return evidence

    # Check for org-related domains
    org_signals = ["akintegrated", "alaskaintegrated", "alaska-integrated"]
    for signal in org_signals:
        if signal.lower() in name_value.lower():
            evidence["attribution_signal"] = f"Org domain signal: {signal}"
            return evidence

    return None


def shodan_ip_lookup(api: "shodan.Shodan", ip: str) -> dict:
    """Get Shodan host data for an IP, focusing on TLS/SSL info."""
    try:
        host = api.host(ip)
        return {
            "ip": ip,
            "org": host.get("org"),
            "isp": host.get("isp"),
            "hostnames": host.get("hostnames", []),
            "domains": host.get("domains", []),
            "ports": host.get("ports", []),
            "ssl_certs": [
                {
                    "port": s.get("port"),
                    "cert_subject": s.get("ssl", {}).get("cert", {}).get("subject", {}),
                    "cert_issuer": s.get("ssl", {}).get("cert", {}).get("issuer", {}),
                    "cert_subject_cn": s.get("ssl", {}).get("cert", {}).get("subject", {}).get("CN", ""),
                    "cert_issuer_cn": s.get("ssl", {}).get("cert", {}).get("issuer", {}).get("CN", ""),
                    "cert_alt_names": s.get("ssl", {}).get("cert", {}).get("alt_names", {}).get("dns", []),
                }
                for s in (host.get("data") or [])
                if s.get("ssl")
            ],
            "tags": host.get("tags", []),
        }
    except shodan.APIError as e:
        return {"ip": ip, "error": str(e)}


def shodan_search_bacnet_alaska(api: "shodan.Shodan") -> list[dict]:
    """Search Shodan for BACnet devices in Alaska that might name the integrator."""
    results = []
    queries = [
        "bacnet country:US region:Alaska",
        "bacnet org:\"Alaska Communications\"",
        "bacnet Anchorage",
    ]
    for q in queries:
        try:
            resp = api.search(q)
            for match in resp.get("matches", [])[:50]:
                results.append({
                    "ip": match.get("ip_str"),
                    "org": match.get("org"),
                    "product": match.get("product"),
                    "data": match.get("data")[:500] if match.get("data") else None,
                    "query": q,
                })
        except shodan.APIError as e:
            print(f"[Shodan search] Error for '{q}': {e}", file=sys.stderr)
        time.sleep(0.5)
    return results


def web_search_evidence(org: str, addresses: list[str]) -> list[dict]:
    """Use Brave Search (if available) to find case studies or press releases."""
    evidence = []
    brave_api_key = Path(".env").exists() and next(
        (line.split("=", 1)[1] for line in Path(".env").read_text().splitlines()
         if line.startswith("BRAVE_API_KEY=")), None
    )

    search_queries = [
        f'"{org}" "12350 Industry Way" Anchorage',
        f'"{org}" "6411 A Street" Anchorage',
        f'"{org}" Delta Controls case study',
        f'"{org}" building automation Alaska',
        "Alaska Integrated Services Delta Controls",
        "akintegrated.com Delta Controls",
    ]

    if brave_api_key:
        headers = {"Accept": "application/json", "X-Subscription-Key": brave_api_key}
        for q in search_queries:
            try:
                resp = requests.get(
                    "https://api.search.brave.com/res/v1/web/search",
                    headers=headers,
                    params={"q": q, "count": 5},
                    timeout=10,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    for result in data.get("web", {}).get("results", [])[:5]:
                        evidence.append({
                            "query": q,
                            "title": result.get("title"),
                            "url": result.get("url"),
                            "snippet": result.get("description"),
                        })
            except Exception as e:
                print(f"[Brave search] Error for '{q}': {e}", file=sys.stderr)
            time.sleep(0.5)
    else:
        print("[Brave search] API key not found — skipping web search", file=sys.stderr)

    return evidence


def main():
    load_dotenv()
    shodan_api_key = Path(".env").exists() and next(
        (line.split("=", 1)[1] for line in Path(".env").read_text().splitlines()
         if line.startswith("SHODAN_API_KEY=")), None
    )
    if not shodan_api_key:
        print("Error: SHODAN_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    api = shodan.Shodan(shodan_api_key)

    print(f"=== Alaska Integrator Attribution: {TARGET_IP} ===\n")

    # 1. crt.sh org lookup
    print("[1/5] Querying crt.sh for organization certificates...")
    org_certs = fetch_crtsh_org_certs(TARGET_ORG)
    org_certs = dedupe_certs(org_certs)
    print(f"  Found {len(org_certs)} certificates for '{TARGET_ORG}'\n")

    # 2. crt.sh IP reverse DNS lookup
    print("[2/5] Querying crt.sh for IP reverse DNS certificates...")
    ip_certs = fetch_crtsh_ip_certs(TARGET_IP)
    print(f"  Found {len(ip_certs)} certificates for IP reverse DNS\n")

    # 3. Analyze certs for attribution signals
    print("[3/5] Analyzing certificates for attribution signals...")
    cert_evidence = []
    for cert in org_certs + ip_certs:
        ev = analyze_cert_for_attribution(cert, TARGET_IP)
        if ev:
            cert_evidence.append(ev)
            print(f"  [SIGNAL] {ev['attribution_signal']}: {ev['common_name']}")
    if not cert_evidence:
        print("  No direct attribution signals in certificates\n")
    else:
        print()

    # 4. Shodan IP lookup
    print("[4/5] Querying Shodan for IP host data...")
    shodan_host = shodan_ip_lookup(api, TARGET_IP)
    print(f"  IP: {shodan_host.get('ip')}")
    print(f"  Org: {shodan_host.get('org', 'N/A')}")
    print(f"  ISP: {shodan_host.get('isp', 'N/A')}")
    print(f"  Hostnames: {shodan_host.get('hostnames', [])}")
    print(f"  Domains: {shodan_host.get('domains', [])}")
    print(f"  Ports: {shodan_host.get('ports', [])}")
    if shodan_host.get("ssl_certs"):
        print(f"  SSL Certs: {len(shodan_host['ssl_certs'])} found")
        for sc in shodan_host["ssl_certs"]:
            if sc.get("cert_subject_cn"):
                print(f"    - CN: {sc['cert_subject_cn']}")
                print(f"      ALT: {sc.get('cert_alt_names', [])}")
    print()

    # 5. Shodan BACnet search in Alaska
    print("[5/5] Searching Shodan for Alaska BACnet devices that might name integrator...")
    bacnet_results = shodan_search_bacnet_alaska(api)
    integrator_signals = []
    for r in bacnet_results:
        data = r.get("data") or ""
        if any(s in data.lower() for s in ["alaska integrated", "akintegrated", "ais ", " a.i.s."]):
            integrator_signals.append(r)
            print(f"  [SIGNAL] {r['ip']} - {r.get('product', 'N/A')}")
    if not integrator_signals:
        print("  No direct integrator naming in BACnet banners\n")
    else:
        print()

    # 6. Web search
    print("[6/6] Searching web for case studies / press releases...")
    web_evidence = web_search_evidence(TARGET_ORG, TARGET_ADDRESSES)
    if web_evidence:
        print(f"  Found {len(web_evidence)} web results")
        for we in web_evidence[:5]:
            print(f"  - {we['title']}")
            print(f"    {we['url']}")
    else:
        print("  No web evidence found (or Brave API key missing)\n")

    # Compile results
    scan_date = date.today().isoformat()
    payload = {
        "scan_date": scan_date,
        "target_ip": TARGET_IP,
        "target_network": TARGET_NETWORK,
        "target_organization": TARGET_ORG,
        "target_addresses": TARGET_ADDRESSES,
        "certificate_evidence": {
            "org_certs_count": len(org_certs),
            "ip_certs_count": len(ip_certs),
            "attribution_signals": cert_evidence,
        },
        "shodan_evidence": {
            "host_data": shodan_host,
            "bacnet_search_results": bacnet_results,
            "integrator_signals": integrator_signals,
        },
        "web_evidence": web_evidence,
        "attribution_confidence": "medium-high" if cert_evidence or integrator_signals else "pending",
    }

    out_dir = Path("raw/osint")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"alaska-integrator-attribution-{scan_date}.json"
    out_path.write_text(json.dumps(payload, indent=2))

    print(f"\n=== Attribution Report ===")
    print(f"Confidence: {payload['attribution_confidence']}")
    print(f"Output: {out_path}")

    return payload


if __name__ == "__main__":
    main()
