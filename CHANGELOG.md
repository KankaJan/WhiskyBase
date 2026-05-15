# Changelog

All notable schema changes are recorded here. Data additions (new
distilleries, lines, bottlings) are tracked through Git history, not
in this file.

The schemas use independent version numbers; a single project version
covers them all.

---

## [0.4.0] — 2026-05-15

Cross-reference graph completion (concept-page arc),
Wikipedia-volatility policy, first bottler entry and bottler v0.1
pressure-test. All previously-tracked concept dangling references
now resolve. The schema model is fully exercised: every entity
type referenced in the data has at least one populated entry, and
every IB discriminator field on the bottling schema has been
exercised against real bottler data.

### Schema versions at this entry

- `distillery.template.yml` v0.1
- `production_line.template.yml` v0.2.1
- `bottling.template.yml` v0.2
- `concept.template.yml` v0.1
- `bottler.template.yml` v0.1 (stub, pressure-tested; v0.2
  deferred pending Signatory IB case)
- `cask.template.yml` v0.1

### Schema changes

None at this entry. Bottler v0.2 promotion is deferred pending a
second IB case (Signatory Vintage is the expected trigger; its
formal sub-series structure will force the parent/child
relationship in the bottler series field). See SCHEMA-GAPS block
in `data/bottlings/cadenheads-bunnahabhain-stub.yml` for the five
observations that should feed into v0.2 when triggered.

### Policy and conventions

**Wikipedia-volatility policy** introduced in
`docs/source-conflict-policy.md`. Wikipedia is now treated as a
volatile source — entries change without notification, can be
subject to vandalism between revisions, and their citation graphs
evolve as editors come and go. Demoted from tier 2 to tier 3 in
the source reliability hierarchy with an explicit caveat. Primary
databases (PubChem, NIST WebBook, IUPAC, CFR, INAO regulatory
text) are recognised at tier 1 alongside producer structured
specs. Peer-reviewed journal papers are recognised at tier 2.

**New source-type vocabulary entries:**

- `chemistry_database` — primary chemistry database (PubChem,
  NIST WebBook, etc.). Used for compound-identity claims.
- `regulatory_text` — government or appellation-council
  regulatory publication (CFR, INAO *cahier des charges*,
  Consejo Regulador del Vino de Jerez DO text, Italian DOC/DOCG
  ministerial publications).
- `peer_reviewed_paper` — reserved for future use as research-
  request items are resolved.

### Concept-page completion

The cross-reference resolver now reports zero dangling concept
references. Remaining dangling refs (22 total) are forward
references from `equipment/worm-tub` to distilleries not yet
populated (20) and from the IB pressure-test stub to Bunnahabhain
(2). All expected per handover §8.

**New concept pages this entry:**

- Methodology (2 new): `harris-published-ppm`,
  `scotch-whisky-published-ppm`.
- Educational (2 new): `aromatic-compounds-in-whisky` (substantial
  teaching page covering phenolic chemistry, fermentation
  aromatics, and wood-derived compounds), `copper-conversation`
  (sulphur-removal chemistry; established-vs-convention split).
- Equipment (1 new): `shell-and-tube-condenser` (contrast case
  for the worm-tub page).
- Glossary (9 new): `peating-block`, `phenol-ppm`, `phenol`,
  `cresol`, `guaiacol`, `standard-seven-phenols`,
  `sulphur-in-new-make`, `lyne-arm`, `classic-malts`. All
  chemistry glossary entries cite PubChem as primary source.

**Concept page count: 17** (3 methodology, 3 educational, 2
equipment, 9 glossary).

### Bottler IB pressure-test

**`data/bottlers/cadenheads.yml`** (new) — first real bottler
entry, exercises the bottler v0.1 stub schema. Confidence: medium.
Documents Wm Cadenhead Ltd: 1842 founding (with lineage hedged
pending primary historical source), J&A Mitchell ownership since
1972, four major series (Authentic Collection, Original
Collection, Small Batch, Closed Distillery Series).

