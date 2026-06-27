#!/usr/bin/env python3
"""
Basic Alias Sync / Checker for World History Wiki

Obsidian-style aliases are often stored as:
aliases:
  - Foo Bar
  - Another Name

This script:
- Extracts aliases from frontmatter
- Reports pages that have aliases
- Can be extended to generate a redirects map or check for alias collisions.

Run: python scripts/alias_sync.py
"""

import re
from pathlib import Path
from typing import Dict, List

WIKI_ROOT = Path(__file__).parent.parent / "wiki"

def extract_aliases(text: str) -> List[str]:
    """Extract aliases list from frontmatter if present.
    Supports both:
      aliases:
        - Foo
        - Bar
    and inline:
      aliases: [Foo, Bar, "Baz Quux"]
    """
    aliases = []
    # Block list style
    match = re.search(r"aliases:\s*\n((?:\s*-\s*.+\n?)+)", text, re.IGNORECASE)
    if match:
        for line in match.group(1).splitlines():
            m = re.match(r"\s*-\s*(.+)", line)
            if m:
                aliases.append(m.group(1).strip().strip('"').strip("'"))
    # Inline array style: aliases: [A, B, "C D"]
    inline = re.search(r"aliases:\s*\[([^\]]+)\]", text, re.IGNORECASE)
    if inline:
        for item in re.split(r",\s*", inline.group(1)):
            item = item.strip().strip('"').strip("'")
            if item:
                aliases.append(item)
    # Dedup preserve order
    seen = set()
    out = []
    for a in aliases:
        if a.lower() not in seen:
            seen.add(a.lower())
            out.append(a)
    return out

def main():
    print("=== Alias Sync / Checker ===")
    alias_map: Dict[str, List[str]] = {}

    for md in WIKI_ROOT.rglob("*.md"):
        try:
            content = md.read_text(encoding="utf-8", errors="ignore")
        except:
            continue

        aliases = extract_aliases(content)
        if aliases:
            rel = str(md.relative_to(WIKI_ROOT))
            alias_map[rel] = aliases

    if not alias_map:
        print("No alias declarations found in frontmatter.")
        return 0

    print(f"Found {len(alias_map)} pages declaring aliases:\n")
    for page, alist in sorted(alias_map.items())[:30]:
        print(f"  {page}")
        for a in alist:
            print(f"    - {a}")

    if len(alias_map) > 30:
        print(f"  ... and {len(alias_map)-30} more pages")

    print("\n(Note: Full alias collision detection and redirect generation can be added here.)")
    return 0

if __name__ == "__main__":
    exit(main())
