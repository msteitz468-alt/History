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

**Status:** ACTIONED — Applied to task-observer (2026-07-02 weekly review): Added lightweight silent confirmation sentence, explicit "low-visibility" rule, simple status self-check, and made self-enforcement checklist prominent in the staged SKILL.md. See skill-updates/2026-07-02/task-observer/SKILL.md.




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

**Status:** ACTIONED — Applied to CLAUDE.md Step-4 Read-before-Edit (weekly review 2026-07-03)

### Observation 9: Verifying "0 new broken links" — the wikilink checker only prints the first 50 files

**Date:** 2026-06-26
**Session context:** Lint/validate step of the Major & Cook ingest. Needed to confirm the ingest introduced 0 new broken links. New pages sort alphabetically after the displayed range, so they never appear in the checker's printed list.
**Skill:** CLAUDE.md Deployed Subagent Strategy (project ingest workflow) — Step 5 lint/validate
**Type:** internal
**Phase/Area:** Step 5 — wikilink validation

**Issue:** `scripts/wikilink_checker.py` prints a per-source-file detail list capped at the first 50 files (`sorted(by_source)[:50]`, ~ends at "h") but reports a global `Total broken links` over all files. Grepping the printed output for my new pages (major-cook, qinling, etc.) returned nothing, which falsely looked clean. The reliable way to prove 0-new was a **stash-comparison**: move new files aside + `git stash` the edits, run the checker (baseline total), restore, run again (post-change total), and compare. This caught that my changes actually reduced the count by 2 (and earlier caught a +3 I had to fix). A lighter alternative is a targeted slug-existence scan of every `[[target]]` in the changed files against the set of existing page basenames.

**Suggested improvement:** Codify the verification method in the ingest lint step: do not rely on reading the checker's printed list to confirm new pages are clean (it is capped at 50 files). Instead (a) compare the global `Total broken links` before vs after via stash/aside, or (b) run a slug-existence scan over only the changed files. Consider adding a `--source <glob>` or `--changed` flag to `wikilink_checker.py` so a per-ingest check is one command. Watch the `[[[triple-bracket]]]` frontmatter convention when scanning — naive regex mis-parses it.

**Principle:** A linter's human-readable summary is not the same as its full result set; truncated displays can read as "clean" when they are merely "not shown." Verify scoped claims ("0 *new* X") with a delta measurement (before/after) or a scoped scan, never by eyeballing a capped report.

**Status:** ACTIONED — Applied to CLAUDE.md Step-5 stash-comparison for 0-new links (weekly review 2026-07-03)

### Observation 10: New event pages need a small authoring pre-flight (Historiography section + no phrase-links in frontmatter)

**Date:** 2026-06-26
**Session context:** Created three new `events/` pages (spring-and-autumn, qin-unification, three-kingdoms) during the Major & Cook ingest. Two distinct defects surfaced at lint time, both on event pages.
**Skill:** CLAUDE.md page schema (Event Page) + Deployed Subagent Strategy reconciliation
**Type:** internal
**Phase/Area:** Event page authoring / schema compliance

**Issue:** (1) `schema_validator.py` flagged one event page (spring-and-autumn) for a missing `## Historiography` section — required for "period and major event pages" — which I had omitted while two other event pages happened to include it. (2) The event frontmatter `causes:`/`consequences:` convention uses `[[slug]]` for real links but free text otherwise; I wrapped a descriptive phrase (`[[the sack of the Western Zhou capital in 771 BCE]]`) in brackets, which the wikilink checker counted as a phantom broken link to a non-existent slug. Both are easy-to-miss, recurring event-page traps.

**Suggested improvement:** Add a short "new event page pre-flight" to the ingest workflow / Event Page schema note: (a) include a `## Historiography` section on every event page (the validator treats major events like period pages); (b) in `causes`/`consequences`/`actors_*` frontmatter lists, only bracket real slugs — descriptive phrases go in plain text. Run `schema_validator.py` filtered to the new event pages before commit.

**Principle:** Recurring schema defects cluster by page-type; the cheapest fix is a type-specific pre-flight checklist applied at authoring time, not a generic "run the validator" at the end. Frontmatter that mixes link-syntax with free text needs an explicit rule about when brackets mean "link."

**Status:** ACTIONED — Applied to CLAUDE.md Event Page pre-flight (weekly review 2026-07-03)

### Observation 11: Subagents propose NEW pages that duplicate existing wiki pages

**Date:** 2026-06-26
**Session context:** Deployed-Subagent ingest of Barry J. Kemp, *Ancient Egypt: Anatomy of a Civilization* (3rd ed., 2018). Six Sonnet subagents extracted range-exclusive claims and were permitted to propose new pages via `## TARGET: NEW <folder>/<slug>`.
**Skill:** Ingest workflow (CLAUDE.md "Deployed Subagent Strategy") — new skill candidate: "deployed-subagent-ingest"
**Type:** internal
**Phase/Area:** Step 3 (subagent prompts) / Step 4 (main-thread reconciliation)

**Issue:** Two of the subagents' proposed NEW pages duplicated pages that already existed in the wiki: R6 proposed `concepts/aten-religion-atenism` when `concepts/atenism.md` already exists, and R5 proposed `concepts/egyptian-temple-economy` which partially overlaps the existing general `concepts/temple-economy.md`. Subagents read only their line-range and have no view of the existing wiki, so they cannot know what already exists. The main thread caught both during reconciliation (folded Aten claims into existing atenism; made egyptian-temple-economy a deliberate Egypt-specific complement and cross-linked it to the general page), but only because it happened to have surveyed existing Egypt pages during scaffolding.

**Suggested improvement:** (1) In Step 1 scaffolding, run a quick inventory of existing pages for the source's topic area (`ls`/grep of actors|places|concepts|events) and pass that list into each subagent prompt as "pages that already exist — do NOT propose these as NEW; link to them instead." (2) Add an explicit Step-4 reconciliation check: before creating any subagent-proposed NEW page, grep the wiki for an existing page on that topic (including more-general or more-specific variants) and decide fold-in vs. create-complement vs. create-new.

**Principle:** Range-isolated extractors are structurally blind to global state; any "create new X" they emit must be validated against the existing corpus by the one actor that can see the whole — the main thread. Make the dedupe-against-existing check an explicit reconciliation step rather than relying on the author happening to remember what exists.

**Status:** ACTIONED — Applied to CLAUDE.md Step-1 duplicate pre-scan + lint check (weekly review 2026-07-03)

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

**Status:** ACTIONED — Applied to task-observer (2026-07-02 weekly review): Reinforced minimal/silent activation rules, added explicit "no persistent monitors, no ceremony" language, and low-visibility confirmation in staged update. Matches user clarification exactly.


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

### Observation 33: Exclusive page-ownership + claims-files prevents concurrent-edit collisions among background subagents

**Date:** 2026-06-27
**Session context:** Ingesting Hutton, *Blood and Mistletoe* (reception history of Druids in Britain) via the Deployed Subagent Strategy with 4 Sonnet agents run with run_in_background:true over disjoint chapter ranges.
**Skill:** Deployed Subagent Strategy (CLAUDE.md ingest workflow) / off-list-raw-batch
**Type:** internal
**Phase/Area:** Step 3 (spawn subagents) / Step 4 (reconcile)

**Issue:** The standard strategy says "subagents own exclusive claim titles" so no two write the same file. But with background agents running concurrently AND a set of pre-scaffolded *shared* anchor pages (process page, central actors that several chapters discuss), multiple agents naturally want to enrich the SAME scaffold page (e.g. Iolo Morganwg is introduced in ch5 but his legacy runs through ch8; the central process page is relevant to every chunk). Concurrent edits to one file would corrupt it. The mitigation that worked cleanly: (a) assign each scaffold page to EXACTLY ONE agent for enrichment, listed explicitly in that agent's prompt; (b) forbid all agents from editing index.md/log.md and any page not in their list; (c) when an agent's range yields strong claims about a page another agent owns, have it append those claims (with quotes + target page) to a per-range claims file in scratchpad (claims_A.md etc.) rather than edit the shared page; (d) main thread integrates the claims files during reconciliation. Result: 0 edit collisions, 0 broken links, and the claims files surfaced genuinely valuable cross-chunk material (continental origins, convivial clubs) that would otherwise have been lost or duplicated.

**Suggested improvement:** Add an explicit note to the Deployed Subagent Strategy (Step 3) that when subagents run in the background (concurrent), each shared scaffold page must have a single named owner-agent, and non-owners route cross-page claims to a per-range claims file for main-thread integration in Step 4. This is stronger than "exclusive claim titles," which only covers newly-created pages, not shared anchors.

**Principle:** Parallel writers to shared mutable state need single-owner assignment, not just disjoint-creation namespaces. For concurrent agents, separate "pages you may edit" (exactly one owner each) from "claims you discovered for someone else's page" (write to a handoff file). The reconciling thread merges handoffs.

### Observation 34: Polemical/low-trust sources need an "artifact-mode" ingest variant

**Date:** 2026-07-01
**Session context:** Ingest of D'Souza, *The Big Lie* (2017) — a partisan polemic, not scholarship.
**Skill:** CLAUDE.md ingest workflow (Deployed Subagent Strategy)
**Type:** internal
**Phase/Area:** Step 1 scaffold / source-type handling

**Issue:** CLAUDE.md's Source-Type Handling covers Cambridge, primary translations, monographs, and archaeology — but not popular polemics/advocacy works. This ingest improvised a variant: (a) source page carries heavy reliability_notes plus an explicit "do not cite for factual claims" rule; (b) the book's claims are filed as a POSITION on a controversies/ page, not into period/event/actor pages; (c) subagents extract claims + verbatim quotes + rhetorical-method notes + checkable-assertion lists to scratchpad ONLY — all wiki writing stays on the main thread; (d) footprint kept deliberately small (source + controversy + one legitimate concept + cross-links). Worked well and kept the wiki's factual layer uncontaminated.

**Suggested improvement:** Add a "Polemics and advocacy works" bullet to Source-Type Handling codifying (a)–(d): ingest as historiographical artifact; claims become controversy-page positions; subagent output confined to scratchpad extraction; explicit do-not-cite rule on the source page.

