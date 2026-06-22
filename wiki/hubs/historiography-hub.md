---
title: "Historiography Hub — How We Know"
hub_type: historiography
last_updated: 2026-06-22
tags: [hub, historiography]
---

# Historiography Hub — How We Know

> Per CLAUDE.md, **historiography is first-class content**: how we know what we know — the sources,
> their biases, the methods, and the live scholarly disputes — sits alongside the history itself.
> This hub is the index to that layer: the **55 controversy pages** (grouped below by the kind of
> dispute), the **methods and traditions** of history-writing, and the standing debates the wiki is
> committed to tracking. The exhaustive, auto-grouped list is the **Bases view** at the bottom.

[[home|← Home]] · [[master-timeline|Master Timeline]] · [[overview|Coverage Map]]

---

## Controversies by type of dispute

Most pages carry a `dispute_type` (causation / periodization / scale / source-reliability /
interpretation / counterfactual / moral-assessment). Curated groupings:

### Causation — *what caused X?*
[[causes-of-the-fall-of-the-western-roman-empire|Fall of the West]] ·
[[fall-of-rome-causes|Fall of Rome (causes)]] · [[fall-of-roman-republic|Fall of the Republic]] ·
[[causes-of-second-punic-war|Second Punic War]] · [[causes-of-the-first-world-war|First World War]] ·
[[causes-of-the-second-world-war|Second World War]] · [[great-divergence|the Great Divergence]] ·
[[causes-of-latin-american-underdevelopment|Latin American underdevelopment]] ·
[[why-did-agriculture-begin|why agriculture began]] · [[pirenne-thesis|the Pirenne thesis]] ·
[[societal-collapse-and-environmental-determinism|collapse & environmental determinism]].

### Source reliability — *can we trust the evidence?*
[[herodotus-reliability|Herodotus]] · [[homeric-poems-as-history|the Homeric poems]] ·
[[reliability-of-early-roman-tradition|early Roman tradition]] · [[the-exodus|the Exodus]] ·
[[the-mongol-yasa|the Mongol Yasa]] · [[philinus-treaty-controversy|the Philinus treaty]].

### Interpretation — *what does it mean / how did it work?*
[[nature-of-roman-imperialism|Roman imperialism]] · [[roman-grand-strategy|Roman "grand strategy"]] ·
[[nature-of-carolingian-government|Carolingian government]] · [[feudalism-construct-debate|is "feudalism" a real thing?]] ·
[[feudal-revolution-debate|the feudal revolution]] · [[indian-feudalism-debate|Indian feudalism]] ·
[[seleucid-hellenization|Seleucid Hellenization]] · [[ptolemaic-economy|the Ptolemaic economy]] ·
[[military-revolution-thesis|the Military Revolution]] · [[ottoman-decline-thesis|Ottoman "decline"]] ·
[[axial-age-controversy|the Axial Age]] · [[zen-and-medieval-japanese-aesthetics|Zen & Japanese aesthetics]] ·
the theological disputes [[arian-controversy|Arian]], [[monothelite-controversy|Monothelite]],
[[three-chapters-controversy|Three Chapters]].

### Scale & population — *how big / how many?*
[[pre-columbian-american-population|pre-Columbian American population]] ·
[[pleistocene-megafaunal-extinction|megafaunal extinction]] ·
[[impact-of-atlantic-slave-trade-on-africa|impact of the Atlantic slave trade]].

### Origins, peopling & diffusion — *where did they come from?*
[[indo-european-origins|Indo-European origins]] · [[afroasiatic-homeland|Afroasiatic homeland]] ·
[[austronesian-dispersal|Austronesian dispersal]] · [[demic-vs-cultural-diffusion|demic vs. cultural diffusion]] ·
[[homo-sapiens-emergence-date|emergence of *Homo sapiens*]] ·
[[clovis-first-vs-pre-clovis|Clovis-first vs. pre-Clovis]] ·
[[australasian-colonization-timing|peopling of Australasia]] ·
[[peopling-of-ancient-egypt|peopling of ancient Egypt]] ·
[[hamitic-hypothesis-african-states|the Hamitic hypothesis]] (and its racist legacy).

### Periodization & definition — *where are the boundaries?*
[[what-defines-a-city|what defines a city?]] ·
[[hierarchy-vs-heterarchy-early-cities|hierarchy vs. heterarchy in early cities]] ·
[[north-american-states-debate|were there North American "states"?]] ·
[[axial-age-controversy|the Axial Age]] (also periodization).

### Chronology — *when, exactly?*
[[mesopotamian-chronology|Mesopotamian chronology]] · [[ancient-near-eastern-chronology|ANE chronology (method)]] ·
[[fall-of-knossos|the fall of Knossos]] · [[ahhiyawa-question|the Ahhiyawa question]].

### Moral assessment — *how do we judge it?*
[[black-legend|the Black Legend]] · [[williams-thesis-abolition-debate|the Williams thesis]] ·
[[agriculture-and-human-health|did farming make us worse off?]] ·
[[ottoman-impact-on-european-expansion|Ottoman impact on European expansion]] ·
[[pre-islamic-trans-saharan-trade|pre-Islamic trans-Saharan trade]].

---

## How history is written — methods & traditions

The *emic* historiographies (how past societies recorded their own past) and *etic* methods
(how modern scholars reconstruct it):

- **Ancient traditions:** [[classical-greek-historiography|Greek]] ·
  [[fourth-century-greek-historiography|4th-c. Greek]] · [[hellenistic-historiography|Hellenistic]] ·
  [[early-roman-source-criticism|early Roman source criticism]] ·
  [[christian-providential-historiography|Christian providential history]].
- **Non-Western & oral:** [[african-historiography|African historiography]] ·
  [[griot-oral-tradition|the griot oral tradition]] · [[global-historiography|global history]].
- **Method & framing:** [[periodization-world-history|periodizing world history]] ·
  [[archaeogenetics|archaeogenetics]] · [[ancient-near-eastern-chronology|absolute & relative chronology]].

---

## Standing debates the wiki commits to track
(from CLAUDE.md's required-controversies list)

- Causes of the [[bronze-age-collapse-1200bce|Bronze Age Collapse]]
- [[causes-of-the-fall-of-the-western-roman-empire|Fall of the Western Roman Empire]]
- [[pre-columbian-american-population|Population of the pre-Columbian Americas]]
- Great-Man vs. structural causation — see [[strategy]] and the causation cluster above
- [[herodotus-reliability|Reliability of Herodotus]]
- [[indo-european-origins|Origins of the Indo-Europeans]]
- Geographic determinism (Diamond) & its critics —
  [[societal-collapse-and-environmental-determinism|collapse & environmental determinism]]

---

## Every controversy (live, grouped by dispute type)

```base
filters:
  and:
    - 'tags.contains("controversy")'
views:
  - type: table
    name: Controversies by dispute type
    group_by: dispute_type
    order:
      - title
      - dispute_type
      - resolution_status
      - period_involved
    sort:
      - property: dispute_type
        direction: ASC
```

> **Bases note:** this groups on the `dispute_type` property and shows `resolution_status`
> (open / partially-resolved / resolved-by-consensus). If grouping errors in your Bases version,
> drop the `group_by` line for a flat table and tell me the message.
