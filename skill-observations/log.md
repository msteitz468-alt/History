# Skill Observation Log

Observations captured during task-oriented work. Each entry identifies a
potential skill improvement or new skill opportunity.

**Status key:** OPEN = not yet actioned | ACTIONED = skill updated/created |
DECLINED = user decided not to pursue

---

## 2026-06-25 — Tesla ingest (Seifer, *Wizard*)

### Observation 1: Documented `sleep 35` stagger conflicts with harness foreground-sleep block

**Date:** 2026-06-25
**Session context:** Ingesting Seifer's *Wizard* via the Deployed Subagent Strategy in CLAUDE.md
**Skill:** Project ingest workflow (CLAUDE.md "Deployed Subagent Strategy") — not a library skill
**Type:** internal
**Phase/Area:** Step 3 — staggered subagent batching

**Issue:** CLAUDE.md instructs `sleep 35` between subagent batches for rate-limit mitigation. The Claude Code harness blocks foreground `sleep` ("To wait for a condition, use Monitor… To wait for a command you started, use run_in_background"). I had to re-run each stagger as a `run_in_background: true` Bash sleep and wait for the completion notification.

**Suggested improvement:** Update the CLAUDE.md Step-3 wording to say "run the stagger `sleep` as a background command (run_in_background) and wait for its completion notification" rather than a bare `sleep 35`, so future runs don't hit the block and retry.

**Principle:** When a documented workflow names a concrete shell command, verify it's compatible with the execution harness; prefer harness-native waiting primitives (background commands + notifications) over foreground blocking sleeps.

### Observation 2: Schema validator expects fields/sections not in the CLAUDE.md page templates

**Date:** 2026-06-25
**Session context:** Linting new Tesla pages with scripts/schema_validator.py
**Skill:** Project ingest workflow (CLAUDE.md page schemas + scripts/schema_validator.py)
**Type:** internal
**Phase/Area:** Step 5 — lint/validate

**Issue:** The validator flagged (a) event pages missing a `## Historiography` section and (b) the source page missing `sources_ingested` and `last_updated` frontmatter — but the CLAUDE.md source template uses `pages_created`/`pages_updated`/`ingested` and does not list `sources_ingested`/`last_updated`, and the event template marks Historiography "(if contested)". Other already-committed source pages (e.g. service-penguin, crosby) fail the same source-field check, so the mismatch is pre-existing and recurring.

**Suggested improvement:** Reconcile CLAUDE.md templates with scripts/schema_validator.py — either add `sources_ingested`/`last_updated` to the source frontmatter template and make `## Historiography` explicitly required on all event pages, or relax the validator. Until reconciled, default to adding both fields and a Historiography section on every new event/source page during scaffolding.

**Principle:** When a repo ships both a written schema and an automated validator, treat divergences between them as a maintenance task; in the meantime satisfy the stricter of the two so lint passes cleanly.

### Observation 3: User explicitly querying task-observer activation status ("Are you always running this skill?")

**Date:** 2026-06-25
**Session context:** Direct /task-observer invocation with meta question about persistent activation, following a major task-oriented ingest session (Jefferson Vol 2) in the History wiki project.
**Skill:** task-observer
**Type:** open-source
**Phase/Area:** Activation / Recommended Activation Setup / Surfacing Protocol

**Issue:** The user prefixed the query with /task-observer and asked "Are you always running this skill?" This surfaces uncertainty about whether the meta-monitoring layer is reliably and continuously active, or only conditionally. In the current implementation, activation depends on (1) description matching, (2) explicit /task-observer commands, and (3) the recommended CLAUDE.md structural trigger at the start of task-oriented sessions. The question implies the user wants assurance or greater transparency about when observation logging is happening.

**Suggested improvement:** 
- Add a lightweight, non-intrusive activation confirmation at the very start of task-oriented sessions (e.g., a single sentence: "Task-observer activated for this session (config trigger + description match). Observations will be logged silently and surfaced at end-of-session or on explicit request.").
- Update the skill's "Recommended Activation Setup" and USER-GUIDE to include an example of what a user sees when it is active.
- Consider a simple status sub-command or self-check that can be invoked mid-session without full observation overhead ("Is task-observer active right now?").
- Make the self-enforcement section more visible so users know the skill monitors its own activation reliability.

**Principle:** For any meta-skill whose value depends on consistent background operation, the activation status itself should be observable and verifiable by the user with minimal friction. Users should not have to ask "are you running?" to trust that continuous improvement data is being captured; the system should surface the fact of its own operation proactively at session boundaries.




### Observation (post-continue): Precise artifact cleanup and per-range log discipline for Biography Hub reingests

**Date:** 2026-06-26
**Session context:** Continuation of Deployed Subagent Strategy application to 5 high-res bios (Caro Moses, Isaacson Musk, Chernow Grant, Massie Peter, Stiles Vanderbilt). R05 Musk content already integrated in bio; needed final bookkeeping.
**Skill:** N/A (main wiki ingest workflow per CLAUDE.md)
**Type:** internal
**Phase/Area:** post-integration cleanup + bookkeeping

**Issue:** After subagent range deliveries, stray HTML comments like <!-- Range 09 --> / <!-- Range 08 / Range 09 --> remained in Grant bio (from prior range integrations); index/log lacked granular "Musk Range 05" entry (only R04 + full reingest-complete present) despite bio content and pattern for Moses/Peter/Vanderbilt. Earlier history had over-deletion from broad sed on Moses.

**Suggested improvement:** 1) Always use search_replace with exact unique paragraph strings (never broad sed -i for Range comments). 2) After every range integration batch for a bio, immediately prepend both log.md *and* index.md specific "range integrate | X Range NN" entries modeled on exemplars, even if full reingest-complete follows. 3) Add a post-reconcile "artifact scan" step (grep -l "<!-- Range" on the target bio before lints).

**Principle:** Main-thread ownership of reconciliation includes explicit hygiene and bookkeeping invariants; relying on subagent cleanliness or "later" creates drift and violates the "commit to disk" + transparent log discipline in CLAUDE.md Deployed Subagent Strategy.

Reference: grant clean required 3 targeted replaces; Musk R05 log+index added to match Moses R05 precedent.

## 2026-06-26 — Major & Cook *Ancient China* ingest

### Observation 8: Main-thread page updates need the Read tool, not Bash `cat`, before Edit