**Principle:** A wiki's trust model should be enforced at ingest time by routing, not just annotation: low-trust sources get quarantined into controversy/concept pages where their claims are attributed positions, never merged into the factual record.

**Status:** ACTIONED — Applied to CLAUDE.md Source-Type Handling: artifact mode (weekly review 2026-07-03)

### Observation 35: Controversy pages must not adjudicate in wiki voice — curator adjudicates

**Date:** 2026-07-01
**Session context:** D'Souza *Big Lie* ingest. Curator rejected the wiki-voice verdicts I embedded ("untenable causal frame," "polemical revisionism" as a position label, resolved-by-consensus, a blanket do-not-cite rule) and endorsed the source's thesis, especially the Lockean-American-right point.
**Skill:** CLAUDE.md controversy-page rule + Division of Labor
**Type:** internal
**Phase/Area:** Controversy page authoring / source reliability_notes

**Issue:** CLAUDE.md already says "Do not adjudicate unless I explicitly ask" for controversies/, but on a source I judged low-trust I let adjudication leak into position labels, the frontmatter resolution_status, the assessment section's framing, and the source page's reliability_notes. The fix that satisfied both honesty and the protocol: neutral position labels; each position stated in its strongest form; a "shared factual ground, framed per side" section instead of a wiki-voice assessment; resolution recorded as "open as discourse / closed within the academy" (both facts, attributed); and a dated curator's note recording the owner's assessment. This partially supersedes Observation 34's "do-not-cite quarantine" — routing contested claims through the controversy page stands, but the blanket do-not-cite rule and pejorative genre framing do not.

**Suggested improvement:** When ingesting contested/advocacy sources: (a) position labels and resolution_status are adjudication surfaces too — keep them neutral; (b) state the opposing position in its strongest (steel-manned) form incl. where it touches mainstream scholarship; (c) record academy consensus as an attributed fact, not a verdict; (d) capture the curator's own assessment as a dated curator's note rather than absorbing or resisting it in wiki voice.

**Principle:** In a curator-directed wiki, the assistant's honesty obligation is to attribution accuracy (who holds what, on what evidence), not to rendering verdicts; adjudication hides in metadata and labels, not just prose.

**Status:** ACTIONED — Applied to CLAUDE.md Source-Type Handling: curator adjudicates (weekly review 2026-07-03)

### Observation 37: Artifact-mode ingest validated on a substantive polemic (Flynn), not just a shallow one (D'Souza)

**Date:** 2026-07-02
**Session context:** Ingest of Flynn, *The Roosevelt Myth* (1948) — polemical but heavily sourced Old Right revisionism.
**Skill:** CLAUDE.md ingest workflow (contested/advocacy-source handling; extends Observations 34/35)
**Type:** internal
**Phase/Area:** Source-type handling / reconciliation

**Issue:** Obs 34's artifact-mode variant (subagents extract to scratchpad only; main thread writes all wiki content; theses routed to controversy-page positions) was designed on D'Souza, where the book contributed almost no usable facts. Flynn is different: the interpretation is polemical but the documentation (insider memoirs, a Senate report, conference records) is substantial and wiki-worthy. The protocol still worked with one refinement: split each extract into FACTS (with named-source attribution chains) vs THESES vs QUOTES, then let facts flow onto event/actor/process pages as attributed material while only the theses are quarantined as controversy positions. Also useful: instructing extractors to flag the author's uncorroborated first-person claims separately (Flynn's Nye Committee testimony) — these are neither facts nor mere theses and belong in the source page's reliability analysis.

**Suggested improvement:** When codifying the "Polemics and advocacy works" bullet (obs 34), distinguish two grades: (a) thin polemics — minimal footprint, claims only as positions; (b) documented polemics — facts-with-attribution may enrich the factual layer, provided each borrowed fact carries the full attribution chain (author → his cited source) and per-page revisionist material is confined to attributed sections. Require extractors to separate facts/theses/quotes and to flag author-as-sole-witness claims.

**Principle:** The quarantine boundary for low-trust sources should run between a source's evidence and its inferences, not around the whole book — attribution chains, not blanket exclusion, are what keep the factual layer clean.

**Status:** ACTIONED — Applied to CLAUDE.md Source-Type Handling: FACTS/THESES/QUOTES split (weekly review 2026-07-03)

### Observation 38: Ebook-converted sources can contain internally duplicated passages — instruct subagents to flag, not re-extract

**Date:** 2026-07-02
**Session context:** Sternhell *Birth of Fascist Ideology* ingest (deployed-subagent strategy, 4 ranges)
**Skill:** Ingest workflow (CLAUDE.md Deployed Subagent Strategy, Step 2/3)
**Type:** internal
**Phase/Area:** Chunking / subagent extraction prompts

**Issue:** The range-2 subagent discovered that the ebook-converted text repeated ~330 lines of Chapter 3 opening material verbatim inside its slice (lines ~2252–2580 duplicated earlier content). The agent handled it well spontaneously — flagged the duplication and did not double-count claims — but nothing in the standard prompt asks for this, so a less careful agent could have extracted the passage twice, inflating claims and skewing chunk-weighting line counts.

**Suggested improvement:** Add one line to the standard subagent prompt template: "If you find passages duplicated verbatim within your slice (an ebook-conversion artifact), flag them and extract once." Optionally, at scaffold time, a cheap duplicate-block check (e.g., sort | uniq -d on longer lines) on conversion-derived texts before drawing chunk boundaries.

**Principle:** Ebook→text conversions introduce not only missing headings (Obs. 12) but content-level artifacts (duplicated blocks). Chunking and extraction assumptions that hold for clean PDF-derived text need a duplication guard for epub-derived text.
**Status:** ACTIONED — Applied to CLAUDE.md Step-3 prompt: flag internal duplication (weekly review 2026-07-03)

### Observation 39: Extraction subagents should flag name/date ambiguities — and it works

**Status:** ACTIONED — Applied to CLAUDE.md Step-3 prompt: flag entity mismatch (weekly review 2026-07-03)
**Date:** 2026-07-02
**Session context:** Whitman *Verdict of Battle* (2012) ingest, deployed-subagent strategy, 3 Sonnet agents
**Skill:** Deployed Subagent Strategy (CLAUDE.md ingest workflow)
**Type:** internal
**Phase/Area:** Step 3 subagent prompts / Step 4 reconciliation

**Issue:** The main thread scaffolded `battle-of-fontenoy-1745` from the book's introduction ("Malplaquet, Leuthen, Fontenoy"), but two subagents independently discovered that nearly all of the book's "Fontenoy" references are to Fontenoy-en-Puisaye (841 CE, Carolingian succession) — a different battle that already had its own wiki page. Both agents flagged the mismatch explicitly instead of force-filing claims under the given target name, letting the main thread route the 841 material correctly and add mutual disambiguation lines.

**Suggested improvement:** Add one line to the standard subagent prompt template: "If material near-matches a target page name but the entity differs (different date, person, place), file it under Miscellaneous with an explicit mismatch flag rather than under the target." This session's agents did it unprompted; make it a guaranteed behavior.

**Principle:** Scaffold names are hypotheses formed before reading; extractors are the first to see disconfirming evidence. Explicitly licensing them to contradict the scaffold's naming converts silent misfiling into cheap, visible flags.

### Observation 40: Repair wikilinks with the Edit tool, not sed — pipe delimiters and frontmatter break

**Status:** ACTIONED — Applied to CLAUDE.md Step-5 Edit-not-sed for wikilinks (weekly review 2026-07-03)
**Date:** 2026-07-02
**Session context:** Evans, The Third Reich in Power ingest — Step 4/5 link reconciliation
**Skill:** Ingest workflow (CLAUDE.md Deployed Subagent Strategy, Step 5 lint)
**Type:** internal
**Phase/Area:** wikilink repair after renaming/creating actor pages

