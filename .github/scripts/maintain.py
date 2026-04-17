"""
Wiki maintenance script — runs in GitHub Actions daily.

What it does:
  1. Counts wiki pages and raw sources by category
  2. Finds pages updated in the last 7 days
  3. Detects orphan pages (no inbound [[wikilinks]])
  4. Updates the stats block in wiki/overview.md
  5. Appends a maintenance entry to wiki/log.md
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

WIKI_DIR = Path("wiki")
RAW_DIR = Path("raw")
OVERVIEW = WIKI_DIR / "overview.md"
LOG = WIKI_DIR / "log.md"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


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
            stem = Path(link).stem.lower()
            referenced.add(stem)

    orphans = [
        str(path) for stem, path in all_pages.items()
        if stem.lower() not in referenced
    ]
    return sorted(orphans)


# ── Overview update ───────────────────────────────────────────────────────────

def update_overview(total_pages, by_dir, total_sources):
    text = OVERVIEW.read_text(encoding="utf-8")

    new_stats = (
        f"- Sources ingested: {total_sources}\n"
        f"- Wiki pages: {total_pages}\n"
        f"- Last maintenance: {NOW}\n"
    )

    # Replace the stats block between "## Current knowledge state" and the next "##"
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

def append_log(total_pages, by_dir, total_sources, recent, orphans):
    entry_lines = [
        f"\n---\n",
        f"## [{TODAY}] maintenance | Automated daily check\n",
        f"\n",
        f"Run: {NOW}\n",
        f"Wiki pages: {total_pages} | Raw sources: {total_sources}\n",
        f"\n",
    ]

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
    append_log(total_pages, by_dir, total_sources, recent, orphans)

    print("Maintenance complete.")