**`data/bottlings/cadenheads-bunnahabhain-stub.yml`** (new) —
deliberate schema-pressure-test placeholder. Confidence: stub.
Exercises all four bottling v0.2 IB discriminator fields:
`produced_at_distillery: bunnahabhain` (forward ref),
`bottled_by: cadenheads` (resolves), `bottler_type:
independent_bottler` (enum), `bottler_series:
cadenheads/authentic-collection` (resolves via the bottler
entry's series block). All four resolve cleanly. The entry's
SCHEMA-GAPS block documents 5 observations for future bottler
v0.2 promotion.

### Source migrations

6 Wikipedia citations migrated this entry:

- `educational/aromatic-compounds-in-whisky` — 4 chemistry
  sources (Phenol, Guaiacol, Cresol, Vanillin) removed. The
  page's compound-identity claims are now sourced via its
  `educational.covers` linkage to glossary entries, each of
  which carries the canonical PubChem citation.
- `educational/copper-conversation` — DMS source migrated from
  Wikipedia to PubChem CID 1068.
- `data/casks/bourbon-barrel.yml` — Wikipedia "Bourbon_whiskey"
  migrated to ecfr.gov 27 CFR §5.143 under the new
  `regulatory_text` source type.

12 Wikipedia citations remain across 12 files, all tracked in
TODO Research Requests for future upgrades:

- 8 wine-cask appellation entries (pomerol, pauillac, sauternes,
  burgundy, rhone, ventoux, mourvedre, amarone) — INAO
  regulatory text pending.
- 2 sherry-butt entries (oloroso, fino) — Consejo Regulador del
  Vino de Jerez DO text pending.
- `harris.yml` and `bruichladdich.yml` — distillery historical
  sources; acceptable per the volatility caveat for historical
  facts.

### Tooling

**`skills/safe-bulk-writes/SKILL.md`** (new). Project-local
Claude skill codifying the rule learned in the cask-population
session: parallel Write batches of 5+ files have produced NUL-byte
padding and silent truncation; safer to write serially or in
batches of ≤4. Updated subsequently with a separate finding:
single Writes can also truncate large files (~11 KB threshold),
with a bash-mediated repair pattern documented.

**`scripts/check_references.py`** extended to recognise the
`data/casks/` directory and handle the context-sensitive `parent:`
field correctly (cask `related.parent` resolves as a cask slug;
distillery `ownership.parent` is a company-name string, not a
slug reference).

### Post-population correctness passes

Multiple critical-analysis passes during the session identified
and fixed:

- **Chemistry terminology** in `glossary/phenol.yml` — wrongly
  stated "Phenol is the simplest aromatic alcohol"; phenols are
  not aromatic alcohols (different IUPAC class). Corrected with
  explicit contrast paragraph.
- **Slavonian oak species attribution** in `amarone-wine-cask.yml`
  changed from `Quercus petraea` to "most likely Q. robur or
  Q. petraea — trade references typically do not specify
  species."
- **Speculative porosity claim** in `oloroso-sherry-butt.yml`
  reframed from project voice to attributed trade convention.
- **Ambiguous Frilli attribution** in
  `equipment/shell-and-tube-condenser.yml` — the manufacturer
  reference was attached to the still pair, not the condenser;
  clarified.
- **`wine-cask.yml` prior_contents.category** changed from
  `red_wine` to `null` to reflect catch-all usage (Classic
  Laddie includes Madeira / fortified casks).
- **Invented source type** `project_doc` removed from
  `undisclosed-cask.yml`.
- **TODO Wikipedia citation count** corrected from 9 → 12 after
  this session's migrations.
- **`cadenheads.yml` founding-history contradiction** — the
  Duncan/Cadenhead specific story was internally inconsistent
  with the ownership history block; description hedged to retain
  the consistently-cited 1842 founding date while flagging the
  pre-Cadenhead lineage as a research request.

### Documentation updates

- `docs/handover.md` — §10 populated counts and next priorities
  rewritten across multiple sub-passes; Signatory IB pressure-
  test is the new highest priority for bottler v0.2 promotion.
- `docs/source-conflict-policy.md` — Wikipedia-volatility caveat
  section, updated reliability hierarchy table, expanded
  source-type vocabulary.
- `TODO.md` — Research Requests section (Wikipedia sourcing
  upgrade backlog), multiple Recently Completed entries for each
  sub-pass.

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
  Roses, Jim Beam — predominantly Kentucky) from Tennessee
  whiskey (Jack Daniel's), noting that ex-Jack-Daniel's barrels
  enter the Scotch supply chain alongside bourbon despite the
  legal separation of the two categories.
- **Burgundy single-variety claim hedged** in
  `burgundy-wine-cask.yml` to acknowledge the Aligoté, Gamay, and
  minor-variety exceptions.
- **Sauternes geography corrected** in `sauternes-wine-cask.yml`:
  Sauternes is a separate AOC from Graves under the modern
  Bordeaux AOC structure, not "the Graves region of Bordeaux" as
  initially written.
- **Invented source type removed**: `undisclosed-cask.yml` had a
  source with `type: project_doc` pointing at `docs/handover.md`
  — not a value used elsewhere in the project. Removed; the
  design rationale lives in the description.
- **`wine-cask.yml` prior_contents.category** changed from
  `red_wine` to `null` to reflect actual usage: the slug is used
  as the catch-all where a vatting combines several different
  ex-wine cask sources (e.g. Bruichladdich Classic Laddie
  includes Madeira, Merlot, Syrah, Muscat, and sweet wine cases
  within a single bottling).

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

- Added `none` to the `peat_origin` enum for positive "no peat
  used" declarations (was previously expressed as `null` with a
  comment, which conflated "unknown" and "intentionally none").