**Issue:** Two sed-based bulk link repairs introduced artifacts: (1) a sed replacing \[\[actors/emanuel-moravec| inside quoted YAML frontmatter produced malformed entries ("Emanuel Moravec [[|Emanuel Hácha]]"); (2) using | as both sed delimiter and wikilink display separator silently failed ("unknown option to s"), and a follow-up # -delimited sed with a typoed replacement left a stray "g" in a cross-links line. Each required a manual fix pass and re-running the checker.

**Suggested improvement:** For link repairs in files with piped wikilinks or quoted frontmatter, use the Edit tool with exact old/new strings (or sed with # delimiter and a verbatim-checked replacement), then always re-grep the exact edited lines before re-running the checker.

**Principle:** Bulk regex edits on structured markup (YAML frontmatter, [[target|display]] links) fail in quiet, syntax-corrupting ways; targeted exact-string replacement is slower but self-verifying.

### Observation 41: Duplicate canonical event pages discovered mid-ingest (second-world-war-1939 vs world-war-ii-1939-1945)

**Date:** 2026-07-02
**Session context:** Evans, *Third Reich in History and Memory* ingest — while verifying link targets for scaffold pages, found TWO full WWII event pages: events/second-world-war-1939.md (38 inbound links) and events/world-war-ii-1939-1945.md (108 inbound), both with complete frontmatter and narrative.
**Skill:** CLAUDE.md ingest workflow (Step 1 scaffold / Step 5 lint) + lint workflow
**Type:** internal
**Phase/Area:** Link-target verification / wiki hygiene

**Issue:** The naming convention says events are `[event-name]-[start-year].md`, which both arguably satisfy under different names. Successive ingests have enriched both pages independently (this session added Kershaw/Kennedy material to second-world-war-1939 while adolf-hitler.md links world-war-ii-1939-1945), deepening the fork. The wikilink checker cannot catch this class of defect — both targets resolve.
**Suggested improvement:** Add a "duplicate canonical page" check to the lint workflow (heuristic: near-synonymous titles / same date_start+date_end+event_type in frontmatter), and at ingest Step 1 require a one-grep synonym check before accepting any high-traffic page name. When Mark next requests a lint pass, propose merging the WWII pair (canonical: world-war-ii-1939-1945 by inbound count, or second-world-war-1939 by naming convention — needs his call).
**Principle:** Link checkers verify resolution, not identity; a wiki can silently fork its most important pages when two valid names both exist. Dedupe needs a semantic check (title/date collision), not just a broken-link check.

**Status:** ACTIONED — Applied to CLAUDE.md lint duplicate-canonical-page check (weekly review 2026-07-03)

### Observation 42: `cat >>` appends silently create orphan pages when the target path is wrong — verify existence before appending

**Date:** 2026-07-02
**Session context:** Evans *Third Reich at War* ingest; appending attributed Evans sections to ~30 existing pages via shell heredocs
**Skill:** CLAUDE.md Deployed Subagent Strategy (Step 4 reconciliation)
**Type:** internal
**Phase/Area:** main-thread reconciliation / page updates

**Issue:** An append targeted `wiki/actors/religion-in-germany-1870-1945.md` but the real page lives in `wiki/processes/`. `cat >>` silently created a new headerless file in actors/, discovered only by a later existence check. Same-session near-misses: schema validator would not have flagged it as the file had no frontmatter to validate oddly (it appeared as an orphan).

**Suggested improvement:** When batch-appending to existing pages, first verify each target with `test -f` (or generate the file list from `ls`), or use the Edit tool (which errors on unread/missing files). A one-line guard per append is cheap; a stray orphan page corrupts the wiki silently.

**Principle:** Shell append semantics (create-if-missing) are wrong for update-only workflows; prefer tools that fail loudly on missing targets.

### Observation 43: Part-aligned chunking can strand off-theme narrative inside a thematic range — run a main-thread expected-topics sweep after subagents return

**Date:** 2026-07-02
**Session context:** Evans *Third Reich at War* ingest; 7 ranges aligned to the book's Parts
**Skill:** CLAUDE.md Deployed Subagent Strategy (Steps 2–4)
**Type:** internal
**Phase/Area:** chunk-boundary design / reconciliation

**Issue:** The Bagration/D-Day/Warsaw Uprising military narrative sat physically inside Part 6 ("German Moralities"); the subagent, briefed on moralities/resistance themes, skipped it, and the Part 7 agent correctly reported its range started after the July Plot. The gap surfaced only because the Warsaw Uprising anchor page still had placeholders; a grep across caches located the material and the main thread recovered it.

**Suggested improvement:** Add a reconciliation-step check: list the major expected events of the book's period, grep each across all cache slices, and confirm each is claimed in some claims file. Also brief each subagent to extract everything in its range, not just its range's headline theme.

**Principle:** Chunk boundaries define ownership, but thematic prompts bias extraction; ownership must be exhaustive ("everything in your lines"), and the reconciler should verify coverage against an expected-topics list, not just merge what came back.

### Observation 44: Anchor-scaffold dedup check missed an existing page under a different slug pattern (expulsion-of-germans-1945 vs proposed 1944-1950) — recurrence of Obs 21

**Date:** 2026-07-02
**Session context:** Evans *Third Reich at War* ingest; created events/expulsion-of-germans-1944-1950.md although events/expulsion-of-germans-1945.md existed from the Evans-2015 ingest earlier the same day
**Skill:** CLAUDE.md Deployed Subagent Strategy (Step 1 scaffold)
**Type:** internal
**Phase/Area:** create-vs-update decision

**Issue:** The pre-creation greps covered obvious keywords (katyn, wannsee, etc.) but not every proposed page title; the expulsion page existed with a different year-suffix and was only caught when the index.md entry for the 2015 ingest was read during bookkeeping. Merged and deleted the duplicate; links repointed.

**Suggested improvement:** Before creating ANY new page in reconciliation, run a stem-based search (e.g., `ls wiki/*/ | grep -i <stem>` plus `grep -ril <stem> wiki/sources wiki/index.md`) for each proposed slug — especially for topics likely touched by same-week parallel ingests. Year suffixes vary; search the stem, not the slug.

**Principle:** Duplicate risk is highest exactly where coverage is densest (recently ingested adjacent sources); dedup checks must be stem-based and include index.md/log.md, which record pages faster than directory listings register in memory.

### Observation 45: Word-count sanity check before scaffolding — epub extraction silently missing half the book

**Status:** ACTIONED — Applied to CLAUDE.md Step-1 wc -w intake check (weekly review 2026-07-03)
**Date:** 2026-07-02
**Session context:** Ingest of Hartz, *The Founding of New Societies* (1964)
**Skill:** New skill candidate / CLAUDE.md ingest workflow (internal)
**Type:** internal
**Phase/Area:** Step 1 scaffold / pre-ingest intake

**Issue:** The raw/ text file for a ~350-page multi-author volume contained only ~16,000 words (95KB): the epub→txt conversion captured only Part One (Hartz's 3 theoretical chapters) and dropped Part Two entirely (Hartz's US chapter + the Morse/McRae/Rosecrance country studies). TOC listed all chapters, so a TOC-only scaffold read would not have caught it. Caught only by an explicit wc -w sanity check against expected book length.

**Suggested improvement:** Add a mandatory intake check to the ingest workflow: before scaffolding, compare `wc -w` against expected length (~250–350 words/page × page count); if the ratio is badly off, grep for each TOC chapter heading in the body to find where the text actually ends. Note incompleteness on the source page and in reliability_notes.

**Principle:** Converted ebooks fail silently and partially — the TOC survives even when body chapters don't. A 10-second word-count-per-page ratio check is the cheapest guard against ingesting (and logging as complete) a fraction of a book.

### Observation 46: Extraction subagents self-report partial slice coverage — read the completion summary for coverage bounds and gap-fill

**Status:** ACTIONED — Applied to CLAUDE.md Step-3 prompt: report actual coverage (weekly review 2026-07-03)
**Date:** 2026-07-02
**Session context:** Ingest of Hayek, The Constitution of Liberty (Definitive Edition) via Deployed Subagent Strategy, 7 range agents + 1 gap-fill
**Skill:** Ingest workflow (CLAUDE.md Deployed Subagent Strategy, Step 3)
**Type:** internal
**Phase/Area:** Subagent monitoring / recovery

**Issue:** The chunk-1 agent hit a read cap and reported covering only lines 1–1424 of its 2,556-line slice, stating the uncovered remainder explicitly in its completion summary. Because the summary declared its coverage bounds, the main thread could immediately spawn a cheap gap-fill agent scoped to exactly the uncovered lines (1425–2557) instead of discovering the gap at reconciliation or losing the material silently. A second agent (chunk 6) reported coverage "through ~line 3000" of 3,492 — a softer signal needing a judgment call on whether the tail was substantive.

**Suggested improvement:** Add to the Step-3 subagent prompt template: "In your completion summary, state the exact line range you actually covered; if you did not reach the end of your slice, say so explicitly." And add to Step 3 monitoring: on any completion summary reporting partial coverage, spawn a gap-fill agent scoped to the uncovered lines (or main-thread recover if small) before reconciliation.

**Principle:** Coverage gaps are invisible unless the worker is required to declare them; a one-line self-report of actual bounds converts silent data loss into a cheap, immediately actionable fix.

### Observation 47: Filing step must verify the exact ingested file (duplicate-twin trap)

**Date:** 2026-07-02
**Session context:** User asked why *The Coming of the Third Reich* and *The Road to Serfdom* were "ingested but still in raw/ root." Vol I turned out to be scaffold-only (correctly unfiled), but Serfdom revealed a real defect: the collection held two copies (a 5,374-line abridged twin and the 13,527-line Caldwell Definitive Edition actually used for the ingest); the filing step moved the *wrong twin* into `4. Modern Times/`, leaving the ingested Caldwell copy in the root queue.
**Skill:** CLAUDE.md ingest workflow — Step 6 filing
**Type:** internal
**Phase/Area:** Bookkeeping/filing

**Issue:** The filing instruction says "file the source" but doesn't force verification that the moved file is byte-identical to the one the caches were cut from. With near-duplicate filenames, a plausible-looking twin got filed and the real source stayed in the queue, making the root queue misleading (it looked un-ingested).

**Suggested improvement:** At Step 6, file by the exact path used to build the cache slices (echo it from the session, or `wc -l` match against the cache total); if a same-work twin exists in raw/, move it to `raw/_duplicates/` in the same step. A scaffolded-but-unfinished ingest should also leave a breadcrumb (e.g., "claims pending" note already on the source page — check log.md for `ingest-complete` before assuming filed=done).

**Principle:** Filing by title match instead of by the exact ingested path silently corrupts the queue when duplicates exist; always file the path you read from, and quarantine twins at the same moment.

**Status:** ACTIONED — Applied to CLAUDE.md Step-6 file-by-exact-path (weekly review 2026-07-03)

### Observation 48: Content-filter blocks are not predicted by atrocity-density triage

**Status:** ACTIONED — Applied to CLAUDE.md Step-2 triage (weekly review 2026-07-03)
**Date:** 2026-07-02
**Session context:** Ingest of Griffin, *Modernism and Fascism* (2007), Deployed Subagent Strategy (5 Sonnet agents)
**Skill:** CLAUDE.md ingest workflow (atrocity-dense triage rule, Step 2)
**Type:** internal
**Phase/Area:** Step 2 chunking / Step 3 failure recovery

**Issue:** The range that got output-blocked by content filtering was ch. 3–4 — the *anthropology/theory* chapters (sacred canopy, Terror Management Theory, rites of passage), with only incidental Nazi/Holocaust references — while the genuinely atrocity-dense ch. 11 (routed to main thread per triage) and the ch. 7–10 fascism chapters all completed fine in subagents. The triage heuristic (route atrocity-dense documentation to main thread) did not predict which range would be blocked.

**Suggested improvement:** Keep the triage rule (it correctly protects the highest-stakes material), but treat subagent content-filter blocks as effectively stochastic on any fascism/genocide-adjacent source: the recovery path (main thread reads the cache slice and extracts, per Step 3) is the real safeguard and worked losslessly here. Do not over-invest in predicting blocks at chunking time.

**Principle:** When a failure mode is cheap to recover from and hard to predict, invest in the recovery path rather than the prediction heuristic.

### Observation 49: raw/ is user-curated and can change mid-session — slice to scratchpad early, re-verify paths after time gaps

**Date:** 2026-07-02
**Session context:** Law, Legislation and Liberty I–III ingest
**Skill:** CLAUDE.md ingest workflow (deployed subagent strategy)
**Type:** internal
**Phase/Area:** Step 2 — cache-slice preparation
**Status:** ACTIONED — Applied to CLAUDE.md Step-2 slice-to-scratchpad-early / raw mutable (weekly review 2026-07-03)

**Issue:** The separate Vol 1 and Vol 3 .txt files in raw/ disappeared mid-ingest. Initially read as an anomaly; the user clarified he deleted them deliberately in favor of the combined 3-volume PDF. The ingest was unaffected only because the combined PDF had already been converted and sliced to the scratchpad.

**Suggested improvement:** In Step 2, cut the cache slices to the scratchpad immediately after locating the source, before scaffolding — the user actively curates raw/ during sessions, so treat it as mutable. Re-verify a source path right before any read that follows a gap in time, and when a file disappears, ask/check for deliberate curation before treating it as an error.

**Principle:** Shared directories the user actively curates are not stable inputs; copy dependencies to session-local storage first, and prefer "the user changed it deliberately" over "something broke" as the first hypothesis.

### Observation 50: Filename/content mismatch — queue file labeled Rawlinson but contains Fomenko "History: Fiction or Science?"

**Date:** 2026-07-02
**Session context:** User query: "ingest George Rawlinson - The Five Great Monarchies of the Ancient Eastern World". Per CLAUDE.md mandatory task-observer activation + Deployed Subagent Strategy at start of ingest session. Initial file stats and sampling (head, grep for structure) performed to begin Step 1 scaffold before any agent spawn or deep read.
**Skill:** CLAUDE.md ingest workflow (Deployed Subagent Strategy Step 1/6, Top_100_Structural_Sources.md queue management, filing hygiene)
**Type:** internal
**Phase/Area:** Pre-ingest diagnosis / source acquisition verification / Step 6 filing prevention

**Issue:** The only file present matching the requested title is `raw/George Rawlinson - The Five Great Monarchies of the Ancient Eastern World Or, The History, Geography, and Antiquities of Chaldea, Assyria, Babylon, Media, and Persia.md` (57k lines, 1.9 MB). Its internal content begins with Fomenko's "History: Fiction or Science?" (full multi-volume Chronology set header, "Jesus Christ was born in 1053 A.D.", Scaligerian chronology critique, "consensual history is a finely woven magic fabric of intricate lies", 7 chronology volumes description, Delamere Publishing). Header even records "Source file: [Rawlinson name].pdf" and "Pages/chapters: 626" (the converter used the filename for Title but the PDF content was Fomenko). No "Rawlinson", "First Monarchy", "Chaldea" descriptive content from the real 19th-c. work exists. Searches of workspace and broader /home found no Rawlinson PDF or alternate .md/.txt. Wiki has no source page or pages created from it; only incidental references to Henry C. Rawlinson (decipherer, brother) and a WWI general.
**Suggested improvement:** (1) Strengthen pre-scaffold verification in CLAUDE.md Step 1 and "source acquisition": immediately after locating the candidate file for a Top_100 entry, perform a quick content signature check (first 20 lines + author/title phrase grep for the *expected* work, not just filename). If mismatch, halt and surface before any TOC reading or cache slicing. (2) Treat filename-based headers from ebook_to_txt.py as untrusted; always cross-validate against internal text (look for "by George Rawlinson" or "The Five Great Monarchies" actual prose vs. Fomenko-style opening). (3) When such a mismatch is found, quarantine the file (move to raw/_duplicates/ with note) and update the queue entry in Top_100 with "[FILE MISMATCH - actual: Fomenko Chronology; correct Rawlinson PDF required]". (4) Add a one-line "source fingerprint" comment or frontmatter on source pages once ingested. This is recurrence of twin/identity problems (obs 47) and raw mutability (49).
**Principle:** Filenames and conversion metadata are not authoritative for work identity. In a large collection ingested from archives (zlib etc.), label drift is common; the ingest workflow must verify *content* against the intended bibliographic identity at the first tool use, before any investment in scaffolding or subagent ranges. A wrong file under a high-priority Top_100 name blocks the actual priority source and risks ingesting the wrong historiography (here, 19th-c. positivist ANE specialist vs. 21st-c. extreme revisionist).

**Reference file:** raw/George Rawlinson - The Five Great Monarchies of the Ancient Eastern World Or, The History, Geography, and Antiquities of Chaldea, Assyria, Babylon, Media, and Persia.md (misidentified)


### Observation 51: User directed "ingest it!" for the Fomenko file queued under Rawlinson name; applied artifact-mode + main-thread primary authorship

**Date:** 2026-07-02
**Session context:** Follow-up to "ingest George Rawlinson..." query. User confirmed file location in raw/ then explicitly said "ingest it!" after diagnosis that content is Fomenko 2003 "History: Fiction or Science?" (not Rawlinson). Task-observer active; obs 50 already documented the mismatch.
**Skill:** CLAUDE.md ingest workflow + artifact-mode handling (obs 34/35/37)
**Type:** internal
**Phase/Area:** Source-type handling / user directive vs. strict bibliographic identity

**Issue:** User overrode the filename mismatch by directing ingest of the actual file present. The content is a major fringe chronology revisionist work (New Chronology), not the 19th-c. ANE history listed in Top_100. Standard factual ingest would contaminate the wiki; full quarantine would ignore explicit user direction.
**Suggested improvement:** When user explicitly directs ingest of a file whose content differs from its queued/Top_100 label, (a) ingest the actual content under correct bibliographic identity, (b) document the label drift prominently on the source page and in log/Top_100, (c) default to artifact-mode for the actual work type (here: polemical/revisionist), (d) still perform pre-scaffold content signature check and record it. This preserves user direction while protecting the factual layer.
**Principle:** User direction takes precedence on what material to process, but the assistant's responsibility for accuracy of representation and protection of the wiki's epistemic standards remains; correct attribution + routing (artifact/contested) satisfies both.

**Reference file:** raw/George Rawlinson - The Five Great Monarchies... .md (actual content Fomenko)


### Observation 52: Content-filter triage should flag atrocity-DISCOURSE chapters, not only atrocity-documentation chapters
**Status:** ACTIONED — Applied to CLAUDE.md Step-2 triage — atrocity discourse (weekly review 2026-07-03)

**Date:** 2026-07-02
**Session context:** Ingest of Evans, *In Defence of History* (1997) via Deployed Subagent Strategy (3 Sonnet agents)
**Skill:** CLAUDE.md ingest workflow (Step 2 atrocity-dense triage rule)
**Type:** internal
**Phase/Area:** Step 2 chunk triage / Step 3 failure recovery

**Issue:** Chunk C (Ch. 6–8) was blocked by the output content filter even though the book is a historiographical monograph containing no graphic atrocity documentation — the trigger was evidently the chapter *discussing* Holocaust denial (quoting denial claims like "the death camps were an anti-German hoax" in order to refute them) plus de Man's antisemitic wartime writings. The triage rule as written targets chapters that *document* atrocities; this range was not flagged because it only *debates* them. Main-thread recovery worked exactly as specified (read the 3,163-line cache slice directly, composed pages at full fidelity).

**Suggested improvement:** Extend the Step-2 triage checklist: also flag ranges dense in atrocity *discourse* — Holocaust-denial refutations, quoted extremist/antisemitic texts, apologetics analysis — even in methodology/historiography books, and route them to the main thread by default.

**Principle:** Output filters react to reproduced content regardless of the reproducing text's stance; quoting denial literature to demolish it trips the same wire as quoting perpetrator documents. Triage on surface content, not authorial intent.

### Observation 53: Parallel ingest sessions clobber shared wiki pages — Write-tool full rewrites are the hazard

**Date:** 2026-07-02
**Session context:** Payne *Fascism: Comparison and Definition* (1980) ingest, running concurrently with a separate session ingesting Griffin's *Fascism* (Oxford Reader 1995) — both touching the same fascism-batch pages
**Skill:** CLAUDE.md Deployed Subagent Strategy (Step 4 reconciliation) / cross-session hygiene
**Type:** internal
**Status:** ACTIONED — Applied to CLAUDE.md Step-4 Edit-append on parallel-session pages (weekly review 2026-07-03)
**Phase/Area:** Page integration writes

**Issue:** This session created `concepts/theories-of-fascism.md` as a scaffold, then later replaced it with a full Write. In between, the concurrent Griffin session Edit-appended its own section to the same file (it appears in its "Pages updated (12)" list). The full Write clobbered that addition silently — discovered only because the Griffin session's log entry and source page claimed an update the file no longer contained. Its scratch caches could not be located, so the lost section was reconstructed only in summary form with an explicit loss note on the page. Edits by the parallel session to *other* shared pages (generic-fascism) survived because both sessions used anchored Edits there, which interleave safely.

**Suggested improvement:** During ingest integration, (1) prefer anchored Edit/append over full-file Write for any page that other sessions may plausibly touch (any page in an active topic batch); reserve Write for brand-new files in the same turn they are scaffolded; (2) before a full-file Write of a page scaffolded earlier in the session, re-read the file (or check mtime) to detect intervening external edits; (3) after finishing, cross-check other same-day log.md entries claiming updates to pages this session rewrote.

**Principle:** In a multi-session wiki, a full-file Write is a last-writer-wins race; the observation-log's check-then-act-then-verify numbering discipline applies equally to content pages — verify after writing that nobody else's claimed update was erased.

### Observation 54: Content filter blocked the *definitional* fascism chapters — treat fascism-studies texts as filter-prone regardless of atrocity density

**Date:** 2026-07-02
**Session context:** Payne 1980 ingest; subagent for chs. 1–3 (definitional typology, 19th-c. antecedents, movement comparison — minimal atrocity content) died with "Output blocked by content filtering policy" after 4 tool uses; chs. 4–5 and 6–9 agents (with far more violence/genocide discourse) completed fine
**Skill:** CLAUDE.md ingest workflow (Step 2 atrocity-dense triage rule); reinforces Observations 48 and 52
**Type:** internal
**Status:** ACTIONED — Applied to CLAUDE.md Step-2 — fascism sources filter-prone (weekly review 2026-07-03)
**Phase/Area:** Chunk triage / subagent spawning

**Issue:** Filter blocks remain unpredicted by atrocity-density triage: the *least* graphic range of a fascism book was the one blocked, likely on ideological-doctrine reproduction (fascist programs, Nazi Twenty-Five Points, racial-doctrine exposition). Main-thread recovery worked exactly as designed (range read directly, integrated at full fidelity, other agents unaffected).

**Suggested improvement:** For fascism/extremist-ideology sources, assume any range can be blocked; keep ranges sized so single-range main-thread recovery stays cheap (this session's ~2,000-line ranges were right), and don't spend effort predicting which range will trip the filter.

**Principle:** The triage rule's routing logic (recover, never respawn or soften) is validated; its *prediction* logic is not — plan for random block placement in ideology-dense sources.

### Observation 55: Scaffold step should include a duplicate-page pre-check; agents keep tripping over existing duplicates

**Status:** ACTIONED — Applied to CLAUDE.md Step-1 duplicate pre-scan (weekly review 2026-07-03)
**Date:** 2026-07-02
**Session context:** Paxton *Europe in the Twentieth Century* ingest (10 extraction + 3 integration subagents)
**Skill:** Deployed Subagent Ingest workflow (CLAUDE.md)
**Type:** internal
**Phase/Area:** Step 1 (scaffold) / Step 4 (reconcile)

**Issue:** Three independent extraction agents each separately discovered and flagged the same pre-existing duplicate pages (charles-de-gaulle.md vs de-gaulle-charles.md; french-indochina under both processes/ and actors/), burning tokens re-detecting a known-class problem, and each had to guess which to link.

**Suggested improvement:** In Step 1, before spawning agents, run a quick surname-collision scan over the page list for the actors the ingest will touch (e.g. grep both name orders) and state the canonical name in every agent prompt; queue duplicates for main-thread merge in Step 4.

**Principle:** Pre-resolving naming ambiguity once on the main thread is cheaper than letting N agents each rediscover and work around it.

### Observation 56: Subagent chunk briefs must not assert chapter content beyond what the TOC supports

**Date:** 2026-07-02
**Session context:** Flynn *Country Squire in the White House* (1940) ingest, 2-agent artifact-mode extraction
**Skill:** Deployed Subagent Strategy (CLAUDE.md ingest workflow)
**Type:** internal
**Phase/Area:** Step 3 — subagent prompt drafting

**Issue:** The CSQ-B brief described Ch. IV "The Crisis" as covering the 1937–38 recession (inferred from the chapter title + book position); the chapter actually covers the 1933 banking crisis. The agent correctly extracted the real content and flagged the mismatch, but a less careful agent could have force-fitted extraction to the wrong frame or wasted effort hunting for absent material.

**Suggested improvement:** When drafting chunk briefs from TOC titles alone, phrase content descriptions as expectations ("likely covers X — verify against the text; extract what is actually there"), not assertions. Alternatively, spot-read the first ~10 lines of each chapter while drawing boundaries — it costs seconds and grounds the brief.

**Principle:** Subagent instructions are treated as ground truth by the agent; any unverified inference embedded in them becomes a potential extraction bias. State inferences as hypotheses and instruct agents to privilege the text over the brief (which CSQ-B did — the "flag ambiguities" instruction plus obs-39-style self-reporting worked as designed).

**Status:** ACTIONED — Applied to CLAUDE.md Step-3 prompt: briefs as expectations (weekly review 2026-07-03)

### Observation 57: Two-stage subagent ingest — extraction by line-range, integration by page-ownership

**Status:** ACTIONED — Applied to CLAUDE.md Step-4 two-stage variant (weekly review 2026-07-03)
**Date:** 2026-07-03
**Session context:** Shirer *Rise and Fall of the Third Reich* ingest (~1,600 pp) into a wiki with dense pre-existing coverage (Evans/Kershaw/Taylor)
**Skill:** New skill candidate / CLAUDE.md ingest workflow refinement
**Type:** internal
**Phase/Area:** Deployed Subagent Strategy, Steps 3–4

**Issue:** For a well-trodden source, most claims are UPDATEs to existing pages, and many extraction ranges target the same pages (goebbels-joseph appeared in 6 of 11 ranges). Applying updates directly from range-partitioned agents would collide. This session ran a second parallel wave: 4 integration subagents partitioned by EXCLUSIVE WIKI-PAGE ownership (not by source range), each grepping ALL claims files for its owned slugs, restricted to the Edit tool (no full rewrites). Main thread kept the filter-prone/atrocity pages plus all new-page creation it had scaffolded.

**Suggested improvement:** Document the two-stage pattern in CLAUDE.md's Deployed Subagent Strategy: Stage 1 extraction agents own disjoint line-ranges and write claims files only; Stage 2 integration agents own disjoint page sets and read all claims files. Cross-cutting pages (Hitler, Goebbels, Göring) must be explicitly assigned to exactly one integrator or the main thread.

**Principle:** Partition parallel writers by the resource they mutate, not by the resource they read. Extraction mutates claims files → partition by source range; integration mutates wiki pages → partition by page. One partition scheme cannot safely serve both stages.

### Observation 58: Chunk boundaries drawn on subsection greps can leave inter-agent gaps at chapter openings

**Date:** 2026-07-03
**Session context:** Deployed-subagent ingest of Taylor, *A History of the Vietnamese* (13 chapters, 320k words) — CLAUDE.md World History Wiki
**Skill:** CLAUDE.md ingest workflow (Deployed Subagent Strategy, Step 2 "Split the book by disjoint line-ranges")
**Type:** internal
**Phase/Area:** Step 2 boundary-drawing / Step 4 reconciliation

**Issue:** I located chapter boundaries by grepping distinctive *subsection* titles from the TOC and set each agent's start line at the first subsection I picked. For Chapter 6 I picked "Dao Duy Tu and southern mobilization," but the chapter actually opened with three earlier generic-titled subsections ("The north," "The south," "War begins"). Agent C (Ch4–5) correctly stopped at the true chapter-6 start and treated the opening as out-of-scope; Agent D (Ch6–8) began at my later marker. The result was a ~950-line gap (the Nguyen Hoang / north–south-divergence setup, foundational to the Trinh/Nguyen pages) that no agent covered. A second smaller gap appeared where Agent B stopped short of its assigned range. Both were caught only because agents reported exact coverage; main-thread gap-reads confirmed them enrichment-level, not page-breaking.

**Suggested improvement:** When choosing a grep marker for a chunk's start boundary, use the **chapter heading itself** (or the *first* subsection listed under it in the TOC), not a memorable mid-chapter subsection. If chapter headings aren't standalone lines in the body (as here — they lived only in the TOC), pick the earliest subsection title under each chapter and verify with a ~5-line spot-read that nothing chapter-relevant precedes it. Add to Step 4 a routine "boundary-seam check": for each adjacent agent pair, confirm agent N's actual end line abuts agent N+1's start line with no gap, using their reported coverage.

**Principle:** Disjoint line-ranges are only truly disjoint-and-complete if adjacent boundaries *abut*. Markers chosen for memorability tend to sit inside a section, so two agents can each correctly exclude the material between the true boundary and the marker, silently dropping it. Boundaries should be set at section *starts* and seams verified pairwise at reconciliation.

---

## 2026-07-08 — Captivating "Native American History" filename/content mismatch

### Observation 59: Filename/content mismatch — queue file labeled Native American History (Captivating) but contains American History omnibus

**Date:** 2026-07-08
**Session context:** User query: "ingest Native American History A Captivating Guide to the Long History...". Task-observer session-start protocol run; Step-1 word-count intake and content fingerprint before scaffold.
**Skill:** CLAUDE.md ingest workflow (Deployed Subagent Strategy Step 1, source acquisition verification)
**Type:** internal
**Phase/Area:** Pre-ingest diagnosis / source acquisition verification
**Status:** OPEN

**Issue:** The only matching file in raw/ is `Native American History A Captivating Guide to the Long History of Native Americans Including Stories of the Wounded Knee… (Captivating History [History, Captivating]) (z-library.sk, 1lib.sk, z-lib.sk).txt` (~34,450 lines, ~206k words, converter header claims 1162 pages and the Native American title). Internal content is **not** that book. Body title page and TOC are *American History: A Captivating Guide to the History of the United States…* (© 2020), an 8-part omnibus: (1) History of the United States, (2) American Revolution, (3) Civil War, (4) History of Chicago, (5) Roaring Twenties, (6) Great Depression, (7) Pearl Harbor, (8) Gulf War. Native content is incidental survey material only (Part 1 Ch.1 "The People Who Were There First", Ch.9 "Horrors for the Natives", brief Wounded Knee passage ~lines 2930–3060). No Hiawatha-focused Native American History guide exists in the text. Converter Title/Source-file header used the *filename*, not content identity. Recurrence of Obs 50 (Rawlinson→Fomenko).

**Suggested improvement:** (Already partially in Obs 50.) Keep content-fingerprint as a hard gate before cache-slice or scaffold. When filename and body title diverge, surface immediately with: labeled-as, actual-content identity, word count, and options (quarantine / ingest-as-actual / wait for correct file). Do not invent a Native American source page from incidental US-survey chapters.

**Principle:** Filenames and ebook-converter metadata are not bibliographic identity. In zlib-sourced collections, label drift is common; verify content against the intended work at first tool use before any ingest investment.

**Reference file:** raw/Native American History A Captivating Guide to the Long History of Native Americans Including Stories of the Wounded Knee… (Captivating History [History, Captivating]) (z-library.sk, 1lib.sk, z-lib.sk).txt

### Observation 60: Subagents emit wikilinks inside YAML frontmatter list fields, creating malformed/broken links

**Date:** 2026-07-08
**Session context:** Ingesting Warwick Ball, *Rome in the East* (Deployed Subagent Strategy). Creation subagents drafted 27 new pages from a shared CREATE_BRIEF that told them to "link only real page slugs" and "do NOT wrap descriptive phrases in [[ ]]."
**Skill:** task-observer / ingest workflow (CLAUDE.md Deployed Subagent Strategy)
**Type:** internal
**Phase/Area:** Step 3 subagent prompts + Step 5 lint

**Issue:** Despite the brief's linking rules, a creation subagent wrote `opposed_by: [[[praetorian-guard]]]` in a page's YAML frontmatter — a wikilink placed inside a YAML list, producing a malformed triple-bracket token the wikilink checker flags as broken (praetorian-guard has no page). Other agents linked plausible-but-nonexistent slugs in body text (`phoenicia` vs the real `phoenicians`; `hadrians-wall`, which is only a person page `hadrian`). The brief's rule addressed *body* over-linking but did not explicitly forbid wikilinks in *frontmatter list fields*, where entity names should be plain strings (the schema's `opposed_by`/`affiliated_with`/`key_events` fields are descriptive lists, not link fields). The `--files` scoped wikilink check caught all of them cheaply.

**Suggested improvement:** Add one line to the ingest subagent brief: "Frontmatter list fields (`opposed_by`, `affiliated_with`, `key_events`, `causes`, `consequences`, etc.) take **plain-text entity names, not wikilinks** — never put `[[ ]]` inside a YAML `[...]` list. Only body prose carries wikilinks, and only to slugs you can confirm exist." Also standardise a post-integration `wikilink_checker.py --files <touched set>` pass (not just `--changed`, which is polluted by other sessions' modified files) as the canonical "0 new broken links" check.

**Principle:** Subagents follow positive linking rules but miss the structural boundary between link-bearing prose and plain-text frontmatter; the brief must name that boundary explicitly. And in a repo where many files are concurrently dirty, broken-link verification must be scoped to the *explicit touched-file list*, since `--changed`/git-status-based scoping conflates other sessions' work and buries the ingest's own new links.

### Observation 61: Locate chapter boundaries via uppercase chapter-opener lines when OCR strips heading structure

**Date:** 2026-07-08
**Session context:** Ingesting Laiou & Morrisson, *The Byzantine Economy* (Cambridge Medieval Textbooks, 2007) via the Deployed Subagent Strategy; needed disjoint chapter-aligned line ranges for 4 extractor agents.
**Skill:** Ingest Workflow — Deployed Subagent Strategy (CLAUDE.md Step 2)
**Type:** internal
**Phase/Area:** Step 2 — splitting the book by disjoint line-ranges

**Issue:** The epub→md conversion lost heading markup: TOC section subtitles ("Demography", "Exchange"...) appeared only in the TOC block, and running-page headers repeated the chapter title dozens of times (page decoration), so neither TOC-line grepping nor running-header frequency reliably marked where each chapter's *body* began. Bare page-number anchors were also absent. What DID work: the converter preserved chapter openers as ALL-CAPS lines (e.g. "SHIFT TO MEDIEVAL STRUCTURES", "CONTROLLED EXPANSION (EARLY"), each immediately preceded by the Roman numeral. Grepping for distinctive uppercase fragments of each chapter title gave exact, unambiguous body-start line numbers in one pass.

**Suggested improvement:** Add to the boundary-drawing toolkit: when converted text has lost heading structure, try `grep -nE` for ALL-CAPS fragments of chapter titles (and standalone Roman-numeral lines) to find true body chapter-starts, rather than relying on TOC line numbers (which sit in the front-matter block) or running-header frequency (page decoration that repeats every ~86 lines and conflates with real headings). Verify with a 3-line context read at each hit.

**Principle:** OCR/ebook conversion degrades *structure* differently from *content*: headings often survive as capitalization even when markdown/indentation is gone. Detect boundaries from the surviving signal (case), not the lost one (markup/whitespace), and cross-check that a candidate marker is a one-time body event, not a repeating page ornament.

### Observation 62: Partial-ingest source pages can claim integration that is not on disk

**Date:** 2026-07-08
**Session context:** Re-ingesting Wickham *Framing the Early Middle Ages* after a 2026-07-02 scaffold left incomplete status notes
**Skill:** CLAUDE.md Deployed Subagent Strategy / project ingest workflow
**Type:** internal
**Phase/Area:** Step 1 status audit before re-running a "partial" source
**Status:** OPEN

**Issue:** The source page `wickham-framing-the-early-middle-ages-2005.md` asserted Ranges 03–12 "integrated" and listed place pages (Lucca, Vorbasse, etc.) as if created, but `rg -l wickham-framing` hit only index/log, most listed places were MISSING, cache was gone, and frontmatter still had pages_created: 0. Trusting the narrative would have skipped re-extraction.

**Suggested improvement:** At ingest start, when a source page exists with non-complete status, require a mechanical audit: (1) count pages citing the source slug; (2) existence-check every "created" slug listed on the source page; (3) presence of claims/cache dirs. Treat prose status as aspirational until the audit passes. Only then decide resume vs full re-extract.

**Principle:** Status prose on source pages is not evidence of completion; completion is verified by on-disk page existence, citation counts, and frontmatter tallies.

### Observation 63: Agent FOCUS narrower than its slice forces a gap-fill pass

**Date:** 2026-07-08
**Session context:** Ingesting Formichi, *Islam and Asia* (2020). Chapter chunks were cut one-agent-per-chapter by line range, but the Ch.1 agent was given a FOCUS ("Central Asia / Ghaznavid / Samanid / overland") narrower than its slice, which also contained the chapter's "Muslims of Maritime Asia" section. The agent correctly extracted only its focus and flagged the maritime section as unextracted, forcing a scoped main-thread gap-fill agent.
**Skill:** CLAUDE.md ingest workflow (Deployed Subagent Strategy, Step 3)
**Type:** internal
**Phase/Area:** chunk briefing / focus scoping

**Issue:** When a per-agent chunk equals a full chapter but the prompt's FOCUS covers only part of that chapter's content, the agent honours the focus and leaves the rest of its exclusive slice unextracted — creating a silent coverage hole that only surfaces because a well-behaved agent flags it.
**Suggested improvement:** In Step 3, add: an agent's FOCUS must span its entire exclusive line-range. If a chapter mixes two topics you'd rather brief separately, either (a) give one agent both topics as its focus, or (b) split the line-range so each focus maps to its own disjoint slice. Never hand an agent a slice wider than its stated focus.
**Principle:** Exclusive-ownership only guarantees coverage if each owner's mandate covers all of what it owns. A focus narrower than the slice reintroduces the very gap the disjoint-partition was meant to prevent.

### Observation 64: Roman-numeral person slugs can be the wrong entity (tsar vs pope)

**Date:** 2026-07-08
**Session context:** Ingest of Logan, *A History of the Church in the Middle Ages*
**Skill:** Internal: wiki-ingest / CLAUDE.md naming + duplicate pre-scan
**Type:** internal
**Phase/Area:** Step 1 scaffold / duplicate-page pre-scan

**Issue:** Existence checks for `nicholas-i` and `alexander-iii` returned true, so extractors and the source-page CANONICAL list treated them as the medieval popes. Both pages are actually nineteenth-century **Russian emperors**. Integrators correctly refused to clobber them and created `pope-nicholas-i` and `alexander-iii-pope`; similarly `hildegard` was Charlemagne's queen, not Hildegard of Bingen. The pre-scan only checked slug presence, not identity (title/period/region).

**Suggested improvement:** In the ingest pre-scan / CANONICAL_NAMES step, when a slug exists, **read the page title and period** (first ~15 lines). If the entity is wrong, mint a disambiguated slug (`pope-X`, `X-of-place`) and record it before spawning extractors. Add to CLAUDE.md "duplicate-page pre-scan": existence is necessary but not sufficient — verify identity for shared regnal names and roman numerals.

**Principle:** A green "EXISTS" on a slug is not a green light to link if the page is a different person. Shared personal names and roman numerals across cultures are high-risk collision zones; identity-check the title, not just the filename.

### Observation 65: Duplicate-page pre-scan must cover transliteration variants

**Date:** 2026-07-08
**Session context:** Formichi *Islam and Asia* ingest. A subagent created actors/chagatai-khanate.md while an established actors/chaghatay-khanate.md already existed (4 inbound links, Hodgson-sourced). The Step-1 duplicate pre-scan missed it because it only checked the "chagatai" spelling and a "chag*khanate" glob that the agent's chosen slug happened to match but the canonical "chaghatay" did not surface in the relevant grep. Caught only during main-thread integration when the mongol-conversion event page referenced the other spelling.
**Skill:** CLAUDE.md ingest workflow (Step 1 duplicate-page pre-scan)
**Type:** internal
**Phase/Area:** duplicate pre-scan / naming reconciliation

**Issue:** The pre-scan checks name-order variants (surname-first vs given-first) but not TRANSLITERATION variants of the same non-English name (chaghatay/chagatai, quran/koran, mohammed/muhammad, umayyad/omayyad). Islamic/Central-Asian/Chinese material is especially prone to this. Result: a subagent mints a near-duplicate under a different romanization.
**Suggested improvement:** Add to the Step-1 duplicate pre-scan: for every non-Latin-origin entity the ingest will touch, grep the wiki for plausible transliteration variants (vowel swaps a/o/u, gh/g, q/k, y/i/ai endings, doubled consonants) BEFORE spawning, and state the canonical existing slug in the agent prompt. When an ingest is heavy in one naming tradition (Arabic, Persian, Turkic, Chinese pinyin/Wade-Giles), run a variant sweep as a matter of course.
**Principle:** A duplicate check keyed on one spelling of a transliterated name gives false confidence; the canonical page can exist under a romanization you didn't grep. Enumerate spelling variants, not just word-order variants.

### Observation 66: Extraction agents over-propose granular NEW pages on well-trodden large-volume ingests

**Date:** 2026-07-08
**Session context:** Ingesting *The Cambridge Economic History of the Greco-Roman World* (Scheidel/Morris/Saller 2007, 28 chapters, ~401k words) into a wiki already dense in classical-antiquity coverage. Deployed-subagent strategy: 11 extraction agents → claims files → 5 integration agents.
**Skill:** CLAUDE.md ingest workflow (Deployed Subagent Strategy) — relates to existing memory [[ingest-subagent-overlinking]]
**Type:** internal
**Phase/Area:** Step 3 extraction prompts / Step 4 main-thread reconciliation

**Issue:** Extraction subagents reliably proposed too many fine-grained NEW pages from single chapters — e.g. Ch.4 (Household & Gender) yielded four proposed pages (household-economy, women-property-rights, guardianship-of-orphans, gendered-labor-division); other chapters proposed standalone roman-frontier-economy, roman-manufacturing-and-mining, christian-economic-ethics, roman-per-capita-income-GDP-controversy, roman-slave-mode-of-production pages. The main thread consolidated each cluster into one parent page (ancient-household-economy; roman-provincial-economy absorbing the frontier zone; late-roman-economy absorbing Christian ethics; roman-consumption folding in the GDP debate as a historiography subsection). This is distinct from the known wikilink over-bracketing pattern — it is over-fragmentation at the *page* level. Left unconsolidated it would have produced ~35 thin pages instead of 21 substantive ones.

**Suggested improvement:** In extraction-agent prompts, keep the instruction to *propose* target pages but explicitly tell agents to prefer folding a chapter's sub-topics into ONE consolidated page and to mark finer splits as "optional sub-sections, main thread's call" rather than as separate page proposals. Reserve the create/split decision for the main thread's Step-4 reconciliation (or, in the two-stage variant, pre-decide the consolidated page set during Step-1 scaffolding and pass it to integrators as the canonical target list — which worked well here: the 5 integrators were each handed an explicit "CONSOLIDATE into ONE page, do NOT create separate tiny pages" instruction and complied cleanly).

**Principle:** Bulk extractors optimize for capturing everything they see and therefore over-split; page-granularity is a structural/taxonomy decision that must stay with the main thread. Give subagents a pre-decided consolidated target list, not license to mint pages — the same principle as reserving naming/linking decisions for the main thread, applied one level up at page creation.

### Observation 67: Full multi-volume survey mislabeled by split-paperback filename

**Date:** 2026-07-08
**Session context:** Ingesting Boardman/Griffin/Murray *Oxford History of the Classical World*
**Skill:** CLAUDE.md ingest / word-count intake (Deployed Subagent Strategy)
**Type:** internal
**Phase/Area:** Step 1 intake / source identification
**Status:** OPEN

**Issue:** The raw file was named *…Greece and the Hellenistic World.md* (the paperback split title), but the TOC and body contained the **full** 32-chapter classical survey including Rome (chs 16–32 + Envoi). Treating the filename as scope would have under-chunked Rome and mis-filed the source as a Greece-only volume.

**Suggested improvement:** At intake, always reconcile **filename vs TOC chapter list** for multi-author Oxford/Cambridge paperbacks that were split for reprint; state the actual coverage on the source page and in the Top_100 note. Do not size ranges from the short title alone.

**Principle:** Collection filenames are not bibliographic authorities — TOC/body structure is. Split-series reissues are a recurring trap for under-scoping large multi-author volumes.

### Observation 68: OCR numeral corruption is a distinct intake risk from word-count truncation

**Date:** 2026-07-08
**Session context:** Ingesting Osborne (ed.), *Classical Greece 500–323 BC* (2000) via Deployed Subagent Strategy (4 extraction + 5 integration Sonnet agents).
**Skill:** CLAUDE.md ingest workflow (Deployed Subagent Strategy, Step 1 intake check / Step 3 extraction-prompt standing instructions)
**Type:** internal
**Phase/Area:** Step 1 word-count intake check; Step 3 subagent standing instructions

**Issue:** The source passed the word-count intake check cleanly (~103k words, ratio healthy, not truncated) — but the PDF→md conversion had pervasively corrupted *numerals*: talent sums, tribute totals, troop/population counts, dates, and interest rates were dropped or garbled throughout (e.g. "in the s", "[X],000 talents", blank casualty figures). All four extraction agents independently flagged this and reconstructed figures from context, correctly marking them uncertain. Because I had pre-emptively put a "hedge all reconstructed numerals; state only canonical figures as exact" rule in every extraction and integration prompt, no wrong precise figure reached a live page — but that rule was added ad hoc this session, not from the workflow.

**Suggested improvement:** Add numeral-integrity to the Step 1 intake check as a *separate* signal from length ("spot-grep the body for blank/broken numerals in a few number-dense pages"), and make "flag every reconstructed numeral; never assert an OCR-derived figure as exact — hedge or omit; state only independently canonical figures as exact" a *standing* line in the Step 3 extraction-prompt and Step 4/Stage-2 integration-prompt boilerplate, alongside the existing coverage-report / entity-mismatch / internal-duplication standing instructions.

**Principle:** Passing the length-based intake check certifies completeness, not fidelity. OCR/ebook conversions degrade the highest-stakes, least-redundant tokens (numbers) precisely where prose context can't reconstruct them, so numeral hedging must be a default posture for every converted source, not a per-session afterthought.

### Observation 69: Wikilink checker's --changed mode is polluted by a dirty working tree; isolate new links via --all + per-file awk extraction

**Date:** 2026-07-08
**Session context:** Ingesting Keegan, *Graffiti in Antiquity* (2014). Needed to prove "0 new broken links" for the ~15 pages the ingest created/edited.
**Skill:** CLAUDE.md ingest workflow (Step 5 lint/validate)
**Type:** internal
**Phase/Area:** Lint & validate — proving 0-new broken links

**Issue:** `wikilink_checker.py --changed` scopes to git-changed files, but the working tree already carried ~430 pre-existing modified files (visible in the session-start git status). So `--changed` reported 103 broken links spanning many files the ingest never touched — useless for isolating *this* ingest's contribution. The global total (956) is likewise dominated by a large pre-existing baseline. The reliable method was: run `--all` once to a temp file, then `awk -v f="path.md:" 'BEGIN{s=0}/:$/{s=($0==f)}s'` per each page the ingest actually created/edited. This surfaced exactly the per-page broken links, showing the ingest introduced only one new one ([[imhotep]]), which was then de-linked.

**Suggested improvement:** In CLAUDE.md Step 5, note that `--changed` is unreliable when the working tree is already dirty with unrelated modifications (common here — the repo is frequently mid-edit). Recommend the `--all` + per-file awk-extraction pattern (grep/awk the checker's `--all` output for each page in the ingest's own created/updated set) as the cheap way to prove 0-new without a stash dance. The existing stash-comparison tip addresses the 50-file print cap; this addresses a different failure (dirty-tree pollution of --changed).

**Principle:** To attribute lint deltas to your own change set, filter the checker's *full* output down to the exact files you touched — do not trust a git-diff-scoped flag when the working tree contains unrelated in-flight edits.

### Observation 70: Duplicate pre-scan must cover cross-language / epithet name variants

**Date:** 2026-07-08
**Session context:** Ingesting Fisher, *Rome, Persia, and Arabia* (2020). Scaffolding named a new actor page `mavia` for the Arab queen; an existing canonical page `queen-mawiyya` already covered her (Latin "Mavia" vs Arabic "Mawiyya" rendering of the same name). A page-writing subagent had already begun creating the duplicate before the main thread caught it via a tail-read of a related page's Related list.
**Skill:** CLAUDE.md ingest workflow (Step 1 duplicate-page pre-scan)
**Type:** internal
**Phase/Area:** Step 1 scaffold — duplicate-page pre-scan

**Issue:** The pre-scan heuristics in CLAUDE.md name two vectors: both surname/given orders and synonymous event titles. They do not explicitly name the vector that bit here — the SAME person under a different-language transliteration or an epithet-vs-name form (Mavia/Mawiyya; also latent risk with Alamoundaros/al-Mundhir, Arethas/al-Harith, Dhu Nuwas/Joseph/Yusuf). The existing page also used a `queen-` prefix the ingest's naming convention (surname-given) would never have guessed.

**Suggested improvement:** Add to the Step-1 duplicate pre-scan an explicit check for cross-language/transliteration and epithet variants of every person/place the ingest will touch, especially for ancient Near Eastern figures who appear under Greek, Latin, Syriac, and Arabic names. Concretely: before naming any new actor page, grep the wiki for the figure's alternate renderings and for descriptive-prefix slugs (`queen-`, `king-`, `saint-`). Cheaper than a mid-run subagent recall.

**Principle:** Duplicate detection must key on the *referent*, not the string. For multilingual source domains a single historical person routinely has 3–4 attested name forms; a pre-scan that only permutes word order misses the most common duplicate vector in exactly the domains (antiquity, translated primary sources) this wiki ingests most.

### Observation 71: When an ingest's new pages dangle-link a page-worthy entity, grep for pre-existing dangles of the same slug before deciding create-vs-delink

**Date:** 2026-07-08
**Session context:** Ingesting Mark R. Cohen, *Under Crescent and Cross* (Deployed Subagent Strategy). New/updated pages referenced several non-existent slugs (cairo-geniza, al-hakim, granada-massacre-1066, kiddush-ha-shem, radhanites, umar-ibn-al-khattab, al-mansur-almohad, fatimids). Standard Step-5 broken-link resolution is create-the-page-or-delink-to-plain-text.
**Skill:** CLAUDE.md ingest workflow (Deployed Subagent Strategy, Step 4–5 tie-together/lint)
**Type:** internal
**Phase/Area:** Step 5 broken-link resolution / create-vs-delink triage

**Issue:** Deciding whether a dangling wikilink target deserves its own page or should be delinked is usually judged only by the *current* ingest's needs. But `grep -rl "\[\[<slug>"` across the whole wiki before deciding revealed that `cairo-geniza` was *already* dangle-linked by an unrelated existing page (`processes/afro-eurasian-world-system.md`) — so creating it resolved both the new reference and a pre-existing broken link in one move. Separately, `fatimids` looked missing but a whole-wiki `find`/grep showed the page existed under a different slug (`fatimid-caliphate`) with many inbound links, so the correct fix was to re-point the link, not create a duplicate.

**Suggested improvement:** Add to Step 5: before resolving any dangling wikilink introduced by an ingest, run two whole-wiki greps on the bare slug — (1) `grep -rl "\[\[<slug>"` to see if *existing* pages already dangle the same target (if so, creating the page clears a pre-existing broken link too, strengthening the create decision and improving the wiki beyond the ingest's footprint), and (2) a `find -iname "*<root>*"` / alias check to catch the entity already existing under a different slug (re-point, don't duplicate). This converts create-vs-delink from a local judgment into a wiki-wide one.

**Principle:** A broken link introduced by new work is an opportunity to survey the wiki's *existing* dangling references and canonical-slug aliases for the same entity; resolving links against the whole graph (not just the current change set) both prevents duplicate pages and opportunistically repairs latent breakage.

### Observation 72: Preface/front-matter can fall outside first body-range cache when slicing from key-dates

**Date:** 2026-07-08
**Session context:** Ingesting Woolf *Rome: An Empire's Story* via two-stage Deployed Subagent Strategy
**Skill:** Project ingest workflow (CLAUDE.md Deployed Subagent Strategy) — internal
**Type:** internal
**Phase/Area:** Step 2 cache slicing / Stage 1 extraction
**Status:** OPEN

**Issue:** Range 1 was cut from line 378 (first "key dates in chapter i") so subagents never saw the Preface (lines ~56–210), which held the book's load-bearing theses (empire as pattern/resonance; longevity as modern puzzle; hard-matter roads/ports). The agent correctly reported "Preface missing from this cache." Main thread recovered the preface after Stage 1.

**Suggested improvement:** When drawing the first body range, include Preface/Introduction/Notes on method if they sit before chapter 1 key-dates or chapter openers — either extend range 1 upward to the Preface start, or cut a dedicated main-thread "front-matter" slice and extract it before or with Stage 1. Do not assume "body starts at first key-dates block."

**Principle:** Structural front matter often carries the author's controlling thesis; range maps drawn only from chapter/key-date markers systematically drop it unless the scaffold step explicitly includes it.

### Observation 73: wikilink_checker --changed is polluted by a broadly-dirty tree; prove 0-new via --all + per-file awk on session slugs

**Date:** 2026-07-08
**Session context:** Ingest of Jiwa, *The Fatimids: 1* (21 new pages, 7 updated) into the World History Wiki.
**Skill:** World History Wiki ingest workflow (CLAUDE.md, "Lint and validate" / "proving 0 new broken links")
**Type:** internal
**Phase/Area:** Step 5 — Lint and validate

**Issue:** CLAUDE.md's guidance for proving "0 new broken links" prescribes a stash-comparison (move the change set aside, get a baseline total, restore, compare). The `wikilink_checker.py` now exposes a `--changed` flag, which looks like a shortcut — but it scopes to the *entire git-dirty tree*, not the current session's files. Because the wiki working tree is very often already broadly dirty (this session began with ~hundreds of modified files from prior sessions), `--changed` surfaced 139 broken links across unrelated pages (alexander-iv, eastern-zhou, etc.), none from this ingest — making it useless for isolating *my* new breakage. The stash-comparison also gives only a total, not a per-file attribution.

**Suggested improvement:** Add to the CLAUDE.md lint step: to prove 0-new broken links for an ingest, run `wikilink_checker.py --all > /tmp/wlc.txt` once, then filter to the session's own created/edited slugs with a per-file awk block (match `^slug.md:` start, stop at the next `^*.md:$`, print `→` lines between). This gives precise per-page confirmation that each *new* page has zero broken outbound links and isolates any breakage introduced into *updated* pages, cleanly separating it from the pre-existing dirty-tree noise that both `--changed` and a bare total conflate. Keep the stash-comparison only as a fallback when a global new-vs-old total is specifically wanted.

**Principle:** When a repo's working tree is chronically dirty, "changed-files" tooling scoped to git status is unreliable for attributing new problems to the current task — scope verification to the explicit list of artifacts the task produced, not to VCS dirtiness. Per-artifact attribution beats aggregate deltas when isolating a session's own contribution.

### Observation 74: Duplicate-page pre-scan must cover morphological name variants, not just name-order

**Date:** 2026-07-08
**Session context:** Ingesting Fagan & Durrani *World Prehistory* (10th ed., 2020). Two Stage-1-scaffolded "new" actor pages (`chimu`, `toltecs`) turned out to duplicate existing canonical pages created by prior/concurrent ingests (`chimor`, `toltec`). The wikilink checker did NOT catch them (both slugs resolve), exactly as CLAUDE.md warns. Caught only when reading `index.md` during bookkeeping, which listed the prior CHNPA-III ingest's Andean pages.
**Skill:** CLAUDE.md ingest workflow (Step 1 duplicate-page pre-scan) — project-internal, not the open-source task-observer skill.
**Type:** internal
**Phase/Area:** Deployed Subagent Strategy — Step 1 pre-scan; Step 4 reconciliation.

**Issue:** The Step-1 duplicate pre-scan (as written in CLAUDE.md) emphasizes checking *both name orders* for persons (de-gaulle-charles / charles-de-gaulle) and synonymous event titles. It does not explicitly call out **morphological/orthographic variants of the same entity name**: Spanish-vs-anglicized (`chimor`/`chimu`) and singular-vs-plural (`toltec`/`toltecs`). My pre-scan checked candidate slugs like `chimu`/`chimu-empire` and `toltecs` and found nothing, so I authorized creation — but the canonical pages lived under the *other* form. Subagents (correctly instructed to only create pre-named pages) created the dupes as told; the fault was in the pre-scan, not the agents.

**Suggested improvement:** Extend CLAUDE.md's Step-1 duplicate pre-scan bullet to include: (a) singular/plural and Anglicized/indigenous-or-Spanish spelling variants of the same polity/culture (toltec(s), chimu/chimor, aztec/mexica, inca/inka); (b) a fast `index.md` grep for the entity as the *first* check, since index.md is the running catalogue where prior/concurrent ingests announce newly-created pages (it surfaced both dupes instantly). Cheaper than N agents each re-discovering the collision, and the wikilink checker structurally cannot flag it.

**Principle:** When a validator provably cannot catch a class of error (here: duplicate canonical pages both resolve), the guard has to move upstream into a pre-flight scan — and that scan must enumerate the realistic *variant forms* of an identifier, not just one canonical form. For a knowledge base assembled by many parallel/serial agents, the shared running index is the authoritative "what already exists" oracle and should be consulted before creating any structural page.

### Observation 75: Subagents systematically stop short of assigned line-ranges, creating sub-range coverage gaps at chunk boundaries

**Date:** 2026-07-08
**Session context:** Deployed-subagent ingest of Freeman, *Egypt, Greece, and Rome* (401k-word survey, 7 disjoint range-partitioned extraction agents).
**Skill:** Ingest workflow (CLAUDE.md Deployed Subagent Strategy) / task-observer-adjacent
**Type:** internal
**Phase/Area:** Step 3 (spawn per-chunk extraction agents) + Step 4 (review/gap-fill)

**Issue:** 6 of 7 extraction agents (each assigned a ~4000-line cache slice) stopped extracting well before the end of their assigned range — reading ~2900–3550 of 4000 lines — even though CLAUDE.md already instructs them to "report actual coverage." They *did* report the shortfall honestly, but the shortfalls clustered at the *tail* of each slice, so the untouched tails lined up with the *heads* of the next agent's slice being fine, leaving systematic gaps precisely at chunk boundaries (e.g. Ch.10 colonization + the Sappho interlude fell in range_2's unread tail while range_3 started after it; Interlude 9 "Romans as Builders" and the substantive Legacies chapter fell in unread tails). Because content near chunk edges (interludes, chapter transitions) is exactly where distinctive/new-page-worthy material sat, the gaps disproportionately hit high-value content, requiring a consolidated main-thread recovery read of 4 separate sub-ranges.

**Suggested improvement:** When range-partitioning a large book, (a) deliberately OVERLAP adjacent slices by ~200–300 lines so a short-reading agent's tail gap is covered by the next agent's head, OR (b) size slices ~25% smaller than an agent can comfortably read (aim ~2500–3000 lines/agent for dense text, not 4000) so "read to the end" is achievable, AND (c) place known high-value boundary material (interludes, pivotal chapters) in the *interior* of a slice, never at its edge. Add to CLAUDE.md Step 2 (chunk-drawing): "Do not put an interlude/pivotal chapter at a slice boundary; overlap slice edges or undersize slices so tail-truncation cannot silently drop boundary content."

**Principle:** Honest coverage-reporting catches gaps but doesn't prevent them; when workers reliably under-run a fixed quota, the fix is to change the work-unit geometry (overlap or undersize) rather than to exhort harder. Systematic truncation at a consistent fraction of the quota produces *aligned* gaps at partition boundaries — the most dangerous kind, because boundaries are where transitions and summaries (high-value content) live.

### Observation 76: Target-partitioned parallel page-creation collides on the same entity under variant slugs

**Date:** 2026-07-08
**Session context:** Wiki-wide broken-link cleanup — 8 parallel agents partitioned by disjoint *target slug* each created pages for their missing-link targets.
**Skill:** Ingest/maintenance workflow (Deployed Subagent Strategy) — parallel page creation
**Type:** internal
**Phase/Area:** Fan-out page creation / duplicate prevention

**Issue:** Partitioning work by disjoint target *slug* does NOT prevent duplicate-entity creation, because the SAME real entity is frequently referenced under different slugs in different files, and those slug-variants land in different agents' batches. Result: the same person got created 2–3 times under name-order variants — `philip-sheridan` (batch 01) / `sheridan-philip` + `sheridan-philip-h` (batches 03/07); `stonewall-jackson` vs `thomas-j-jackson`; `george-pickett` vs `pickett-george-e`; `jeb-stuart` vs `stuart-jeb`; `gouverneur-warren` vs `warren-gouverneur-k`; plus new pages colliding with EXISTING canonical pages under a different order (`acheson-dean` vs existing `dean-acheson`, `urien-rheged` vs `urien-of-rheged`, `reliability-of-herodotus` vs existing `herodotus-reliability`). 10 duplicates across ~408 creates. Caught by a post-hoc name-token-set dedup scan (sort tokens, drop initials/particles/roman-numerals) — but roman numerals must NOT be dropped (that false-matched Alexander I–IV and Henry II/IV/V as dupes).

**Suggested improvement:** For any fan-out that CREATES pages keyed on free-form targets, add a **canonicalization pre-pass on the main thread before spawning**: normalize every target to a canonical slug (surname-first for persons, resolve against existing pages + aliases), collapse variant slugs to one owner, and pass each agent the *canonical* name to create plus the variant slugs to add as `aliases:`. Failing that, always run the token-set dedup scan (excluding roman numerals from the drop-list) as a mandatory Step-4 merge, deleting dupes and folding variant slugs into the survivor's `aliases:`. Add to CLAUDE.md's duplicate-page pre-scan guidance: "partition-by-target is not collision-safe for the same entity under different slugs; canonicalize target names before fan-out or dedup-by-name-token-set after."

**Principle:** Disjoint *work items* are not the same as disjoint *outputs*. When N workers each map an input to an output name they compute independently, two different inputs can map to the same real-world thing under different names — the partition prevents item-collisions but not entity-collisions. Deduplication must key on the entity's canonical identity, not on the input slug.
