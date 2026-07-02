#!/usr/bin/env python3
"""
normalize_frontmatter.py — Fix and normalize YAML frontmatter across the wiki.

Problems addressed (common "yaml front end" issues):
- Inconsistent list syntax (scalar vs [ ] vs block -).
- Unquoted strings containing special characters (: # [ ] etc.) that break parsers / Obsidian Bases.
- Ugly empty scalars (`key: ` instead of `key: ""`).
- sources_ingested used as bare number instead of list (or vice versa).
- Mixed quoting and whitespace.
- Non-canonical key ordering.
- Fragile parse/emit that makes future edits error-prone.

Usage:
  python scripts/normalize_frontmatter.py --dry-run                # report only
  python scripts/normalize_frontmatter.py --fix                    # rewrite in place (creates .bak)
  python scripts/normalize_frontmatter.py --fix --no-backup        # careful!
  python scripts/normalize_frontmatter.py --files wiki/actors/foo.md
  python scripts/normalize_frontmatter.py --type actor --fix
  python scripts/normalize_frontmatter.py --report                 # summary stats

It re-uses the robust (custom, no-PyYAML) parser from schema_validator.py.

After running --fix, re-run:
  python scripts/lint.py --schema
  python scripts/wikilink_checker.py

This is safe for content — it only touches the frontmatter block and preserves the markdown body exactly.
"""

import argparse
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Import the battle-tested parser from the existing validator
sys.path.insert(0, str(Path(__file__).parent))
from schema_validator import (
    parse_frontmatter,
    WIKI_ROOT,
    get_page_type,
    SCHEMAS,
    SKIP_NAMES,
)

REPO_ROOT = Path(__file__).parent.parent


# Fields that should be lists (from schemas + common practice)
LIST_FIELDS = {
    "period", "periods", "region", "regions", "regions_covered",
    "tags", "key_events", "key_processes", "key_sources",
    "actors_primary", "actors_secondary",
    "causes", "consequences",
    "controlled_by", "events_here", "processes_here",
    "affiliated_with", "opposed_by",
    "period_coverage", "region_coverage",
    "positions",  # for controversies
    "sources_ingested",  # normalize to list
}


def needs_quoting(val: str) -> bool:
    """Return True if this scalar needs double quotes for safe YAML."""
    if not val or not isinstance(val, str):
        return False
    val = val.strip()
    if not val:
        return False
    # Starts with special or contains YAML-significant chars
    special = (":", "#", "[", "]", "{", "}", ",", "&", "*", "?", "|", "-", ">", "<",
               "!", "%", "@", "`", '"', "'", "\n", "\r")
    if any(c in val for c in special):
        return True
    if val[0] in (" ", "\t", "#", "-", ":", ">", "|", "&", "*", "?", "!", "%", "@", "`", '"', "'"):
        return True
    # Looks like a number or bool but we want it as string sometimes (e.g. years with context)
    return False


def quote(val: str) -> str:
    if not isinstance(val, str):
        val = str(val)
    if not needs_quoting(val):
        return val
    # Escape inner double quotes
    escaped = val.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def normalize_value(key: str, val: Any, ptype: str) -> Any:
    """Return a normalized Python value for emission."""
    if val is None:
        return ""

    # Lists
    if key in LIST_FIELDS or (isinstance(val, (list, tuple))):
        if isinstance(val, (list, tuple)):
            items = [str(x).strip() for x in val if str(x).strip()]
            return items
        # scalar -> list (common for sources_ingested: 5 or single string)
        s = str(val).strip()
        if s:
            # If it was a bare count, keep as single-item list so it's an array
            # Users can later expand with actual source slugs.
            return [s]
        return []

    # Scalars
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        # Keep numbers for counts/dates when they make sense
        return val
    s = str(val).strip()
    if not s:
        return ""
    # Clean obvious empty markers
    if s.lower() in ("none", "null", "n/a", "unknown"):
        return "unknown" if key in {"date_start", "date_end", "causes", "consequences"} else ""
    return s


def canonical_key_order(ptype: str) -> List[str]:
    """Return preferred key order for this page type (stable + human readable)."""
    base = ["title"]
    schema_req = SCHEMAS.get(ptype, {}).get("required", [])
    # Put required first in schema order, then common others
    order = []
    seen = set()
    for k in base + schema_req:
        if k not in seen:
            order.append(k)
            seen.add(k)

    # Common nice-to-haves after required
    extras = ["actor_type", "place_type", "concept_type", "event_type", "process_type",
              "dispute_type", "source_type", "analysis_type",
              "date_start", "date_end", "date_birth", "date_death", "date_precision",
              "period", "region", "location",
              "tags", "last_updated", "ingested"]
    for k in extras:
        if k not in seen:
            order.append(k)
            seen.add(k)
    return order


