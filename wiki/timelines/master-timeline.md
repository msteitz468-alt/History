---
title: Master Timeline
hub_type: timeline
last_updated: 2026-06-22 (cross-checked against The Times Atlas of World History 1999 ed. for selected geographic/chronological anchors)
tags: [hub, timeline]
---

# Master Timeline

> The chronological spine of the wiki. Every page is anchored to at least one of the 24
> periods below. Each period page is wired with `preceded_by` / `followed_by` so you can
> walk the spine forward or backward from any point. The **transitions** between periods —
> the genuine discontinuities — get their own pages.

[[home|← Home]] · [[overview|Coverage Map]]

---

## The 24-Period Framework

| # | Period | Date Range | Coverage | Major transition into the next |
|---|---|---|---|---|
| 1 | [[deep-prehistory|Deep Prehistory]] | before 3.3 Mya BP | weak | — |
| 2 | [[early-prehistory|Early Prehistory]] | 3.3 Mya–300,000 BP | moderate | emergence of _Homo sapiens_ |
| 3 | [[late-prehistory|Late Prehistory]] | 300,000–50,000 BP | moderate | behavioral modernity |
| 4 | [[behavioral-modernity|Behavioral Modernity]] | 50,000–12,000 BP | strong | end of the Ice Age |
| 5 | [[mesolithic|Mesolithic]] | 12,000–9,500 BP | moderate | adoption of farming |
| 6 | [[neolithic|Neolithic]] | 9,500–3,000 BCE | strong | metallurgy, first cities |
| 7 | [[chalcolithic|Chalcolithic]] | 5,500–3,300 BCE | moderate | bronze, urban states |
| 8 | [[early-bronze-age|Early Bronze Age]] | 3,300–2,100 BCE | moderate | — |
| 9 | [[middle-bronze-age|Middle Bronze Age]] | 2,100–1,550 BCE | moderate | — |
| 10 | [[late-bronze-age|Late Bronze Age]] | 1,550–1,200 BCE | strong | **[[bronze-age-collapse-1200bce|the Bronze Age Collapse]]** |
| 11 | _[[bronze-age-collapse-1200bce|Bronze Age Collapse]]_ (transition) | ~1,200–1,150 BCE | strong | systemic collapse of palace economies |
| 12 | [[early-iron-age|Early Iron Age]] | 1,200–800 BCE | moderate | rise of the polis & alphabet |
| 13 | [[archaic-period|Archaic Period]] | 800–500 BCE | strong | classical efflorescence |
| 14 | [[classical-antiquity|Classical Antiquity]] | 500–31 BCE | strong | Roman imperial order |
| 15 | [[late-antiquity|Late Antiquity]] | 31 BCE–600 CE | strong | **[[fall-of-the-western-roman-empire-476|fall of the Western Roman Empire]]**; rise of Islam |
| 16 | [[early-middle-ages|Early Middle Ages]] | 600–1000 CE | strong | commercial & demographic takeoff |
| 17 | [[high-middle-ages|High Middle Ages]] | 1000–1300 CE | strong | **[[mongol-conquests-13th-century|the Mongol conquests]]**; crisis of the 14th c. |
| 18 | [[late-middle-ages|Late Middle Ages]] | 1300–1500 CE | strong | **[[columbian-exchange-1492|1492 & the Columbian Exchange]]** |
| 19 | [[early-modern|Early Modern]] | 1500–1700 CE | moderate | global trade, gunpowder empires |
| 20 | [[age-of-expansion|Age of Expansion]] | 1700–1800 CE | moderate | **[[french-revolution-1789|1789 & the Atlantic Revolutions]]** |
| 21 | [[long-19th-century|Long 19th Century]] | 1800–1914 CE | moderate | **[[1914-end-of-long-19th-century|1914]]** |
| 22 | [[world-wars-era|World Wars Era]] | 1914–1945 CE | moderate | **[[1945-postwar-order|1945 & the postwar order]]** |
| 23 | [[cold-war|Cold War]] | 1945–1991 CE | strong | **[[1991-end-of-cold-war|1991 & the end of the Cold War]]** |
| 24 | [[contemporary|Contemporary]] | 1991–present | weak | — |

---

## Regional sub-period spines

Some regions are tracked at finer resolution, nested under the global periods:

- **Aegean (within Early Iron Age):** [[greek-dark-age|Greek Dark Age]] (c. 1200–800 BCE)
- **India:** [[vedic-period|Vedic Period]] (c. 1500–600 BCE)
- **Japan:** [[nara-period|Nara]] → [[heian-period|Heian]] → [[kamakura-period|Kamakura]] →
  [[muromachi-period|Muromachi]] → [[azuchi-momoyama-period|Azuchi–Momoyama]] →
  [[edo-period|Edo]] → [[meiji-period|Meiji]] → [[taisho-period|Taishō]]

---

## Synchronic snapshots — "meanwhile, around the world"

Cross-regional cuts through a single moment, showing what was happening everywhere at once.

- **[[synchronic-1200bce|c. 1200 BCE]]** — the Bronze Age Collapse
- **[[synchronic-1ce|c. 1 CE]]** — the age of empires (Rome, Han, Parthia, Kushan)
- **[[synchronic-1200ce|c. 1200 CE]]** — the Eurasian high-medieval world on the eve of the Mongols
- **[[synchronic-1500ce|c. 1500 CE]]** — the world the Columbian Exchange connected

---

## All period pages (live)

```base
filters:
  and:
    - 'tags.contains("period")'
views:
  - type: table
    name: Periods by number
    order:
      - period_number
      - title
      - date_range
      - collection_coverage
    sort:
      - property: period_number
        direction: ASC
```

## All events on the timeline (live)

```base
filters:
  and:
    - 'tags.contains("event")'
views:
  - type: table
    name: Events by start date
    order:
      - title
      - date_start
      - region
      - event_type
      - scale_consequential
    sort:
      - property: date_start
        direction: ASC
```

> **Note:** the event view sorts on the raw `date_start` field, which mixes BP / BCE / CE
> string formats; ordering is approximate near the prehistoric/historic boundary. For exact
> chronology within a period, use that period page's own narrative.
