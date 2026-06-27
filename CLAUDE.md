# CLAUDE.md — World History Wiki

## Overview

A persistent, LLM-maintained wiki covering world history from prehistory to the
present. The source collection (Bibliotheca Alexandrina, ~11,800 PDFs) is the raw
material. You read sources and build a structured, interlinked knowledge base. I
direct the analysis; you do all filing, cross-referencing, synthesis, and
bookkeeping.

Environment: Obsidian; all wiki files are markdown. Sources live in the collection
directory; the wiki lives in `wiki/`. **Never modify source files.** The ingestion
sequence, sourcing priorities, and gap analysis live in `Top_100_Structural_Sources.md`
(the sole active list).

---

## Task-Observer Activation (mandatory)

At the start of any task-oriented session (ingest, lint, query, or any tool-using
work), invoke the `task-observer` (`one-skill-to-rule-them-all`) skill **before**
reading source content or beginning work. It captures skill-improvement observations
and runs the session-start protocol (weekly-review check, observation log). When
loading any skill, also check `skill-observations/log.md` for OPEN observations
relevant to the work and apply their insight even if the skill file isn't yet updated.

---

## Core Design Principles

- **History is a network, not a tree.** Every page sits at the intersection of what,
  where, and when. Links must preserve all three dimensions — topical similarity alone
  does not justify a link.
- **Granularity is fractal.** The same moment can be one line on a period page, a full
  event page, or the anchor of a dozen sub-events. Create pages at whatever granularity
  the source and analytical value warrant; don't force one resolution level.
- **Causation is not sequence.** The schema distinguishes temporal succession from
  causal connection from correlation — different link types. Conflating them is the most
  common error in historical wikis. Use the link taxonomy precisely.
- **Historiography is first-class content.** How we know what we know — sources, biases,
  gaps, debates — belongs alongside the history. Every major period and event page gets
  a historiography section.
- **The collection has a known bias.** It is exceptionally strong for Greco-Roman
  antiquity, medieval Europe/Mediterranean, pre-modern East Asia (Asian Classics), and
  the ancient Near East; weak on sub-Saharan Africa, South/Southeast Asia, the post-1750
  world, the Americas (outside archaeology), and Russia/Eastern Europe. Flag this bias
  explicitly on period overviews for thin regions; write only what the sources support
  and note the gap.

---

## Directory Structure

```
wiki/
  index.md              # Master catalog — updated after every ingest session
  log.md                # Append-only record of all ingests, queries, lint passes
  overview.md           # Current coverage map and known gap register

  periods/              # Chronological overview pages (one per period in framework)
  events/               # Discrete bounded occurrences
  processes/            # Long-duration historical dynamics
  actors/               # People, states, dynasties, institutions, movements
  places/               # Geographic and political entities
  concepts/             # Analytical and historiographical frameworks
  comparisons/          # Cross-period/civilization comparisons (see comparisons-plan.md)
  controversies/        # Disputed interpretations and scholarly debates
  timelines/            # Standalone chronological reference pages
  queries/              # Filed answers to significant questions
  sources/              # One summary page per ingested source

  hubs/                 # High-resolution special sections (see Warfare/Biography Hubs)
    warfare/            # Tactical/operational battle and campaign analysis (West Point grade)
    biographies/        # Graduate-level analytic lives (detailed vs. summary actors/)
```

---

## Temporal Framework

Anchor every page to at least one period; use the period name in frontmatter `period`
fields. List all periods for events that span them.

| # | Period | Date Range |
|---|---|---|
| 1 | Deep Prehistory | before 3.3 million BP |
| 2 | Early Prehistory | 3.3 million–300,000 BP |
| 3 | Late Prehistory | 300,000–50,000 BP |
| 4 | Behavioral Modernity | 50,000–12,000 BP |
| 5 | Mesolithic | 12,000–9,500 BP |
| 6 | Neolithic | 9,500–3,000 BCE |
| 7 | Chalcolithic | 5,500–3,300 BCE |
| 8 | Early Bronze Age | 3,300–2,100 BCE |
| 9 | Middle Bronze Age | 2,100–1,550 BCE |
| 10 | Late Bronze Age | 1,550–1,200 BCE |
| 11 | Bronze Age Collapse | ~1,200–1,150 BCE |
| 12 | Early Iron Age | 1,200–800 BCE |
| 13 | Archaic Period | 800–500 BCE |
| 14 | Classical Antiquity | 500–31 BCE |
| 15 | Late Antiquity | 31 BCE–600 CE |
| 16 | Early Middle Ages | 600–1000 CE |
| 17 | High Middle Ages | 1000–1300 CE |
| 18 | Late Middle Ages | 1300–1500 CE |
| 19 | Early Modern | 1500–1700 CE |
| 20 | Age of Expansion | 1700–1800 CE |
| 21 | Long 19th Century | 1800–1914 CE |
| 22 | World Wars Era | 1914–1945 CE |
| 23 | Cold War | 1945–1991 CE |
| 24 | Contemporary | 1991–present |

