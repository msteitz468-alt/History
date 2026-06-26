---
title: "Disease & Demography — Thematic Hub"
hub_type: theme
theme: disease-demography
last_updated: 2026-06-22
tags: [hub, theme, disease-demography]
---

# Disease & Demography — Thematic Hub

> Population — its growth, movement, and catastrophic contraction — is one of history's deepest
> forces, and disease is its sharpest editor. This hub ties together the great migrations, the
> demographic regimes that farming and cities created, and the epidemics that repeatedly reshaped
> the human map. The exhaustive auto-list is the **Bases view** below.

[[home|← Home]] · [[master-timeline|Master Timeline]] · related: [[hubs/themes/technology|Technology]] ·
[[hubs/themes/trade-economy|Trade & Economy]] · [[hubs/themes/empire-and-collapse|Empire & Collapse]]

---

## Peopling the planet — migration
- [[paleolithic-global-dispersal|Paleolithic global dispersal]] · [[migration-in-human-history|migration in human history]] ·
  [[sedentism|sedentism]] · [[urbanization|urbanization]].
- Major movements: the [[indo-european-migrations|Indo-European migrations]] · the [[bantu-expansion|Bantu expansion]] ·
  [[greek-colonization|Greek colonization]] · [[seleucid-colonization|Seleucid colonization]] ·
  [[pacific-voyaging-and-settlement|Pacific voyaging]] · [[early-modern-migrations|early-modern migrations]].
- Forced movement: [[assyrian-mass-deportation|Assyrian deportation]] · the [[babylonian-exile|Babylonian Exile]] ·
  the [[atlantic-slave-trade|Atlantic slave trade]].

## Demographic regimes
- The farming transition and its costs; the [[late-medieval-crisis|late-medieval crisis]];
  the [[demographic-transition|demographic transition]] of the modern era; [[disease-in-modern-history|disease in modern history]].

## Epidemics that bent history
- [[plague-of-athens-430bce|Plague of Athens (430 BCE)]] · the [[antonine-plague-165|Antonine Plague (165)]] ·
  the [[justinianic-plague-541|Justinianic Plague (541)]] · the [[black-death|Black Death]] ·
  the [[virgin-soil-epidemics|virgin-soil epidemics]] of the [[columbian-exchange-1492|Columbian Exchange]].

## Debates (→ [[hubs/historiography-hub|Historiography Hub]])
- [[pre-columbian-american-population|How many people lived in the pre-Columbian Americas?]] ·
  [[pleistocene-megafaunal-extinction|did humans cause the megafaunal extinctions?]]
- [[agriculture-and-human-health|Did agriculture worsen human health?]] ·
  [[impact-of-atlantic-slave-trade-on-africa|the demographic impact of the slave trade on Africa]].

---

## All disease & demography pages (live)

```base
filters:
  and:
    - 'process_type.contains("demographic") or event_type.contains("epidemic") or event_type.contains("migration") or tags.contains("disease-demography")'
views:
  - type: table
    name: Disease & demography pages by date
    order: [title, date_start, period, region]
    sort:
      - property: date_start
        direction: ASC
```
