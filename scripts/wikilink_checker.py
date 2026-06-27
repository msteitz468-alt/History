#!/usr/bin/env python3
"""
Wikilink Checker for World History Wiki

Finds broken [[links]] in the wiki.

Usage:
  python scripts/wikilink_checker.py              # full wiki scan (default)
  python scripts/wikilink_checker.py --changed    # only links inside files changed vs HEAD
  python scripts/wikilink_checker.py --since main  # only links inside files changed vs a ref
  python scripts/wikilink_checker.py --files a.md b.md
  python scripts/wikilink_checker.py --all         # do not truncate the printed report
  python scripts/wikilink_checker.py --json        # machine-readable output

The page-existence index is ALWAYS built from the full working tree, so `--changed`
answers exactly: "do the files I touched contain broken links?" — i.e. did this
ingest introduce any. CLAUDE.md requires 0 broken links on the pages an ingest adds.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from collections import defaultdict
from typing import Set, List, Tuple, Dict, Optional

WIKI_ROOT = Path(__file__).parent.parent / "wiki"
REPO_ROOT = Path(__file__).parent.parent

# Regex for Obsidian wikilinks: [[target]] or [[target|display]] or [[target#anchor|display]]
WIKILINK_RE = re.compile(r'\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]')

# Known good exceptions (pages that may not exist yet or are intentional placeholders)
# These are skipped during checks, especially useful during ingests.
KNOWN_GOOD_EXCEPTIONS = {
    "unknown", "tbd", "placeholder", "[[unknown]]",
    "master-timeline",  # often referenced conceptually
}

def normalize_slug(name: str) -> str:
    """Normalize a link target to possible filename with good heuristics."""
    name = name.strip().strip('"').strip("'")
    if name.startswith("wiki/"):
        name = name[5:]
    # Handle common punctuation and variants
    name = name.lower()
    name = re.sub(r'[^\w\-/ ]', '', name)  # remove most special chars
    name = name.replace(" ", "-").replace("_", "-")
    name = re.sub(r'-+', '-', name)  # collapse multiple dashes
    name = name.strip('-')
    return name

def extract_aliases(text: str) -> List[str]:
    """Extract aliases from frontmatter (both block list and inline styles)."""
    aliases: List[str] = []
    # block
    m = re.search(r"aliases:\s*\n((?:\s*-\s*.+\n?)+)", text, re.IGNORECASE)
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r"\s*-\s*(.+)", line)
            if mm:
                aliases.append(mm.group(1).strip().strip('"').strip("'"))
    # inline
    mi = re.search(r"aliases:\s*\[([^\]]+)\]", text, re.IGNORECASE)
    if mi:
        for item in re.split(r",\s*", mi.group(1)):
            item = item.strip().strip('"').strip("'")
            if item:
                aliases.append(item)
    return aliases

def build_existing_pages() -> Dict[str, Path]:
    """
    Build mapping of normalized slugs -> actual Path.
    Includes full relative paths and basenames for flexible matching.
    Directory-aware: full path like "events/foo-bar" is preferred.
    Also indexes declared aliases (from frontmatter) as valid link targets.
    """
    pages: Dict[str, Path] = {}
    alias_targets: Dict[str, Path] = {}  # alias_norm -> page
    for md in WIKI_ROOT.rglob("*.md"):
        rel = md.relative_to(WIKI_ROOT)
        # Full relative path without extension, normalized
        full_slug = str(rel.with_suffix("")).lower().replace("\\", "/").replace("_", "-").replace(" ", "-")
        pages[full_slug] = md
        # Basename only
        base = rel.stem.lower().replace("_", "-").replace(" ", "-")
        if base not in pages:  # prefer full path if conflict
            pages[base] = md
        # Also index by directory/basename
        if len(rel.parts) > 1:
            dir_base = f"{rel.parts[0]}/{base}"
            pages[dir_base] = md

        # Index aliases for this page (so [[alias-text]] resolves)
        try:
            content = md.read_text(encoding="utf-8", errors="ignore")
            for a in extract_aliases(content):
                a_norm = normalize_slug(a)
                if a_norm and a_norm not in pages:
                    alias_targets[a_norm] = md
                # Also bare base of alias
                a_base = a_norm.split("/")[-1]
                if a_base and a_base not in pages:
                    alias_targets[a_base] = md
        except:
            pass

    # Merge alias targets (aliases do not override real pages)
    for k, v in alias_targets.items():
        if k not in pages:
            pages[k] = v
    return pages

def find_links_in_file(file_path: Path) -> List[str]:
    """Return list of raw link targets found in the file."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    links = []
    for match in WIKILINK_RE.finditer(content):
        target = match.group(1).strip()
        if target.startswith(("http", "assets/", "file:")):
            continue
        if target.lower() in KNOWN_GOOD_EXCEPTIONS:
            continue
        links.append(target)
    return links

def resolve_link(target: str, existing: Dict[str, Path], source_dir: Optional[str] = None) -> Optional[Path]:
    """Try to resolve a link target against the existing pages map."""
    norm = normalize_slug(target)

    # Direct hits
    if norm in existing:
        return existing[norm]

    # Try with common directory prefixes (directory-aware)
    prefixes = ["actors/", "events/", "processes/", "places/", "concepts/", "periods/", "sources/", "hubs/biographies/", "comparisons/", "controversies/", "timelines/", "hubs/warfare/", ""]
    if source_dir:
        # Boost the directory the source file is in
        prefixes = [f"{source_dir}/"] + [p for p in prefixes if p != f"{source_dir}/"] + prefixes

    for prefix in prefixes:
        cand = (prefix + norm).strip("/")
        if cand in existing:
            return existing[cand]
        # Also try without the prefix if it was a full link
        if norm.startswith(prefix):
            stripped = norm[len(prefix):]
            if stripped in existing:
                return existing[stripped]

    # Last resort: exact basename match across everything
    base = norm.split("/")[-1]
    for key, path in existing.items():
        if key.endswith("/" + base) or key == base:
            return path

    return None

