"""
Wiki maintenance script — runs in GitHub Actions daily.

What it does:
  1. Counts wiki pages and raw sources by category
  2. Finds pages updated in the last 7 days
  3. Detects orphan pages (no inbound [[wikilinks]])
  4. Detects broken links (links to non-existent pages)
  5. Suggests missing links (unlinked mentions of page titles)
  6. Updates the stats block in wiki/overview.md
  7. Appends a maintenance entry to wiki/log.md
  8. Regenerates wiki/index.md from page frontmatter
  9. Runs graphify update and structural drift detection
"""

import re
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

WIKI_DIR = Path("wiki")
RAW_DIR = Path("raw")
OVERVIEW = WIKI_DIR / "overview.md"
INDEX = WIKI_DIR / "index.md"
LOG = WIKI_DIR / "log.md"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


# ── Metadata Extraction ───────────────────────────────────────────────────────


def parse_frontmatter(content):
    """Simple parser for YAML-like frontmatter."""
    fm = {}
    m = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if m:
        fm_text = m.group(1)
        for line in fm_text.split("\n"):
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key, val = parts
                    fm[key.strip()] = val.strip()
    return fm


def get_summary(content):
    """Extract first paragraph after the H1 header."""
    content = re.sub(r"^---\n.*?\n---\n", "", content, flags=re.DOTALL)
    content = re.sub(r"^# .*?\n", "", content)
    for line in content.split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            clean = re.sub(r"\[\[(.*?)\]\]", r"\1", line)
            clean = re.sub(r"\*\*(.*?)\*\*", r"\1", clean)
            if len(clean) > 150:
                clean = clean[:147] + "..."
            return clean
    return ""


# ── Counts ────────────────────────────────────────────────────────────────────


def count_wiki_pages():
    pages = [
        p
        for p in WIKI_DIR.rglob("*.md")
        if p.name not in ("index.md", "log.md", "overview.md")
    ]
    by_dir = defaultdict(int)
    for p in pages:
        by_dir[p.parent.name] += 1
    return len(pages), dict(by_dir)


def count_raw_sources():
    sources = list(RAW_DIR.rglob("*.md"))
    by_dir = defaultdict(int)
    for s in sources:
        by_dir[s.parent.name] += 1
    return len(sources), dict(by_dir)


# ── Link Validation ───────────────────────────────────────────────────────────


def find_links_and_orphans():
    """Detects orphans, broken links, and suggested links."""
    all_pages = {}
    for p in WIKI_DIR.rglob("*.md"):
        if p.name in ("index.md", "log.md", "overview.md"):
            continue
        all_pages[p.stem.lower()] = p.relative_to(WIKI_DIR)

    referenced_stems = set()
    broken_links = []

    for p in WIKI_DIR.rglob("*.md"):
        text = p.read_text(encoding="utf-8")
        links = re.findall(r"\[\[([^\]]+)\]\]", text)
        for link in links:
            target = link.split("|")[0]
            target_path = Path(target)
            stem = target_path.stem.lower()
            referenced_stems.add(stem)
            if stem not in all_pages:
                broken_links.append((str(p.relative_to(WIKI_DIR)), link))

    orphans = [
        str(path) for stem, path in all_pages.items() if stem not in referenced_stems
    ]

    suggested = []
    titles_to_check = {
        stem: str(path) for stem, path in all_pages.items() if len(stem) > 5
    }
    for p in WIKI_DIR.rglob("*.md"):
        if p.name in ("index.md", "log.md", "overview.md"):
            continue
        text = p.read_text(encoding="utf-8")
        current_stem = p.stem.lower()
        clean_text = re.sub(r"\[\[.*?\]\]", "", text)
        clean_text = re.sub(r"```.*?```", "", clean_text, flags=re.DOTALL)
        clean_text = re.sub(r"`.*?`", "", clean_text)

        for stem, path in titles_to_check.items():
            if stem == current_stem:
                continue
            if re.search(r"\b" + re.escape(stem) + r"\b", clean_text, re.IGNORECASE):
                suggested.append((str(p.relative_to(WIKI_DIR)), stem))

    return sorted(orphans), sorted(broken_links), sorted(suggested)[:15]