**Date:** 2026-06-26
**Session context:** Ingesting Major & Cook, *Ancient China: A History* (2017) via the Deployed Subagent Strategy. The ingest updated 22 existing wiki pages. Repeatedly hit `Edit` failures: "File has not been read yet. Read it first before writing to it."
**Skill:** CLAUDE.md Deployed Subagent Strategy (project ingest workflow)
**Type:** internal
**Phase/Area:** Step 4 — main-thread reconciliation / updating existing pages

**Issue:** I pre-read the target pages with `cat` via the Bash tool to gather context efficiently, but the harness only tracks the Read *tool* for its Edit safety gate. Every Edit to a page I had only `cat`-ed failed until I issued a Read-tool call on the exact lines first. This cost a Read round-trip per page across ~15 pages and is the same friction noted in the prior Liu session. Bash `cat` is fine for scanning many files fast, but it does not satisfy the Edit precondition.

**Suggested improvement:** Add a one-line note to the Deployed Subagent Strategy Step 4 (and the Standard/Large-Volume update steps): "Before editing any existing page, open it with the Read tool (not Bash `cat`) — the Edit gate only recognises the Read tool. Use `cat`/grep only for bulk scanning, then Read the specific offset/lines you will edit." Optionally: when an update touches N known pages, batch the Read-tool calls up front.

**Principle:** Tool choice has side effects beyond fetching bytes: the harness's edit-safety gate is satisfied only by the Read tool. Workflows that update files in bulk should standardise on Read-before-Edit so the context-gathering step also clears the write gate, rather than incurring a second pass.

**Status:** OPEN

### Observation 9: Verifying "0 new broken links" — the wikilink checker only prints the first 50 files

**Date:** 2026-06-26
**Session context:** Lint/validate step of the Major & Cook ingest. Needed to confirm the ingest introduced 0 new broken links. New pages sort alphabetically after the displayed range, so they never appear in the checker's printed list.
**Skill:** CLAUDE.md Deployed Subagent Strategy (project ingest workflow) — Step 5 lint/validate
**Type:** internal
**Phase/Area:** Step 5 — wikilink validation

**Issue:** `scripts/wikilink_checker.py` prints a per-source-file detail list capped at the first 50 files (`sorted(by_source)[:50]`, ~ends at "h") but reports a global `Total broken links` over all files. Grepping the printed output for my new pages (major-cook, qinling, etc.) returned nothing, which falsely looked clean. The reliable way to prove 0-new was a **stash-comparison**: move new files aside + `git stash` the edits, run the checker (baseline total), restore, run again (post-change total), and compare. This caught that my changes actually reduced the count by 2 (and earlier caught a +3 I had to fix). A lighter alternative is a targeted slug-existence scan of every `[[target]]` in the changed files against the set of existing page basenames.

**Suggested improvement:** Codify the verification method in the ingest lint step: do not rely on reading the checker's printed list to confirm new pages are clean (it is capped at 50 files). Instead (a) compare the global `Total broken links` before vs after via stash/aside, or (b) run a slug-existence scan over only the changed files. Consider adding a `--source <glob>` or `--changed` flag to `wikilink_checker.py` so a per-ingest check is one command. Watch the `[[[triple-bracket]]]` frontmatter convention when scanning — naive regex mis-parses it.

**Principle:** A linter's human-readable summary is not the same as its full result set; truncated displays can read as "clean" when they are merely "not shown." Verify scoped claims ("0 *new* X") with a delta measurement (before/after) or a scoped scan, never by eyeballing a capped report.

**Status:** OPEN

### Observation 10: New event pages need a small authoring pre-flight (Historiography section + no phrase-links in frontmatter)

**Date:** 2026-06-26
**Session context:** Created three new `events/` pages (spring-and-autumn, qin-unification, three-kingdoms) during the Major & Cook ingest. Two distinct defects surfaced at lint time, both on event pages.
**Skill:** CLAUDE.md page schema (Event Page) + Deployed Subagent Strategy reconciliation
**Type:** internal
**Phase/Area:** Event page authoring / schema compliance

**Issue:** (1) `schema_validator.py` flagged one event page (spring-and-autumn) for a missing `## Historiography` section — required for "period and major event pages" — which I had omitted while two other event pages happened to include it. (2) The event frontmatter `causes:`/`consequences:` convention uses `[[slug]]` for real links but free text otherwise; I wrapped a descriptive phrase (`[[the sack of the Western Zhou capital in 771 BCE]]`) in brackets, which the wikilink checker counted as a phantom broken link to a non-existent slug. Both are easy-to-miss, recurring event-page traps.

**Suggested improvement:** Add a short "new event page pre-flight" to the ingest workflow / Event Page schema note: (a) include a `## Historiography` section on every event page (the validator treats major events like period pages); (b) in `causes`/`consequences`/`actors_*` frontmatter lists, only bracket real slugs — descriptive phrases go in plain text. Run `schema_validator.py` filtered to the new event pages before commit.

**Principle:** Recurring schema defects cluster by page-type; the cheapest fix is a type-specific pre-flight checklist applied at authoring time, not a generic "run the validator" at the end. Frontmatter that mixes link-syntax with free text needs an explicit rule about when brackets mean "link."

**Status:** OPEN

### Observation 11: Subagents propose NEW pages that duplicate existing wiki pages

**Date:** 2026-06-26
**Session context:** Deployed-Subagent ingest of Barry J. Kemp, *Ancient Egypt: Anatomy of a Civilization* (3rd ed., 2018). Six Sonnet subagents extracted range-exclusive claims and were permitted to propose new pages via `## TARGET: NEW <folder>/<slug>`.
**Skill:** Ingest workflow (CLAUDE.md "Deployed Subagent Strategy") — new skill candidate: "deployed-subagent-ingest"
**Type:** internal
**Phase/Area:** Step 3 (subagent prompts) / Step 4 (main-thread reconciliation)

**Issue:** Two of the subagents' proposed NEW pages duplicated pages that already existed in the wiki: R6 proposed `concepts/aten-religion-atenism` when `concepts/atenism.md` already exists, and R5 proposed `concepts/egyptian-temple-economy` which partially overlaps the existing general `concepts/temple-economy.md`. Subagents read only their line-range and have no view of the existing wiki, so they cannot know what already exists. The main thread caught both during reconciliation (folded Aten claims into existing atenism; made egyptian-temple-economy a deliberate Egypt-specific complement and cross-linked it to the general page), but only because it happened to have surveyed existing Egypt pages during scaffolding.