---

## Regional Framework

Tag pages with the most specific applicable region; add parent regions as secondary tags.

```
Africa:      north-africa, sub-saharan-africa, east-africa, west-africa,
             central-africa, southern-africa, horn-of-africa
Americas:    north-america, mesoamerica, caribbean, andes, amazonia,
             southern-cone, eastern-north-america
Asia:        near-east, levant, mesopotamia, anatolia, iran-plateau,
             arabian-peninsula, central-asia, south-asia, southeast-asia,
             east-asia, china, japan, korea, steppe
Europe:      western-europe, northern-europe, eastern-europe, mediterranean,
             iberia, british-isles, balkans, scandinavia
Oceania:     australia, polynesia, melanesia, micronesia
Transregional: silk-road, indian-ocean, atlantic-world, mediterranean-world,
             eurasian-steppe
```

---

## Page Types and Formats

Each page type's frontmatter schema is below. Fill **all** fields. Required body
sections follow each schema.

### Period Page (`wiki/periods/`)
One page per period; regional sub-period pages are nested (e.g., `tang-dynasty.md`
under `early-middle-ages.md`).

```yaml
---
title: [Period Name]
period_number: [1–24]
date_range: [start–end with BCE/CE/BP]
regions_covered: []
major_themes: []
collection_coverage: [strong / moderate / weak / absent]
sources_ingested: [count]
last_updated: [YYYY-MM-DD]
tags: [period]
---
```
Required body: **Overview** (narrative summary) · **Major Developments** (key events,
processes, transformations) · **Key Actors** (linked) · **Geographic Scope** (regions
active this period) · **Transition** (what ended the prior period, what begins the next)
· **Historiography** (source quality, debates, recent revisionism, methods; for
prehistoric periods cover dating methods and confidence explicitly) · **Collection
Coverage Note** (honest statement of strengths and gaps for this period).

### Event Page (`wiki/events/`)
A discrete occurrence with identifiable bounds.

```yaml
---
title: [Event Name]
date_start: [YYYY, YYYY-MM-DD, or approximate]
date_end: [same as start if single moment]
date_precision: [exact / year / decade / quarter-century / century / approximate / disputed / unknown]
dating_method: [for prehistoric: radiocarbon / stratigraphy / genetic / linguistic / other]
period: []
region: []
location: []
actors_primary: []
actors_secondary: []
event_type: [battle / war / migration / revolution / collapse / treaty / discovery /
             epidemic / famine / religious / political / economic / cultural /
             transition / other]
scale_immediate: [local / regional / civilizational / hemispheric / global]
scale_consequential: [local / regional / civilizational / hemispheric / global]
causes: []
consequences: []
sources_ingested: [count]
last_updated: [YYYY-MM-DD]
tags: [event, period-name, region-name]
---
```
`causes` and `consequences` are mandatory — use `[[unknown]]` explicitly if genuinely
unclear; never leave blank. Required body: **Narrative** · **Causal Analysis** (with
explicit link types) · **Consequence Analysis** · **Actors** (linked) · **Historiography**
(if contested: positions, scholars, resolution status).

### Process Page (`wiki/processes/`)
A long-duration dynamic not bounded as a discrete event (feudalization, spread of Islam,
Atlantic slave trade, industrialization).

```yaml
---
title: [Process Name]
date_start: [approximate]
date_end: [approximate or "ongoing"]
date_precision: [century / generation / approximate]
period: []
region: []
process_type: [political / economic / demographic / religious / technological /
               cultural / environmental / ideological]
driven_by: []
produces: []
sources_ingested: [count]
last_updated: [YYYY-MM-DD]
tags: [process, period-name, region-name]
---
```
Required body: **Definition and Scope** (what it is and is not) · **Causal Drivers** ·
**Major Phases** (turning points) · **Geographic Spread** · **Interaction** (relation to
other processes) · **End Conditions** (what stopped/transformed it, or why it continues).

### Actor Page (`wiki/actors/`)
Any agent capable of action: persons, states, dynasties, empires, institutions, armies,
movements, religious organizations.

