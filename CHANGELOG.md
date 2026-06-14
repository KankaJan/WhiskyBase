# Changelog

All notable schema changes are recorded here. Data additions (new
distilleries, lines, bottlings) are tracked through Git history, not
in this file.

The schemas use independent version numbers; a single project version
covers them all.

---

## [0.8.6] — 2026-06-14

**Schema — `continuous` added to the production-line
`distillation.regime` enum.** The enum previously covered only batch
pot-still regimes (`double`, `triple`, `partial_triple`, `2.5x`,
`2.81x`, `other`). `continuous` is added for column / Coffey (patent)
still distillation, driven by the first grain-whisky distillery
(Cameronbridge). Additive and backward-compatible; production-line
`schema_version` stays 0.2.1 (no re-stamp). Template comment synced.

Grain distilleries also surfaced two structuring needs that are
deliberately deferred (recorded as SCHEMA-OBSERVATIONS in
`cameronbridge.NOTES.md`, per the project's pressure-test-then-structure
practice): a structured representation of column / Coffey stills (the
`stills` block is pot-still-shaped, so column stills are captured in
`stills.notes` prose for now), and a cereal / grain-bill field (the
`malt` block is barley-centric, so the wheat/maize majority is in
prose). Both will be structured when a second grain distillery confirms
the shape.

## [0.8.5] — 2026-06-14

**Schema — `wood` added to the distillery `washbacks.material` enum.**
`schema/json/distillery.schema.json` `washbacks.material` previously
listed only specific species (`oregon_pine`, `larch`, `douglas_fir`,
`scottish_larch`), `stainless_steel`, `corten_steel` and `other`. The
generic value `wood` — already valid for `mash_tun.material` — is now
also accepted for washbacks, so a source that states "wooden washbacks"
without naming the species can be recorded at genus level (Glenlivet is
the first such case, from the Diffords Guide source-migration). Additive
and backward-compatible: all existing entries still validate and the
distillery `schema_version` stays 0.2 (no re-stamp). The template comment
(`schema/distillery.template.yml`) is synced, also restoring the omitted
`scottish_larch` value.

## [0.8.4] — 2026-06-11

Audit remediation: tooling gate, schema migration, and consistency
fixes. Driven by `docs/audit-2026-06-11.md`.

**Tooling — `scripts/check_references.py` gains four capabilities
and a gating mode.** A `--strict` flag exits non-zero on hard
problems (YAML parse failures, duplicate IDs, JSON Schema
violations, bad `source_id` / inline `[N]` citations, *unexpected*
dangling references, and cross-file consistency contradictions);
default output stays warn-only. New: an expected-dangling allowlist
(`scripts/expected_dangling.txt`) that splits forward references
from genuine misses; a schema-version currency check (warns when a
file's `schema_version` differs from its entity's current
template); and cross-file consistency checks (hard contradiction
when a bottling's `produced_at_distillery` disagrees with its
production line's distillery; soft mirroring gaps for
distillery↔line and line↔bottling membership). The pre-commit hook
now runs `check_references.py --strict` as a second gate alongside
the `check_writes.py` hard-corruption gate, so schema drift can no
longer reach a commit. Added `scripts/test_checks.py` with unit
tests for both gate scripts.

**Schema — concept per-kind enforcement strengthened.**
`schema/json/concept.schema.json` previously required only that the
block matching `kind` be an object when present. It now enforces
the documented "exactly one per-kind block" rule fully: the
matching block is required, and the other four blocks must be null
if present. No data changed (all 85 concepts already satisfied
this).

**Data — Macallan migrated to current schema.** The Macallan
production line and three bottlings (Sherry Oak 12, Double Cask 12,
Triple Cask Matured 15) were authored against a pre-v0.2 flat field
shape while declaring v0.2 in metadata. They are migrated to the
structured v0.2 / v0.2.1 shape (`produced_at_distillery`,
`bottled_by`, `bottler_type`, `maturation[]`, structured
`malt`/`peating`/`fermentation`/`distillation` blocks). No facts
changed; former free-text fields are preserved in `description`.