**Suggested improvement:** (1) In Step 1 scaffolding, run a quick inventory of existing pages for the source's topic area (`ls`/grep of actors|places|concepts|events) and pass that list into each subagent prompt as "pages that already exist — do NOT propose these as NEW; link to them instead." (2) Add an explicit Step-4 reconciliation check: before creating any subagent-proposed NEW page, grep the wiki for an existing page on that topic (including more-general or more-specific variants) and decide fold-in vs. create-complement vs. create-new.

**Principle:** Range-isolated extractors are structurally blind to global state; any "create new X" they emit must be validated against the existing corpus by the one actor that can see the whole — the main thread. Make the dedupe-against-existing check an explicit reconciliation step rather than relying on the author happening to remember what exists.

**Status:** OPEN

### Observation 12: Ebook-converted sources arrive without markdown headings — scaffold must locate structure by running-header/all-caps greps

**Date:** 2026-06-27
**Session context:** Deployed-Subagent ingest of Barry J. Kemp, *Ancient Egypt: Anatomy of a Civilization* (3rd ed., 2018), an ebook→markdown conversion (~23,900 lines).
**Skill:** Ingest workflow (CLAUDE.md "Deployed Subagent Strategy" — Step 1 scaffold / Large-Volume Protocol Step 1 "Read the Structural Map")
**Type:** internal
**Phase/Area:** Step 1 — building the Section Plan / chapter line-range map

**Issue:** The source file had exactly ONE markdown heading (the title); all chapter and part divisions were plain text. `grep -nE "^#{1,3} "` returned only the title, so the line-range map for the Section Plan could not be built from headings. The structure had to be recovered indirectly: the printed TOC was read from the front matter for the logical outline, then each chapter's true start line was found via the ALL-CAPS chapter-opener (e.g. "THE BUREAUCRATIC MIND") and the index/back-matter boundary via repeated running-header greps. Running headers ("Introduction", "Who were the ancient Egyptians?") repeat on every page and produce dozens of false hits, so the FIRST all-caps occurrence had to be distinguished from later running-header repeats.

**Suggested improvement:** Add a note to the scaffold/Section-Plan step: ebook-converted sources (epub/pdf → md via ebook-convert) usually lack markdown headings. Don't rely on `grep "^#"`. Instead (a) read the printed TOC in the front matter for the logical outline, (b) locate each chapter's body start via its ALL-CAPS opener line, and (c) find the index/notes/bibliography boundary to bound the body line-count before sizing/weighting ranges. Expect running headers to generate many duplicate matches; take the first occurrence as the chapter start.

**Principle:** When the input format strips the structure you normally navigate by, recover structure from a redundant secondary signal the format preserves (printed TOC, page running-heads, all-caps display type) rather than assuming the primary signal exists. Verify the body's true start/end line numbers before computing chunk weights — front matter, notes, and index can be a third to a half of the file.

### Observation 13: Dedup existence-checks must cover transliteration/spelling variants of slugs

**Date:** 2026-06-27
**Session context:** Ingesting *The Oxford History of Ancient Egypt* (Shaw 2000) via Deployed Subagent Strategy. During reconciliation I ran an existence check for proposed-new actor slugs and created `actors/mentuhotep-ii.md` and `actors/senusret-iii.md` — only to find the wiki already had `actors/mentuhotpe-ii.md` and `actors/senwosret-iii.md` (older transliterations used consistently across ~9 inbound-linking pages). I had to delete the duplicates, conform to the existing slugs, and rewrite the links in my other new pages.
**Skill:** task-observer / World History Wiki ingest workflow (CLAUDE.md Deployed Subagent Strategy, Step 4 reconciliation)
**Type:** internal
**Phase/Area:** Step 4 (review and tie together) — dedup against existing pages

**Issue:** The standard `[ -f "$slug.md" ]` existence check only catches an exact-slug collision. For ancient-history subjects (Egyptian, Mesopotamian, Chinese rulers; place names) the SAME entity routinely has multiple romanizations — Mentuhotpe/Mentuhotep, Senwosret/Senusret/Sesostris, Amenophis/Amenhotep, Cheops/Khufu — so an exact check reports "missing" and a duplicate gets created under a variant spelling. This is the spelling-variant cousin of Observation 11 (subagents proposing dup pages).

**Suggested improvement:** Before creating any new actor/place page during reconciliation, run a FUZZY existence check, not just exact: grep the actors/places dirs for the surname stem and known romanization variants (e.g. `ls actors | grep -iE 'mentuh|sen(w|u)osret|senusret|amen(h|)otep'`), and grep the wiki for inbound links to the intended display name. Add a short "known-variant romanizations" reminder to CLAUDE.md's Step 4. Cheap, and it prevents the delete-and-rewrite churn.

**Principle:** Identity is not the same as string-equality. When a knowledge base names real-world entities that have multiple legitimate spellings, deduplication must match on the entity (stem + variant set + display-name inbound links), not on the exact slug — otherwise the "does it already exist?" guard silently fails exactly where collisions are most likely.

### Observation 14: `git add` with one nonexistent path silently aborts the whole batch

**Date:** 2026-06-27
**Session context:** Final bookkeeping commit of the *Oxford History of Ancient Egypt* ingest. I staged my new + modified pages with a single multi-file `git add ... 2>/dev/null`. One path in the list was wrong (`wiki/actors/predynastic-egypt.md` — the page actually lives in `processes/`). git aborted the entire `add` with a fatal error, and because I had appended `2>/dev/null`, the error was hidden. Result: NONE of the ~37 files in that batch were staged. I only caught it because the subsequent `git diff --cached --name-only | wc -l` showed 25 (the second batch) instead of the expected ~50, so the new R3–R8 pages were silently left uncommitted until I re-ran the add without the bad path.

**Skill:** task-observer / World History Wiki ingest workflow (CLAUDE.md Step 6 — bookkeeping/commit)
**Type:** internal
**Phase/Area:** Step 6 (commit) — staging an explicit file list

**Issue:** Two compounding traps. (1) `git add a b c nonexistent` fails atomically — git stages nothing from the batch, not "everything except the bad path." (2) Piping `git add` stderr to `/dev/null` (often added to suppress "pathspec did not match" noise during ingests) hides the very fatal that tells you the batch failed. Combined, a single typo'd path can silently drop dozens of files from the commit — exactly the kind of partial-commit data-loss the explicit-file-list rule is meant to prevent.

