# Changelog

All notable schema changes are recorded here. Data additions (new
distilleries, lines, bottlings) are tracked through Git history, not
in this file.

The schemas use independent version numbers; a single project version
covers them all.

---

## [0.3.0] — 2026-05-15

Cask schema and population. The schema model now covers every entity
type referenced in existing data; the cross-reference resolver reports
zero dangling cask references (was 16 distinct cask slugs in v0.2.1).

### Schema versions at this entry

- `distillery.template.yml` v0.1
- `production_line.template.yml` v0.2.1
- `bottling.template.yml` v0.2
- `concept.template.yml` v0.1
- `bottler.template.yml` v0.1 (stub, no entries populated)
- `cask.template.yml` v0.1 (new — 16 entries populated)

### Schema additions

**`cask.template.yml` v0.1 (new)**

A new top-level entity type, parallel to distillery / production_line /
bottling / bottler. Cask slugs are referenced from
`bottling.maturation[*].cask_type`, `bottling.finish.cask_type`, and
`production_line.typical_cask_program`.

The schema's load-bearing design decision is the `disclosure_status`
enum (`disclosed | partially_disclosed | undisclosed | unknown`):
`undisclosed` is a positive declaration about producer secrecy (the
Bruichladdich Black Art series is the canonical case), distinct from
`unknown` which records missing-data-may-be-discoverable. The two are
queryable as distinct categories. The first-class `undisclosed-cask`
entry exists to make this explicit at the slug level — producer-secret
information is information, not absence.

Cask slugs are bare (not kind-prefixed), matching the convention for
other top-level entity types. The previously-aspirational
`cask/<type>` namespace mentioned in handover §6 is rejected in favour
of the convention already used throughout the data
(`cask_type: bourbon-barrel`).

Schema fields: identity (id, name, aliases); classification (category,
subcategory); vessel characteristics (typical_volume_litres,
wood_species); prior_contents (category + free-text specifics); origin
(country, region, appellation, producer); disclosure_status with
optional disclosure_notes; description (strict reference register);
related (parent slug, alternatives list); sources.

### Data populated

16 cask entries created under `/data/casks/`, covering all 16
previously-dangling cask slugs reported by the cross-reference
resolver:

- **High confidence (5)**: `bourbon-barrel`, `oloroso-sherry-butt`,
  `fino-sherry-butt`, `virgin-oak`, `undisclosed-cask`.
- **Medium confidence (6)**: `wine-cask` (parent); named wine
  appellations `pomerol-wine-cask`, `pauillac-wine-cask`,
  `sauternes-wine-cask`, `amarone-wine-cask`, `burgundy-wine-cask`.
- **Low confidence (5)**: `bordeaux-wine-cask` (generic Bordeaux),
  `rhone-wine-cask` (generic Rhône), `ventoux-wine-cask`,
  `mourvedre-wine-cask` (variety rather than appellation),
  `sweet-wine-cask` (generic).

### Documentation updates

- **`docs/handover.md` §1 intro**: cask added as the fifth top-level
  entity type alongside bottler.
- **`docs/handover.md` §6 slug conventions**: cask slug form
  specified as bare (matching other top-level entity types); concept
  reference forms clarified (structured `<kind>/<slug>` vs URL-form
  `concept/<kind>/<slug>`); bottler slug form added.
- **`docs/handover.md` §10**: cask schema entry added to schema-list,
  cask counts added to populated-data summary, next-priorities list
  updated (cask schema item removed as resolved).
- **`README.md`**: entities table extended with cask row; entity-
  schemas row updated; casks-populated row added to state table.
- **`TODO.md`**: cask schema item moved from "Not yet drafted" to
  "Drafted but not finalised" with follow-up items.

### Tooling

- **`scripts/check_references.py`** extended to recognise the new
  `casks/` directory under `/data/` and to handle the context-
  sensitive `parent:` field correctly: cask `related.parent`
  resolves as a cask slug, while distillery `ownership.parent` is a
  company name string and is no longer false-flagged as a dangling
  cask reference.

### Post-population correctness pass

A critical-analysis pass over the 16 cask entries identified and
fixed several issues introduced in initial drafting:

- **3 hallucinated source URLs removed.** `bourbon-barrel.yml`,
  `oloroso-sherry-butt.yml`, and `virgin-oak.yml` cited
  `scotchwhisky.com/whiskypedia/<NUM>/<slug>/` URLs whose specific
  numeric IDs were not verified — only the URL pattern was
  authentic (e.g. `/1827/bruichladdich/` exists and is correctly
  cited elsewhere). Removed. The Wikipedia citations on the same
  entries are retained as the sole external reference; virgin-oak
  drops to `confidence: medium` with sources empty pending a
  reliable cooperage publication.
- **11 source-type misclassifications corrected.** Wikipedia URLs
  were tagged `trade_publication` in 11 cask entries; corrected to
  `type: wikipedia` to match the project convention (cf. existing
  `harris.yml` source 3 as the worked example).
- **Wood-species binomials hedged** where attribution is contested:
  `amarone-wine-cask.yml` Slavonian oak changed from
  `(Quercus petraea)` to `(most likely Quercus robur or
  Q. petraea)`; `oloroso-sherry-butt.yml` and `fino-sherry-butt.yml`
  similarly hedge "Spanish oak" species attribution.
- **Speculative claims reframed.** The Spanish-oak-porosity claim
  in `oloroso-sherry-butt.yml` and the drier-and-more-saline claim
  in `fino-sherry-butt.yml` were stated in project voice; both
  reattributed to trade convention or removed.
- **Factual framing**: `bourbon-barrel.yml` description and origin
  block now distinguish bourbon (Heaven Hill, Buffalo Trace, Four
  Roses, Jim Beam — predominantly Kentucky) from Tennessee whiskey
  (Jack Daniel's), noting that ex-Jack-Daniel's barrels enter the
  Scotch supply chain alongside bourbon despite the legal
  separation of the two categories.
- **Burgundy single-variety claim hedged** in `burgundy-wine-cask.yml`
  to acknowledge the Aligoté, Gamay, and minor-variety exceptions.
- **Sauternes geography corrected** in `sauternes-wine-cask.yml`:
  Sauternes is a separate AOC from Graves under the modern Bordeaux
  AOC structure, not "the Graves region of Bordeaux" as initially
  written.
- **Invented source type removed**: `undisclosed-cask.yml` had a
  source with `type: project_doc` pointing at `docs/handover.md` —
  not a value used elsewhere in the project. Removed; the design
  rationale lives in the description.
- **`wine-cask.yml` prior_contents.category** changed from
  `red_wine` to `null` to reflect actual usage: the slug is used as
  the catch-all where a vatting combines several different ex-wine
  cask sources (e.g. Bruichladdich Classic Laddie includes Madeira,
  Merlot, Syrah, Muscat, and sweet wine cases within a single
  bottling).

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
