# CLAUDE.md — World History Wiki

## Overview

This is a persistent, LLM-maintained wiki covering world history from prehistory
to the present. The source collection (Bibliotheca Alexandrina, ~11,800 PDFs) is
the raw material. You read sources and build a structured, interlinked knowledge
base. I direct the analysis. You do all filing, cross-referencing, synthesis,
and bookkeeping.

Working environment: Obsidian. All wiki files are markdown. Sources live in the
collection directory. The wiki lives in `wiki/`. Never modify source files.

The ingestion sequence is defined in `Processing List.md`. Follow phase order.
The gap analysis and sourcing roadmap is in `Outstanding Sources.md`.

---

## Core Design Principles

**History is a network, not a tree.** Every page exists at the intersection of
what happened, where it happened, and when it happened. Links must preserve all
three dimensions — topical similarity alone is not enough to justify a link.

**Granularity is fractal.** The same moment can be one line on a period page, a
full event page, or the anchor of a dozen sub-event pages. Create pages at
whatever granularity the source material and analytical value warrant. Do not
force everything to one resolution level.

**Causation is not sequence.** The schema distinguishes temporal succession from
causal connection from correlation. These are different link types. Conflating
them is the most common error in historical wikis. Use the link taxonomy below
precisely.

**Historiography is first-class content.** How we know what we know — the sources,
their biases, their gaps, the scholarly debates — belongs in the wiki alongside the
history itself. Every major period page and event page gets a historiography section.

**The collection has a known bias.** The Bibliotheca Alexandrina is exceptionally
strong for Greco-Roman antiquity, medieval Europe and the Mediterranean, pre-modern
East Asia (via the Asian Classics series), and ancient Near East. It is weak on
sub-Saharan Africa, South and Southeast Asia, the post-1750 world, the Americas
(outside archaeology), and Russia/Eastern Europe. Flag this bias explicitly when
writing period overview pages for those regions. Do not write confident overviews
where the source base is thin — write what the sources support and note the gap.

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
  comparisons/          # Cross-period, cross-civilization comparison pages (see comparisons-plan.md for the plan)
  controversies/        # Disputed interpretations and scholarly debates
  timelines/            # Standalone chronological reference pages
  queries/              # Filed answers to significant questions
  sources/              # One summary page per ingested source

  hubs/                 # High-resolution special sections (see Warfare Hub and Biography Hub below)
    warfare/            # Tactical/operational battle and campaign analysis (West Point grade)
    biographies/        # Graduate-level analytic lives (detailed vs. summary actors/)
```

---

## Temporal Framework

Every page is anchored to at least one period from this list. Use the period name
in all frontmatter `period` fields. For events spanning multiple periods, list all.

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

Tag all pages with the most specific applicable region. Add parent regions as
secondary tags.

```
Africa:
  north-africa, sub-saharan-africa, east-africa, west-africa,
  central-africa, southern-africa, horn-of-africa

Americas:
  north-america, mesoamerica, caribbean, andes, amazonia,
  southern-cone, eastern-north-america

Asia:
  near-east, levant, mesopotamia, anatolia, iran-plateau,
  arabian-peninsula, central-asia, south-asia, southeast-asia,
  east-asia, china, japan, korea, steppe

Europe:
  western-europe, northern-europe, eastern-europe, mediterranean,
  iberia, british-isles, balkans, scandinavia

Oceania:
  australia, polynesia, melanesia, micronesia

Transregional:
  silk-road, indian-ocean, atlantic-world, mediterranean-world,
  eurasian-steppe
