import json
from pathlib import Path

import networkx as nx
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent / "templates"


def build_viz(graphml_path: Path, enriched_path: Path, out_dir: Path = None) -> Path:
    """Render a self-contained D3.js HTML visualization from the GraphML file."""
    G = nx.read_graphml(str(graphml_path))

    enriched = json.loads(enriched_path.read_text())
    scan_date = enriched["scan_date"]

    if out_dir is None:
        out_dir = graphml_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    nodes = []
    for node_id, attrs in G.nodes(data=True):
        n = dict(attrs)
        n["id"] = node_id
        nodes.append(n)

    links = []
    for src, tgt, attrs in G.edges(data=True):
        links.append({"source": src, "target": tgt, **attrs})

    total_hosts = sum(
        len(p["hosts"]) for p in enriched["protocols"].values()
    )

    graph_json = json.dumps({"nodes": nodes, "links": links})

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)
    template = env.get_template("viz.html.j2")
    html = template.render(
        scan_date=scan_date,
        graph_json=graph_json,
        total_hosts=total_hosts,
        total_nodes=len(nodes),
        total_edges=len(links),
    )

    out_path = out_dir / f"{scan_date}-viz.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Viz: {len(nodes)} nodes, {len(links)} edges -> {out_path}")
    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("graphml_path", type=Path)
    parser.add_argument("enriched_path", type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()
    build_viz(args.graphml_path, args.enriched_path, args.out_dir)