### Data corrections

- **`basis_concept` slug form normalised across 19 references.**
  The bare-suffixed form `<slug>-methodology` (e.g.
  `bruichladdich-published-ppm-methodology`) is replaced with
  the kind-prefixed concept slug `methodology/<slug>`.
- **Port Charlotte Islay Barley 2014 `duration_years`** updated
  from 7 to 9 across all three cask entries. The "Aged 7 Years"
  label is the SWA youngest-cask convention; actual elapsed
  maturation is ≈9 years. The `age_statement` field still
  reflects the producer's published label. Resolution documented
  in `bruichladdich.NOTES.md`.
- **Source-type misclassifications** in three sources corrected.
- **`ancient` removed** from the Bruichladdich line description
  per the voice-register disallowed-words list.
- **Stale schema-header comments** on all 10 bottling files
  updated from v0.1 to v0.2.
- **`peat_origin: none`** applied to
  `bruichladdich-bruichladdich.yml` per the new enum.
- **Production line schema_version** bumped to 0.2.1 on all four
  production_line entries.

### Documentation corrections

- **`docs/handover.md`** Harris washback count resolution
  corrected from "Resolved to 8" to "Resolved to 5"; bottler
  schema acknowledged as drafted v0.1 stub; schema-version list
  updated.
- **`docs/source-conflict-policy.md`** same Harris washback fix.
- **`README.md`** entity-schemas row updated.
- **`TODO.md`** three previously-unacknowledged dangling
  references added.

### Tooling

- **`scripts/check_references.py`** (new). Cross-reference
  resolver. Walks every YAML under `/data/`, builds the slug
  index across all entity types, and reports YAML parse
  failures, duplicate IDs, dangling cross-references, invalid
  source_id references, and inline `[N]` citations that don't
  match the entry's declared sources. Warn-only per handover §8.

### Project conventions

- **`skills/voice-register/SKILL.md`** (new). Project-local
  Claude skill encoding the voice register rules from
  `docs/voice-register.md`. Loads on demand when prose is being
  authored or edited for any entry.

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

- Renamed `distillery` field to `produced_at_distillery` for
  clarity when independent bottlings are introduced. Migrates
  all 10 existing bottlings.
- Added `bottled_by` (REQUIRED). For OB releases, references the
  same slug as `produced_at_distillery`. For IB releases (none
  yet populated), references a slug under `/data/bottlers/`.
- Added `bottler_type` (REQUIRED). One of `distillery |
  independent_bottler`.
- Added `bottler_series` (OPTIONAL). Series slug namespaced
  under the bottler.

**`production_line.template.yml` v0.1 → v0.2** (in prior session,
but relevant for migration history)

- Replaced flat `peating_ppm` field with structured `peating`
  block supporting multi-stage, multi-method measurement records.
- Added source-level `methodology` block for declaring
  measurement methods once per source rather than per-figure.

### Data populated at commit time

- 2 distilleries: Harris, Bruichladdich
- 4 production lines: 3 Bruichladdich, 1 Harris
- 10 bottlings: 9 Bruichladdich, 1 Harris (all OB releases)
- 3 concept pages: 1 methodology, 1 educational, 1 equipment
- 5 NOTES files documenting source conflicts and per-entry
  context

### Documentation added in this commit

- `README.md`
- `docs/handover.md` — design rationale and current state
- `docs/voice-register.md` — writing discipline rules
- `docs/source-conflict-policy.md` — source disagreement handling
- `docs/schema-design-notes.md` — schema design rationale
- `docs/contributing.md` — stub

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
