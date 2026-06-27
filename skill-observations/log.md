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

### Observation 4: Explicit requirement to always run task-observer during file ingests

**Date:** 2026-06-25
**Session context:** User providing direct instruction after a major source ingest (Dumas Malone Jefferson and His Time Vol. 2) using the Deployed Subagent Strategy. User clarified that previous observation log entry was from another agent ("Claude") and stated the requirement: "I need you to always be running that skill when you're ingesting files".
**Skill:** task-observer + project ingest workflow (CLAUDE.md "Deployed Subagent Strategy")
**Type:** internal
**Phase/Area:** Activation / Integration with Ingest Workflow

**Issue:** During the Jefferson Vol. 2 ingest (large .txt + 7 subagents + main-thread reconciliation), task-observer was not automatically active from the beginning of the ingest work. The user had to explicitly invoke it later with a meta question. The user now states a hard requirement that task-observer must always be running when performing file ingests (especially the full Deployed Subagent Strategy process for books).

**Suggested improvement:** 
- Add an explicit mandatory first step in the CLAUDE.md "Ingest Workflow — Deployed Subagent Strategy" section: "Before doing any ingest work (reading source, creating caches, spawning subagents, or writing pages), invoke the task-observer skill."
- Update the project's root CLAUDE.md (or a dedicated "Ingest Protocol" subsection) to include the activation instruction from task-observer's own "Recommended Activation Setup".
- In future ingest sessions, the very first action after identifying the source file should be to ensure task-observer is loaded and will monitor the entire process (including subagent handoff, reconciliation, lints, filing, and git).
- Consider adding a short checklist at the top of every ingest session log entry or source page work: "task-observer active: yes".

**Principle:** When a user gives an explicit standing instruction about when a meta-monitoring skill must be active, that instruction must be turned into a structural, non-optional step in the relevant workflow documentation. "Always during ingests" is stronger than "at the start of task-oriented sessions" and must be enforced at the workflow definition level, not left to description matching or ad-hoc invocation.
### Observation 4: Explicit task-observer activation for Jefferson Vol 3 ingest (hard requirement enforcement)

**Date:** 2026-06-25
**Session context:** User request: "ingest jefferson and his time 03". Starting full Deployed Subagent Strategy ingest of Malone *Jefferson and the Ordeal of Liberty* (Vol. 3 of Jefferson and His Time). 21,062-line .txt source.
**Skill:** task-observer
**Type:** internal
**Phase/Area:** Activation / Ingest precondition (CLAUDE.md)

**Issue:** Per explicit standing instruction in CLAUDE.md ("Mandatory precondition — task-observer must always be active during file ingests") and user feedback ("You can't just load the metaskill without making a big deal about it?"), the meta-skill must be invoked visibly and structurally at the absolute start of any ingest before any source content is read, caches created, or subagents spawned. In the prior Vol 2 session it was activated reactively after user meta-question. Previous workflow relied on description matching or ad-hoc.

**Suggested improvement:** 
- Make invocation loud and documented: (1) read SKILL.md, (2) launch persistent monitor on log.md, (3) immediately append a numbered invocation observation, (4) mark in todo list and announce in session, (5) keep monitor running through all phases (scaffold reads, subagent spawns with rate-limit sleeps, reconciliation, lints, filing, git ops).
- Update CLAUDE.md "Ingest Workflow — Deployed Subagent Strategy" Step 0 to include these 5 concrete actions.
- For every ingest session, first terminal output or chat message should surface "Task-observer explicitly invoked and monitoring".

**Principle:** Standing user requirements for meta-monitoring during high-stakes, multi-agent workflows (ingests that create permanent wiki content and touch rate-limited subagent infrastructure) must be turned into non-skippable, self-documenting first actions with visible confirmation. "Making a big deal" is the enforcement mechanism that prevents the skill from being silently loaded or overlooked.

**Status:** OPEN


### Observation 5: Explicit task-observer activation for "ingest jefferson and his time 04" (Vol. 4)

**Date:** 2026-06-25
**Session context:** User request: "ingest jefferson and his time 04". Beginning Deployed Subagent Strategy for Dumas Malone's *Jefferson and His Time* Vol. 4 (~20k lines). Following hard CLAUDE.md precondition and prior explicit user requirement for visible activation *before* any source file content reads, /tmp caches, subagent spawns, page writing, lints, filing or git.
**Skill:** task-observer
**Type:** internal
**Phase/Area:** Activation / Ingest precondition (CLAUDE.md "Deployed Subagent Strategy")