```

---

## Page Types and Formats

### Period Page (`wiki/periods/`)

One page per period in the temporal framework. Regional sub-period pages are
nested (e.g., `tang-dynasty.md` under `early-middle-ages.md`).

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

Body sections (all required):
- **Overview**: narrative summary of the period
- **Major Developments**: key events, processes, transformations
- **Key Actors**: states, rulers, movements (linked)
- **Geographic Scope**: which regions are historically active in this period
- **Transition**: what ended the prior period; what begins the next
- **Historiography**: source quality, major debates, recent revisionism,
  methodological approaches; for prehistoric periods cover dating methods
  and confidence levels explicitly
- **Collection Coverage Note**: state honestly what the collection covers
  well and where gaps exist for this period

---

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

`causes` and `consequences` are mandatory. Use `[[unknown]]` explicitly if
genuinely unclear. Do not leave blank.

Body sections:
- **Narrative**: what happened
- **Causal Analysis**: what drove this event (with explicit link types)
- **Consequence Analysis**: what it produced
- **Actors**: linked actor pages
- **Historiography** (if contested): positions, scholars, resolution status

---

### Process Page (`wiki/processes/`)

A long-duration dynamic that cannot be bounded as a discrete event:
feudalization, the spread of Islam, the Atlantic slave trade, industrialization.

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

Body sections:
- **Definition and Scope**: what this process is and what it is not
- **Causal Drivers**: what conditions and actors drove it
- **Major Phases**: turning points within the process
- **Geographic Spread**: how and where it expanded
- **Interaction**: how it relates to other processes
- **End Conditions**: what stopped or transformed it (or why it continues)

---

### Actor Page (`wiki/actors/`)

Any historical agent capable of action: persons, states, dynasties, empires,
institutions, armies, movements, religious organizations.

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

**Summary vs. detailed treatment**: The `wiki/actors/[person-slug].md` page is the concise
network-oriented summary (compact overview, role, high-level key events/processes, brief
counterfactual significance, full but concise historiography, and dense network links).
Very detailed analytic biographies for historically significant individuals live in the
parallel high-resolution Biography Hub (`hubs/biographies/`) — see the dedicated
"Biography Hub" section below.

For **persons**: role/title, major decisions and their consequences, counterfactual
significance (what changes without this actor — analytical, not celebratory).

For **states and empires**: territorial extent at peak, governing structure,
economic base, military capacity, mechanisms of decline.

For **institutions and movements**: founding conditions, structural features,
how they shaped events and processes.

Every detailed biography (`hubs/biographies/...`) must declare `actor_page` pointing to its
summary and the summary actor page must carry a reciprocal link back.

---

### Place Page (`wiki/places/`)

A geographic or political entity that persists across time as a location for events.

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

Body includes: geographic description, history of control and settlement, why
this place mattered (strategic, economic, religious, demographic), how its
significance changed over time.

---

### Concept Page (`wiki/concepts/`)

Analytical frameworks, historical categories, and interpretive tools. Both emic
(used by historical actors) and etic (applied by historians).

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

Always distinguish emic from etic. Always state limitations and critiques.

---

### Controversy Page (`wiki/controversies/`)

Genuine interpretive disputes between serious scholars. Distinct from factual
uncertainty — controversies are interpretive conflicts.

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

Do not adjudicate controversies unless I explicitly ask for analysis. Record
each position with its best arguments and the scholars who hold it.

**Standing controversies to create immediately during Phase 1–3 ingestion:**
- Causes of the Bronze Age Collapse (~1200 BCE)
- Causes of the Fall of the Western Roman Empire
- The population of pre-Columbian Americas
- Great Man vs. structural/systemic causation in history
- Reliability of Herodotus as a historical source
- Origins of the Indo-Europeans
- Geographic determinism (Diamond) and its critics

---

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

The `caused_by` / `preceded_by` distinction is the most critical. Never conflate
temporal sequence with causation.

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

For prehistoric dates, always state the dating method and confidence interval.
Never present approximate dates as exact.

---

## Source-Type Handling

### Cambridge Reference Series (CAH, NCMH, Cambridge World History)
Multi-author peer-reviewed reference volumes. The most authoritative sources
in the collection. Each volume is 800–1,000 pages and must be processed using
the Large-Volume Protocol below — do not attempt to read these in a single pass.
When they conflict with other sources, flag for controversy page but give
Cambridge volumes presumptive weight unless the conflict is itself actively debated.

### Primary Source Translations (Oxford World's Classics, Penguin Classics,
Translated Texts for Historians, Translations from the Asian Classics)
Record: original language, author's dates, translator's approach, known
translation controversies. Cross-link heavily. Translation choices affect
interpretation — note where this matters. Most of these are under 400 pages
and can be read in a single pass.

### Specialist Monographs (Brill, Routledge, Oxford Studies series)
These contain the most current scholarship. When a monograph contradicts a
Cambridge reference volume, flag for controversy page — this usually signals
recent revisionism worth tracking. Most are 200–400 pages; use the standard
ingest workflow. If over 400 pages, use the Large-Volume Protocol.

### Archaeological Reports
Treat as primary evidence for prehistoric and ancient periods. When
archaeological evidence conflicts with textual sources, create a controversy
page — this conflict is often more significant than purely textual disputes.

---

## Ingest Workflow — Deployed Subagent Strategy (DEFAULT, as of 2026-06-22; staggered batching added for rate limits)

This is the **primary ingest method for all sources going forward.** It parallelizes
claim extraction across Sonnet subagents while keeping all scaffolding, reconciliation,
and validation on the main thread. The Standard and Large-Volume protocols below are now
**reference material** for the per-page schema, section logic, and historiography
requirements that this method's main-thread steps draw on — not separate workflows to
choose between.

The non-negotiable principle: **the main thread owns structure; subagents own bulk
extraction.** Subagents never decide taxonomy, naming, or cross-links — they fill in
claims within boundaries the main thread has already drawn.

### Step 1 — Scaffold first, on the main thread

Read enough of the source (TOC, introduction, conclusion, and targeted sampling) to:
- Write the **source page** in `wiki/sources/` (with the Section Plan for large volumes).
- Create the **key person/concept/place pages** that everything else will link to.
- For dedicated biographical sources or sources with major biographical cores: decide
  whether a **detailed biography page** in `hubs/biographies/` is warranted (see
  "Biography Hub" section) in addition to the standard summary actor page, and
  pre-establish the name.
- Decide the **topic taxonomy** and **establish naming conventions** for every page the
  ingest will create.

Do not spawn any agent until the naming conventions and the set of linkable page names
exist on disk. Subagents must inherit names, never invent the structural ones.

### Step 2 — Split the book by disjoint line-ranges

Divide the raw text into **N contiguous, non-overlapping chunks** by line number.

- **Size the agent count to the book, not to a fixed number.** Base N on **substantive body length ×
  density** (count the *body* lines, excluding front matter, endnotes, bibliography, and index — these
  can be half the file). A useful rule of thumb is **one agent per ~2,000–3,500 body lines**, with a
  floor of 2–3 and up to **10** for very large or multi-volume references. Do NOT default to 6: a short
  book (e.g. ~2,700 body lines) wants ~3 agents, not 6 — over-splitting starves agents of context (a
  200-line range can't cover its subject).
- **Weight the chunks by content density and importance, not by even section boundaries.** A dense or
  pivotal stretch deserves its own agent (or more than one — for dense or multi-doctrine material, run
  **multiple passes over one major section** so no doctrine is missed); lighter, thinner material can be
  combined into a single larger range. Align chunk edges to natural section/chapter boundaries *where it
  doesn't fight the weighting* — content weight wins over tidy boundaries.
- Ranges must be **disjoint** — every line belongs to exactly one chunk.

### Step 3 — Spawn one Sonnet subagent per chunk (staggered batches + background)

Use the Agent tool with **`model: sonnet`** and `run_in_background: true`, one agent per
chunk. Each agent's prompt must contain:
- Its **exclusive line-range** (read only that range).
- The **schema and naming conventions** from this file.
- The **established page names** it may link to (from Step 1).
- **Exclusive ownership of the claim titles it creates** — assign each agent a distinct
  title namespace/prefix or topic set so **two agents never write the same file**.
- The instruction to extract claims **with grounding quotes from its range only** — no
  outside knowledge, no reading beyond its range.

**Staggered deployment (rate-limit mitigation):** Never launch all subagents at once.
Spawn in small batches of 2 (or at most 3 for lighter/thinner ranges). After issuing the
`spawn_subagent` calls for a batch, run `run_terminal_command` with `sleep 10` (10 seconds)
before launching the next batch. This spaces out peak concurrent TPM usage. Use 20 seconds
(or longer) if rate limits (429 / token exhaustion) occur again. Collect every returned
subagent task_id. Once all batches are launched, use `wait_commands_or_subagents`
(mode "wait_all" or "wait_any") and/or `get_command_or_subagent_output` (polling specific
ids) to monitor progress and completion. Always prepare small per-range cache files first
(`/tmp/..._cache/range_N_START_END.txt` or equivalent) so each agent can do cheap one-shot
reads of *only* its slice. If any subagent fails (e.g. 429 resource-exhausted), the main
thread performs immediate recovery for *that range alone* (read its small cache slice via
sed/read_file and extract the claims), labels the block "Main-thread recovery (rate limit
on subagent)", and lets the other agents continue. Do not restart a rate-limited agent.

### Step 4 — Review and tie together, on the main thread

After all agents finish:
- **Dedupe** overlapping claims.
- **Fix cross-links** between the new pages (subagents only linked to Step-1 names).
- **Fill the source page's claim list.**
- **Remove agent artifacts** — stray instructions, prompt echoes, or `</content>`-style
  tags left in files (grep for these before proceeding).
- **Reconcile naming** across everything the agents produced.

### Step 5 — Lint and validate

Run, and fix until clean:
- the **schema validator**,
- the **wikilink checker** (must report **0 broken links**),
- the **alias-sync script**.

### Step 6 — Bookkeeping, file the source, commit (and push)

After reconciliation and lint, before/with the commit:

1. **Update `Outstanding Sources.md`** (repo root): if the ingested source is a line item there,
   change its status marker to ✅ (or 🟡 for partial multi-volume) and update the note. This keeps the
   sourcing roadmap honest about what is now in the collection.
2. **File the source** into the appropriate `raw/` subfolder (matching the Processing List / existing
   structure — numbered era folders like `4. Modern Times`, or underscore-prefixed grouping folders
   like `_africa-cha` for a multi-volume set). Move the ingested text file (`.md`/`.txt`) **and** its
   original (`.pdf`/`.epub`) out of `raw/` root into that folder, so `raw/` root only ever holds the
   un-ingested queue.
3. **Commit** per the standing rules below. **Push only once the whole source is complete** (commit per
   section is fine; push at the end). Append the `log.md` entry and update `index.md`. Commit messages
   end with the standard `Co-Authored-By` trailer.

> The two protocols that follow remain authoritative for **what each page must contain**
> (page types, frontmatter, link taxonomy, historiography sections) and for **how to draw
> section boundaries** in large volumes (the Section Plan). Apply them within Steps 1–2 above.

---

## Ingest Workflow — Standard (books under ~400 pages)

For each source in Processing List.md that is under approximately 400 pages:

1. **Identify** source type, period coverage, regional coverage, methodological
   approach.
2. **Read** the full source in one pass.
3. **Write a source page** in `wiki/sources/`.
4. **Create or update**:
   - Period pages for covered periods
   - Event pages for discrete events
   - Process pages for long-duration dynamics
   - Actor pages for significant persons, states, institutions
   - Place pages for significant locations
   - Concept pages for analytical frameworks
   - Controversy pages for interpretive disputes
5. **Update `index.md`** with all new and modified pages.
6. **Append to `log.md`**:
   `## [YYYY-MM-DD] ingest | [Source Title] | [Period(s)] | [Region(s)] | [Pages created: N] | [Pages updated: N]`
