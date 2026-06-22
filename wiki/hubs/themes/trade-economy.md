---
title: "Trade & Economy — Thematic Hub"
hub_type: theme
last_updated: 2026-06-22
tags: [hub, theme, trade-economy]
---

# Trade & Economy — Thematic Hub

> **Stub hub** — part of the wiki's navigation skeleton. The live Bases view below auto-lists every
> page tagged for this theme; a curated narrative spine and "key threads" list are written in a
> later pass. See [[home|Home]] for the full hub map and [[master-timeline|the timeline]] for chronology.

[[home|← Home]] · [[master-timeline|Master Timeline]] · [[overview|Coverage Map]]

## All trade & economy pages (live)

```base
filters:
  and:
    - 'process_type.contains("economic") or event_type.contains("economic")'
views:
  - type: table
    name: trade & economy pages
    order:
      - title
      - date_start
      - period
      - region
    sort:
      - property: date_start
        direction: ASC
```

> **Bases note (stub):** the filter above is provisional. If it under-lists, the relevant pages may
> need a `trade-economy` tag normalized into their frontmatter, or the filter expression adjusted to your
> installed Bases version.
