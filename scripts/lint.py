#!/usr/bin/env python3
"""
Main Lint Runner for World History Wiki

Implements (and expands) the checks referenced in CLAUDE.md:
- schema_validator
- wikilink_checker (0 broken links required)
- alias_sync
- Empty causes/consequences on events
- Missing Historiography sections (periods + major events)
- Reciprocal biography links (detailed <-> summary)
- Orphan detection (pages with no inbound links)
- caused_by vs preceded_by heuristics (flagging likely temporal misuse)
- Actors/places/processes referenced but missing pages
- Other health checks from the Lint Workflow section

Usage:
  python scripts/lint.py                 # run full suite
  python scripts/lint.py --wikilinks
  python scripts/lint.py --schema
  python scripts/lint.py --biographies

Exit code 0 = clean (or only minor issues)
"""

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import re

SCRIPTS_DIR = Path(__file__).parent
WIKI_ROOT = SCRIPTS_DIR.parent / "wiki"

def run_script(script_name: str, args: list = None) -> int:
    """Run a sub-script and return its exit code."""
    cmd = [sys.executable, str(SCRIPTS_DIR / script_name)]
    if args:
        cmd.extend(args)
    print(f"\n>>> Running {script_name}")
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode

def check_biography_reciprocals() -> int:
    """Check that every detailed bio has a reciprocal link from its actor page."""
    print("\n>>> Checking biography reciprocals (detailed <-> summary)")
    issues = 0

    bio_dir = WIKI_ROOT / "hubs" / "biographies"
    for bio_file in bio_dir.rglob("*.md"):
        if bio_file.name == "biographies-hub.md":
            continue
        try:
            content = bio_file.read_text(encoding="utf-8", errors="ignore")
        except:
            continue

        # Look for actor_page in frontmatter
        import re
        m = re.search(r"actor_page:\s*\"?\[\[([^\]]+)\]\]\"?", content)
        if not m:
            print(f"  WARNING: {bio_file.relative_to(WIKI_ROOT)} missing actor_page field")
            issues += 1
            continue

        actor_link = m.group(1)
        # Resolve the actor file
        actor_slug = actor_link.split("/")[-1].split("|")[0].strip()
        actor_file = None

        # Search for it
        for cand in (WIKI_ROOT / "actors").rglob("*.md"):
            if cand.stem.lower() == actor_slug.lower() or str(cand.relative_to(WIKI_ROOT)).lower().endswith(actor_slug.lower() + ".md"):
                actor_file = cand
                break

        if not actor_file:
            print(f"  BROKEN: {bio_file.relative_to(WIKI_ROOT)} points to non-existent actor [[{actor_link}]]")
            issues += 1
            continue

        actor_content = actor_file.read_text(encoding="utf-8", errors="ignore")
        bio_rel = str(bio_file.relative_to(WIKI_ROOT))
        if bio_rel not in actor_content and bio_file.stem not in actor_content:
            print(f"  MISSING RECIPROCAL: {actor_file.relative_to(WIKI_ROOT)} does not link back to detailed bio")
            issues += 1

    if issues == 0:
        print("  ✓ All biography reciprocal links look good.")
    return issues

def check_empty_causes_consequences() -> int:
    print("\n>>> Checking events for empty causes / consequences")
    issues = 0
    for event in (WIKI_ROOT / "events").rglob("*.md"):
        try:
            content = event.read_text(encoding="utf-8", errors="ignore")
        except:
            continue

        # Very rough check
        if "causes:" in content and ("causes: []" in content or "causes: \n" in content[:500]):
            print(f"  Empty causes: {event.relative_to(WIKI_ROOT)}")
            issues += 1
        if "consequences:" in content and ("consequences: []" in content or "consequences: \n" in content[:500]):
            print(f"  Empty consequences: {event.relative_to(WIKI_ROOT)}")
            issues += 1

    if issues == 0:
        print("  ✓ No empty causes/consequences found in events.")
    return issues

def check_orphan_pages() -> int:
    """Find pages with no inbound wikilinks (basic orphan detection)."""
    print("\n>>> Checking for orphan pages (no inbound links)")
    # Build reverse links
    incoming = defaultdict(set)
    WIKILINK_RE = re.compile(r'\[\[([^\]|#]+)')

    for md in WIKI_ROOT.rglob("*.md"):
        try:
            content = md.read_text(encoding="utf-8", errors="ignore")
        except:
            continue
        rel = str(md.relative_to(WIKI_ROOT))
        for m in WIKILINK_RE.finditer(content):
            target = m.group(1).strip().lower().replace(" ", "-")
            incoming[target].add(rel)

    orphans = []
    for md in WIKI_ROOT.rglob("*.md"):
        rel = str(md.relative_to(WIKI_ROOT))
        base = md.stem.lower().replace(" ", "-")
        if base not in incoming and rel not in incoming and "index" not in rel and "home" not in rel and "log" not in rel:
            # Skip hub roots and very small pages
            if md.stat().st_size > 300:
                orphans.append(rel)

    if orphans:
        print(f"  Found ~{len(orphans)} potential orphans (no inbound links):")
        for o in sorted(orphans)[:15]:
            print(f"    - {o}")
        if len(orphans) > 15:
            print(f"    ... and {len(orphans)-15} more")
    else:
        print("  ✓ No obvious orphan pages found (basic scan).")
    return len(orphans)