7. **File the source**: move the source file to its appropriate folder matching
   the Processing List directory structure. If the source is a PDF, convert it
   to `.md` first, then delete the PDF. Confirm the `.md` file exists on disk
   before deleting the PDF.
8. **Commit and push to GitHub**: stage the `wiki/` changes, commit with a
   message naming the ingested source, and push to the `main` branch. This is a
   standing instruction — perform it automatically after every completed source
   ingest without waiting to be asked. Commit messages end with the standard
   `Co-Authored-By` trailer.

A specialist monograph may touch 5–15 pages. A shorter primary source may
touch 10–20 through its cross-links. Both are correct.

---

## Ingest Workflow — Large-Volume Protocol (books over ~400 pages)

Large volumes — primarily the Cambridge Ancient History, New Cambridge Medieval
History, Cambridge World History, and any other reference volumes over 400 pages —
must be processed in logical sections rather than mechanical token chunks. The
goal is to keep the full context of a coherent argument in the working window
when writing pages from it, then commit those pages to disk before moving on.
Never hold a section's content in context while reading the next section. Write
first, then advance.

### Step 1 — Read the Structural Map (before reading any content)

Before reading any chapter content, read only:
- The table of contents
- The volume editor's introduction (or preface)
- The conclusion or afterword if present

From this, produce a **Section Plan** in the source's wiki page
(`wiki/sources/[source-slug].md`) listing every logical section with:
- Section title and chapter numbers
- Period(s) covered
- Region(s) covered
- Estimated page count
- Key actors, events, or processes flagged in the introduction

