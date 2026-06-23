# Comparisons Plan — World History Wiki

**Persistent implementation plan for the `wiki/comparisons/` section.**

This file contains the approved roadmap for creating explicit structural comparison pages (cross-civilizational, cross-period, and thematic). It is meant to be referenced in future sessions so work on the Comparisons section can be continued consistently.

- See [CLAUDE.md](CLAUDE.md) for the overall rules, especially:
  - Directory structure
  - "Comparative Civilization Pages" under Special Page Types
  - Link taxonomy (especially `analogous_to` and `contrasts_with`)
  - Ingest / synthesis discipline
- Related files: [wiki/index.md](wiki/index.md), [wiki/overview.md](wiki/overview.md), [wiki/home.md](wiki/home.md), thematic hubs under `wiki/hubs/themes/`

**Status**: Approved (developed 2026-06-22)

**Current progress**: 
- #1 Early Cities created + integrated (back-links added).
- #2 Pristine State Formation: Dedup gate applied — audited hub + process coverage + overlap with #1; decision: no new page (documented in list). 
- #3 Commercial Revolutions Compared created.
- #4 Frontier Societies, #5 Religious Authority, #6 Empire Formation (narrow extraction axis) created. Back-links added to referenced pages. Index, log, and plan updated. All ready for review.
- Optional follow-on (both): `polycentric-world-systems-and-trade-networks` and `legal-legitimation-styles-compared` created + integrated (dedup gate applied; B scoped to "grounds of legal authority" to avoid duplicating the islamdom moralism/formalism section).
- Courtly Culture across Eurasia created (CWH V Ch 7 candidate from deepsearch). Comparisons section now at **12 pages**. Plan, index, log, and concept back-link updated.
- Educational Institutions in Comparative Perspective created (CWH V Ch 5, Walton). Dedup gate: the existing `concepts/educational-institutions` already surveys the forms, so the comparison page was scoped to the residual axis — institutional autonomy vs. state-fusion (examination/madrasa/university/monastery) — and cross-links the concept page rather than duplicating it. Comparisons section now at **13 pages**. Index, log, plan, and back-links updated.
- Deepsearch candidate list (#3–#8) worked through with the dedup gate. **Created** #4 `theatre-state-and-the-bases-of-power` (spectacle vs. coercion), #7 `managing-religious-pluralism-compared` (dhimma/millet/convivencia; distinct from the colonial `plural-society` concept), #8 `unfree-labor-systems-compared` (debt/chattel/serf/military/mita; no prior comparative page). **Skipped as dups** (documented inline below): #3 Social Hierarchy (the `social-hierarchy-and-solidarity` concept is already Reynolds' comparison), #5 Industrious Revolution (already covered by the `industrious-revolution` process page + `great-divergence` + `commercial-revolutions-compared`), #6 Military Revolutions (already covered by the `military-revolution` concept + `gunpowder-empires` + `strategic-practice`). Comparisons section now at **16 pages**. Remaining: "bonus granular" Han–Rome / Mediterranean–China items only.

**How to use this file**: When resuming Comparisons work, read this file first. It defines scope, priorities, templates, files to touch, and verification steps. Update this file (and the wiki) as progress is made.

---

# Plan: Creating Pages for the `wiki/comparisons/` Section

## Context

The `wiki/comparisons/` directory implements CLAUDE.md's directive for "Comparative Civilization Pages" and "Cross-period, cross-civilization comparison pages": "Explicit structural comparisons. File in `wiki/comparisons/`. File permanently."

Currently four pages exist (frontmatter normalized to canonical schema; index.md catalog table populated):

- `wiki/comparisons/celtic-lands-and-english-expansion.md` (NCMH-derived; divergent responses to English expansion in the British Isles)
- `wiki/comparisons/islamdom-and-occident-high-medieval.md` (Hodgson *Venture of Islam* Vol 2 structural comparison of legitimation, law, religion, society c. 1100–1300)
- `wiki/comparisons/sexuality-in-world-belief-systems.md` (Cambridge World History of Sexualities Vol 2 — cultural/religious frameworks)
- `wiki/comparisons/strategic-practice-across-civilizations.md` (Cambridge History of Strategy — recurring vs. culture-specific patterns)

These demonstrate the genre: frontmatter with comparison axes + source grounding; body sections contrasting cases or features; assessment of what the comparison reveals; heavy use of the mandated link taxonomy (`analogous_to`, `contrasts_with`, `part_of`, etc.); cross-links back from hubs and source pages.

**Why more pages are needed now**:

- Many ingested sources are explicitly comparative or contain strong comparative sections that were turned into period/event/actor/concept pages but not distilled into standalone comparison pages (e.g., Yoffee ed., *Cambridge World History Vol. III: Early Cities in Comparative Perspective* — 6 thematic parts with cross-civilizational case juxtapositions; NCMH volumes; Hodgson; world-systems sources like Abu-Lughod; CWH Vols V–VII thematic chapters).
- Thematic hubs (`wiki/hubs/themes/`) and civilization portals repeatedly surface recurring axes (pristine state formation variants, empire/collapse patterns, warfare systems, commercial revolutions, religious institutions, frontier responses) that require dedicated comparison treatment to realize the "history is a network" principle.
- `wiki/index.md` still shows "*(none yet)*" under Comparisons (stale; stats correctly show 4). Hubs reference only the existing handful.
- Outstanding Sources and collection strengths (Cambridge series, Hodgson, transregional works) now supply the raw material; the gap is synthesis into the comparisons/ category.
- Without them, structural insights (e.g., heterarchy vs. hierarchy in early cities, moralistic vs. formalistic law per Hodgson, universal-monarchy aspirations) remain scattered or buried in source notes/concepts.

**Goal**: a concrete, prioritized plan to populate the section systematically using existing ingested material (no new full source reads required beyond synthesis from source pages and hubs).

## Recommended Approach

Adopt and slightly formalize the pattern visible in the four existing pages rather than inventing a new schema (CLAUDE.md gives comparisons lighter treatment than events/processes).

**Frontmatter template** (canonical — closest to the two broadest existing pages, with `axis_of_comparison` now required for all comparison pages; normalization of the original four is complete). Note: `cross-period` is retained in the type enum because CLAUDE.md explicitly sanctions "cross-period, cross-civilization comparison pages."

```yaml
---
title: [Descriptive Title]
comparison_type: [cross-civilizational | civilizational-structural | cross-regional | cross-period | thematic-axis]
periods_covered: []
regions_covered: []
civilizations_compared: []   # broad civilizations; for narrow cases (e.g. Celtic lands) use `cases: []` as an additional field
axis_of_comparison: [short phrase]
sources_ingested: [count]
last_updated: [YYYY-MM-DD]
tags: [comparison, period-name(s), region-name(s), ...]
---
```

**Normalization step**: As the first action in any batch, update the frontmatter of the existing four pages to the canonical fields above — preserving their data **and enriching it where the canonical schema requires more than relabeling**. Concretely: this means *adding* `axis_of_comparison` to the three pages that lack it (only `celtic` has one today — `sexuality`, `strategic`, and `islamdom` will each need a one-phrase axis written), and relabeling legacy fields (`period_involved`→`periods_covered`, `regions_involved`/`regions_compared`→`regions_covered`). Adding the axis is the point, not overhead: a page that cannot state a single clear axis is a topical roundup, which CLAUDE.md forbids. This prevents schema drift.

**Immediate, standalone fix (completed)**: The stale "*(none yet)*" under `## Comparisons` in `wiki/index.md` has been replaced with a catalog table of the four existing pages (and the Summary Statistics count confirmed). Future new pages should simply append rows to that table.

**Body structure** (flexible but consistent):

- Intro + Purpose/Framework (anchor to source + why this comparison matters)
- The Comparison (structured by cases, features, or axes; use tables or clear bullets where helpful)
- Recurring Features vs. Variation / Significance / Assessment
- Related (explicit `part_of:`, `analogous_to:`, `contrasts_with:`, `concurrent_with:`, links to source pages, hubs, controversies, concepts; **this section is also where target pages should link back to this comparison for full network integration**)
- (Optional) Historiography note if the comparison itself is contested

**Sourcing & creation process**:

- **Dedup / coverage gate (mandatory before scoping any new page)**: Audit the relevant hub(s), the main `state-formation` / `empire` / `strategy` process pages, existing controversies, and already-created comparison pages. Only create a new comparison page if there is a distinct *structural axis* (not just topical similarity) that is not already adequately covered. CLAUDE.md principle: "topical similarity alone is not enough."
- Main-thread only for structure, naming, and final synthesis (per current Deployed Subagent Strategy discipline).
- Draw from already-written source pages (Section Plan + Volume Synthesis Notes + claims), hub pages, and the pages they link to.
- Prioritize comparisons that add analytic value *not* already captured in a single concept/controversy/process page or hub.
- After writing: update source page `pages_created`/`pages_updated`; **actively look for integration opportunities** — ensure the network is bidirectional by adding the new comparison page (with a short description of its axis) to the Related sections (or appropriate body text) of the key concepts, controversies, places, hubs, and other pages it references; update `wiki/index.md`; append `log.md` entry in the established format.
- Integrate opportunistically: when a future ingest (or re-read for synthesis) surfaces a comparative chapter, include a comparisons/ pass in the "Step 4 — Review and tie together" phase.

**Prioritization criteria** (use for ordering):

1. Source is already ingested and explicitly comparative (CWH III highest priority).
2. Directly supports a major hub/theme that currently lacks a comparison link.
3. Cuts across multiple periods/civilizations with clear structural payoff.
4. Can be scoped tightly (one strong axis) rather than encyclopedic.

**Scope discipline**: Start with 5–8 focused, high-leverage pages rather than dozens. One broad "early cities" page + a handful of narrower ones is better than 20 micro-comparisons. Revisit after first batch.

## Critical Files to Modify / Create

**New files (the pages themselves)**:

- `wiki/comparisons/early-cities-in-comparative-perspective.md` (single synthesis page on the six axes; do not split unless the volume's experiment itself demands it)
- `wiki/comparisons/commercial-revolutions-compared.md`
- `wiki/comparisons/pristine-state-formation-variants.md`
- `wiki/comparisons/frontier-societies-and-core-expansion.md`
- `wiki/comparisons/religious-authority-structures-compared.md`
- `wiki/comparisons/empire-formation-and-collapse-patterns.md` (or more specific)
- Possibly 1–2 more (world-systems polycentricity; military-fiscal or ways-of-war)

**Edit existing**:

- `wiki/index.md` — append new rows to the existing Comparisons table (modeled on other sections) as pages are created; bump count in Summary Statistics when needed. (The initial catalog of the four existing pages is already in place.)
- `wiki/sources/yoffee-cwh-v3-2015.md` (and any others used) — increment `pages_created`/`pages_updated`, append comparison claim references if needed.
- `wiki/hubs/themes/state-formation.md`, `wiki/hubs/themes/empire-and-collapse.md`, `wiki/hubs/themes/warfare.md`, `wiki/hubs/themes/trade-economy.md`, `wiki/hubs/themes/religion.md`, `wiki/hubs/themes/technology.md` — add or expand a "Comparisons" or "See also structural comparisons" subsection linking the new pages (and ensure key concepts/controversies/places gain back-links).
- `wiki/hubs/civilizations/*.md` (selectively, e.g. rome, islam, china) — cross-link where relevant.
- `wiki/log.md` — append standard ingest/synthesis-style entries for the batch.
- (Light) `wiki/home.md` if the Comparisons blurb needs refreshing.
- Existing 4 comparison pages: normalization of frontmatter to the canonical schema is complete (axis_of_comparison added where missing; legacy field names standardized).

**No changes needed** to raw sources, Processing List, Outstanding Sources (derived pages), or core schemas.

## Existing Functions / Utilities / Patterns to Reuse

- **Page templates & tone**:
  - [wiki/comparisons/celtic-lands-and-english-expansion.md](wiki/comparisons/celtic-lands-and-english-expansion.md) — focused regional cases + outcomes + significance + Related with link types.
  - [wiki/comparisons/islamdom-and-occident-high-medieval.md](wiki/comparisons/islamdom-and-occident-high-medieval.md) — deep structural (Hodgson) with cosmology/law/society sections + assessment.
  - [wiki/comparisons/strategic-practice-across-civilizations.md](wiki/comparisons/strategic-practice-across-civilizations.md) and [wiki/comparisons/sexuality-in-world-belief-systems.md](wiki/comparisons/sexuality-in-world-belief-systems.md) — broad cross-civ from dedicated Cambridge vols: recurring vs. variation + assessment + Related.
- **Link taxonomy & distinctions**: CLAUDE.md "Link Types — Mandatory Distinctions" (especially `analogous_to` / `contrasts_with` for comparisons; never conflate with causation).
- **Source handling for comparative volumes**:
  - [wiki/sources/yoffee-cwh-v3-2015.md](wiki/sources/yoffee-cwh-v3-2015.md) (Section Plan + Volume Synthesis Note explicitly calls the volume a "comparative experiment"; lists the 6 parts and provocative juxtapositions like Rome–Tenochtitlan, Athens–Jenne-jeno).
  - Hodgson source pages (esp. Vol 2 synthesis of the Book Three Ch. VII comparison).
  - NCMH source pages (abulafia-ncmh-v5-2000.md, jones-ncmh-v6-2000.md, allmand-ncmh-v7-1998.md) that already credit the Celtic comparison.
- **Hub patterns**: See `wiki/hubs/themes/warfare.md` (already links the strategy comparison); `wiki/hubs/themes/empire-and-collapse.md`, `wiki/hubs/themes/state-formation.md`, `wiki/hubs/themes/trade-economy.md` (list debates + related hubs).
- **Synthesis & bookkeeping discipline**: CLAUDE.md "Step 4 — Review and tie together" + "Step 6 — Bookkeeping"; use of Volume Synthesis Notes; log entries; update index/overview after changes.
- **Naming**: kebab-case; titles descriptive of the axis (not just "X vs Y").
- **Lint / validation habits**: CLAUDE.md "Lint Workflow" + "Schema validator / wikilink checker" (ensure 0 broken links; complete frontmatter; Related section present).

## Proposed Prioritized List of Pages (First Batch)

**Note on deduplication**: Items 2 and 6 below were flagged during plan review as carrying high duplication risk with existing hubs, process pages, the `strategic-practice-across-civilizations` page, and standing controversies. They must pass the mandatory dedup gate above. If the residual structural axis is weak, they should be merged, dropped, or re-scoped narrowly.

1. ~~**Early Cities / Urbanism in Comparative Perspective**~~ (highest priority) — **created**
   - Source anchor: Yoffee *CWH Vol. III*.
   - Scope: One page covering the volume's experimental method + the six axes (performance/ritual, information technologies, landscapes, distribution of power/heterarchy, cities as creations, early imperial cities). Highlight key juxtapositions and the heterarchy insight.
   - Tags/scope: transregional; Chalcolithic–High Middle Ages.
   - Why: Directly titled "in Comparative Perspective"; foundational for places/urbanism; currently only fragmented into individual city pages. Low duplication risk.

2. **Pristine State Formation — Variants Across Regions** *(high duplication risk — audited, no new page created)*
   - Sources: CWH II/III/IV, state-formation process + hub material.
   - **Dedup gate result (2026-06-22)**: The `state-formation` hub already has a dedicated "## Pristine state formation — the first states" section listing independent emergences (Levant, Anatolia, Mesoamerica, Andes) and linking to the general process. The main `state-formation` process page covers "Pristine/secondary state emergence" as a phase, notes polycentric independent hearths, and discusses secondary formation. The just-completed Early Cities comparison already extracted the key structural insights from CWH III (including heterarchy vs hierarchy in Part IV cases like Jenne-jeno/Teotihuacan). Existing controversies on urban definitions and power distribution cover the interpretive debates. No sufficiently distinct *structural axis* remains that wouldn't duplicate or become a topical list. Decision: Do not create new page; value stays distributed in hub + process + Early Cities comparison. (May revisit if new source provides a sharper axis.)

3. **Commercial Revolutions Compared (Song China, High Medieval Occident, Southeast Asian Age of Commerce)**
   - Sources: CWH V (Song, commercial revolution), Reid *Age of Commerce*, related trade-economy pages.
   - Scope: Drivers, scale, social effects, limits; relation to state capacity and world-system position.
   - Ties to `wiki/hubs/themes/trade-economy.md` and Great Divergence controversy.

4. ~~**Frontier Societies and Responses to Core Expansion**~~ — **created**
   - Model on existing Celtic page.
   - Scope: British Isles (extend the existing), Baltic (Teutonic), Iberian Reconquista, Chinese southern frontiers, Russian steppe, perhaps American.
   - Sources: NCMH (already used), CWH chapters, empire/expansion material.
   - Leverages the existing Celtic page as precedent. Good structural focus on divergent outcomes under similar pressure.

5. ~~**Religious Authority and Institutions Across Major Traditions**~~ — **created**
   - Sources: Hodgson (ulama/amir aloofness, madrasa), Christianity pages, Indian/Confucian/Buddhist concepts, religion hub.
   - Scope: 'Ulama vs. Church hierarchy vs. monastic/sangha vs. Brahminical; integration with state; education and law.
   - Complements the existing sexuality comparison; supports `wiki/hubs/themes/religion.md` and civilization hubs.

6. ~~**Empire Formation, Universal Aspirations, and Collapse Patterns**~~ *(narrow residual axis after dedup gate)* — **created**
   - Sources: Strategy comparison (already covers universal monarchy), empire hub, CWH, specific collapses (Bronze Age, Western Rome, etc.), Harper, Diamond.
   - **Scope constraint**: The existing `strategic-practice-across-civilizations.md` already treats universal monarchy aspirations. The `empire-and-collapse.md` hub already organizes systems and collapses. This page may only proceed if a narrow residual structural axis is identified (e.g. "Distinct mechanisms of surplus extraction across imperial types"). Otherwise drop or contribute updates to the strategy page + hub instead.
   - Must not duplicate the collapse controversies.

**Optional follow-on** (if time/material strong):
- Polycentric world-systems / trade networks compared (Abu-Lughod + Indian Ocean + Atlantic sources).
- Legal legitimation styles (expand on the existing Hodgson page's moralism vs. formalism section).

## Additional Candidates from Deepsearch (for future batches, pending review)

Deepsearch across concepts/, hubs/, sources/, and log.md (targeting CWH V comparative syntheses, Reid material, ingest notes on cross-civilizational claims, and untapped axes) uncovered several strong structural comparison opportunities not yet distilled into standalone `comparisons/` pages. These fit plan criteria: explicit structural (not topical lists), clear axis of comparison, drawing from existing ingested sources (esp. CWH V chapters), avoiding duplication with current comparisons, hubs, or controversies.

Candidates (prioritized roughly by source strength and distinctiveness):

1. ~~**Courtly Culture in Eurasia**~~ — **created**  
   Source: CWH V Ch. 7 (Geary et al.).  
   Axis: Courts as specialized communities generating codes of conduct via favor-competition; borrowing created a "single Eurasian system" of power representation (Europe, Byzantium, Islamic, India, China, Japan).  
   Why: Distinct from empire/strategy; cultural-political performance focus. Concept exists; no dedicated comparison page.

2. **Educational Institutions in Comparative Perspective**  
   Source: CWH V Ch. 5 (Linda Walton).  
   Axis: Knowledge valued/transmitted; relation to state; access determining status/power (Confucian exams, madrasa, universities, etc.). Ties to collective learning.  
   Why: Builds on religious authority comparison but education-specific. Strong CWH synthesis.

3. ~~**Social Hierarchy and Solidarity Comparatively**~~ — **SKIPPED (dedup)**: the `concepts/social-hierarchy-and-solidarity` page already *is* Reynolds' comparative synthesis (Key Claims + the feudalism critique). No distinct residual axis.  
   Source: CWH V Ch. 4 (Susan Reynolds).  
   Axis: Universality of justified inequality via reciprocity; hierarchy + solidarity coexisting; "feudalism" as Eurocentric category (comparative critique).  
   Why: Addresses structural causation and feudalism debates; complements empire/hierarchy work.

4. ~~**The Theatre State and Exemplary Centres**~~ — **CREATED** as `theatre-state-and-the-bases-of-power` (scoped to spectacle vs. coercion as the basis of power, with the critique that the dichotomy is overdrawn).  
   Sources: Reid Vol. 1 (Geertz model), SE Asia concepts (theatre-state, devaraja, absolutism).  
   Axis: Power as spectacle/ritual (not coercion); court as cosmic model; festival as politics (SE Asia/Indic, with critiques).  
   Why: Specific structural model; already concept + Reid synthesis; extends cultural florescence.

5. ~~**Industrious Revolutions in Global Perspective**~~ — **SKIPPED (dedup)**: the `processes/industrious-revolution` page already carries the "Shared Phenomenon, Divergent Paths" comparison (Sugihara), reinforced by `great-divergence` and `commercial-revolutions-compared`.  
   Sources: CWH VI/VII (Sugihara/Wong), Song material, Great Divergence controversy.  
   Axis: Labor-intensive household production (East Asia) vs capital/resource-intensive paths (Europe); implications for divergence/convergence.  
   Why: Extends commercial revolutions comparison; economic paths without duplicating.

6. ~~**Military Revolutions Comparatively**~~ — **SKIPPED (dedup)**: the `concepts/military-revolution` page already carries Parker's global thesis + Black's critique across ~21 civilizations, with `gunpowder-empires` and `strategic-practice-across-civilizations` covering the cases.  
   Sources: Strategy volumes, CWH, military-revolution controversy, SE Asian absolutism/gunpowder.  
   Axis: Gunpowder, drill, fiscal-military adaptations across Europe, Ottoman/Mughal, China, Japan, SE Asia (not single Western event).  
   Why: Narrows strategic-practice page; global test cases.

7. ~~**Convivenica and Plural Societies**~~ — **CREATED** as `managing-religious-pluralism-compared` (dhimma/millet/convivencia/Latin-Christendom; scoped to the legal form of incorporating subordinate religions, distinct from the Furnivall *colonial* `plural-society` concept).  
   Sources: Iberia (NCMH/Lapidus), Ottoman concepts, convivencia mentions.  
   Axis: Managed religious/ethnic pluralism under different legal regimes (dhimmi, millet) vs assimilation/conflict.  
   Why: Structural on coexistence; complements religious authority.

8. ~~**Debt Bondage and Unfree Labor Systems Comparatively**~~ — **CREATED** as `unfree-labor-systems-compared` (debt-bondage / chattel slavery / serfdom / military slavery / mita on the manpower-vs-land axis; no prior comparative page existed).  
   Sources: SE Asia debt-bondage concept, slavery process, serfdom mentions, comparative notes (log: South Atlantic/Mediterranean roots).  
   Axis: Manpower vs land as power basis; debt as master-bond vs chattel slavery/serfdom; state/economic implications.  
   Why: Cross-civilizational on unfree labor forms.

**Bonus granular (from ingest log notes):** Han–Rome comparisons (coinage, taxation, administration, women's roles); Mediterranean–China urban/commercial contrasts.

These could expand the section significantly while preserving quality. Add to future batches after review. (Sources: mostly CWH V syntheses and Reid material already in wiki.)

## Verification Section (End-to-End Test)

After implementation of a batch:

1. Create the new `.md` file(s) with complete frontmatter + body per template. Confirm via `read_file`.
2. Ensure every wikilink targets an existing page (use grep or Obsidian-style check mentally; aim for 0 broken).
3. Add inbound links from at least the source page + 1–2 relevant hubs/themes/civilization pages; **actively add back-links from the key concepts/controversies/places referenced in this page** (e.g., to their Related sections); verify the new comparison page links back usefully with correct link labels.
4. Edit `wiki/index.md`:
   - Replace the Comparisons header block with an actual catalog table (title | axis | key sources | periods/regions).
   - Confirm the "Comparisons | N" stat is accurate or incremented.
5. Update the source page(s) `pages_created` / `pages_updated` counts and add a brief note in the synthesis section.
6. Append a dated log entry (or section entries) following patterns in `log.md` (e.g. "comparison | Title | Sources: X | Pages created: 1").
7. Spot-check 1–2 hubs read the new links; optionally update `wiki/overview.md` "Known Gaps" or hub "Debates" if a comparison resolves or reframes something.
8. Review each new page against CLAUDE.md principles:
   - Clear axis of comparison (not just topical similarity).
   - Link taxonomy used precisely.
   - Historiography or assessment present where the comparison is interpretive.
   - Collection bias noted if relevant.
9. (Optional but recommended) Run a full-repo grep for the new page name to confirm cross-references; re-read the new file after any link edits.
10. Commit discipline: stage only `wiki/` changes, commit with source-aware message ending in Co-Authored-By trailer (per CLAUDE standing rule).

**Success criteria**: The new pages are discoverable from home → hubs → comparisons; they surface non-obvious structural insight; they integrate cleanly without duplicating existing pages; index and hubs are consistent.

## Notes on Trade-offs & Open Items

- **Broad vs. narrow**: Existing pages show both work. Prefer one solid page per major source axis rather than micro-pages.
- **Order**: CWH III first (because the source itself is framed as comparative and under-exploited for this purpose). Then hub-derived.
- **No new source ingestion**: This plan uses material already on disk (source pages, hubs, prior synthesis). If a key comparative chapter was only lightly touched, a targeted main-thread re-read of that slice is acceptable but should be logged.
- **Maintenance**: Comparisons are "permanent" (per CLAUDE); they will be updated when new contradictory or deepening material arrives (use Contradiction Protocol if needed).
- **Ambiguity resolved in plan**: We do not create a page for every possible juxtaposition; only those with clear source grounding and hub value. If user prefers a different first batch or different scoping, they can adjust the list at execution time.

This plan is actionable, reuses all documented patterns, touches only the necessary files, and directly fulfills the request to "create the pages that will go into the Comparisons section."

---

**Maintenance note**: When work progresses, update the "Currently only four pages exist" section, cross off completed items in the prioritized list, and append a short progress note at the top of this file.