**Data — `french-oak-cask` cask entry added** (virgin French oak),
resolving the only genuine dangling cask reference (from
`ardbeg-corryvreckan`). Cask count 17 → 18.

**Data — bottling slug renamed for consistency.**
`bruichladdich-islay-barley-2023` → `bruichladdich-islay-barley-2014`
(id + filename) to use the vintage year, matching its sibling
`bruichladdich-port-charlotte-islay-barley-2014`; the parent line's
`bottlings:` list updated.

**Docs — source-type vocabulary reconciled to one canonical list.**
The `source_type` enum in `schema/json/_common.schema.json` (12
values) is now declared canonical; `docs/source-conflict-policy.md`,
`CLAUDE.md`, and the distillery / production_line template comments
are aligned to it. A document-precedence order (JSON Schemas >
templates > policy docs > handover) is stated in `docs/handover.md`
§12. `CLAUDE.md` and `handover.md` verification sections updated to
describe the two-gate pre-commit model. Stale counts in
`handover.md` §1/§10 corrected (45 bottlings, 18 casks) and the
resolved stub-tombstone priority removed. Audit report saved at
`docs/audit-2026-06-11.md`.

---

## [0.8.3] — 2026-05-26

Diagram-style spec extended; cross-section diagrams re-authored in
a new register.

`docs/diagram-style.md` now defines **three** visual registers
(was two): the existing **sketch** register for external-assembly
schematics (pot still, production-chain flowchart, peating-
measurement matrix), the existing **strict** register for data
graphs (spirit cut, cask-maturation kinetics), and a new
**technical-schematic** register for cross-section diagrams (mash
tun, washback, worm tub, shell-and-tube condenser, Coffey-still
columns, spirit safe). The sketch register's displacement filter
smears interior strokes in cross-section views; the technical-
schematic register uses clean lines instead.

Within the technical-schematic register, the spec also documents
the **blueprint conventions** settled in the 2026-05-26 pilot:
`stroke="currentColor"` throughout (CSS variables do not resolve
reliably for stroke in all viewers); double-walled vessel outlines
with generic diagonal section hatching via SVG pattern + even-odd
fill; dashed annotation leaders (5 3 pattern, stroke 1.0) ending
in filled-circle dots at the part-end; short solid pipe-nozzle
stubs at every inlet and outlet (so leaders point at a visible
structural element); dashed hidden lines (3 2 pattern) for
occluded interior parts; explicit stroke-weight hierarchy; no
flow-direction arrowheads. Material-specific hatching, dimensions,
and scale bars remain forbidden.

The six cross-section SVGs in `data/diagrams/` are re-authored to
the new register and the six corresponding equipment concept-page
alt-texts updated.

No schema fields were added or changed — this is a docs + asset
change. The optional `diagrams:` field on `concept.template.yml`
v0.1 remains unchanged.

The `safe-bulk-writes` skill is updated with two new lessons from
the same session: the Write tool's single-write truncation
threshold is revised down to ~3 KB (from the previously documented
~10 KB); and the Edit tool's failure mode on multi-line block
replacements over existing data files is escalated from "rare" to
"common when growing a block by more than ~5 lines", with a
recovery pattern via `git show HEAD:<path>` and Python splice.

`CLAUDE.md` is extended with a new "Reducing wasted iteration"
section adapted from the karpathy-skills behavioural guidelines —
pre-write discipline (state assumptions, simplicity first,
surgical changes, goal-driven execution) complementing the
existing post-write iterative pattern.

### Schema versions at this entry

- `distillery.template.yml` v0.2
- `production_line.template.yml` v0.2.1
- `bottling.template.yml` v0.2
- `concept.template.yml` v0.1
- `bottler.template.yml` v0.2
- `cask.template.yml` v0.1
- `supplier.template.yml` v0.1