```yaml
---
title: [Actor Name]
actor_type: [person / state / dynasty / empire / institution / movement /
             organization / military-force / other]
date_start: [birth, founding, or first appearance]
date_end: [death, dissolution, or last appearance — "ongoing" if still exists]
period: []
region: []
affiliated_with: []
opposed_by: []
key_events: []
key_processes: []
sources_ingested: [count]
last_updated: [YYYY-MM-DD]
tags: [actor, actor-type, period-name, region-name]
---
```
The `actors/` page is the **concise network-oriented summary** (compact overview, role,
high-level key events/processes, brief counterfactual significance, full-but-concise
historiography, dense links). Very detailed analytic lives live in the **Biography Hub**
(`hubs/biographies/`) — see that section. Content focus by type:
- **Persons**: role/title, major decisions and consequences, counterfactual significance
  (what changes without this actor — analytical, not celebratory).
- **States/empires**: peak territorial extent, governing structure, economic base,
  military capacity, mechanisms of decline.
- **Institutions/movements**: founding conditions, structural features, how they shaped
  events and processes.

Every detailed biography declares `actor_page` pointing to its summary; the summary
carries a reciprocal link back.

### Place Page (`wiki/places/`)
A geographic/political entity persisting across time as a location for events.

```yaml
---
title: [Place Name]
place_type: [city / region / empire-territory / geographic-feature /
             trade-route / battle-site / other]
modern_equivalent: []
coordinates: [approximate lat/lon]
period_active: []
controlled_by: []
events_here: []
processes_here: []
sources_ingested: [count]
last_updated: [YYYY-MM-DD]
tags: [place, region-name, period-name]
---
```
Body: geographic description, history of control and settlement, why it mattered
(strategic/economic/religious/demographic), how its significance changed over time.

### Concept Page (`wiki/concepts/`)
Analytical frameworks and interpretive tools, both emic (used by historical actors) and
etic (applied by historians).

```yaml
---
title: [Concept Name]
concept_type: [analytical / periodization / historiographical / ideological /
               economic / political / social / cultural]
origin: [who coined it, when, in what context]
applies_to_periods: []
applies_to_regions: []
contested: [yes / no]
sources_ingested: [count]
last_updated: [YYYY-MM-DD]
tags: [concept]
---
```
Always distinguish emic from etic; always state limitations and critiques.

### Controversy Page (`wiki/controversies/`)
Genuine interpretive disputes between serious scholars — distinct from factual uncertainty.

```yaml
---
title: [Controversy Description]
dispute_type: [causation / periodization / scale / source-reliability /
               interpretation / counterfactual / moral-assessment]
period_involved: []
regions_involved: []
positions: []
resolution_status: [open / partially-resolved / resolved-by-consensus]
last_updated: [YYYY-MM-DD]
tags: [controversy]
---
```
Do not adjudicate unless I explicitly ask for analysis — record each position with its
best arguments and the scholars who hold it. **Standing controversies to create during
Phase 1–3 ingestion:** Bronze Age Collapse causes (~1200 BCE) · Fall of the Western Roman
Empire causes · pre-Columbian American population · Great Man vs. structural causation ·
reliability of Herodotus · Indo-European origins · geographic determinism (Diamond) and
its critics.

### Source Page (`wiki/sources/`)
One page per ingested source.

```yaml
---
title: [Source Title]
author: []
year: [publication year]
source_type: [primary / secondary / reference / series]
period_coverage: []
region_coverage: []
methodological_approach: [narrative / archaeological / quantitative /
                           diplomatic / social / economic / cultural / other]
reliability_notes: []
pages_created: [count]
pages_updated: [count]
ingested: [YYYY-MM-DD]
tags: [source]
---
```

---

## Link Types — Mandatory Distinctions

| Label | Meaning |
|---|---|
| `caused_by: [[X]]` | X is a direct causal antecedent |
| `contributed_to: [[X]]` | X is a partial or enabling cause |
| `preceded_by: [[X]]` | X came before temporally; causation not asserted |
| `followed_by: [[X]]` | X came after temporally; causation not asserted |
| `produced: [[X]]` | this directly caused or created X |
| `enabled: [[X]]` | this created conditions for X without direct causation |
| `concurrent_with: [[X]]` | simultaneous; relationship uncertain or absent |
| `part_of: [[X]]` | this is a sub-component of X |
| `contains: [[X]]` | X is a sub-component of this |
| `analogous_to: [[X]]` | structurally similar in different time/place |
| `contrasts_with: [[X]]` | explicitly different from X in important ways |

The `caused_by` / `preceded_by` distinction is the most critical. Never conflate temporal
sequence with causation.

---

## Scale Framework