**Suggested improvement:** In the ingest workflow's Step 6 (and the "no blanket git-add" memory): after staging an explicit list, ALWAYS verify with `git diff --cached --name-only | wc -l` and confirm the count matches the intended file count before committing. Do NOT silence `git add` stderr; if suppressing pathspec warnings, check the exit code instead. Prefer staging via a verified file list (e.g. build the list, confirm each path exists with `ls`/`test -f`, then add) so a typo can't abort the batch.

**Principle:** Commands that operate on a batch can fail atomically and silently — a single bad element can void the whole operation. Never trust that a multi-item mutating command did what you intended; verify the resulting state (here, the staged set) against the expected count before the irreversible next step (commit). And never pipe away the stderr of a state-changing command you depend on.

### Observation 15: Source pages inconsistently carry sources_ingested/last_updated for the schema validator

**Status:** ACTIONED — Fixed in `scripts/schema_validator.py` 2026-06-27: the `source` schema now requires the real CLAUDE.md source fields (`pages_created`, `ingested`) instead of the actor/event fields (`sources_ingested`, `last_updated`). Whole-wiki false-positive count dropped 1056 → 224. Resolves the drift in direction (b).

**Date:** 2026-06-27
**Session context:** Ingesting Nelson, *King and Emperor* (Charlemagne biography) via the Biography Hub workflow.
**Skill:** New skill candidate / CLAUDE.md ingest workflow (wiki-ingest)
**Type:** internal
**Phase/Area:** Step 5 lint — schema validation of `wiki/sources/` pages

**Issue:** `scripts/schema_validator.py` flags every `wiki/sources/` page for "Missing or empty required field: sources_ingested / last_updated", even though the CLAUDE.md **source-page schema** specifies `pages_created`, `pages_updated`, and `ingested` instead (not those two fields). Recent source pages are inconsistent: `geary-before-france-germany-1988.md` omits the two fields (and is flagged), while the Di Cosmo ingest log explicitly records "added sources_ingested/last_updated to source page" to silence the validator. I added both fields to the Nelson source page to make it pass. This wastes a verification cycle every ingest and produces drift between source pages.

**Suggested improvement:** Resolve the mismatch in ONE direction: either (a) update the CLAUDE.md source-page schema + validator to make `sources_ingested`/`last_updated` standard on source pages (simplest: add them to the source frontmatter template), or (b) teach `schema_validator.py` that `source_type`-tagged pages use `ingested`/`pages_created` and should not require the two actor/event fields. Document the decision in CLAUDE.md so future ingests stop re-deciding ad hoc.

**Principle:** When a linter and the authoring spec disagree on required fields for a page type, every ingest silently re-litigates it and the corpus drifts. Make the validator and the template agree once, and the ambiguity stops costing a cycle per ingest.

### Observation 16: Subagent "page numbers" from line-range caches are unreliable artifacts

**Date:** 2026-06-27
**Session context:** Ingesting Manning, *The Last Pharaohs* (Deployed Subagent Strategy, 5 line-range caches; subagents extracted grounded claims with verbatim quotes + page numbers)
**Skill:** CLAUDE.md ingest workflow (Deployed Subagent Strategy)
**Type:** internal
**Phase/Area:** Step 3 (subagent claim extraction) → Step 4 (main-thread reconciliation)