def dump_frontmatter(data: Dict[str, Any], ptype: str) -> str:
    """Emit clean, Obsidian-Bases-friendly, quoted YAML frontmatter."""
    if not data:
        return ""

    # Normalize values
    norm: Dict[str, Any] = {}
    for k, v in data.items():
        norm[k] = normalize_value(k, v, ptype)

    # Order keys
    ordered_keys = []
    for k in canonical_key_order(ptype):
        if k in norm:
            ordered_keys.append(k)
    # Append any extra keys that existed (preserve data)
    for k in sorted(norm.keys()):
        if k not in ordered_keys:
            ordered_keys.append(k)

    lines = []
    for k in ordered_keys:
        v = norm[k]
        if v == "" or v is None or v == []:
            lines.append(f'{k}: ""')
            continue

        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
                continue
            # Inline list, quoted items
            items = ", ".join(quote(str(item)) for item in v)
            lines.append(f"{k}: [{items}]")
            continue

        if isinstance(v, bool):
            lines.append(f"{k}: {str(v).lower()}")
            continue

        if isinstance(v, (int, float)):
            lines.append(f"{k}: {v}")
            continue

        # Scalar string
        lines.append(f"{k}: {quote(str(v))}")

    return "\n".join(lines)


def rewrite_file(path: Path, dry_run: bool = True, backup: bool = True) -> Dict[str, Any]:
    """Rewrite one file's frontmatter. Returns report dict."""
    try:
        rel = path.relative_to(WIKI_ROOT)
    except ValueError:
        rel = path  # outside wiki (e.g. test copy)
    report = {"file": str(rel), "changed": False, "errors": []}
    try:
        original = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        report["errors"].append(f"read error: {e}")
        return report

    if not original.startswith("---"):
        report["errors"].append("no frontmatter")
        return report

    m = re.match(r"^(---\s*\n.*?\n---\s*\n)(.*)$", original, re.DOTALL)
    if not m:
        report["errors"].append("could not split frontmatter/body")
        return report

    fm_block, body = m.groups()
    fm = parse_frontmatter(original)
    try:
        ptype = get_page_type(path)
    except Exception:
        ptype = "unknown"
    if ptype == "unknown":
        # Try to guess from path for test files etc.
        if "actors" in str(path):
            ptype = "actor"
        else:
            return report

    new_fm_text = dump_frontmatter(fm, ptype)
    new_block = f"---\n{new_fm_text}\n---\n"

    if dry_run:
        looks_different = new_fm_text.strip() != fm_block.split("\n---", 1)[0].replace("---\n", "", 1).strip()
        if looks_different:
            report["changed"] = True
            report["would_change"] = True
        return report

    # --fix: always apply clean style
    report["changed"] = True
    if backup:
        bak = path.with_suffix(path.suffix + ".bak")
        if not bak.exists():
            shutil.copy2(path, bak)

    new_content = new_block + body
    path.write_text(new_content, encoding="utf-8")
    return report


def main():
    ap = argparse.ArgumentParser(description="Normalize/fix YAML frontmatter in the wiki")
    ap.add_argument("--fix", action="store_true", help="Actually rewrite files (default is dry-run)")
    ap.add_argument("--no-backup", action="store_true", help="Do not create .bak files when fixing")
    ap.add_argument("--files", nargs="*", help="Specific files to process")
    ap.add_argument("--type", choices=["period", "event", "actor", "process", "place",
                                       "concept", "controversy", "source", "biography"],
                    help="Only process one page type")
    ap.add_argument("--report", action="store_true", help="Just print a summary report")
    args = ap.parse_args()

    dry_run = not args.fix
    backup = not args.no_backup

    if args.files:
        files = [Path(f).resolve() for f in args.files if Path(f).exists()]
    else:
        files = [p for p in WIKI_ROOT.rglob("*.md") if p.name not in SKIP_NAMES]

    if args.type:
        def _safe_ptype(p):
            try:
                return get_page_type(p)
            except Exception:
                pstr = str(p)
                if "actors" in pstr: return "actor"
                if "events" in pstr: return "event"
                return "unknown"
        files = [p for p in files if _safe_ptype(p) == args.type]

    stats = defaultdict(int)
    changed_files = []
    errors = []

    print(f"{'DRY-RUN' if dry_run else 'FIXING'} frontmatter on {len(files)} files...")

    for f in files:
        res = rewrite_file(f, dry_run=dry_run, backup=backup)
        try:
            ptype = get_page_type(f)
        except Exception:
            pstr = str(f)
            if "actors" in pstr: ptype = "actor"
            elif "events" in pstr: ptype = "event"
            else: ptype = "unknown"
        stats[ptype] += 1
        if res.get("changed"):
            changed_files.append(res["file"])
        if res.get("errors"):
            errors.extend([f"{res['file']}: {e}" for e in res["errors"]])

    print("\n=== Summary ===")
    print(f"Files examined: {len(files)}")
    print(f"Files that would change / changed: {len(changed_files)}")
    if changed_files:
        print("Changed (or would change):")
        for c in sorted(changed_files)[:20]:
            print(f"  {c}")
        if len(changed_files) > 20:
            print(f"  ... and {len(changed_files)-20} more")

    if errors:
        print("\nErrors:")
        for e in errors[:10]:
            print(f"  {e}")

    if args.report:
        print("\nPer type counts:")
        for t, c in sorted(stats.items()):
            print(f"  {t}: {c}")

    if not dry_run and changed_files:
        print("\nDone. Remember to run:")
        print("  python scripts/schema_validator.py --files " + " ".join(changed_files[:5]) + " ...")
        print("  python scripts/lint.py --schema")

    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