| Scale | Definition |
|---|---|
| `local` | City, valley, or sub-regional |
| `regional` | Multi-city or multi-polity |
| `civilizational` | Full civilization or imperial system |
| `hemispheric` | Old World or New World broadly |
| `global` | Genuinely worldwide impact |

Every event page specifies both `scale_immediate` and `scale_consequential`.

---

## Chronological Uncertainty Protocol

| Flag | Meaning |
|---|---|
| `exact` | Documented to the day or year |
| `year` | Documented to the year; exact day unknown |
| `decade` | Known within a decade |
| `quarter-century` | Known within 25 years |
| `century` | Known within a century |
| `approximate` | Known within a few centuries; consensus exists |
| `disputed` | Scholars disagree significantly |
| `unknown` | No reliable dating available |

For prehistoric dates, always state the dating method and confidence interval. Never
present approximate dates as exact.

---

## Source-Type Handling

- **Cambridge Reference Series (CAH, NCMH, Cambridge World History)** — the most
  authoritative sources; multi-author peer-reviewed, 800–1,000 pages each. Use the
  Large-Volume Protocol; never read in one pass. On conflict, flag for a controversy
  page but give Cambridge presumptive weight unless the conflict is itself actively debated.
- **Primary Source Translations (Oxford World's Classics, Penguin Classics, Translated
  Texts for Historians, Translations from the Asian Classics)** — record original
  language, author's dates, translator's approach, known translation controversies.
  Cross-link heavily; note where translation choices affect interpretation. Usually
  under 400 pages, single pass.
- **Specialist Monographs (Brill, Routledge, Oxford Studies)** — most current scholarship.
  When one contradicts a Cambridge volume, flag for a controversy page (usually signals
  recent revisionism). Usually 200–400 pages (standard workflow); over 400, Large-Volume.
- **Archaeological Reports** — treat as primary evidence for prehistoric/ancient periods.
  When archaeology conflicts with textual sources, create a controversy page — often more
  significant than purely textual disputes.

---

## Ingest Workflow — Deployed Subagent Strategy (DEFAULT, as of 2026-06-22)

**Primary ingest method for all sources.** Parallelizes claim extraction across Sonnet
subagents while keeping all scaffolding, reconciliation, and validation on the main
thread. The Standard and Large-Volume protocols below are now **reference material** for
per-page schema, section logic, and historiography requirements — not separate workflows
to choose between.

Non-negotiable principle: **the main thread owns structure; subagents own bulk
extraction.** Subagents never decide taxonomy, naming, or cross-links — they fill claims
within boundaries the main thread already drew.

**Step 1 — Scaffold first, on the main thread.** Read enough (TOC, intro, conclusion,
targeted sampling) to: write the **source page** (with Section Plan for large volumes);
create the **key person/concept/place pages** everything links to; decide whether a
**detailed biography page** (`hubs/biographies/`) is warranted for biographical sources
and pre-establish its name; decide the **topic taxonomy** and **naming conventions** for
every page the ingest will create. Do not spawn any agent until naming conventions and
the set of linkable page names exist on disk — subagents inherit names, never invent
structural ones.

**Step 2 — Split the book by disjoint line-ranges.** Divide raw text into N contiguous,
non-overlapping chunks by line number.
- **Size N to the book, not a fixed number.** Base it on *body* length × density (exclude
  front matter, endnotes, bibliography, index — can be half the file). Rule of thumb: one
  agent per ~2,000–3,500 body lines; floor 2–3; up to 10 for very large/multi-volume
  references. **Do NOT default to 6** — a ~2,700-body-line book wants ~3 agents; over-
  splitting starves agents of context.
- **Weight chunks by content density and importance, not even boundaries.** Dense/pivotal
  stretches get their own agent (or multiple passes over one major section for dense,
  multi-doctrine material); lighter material combines into a larger range. Align edges to
  natural section/chapter boundaries only where it doesn't fight the weighting — content
  weight wins.
- Ranges must be **disjoint** — every line in exactly one chunk.

**Step 3 — Spawn one Sonnet subagent per chunk (staggered batches + background).** Use
the Agent tool with **`model: sonnet`** and `run_in_background: true`, one agent per
chunk. Each prompt must contain: its **exclusive line-range** (read only that range); the
**schema and naming conventions** from this file; the **established page names** it may
link to (Step 1); **exclusive ownership of the claim titles it creates** (distinct title
namespace/prefix or topic set so no two agents write the same file); the instruction to
extract claims **with grounding quotes from its range only** — no outside knowledge, no
reading beyond its range.
- **Staggered deployment (rate-limit mitigation):** never launch all at once. Spawn in
  batches of 2 (at most 3 for lighter ranges), then `sleep 10` before the next batch (use
  20s+ if 429s recur). Prepare small per-range cache files first
  (`/tmp/..._cache/range_N_START_END.txt`) so each agent does cheap one-shot reads of only
  its slice. Collect all task_ids; monitor to completion. If a subagent fails (e.g. 429),
  the main thread recovers *that range alone* (read its cache slice, extract claims, label
  the block "Main-thread recovery (rate limit on subagent)") and lets the others continue.
  Do not restart a rate-limited agent.