Write and save this source page before proceeding. This is the map you will
navigate by. Do not begin content reading until this page exists on disk.

Example Section Plan format:
```
## Section Plan

| Section | Chapters | Pages | Period | Region | Key Topics |
|---|---|---|---|---|---|
| The Early Bronze Age Near East | 1–3 | 1–87 | Early Bronze Age | mesopotamia, levant | Uruk expansion, early writing |
| Egypt to the End of the Old Kingdom | 4–6 | 88–175 | Early Bronze Age | north-africa | Pyramid Age, Old Kingdom collapse |
...
```

### Step 2 — Process One Section at a Time

For each section in the Section Plan, follow this complete cycle before
moving to the next section. Do not read ahead.

**2a. Read the section.**
Read the full text of the section's chapters in one pass. Hold this in context
for the next step only.

**2b. Identify all pages affected.**
Before writing anything, list every wiki page this section creates or updates:
- New pages to create (with proposed file names)
- Existing pages to update (with what changes)

Write this list as a comment block at the top of your working notes.
Do not begin writing pages until the full list is identified.

**2c. Write all affected pages.**
Write or update every page on the list. For each page:
- Write the complete content, not a stub
- Fill all required frontmatter fields
- Include all cross-links identified from this section
- Write the historiography section if this is a period or major event page