def check_caused_by_vs_preceded_by() -> int:
    """Heuristic: flag likely misuse of caused_by where only temporal succession is shown."""
    print("\n>>> Checking for caused_by / preceded_by misuse heuristics")
    issues = 0
    pattern = re.compile(r'caused_by:\s*\[\[([^\]]+)\]\]', re.IGNORECASE)

    for md in WIKI_ROOT.rglob("*.md"):
        try:
            content = md.read_text(encoding="utf-8", errors="ignore")
        except:
            continue

        for m in pattern.finditer(content):
            target = m.group(1)
            # Simple heuristic: if the sentence nearby uses words like "before", "earlier", "preceded", "following the", "after", flag it
            start = max(0, m.start() - 150)
            snippet = content[start:m.end() + 100].lower()
            if any(word in snippet for word in ["before ", "earlier", "preceded by", "following the", "after the", "in ", "during "]):
                rel = str(md.relative_to(WIKI_ROOT))
                print(f"  Potential caused_by/temporal confusion in {rel} → [[{target}]]")
                issues += 1
                break  # one per file to avoid spam

    if issues == 0:
        print("  ✓ No obvious caused_by sequence/causation conflations detected.")
    return issues

def check_missing_historiography() -> int:
    print("\n>>> Checking for missing Historiography sections on periods and major events")
    issues = 0
    for md in list((WIKI_ROOT / "periods").rglob("*.md")) + list((WIKI_ROOT / "events").rglob("*.md")):
        if md.name in ("index.md",):
            continue
        try:
            content = md.read_text(encoding="utf-8", errors="ignore")
        except:
            continue
        if "## Historiography" not in content and "## historiography" not in content:
            # Only flag larger pages or periods
            if md.stat().st_size > 800 or "periods" in str(md):
                print(f"  Missing Historiography: {md.relative_to(WIKI_ROOT)}")
                issues += 1

    if issues == 0:
        print("  ✓ Historiography sections present where expected.")
    return issues

def check_missing_referenced_pages() -> int:
    """Basic scan for actors, places, processes that are linked but have no page."""
    print("\n>>> Checking for missing referenced actors/places/processes (basic)")
    issues = 0
    WIKILINK_RE = re.compile(r'\[\[([^\]|#]+)')

    referenced = {"actors": set(), "places": set(), "processes": set()}
    existing = {"actors": set(), "places": set(), "processes": set()}

    for md in WIKI_ROOT.rglob("*.md"):
        try:
            content = md.read_text(encoding="utf-8", errors="ignore")
            rel = str(md.relative_to(WIKI_ROOT))
        except:
            continue

        for m in WIKILINK_RE.finditer(content):
            tgt = m.group(1).strip().lower().replace(" ", "-")
            if tgt.startswith("actors/") or ("/" not in tgt and "actors" in rel):
                if "actors/" in tgt:
                    referenced["actors"].add(tgt.split("/")[-1])
            if "places/" in tgt:
                referenced["places"].add(tgt.split("/")[-1])
            if "processes/" in tgt:
                referenced["processes"].add(tgt.split("/")[-1])

        # Collect existing
        if "actors/" in rel:
            existing["actors"].add(md.stem.lower())
        if "places/" in rel:
            existing["places"].add(md.stem.lower())
        if "processes/" in rel:
            existing["processes"].add(md.stem.lower())

    for cat in ["actors", "places", "processes"]:
        missing = referenced[cat] - existing[cat]
        if missing:
            print(f"  Missing {cat} pages referenced in links: {len(missing)}")
            for m in list(missing)[:5]:
                print(f"    - {m}")
            issues += len(missing)

    if issues == 0:
        print("  ✓ No obviously missing referenced core pages in this scan.")
    return issues

def main():
    parser = argparse.ArgumentParser(description="Wiki Lint Suite")
    parser.add_argument("--schema", action="store_true", help="Run schema validator only")
    parser.add_argument("--wikilinks", action="store_true", help="Run wikilink checker only")
    parser.add_argument("--aliases", action="store_true", help="Run alias sync/checker only")
    parser.add_argument("--biographies", action="store_true", help="Check biography reciprocals")
    args = parser.parse_args()

    total_issues = 0
    date_str = datetime.now().strftime("%Y-%m-%d")

    print(f"=== World History Wiki Lint Report ({date_str}) ===")

    if args.schema or not any([args.wikilinks, args.aliases, args.biographies]):
        total_issues += run_script("schema_validator.py")

    if args.wikilinks or not any([args.schema, args.aliases, args.biographies]):
        total_issues += run_script("wikilink_checker.py")

    if args.aliases or not any([args.schema, args.wikilinks, args.biographies]):
        total_issues += run_script("alias_sync.py")

    if args.biographies or not any([args.schema, args.wikilinks, args.aliases]):
        total_issues += check_biography_reciprocals()

    # Always run these core checks (from CLAUDE.md Lint Workflow)
    total_issues += check_empty_causes_consequences()
    total_issues += check_biography_reciprocals()
    total_issues += check_orphan_pages()
    total_issues += check_caused_by_vs_preceded_by()
    total_issues += check_missing_historiography()

    # Quick targeted scan for common "mentioned but no page" cases
    total_issues += check_missing_referenced_pages()

    print(f"\n=== Summary ===")
    print(f"Total issue count (approximate): {total_issues}")

    if total_issues == 0:
        print("✓ Lint clean (or only minor issues).")
        # In real use, you might append to log.md here
        return 0
    else:
        print("Some issues found. Fix and re-run.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