**Step 4 — Review and tie together (main thread).** Dedupe overlapping claims; fix
cross-links between new pages (subagents only linked Step-1 names); fill the source page's
claim list; remove agent artifacts (stray instructions, prompt echoes, `</content>`-style
tags — grep first); reconcile naming.

**Step 5 — Lint and validate.** Run and fix until clean: the **schema validator**, the
**wikilink checker** (must report **0 broken links**), the **alias-sync script**.

**Step 6 — Bookkeeping and file.**
1. **Update `Top_100_Structural_Sources.md`**: if the source is a line item, mark it
   ingested (append ✅ / change status) and update any note.
2. **File the source** into the right `raw/` subfolder (numbered era folders like
   `4. Modern Times`, or underscore-prefixed grouping folders like `_africa-cha` for
   multi-volume sets). Move both the text file (`.md`/`.txt`) and its original
   (`.pdf`/`.epub`) out of `raw/` root so the root holds only the un-ingested queue.
3. Append the `log.md` entry and update `index.md`. **Do not run `git commit` or `git push`
   — the user handles all git operations.** Leave the work staged-or-unstaged as-is.

> The two protocols below remain authoritative for **what each page must contain** (page
> types, frontmatter, link taxonomy, historiography) and **how to draw section boundaries**
> in large volumes (the Section Plan). Apply them within Steps 1–2 above.

---

## Ingest Workflow — Standard (books under ~400 pages)

For each source under ~400 pages:
1. **Identify** source type, period/regional coverage, methodological approach.
2. **Read** the full source in one pass.
3. **Write a source page** in `wiki/sources/`.
4. **Create or update** period, event, process, actor, place, concept, and controversy
   pages as the material warrants.
5. **Update `index.md`** with all new/modified pages.
6. **Append to `log.md`**:
   `## [YYYY-MM-DD] ingest | [Source Title] | [Period(s)] | [Region(s)] | [Pages created: N] | [Pages updated: N]`
7. **File the source** to its `raw/` folder. If a PDF, convert to `.md` first, confirm
   the `.md` exists on disk, then delete the PDF.
8. **Do not run `git commit` or `git push`** — the user handles all git operations once the
   ingest is complete.

A specialist monograph may touch 5–15 pages; a shorter primary source 10–20 through
cross-links. Both are correct.

---

## Ingest Workflow — Large-Volume Protocol (books over ~400 pages)

Large reference volumes (CAH, NCMH, Cambridge World History, any volume over 400 pages)
are processed in logical sections, not mechanical token chunks. Keep the full context of
a coherent argument in the window while writing its pages, then commit to disk before
advancing. **Never hold one section's content in context while reading the next. Write
first, then advance.**

**Step 1 — Read the Structural Map first.** Before any chapter content, read only the
TOC, the editor's introduction/preface, and the conclusion/afterword if present. From
these produce a **Section Plan** in `wiki/sources/[source-slug].md` listing every logical
section with: title and chapter numbers, period(s), region(s), estimated page count, and
key actors/events/processes flagged in the introduction. Write and save this page before
any content reading. Format:

```
## Section Plan

| Section | Chapters | Pages | Period | Region | Key Topics |
|---|---|---|---|---|---|
| The Early Bronze Age Near East | 1–3 | 1–87 | Early Bronze Age | mesopotamia, levant | Uruk expansion, early writing |
| Egypt to the End of the Old Kingdom | 4–6 | 88–175 | Early Bronze Age | north-africa | Pyramid Age, Old Kingdom collapse |
...
```

**Step 2 — Process one section at a time** (complete this full cycle before the next; do
not read ahead):
- **2a. Read the section** in one pass; hold in context for the next step only.
- **2b. Identify all pages affected** — list new pages (with file names) and existing
  pages to update (with what changes) before writing anything.
- **2c. Write all affected pages** — complete content (not stubs), all frontmatter, all
  cross-links from this section, plus the historiography section for period/major-event pages.
- **2d. Commit all pages to disk** before reading the next section. Critical discipline:
  Section N must be fully on disk before Section N+1 enters context.
- **2e. Append a section log entry**:
  `## [YYYY-MM-DD] section | [Volume Title] | Section: [Section Title] | [Pages created: N] | [Pages updated: N]`
