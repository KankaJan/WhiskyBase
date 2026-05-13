# Changelog

All notable schema changes are recorded here. Data additions (new
distilleries, lines, bottlings) are tracked through Git history, not
in this file.

The schemas use independent version numbers; a single project version
covers them all.

---

## [0.2] — 2026-05-13

Initial repository commit. Project state extracted from prior
design conversation; all schemas brought to internally consistent
versions before commit.

### Schema versions at commit time

- `distillery.template.yml` v0.1
- `production_line.template.yml` v0.2
- `bottling.template.yml` v0.2
- `concept.template.yml` v0.1
- `bottler.template.yml` v0.1 (draft, no entries populated)

### Schema changes in this commit

**`bottling.template.yml` v0.1 → v0.2**

- Renamed `distillery` field to `produced_at_distillery` for clarity
  when independent bottlings are introduced. Migrates all 10 existing
  bottlings.
- Added `bottled_by` (REQUIRED). For OB releases, references the same
  slug as `produced_at_distillery`. For IB releases (none yet
  populated), references a slug under `/data/bottlers/`.
- Added `bottler_type` (REQUIRED). One of `distillery |
  independent_bottler`. Stored on the bottling for direct filtering
  without entity lookup.
- Added `bottler_series` (OPTIONAL). Series slug namespaced under the
  bottler, e.g. `cadenheads/authentic-collection`. Used for both IB
  series and producer series like `octomore-masterclass-08`.

**`production_line.template.yml` v0.1 → v0.2** (in prior session, but
relevant for migration history)

- Replaced flat `peating_ppm` field with structured `peating` block
  supporting multi-stage, multi-method measurement records.
- Added source-level `methodology` block for declaring measurement
  methods once per source rather than per-figure.

### Data populated at commit time

- 2 distilleries: Harris (confidence: medium), Bruichladdich (high)
- 4 production lines: 3 Bruichladdich (high), 1 Harris (medium)
- 10 bottlings: 9 Bruichladdich, 1 Harris (all OB releases)
- 3 concept pages: 1 methodology, 1 educational, 1 equipment
- 5 NOTES files documenting source conflicts and per-entry context

### Documentation added in this commit

- `README.md`
- `docs/handover.md` — design rationale and current state, written
  for future contributors (human or AI) picking up the project
- `docs/voice-register.md` — writing discipline rules
- `docs/source-conflict-policy.md` — how to handle disagreements
  between sources
- `docs/schema-design-notes.md` — why the schemas are shaped the way
  they are
- `docs/contributing.md` — stub for now

---

## Format for future entries

```
## [version] — YYYY-MM-DD

### Schema changes
- ...

### New entities
- (only summarised here if introducing a new entity type)

### Migration notes
- ...
```
