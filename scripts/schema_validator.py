#!/usr/bin/env python3
"""
Schema Validator for World History Wiki

Validates frontmatter against the page-type schemas defined in CLAUDE.md.

Usage:
  python scripts/schema_validator.py                 # validate the whole wiki
  python scripts/schema_validator.py --changed       # only files changed vs HEAD (+ staged + untracked)
  python scripts/schema_validator.py --since main     # only files changed vs a git ref
  python scripts/schema_validator.py --files a.md b.md
  python scripts/schema_validator.py --strict         # warnings also fail the run
  python scripts/schema_validator.py --json           # machine-readable output

Exit code 0 = no ERRORS (warnings allowed unless --strict). 1 = errors present.

Notes
-----
* The frontmatter parser understands inline lists (`k: [a, b]`), block lists
  (`k:` then `  - a`), and block scalars (`k: >` / `k: |`). It does NOT require
  PyYAML.
* Findings are split into ERROR (schema violations) and WARN (advisory, e.g.
  weak collection coverage). Only errors fail the run by default.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

WIKI_ROOT = Path(__file__).parent.parent / "wiki"
REPO_ROOT = Path(__file__).parent.parent

# Required fields per page type. These mirror the CLAUDE.md page-type schemas.
#   - "required": fields that must be present and non-empty (ERROR if missing)
#   - "directory"/"directory_pattern": how the type is detected from the path
SCHEMAS: Dict[str, Dict[str, Any]] = {
    "period": {
        "required": ["title", "period_number", "date_range", "regions_covered",
                     "collection_coverage", "sources_ingested", "last_updated", "tags"],
        "directory": "periods",
    },
    "event": {
        "required": ["title", "date_start", "date_end", "date_precision", "period",
                     "region", "causes", "consequences", "sources_ingested",
                     "last_updated", "tags"],
        "directory": "events",
    },
    "actor": {
        "required": ["title", "actor_type", "date_start", "date_end", "period",
                     "region", "sources_ingested", "last_updated", "tags"],
        "directory": "actors",
    },
    "process": {
        "required": ["title", "date_start", "date_end", "date_precision", "period",
                     "region", "process_type", "sources_ingested", "last_updated", "tags"],
        "directory": "processes",
    },
    "place": {
        "required": ["title", "place_type", "period_active", "sources_ingested",
                     "last_updated", "tags"],
        "directory": "places",
    },
    "concept": {
        "required": ["title", "concept_type", "sources_ingested", "last_updated", "tags"],
        "directory": "concepts",
    },
    "controversy": {
        "required": ["title", "dispute_type", "period_involved", "regions_involved",
                     "resolution_status", "last_updated", "tags"],
        "directory": "controversies",
    },
    # FIX (skill-obs #15): source pages use the CLAUDE.md source schema — `ingested`,
    # `pages_created`, `pages_updated` — NOT the actor/event fields `sources_ingested`/
    # `last_updated`. The old schema demanded the wrong fields and falsely flagged
    # every source page in the wiki.
    "source": {
        "required": ["title", "author", "year", "source_type", "period_coverage",
                     "region_coverage", "methodological_approach", "pages_created",
                     "ingested", "tags"],
        "directory": "sources",
    },
    "biography": {
        "required": ["title", "analysis_type", "actor_page", "period", "date_birth",
                     "date_death", "region", "key_sources", "scale", "last_updated", "tags"],
        "directory_pattern": "hubs/biographies",
    },
}

# Files that are catalogs / logs, not schema'd content pages.
SKIP_NAMES = {"index.md", "home.md", "log.md", "overview.md", "master-timeline.md"}


# --------------------------------------------------------------------------- #
# Frontmatter parsing (no PyYAML dependency)
# --------------------------------------------------------------------------- #
def parse_frontmatter(text: str) -> Dict[str, Any]:
    """Parse YAML-ish frontmatter into a dict.

    Handles inline lists, block lists, and block scalars (`>` / `|`). Values are
    returned as strings, lists, or bools. Empty/blank values become "".
    """
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    lines = m.group(1).splitlines()
    data: Dict[str, Any] = {}
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        km = re.match(r"^(\s*)([\w\-]+):\s?(.*)$", line)
        if not km:
            i += 1
            continue
        indent, key, val = len(km.group(1)), km.group(2), km.group(3).strip()

        # Block scalar: `key: >` or `key: |`
        if val in (">", "|", ">-", "|-", ">+", "|+"):
            block: List[str] = []
            i += 1
            while i < n and (not lines[i].strip() or _indent_of(lines[i]) > indent):
                block.append(lines[i].strip())
                i += 1
            data[key] = " ".join(b for b in block if b).strip()
            continue

        # Inline list: `key: [a, b, c]`
        if val.startswith("[") and val.endswith("]"):
            data[key] = _split_inline_list(val[1:-1])
            i += 1
            continue

        # Block list: `key:` followed by indented `- item` lines
        if val == "":
            j = i + 1
            items: List[str] = []
            while j < n:
                lm = re.match(r"^(\s*)-\s+(.*)$", lines[j])
                if lm and _indent_of(lines[j]) > indent:
                    items.append(lm.group(2).strip().strip('"').strip("'"))
                    j += 1
                elif not lines[j].strip():
                    j += 1
                else:
                    break
            if items:
                data[key] = items
                i = j
                continue
            data[key] = ""
            i += 1
            continue

        # Scalar
        if val.lower() in ("true", "false"):
            data[key] = val.lower() == "true"
        else:
            data[key] = val.strip('"').strip("'")
        i += 1
    return data


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _split_inline_list(body: str) -> List[str]:
    """Split an inline list body on top-level commas (ignores commas inside [[ ]])."""
    items, depth, cur = [], 0, ""
    for ch in body:
        if ch == "[":
            depth += 1
            cur += ch
        elif ch == "]":
            depth -= 1
            cur += ch
        elif ch == "," and depth <= 0:
            items.append(cur.strip().strip('"').strip("'"))
            cur = ""
        else:
            cur += ch
    if cur.strip():
        items.append(cur.strip().strip('"').strip("'"))
    return [x for x in items if x]


def _is_empty(v: Any) -> bool:
    return v is None or v == "" or v == [] or v == {}


# --------------------------------------------------------------------------- #
# Page typing + validation
# --------------------------------------------------------------------------- #
def get_page_type(file_path: Path) -> str:
    rel = file_path.relative_to(WIKI_ROOT)
    parts = rel.parts
    if "hubs" in parts and "biographies" in parts:
        # Templates and the hub portal page are not schema'd biographies.
        if "templates" in parts or rel.name == "biographies-hub.md":
            return "unknown"
        return "biography"
    first = parts[0]
    by_dir = {
        "periods": "period", "events": "event", "actors": "actor",
        "processes": "process", "places": "place", "concepts": "concept",
        "controversies": "controversy", "sources": "source",
    }
    return by_dir.get(first, "unknown")


def validate_file(file_path: Path) -> Dict[str, List[str]]:
    """Return {'errors': [...], 'warnings': [...]} for one file."""
    out = {"errors": [], "warnings": []}
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        out["errors"].append(f"Cannot read: {e}")
        return out

    ptype = get_page_type(file_path)
    if ptype == "unknown":
        return out

    fm = parse_frontmatter(content)
    if not fm:
        out["errors"].append("Missing or unparseable YAML frontmatter")
        return out

    for field in SCHEMAS.get(ptype, {}).get("required", []):
        if field not in fm or _is_empty(fm[field]):
            out["errors"].append(f"Missing or empty required field: {field}")

    if ptype == "event":
        if _is_empty(fm.get("causes")):
            out["errors"].append("Event has empty 'causes' (use [[unknown]] if genuinely unclear)")
        if _is_empty(fm.get("consequences")):
            out["errors"].append("Event has empty 'consequences' (use [[unknown]] if genuinely unclear)")

    # Historiography section required on period + event pages.
    if ptype in ("period", "event") and not re.search(r"^#+\s+Historiography", content, re.MULTILINE):
        out["errors"].append("Missing ## Historiography section")

    # Advisory: weak coverage is a real signal but not a schema violation.
    if ptype == "period":
        cov = fm.get("collection_coverage", "")
        if cov in ("weak", "absent"):
            out["warnings"].append(f"collection_coverage is '{cov}' (flag the gap on the page)")

    # Advisory: bio should be discoverable via a reciprocal actor_page.
    if ptype == "biography" and not _is_empty(fm.get("actor_page")):
        out["warnings"].append(
            "verify reciprocal link exists on the actor_page summary"
        ) if "actor_page" not in content else None
        out["warnings"] = [w for w in out["warnings"] if w]

    return out


# --------------------------------------------------------------------------- #
# File selection (whole wiki / changed / since ref / explicit list)
# --------------------------------------------------------------------------- #
def git_changed_files(since: Optional[str]) -> List[Path]:
    """Wiki .md files that differ from a baseline.

    --since REF : everything changed vs REF (committed diff).
    default     : staged + unstaged + untracked vs HEAD (your working set).
    """
    cmds = []
    if since:
        cmds.append(["git", "diff", "--name-only", f"{since}", "--", "wiki"])
    else:
        cmds.append(["git", "diff", "--name-only", "HEAD", "--", "wiki"])
        cmds.append(["git", "diff", "--name-only", "--staged", "--", "wiki"])
        cmds.append(["git", "ls-files", "--others", "--exclude-standard", "--", "wiki"])
    seen = set()
    for cmd in cmds:
        try:
            r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=True)
        except Exception:
            continue
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.endswith(".md"):
                seen.add((REPO_ROOT / line).resolve())
    return [p for p in sorted(seen) if p.exists()]


def select_files(args) -> List[Path]:
    if args.files:
        return [Path(f).resolve() for f in args.files if Path(f).exists()]
    if args.changed or args.since:
        return [p for p in git_changed_files(args.since)
                if WIKI_ROOT.resolve() in p.parents and p.name not in SKIP_NAMES]
    return [p for p in WIKI_ROOT.rglob("*.md") if p.name not in SKIP_NAMES]


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="World History Wiki schema validator")
    ap.add_argument("--changed", action="store_true",
                    help="only files changed vs HEAD (staged+unstaged+untracked)")
    ap.add_argument("--since", metavar="REF", help="only files changed vs a git ref")
    ap.add_argument("--files", nargs="*", help="explicit list of files to validate")
    ap.add_argument("--strict", action="store_true", help="warnings also fail the run")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    files = select_files(args)
    results = []
    n_err = n_warn = 0
    for f in files:
        res = validate_file(f)
        if res["errors"] or res["warnings"]:
            rel = f.relative_to(WIKI_ROOT) if WIKI_ROOT.resolve() in f.parents else f
            results.append((str(rel), res))
            n_err += len(res["errors"])
            n_warn += len(res["warnings"])

    if args.json:
        print(json.dumps({
            "files_checked": len(files),
            "files_with_issues": len(results),
            "errors": n_err,
            "warnings": n_warn,
            "results": [{"file": p, **r} for p, r in results],
        }, indent=2))
    else:
        scope = "changed files" if (args.changed or args.since) else \
                "selected files" if args.files else "whole wiki"
        print(f"=== Schema Validator ({scope}; {len(files)} files) ===")
        if not results:
            print("No schema issues found.")
        for path, res in sorted(results):
            print(f"\n{path}")
            for e in res["errors"]:
                print(f"  ERROR  {e}")
            for w in res["warnings"]:
                print(f"  warn   {w}")
        if results:
            print(f"\nFiles with issues: {len(results)}  |  errors: {n_err}  |  warnings: {n_warn}")

    return 1 if (n_err or (args.strict and n_warn)) else 0


if __name__ == "__main__":
    sys.exit(main())