- **2f. Clear and advance** only after pages are written and the log entry appended.

**Step 3 — Cross-Section Synthesis Pass** (with the source page and `index.md` in context,
not the raw text): read all pages from this volume; identify arguments spanning multiple
sections captured in separate pages; add cross-links visible only at the whole-volume
level; write a **Volume Synthesis Note** at the bottom of the source page (3–5 paragraphs:
the volume's overall argument, what it adds to the wiki, any cross-volume tensions with
already-ingested sources).

**Step 4 — File the source** (PDF → `.md`, confirm on disk, delete PDF) to its `raw/` folder.

**Step 5 — Final log entry**:
`## [YYYY-MM-DD] ingest-complete | [Volume Title] | [Total pages created: N] | [Total pages updated: N] | [Sections processed: N]`

**Step 6 — Stop after bookkeeping.** Do not run `git commit` or `git push` — the user
handles all git operations once the volume is complete.

### Applied to specific series
- **Cambridge Ancient History** — read the editor's introduction first (it frames the
  whole volume). Section boundaries follow part divisions (typically 3–6 chapters per
  civilization/period), one part = one cycle. The Vol 1 Part 1 "Prolegomena" is
  exceptionally important — give it its own cycle and create
  `wiki/concepts/cambridge-ancient-history-methodology.md`.
- **New Cambridge Medieval History** — boundaries follow geographic/thematic parts (e.g.
  "The Carolingian Empire", "The Islamic World"), one part = one cycle. NCMH treats regions
  in isolation; the synthesis pass must reconnect them.
- **Cambridge World History** — follow the explicit thematic parts. Vols 1–2 (to 10,000
  BCE; agriculture) create the most new pages; Vols 6–7 (Early Modern, Modern) mostly
  update existing pages — flag updates separately from creations.
- **Brill/Routledge volumes over 400 pages** — rarely have explicit parts; group 3–5
  chapters sharing a subject/argument as section boundaries. If unclear, treat each chapter
  as its own cycle.

### What "commit to disk" means (after each Step 2c)
1. Write every new `.md` file. 2. Edit every existing `.md` file. 3. Confirm each by
reading its path back. 4. Only then proceed to Step 2e. If a write fails, retry before
advancing. Context is ephemeral; disk is permanent — always resolve to disk.

---

## Historiography Protocol

Every period page and every major event page requires a `## Historiography` section
covering: **source quality** (what primary sources exist; biases and gaps); **scholarly
debates**; **methodological approaches**; **recent revisionism** (significant changes in
the standard account, last 30 yrs); **collection coverage** (what covers this well, where
gaps exist). For prehistoric periods, cover dating methods and confidence levels explicitly.
Absence of written sources is not absence of history.

---

## Contradiction Protocol

When new material contradicts existing content: 1. flag with `[CONTRADICTION]` on both
pages; 2. create/update the `wiki/controversies/` page; 3. classify (factual dispute /
interpretive difference / source-reliability conflict); 4. never silently overwrite —
preserve both claims with attribution and date.

---

## Query Workflow

1. Read `index.md` for relevant pages. 2. Read those pages. 3. Synthesize with citations
to wiki pages. 4. Offer to file as `wiki/queries/` if synthesis was non-trivial. 5. Append
to `log.md`: `## [YYYY-MM-DD] query | [Question summary]`.

---

## Lint Workflow

On a health-check request, report:
- Event pages with empty `causes` or `consequences`
- Actors mentioned but lacking their own page
- Places mentioned repeatedly without a place page
- Period pages missing historiography sections
- Orphan pages (no inbound links)
- Processes referenced inline without a process page
- Controversies described inline not yet promoted to `controversies/`
- `caused_by` links that appear to conflate sequence with causation
- Period pages where `collection_coverage` is `weak` or `absent`
- Detailed bios (`hubs/biographies/`) missing the reciprocal link from their `actors/`
  summary (or vice versa)
- Orphan detailed bios or summary actors that qualify for depth but lack a detailed page
- 3–5 sources from `Top_100_Structural_Sources.md` to prioritize next
- 3–5 analytical questions worth investigating

---

## Naming Conventions

- File names: `kebab-case.md`
- Events: `[event-name]-[start-year].md`
- Actors (persons): `[surname]-[given-name].md`
- Actors (states): `[state-name]-[qualifier].md`
- Places: `[place-name].md` (modern qualifier if ambiguous)
- Periods: `[period-name].md`
- Sources: `[author-surname]-[short-title]-[year].md`
- Obsidian links: `[[page-name|Display Name]]`
- Dates: BCE/CE throughout; BP for prehistoric before 10,000 BCE
- Calendar systems: specify when historically relevant