**2d. Commit all pages to disk.**
Save every page created or updated in this section cycle before reading the
next section. This is the critical discipline: context for Section N must be
fully written to disk before Section N+1 enters the context window.

**2e. Append a section log entry.**
```
## [YYYY-MM-DD] section | [Volume Title] | Section: [Section Title] | [Pages created: N] | [Pages updated: N]
```

**2f. Clear and advance.**
Only after all pages are written and the log entry is appended, read the
next section.

### Step 3 — Cross-Section Synthesis Pass

After all sections are processed, do a synthesis pass with the source page
and index.md in context (not the raw source text):

- Read all pages created or updated from this volume
- Identify arguments that span multiple sections but were captured in
  separate pages
- Add cross-links between pages where the connection only becomes visible
  at the whole-volume level
- Write a **Volume Synthesis Note** at the bottom of the source page:
  a 3–5 paragraph summary of the volume's overall argument, what it adds
  to the wiki as a whole, and any cross-volume tensions with other
  already-ingested sources

### Step 4 — File the Source

Move the source file to its appropriate folder matching the Processing List
directory structure. If the source is a PDF, convert it to `.md` first, then
delete the PDF. Confirm the `.md` file exists on disk before deleting the PDF.

### Step 5 — Final Log Entry

```
## [YYYY-MM-DD] ingest-complete | [Volume Title] | [Total pages created: N] | [Total pages updated: N] | [Sections processed: N]
```

### Step 6 — Commit and Push to GitHub

After the final log entry, stage the `wiki/` changes, commit with a message
naming the ingested volume, and push to the `main` branch. This is a standing
instruction — perform it automatically once the volume's ingest is complete,
without waiting to be asked. Commit messages end with the standard
`Co-Authored-By` trailer.

---

### Large-Volume Protocol: Applied to Specific Series

**Cambridge Ancient History (each volume)**
- Read the editor's introduction first — these contain the historiographical
  framework for the entire volume
- Section boundaries follow part divisions, not individual chapters
  (CAH parts are typically 3–6 chapters covering one civilization or period)
- Each part is one section cycle
- The CAH Vol 1 Part 1 "Prolegomena" chapter is exceptionally important —
  it frames the methodology for the entire series; give it its own cycle
  and create a `wiki/concepts/cambridge-ancient-history-methodology.md` page

**New Cambridge Medieval History (each volume)**
- Section boundaries follow the volume's geographic/thematic parts
  (e.g., "The Carolingian Empire", "The British Isles", "The Islamic World")
- Each part is one section cycle regardless of chapter count
- Cross-links between geographic parts are especially important — the NCMH
  tends to treat regions in isolation; your synthesis pass must reconnect them

**Cambridge World History (each volume)**
- These are explicitly organized into thematic parts — follow those divisions
- Volume 1 (to 10,000 BCE) and Volume 2 (agriculture) will create the most
  new pages since they cover periods where few other sources exist yet
