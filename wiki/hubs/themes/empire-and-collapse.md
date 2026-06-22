---
title: "Empire & Collapse — Thematic Hub"
hub_type: theme
last_updated: 2026-06-22
tags: [hub, theme, empire-and-collapse]
---

# Empire & Collapse — Thematic Hub

> **Stub hub** — part of the wiki's navigation skeleton. The live Bases view below auto-lists every
> page tagged for this theme; a curated narrative spine and "key threads" list are written in a
> later pass. See [[home|Home]] for the full hub map and [[master-timeline|the timeline]] for chronology.

[[home|← Home]] · [[master-timeline|Master Timeline]] · [[overview|Coverage Map]]

## All empire & collapse pages (live)

```base
filters:
  and:
    - 'actor_type.contains("empire") or event_type.contains("collapse")'
views:
  - type: table
    name: empire & collapse pages
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
> need a `empire-and-collapse` tag normalized into their frontmatter, or the filter expression adjusted to your
> installed Bases version.
