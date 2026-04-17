"""
Wiki maintenance script — runs in GitHub Actions daily.

What it does:
  1. Counts wiki pages and raw sources by category
  2. Finds pages updated in the last 7 days
  3. Detects orphan pages (no inbound [[wikilinks]])
  4. Updates the stats block in wiki/overview.md
  5. Appends a maintenance entry to wiki/log.md
  6. Regenerates wiki/index.md from page frontmatter
  7. Runs graphify update and structural drift detection
"""

import os
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
    # Strip frontmatter
    content = re.sub(r"^---\n.*?\n---\n", "", content, flags=re.DOTALL)
    # Find first # Header
    content = re.sub(r"^# .*?\n", "", content)
    # Get first non-empty paragraph
    for line in content.split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            # Remove existing wikilinks and formatting for a clean summary
            clean = re.sub(r"\[\[(.*?)\]\]", r"\1", line)
            clean = re.sub(r"\*\*(.*?)\*\*", r"\1", clean)
            # Truncate if too long
            if len(clean) > 150:
                clean = clean[:147] + "..."
            return clean
    return ""


# ── Counts ────────────────────────────────────────────────────────────────────

def count_wiki_pages():
    pages = [p for p in WIKI_DIR.rglob("*.md") if p.name not in ("index.md", "log.md", "overview.md")]
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


# ── Recently updated pages ────────────────────────────────────────────────────