def check_wikilinks(only_files: Optional[Set[Path]] = None,
                    include_sources: bool = False) -> List[Tuple[str, str, str]]:
    """Return list of (source_file, broken_link, suggestion).

    The existence index is always built from the whole wiki. `only_files`, when
    given, restricts which source files are *scanned* for broken links (used by
    --changed / --files). When scanning an explicit subset, source/ pages and the
    index/home/log catalogs are included so nothing the user named is silently
    skipped.
    """
    existing = build_existing_pages()
    broken = []

    scan = sorted(only_files) if only_files is not None else sorted(WIKI_ROOT.rglob("*.md"))
    # `include_sources` (set only by --files) force-scans catalog/source pages the
    # user named explicitly. --changed/--since still skip the append-only catalogs
    # (index/home/log) and source/ index-debt, so they report only real content edits.
    for md_file in scan:
        if not include_sources and md_file.name in ("index.md", "home.md", "log.md"):
            continue
        rel_source = str(md_file.relative_to(WIKI_ROOT))
        if not include_sources and rel_source.startswith("sources/"):
            continue  # source summary pages intentionally index many names ("index debt")
        links = find_links_in_file(md_file)
        source_dir = rel_source.split("/")[0] if "/" in rel_source else None

        for target in links:
            resolved = resolve_link(target, existing, source_dir)
            if not resolved:
                # Try to find a close match for suggestion
                suggestion = suggest_closest(target, existing)
                broken.append((rel_source, target, suggestion or "No matching page found"))

    return broken

def suggest_closest(target: str, existing: Dict[str, Path]) -> Optional[str]:
    """Very basic suggestion: find pages containing key words from the target."""
    norm = normalize_slug(target)
    words = [w for w in norm.split("-") if len(w) > 3]
    if not words:
        return None
    candidates = []
    for key in list(existing.keys())[:500]:  # limit for speed
        if all(w in key for w in words):
            candidates.append(key)
    if candidates:
        return "Did you mean: " + ", ".join(candidates[:3])
    return None

def git_changed_files(since: Optional[str]) -> Set[Path]:
    """Wiki .md files changed vs a baseline (default: working set vs HEAD)."""
    cmds = []
    if since:
        cmds.append(["git", "diff", "--name-only", since, "--", "wiki"])
    else:
        cmds.append(["git", "diff", "--name-only", "HEAD", "--", "wiki"])
        cmds.append(["git", "diff", "--name-only", "--staged", "--", "wiki"])
        cmds.append(["git", "ls-files", "--others", "--exclude-standard", "--", "wiki"])
    out: Set[Path] = set()
    for cmd in cmds:
        try:
            r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=True)
        except Exception:
            continue
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.endswith(".md"):
                p = (REPO_ROOT / line).resolve()
                if p.exists():
                    out.add(p)
    return out


def select_files(args) -> Optional[Set[Path]]:
    """Return the source-file subset to scan, or None for the full wiki."""
    if args.files:
        return {Path(f).resolve() for f in args.files if Path(f).exists()}
    if args.changed or args.since:
        return {p for p in git_changed_files(args.since)
                if WIKI_ROOT.resolve() in p.parents}
    return None


def main():
    ap = argparse.ArgumentParser(description="World History Wiki wikilink checker")
    ap.add_argument("--changed", action="store_true",
                    help="only scan files changed vs HEAD (staged+unstaged+untracked)")
    ap.add_argument("--since", metavar="REF", help="only scan files changed vs a git ref")
    ap.add_argument("--files", nargs="*", help="explicit list of files to scan")
    ap.add_argument("--all", action="store_true", help="print every broken link (no truncation)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    only = select_files(args)
    # Only an explicit --files selection force-includes catalog/source pages.
    broken = check_wikilinks(only_files=only, include_sources=bool(args.files))

    by_source = defaultdict(list)
    for src, link, note in broken:
        by_source[src].append((link, note))

    if args.json:
        print(json.dumps({
            "scope": "changed" if (args.changed or args.since) else "files" if args.files else "wiki",
            "files_scanned": len(only) if only is not None else None,
            "total_broken": len(broken),
            "by_source": {s: [{"link": l, "note": n} for l, n in v] for s, v in by_source.items()},
        }, indent=2))
        return 1 if broken else 0

    scope = "changed files" if (args.changed or args.since) else \
            "selected files" if args.files else "full wiki"
    print(f"=== Wikilink Checker ({scope}) ===")
    if not broken:
        print("✓ 0 broken links found. Good.")
        return 0

    src_limit = None if args.all else 50
    link_limit = None if args.all else 5
    for src in sorted(by_source)[:src_limit]:
        print(f"\n{src}:")
        for link, note in by_source[src][:link_limit]:
            print(f"  →  [[{link}]]  ({note})")
        if link_limit and len(by_source[src]) > link_limit:
            print(f"  ... and {len(by_source[src])-link_limit} more in this file")
    if src_limit and len(by_source) > src_limit:
        print(f"\n... and {len(by_source)-src_limit} more files "
              f"(use --all to print everything, or --changed to scope to your edits)")

    print(f"\nTotal broken links: {len(broken)}")
    if only is None:
        print("Tip: run with --changed to check only the files your ingest touched.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
