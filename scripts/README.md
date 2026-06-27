# Wiki Lint Scripts

These scripts implement the linting and validation tools referenced throughout `CLAUDE.md`.

## Available Scripts

- `lint.py` — Main runner. Orchestrates the checks.
  - `python scripts/lint.py` — full suite
  - `python scripts/lint.py --wikilinks`
  - `python scripts/lint.py --schema`
  - `python scripts/lint.py --biographies`

- `wikilink_checker.py` — Finds broken `[[wikilinks]]`. CLAUDE.md requires this to report **0 broken links** before commit.

- `schema_validator.py` — Validates frontmatter fields against the page-type schemas defined in CLAUDE.md (periods, events, actors, biographies in the hub, etc.).

- `alias_sync.py` — Extracts and reports Obsidian-style `aliases:` declared in frontmatter. Basic collision detection can be added later.

## Typical Workflow (per CLAUDE.md)

After any ingest or large edit:

```bash
python scripts/lint.py
```

Fix issues until the wikilink checker reports 0 broken links and schema issues on touched files are resolved.

## Extending

The main `lint.py` already includes several of the manual checks listed in the "Lint Workflow" section of CLAUDE.md (empty causes/consequences, biography reciprocals, etc.).

Add more targeted checkers here as the wiki grows (e.g., orphan detection, caused_by vs preceded_by heuristics, historiography presence on all periods).

Run from repo root.
