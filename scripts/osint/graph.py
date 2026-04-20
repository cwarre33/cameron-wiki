import json
from pathlib import Path

import networkx as nx

PROTOCOL_COLORS = {
    "modbus": "#e63946",
    "bacnet": "#457b9d",
    "dnp3": "#2a9d8f",
    "s7": "#e9c46a",
}


def build_graph(enriched_path: Path, out_dir: Path = None) -> Path:
    """Build NetworkX directed graph from enriched scan, export as GraphML."""
    data = json.loads(enriched_path.read_text())

    if out_dir is None:
        out_dir = enriched_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    G = nx.DiGraph()
    scan_date = data["scan_date"]

    country_counts: dict[str, int] = {}
    protocol_counts: dict[str, int] = {}
    asn_ip_counts: dict[str, int] = {}
    asn_org: dict[str, str] = {}

    for protocol, proto_data in data["protocols"].items():
        for host in proto_data["hosts"]:
            ip = host.get("ip") or ""
            asn = host.get("asn") or ""
            country = host.get("country") or ""

            if not ip:
                continue

            # ip node
            G.add_node(
                ip,
                node_type="ip",
                org=host.get("org") or "",
                city=host.get("city") or "",
                vuln_count=len(host.get("vulns") or []),
                port=host.get("port") or 0,
                protocol=protocol,
            )

            # protocol node
            if protocol not in G:
                G.add_node(
                    protocol,
                    node_type="protocol",
                    color=PROTOCOL_COLORS.get(protocol, "#888"),
                    exposure_count=0,
                )
            G.nodes[protocol]["exposure_count"] = G.nodes[protocol].get("exposure_count", 0) + 1
            G.add_edge(ip, protocol, edge_type="exposes")
            protocol_counts[protocol] = protocol_counts.get(protocol, 0) + 1

            if asn:
                if asn not in G:
                    G.add_node(asn, node_type="asn", asn_number=asn, org_name=host.get("org") or "", ip_count=0)
                G.nodes[asn]["ip_count"] = G.nodes[asn].get("ip_count", 0) + 1
                G.add_edge(ip, asn, edge_type="belongs_to")
                asn_ip_counts[asn] = asn_ip_counts.get(asn, 0) + 1
                if not asn_org.get(asn):
                    asn_org[asn] = host.get("org") or ""

                if country:
                    if country not in G:
                        G.add_node(country, node_type="country", name=country, total_exposed=0)
                    G.nodes[country]["total_exposed"] = G.nodes[country].get("total_exposed", 0) + 1
                    if not G.has_edge(asn, country):
                        G.add_edge(asn, country, edge_type="located_in")
                    country_counts[country] = country_counts.get(country, 0) + 1

    out_path = out_dir / f"{scan_date}-graph.graphml"
    nx.write_graphml(G, str(out_path))
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"Saved: {out_path}")
    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("enriched_path", type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()
    build_graph(args.enriched_path, args.out_dir)