---

## [0.8.2] — 2026-05-22

The `concept` schema gained an optional `diagrams` field — a list
of `{file, alt, caption?, source_id?}` records attaching
deterministic SVG diagrams to a concept page. The field is
additive and optional, so it is a change within `concept.template.yml`
v0.1 rather than a version promotion; existing entries without
diagrams remain valid. `concept.template.yml` and
`schema/json/concept.schema.json` carry the field; the site loader
(`attachDiagramSvg`) inlines each SVG at build time and the
concept detail page renders a `<figure>` with caption and source
citation. Diagram files live in `data/diagrams/`; the authoring
spec is `docs/diagram-style.md`. No other schema changes.

### Schema versions at this entry

- `distillery.template.yml` v0.2
- `production_line.template.yml` v0.2.1
- `bottling.template.yml` v0.2
- `concept.template.yml` v0.1
- `bottler.template.yml` v0.2
- `cask.template.yml` v0.1
- `supplier.template.yml` v0.1

---

## [0.8.1] — 2026-05-21

Verification policy change: a pre-commit hard-corruption gate.
`scripts/check_writes.py` added — it scans text files for the
Windows <-> Linux mount-sync damage signatures (embedded NUL
bytes, silent truncation, YAML parse failure). The pre-commit
hook in `scripts/hooks/` runs it against the staged files and
**blocks the commit** on a finding; activate it per clone with
`git config core.hooksPath scripts/hooks`. This is the project's
first commit-blocking check — `check_references.py` remains
warn-only for soft findings (dangling references, schema
warnings). The gate immediately surfaced a pre-existing bug:
`README.md` had been committed truncated (in commit 7c212f2) and
is repaired here, with its stale "Current state" counts
refreshed at the same time. No schema changes.

### Schema versions at this entry

- `distillery.template.yml` v0.2
- `production_line.template.yml` v0.2.1
- `bottling.template.yml` v0.2
- `concept.template.yml` v0.1
- `bottler.template.yml` v0.2
- `cask.template.yml` v0.1
- `supplier.template.yml` v0.1

---

## [0.8.0] — 2026-05-16

New `supplier` entity type schema drafted at v0.1, registered with
the resolver and JSON Schema validator. Currently 0 populated
entries — schema is DRAFT until a real pressure-test case lands.
Plus appellation-citation migrations across 10 cask entries
(INAO / MIPAAF / Consejo Regulador del Vino de Jerez), the
chill-filtering and scotch-presentation-conventions educational
pages, and the bibliography expansion to 33 entries across 7
sections.

### Schema versions at this entry

- `distillery.template.yml` v0.2
- `production_line.template.yml` v0.2.1
- `bottling.template.yml` v0.2
- `concept.template.yml` v0.1
- `bottler.template.yml` v0.2
- `cask.template.yml` v0.1
- `supplier.template.yml` v0.1 (NEW, DRAFT)

### New entity type: supplier

Models commercial upstream third parties — maltsters, cooperage
sources (bourbon distilleries supplying ex-bourbon barrels),
yeast suppliers, barley breeders — that the project's existing
entity types either represent only via free-text mentions
(maltsters in production_line.malt.maltster as a string,
cooperage sources in cask description prose) or not at all
(yeast suppliers). The schema parallels `bottler` in shape:

- Top-level identity (id, name, also_known_as, website).
- `type` enum discriminator (maltster | cooperage_source |
  yeast_supplier | barley_breeder | other).
- Country/region + optional `sites:` list for multi-site
  operators (Bairds Malt with Inverness, Pencaitland, Witham).
- Ownership block matching the distillery/bottler pattern.
- `products:` list for principal product types / specification
  capabilities.
- `supplies_to:` list of distillery slugs (build-pipeline-
  computable from the inverse direction).