**Issue:** Invocation must be loud, documented, and first: SKILL.md read (earlier), log reviewed for max obs# and recent Jefferson entries, source line count retrieved via wc (20,208 lines), prior wiki state for Jefferson/Malone surveyed via grep/index/log (Vols 1-3 ingested today with detailed bio + source pages + events). This append is the visible numbered confirmation before scaffold sampling of source.

**Suggested improvement:** Continue treating ingest as the canonical trigger for full visible activation checklist as outlined in prior obs.
**Principle:** Standing user requirement for meta-skill during ingests must produce self-documenting first action with chat-visible confirmation + log entry. "Task-observer explicitly invoked and monitoring" must precede source work.
**Status:** OPEN


### Observation 6: Explicit task-observer activation for "ingest jefferson and his time 05" (Vol. 5)

**Date:** 2026-06-25
**Session context:** User request: "ingest jefferson and his time 05". Beginning full Deployed Subagent Strategy ingest of Dumas Malone's *Jefferson and His Time* Vol. 5 ("Jefferson the President Second Term 1805-1809", 25,953 lines). Strictly following CLAUDE.md mandatory precondition and prior explicit user requirement: visible, documented, first action before reading source content (beyond wc for planning), creating /tmp caches, spawning subagents, writing pages, running lints, filing, or git operations.
**Skill:** task-observer
**Type:** internal
**Phase/Area:** Activation / Ingest precondition (CLAUDE.md "Deployed Subagent Strategy")

**Issue:** As with Vol 4, the metaskill must be invoked loudly at absolute start of ingest. SKILL.md read, log reviewed (max prior obs #5 from Vol 4), source line count via wc obtained, header sampled. This entry provides the numbered, self-documenting confirmation. Monitor will be launched immediately for visible streaming of observations throughout scaffold, range planning, staggered subagent batches (with sleeps), reconciliation, lints, bookkeeping, filing and commit.
**Suggested improvement:** Continue and refine the 5-point visible checklist (read SKILL, launch monitor, append numbered obs, todo list entry, announce) for every future ingest. Consider scripting a helper that does the activation sequence atomically.
**Principle:** User-mandated meta-monitoring for all file ingests must be non-skippable and produce immediate visible evidence (chat + numbered log entry + persistent monitor) before any substantive work on the source or wiki outputs. This prevents silent or retroactive activation.

**Status:** OPEN

### Observation 7: Explicit task-observer activation for "ingest alan turing: The enigma"

**Date:** 2026-06-25
**Session context:** User request: "ingest alan turing: The enigma". Beginning full Deployed Subagent Strategy ingest of Andrew Hodges' *Alan Turing: The Enigma* (33,842 lines; the definitive biography, #26 in Top 50 Biographies list). Strictly following CLAUDE.md mandatory precondition ("task-observer must always be active during file ingests") and prior explicit user requirement for visible, documented activation *before* reading source content (beyond wc/ls for planning), creating /tmp caches, spawning subagents, writing pages, running lints, filing the source, or git operations.
**Skill:** task-observer
**Type:** internal
**Phase/Area:** Activation / Ingest precondition (CLAUDE.md "Deployed Subagent Strategy" + INGEST-ACTIVATION.md)

**Issue:** Per standing rule in CLAUDE.md and INGEST-ACTIVATION.md, the meta-skill must be invoked visibly and structurally at the absolute start of any ingest. SKILL.md + INGEST-ACTIVATION.md read, current log tail reviewed (prior max Observation 6 from Jefferson Vol 5), persistent monitor launched on log.md (task 019f01a7-1c49-73b0-807c-63a7531a107c), no pre-existing turing-alan actor or bio confirmed via ls/grep, Processing List confirms priority bio source, biographies-hub.md + template read, source line count via wc obtained (33842 lines). This numbered append is the self-documenting confirmation. No source content sampled yet.

**Suggested improvement:** Enforce the 5-point checklist (1. read SKILL+INGEST-ACT, 2. launch persistent monitor, 3. append numbered obs, 4. todo_write entry for ingest, 5. announce "Task-observer explicitly invoked and monitoring") at the very first response for every future "ingest ..." request. Add a short "Activation complete" banner in chat before any wiki or source work.
**Principle:** The project's hard requirement makes task-observer activation a non-optional, first-class, auditable first step for all ingests; visible logging + monitor + announcement turns the rule into enforceable practice rather than aspirational description matching.

**Status:** OPEN

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