- Volume 6 and 7 (Early Modern and Modern) will mostly update existing pages
  from Cambridge Ancient History and NCMH; flag updates separately from creations

**Brill and Routledge series volumes over 400 pages**
- These rarely have explicit parts; use chapter groupings of 3–5 chapters
  that share a common subject or argument as section boundaries
- If chapter groupings are unclear, treat each chapter as its own section cycle
  — the overhead is worth it for accuracy

---

### What "Commit to Disk" Means in Practice

This is a Claude Code operation, not a conceptual instruction. After completing
Step 2c for each section:

1. Use file write operations to save every new `.md` file
2. Use file edit operations to update every existing `.md` file
3. Confirm each file is written by reading its path back
4. Only after all confirmations, proceed to Step 2e

If a write operation fails, retry before advancing. A section whose pages exist
only in context and not on disk is lost when the next section is read.
Context is ephemeral. Disk is permanent. Always resolve to disk.

---

## Historiography Protocol

Every period page and every major event page requires a `## Historiography` section.

Cover:
- **Source quality**: what primary sources exist; their known biases and gaps
- **Scholarly debates**: what historians disagree about
- **Methodological approaches**: dominant methods used to study this period/event
- **Recent revisionism**: significant changes in the standard account (last 30 yrs)
- **Collection coverage**: what in the Bibliotheca Alexandrina covers this well;
  where gaps exist

For prehistoric periods: cover dating methods and confidence levels explicitly.
Absence of written sources is not absence of history.

---

## Contradiction Protocol

When new material contradicts existing wiki content:

1. Flag with `[CONTRADICTION]` on both affected pages.
2. Create or update the `wiki/controversies/` page.
3. Classify: factual dispute / interpretive difference / source reliability conflict.
4. Do not silently overwrite. Preserve both claims with attribution and date.

---

## Query Workflow

1. Read `index.md` for relevant pages.
2. Read those pages.
3. Synthesize with citations to wiki pages.
4. Offer to file as `wiki/queries/` if synthesis was non-trivial.
5. Append to `log.md`: `## [YYYY-MM-DD] query | [Question summary]`

---

## Lint Workflow

When I ask for a health check, report:

- Event pages with empty `causes` or `consequences`
- Actors mentioned but lacking their own page
- Places mentioned repeatedly without a place page
- Period pages missing historiography sections
- Orphan pages (no inbound links)
- Processes referenced inline without a process page
- Controversies described inline not yet promoted to `controversies/`
- `caused_by` links that appear to conflate sequence with causation
- Period pages where `collection_coverage` is `weak` or `absent`
- Detailed biography pages (hubs/biographies/) missing reciprocal link from their `actors/` summary (or vice versa)
- Orphan detailed bios or summary actors that qualify for depth but lack a detailed page
- 3–5 sources from Outstanding Sources.md to prioritize next
- 3–5 analytical questions worth investigating

---

## Naming Conventions

- File names: `kebab-case.md`
- Events: `[event-name]-[start-year].md`
- Actors (persons): `[surname]-[given-name].md`
- Actors (states): `[state-name]-[qualifier].md`
- Places: `[place-name].md` with modern qualifier if ambiguous
- Periods: `[period-name].md`
- Sources: `[author-surname]-[short-title]-[year].md`
- Obsidian links: `[[page-name|Display Name]]`
- Dates: BCE/CE throughout; BP for prehistoric before 10,000 BCE
- Calendar systems: specify when historically relevant

---

## Special Page Types

### Transition Pages
For genuine discontinuities between periods. Create in addition to component
event pages. File in `wiki/events/` with tag `transition`. Standing list:
- Bronze Age Collapse (~1200 BCE)
- Fall of the Western Roman Empire (476 CE)
- The Mongol Conquests (13th c.)
- 1492 and the Columbian Exchange
- 1789 and the Atlantic Revolutions
- 1914 and the end of the Long 19th Century
- 1945 and the post-war order
- 1991 and the end of the Cold War

### Comparative Civilization Pages
Explicit structural comparisons. File in `wiki/comparisons/`. File permanently.

See `comparisons-plan.md` (in the repo root) for the detailed implementation plan, prioritized pages, frontmatter template, and workflow.

### Counterfactual Pages
File in `wiki/queries/` with tag `counterfactual`.
Use as analytical tools to reveal which causes were contingent vs. structural.