---

## Special Page Types

**Transition Pages** — for genuine discontinuities between periods, created in addition to
component event pages. File in `wiki/events/` with tag `transition`. Standing list: Bronze
Age Collapse (~1200 BCE) · Fall of the Western Roman Empire (476 CE) · the Mongol Conquests
(13th c.) · 1492 and the Columbian Exchange · 1789 and the Atlantic Revolutions · 1914 and
the end of the Long 19th Century · 1945 and the post-war order · 1991 and the end of the
Cold War.

**Comparative Civilization Pages** — explicit structural comparisons. File permanently in
`wiki/comparisons/`. See `comparisons-plan.md` for the plan, prioritized pages, frontmatter
template, and workflow.

**Counterfactual Pages** — file in `wiki/queries/` with tag `counterfactual`; use as
analytical tools to reveal which causes were contingent vs. structural.

---

## Warfare Hub — The High-Detail Section

`wiki/hubs/warfare/` is the **one part of the wiki deliberately built at higher resolution
than everything else**: graduate-level, West Point / staff-college-grade tactical and
operational analysis. This applies *only* here — do not let this depth leak into ordinary
`events/`, `actors/`, or `periods/` pages.

**Structure** — `hubs/warfare/[period]/[war]/[battle].md`, where `[period]` is a kebab-case
framework period (e.g. `classical-antiquity`), `[war]` is a war-slug folder (e.g.
`second-punic-war`) that also holds a `[war].md` campaign/operational overview linking its
battles, and `[battle].md` is the deep tactical page. The hub root holds the cross-cutting
pages: `warfare-hub.md`, the `strategy`/tactics sub-hubs, and `templates/`.

**Division of labor (hub vs. events/)** — the `events/` page owns the **narrative** (what
happened, causes, consequences, the broader story, full source list) at normal resolution;
the hub page owns the **conduct of the battle** (objectives, terrain, order of battle,
phased mechanics, critical decisions, doctrinal lessons). Each hub page links its `events/`
page via `event_page`; the `events/` page gets a reciprocal link back from its Related
section. Keep narrative/historiography light on the hub page.

**Battle-analysis standard (locked).** The single source of truth for frontmatter and
section structure is `wiki/hubs/warfare/templates/battle-analysis-template.md` — copy it,
do not redefine the schema inline (`hubs/warfare/battle-template.md` just points to it).
Frontmatter is flat and quoted (Obsidian-Bases-friendly, no nested maps): `analysis_type`
(`battle`|`campaign`|`siege`), `war` (matches parent folder), `commander_a/b`, `forces_a/b`,
`casualties_a/b` (with source attribution where disputed), `scale_immediate/consequential`,
`event_page`, `key_sources`. Content standard:
- **3,500–5,500+ words.**
- **Order-of-battle and casualty TABLES.**
- Work through **all nine U.S. principles of war (FM 3-0)** — Objective, Offensive, Mass,
  Economy of Force, Maneuver, Unity of Command, Security, Surprise, Simplicity — noting
  which each side honoured and violated, with concrete examples.
- **Quote primary sources verbatim and analyse each author's bias**; reconcile or flag
  conflicting accounts (numbers, sequence, location).
- Always include a **"Modern Doctrine Parallels"** section.
- Nine canonical body sections: Strategic Context & Objectives · Terrain, Weather &
  Intelligence · Order of Battle & Deployment · Course of the Battle (phases) · Outcome &
  Casualties · Critical Decisions · Lessons (Principles of War) · Modern Doctrine Parallels
  · Historiography & Primary Sources.

**Reference exemplar** — `wiki/hubs/warfare/classical-antiquity/second-punic-war/battle-of-cannae.md`
sets the standard; match Cannae when in doubt about depth, frontmatter, or section handling.

**Sourcing** — the roadmap is `Outstanding War Strategy Sources.md` (repo root): a tiered,
de-duplicated list of graduate/West-Point-grade strategy and operational-art literature.

---

## Biography Hub — The High-Detail Section for Individuals

`wiki/hubs/biographies/` is the **second high-resolution section** (after the Warfare Hub):
graduate-level, analytically rigorous life studies of historically significant individuals.
This applies *only* here — do not let this depth leak into ordinary `events/`, `actors/`,
`periods/`, or other actor pages.