def recently_updated(days=7):
    """Pages whose 'updated' frontmatter field is within the last N days."""
    recent = []
    cutoff = datetime.now(timezone.utc).date()
    for p in WIKI_DIR.rglob("*.md"):
        if p.name in ("index.md", "log.md", "overview.md"):
            continue
        text = p.read_text(encoding="utf-8")
        m = re.search(r"^updated:\s*(\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
        if m:
            updated = datetime.strptime(m.group(1), "%Y-%m-%d").date()
            delta = (cutoff - updated).days
            if delta <= days:
                rel = str(p.relative_to(WIKI_DIR))
                recent.append((updated.isoformat(), rel))
    return sorted(recent, reverse=True)


# ── Orphan detection ──────────────────────────────────────────────────────────

def find_orphans():
    """Pages that are never referenced by a [[wikilink]] in any other page."""
    all_pages = {
        p.stem: p.relative_to(WIKI_DIR)
        for p in WIKI_DIR.rglob("*.md")
        if p.name not in ("index.md", "log.md", "overview.md")
    }
    referenced = set()
    for p in WIKI_DIR.rglob("*.md"):
        text = p.read_text(encoding="utf-8")
        for link in re.findall(r"\[\[([^\]]+)\]\]", text):
            # Normalize: strip path, strip .md, lowercase
            stem = Path(link.split("|")[0]).stem.lower()
            referenced.add(stem)

    orphans = [
        str(path) for stem, path in all_pages.items()
        if stem.lower() not in referenced
    ]
    return sorted(orphans)


# ── Graphify Maintenance ──────────────────────────────────────────────────────

def graphify_maintenance():
    """Runs graphify update and checks for structural drift."""
    print("[graphify] Starting graphify maintenance...")
    
    try:
        if Path("graphify-out/.graphify_python").exists():
            python_bin = Path("graphify-out/.graphify_python").read_text().strip()
        else:
            python_bin = "python3"
            
        # 2. Run graphify cluster-only (re-calculates communities/cohesion)
        print(f"[graphify] Running cluster-only using {python_bin}...")
        subprocess.run([python_bin, "-m", "graphify", "cluster-only", "."], check=True)
        
        # 3. Structural drift detection
        graph_path = Path("graphify-out/graph.json")
        if graph_path.exists():
            graph_data = json.loads(graph_path.read_text())
            
            # Nodes vs Communities
            nodes = graph_data.get("nodes", [])
            community_ids = {n.get("community") for n in nodes if n.get("community") is not None}
            
            node_count = len(nodes)
            community_count = len(community_ids)
            
            if node_count > 0:
                fragmentation = community_count / node_count
                print(f"[graphify] Nodes: {node_count}, Communities: {community_count}")
                print(f"[graphify] Fragmentation score: {fragmentation:.3f}")
                
                # Alert threshold: e.g., if more than 50% of nodes are in their own communities
                # for a non-trivial graph.
                if node_count > 20 and fragmentation > 0.5:
                    print(f"🔴 ALERT: High graph fragmentation detected ({fragmentation:.3f})")
                    print("Suggest adding more cross-links between wiki pages.")
                    return fragmentation, True
                return fragmentation, False
    except Exception as e:
        print(f"[graphify] Error during maintenance: {e}")
        
    return None, False


# ── Index Regeneration ───────────────────────────────────────────────────────

SECTION_METADATA = {
    "production-systems": ("Production Systems", "Cameron's FLS production engineering work."),
    "architectures": ("Architectures", "Serverless patterns, agent systems, transformer family, retrieval systems."),
    "techniques": ("Techniques", "CLIP+FAISS, Whisper pipelines, routing algorithms, MBR decoding, etc."),
    "integrations": ("Integrations", "Zendesk API, NetSuite/SuiteQL, AWS, MiCollab, Groq, Copilot Studio."),
    "papers": ("Papers", "Formal published research summaries."),
    "models": ("Models", ""),
    "benchmarks": ("Benchmarks", ""),
    "datasets": ("Datasets", ""),
    "tools": ("Tools", ""),
    "labs": ("Labs", ""),
    "people": ("People", ""),
    "kaggle": ("Kaggle Competitions", ""),
    "trading": ("Trading", ""),
    "decisions": ("Decisions (ADRs)", "Why Cameron chose approach X over Y. Interview-ready architectural reasoning."),
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
        summary = get_summary(content)
        
        rel_path = str(p.relative_to(WIKI_DIR))
        title = fm.get("title", p.stem)
        updated = fm.get("updated", "")
        status = fm.get("status", "")
        visibility = fm.get("visibility", "")
        competition = fm.get("competition", "")
        
        entry = {
            "title": title,
            "path": rel_path,
            "summary": summary,
            "updated": updated,
            "status": status,
            "visibility": visibility,
            "competition": competition
        }
        
        section_key = p.parent.name
        sections[section_key].append(entry)

    # Build index content
    lines = [
        "# Wiki Index\n",
        "Master catalog of all wiki pages. Updated automatically.\n",
        "\n---\n"
    ]
    
    # Sort sections by the order in SECTION_METADATA
    for key in SECTION_METADATA:
        if key not in sections and key not in ["papers", "datasets", "labs"]:
            continue
            
        display_name, desc = SECTION_METADATA[key]
        lines.append(f"\n## {display_name}\n")
        if desc:
            lines.append(f"*{desc}*\n")
        lines.append("\n")
        
        entries = sorted(sections[key], key=lambda x: x["title"])
        
        if not entries:
            lines.append("| Page | Summary | Updated |\n")
            lines.append("|------|---------|---------|\n")
            lines.append("| *(none yet)* | | |\n")
            continue

        if key == "production-systems":
            lines.append("| Page | Summary | Status | Visibility | Updated |\n")
            lines.append("|------|---------|--------|------------|---------|\n")
            for e in entries:
                lines.append(f"| [{e['title']}]({e['path']}) | {e['summary']} | {e['status']} | {e['visibility']} | {e['updated']} |\n")
        elif key == "kaggle":
            lines.append("| Page | Summary | Competition | Updated |\n")
            lines.append("|------|---------|-------------|---------|\n")
            for e in entries:
                comp = e['competition'] or e['title']
                lines.append(f"| [{e['title']}]({e['path']}) | {e['summary']} | {comp} | {e['updated']} |\n")
        else:
            lines.append("| Page | Summary | Updated |\n")
            lines.append("|------|---------|---------|\n")
            for e in entries:
                lines.append(f"| [{e['title']}]({e['path']}) | {e['summary']} | {e['updated']} |\n")

    INDEX.write_text("".join(lines), encoding="utf-8")
    print(f"[index] Regenerated {INDEX}")


# ── Overview update ───────────────────────────────────────────────────────────

def update_overview(total_pages, by_dir, total_sources):
    text = OVERVIEW.read_text(encoding="utf-8")

    new_stats = (
        f"- Sources ingested: {total_sources}\n"
        f"- Wiki pages: {total_pages}\n"
        f"- Last maintenance: {NOW}\n"
    )

    updated = re.sub(
        r"(## Current knowledge state\n).*?(\n## )",
        lambda m: m.group(1) + "\n" + new_stats + "\n" + m.group(2),
        text,
        flags=re.DOTALL,
    )

    if updated != text:
        OVERVIEW.write_text(updated, encoding="utf-8")
        print(f"[overview] Updated stats: {total_pages} pages, {total_sources} sources")
    else:
        print("[overview] No stats change detected")


# ── Log append ────────────────────────────────────────────────────────────────

def append_log(total_pages, by_dir, total_sources, recent, orphans, frag_score=None, frag_alert=False):
    entry_lines = [
        f"\n---\n",
        f"## [{TODAY}] maintenance | Automated daily check\n",
        f"\n",
        f"Run: {NOW}\n",
        f"Wiki pages: {total_pages} | Raw sources: {total_sources}\n",
    ]
    
    if frag_score is not None:
        alert_str = " 🔴 ALERT" if frag_alert else ""
        entry_lines.append(f"Graph Fragmentation: {frag_score:.3f}{alert_str}\n")
    
    entry_lines.append("\n")

    if by_dir:
        entry_lines.append("Pages by section:\n")
        for section, count in sorted(by_dir.items()):
            entry_lines.append(f"  {section}: {count}\n")
        entry_lines.append("\n")

    if recent:
        entry_lines.append(f"Recently updated (last 7 days):\n")
        for date, path in recent[:5]:
            entry_lines.append(f"  [{date}] {path}\n")
        entry_lines.append("\n")

    if orphans:
        entry_lines.append(f"Orphan pages ({len(orphans)} — no inbound wikilinks):\n")
        for o in orphans[:10]:
            entry_lines.append(f"  {o}\n")
    else:
        entry_lines.append("Orphan pages: none\n")

    log_text = LOG.read_text(encoding="utf-8")
    LOG.write_text(log_text + "".join(entry_lines), encoding="utf-8")
    print(f"[log] Appended maintenance entry for {TODAY}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Running wiki maintenance — {NOW}")

    total_pages, by_dir = count_wiki_pages()
    total_sources, _ = count_raw_sources()
    recent = recently_updated(days=7)
    orphans = find_orphans()

    print(f"  Pages: {total_pages} | Sources: {total_sources}")
    print(f"  Recently updated: {len(recent)} | Orphans: {len(orphans)}")

    update_overview(total_pages, by_dir, total_sources)
    
    frag_score, frag_alert = graphify_maintenance()
    append_log(total_pages, by_dir, total_sources, recent, orphans, frag_score, frag_alert)
    regenerate_index()

    print("Maintenance complete.")