---

## Warfare Hub — The High-Detail Section

`wiki/hubs/warfare/` is the **one part of the wiki deliberately built at higher resolution
than everything else.** While the rest of the wiki summarizes, the warfare hub does
graduate-level, West Point / staff-college-grade tactical and operational analysis. This
is intentional and applies *only* here — do not let this depth standard leak into the
ordinary `events/`, `actors/`, or `periods/` pages.

### Structure

Battle and campaign analyses are filed by a three-level path:

```
hubs/warfare/[period]/[war]/[battle].md
```

- `[period]` — a kebab-case period name from the temporal framework (e.g. `classical-antiquity`).
- `[war]` — a war-slug folder (e.g. `second-punic-war`), which also holds a `[war].md`
  hub page linking its battles and giving the campaign/operational overview.
- `[battle].md` — the deep tactical analysis page.

The hub root holds the cross-cutting pages: `warfare-hub.md`, the `strategy`/tactics
sub-hubs, and `templates/`.

### Division of labor: hub vs. events/

- The **`events/` page owns the narrative** — what happened, causes, consequences, the
  broader story, full source list — at normal wiki resolution.
- The **`hubs/warfare/` analysis page owns the conduct of the battle** — objectives,
  terrain, order of battle, the phased mechanics of the engagement, the critical
  decisions, the doctrinal lessons.
- Every analysis page links its `events/` page via `event_page`, and the `events/` page
  gets a **reciprocal link** back from its Related section. Keep narrative/historiography
  light on the hub page; depth there goes on the conduct of the fight.

### Battle-analysis standard (the locked standard)

The **single source of truth** for frontmatter and section structure is
`wiki/hubs/warfare/templates/battle-analysis-template.md`. Copy it; do not redefine the
schema inline. (`hubs/warfare/battle-template.md` is just a pointer to it.)

Frontmatter is flat and quoted (Obsidian-Bases-friendly; no nested maps): `analysis_type`
(`battle` | `campaign` | `siege`), `war` (matches the parent folder), `commander_a/b`,
`forces_a/b`, `casualties_a/b` (with source attribution where disputed),
`scale_immediate/consequential`, `event_page`, `key_sources`.

Content standard for a battle analysis:
- **3,500–5,500+ words.**
- **Order-of-battle and casualty TABLES.**
- Work through **all nine U.S. principles of war (FM 3-0)** — Objective, Offensive, Mass,
  Economy of Force, Maneuver, Unity of Command, Security, Surprise, Simplicity — noting
  which each side **honoured and violated**, with concrete examples.
- **Quote primary sources verbatim and analyse each author's bias**; reconcile or flag
  conflicting accounts (numbers, sequence, location).
- Always include a **"Modern Doctrine Parallels"** section.
- The nine canonical body sections: Strategic Context & Objectives · Terrain, Weather &
  Intelligence · Order of Battle & Deployment · Course of the Battle (phases) · Outcome &
  Casualties · Critical Decisions · Lessons (Principles of War) · Modern Doctrine Parallels
  · Historiography & Primary Sources.

### Reference exemplar

`wiki/hubs/warfare/classical-antiquity/second-punic-war/battle-of-cannae.md` is the
**worked exemplar that sets the standard.** When in doubt about depth, frontmatter, or
section handling, match Cannae.

### Sourcing

The sourcing roadmap for this section is `Outstanding War Strategy Sources.md` (repo root) —
a tiered, de-duplicated list of the graduate/West-Point-grade strategy and operational-art
literature to acquire for deepening the hub.

---

## Biography Hub — The High-Detail Section for Individuals

`wiki/hubs/biographies/` is the **second part of the wiki deliberately built at higher resolution
than everything else** (the first being the Warfare Hub). While the rest of the wiki (including
ordinary `wiki/actors/` pages) summarizes, the biography hub provides graduate-level,
analytically rigorous life studies of historically significant individuals. This is intentional
and applies *only* here — do not let this depth standard leak into the ordinary `events/`,
`actors/`, `periods/`, or other actor pages.

### Division of labor: hubs/biographies vs. actors/

- The **`actors/` page owns the summary** — compact overview, role, high-level key events/processes,
  brief counterfactual significance, full (but concise) historiography, and dense network links —
  at normal wiki resolution.
