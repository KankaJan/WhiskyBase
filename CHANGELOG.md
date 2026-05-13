# Changelog

All notable schema changes are recorded here. Data additions (new
distilleries, lines, bottlings) are tracked through Git history, not
in this file.

The schemas use independent version numbers; a single project version
covers them all.

---

## [0.2.1] — 2026-05-13

Audit-driven correctness pass and the first two reusable patterns
(cross-reference resolver script, voice-register skill).

### Schema versions at this entry

- `distillery.template.yml` v0.1
- `production_line.template.yml` v0.2.1
- `bottling.template.yml` v0.2
- `concept.template.yml` v0.1
- `bottler.template.yml` v0.1 (stub, no entries populated)

### Schema changes

**`production_line.template.yml` v0.2 → v0.2.1**

- Added `none` to the `peat_origin` enum. Previously the unpeated
  Bruichladdich line carried `peat_origin: null` with an inline
  "No peat used" comment, which conflated *unknown* with *intentionally
  none*. The new value records the design choice positively. Migrates
  `bruichladdich-bruichladdich.yml`.
- Documented the `basis_concept` value form as kind-prefixed
  `methodology/<slug>` (matching the existing `related_concepts`
  convention on concept entries).

### Data corrections

- **`basis_concept` slug form normalised across 19 references.** The
  bare-suffixed form `<slug>-methodology` (e.g.
  `bruichladdich-published-ppm-methodology`) is replaced with the
  kind-prefixed concept slug `methodology/<slug>`. All Bruichladdich
  (16), Harris (2), and Scotch Whisky (1) methodology references
  now resolve to real concept slugs.
- **Port Charlotte Islay Barley 2014 `duration_years`.** Updated from
  7 to 9 across all three cask entries. The "Aged 7 Years" label is
  the SWA youngest-cask convention; actual elapsed maturation is
  ~9 years (distilled 2014, bottled 26 July 2023). The `age_statement`
  field still reflects the producer's published label. Resolution
  documented in `bruichladdich.NOTES.md`.
- **Source-type misclassifications.** Three sources retagged:
  `bruichladdich.com` URLs in `bruichladdich.yml` (source 5) and
  `bruichladdich-octomore-8-1.yml` (source 4) corrected from
  `trade_publication` to `official_website`;
  `en.beveragehunters.com` in `harris.yml` (source 9) corrected from
  `official_website` to `trade_publication`.
- **Bruichladdich line description.** Removed `ancient` (per the
  voice-register disallowed-words list) — replaced with `heritage`.
- **Stale schema header comments** on all 10 bottling files updated
  from `# Schema: bottling.template.yml v0.1` to `v0.2`, aligning the
  header comment with the `schema_version: 0.2` declared at the bottom
  of each file.
- **`peat_origin: none`** applied to `bruichladdich-bruichladdich.yml`
  per the new enum.
- **Production line schema_version** bumped to `0.2.1` on all four
  production_line entries.

### Documentation corrections

- **`docs/handover.md`.** Harris washback count resolution corrected
  from "Resolved to 8" to "Resolved to 5" (matching `harris.yml` and
  `harris.NOTES.md`); bottler schema acknowledged as drafted v0.1
  stub in §1, §7, and §10; schema-version list in §10 updated to
  reflect production_line v0.2.1 and bottler v0.1 stub; next-priorities
  list reframed from "draft bottler schema" to "pressure-test the
  v0.1 stub against a real IB case".
- **`docs/source-conflict-policy.md`.** Same Harris washback fix as
  above (the doc carried the same outdated resolution).
- **`README.md`.** Entity-schemas row updated.
- **`TODO.md`.** Three previously-unacknowledged dangling references
  added to the concept-pages-to-create queue: `glossary/peating-block`,
  `glossary/phenol-ppm`, `educational/copper-conversation`.

### Tooling

- **`scripts/check_references.py`** (new). Cross-reference resolver.
  Walks every YAML under `/data/`, builds the slug index across all
  entity types, and reports: YAML parse failures, duplicate IDs,
  dangling cross-references (grouped by target type), invalid
  structured `source_id:` references, and inline `[N]` source
  citations that don't match the entry's declared `sources:`. Warn-
  only per handover §8.

### Project conventions

- **`skills/voice-register/SKILL.md`** (new). Project-local Claude
  skill encoding the voice register rules from `docs/voice-register.md`.
  Loads on demand when prose is being authored or edited for any
  entry. The canonical rules still live in `docs/voice-register.md`;
  the skill is a fast-reference mirror. Skills are kept under
  `/skills/` at the repository root so collaborators can symlink or
  install them into their local Claude skills folder.

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
