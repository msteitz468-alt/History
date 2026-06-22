---
title: "Warfare & Conflict — Thematic Hub"
hub_type: theme
theme: warfare
last_updated: 2026-06-22
tags: [hub, theme, warfare]
---

# Warfare & Conflict — Thematic Hub

> War is the densest single theme in the wiki: **~160 battle/war/siege/conquest events**, plus the
> processes and institutions that made armies possible. This hub reads warfare *vertically* — how
> the conduct of war was transformed, era by era — and *laterally*, across the recurring problems
> (logistics, fortification, the infantry–cavalry balance, sea power, the fiscal cost of armies)
> that every military system had to solve. The exhaustive, auto-updating lists are the **Bases
> views** at the bottom; the curated threads below are the spine.

[[home|← Home]] · [[master-timeline|Master Timeline]] · related: [[hubs/themes/state-formation|State Formation]] ·
[[hubs/themes/technology|Technology]] · [[hubs/themes/empire-and-collapse|Empire & Collapse]]

---

## The long arc of military transformation

Each era is defined less by *who* fought than by *what made armies effective* — and every such
system eventually met a counter-system. This is the analytical spine; follow it forward in time.

### Bronze & Early Iron Age — the chariot and the citizen-soldier
The [[late-bronze-age|Late Bronze Age]] palace armies fought with massed **chariots**
([[battle-of-qadesh-1274bce|Qadesh, 1274 BCE]] — the best-documented battle of the era).
The [[bronze-age-collapse-1200bce|Bronze Age Collapse]] swept this system away; cheaper **iron**
and infantry reopened war to broader social classes.

### Archaic & Classical — the heavy-infantry revolution
The Greek **[[hoplite-warfare|hoplite phalanx]]** ([[greek-warfare|Greek warfare]]) tied military
power to the citizen body and the polis — war and political participation fused.
The [[greco-persian-wars-499bce|Greco-Persian Wars]] ([[battle-of-marathon-490bce|Marathon]],
[[battle-of-salamis-480bce|Salamis]], [[battle-of-plataea-479bce|Plataea]]) and the long
[[peloponnesian-war|Peloponnesian War]] tested it; [[battle-of-leuctra-371bce|Leuctra]] broke
Spartan primacy; [[philip-ii-of-macedon|Philip II]] and the **Macedonian** pike-and-cavalry
combined-arms system ([[battle-of-chaeronea-338bce|Chaeronea]], [[battle-of-gaugamela-331bce|Gaugamela]])
superseded it.

### Roman — the legion and the logistics of empire
The manipular/cohort **legion** turned discipline and engineering into a war-winning system that
survived even [[battle-of-cannae-216bce|Cannae]] in the [[second-punic-war-218-201bce|Second Punic War]].
Rome's real military edge was logistical and political — the capacity to raise, pay, and replace
armies. Its long decay runs through [[battle-of-adrianople-378|Adrianople (378)]] to the
[[fall-of-the-western-roman-empire-476|fall of the West]].

### Medieval — cavalry, castle, and the siege
[[medieval-warfare|Medieval warfare]] centred on the heavy **mounted knight**, the **castle**, and
the dominance of siege over battle ([[military-history-middle-millennium|military history of the middle millennium]]).
The [[first-crusade-1095|Crusades]] projected this system into the Levant; the
[[mongol-conquests-13th-century|Mongol conquests]] and the [[mongol-army|Mongol army]] — steppe
horse-archer mobility ([[pastoral-nomadism|pastoral nomadism]] as a military base) — proved the
deadliest counter until checked at [[battle-of-ain-jalut-1260|Ain Jalut]].
Infantry reasserted itself: [[battle-of-courtrai-1302|Courtrai]], the longbow of the
[[hundred-years-war-1337|Hundred Years' War]].

### Early Modern — the Military Revolution
The **[[military-revolution|Military Revolution]]**: gunpowder, the **trace italienne** fortress,
drilled infantry, and ballooning army sizes drove the rise of the **[[fiscal-military-state|fiscal-military state]]**
— states reorganised to finance war. The [[thirty-years-war-1618|Thirty Years' War]] and the
gunpowder empires of Eurasia (Ottoman [[janissaries|Janissaries]], Mughal, Qing) embody it;
[[battle-of-plassey-1757|Plassey]] and the [[seven-years-war-1756|Seven Years' War]] globalise it.

### Industrial & Total — war without limit
The [[industrialization-of-warfare|industrialization of warfare]] and the
[[napoleonic-wars|levée en masse]] produced the nation-in-arms; the
[[first-world-war-1914|First]] and [[second-world-war-1939|Second World Wars]] realised
**[[total-war|total war]]** — entire economies ([[war-economy|war economy]]) and populations
mobilised. The [[nuclear-arms-race|nuclear arms race]] of the [[cold-war|Cold War]] made
great-power total war potentially suicidal, displacing it into proxy and limited conflict.

---

## Recurring problems (read laterally, across all eras)

- **Infantry vs. cavalry vs. missile** — the rock-paper-scissors that resets with each technology:
  phalanx, legion, knight, horse-archer, pike-and-shot, the machine gun.
- **The fortress and the siege** — from city walls to the *trace italienne*; siege usually beat
  open battle for deciding wars.
- **Sea power** — [[battle-of-salamis-480bce|Salamis]], [[battle-of-actium-31bce|Actium]], and the
  later blue-water navies that made [[hubs/themes/trade-economy|maritime empires]] possible.
- **Paying for it** — [[fiscal-military-state|fiscal-military state]], [[war-economy|war economy]]:
  the deepest structural driver, tying warfare to [[hubs/themes/state-formation|state formation]] and taxation.
- **Steppe vs. sown** — [[pastoral-nomadism|nomadic]] mobility against settled agrarian empires, the
  longest-running asymmetry in Eurasian history.

## Ideas about war

- [[strategy|Strategy]] · [[fabian-strategy|Fabian strategy]] · [[just-war|just-war theory]] ·
  [[total-war|total war]]
- **Comparison:** [[strategic-practice-across-civilizations|Strategic practice across civilizations]]

## Major debates (see the [[hubs/historiography-hub|Historiography Hub]])
- Was there a single early-modern **[[military-revolution|Military Revolution]]**, or several?
- How decisive was warfare (vs. disease, economics) in the European conquest of the Americas?
- Did infantry "supremacy" really rise and fall, or is that narrative a Eurocentric artefact?

---

## All warfare pages (live)

### Battles, wars, sieges & conquests

```base
filters:
  and:
    - 'tags.contains("event")'
    - 'event_type.containsAny("battle", "war", "siege", "conquest")'
views:
  - type: table
    name: Conflicts by date
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

### Military processes & institutions

```base
filters:
  and:
    - 'process_type.contains("military") or tags.contains("warfare")'
views:
  - type: table
    name: Military processes
    order:
      - title
      - date_start
      - region
    sort:
      - property: date_start
        direction: ASC
```

> **Bases note:** these filters use `event_type` / `process_type` / `tags`. If your installed Bases
> version rejects `containsAny` or the `or` expression, split each into separate single-condition
> views — paste me the error and I'll adjust to your version.