- The **`hubs/biographies/` analysis page owns the depth** — formative context, phased career with
  decision mechanics, tables (offices, decisions matrix), verbatim primary source analysis + bias
  critique, multi-scale counterfactuals, character vs. structural factors, legacy assessment, and
  detailed source criticism.
- Every detailed biography page links its summary `actors/` page via `actor_page`, and the actor
  page gets a **reciprocal link** (in Related or near the top) back to the detailed version. Keep
  narrative light on the hub page; depth goes on the conduct and analysis of the life.
- Events and processes continue to own discrete happenings; the bio page analyzes the
  individual's choices within them.

### Structure and naming

Detailed biographies are filed under period folders using the temporal framework:

```
hubs/biographies/[period]/[person-slug].md
```

- `[period]` — kebab-case from the CLAUDE.md list (e.g. `classical-antiquity`, `age-of-expansion`).
- `[person-slug].md` — exactly matches the corresponding `actors/[person-slug].md` for reliable linking.
- The hub root holds: `biographies-hub.md` (portal + selection criteria + list of completed analyses)
  and `templates/`.

Figures spanning periods use the primary/most consequential period folder (or note multiples).

### Biography-analysis standard (the locked standard)

The **single source of truth** for frontmatter and section structure is
`wiki/hubs/biographies/templates/biography-analysis-template.md`. Copy it; do not redefine the
schema inline.

Frontmatter is flat and quoted (Obsidian-Bases-friendly; no nested maps): `analysis_type: biography`,
`actor_page`, `date_birth`/`date_death` + precision, `key_offices`, `major_decisions`,
`primary_sources`, `key_sources`, `scale`, etc.

Content standard for a detailed biography:
- **4,00–5,000+ words minimum, plan for this length when giving instruction to the subagents** (flex by figure significance; current emphasis is 5,000+ as the practical
  target for major lives).
- **Tables**: offices/positions timeline; major decisions matrix (context | decision | intended
  outcome | actual | counterfactual note | sources).
- **Verbatim primary sources** with bias analysis; reconcile conflicting accounts.
- Strong multi-level **counterfactual** treatment (personal agency vs. structural constraints).
- Always include deep **Historiography and Primary Sources**.
- The nine canonical body sections: Formation and Early Influences · Rise / Path to Power ·
  Major Phases of Career · Signature Decisions and Their Mechanics · Intellectual/Policy/Military/
  Religious Style and Methods · Character, Relationships, and Personal Life · Death, Immediate
  Succession/Aftermath · Long-term Legacy and Impact · Historiography and Primary Sources.
- Navigation header: summary link, related events/hubs, biographies-hub.

### Selection criteria (historically significant individuals)

Detailed biographies are reserved for figures with:
- Civilizational, epochal, or trans-regional impact, **or**
- Subjects of one or more high-quality dedicated biographical sources in the collection that supply
  rich primary material justifying the depth.

Exclude routine or composite figures, or cases where the source base is too thin. Start with
exemplars drawn from already-ingested biographical works plus canonical cases.

### Sourcing

Leverage existing biographical monographs (via their source pages + Section Plans) plus reference
series (CAH, CWH, NCMH) that contain strong biographical chapters. When ingesting a new dedicated
life, the scaffold step must decide whether a detailed page is warranted and pre-establish the name.
Prioritize primary-source richness and analytic payoff over volume of sources.

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
| Age of Expansion onward | Absent | Critical gap — see Outstanding Sources |
| China (all periods) | Moderate–Strong | Literary primary strong; medieval secondary thin |
| Japan | Moderate | Narrative history thin |
| India | Weak | See Outstanding Sources |
| Medieval Islamic World | Strong | TTH + specialist series strong |
| Post-1500 Islamic World | Weak | Ottoman/Safavid/Mughal thin |
| Sub-Saharan Africa | Absent | Critical gap |
| Americas | Weak | Archaeology only; narrative absent |
| Russia/Eastern Europe | Absent | Critical gap |
| Southeast Asia | Absent | Critical gap |

---

## Division of Labor

**I handle**: sourcing, directing focus, adjudicating contradictions when asked,
asking questions, reading the wiki, deciding what matters.

**You handle**: all writing, cross-referencing, maintenance, filing, bookkeeping,
and link management. Every word in `wiki/` is yours unless I explicitly edit it.