# ── Recently updated pages ────────────────────────────────────────────────────


def recently_updated(days=7):
    recent = []
    cutoff = datetime.now(timezone.utc).date()
    for p in WIKI_DIR.rglob("*.md"):
        if p.name in ("index.md", "log.md", "overview.md"):
            continue
        text = p.read_text(encoding="utf-8")
        m = re.search(r"^updated:\s*(\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
        if m:
            updated = datetime.strptime(m.group(1), "%Y-%m-%d").date()
            if (cutoff - updated).days <= days:
                recent.append((updated.isoformat(), str(p.relative_to(WIKI_DIR))))
    return sorted(recent, reverse=True)


# ── Graphify Maintenance ──────────────────────────────────────────────────────


def graphify_maintenance():
    print("[graphify] Starting graphify maintenance...")
    try:
        if Path("graphify-out/.graphify_python").exists():
            python_bin = Path("graphify-out/.graphify_python").read_text().strip()
        else:
            python_bin = "python3"
        print(f"[graphify] Running cluster-only using {python_bin}...")
        subprocess.run([python_bin, "-m", "graphify", "cluster-only", "."], check=True)
        graph_path = Path("graphify-out/graph.json")
        if graph_path.exists():
            graph_data = json.loads(graph_path.read_text())
            nodes = graph_data.get("nodes", [])
            community_ids = {
                n.get("community") for n in nodes if n.get("community") is not None
            }
            node_count = len(nodes)
            community_count = len(community_ids)
            if node_count > 0:
                fragmentation = community_count / node_count
                if node_count > 20 and fragmentation > 0.5:
                    return fragmentation, True
                return fragmentation, False
    except Exception as e:
        print(f"[graphify] Error: {e}")
    return None, False


# ── Index Regeneration ───────────────────────────────────────────────────────

SECTION_METADATA = {
    "production-systems": (
        "Production Systems",
        "Cameron's FLS production engineering work.",
    ),
    "architectures": (
        "Architectures",
        "Serverless patterns, agent systems, transformer family, retrieval systems.",
    ),
    "techniques": (
        "Techniques",
        "CLIP+FAISS, Whisper pipelines, routing algorithms, MBR decoding, etc.",
    ),
    "integrations": (
        "Integrations",
        "Zendesk API, NetSuite/SuiteQL, AWS, MiCollab, Groq, Copilot Studio.",
    ),
    "papers": ("Papers", "Formal published research summaries."),
    "models": ("Models", ""),
    "benchmarks": ("Benchmarks", ""),
    "datasets": ("Datasets", ""),
    "tools": ("Tools", ""),
    "labs": ("Labs", ""),
    "people": ("People", ""),
    "kaggle": ("Kaggle Competitions", ""),
    "trading": ("Trading", ""),
    "decisions": ("Decisions (ADRs)", "Why Cameron chose approach X over Y."),
    "interview-prep": ("Interview Prep", ""),
    "comparisons": ("Comparisons", ""),
    "open-questions": ("Open Questions", ""),
    "methodology": ("Methodology", "How this wiki system works."),
}


def regenerate_index():
    sections = defaultdict(list)
    for p in WIKI_DIR.rglob("*.md"):
        if p.name in ("index.md", "log.md", "overview.md"):
            continue
        content = p.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        sections[p.parent.name].append(
            {
                "title": fm.get("title", p.stem),
                "path": str(p.relative_to(WIKI_DIR)),
                "summary": get_summary(content),
                "updated": fm.get("updated", ""),
                "status": fm.get("status", ""),
                "visibility": fm.get("visibility", ""),
                "competition": fm.get("competition", ""),
            }
        )
    lines = [
        "# Wiki Index\n",
        "Master catalog of all wiki pages. Updated automatically.\n",
        "\n---\n",
    ]
    for key, val in SECTION_METADATA.items():
        display_name, desc = val
        if key not in sections and key not in ["papers", "datasets", "labs"]:
            continue
        lines.append(f"\n## {display_name}\n")
        if desc:
            lines.append(f"*{desc}*\n")
        lines.append("\n")
        entries = sorted(sections[key], key=lambda x: x["title"])
        if not entries:
            lines.append(
                "| Page | Summary | Updated |\n|------|---------|---------|\n| *(none yet)* | | |\n"
            )
            continue
        if key == "production-systems":
            lines.append(
                "| Page | Summary | Status | Visibility | Updated |\n|------|---------|--------|------------|---------|\n"
            )
            for e in entries:
                lines.append(
                    f"| [{e['title']}]({e['path']}) | {e['summary']} | {e['status']} | {e['visibility']} | {e['updated']} |\n"
                )
        elif key == "kaggle":
            lines.append(
                "| Page | Summary | Competition | Updated |\n|------|---------|-------------|---------|\n"
            )
            for e in entries:
                lines.append(
                    f"| [{e['title']}]({e['path']}) | {e['summary']} | {e['competition'] or e['title']} | {e['updated']} |\n"
                )
        else:
            lines.append("| Page | Summary | Updated |\n|------|---------|---------|\n")
            for e in entries:
                lines.append(
                    f"| [{e['title']}]({e['path']}) | {e['summary']} | {e['updated']} |\n"
                )
    INDEX.write_text("".join(lines), encoding="utf-8")


# ── Overview update ───────────────────────────────────────────────────────────


def update_overview(total_pages, by_dir, total_sources):
    text = OVERVIEW.read_text(encoding="utf-8")
    new_stats = f"- Sources ingested: {total_sources}\n- Wiki pages: {total_pages}\n- Last maintenance: {NOW}\n"
    updated = re.sub(
        r"(## Current knowledge state\n).*?(\n## )",
        lambda m: m.group(1) + "\n" + new_stats + "\n" + m.group(2),
        text,
        flags=re.DOTALL,
    )
    OVERVIEW.write_text(updated, encoding="utf-8")


# ── Log append ────────────────────────────────────────────────────────────────


def append_log(
    total_pages,
    by_dir,
    total_sources,
    recent,
    orphans,
    broken,
    suggested,
    frag_score=None,
    frag_alert=False,
):
    entry_lines = [
        "\n---\n",
        f"## [{TODAY}] maintenance | Automated daily check\n",
        "\n",
        f"Run: {NOW}\n",
        f"Wiki pages: {total_pages} | Raw sources: {total_sources}\n",
    ]
    if frag_score is not None:
        entry_lines.append(
            f"Graph Fragmentation: {frag_score:.3f}{' 🔴 ALERT' if frag_alert else ''}\n"
        )
    entry_lines.append("\n")

    if broken:
        entry_lines.append("Broken Links (🔴 CRITICAL):\n")
        for page, link in broken:
            entry_lines.append(f"  {page}: [[{link}]]\n")
        entry_lines.append("\n")

    if by_dir:
        entry_lines.append("Pages by section:\n")
        for section, count in sorted(by_dir.items()):
            entry_lines.append(f"  {section}: {count}\n")
        entry_lines.append("\n")

    if recent:
        entry_lines.append("Recently updated (last 7 days):\n")
        for date, path in recent[:5]:
            entry_lines.append(f"  [{date}] {path}\n")
        entry_lines.append("\n")

    if orphans:
        entry_lines.append(f"Orphan pages ({len(orphans)}):\n")
        for o in orphans[:10]:
            entry_lines.append(f"  {o}\n")
        entry_lines.append("\n")

    if suggested:
        entry_lines.append("Suggested Links (Unlinked Mentions):\n")
        for page, stem in suggested:
            entry_lines.append(f"  {page}: mention of '{stem}'\n")

    log_text = LOG.read_text(encoding="utf-8")
    LOG.write_text(log_text + "".join(entry_lines), encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Running wiki maintenance — {NOW}")
    total_pages, by_dir = count_wiki_pages()
    total_sources, _ = count_raw_sources()
    recent = recently_updated(days=7)
    orphans, broken, suggested = find_links_and_orphans()

    update_overview(total_pages, by_dir, total_sources)
    frag_score, frag_alert = graphify_maintenance()
    append_log(
        total_pages,
        by_dir,
        total_sources,
        recent,
        orphans,
        broken,
        suggested,
        frag_score,
        frag_alert,
    )
    regenerate_index()
    print("Maintenance complete.")
