# WhiskyBase

An open-source educational knowledge base for Scotch whisky production,
tasting, and analysis.

## What this project is

A structured, queryable, fact-grounded reference for how Scotch whisky
is made and how specific releases compare. The project is built around
three goals, in this priority order:

1. **Reference accuracy.** Every claim is sourced; conflicts between
   sources are recorded rather than smoothed away.
2. **Educational depth.** Topics that benefit from context (peating
   measurement methods, still geometry, cask programmes) get
   structured explainers, not marketing copy.
3. **Exploratory analysis.** Once enough data exists, the structure
   supports comparison, filtering, and pattern-spotting across
   distilleries, lines, and bottlings.

## What this project is not

- Not a consumer recommendation engine.
- Not a tasting club, scoring site, or market-price tracker.
- Not a marketing channel for distilleries.
- Not a substitute for primary sources — the goal is to organise and
  cite, not to replace.

## How it is organised

The data lives as YAML and Markdown files in this repository. There
are five entity types:

| Entity | Lives in | Documents |
|---|---|---|
| Distillery | `/data/distilleries/` | Physical production site: location, equipment, ownership, history |
| Production line | `/data/production_lines/` | A recipe/spec produced at a distillery (one distillery may run several) |
| Bottling | `/data/bottlings/` | A specific commercial release |
| Concept | `/data/concepts/<kind>/` | Reference pages: methodology, educational, equipment, practice, glossary |
| Bottler | `/data/bottlers/` | Commercial bottling entity, for independent bottlers (planned) |

Cross-references between entities use slug strings; the build pipeline
(not yet implemented) resolves these to links.

Each entity type has a YAML template in `/schema/` that documents the
fields with inline comments. Read the templates before writing entries.

## Voice and discipline

The project uses a **strict reference register** for production-data
descriptions and a slightly more permissive **technical-teaching
register** for educational concept pages. Both registers reject
celebratory marketing language. See `docs/voice-register.md` for the
full rules and the disallowed-words list.

## Sources and conflicts

Every entry numbers its sources and references them inline via `[1]`,
`[2]` notation. When sources disagree, the entry resolves to one figure
with a comment explaining the choice; the conflict itself is preserved
in a sibling `<entity>.NOTES.md` file. See
`docs/source-conflict-policy.md`.

## Licence

- **Data and documentation** (everything in `/data/`, `/docs/`,
  `/schema/`): CC-BY-SA 4.0. See `LICENSE-data`.
- **Code** (scripts, build tooling, future site source): MIT. See
  `LICENSE-code`.

## Contributing

Contribution mechanism is the standard GitHub pull-request flow. There
is no separate authentication, no proposal queue, no custom UI — PRs
*are* the proposal queue. See `docs/contributing.md` (stub for now).

## Current state

| Layer | Status |
|---|---|
| Entity schemas | Distillery v0.1, production_line v0.2.1, bottling v0.2, concept v0.1, bottler v0.1 (stub) |
| Distilleries populated | 2 (Harris, Bruichladdich) |
| Production lines | 4 |
| Bottlings | 10 |
| Concept pages | 3 (1 methodology, 1 educational, 1 equipment) |
| Build pipeline | not yet implemented |

See `TODO.md` for the active queue and `docs/handover.md` for the
project's current design rationale.