**Division of labor (hub vs. actors/)** — the `actors/` page owns the **summary** (compact
overview, role, high-level key events/processes, brief counterfactual significance,
full-but-concise historiography, dense links) at normal resolution; the hub page owns the
**depth** (formative context, phased career with decision mechanics, tables, verbatim
primary-source analysis + bias critique, multi-scale counterfactuals, character vs.
structural factors, legacy assessment, detailed source criticism). Each hub page links its
`actors/` summary via `actor_page`; the actor page gets a reciprocal link back (in Related
or near the top). Events/processes still own discrete happenings; the bio page analyzes the
individual's choices within them.

**Structure and naming** — `hubs/biographies/[period]/[person-slug].md`, where `[period]`
is kebab-case from the framework (e.g. `classical-antiquity`, `age-of-expansion`) and
`[person-slug].md` exactly matches `actors/[person-slug].md` for reliable linking. The hub
root holds `biographies-hub.md` (portal + selection criteria + list of completed analyses)
and `templates/`. Figures spanning periods use the primary/most consequential period folder
(or note multiples).

**Biography-analysis standard (locked).** The single source of truth for frontmatter and
section structure is `wiki/hubs/biographies/templates/biography-analysis-template.md` —
copy it, do not redefine the schema inline. Frontmatter is flat and quoted: `analysis_type:
biography`, `actor_page`, `date_birth`/`date_death` + precision, `key_offices`,
`major_decisions`, `primary_sources`, `key_sources`, `scale`, etc. Content standard:
- **4,000–5,000+ words minimum** — plan for this length in subagent instructions (flex by
  significance; 5,000+ is the practical target for major lives).
- **Tables**: offices/positions timeline; major-decisions matrix (context | decision |
  intended outcome | actual | counterfactual note | sources).
- **Verbatim primary sources** with bias analysis; reconcile conflicting accounts.
- Strong multi-level **counterfactual** treatment (personal agency vs. structural constraints).
- Always include deep **Historiography and Primary Sources**.
- Nine canonical body sections: Formation and Early Influences · Rise / Path to Power ·
  Major Phases of Career · Signature Decisions and Their Mechanics · Intellectual/Policy/
  Military/Religious Style and Methods · Character, Relationships, and Personal Life ·
  Death, Immediate Succession/Aftermath · Long-term Legacy and Impact · Historiography and
  Primary Sources.
- Navigation header: summary link, related events/hubs, biographies-hub.

**Selection criteria** — reserved for figures with civilizational, epochal, or trans-
regional impact, **or** subjects of high-quality dedicated biographical sources supplying
rich primary material. Exclude routine/composite figures or cases with too thin a source
base. Start with exemplars from already-ingested biographical works plus canonical cases.

**Sourcing** — leverage existing biographical monographs (via their source pages + Section
Plans) plus reference series (CAH, CWH, NCMH) with strong biographical chapters. When
ingesting a new life, the scaffold step decides whether a detailed page is warranted and
pre-establishes the name. Prioritize primary-source richness and analytic payoff over
volume of sources.

---

## Collection Coverage Map

| Period | Coverage | Notes |
|---|---|---|
| Deep–Late Prehistory | Strong | Excellent archaeological section |
| Neolithic–Chalcolithic | Strong | Good Bronze/Neolithic coverage |
| Bronze Age | Strong | Collapse period well covered |
| Iron Age | Moderate | European strong; Asia thinner |
| Archaic Period | Strong | Greece, Near East, Persia well covered |
| Classical Antiquity | Excellent | Best-covered period in collection |
| Late Antiquity | Excellent | TTH series + CAH outstanding |
| Early Middle Ages | Strong | Very strong for western Eurasia |
| High Middle Ages | Strong | European and Islamic good |
| Late Middle Ages | Strong | European and Mediterranean strong |
| Early Modern | Moderate | Thin; mostly European |
| Age of Expansion onward | Absent | Critical gap — see Top_100_Structural_Sources.md |
| China (all periods) | Moderate–Strong | Literary primary strong; medieval secondary thin |
| Japan | Moderate | Narrative history thin |
| India | Weak | See Top_100_Structural_Sources.md |
| Medieval Islamic World | Strong | TTH + specialist series strong |
| Post-1500 Islamic World | Weak | Ottoman/Safavid/Mughal thin |
| Sub-Saharan Africa | Absent | Critical gap |
| Americas | Weak | Archaeology only; narrative absent |
| Russia/Eastern Europe | Absent | Critical gap |
| Southeast Asia | Absent | Critical gap |

---

## Division of Labor

**I handle**: sourcing, directing focus, adjudicating contradictions when asked, asking
questions, reading the wiki, deciding what matters.

**You handle**: all writing, cross-referencing, maintenance, filing, bookkeeping, and link
management. Every word in `wiki/` is yours unless I explicitly edit it.