**Issue:** The subagent reading Chapter 5 (range 4) appended "page numbers" to several claims that were clearly impossible for a ~280-page book — e.g. "[p. 984]", "[p. 1011]", "[p. 981]", "[p. 321 fn. 28]". These were line offsets / OCR'd internal-citation numbers the agent mistook for the book's running page numbers. The verbatim quotes themselves were accurate and correctly grounded; only the locators were corrupt. The main thread caught this (the numbers exceed the book's length) and dropped the bogus page numbers when authoring, attributing by chapter instead — but a less careful pass could have propagated fake citations into the wiki.

**Suggested improvement:** In the subagent claim-extraction prompt, instruct agents to (a) prefer the **verbatim quote as the primary locator** and (b) only cite a page number when a clean running-header page number is visibly adjacent in their slice, otherwise cite by chapter/section — and to flag uncertain locators rather than guess. During Step 4 reconciliation, the main thread should sanity-check any page number against the known page count and strip/replace implausible ones.

**Principle:** Quotes are verifiable; locators extracted from OCR'd line-range slices are not. When the grounding evidence (the quote) and the citation (page number) come from the same noisy source, trust the quote and treat the number as suspect until validated against an independent bound (total page count).

### Observation 17: Top_100 running tally drifts stale across parallel ingest sessions

**Date:** 2026-06-27
**Session context:** Ingesting Barnes, *Archaeology of East Asia* (2015) — Deployed Subagent Strategy. On marking Top_100 #19 ✅, found the header tally line read "Current: 8 completed, 25 missing" while an actual grep showed **22 completed, 20 missing** — the counter had not been maintained as ~14 sources were ingested by this and parallel sessions.
**Skill:** CLAUDE.md Ingest Workflow (Step 6 bookkeeping / Top_100_Structural_Sources.md maintenance)
**Type:** internal
**Phase/Area:** Step 6 — "Update Top_100_Structural_Sources.md"

**Issue:** The ingest bookkeeping step instructs marking the line-item ✅ but says nothing about the human-readable running tally at the top of the file. With multiple sessions ingesting concurrently, that tally silently rots (off by 14 here). Anyone reading the file for a status snapshot gets a wrong number.

**Suggested improvement:** Add to the Step 6 / Top_100 instruction: "after marking the item ✅, recompute the header tally by grepping ✅ vs [MISSING] counts rather than incrementing by hand." A one-line `grep -c` recompute makes it parallel-safe (derive, don't increment).

**Principle:** Derived counters in shared files should be **recomputed from ground truth**, never hand-incremented — hand-increment assumes a single serial writer, which breaks under parallel sessions. Prefer "count the source of truth" over "bump the cache."

### Observation 18: Concurrent ingest sessions collide on shared append-only bookkeeping files

**Date:** 2026-06-27
**Session context:** Ingesting Benjamin, *Empires of Ancient Eurasia* (2018) while a parallel session ingested the Oxford Handbook of the Merovingian World.
**Skill:** World History Wiki ingest workflow (CLAUDE.md)
**Type:** internal
**Phase/Area:** Step 6 bookkeeping / commit

**Issue:** I appended my ingest entries to the three SHARED append-only files (`wiki/index.md`, `wiki/log.md`, `Top_100_Structural_Sources.md`). Before I committed, the parallel Merovingian session ran its own commit (`6c07dc4`) whose `git add` swept up MY uncommitted appends to those three shared files — so they were committed under the *other* ingest's commit message, and `git status` then showed them as already-in-HEAD with no diff. My 40 content pages were untouched and committed cleanly afterward, but the bookkeeping edits landed in someone else's commit. Also, `--changed` lint scopes were polluted by the other session's untracked WIP (merovingian-*.md), forcing per-file verification to prove 0 NEW broken links (consistent with prior skill-obs about per-file checking).

**Suggested improvement:** When two ingests may run concurrently, treat the three shared append-only files (index.md, log.md, Top_100) as a contention point: (a) stage and commit them as early as possible after writing, or (b) append + `git add` + commit them in the SAME quick step rather than leaving them dirty across a long content-writing phase, and (c) at commit time, verify with `git diff --cached --stat HEAD -- <those files>` that your own appends are actually in YOUR commit, not silently absorbed by a neighbor. Don't rely on a single end-of-run `git add` of shared files.

**Principle:** Shared, append-only, multi-writer files are a race surface. In any workflow where parallel agents both append to the same ledger/index and commit independently, the writer that commits last may find its edits already swept into another's commit (or, worse, lost to a checkout). Minimize the window between writing a shared file and committing it, and verify ownership of your own staged hunks before declaring the commit done.

### Observation 19: "Interpretive-layer" ingest — deep subagent fleet but predominantly UPDATE, reconciled as per-page author-sections

**Date:** 2026-06-27
**Session context:** Ingesting Liverani, *The Ancient Near East* (2014) — a landmark single-author synthesis covering c. 3500–500 BCE, into a wiki whose ANE backbone was already strong (built mostly from the Cambridge Ancient History).
**Skill:** CLAUDE.md Ingest Workflow (Deployed Subagent Strategy + ingestion-depth-hybrid)
**Type:** internal
**Phase/Area:** Step 4 reconciliation / depth decision

**Issue:** The existing memory `ingestion-depth-hybrid` frames the choice as light-touch (TOC+sampling) for well-trodden topics vs. deep section reads for gaps/distinctive scholarship. This source was BOTH: the factual spine is exceptionally well-trodden (every actor/place/period page already existed) AND Liverani's analytic framing (society/economy/ideology, source-criticism, modes of production) is genuinely distinctive. The right call was a FULL deep subagent fleet (10 ranges, ~560 grounded claims) but where the reconciliation output was ~42 page UPDATES vs only 6 new pages — i.e., a deep extraction feeding an overwhelmingly *update* ingest. The clean reconciliation unit turned out to be a single named "## Liverani: ..." section appended to each existing page (foregrounding only what HE adds/revises, cross-linking to 2–3 new concept pages that carry his framework), plus a frontmatter bump. New pages were reserved for (a) his signature analytic frameworks as concept pages and (b) genuine factual gaps (Ebla had no page at all).

**Suggested improvement:** Add to the depth-decision guidance a third, explicit mode: the **"interpretive-layer ingest"** — when a distinctive secondary synthesis lands on an already-strong backbone, still run the deep subagent fleet, but plan for mostly-UPDATE output and reconcile by adding one **named author-section per existing page** (`## <Author>: <thesis>`), creating new pages only for the author's distinctive analytic frameworks (as concepts) and for true gaps. Decide created-vs-updated by checking page existence up front (a single `ls`/grep sweep over candidate slugs before spawning), so subagents link to real names and the main thread knows the create/update split in advance.

**Principle:** Depth of *reading* and breadth of *new-page creation* are independent axes. A source can warrant maximum extraction depth while warranting almost no new pages; conflating "deep ingest" with "many new pages" leads to either under-reading distinctive scholarship or over-proliferating duplicate pages. Match the reconciliation unit (named author-section vs new page) to what the source actually adds to each existing target.

### Observation 20: Pre-existing broken links surface in the --changed wikilink scan for every touched file and must be triaged, not blindly "fixed"

**Date:** 2026-06-27
**Session context:** Liverani ingest; running `wikilink_checker.py --changed` after each cluster commit.
**Skill:** CLAUDE.md Lint Workflow (wikilink checker) + skill-obs #9 (per-file 0-NEW-broken-links checking)
**Type:** internal
**Phase/Area:** Step 5 lint / per-file broken-link verification

**Issue:** Because the `--changed` scan flags ANY broken link in a touched file, editing a long-standing page (e.g. `early-iron-age.md`, `neo-assyrian-empire.md`) surfaces its pre-existing backlog (craig-benjamin, western-zhou, ironworking, `[[transition]]`, `bronze-age-collapse` without the -1200bce suffix, the deleted `Outstanding Sources.md`, `[[[assyria]]` frontmatter triple-brackets, etc.). These are NOT introduced by the ingest. The correct discipline (skill-obs #9) is to verify my *added* lines introduce 0 new broken links — but in this session I went further and fixed the surfaced pre-existing ones in files I was already committing (pointing to correct slugs where one existed, e.g. western-zhou→zhou-dynasty, craig-benjamin→benjamin-cwh-v4-2015, [[assyria]]→[[ashur]]; unlinking where no target existed). That keeps each commit's touched files at literally 0 broken links, but it is opportunistic repo-debt cleanup, not part of the ingest.

**Suggested improvement:** Make the triage explicit in the lint step: after `--changed`, for each flagged link decide (1) did MY edit introduce it? → must fix; (2) pre-existing in a file I'm committing? → fix only if a correct target is obvious/cheap (repoint or unlink), otherwise leave and note it; (3) pre-existing in a file I'm NOT committing? → ignore. Record in the log which pre-existing links were opportunistically fixed so the cleanup is auditable. (Also: the Edit tool requires a Read-TOOL read of a file before editing — reading via `Bash cat` to plan does NOT satisfy it, so batch a cheap `Read` of each target before its first Edit to avoid a rejected-edit round-trip.)

**Principle:** A "0 broken links" gate on a changed-file scan conflates *newly introduced* breakage (the ingest's responsibility) with *pre-existing* backlog (the repo's). Always triage by provenance (git diff / "is this in a line I wrote?") before fixing, and treat any pre-existing fixes as a separate, logged courtesy — never let backlog-chasing balloon an ingest.

### Observation 21: Scaffold create-vs-update check must scan ALL wiki subdirs, not folder-filtered greps

**Date:** 2026-06-27
**Session context:** Ingesting Bryce, *The Kingdom of the Hittites* (Deployed Subagent Strategy). During Step-1 scaffolding I twice concluded a page was "missing" (`shuppiluliuma-i`, `ahhiyawa-question`, `telipinu-edict-1500bce`) based on `ls wiki/actors/ | grep` checks, then found via `find wiki -iname` that they already existed — `ahhiyawa-question` was in `controversies/`, and an event grep had been filtered out the existing `telipinu-edict`. Heavily-referenced "red links" (29 inbound for shuppiluliuma-i) turned out to be live targets created by prior ingests.
**Skill:** one-skill-to-rule-them-all (ingest workflow in CLAUDE.md, Deployed Subagent Strategy Step 1)
**Type:** internal
**Phase/Area:** Step 1 scaffold — deciding create vs. update

**Issue:** Checking page existence with directory-scoped greps (`ls wiki/actors/ | grep X`) misses pages that live in a sibling type-folder (a controversy, a process) or that get filtered by an over-narrow grep pattern. This risks a subagent (or the main thread) re-creating an existing page under a new slug — the exact duplication failure mode of Observation 11.
**Suggested improvement:** In the ingest workflow, make the canonical existence check a single repo-wide `find wiki -iname "*<stem>*"` (or `grep -rl` over `wiki/`) per candidate slug, run BEFORE writing the naming registry — never a per-folder `ls | grep`. Cross-check inbound red-link counts with actual file presence: a high red-link count does NOT mean the target is missing.
**Principle:** Existence checks in a typed, cross-linked knowledge base must be namespace-wide, not folder-scoped — the same entity can legitimately live in any of several type directories, and the link graph is the source of truth for "is this referenced", not "does this exist". Verify presence by file path, reference by link graph, and never conflate the two.

### Observation 22: Subagent created a homophone-slug duplicate (hattusa vs. hattusha) of an existing page

**Date:** 2026-06-27
**Session context:** Bryce *Kingdom of the Hittites* ingest. Despite the agent contract explicitly listing `hattusha` in the EXISTING/link-only set, a subagent created a full new `wiki/places/hattusa.md` (no medial 'h') duplicating the canonical `wiki/places/hattusha.md`. It was caught only because the final `wikilink_checker --changed` flagged a broken link *inside* the duplicate; the duplicate itself is not flagged by the link checker (it resolves its own slug). Three pre-existing pages (yamhad, luwians, a not-yet-ingested Bryce source page) had long carried red links to the wrong-spelled `[[hattusa]]`, which the duplicate silently "satisfied."
**Skill:** one-skill-to-rule-them-all (Deployed Subagent Strategy — Step 4 reconciliation)
**Type:** internal
**Phase/Area:** Step 4/5 — dedup and validation after subagents return

**Issue:** A near-homophone / variant-transliteration slug (`hattusa` vs `hattusha`) is invisible to the wikilink checker (both are "valid" once a file exists for each) and to a naive "does the page exist" check. Subagents over-create such pages even when told to link the canonical slug, and pre-existing red links to the variant spelling mask the problem. This is a concrete recurrence of [[#11]] and the failure mode [[#21]] warns about.
**Suggested improvement:** Add a Step-4 reconciliation check to the ingest workflow: after subagents return, run a **variant-spelling collision scan** — for each newly created place/actor slug, grep the wiki for near-duplicate slugs differing only by a medial/terminal h, doubled consonant, or s/sh (e.g. `ls wiki/*/ | sort | uniq`-style fuzzy compare, or explicitly grep both spellings of contested names). Resolve to the slug with the most inbound links; delete the duplicate; repoint stray variant links. The link checker alone will NOT catch a self-consistent duplicate.
**Principle:** In a slug-keyed wiki, the dangerous duplicate is not the broken link but the *self-consistent* one — two files for one entity under spelling variants. Validation that only checks "do links resolve" is blind to it; dedup must include an active variant-collision scan keyed on the entity, not the string.

### Observation 23: Transliteration-duplicate near-miss recurred (Bryce gazetteer)

**Date:** 2026-06-27
**Session context:** Ingesting Bryce, *Routledge Handbook of the Peoples and Places of Ancient Western Asia* (reference gazetteer) — focused main-thread reference ingest into the already-strong ANE wiki.
**Skill:** task-observer (ANE-ingest practice; relates to existing Observation 13)
**Type:** internal
**Phase/Area:** Step 1 scaffolding / dedup against existing pages

**Issue:** I scaffolded two new pages — `places/hattusa.md` and `actors/yamhad.md` — before discovering the wiki already had `places/hattusha.md` and `actors/iamkhad.md` (CAH-built, under alternative transliterations). This is the exact failure mode flagged in Observation 13. My pre-flight slug check missed them because I only checked the spelling *I* intended (`hattusa`, `yamhad`), not the transliteration variants the prior ingest had chosen (`hattusha`, `iamkhad`). A repo auto-linter caught and removed the `hattusa.md` duplicate and redirected links, but the `yamhad`/`iamkhad` duplicate I had to catch and fix manually (the linter left those links pointing at my duplicate). Resolved by deleting both dupes and folding the additive Bryce material into the existing pages.

**Suggested improvement:** Before scaffolding ANY new ANE place/people page, grep the wiki for *transliteration variants*, not just the intended slug: h↔kh, double letters (Hattusa/Hattusha), initial Y↔I (Yamhad/Iamkhad), -a↔-ah endings, k↔c, sh↔š. A cheap heuristic: search on a distinctive 4–5 letter root substring (`find . -iname '*amkhad*'`, `find . -iname '*attus*'`) rather than the full slug. Bake this into the ingest scaffold step for reference works especially, where dozens of named places are created at once.

**Principle:** When a wiki already has deep coverage built by a prior source with its own naming conventions, the dominant ingest risk shifts from "writing good content" to "colliding with existing pages under different spellings." Dedup must search the *concept*, not the *chosen slug*. Recurrence of Observation 13 confirms a root-substring transliteration check belongs in the standing pre-scaffold routine, not just as a remembered caution.


### Observation 25: User clarified that task-observer activation should NOT be made a big visible deal

**Date:** 2026-06-27
**Session context:** User feedback correcting over-application of visible/loud activation during Polis ingest (and prior sessions). Earlier log entries had escalated to requiring persistent monitors, numbered public announcements, 5-point checklists, and "make a big deal" ceremony for every ingest.
**Skill:** task-observer
**Type:** internal
**Phase/Area:** Activation / Visibility and ceremony

**Issue:** User stated: "In our previous conversation, I said you DID NOT need to make a big deal (like having a persistent background monitor showing) for the task-observer". Practices had produced unnecessary noise (persistent tail -f monitor streaming log entries, explicit "Task-observer explicitly invoked" banners, etc.).

**Suggested improvement:** 
- Revert activation to the minimum required by CLAUDE.md: read the task-observer SKILL.md and check `skill-observations/log.md` for relevant OPEN observations at the start of task-oriented sessions.
- Do NOT automatically launch persistent background monitors (e.g. `monitor` tool on log.md) for activation.
- Do NOT append a dedicated visible activation observation just to "prove" it was invoked.
- Keep any activation steps quiet/silent unless the user specifically asks for visibility.
- Loud/visible activation language in the log has been removed.

**Principle:** When the user gives explicit feedback about the desired visibility and ceremony level of a meta-skill, that preference overrides earlier escalated instructions in the observation log. "Invoking" the skill should support the work without creating distracting side-effects or visible theater.

**Status:** OPEN


### Observation 26: Dedup sed-repoint inflates the broken-link changed-set with pre-existing noise

**Date:** 2026-06-27
**Session context:** Ingesting Wiesehöfer, *Ancient Persia*. A duplicate empire page (`sassanid-empire.md` vs canonical `sasanian-empire.md`) was merged: ~34 inbound links were `sed`-repointed, then the dup deleted.
**Skill:** CLAUDE.md ingest workflow (Step 5 lint / dedup handling)
**Type:** internal
**Phase/Area:** Lint & validation after a cross-wiki dedup

**Issue:** `wikilink_checker.py --changed` reported 19 "broken links," but every one was a *pre-existing* forward-reference (missing pages like `arab-conquests`, `gokturk`, `valerian`, `high-empire`) inside Roman-third-century pages that the dedup `sed` had touched only to swap `sassanid-empire`→`sasanian-empire`. None were introduced by the new content. Distinguishing introduced-vs-pre-existing breakage took an extra verification pass (grepping variant target names, checking they were missing before the run).

**Suggested improvement:** When a dedup/rename touches many unrelated files, verify "0 broken links" against the *authored* set, not the whole changed-set: e.g. run the checker on a baseline first (or `git stash` the repoint), diff the broken-link counts, and only own the delta. Note in the log entry that changed-set noise is pre-existing. Also: do the dedup link-repoint as the LAST step before lint so its file churn is isolated.

**Principle:** Mechanical mass-edits (rename/repoint/sed) expand the lint changed-set far beyond the semantic change, so a "0 broken links in changed files" gate produces false positives. The reliable signal is the *delta* of broken links the edit introduces, not the absolute count in every file it incidentally modified.

### Observation 27: Editing a pre-existing page during ingest inherits latent schema debt

**Date:** 2026-06-27
**Session context:** Ingesting Wickham, *Medieval Europe* (2016). Added a Wickham subsection + "failure of alternatives" content to the pre-existing events/fourth-crusade-1204.md.
**Skill:** New skill candidate (or CLAUDE.md ingest-workflow note): "wiki-ingest" workflow
**Type:** internal
**Phase/Area:** Step 5 lint / page-update discipline

**Issue:** The Fourth Crusade event page predated the schema requirement that event pages carry a `## Historiography` section, so it had been passing un-flagged. The moment I edited it during this ingest, the changed-files schema validator flagged it as missing Historiography — making the latent debt my responsibility to fix (I added a proper Historiography section). This is a recurring dynamic: touching an old page during an ingest surfaces schema gaps that accumulated before the validator (or the requirement) existed.

**Suggested improvement:** In the ingest workflow's reconciliation/lint step, treat "schema validator surfaces an issue on a page I only lightly edited" as expected, not surprising — budget for fixing inherited gaps on every updated page, and prefer `--changed` schema runs early (before writing much) so the gap is known up front rather than discovered at commit time.

**Principle:** When a quality gate is scoped to "changed files," editing a legacy file silently adopts all of its pre-existing debt. Run the gate on a page *before* substantially editing it, so inherited failures are distinguished from regressions you introduced.

### Observation 28: "0 broken links" is unachievable repo-wide; the real standard is 0 NEW broken links in touched files

**Date:** 2026-06-27
**Session context:** Ingesting Miles, *Carthage Must Be Destroyed* via the Deployed Subagent Strategy. At lint time the wikilink checker reported 1126 pre-existing broken links repo-wide; `--changed` scoped to ALL uncommitted working-tree changes (including unrelated pre-existing edits), not the files this ingest authored.
**Skill:** CLAUDE.md ingest workflow (Step 5 lint) / wiki tooling
**Type:** internal
**Phase/Area:** Lint and validate

**Issue:** CLAUDE.md Step 5 says the wikilink checker "must report 0 broken links," but the repo carries a large standing backlog (1126), so a literal global zero is impossible. Neither `--all` (too noisy) nor `--changed` (catches unrelated working-tree churn) isolates the ingest's own files; I had to hand-roll an awk/grep filter on the explicit file list to verify my edits introduced no broken links.

**Suggested improvement:** Restate the Step 5 standard as "0 NEW broken links among the files this ingest created/updated," and either (a) add a `--files <list>` mode to wikilink_checker.py, or (b) document the awk-filter pattern as the standard verification recipe. Same applies to schema_validator output.

**Principle:** When a validator runs against a corpus with a known pre-existing defect backlog, the meaningful acceptance criterion is "no NEW defects in the changed set," not "global zero." Tooling and instructions should make per-change scoping the default, or the standard becomes unverifiable and gets skipped.

### Observation 29: De-link scripts must guard against [[[ triple-bracket YAML-list frontmatter

**Date:** 2026-06-27
**Session context:** Ingesting the Cambridge History of the Pacific Islanders; bulk-fixing broken wikilinks across 51 new pages with a regex de-link script.
**Skill:** ingestion / wiki-link-maintenance workflow (CLAUDE.md Step 5)
**Type:** internal
**Phase/Area:** post-ingest lint / broken-link remediation

**Issue:** A Python de-link pass using `\[\[([^\]]+)\]\]` corrupted YAML frontmatter list fields written as `events_here: [[[page|Display]], ...]` (list-bracket + wikilink = three opening brackets). The regex captured a leading `[`, so the target basename never matched the valid-page set even when the page existed, and the link was wrongly de-linked — leaving dangling `]` and broken YAML on the 4 region anchor pages. Only caught because the harness surfaced the file modifications.

**Suggested improvement:** When scaffolding place/actor/event frontmatter, write list fields as PLAIN kebab-name lists (no `[[ ]]` inside frontmatter) — links belong in the body. And any regex de-link/link-rewrite pass should (a) skip the YAML frontmatter block, or (b) normalize `[[[`/`]]]` before matching and verify the result re-parses as YAML.

**Principle:** Wikilink syntax inside YAML frontmatter is fragile under bulk regex edits; keep frontmatter link-free and confine `[[ ]]` to body prose. Validate frontmatter still parses after any scripted rewrite.

### Observation 30: Subagents can recreate an anchor page in a different folder, causing slug collisions

**Date:** 2026-06-27
**Session context:** Ingesting *The Cambridge History of Australia, Vol. 1* via the Deployed Subagent Strategy. The main thread pre-created `wiki/processes/australian-frontier-conflict.md` as an anchor and told the Ch13–14 subagent to LINK/append to it, not recreate it. The subagent instead created `wiki/events/australian-frontier-conflict.md` (same slug, different folder), producing a duplicate basename. Because Obsidian wikilinks resolve by basename regardless of folder, `[[australian-frontier-conflict]]` became ambiguous. The main thread had to merge the (richer) event content into the canonical process page and delete the event file.
**Skill:** CLAUDE.md ingest workflow (Deployed Subagent Strategy, Step 1/Step 3) — and applies to the atlas/ingest skills generally.
**Type:** internal
**Phase/Area:** Subagent scaffolding instructions / anchor-page handoff.

**Issue:** Telling a subagent the anchor's bare name ("do NOT recreate [[australian-frontier-conflict]]") is insufficient when the topic plausibly fits more than one page type. The agent didn't realize the existing anchor lived in `processes/` and made a same-slug page in `events/`. Subagents check existence with `ls wiki/<their-guessed-folder>/`, which misses an anchor sitting in a different folder.

**Suggested improvement:** When handing anchor names to subagents, give each anchor's **full relative path including folder** (e.g. `wiki/processes/australian-frontier-conflict.md`), and add an explicit rule: "Before creating ANY page, `grep -rl 'title: <X>' wiki/` or check all type folders for the slug — if a page with that basename exists in ANY folder, enrich it, never create a same-named file elsewhere." Add this to the Step-3 subagent prompt boilerplate.

**Principle:** Wikilink namespaces that are folder-agnostic make the *basename* the unique key. Any workflow that parallelizes page creation must enforce basename uniqueness across all folders, and must hand collaborators the full path of pre-existing anchors — a bare name invites recreation in a sibling folder.

### Observation 31: Subagents wrap link-taxonomy labels as wikilinks and overstep "don't touch index/log"

**Date:** 2026-06-27
**Session context:** CHA Vol. 2 deployed-subagent ingest (8 Sonnet agents over disjoint chapter-ranges).
**Skill:** Ingest Workflow — Deployed Subagent Strategy (CLAUDE.md)
**Type:** internal
**Phase/Area:** Step 3 (subagent prompts) / Step 4 (reconciliation)

**Issue:** Two recurring subagent defects surfaced during reconciliation: (1) one agent wrote event-frontmatter list items as `"[[caused_by]]: collapse of export prices..."` — wrapping the link-taxonomy *label* in `[[ ]]`, which the wikilink checker counts as a broken link (and is semantically wrong: the label is a key/prefix, not a page). This required a sed pass across 3 files. (2) Despite an explicit "do NOT edit the source page or log" instruction, one agent inserted a partial index.md entry covering only its 4 pages and prepended a section entry to log.md — main thread had to rewrite both to cover the whole ingest.

**Suggested improvement:** In the per-agent prompt template add two explicit lines: (a) "Link-taxonomy labels (caused_by, produced, etc.) are plain prefixes, NEVER wikilinks — write `caused_by: [[page]]` or `caused_by: plain text`, never `[[caused_by]]`." (b) "Do NOT write to wiki/index.md or wiki/log.md under any circumstance — the main thread owns all bookkeeping." Consider a main-thread grep for `\[\[(caused_by|produced|contributed_to|preceded_by|followed_by|enabled|concurrent_with|part_of|contains)\]\]` as a standard Step-4 reconciliation check.

**Principle:** Negative instructions to subagents need to be concrete and enumerated; a single "don't touch bookkeeping" line gets overridden by the agent's helpful instinct to update the index. And shared-vocabulary tokens (the link taxonomy) are a predictable place for agents to misapply markup — cheap to catch with a fixed grep, expensive to catch by eye.

### Observation 32: Scope artifact/leak greps to the session's file set, not the whole wiki

**Date:** 2026-06-27
**Session context:** Ingesting Kirby, *The Earliest English Kings* via the Deployed Subagent Strategy; during Step 4 reconciliation I ran a broad `grep -rlnE "</content>|do not read|prompt|range_[A-D]_" wiki/` to find subagent artifacts.
**Skill:** New skill candidate / CLAUDE.md ingest workflow (Deployed Subagent Strategy, Step 4)
**Type:** internal
**Phase/Area:** Step 4 — "remove agent artifacts (stray instructions, prompt echoes, tags — grep first)"

**Issue:** The repo had ~150 untracked files from concurrent/prior ingest sessions (Pacific, Americas, Franks). The wide alternation pattern matched innocuous prose ("prompting", "do not") across dozens of unrelated files, producing a 150-line false-positive dump that had to be re-done scoped to just this ingest's files (built from `git status --porcelain` minus other sessions' work). The real check only needed the ~44 files this ingest created/edited.

**Suggested improvement:** In the ingest workflow's artifact-grep step, first capture the session's own file list (e.g. the set of pages the scaffold + subagents created/edited) and grep ONLY those, with a tight pattern (`</content>`, literal prompt fragments, the cache-file path prefix) rather than fuzzy words like "prompt"/"do not" that occur in normal historical prose.

**Principle:** Verification greps should be scoped to the unit of work and use patterns specific enough to avoid matching legitimate content; a wide repo-wide fuzzy grep in a busy multi-session repo produces noise that defeats the check.