The schema is registered in `schema/json/supplier.schema.json`
(draft-07, additionalProperties: false, parallels bottler in
required-field rigour). The resolver
(`scripts/check_references.py`) adds `data/suppliers/` to the
scan path, `supplies_to` to the LIST_REFS cross-reference
targets, and `supplier` to the entity-schema validator dict.

**Status: DRAFT.** No entries populated. Schema awaits a real
pressure-test (likely Bairds Malt Ltd, which has the most
references in current data). Existing glossary entries
(bairds-malt, heaven-hill, buffalo-trace, distillers-yeast)
remain as short-tooltip references; supplier entries when
added provide the structured-fields layer alongside.

### Appellation regulatory migrations

10 cask entries migrated from Wikipedia-primary to
regulatory-text-primary sourcing for appellation rules:

- 7 INAO French AOCs: Pauillac, Pomerol, Sauternes, Burgundy
  framework, Rhône framework, Ventoux, Bandol (cited as
  Mourvèdre's principal French AOC home).
- 1 Italian DOCG via MIPAAF: Amarone della Valpolicella.
- 2 Consejo Regulador del Vino de Jerez DO entries: oloroso
  and fino sherry butts.

Each migration adds a `regulatory_text` source at id N+1 of
the entry's sources block; Wikipedia citations are preserved
per the project's policy on retaining rejected/secondary
sources for transparency. Specific cahier-des-charges /
disciplinare / reglamento URLs are unstable; entries cite
institutional homepages with explicit notes that specific
document URLs should be verified when accessed (follow-up
work).

### Educational pages added

- `educational/chill-filtering` — chill-haze chemistry (long-
  chain ethyl ester precipitation), the chill-filtering process
  (-4 to +4 °C through cellulose sheets), the 46% ABV
  producer-empirical threshold, and the contested
  mouthfeel-impact question. Sources: Russell 2014, Conner
  et al. 2003 (Worldwide Distilled Spirits Conf. proceedings),
  Conner et al. 1994, SWR 2009.
- `educational/scotch-presentation-conventions` — cluster page
  covering bottling strength, chill-filter vs NCF, natural
  colour vs caramel colouring, cask-strength claims. Maps the
  presentation-positioning matrix (industrial-core / premium
  core / craft transparency / cask-strength special). Sources:
  SWR 2009 reg 6/7, Russell ch. bottling.

### Bibliography expansion

`docs/bibliography.md` expanded from 388 to 767 lines via the
completeness audit. Now covers 33 entries across 7 sections:
technical reference books (Russell, Piggott 1989 and 1983,
Lyons & Hill, Boulton & Quain, Buxton & Hughes, Udo),
peer-reviewed paper groups (Mosedale & Puech, Conner,
Paterson/Piggott Strathclyde, Wanikawa Suntory, Aylott, SWRI
staff), academic journals (JIB, JSFA, Food Chemistry, JAFC,
J Cereal Sci, Trends in Food Sci & Tech, Food Res Intl, LWT,
Chem Senses, Flavour & Fragrance), institutional sources
(SWRI, ICBD, SWA, HMRC, Worshipful Company of Distillers),
annual publications, and historical / contextual works (MacLean,
Moss & Hume 1981, Weir on DCL).

### Counts at this entry

- 45 concept pages (8 educational, 30 glossary, 3 methodology,
  2 equipment, 2 practice)
- 16 cask entries (all with regulatory-text primary sourcing
  where applicable)
- 392 resolved cross-references, 0 JSON Schema findings.

---

## [0.7.0] — 2026-05-16

JSON Schema validation tooling added. Hand-authored draft-07 schemas
for all six entity types live in `/schema/json/`; the resolver in
`scripts/check_references.py` now runs validation as a warn-only pass
alongside the existing reference resolution. The threshold of 5+
distilleries (deferred since the cask-schema work) is crossed,
making the tooling investment defensible against the data set.

### Schema versions at this entry

- `distillery.template.yml` v0.2 (template change: mothballed_periods
  convention canonised to `from`/`to`/`note`, matching ownership.history)
- `production_line.template.yml` v0.2.1
- `bottling.template.yml` v0.2
- `concept.template.yml` v0.1
- `bottler.template.yml` v0.2
- `cask.template.yml` v0.1

### Additions

- `/schema/json/_common.schema.json` — shared definitions (slug, source,
  source_type enum, ABV, currency, year forms, schema_version forms,
  external_id values).
- `/schema/json/{distillery,production_line,bottling,bottler,cask,concept}.schema.json`
  — one per entity type. Draft-07. Cross-file `$ref` to `_common` is
  rewritten to in-document `#/definitions/...` at load time by the
  resolver script (jsonschema 3.2.0 cross-file `$ref` is brittle).
- `scripts/check_references.py` — adds JSON Schema validation pass.
  YAML dates (`datetime.date`) are coerced to ISO strings before
  validation. Findings are printed grouped by entity type, warn-only.

### Schema convention change

**Distillery `mothballed_periods` item shape**

The distillery template previously documented `{start: YYYY, end: YYYY}`
for mothballed period entries. Real data (Springbank, then audited
across the corpus) uses `{from: YYYY, to: YYYY, note: ...}` — matching
the `from`/`to` convention already in `ownership.history`. The
template has been updated to canonise `from`/`to`/`note`. The one
existing entry using `start`/`end` (Bruichladdich) has been migrated.

This is a convention change rather than a schema-shape change — both
forms parse as YAML; the JSON Schema validation now rejects `start`/`end`.
Distillery schema version stays at v0.2 because the on-disk template
shape is unchanged in field count or relationships.

### Resolver bug surfacing

The new JSON Schema validation pass surfaced ten silently-truncated
files left over from earlier sessions:

- 5 cask entries (`amarone-wine-cask`, `burgundy-wine-cask`,
  `fino-sherry-butt`, `oloroso-sherry-butt`, `sauternes-wine-cask`)
  missing their trailing `# --- Metadata` block (schema_version,
  confidence, last_reviewed, contributors).
- 5 concept entries (`copper-conversation`, `shell-and-tube-condenser`,
  `classic-malts`, `peating-block`, `sulphur-in-new-make`) similarly
  truncated.

All ten were restored from the last committed version on `master`.
The cross-reference resolver (YAML parse + index) was tolerant of
the truncations because YAML loaded the partial documents
successfully; only the JSON Schema required-field check caught the
missing metadata blocks. This is the load-bearing case for the
validation tooling and immediately justified the investment.

---

## [0.6.0] — 2026-05-15

Third distillery populated (Springbank), driving distillery schema
v0.1 → v0.2 promotion for multi-warehouse support. Schema model
remains fully exercised across all six entity types. Three
distilleries is the threshold for distillery-pattern observation
that the project has been working toward.

### Schema versions at this entry

- `distillery.template.yml` v0.2 (was v0.1)
- `production_line.template.yml` v0.2.1
- `bottling.template.yml` v0.2
- `concept.template.yml` v0.1
- `bottler.template.yml` v0.2
- `cask.template.yml` v0.1

### Schema changes

**`distillery.template.yml` v0.1 → v0.2**

Single change: `warehouse:` (single block) → `warehouses:` (list of
blocks). The list entries preserve the v0.1 fields (`type`,
`location`, `climate_notes`) and add an OPTIONAL `id:` for
distinguishing multiple warehouses within one entry.

Data-driven from the Springbank pressure-test: Springbank operates
multiple distinct warehouses on the Campbeltown site (dunnage +
racked) plus additional warehousing at the adjacent Glengyle site,
and the single-block `warehouse:` field could not capture this.
The gap was predicted in handover §10's deferred decisions and in
TODO; the Springbank case confirmed it with real data.

Migration: Harris and Bruichladdich both bumped to v0.2 with their
existing warehouse blocks wrapped in single-element lists,
preserving all previous fields.

### Data populated

- **`data/distilleries/springbank.yml`** (new). Third distillery in
  the project. Confidence: medium. Documents Springbank's distinctive
  configuration: 1828 founding with continuous Mitchell family
  ownership since 1837; floor maltings on site; direct-fired wash
  still with worm-tub condensation paired with indirect-steam
  spirit stills using shell-and-tube condensers; three production
  lines (Springbank, Longrow, Hazelburn) sharing equipment.
- **`data/production_lines/springbank-springbank.yml`** (new). 2.5×
  distillation, lightly peated (12-15 ppm spec).
- **`data/production_lines/springbank-longrow.yml`** (new). Double
  distillation, heavily peated (50-55 ppm spec). Revived 1973 from
  an earlier 19th-century Campbeltown distillery name.
- **`data/production_lines/springbank-hazelburn.yml`** (new). Triple
  distillation, unpeated (`peat_origin: none`). First distilled
  1997 from the earlier 19th-century Hazelburn name.
- **`data/bottlings/springbank-springbank-10.yml`** (new). Core 10
  Year Old, 46% NCF natural colour, batch-vatted.
- **`data/bottlings/springbank-longrow-peated.yml`** (new). Core
  Longrow Peated NAS, 46% NCF natural colour.
- **`data/bottlings/springbank-hazelburn-10.yml`** (new). Core
  Hazelburn 10 Year Old, 46% NCF natural colour.

All Springbank-line production lines use the new v0.2.1
`peat_origin: none` for Hazelburn and the existing `2.5x` enum
value for Springbank's distillation regime. The `floor_malted_onsite`
malt source value is in active use for the first time.

### Migrations applied

- **`data/distilleries/harris.yml`** schema_version bumped 0.1 →
  0.2. Single-element `warehouses:` list wrapping the prior
  warehouse block. Stale header comment "Schema:
  distillery.template.yml v0.1" updated.
- **`data/distilleries/bruichladdich.yml`** same: schema_version
  bump and warehouse-block wrapped in single-element list. Stale
  header comment updated.

### Post-population correctness pass

- **`glossary/phenol.yml`** repaired — file had been silently
  truncated mid-sources block during an earlier session; the inline
  citation `[1]` was therefore dangling per the
  check_references.py inline-citation check. Sources block
  restored (PubChem CID 996 citation).
- **`springbank.yml` factual hedges**: washback material changed
  from `boatskin_larch` to plain `larch` (the "boatskin" reference
  is a construction-method term, not a species — conflating the
  two was imprecise); mash tun cast-iron claim hedged with
  acknowledgement that primary-source corroboration would
  strengthen and an alternative interpretation can't be ruled out.

### Documentation updates

- `docs/handover.md` §10 schema versions list (distillery v0.2),
  populated counts (3 distilleries, 7 production lines, 15
  bottlings), next priorities (Springbank done; Research Requests
  audit now #1).
- `README.md` state table updated.
- `TODO.md` — "Multiple warehouses per distillery" item moved out
  of deferred refinements (RESOLVED 2026-05-15). Recently Completed
  entry added.

### Workflow note

Second consecutive v0.x schema bump driven by the iterative-
evaluation pattern codified in CLAUDE.md. Both bottler v0.2
(2026-05-15 earlier) and distillery v0.2 (this entry) followed
the same shape: write the new entry in the existing schema,
document the genuine failure points in a SCHEMA-GAPS block,
design v0.2 based on observation, apply, migrate existing data.
Data-driven schema design rather than speculative.

---

## [0.5.0] — 2026-05-15

Bottler schema v0.1 → v0.2 promotion driven by the Signatory IB
pressure-test. With this entry the schema model is fully exercised
across all six entity types — every schema has been pressure-tested
against real data.

### Schema versions at this entry

- `distillery.template.yml` v0.1
- `production_line.template.yml` v0.2.1
- `bottling.template.yml` v0.2
- `concept.template.yml` v0.1
- `bottler.template.yml` v0.2 (was v0.1 stub)
- `cask.template.yml` v0.1

### Schema changes

**`bottler.template.yml` v0.1 → v0.2**

The Signatory pressure-test confirmed two gaps identified
hypothetically in the Cadenhead's pressure-test (v0.4.0) and added
both fields to the series shape:

- **`parent: <series-id>`** (OPTIONAL). Used when a series is a
  presentation variant or sub-batch of another. Worked example:
  Signatory's Decanter Collection has
  `parent: cask-strength-collection` — the Decanter Collection
  is essentially CSC with different bottle packaging, not a
  wholly separate series.
- **`presentation_defaults:`** (OPTIONAL). Captures consistent
  presentation rules that apply to all bottlings under a series.
  Fields: `cask_strength`, `non_chill_filtered`, `natural_colour`,
  `batch_or_cask_type`, `abv`. Bottlings inherit these unless
  they explicitly override. Worked examples: Signatory's
  Un-Chillfiltered Collection has `presentation_defaults.abv: 46.0`
  and `cask_strength: false`, `non_chill_filtered: true`,
  `natural_colour: true`, `batch_or_cask_type: vatting`; Cask
  Strength Collection has `cask_strength: true`,
  `batch_or_cask_type: single_cask` (with ABV variable per cask).

Both features data-driven from Signatory's actual series structure
rather than speculation. Cadenhead's hypotheses (in the
cadenheads-bunnahabhain-stub SCHEMA-GAPS block) accurately
predicted these features; Signatory's data confirmed them and
provided concrete design parameters.

### Data populated

- **`data/bottlers/signatory.yml`** (new). Second real bottler
  entry. Confidence: medium. Uses both new v0.2 features actively:
  `presentation_defaults` on CSC, UCF, 100 Proof, and Decanter
  series; `parent: cask-strength-collection` on the Decanter
  Collection. Documents Wm Cadenhead Ltd's main competitor and the
  case that drove the v0.2 promotion.
- **`data/bottlings/signatory-caol-ila-stub.yml`** (new).
  Schema-pressure-test placeholder for a Signatory Cask Strength
  Collection release. Confidence: stub. Exercises all four
  bottling v0.2 IB discriminator fields against the Signatory
  bottler entry; the four `[v0.1 redundancy]` markers in the
  field comments document fields that v0.2 makes inheritable from
  the series presentation_defaults.

### Migrations applied

- **`data/bottlers/cadenheads.yml`** schema_version bumped 0.1 →
  0.2. Cadenhead's series do not have strong presentation-default
  enforcement; the v0.2 fields are available but not used in this
  entry. Stale header and series-block-preamble comments updated
  to reflect v0.2 in place.

### Documentation updates

- `docs/handover.md` §1 (intro — bottler now v0.2 with 2 entries),
  §10 (schema versions list, populated counts, next priorities
  rewritten — third distillery now #1).
- `README.md` (entity-schemas row, new "Bottlers populated" row in
  state table).
- `TODO.md` — bottler item moved out of "Drafted but not
  finalised" (now mature for current scope); Recently Completed
  entry added.

### Workflow note

This is the first v0.x schema promotion driven explicitly by the
iterative-evaluation pattern codified in CLAUDE.md: write the
Signatory entry in v0.1 first (the existing stub schema) to
surface what genuinely failed, *then* design and apply v0.2 based
on the actual gaps. The Cadenhead's SCHEMA-GAPS block had
hypothesised the design 2026-05-15 earlier in the session;
Signatory's data confirmed the hypotheses and refined the field
shapes. Data-driven schema design rather than speculative.

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
