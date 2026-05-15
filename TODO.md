# TODO

Active queue for the WhiskyBase project. Items roughly ordered by what
unblocks the most downstream work. Add new items at the bottom of the
relevant section.

---

## Schema work

### Drafted but not finalised

- **Bottler schema** (`schema/bottler.template.yml`) is a draft. Will
  need refinement once IB data starts arriving. The series modelling
  in particular is speculative and may need to change once we have a
  real case (likely Cadenhead's Authentic Collection or Signatory
  Cask Strength Collection).
- **Cask schema** (`schema/cask.template.yml`) is v0.1 with 16
  entries populated. Follow-ups:
  - **Enrich the low-confidence wine entries** (`bordeaux-wine-cask`,
    `rhone-wine-cask`, `ventoux-wine-cask`, `mourvedre-wine-cask`,
    `sweet-wine-cask`) once more bottlings cite these cask types or
    a relevant cooperage source surfaces. Current entries are usable
    but lean on Wikipedia and one or two trade-press references.
  - **Decide whether to split `bourbon-barrel`** into named-supplier
    variants (e.g. `heaven-hill-bourbon-barrel`,
    `buffalo-trace-bourbon-barrel`) once 5+ bottlings disclose
    specific bourbon source. Per-batch disclosure is appearing
    (Harris Hearach Batch 5 named Heaven Hill and Buffalo Trace
    proportions) but the generic slug remains sufficient for now.
  - **Extend the `wood_species` enum** with `slavonian_oak` when more
    Italian / Eastern European wine casks land. `mongolian_oak` and
    `japanese_oak` are already in the enum but unused.
  - **Per-cask `used_by` field** is currently null — should be
    computed at build time rather than authored. Schema reserves it.
  - **Sherry seasoning vs transport butts.** The schema describes
    modern seasoning practice but does not distinguish historical
    transport butts from seasoned butts at the entry level. Add a
    `sherry_history: transport | seasoned | mixed` field if/when a
    bottling materially turns on this distinction.

### Not yet drafted

- (None currently — every entity type referenced in data has at
  least a v0.1 schema and at least one populated entry. The bottler
  schema awaits a real IB case for v0.2 promotion; see above.)

### Refinements deferred

- **Maturation grouping.** When producers disclose aggregate
  proportions ("44% European oak across four named appellations")
  the current per-cask list with `proportion: null` is awkward.
  Defer until the third or fourth distillery forces a real pattern.
- **Re-cask vs finish boundary.** The schema currently has `finish`
  (single object) and `maturation` (list). Port Charlotte PMC:01
  (4y bourbon + 5y Pomerol) is clearly multi-stage maturation, not
  finishing. Octomore 8.2 (6y wine + 2y Amarone) is borderline.
  Document convention: `finish` reserved for terminal cask exposure
  <12 months; substantive secondary maturations use additional
  `maturation` entries. Documentation update only; no schema change.
- **Field-level provenance.** Currently sources are referenced
  via `[N]` notation inline in prose. There is no machine-readable
  way to attach a source ID to a structured field. Defer until a
  real need surfaces.
- **JSON Schema validation tooling.** Currently the only check is
  `yaml.safe_load()` parse-passes. JSON Schema generation from the
  YAML templates would catch typos and shape drift. Defer until the
  data set is large enough to justify the tooling investment —
  probably 5+ distilleries, 50+ bottlings.
- **Multiple warehouses per distillery.** Current distillery schema
  has a single `warehouse:` block. Should probably be a list.
  Bruichladdich uses warehouses at multiple Islay locations.
  Springbank and Bunnahabhain will likely force the change too.
- **RRP across markets.** Bottlings sometimes have RRP in GBP, USD,
  EUR depending on which market the source covered. The schema
  should accept multiple RRP entries (one per market) rather than
  forcing a single canonical figure. Defer until convenient.

---

## Concept pages to create

The previously-tracked dangling concept references are now all
resolved. The cross-reference resolver reports zero dangling
concept slugs (the remaining 20 dangling references are all
expected `used_at_distilleries` forward references from
`equipment/worm-tub` pointing at distilleries not yet populated).

New concept-page creation work is captured in the queue section
below; the highest-priority slot is currently held by the
research-requests work (see Research Requests section), since
sourcing-upgrade work is more load-bearing than authoring new
pages at this point.

### Concept pages to queue

These will be needed but are not currently blocking dangling
references:

- **`educational/cask-maturation-kinetics`** — a teaching-register
  page documenting what is scientifically established about whisky
  maturation in oak, distinguishing peer-reviewed findings from
  trade convention and from open research questions. Suggested
  structure:
  - **Established mechanisms** (cite peer-reviewed work): lignin
    pyrolysis products generated by charring; ellagitannin and
    lactone profiles by oak source (American Quercus alba vs.
    European Q. robur / Q. petraea); oxidative versus reductive
    ageing under different wood permeability and warehouse climate
    conditions; the chemistry of cask charring and toasting.
  - **Trade convention versus established science** (record the
    convention but mark its evidentiary status): the Spanish-oak
    porosity argument; cask-charge ratio effects on extraction
    rates; the "first-fill imparts more sherry character"
    formulation; sweet vs. dry wine cask residue carryover.
  - **Open or sparsely-researched questions**: kinetics of seasoned
    versus genuine transport sherry butts; residue migration from
    Sauternes and other sweet wine casks; the maturation effect of
    re-cask events (decanting partway through ageing).
  Source hierarchy should favour peer-reviewed journals (work by
  Mosedale and Puech on oak extractives; Conner et al. on flavour
  development; SWRI publications) over trade press. Once this page
  exists, several cask entries can tighten their language:
  currently `oloroso-sherry-butt.yml`, `fino-sherry-butt.yml`, and
  `virgin-oak.yml` soft-pedal kinetic claims because no canonical
  reference is cited; this page would let them cite `[N]` to a
  sourced summary rather than hedging in prose.
- `equipment/victorian-rake-and-plough-mash-tun` (Bruichladdich,
  Springbank, one or two others — small population, worth a page)
- `equipment/tall-narrow-neck-stills` (Bruichladdich, Glenmorangie,
  Old Pulteney; geometry/character relationship)
- `equipment/lomond-still` (rare equipment; Bruichladdich, Inchmurrin,
  historical Scapa)
- `practice/bottle-code-transparency` (Bruichladdich's per-batch
  disclosure mechanism)
- `practice/barley-provenance-traceability` (Bruichladdich's Islay
  Barley series, Springbank Local Barley, etc.)
- `practice/on-island-maturation-policy` (Bruichladdich, Kilchoman,
  Bunnahabhain)
- (Glossary entries previously listed here have all been written
  as of 2026-05-15. See Recently Completed.)

---

## Distillery-level TODOs

### Bruichladdich

- Wikidata QID lookup
- Verify 1929-1936 mothballing window against a primary historical
  source rather than secondary references
- Two yeast strains (Mauri/Kerry) — single-source claim needs
  corroboration
- Whiskybase IDs for several Bruichladdich line bottlings

### Harris

- (See `data/distilleries/harris.NOTES.md` from initial population)

---

## Bottling-level TODOs

- **Per-batch child entries.** Decide whether SKUs with documented
  per-batch variation (Bruichladdich Classic Laddie, Glenfarclas
  Family Casks, Springbank Local Barley, Octomore .1 across editions)
  should be split into parent + per-batch child entries, or kept as
  single SKU entries with batch variation noted. Defer until at least
  three such cases are in the data so the right pattern emerges from
  observation rather than guess.
- **Octomore series completion.** The current data has 8.1 / 8.2 /
  8.3 only. Extending to the rest of the series (1.x through 16.x
  as of 2026) is research time, not schema work.
- **Bottler series annotation.** Octomore 8.1/8.2/8.3 should
  probably all reference `bottler_series: bruichladdich/octomore-masterclass-08`
  once the bottler entry for Bruichladdich (as a distillery-bottler)
  is populated. Currently the `bottler_series` field is null on
  all entries.

---

## Research requests

Entries that currently cite Wikipedia (a volatile source per
`docs/source-conflict-policy.md`) or that have empty `sources:`
where they should have authoritative sources. Each needs a
research pass to locate and cite stronger primary sources.

### Compound-chemistry sources (PubChem upgrade)

(All items in this sub-section migrated on 2026-05-15. The
`educational/aromatic-compounds-in-whisky` page now relies on its
`educational.covers` linkage to glossary entries which carry the
canonical PubChem citations. The `educational/copper-conversation`
page now cites PubChem CID 1068 directly for DMS.)

### Appellation/AOC regulatory sources (INAO upgrade)

The wine-cask entries cite Wikipedia for appellation rules and
grape composition. The primary source is the INAO regulatory
text for each AOC (the *cahier des charges*); secondary is the
appellation council's technical publication. Affected:

- `data/casks/pomerol-wine-cask.yml`
- `data/casks/pauillac-wine-cask.yml`
- `data/casks/sauternes-wine-cask.yml`
- `data/casks/burgundy-wine-cask.yml`
- `data/casks/rhone-wine-cask.yml`
- `data/casks/ventoux-wine-cask.yml`
- `data/casks/mourvedre-wine-cask.yml` — grape-variety reference;
  could cite IPGRI / Vitis International Variety Catalogue rather
  than Wikipedia.
- `data/casks/amarone-wine-cask.yml` — DOCG regulatory text from
  the Italian Ministero delle politiche agricole rather than
  Wikipedia.

### Sherry DO sources (Consejo Regulador upgrade)

- `data/casks/oloroso-sherry-butt.yml` cites Wikipedia "Sherry"
  for oloroso style description and Jerez DO geography. The
  Consejo Regulador del Vino de Jerez publishes the DO's
  regulatory text; that is the primary source for the
  designation rules.
- `data/casks/fino-sherry-butt.yml` cites Wikipedia "Fino" for
  fino style description. Same Consejo Regulador as the primary;
  for the flor-yeast microbiology, a published paper would be
  more authoritative than Wikipedia.

### Distilled-spirits regulatory sources (CFR upgrade)

(Migrated on 2026-05-15. `data/casks/bourbon-barrel.yml` now cites
ecfr.gov directly for 27 CFR §5.143 under the new `regulatory_text`
source type.)

### Distillery historical sources

- **`data/distilleries/harris.yml`** cites Wikipedia for opening
  date, production start, and grant funding details. Acceptable
  per the volatility caveat for historical facts; consider
  upgrading to the Highlands and Islands Enterprise grant
  publication for the funding detail specifically.
- **`data/distilleries/bruichladdich.yml`** cites Wikipedia for
  several historical claims about ownership lineage and
  mothballing windows. Same volatility-caveat acceptability;
  consider upgrading the 1929-1936 mothballing window claim in
  particular (currently marked TODO inline) to a primary
  historical source.

### Empty sources — need primary literature

These entries have `sources: []` and would benefit from primary
literature:

- **`data/concepts/glossary/standard-seven-phenols.yml`** — SWRI
  publications or malting industry technical literature for the
  "standard 7" convention's origin and codification.
- **`data/concepts/glossary/lyne-arm.yml`** — Scotch Whisky
  Association technical publications or distilling industry
  textbooks (e.g. Russell's "Whisky: Technology, Production and
  Marketing") for the lyne-arm geometry's effect.
- **`data/concepts/glossary/classic-malts.yml`** — Diageo's own
  archival materials for the portfolio's launch in 1988 and its
  subsequent expansions; independent historical retrospectives
  (Jackson, Murray's annual guides) for corroboration.
- **`data/casks/virgin-oak.yml`** — cooperage technical
  publications (Speyside Cooperage, Tonnellerie Taransaud); SWRI
  papers on new-oak extraction kinetics.
- **`data/casks/wine-cask.yml`** — no external source needed
  (project-internal generic category), but the description's
  claims about typical configuration could be sourced if needed.

### Why this section exists

The project's policy is "every claim is sourced." Wikipedia
citations were used as starting points during initial population
but the volatility-caveat policy (introduced 2026-05-15) prefers
primary sources where they're available and accessible. Migration
is a research-time task rather than a authoring-time task; this
section is the active backlog.

---

## Process

- **Validate every entry against schema before commit.** Once JSON
  Schema tooling is in place, this should be a CI step. Until then,
  the YAML parseability check is the minimum safety net.
- **Build pipeline.** Astro + Pagefind + MapLibre + CC-BY-SA data
  layer, MIT code layer. Deferred until enough data exists to
  justify the work.

---

## Recently completed

(Move items here when done, with the date and a one-line note. Trim
to the most recent five entries; older completions are tracked in
Git history.)

- **2026-05-15** Bottler IB pressure-test completed against
  Cadenhead's Authentic Collection. Created
  `data/bottlers/cadenheads.yml` (first real bottler entry,
  exercises the bottler v0.1 stub schema) and
  `data/bottlings/cadenheads-bunnahabhain-stub.yml` (schema-
  pressure-test placeholder, marked `confidence: stub`,
  exercises all four IB discriminator fields:
  `produced_at_distillery`, `bottled_by`, `bottler_type`,
  `bottler_series`). All four resolve cleanly. The bottling
  entry's SCHEMA-GAPS block documents 5 observations that would
  feed into bottler v0.2 promotion when triggered: sub-series
  support (deferred until Signatory case forces it),
  presentation-defaults on series (useful enhancement),
  production_line forward refs for unpopulated distilleries
  (acceptable per §8), resolver script gap on series-ID
  validation, and bottler-distillery corporate affiliation
  semantics (deferred).
- **2026-05-15** Easy Research Request migrations applied:
  `aromatic-compounds-in-whisky` (4 WP chemistry sources removed
  — glossary entries carry canonical citations);
  `copper-conversation` (WP DMS → PubChem CID 1068);
  `bourbon-barrel` (WP Bourbon_whiskey → ecfr.gov 27 CFR §5.143
  under new `regulatory_text` source type). Source-type
  vocabulary extended with `regulatory_text`. Net effect: 6
  Wikipedia citations eliminated from data; 12 files still
  carry Wikipedia citations (8 wine-cask appellation entries,
  2 sherry-butt entries, harris.yml, bruichladdich.yml — all
  tracked in Research Requests for future appellation /
  historical / sherry upgrades).
- **2026-05-15** Glossary backlog cleared. Wrote
  `glossary/phenol`, `glossary/cresol`, `glossary/guaiacol`,
  `glossary/standard-seven-phenols`, `glossary/sulphur-in-new-make`,
  `glossary/lyne-arm`, `glossary/classic-malts`. With these in
  place, the cross-reference resolver reports zero dangling
  concept references; the only remaining dangling refs are the
  20 distillery forward-references from `equipment/worm-tub`,
  which are expected per handover §8. Concept count: 17 (3
  educational, 2 equipment, 9 glossary, 3 methodology). Also
  introduced the project's Wikipedia-volatility policy in
  `docs/source-conflict-policy.md` and added a new source-type
  vocabulary entry `chemistry_database` for PubChem citations;
  populated a Research Requests section in TODO for entries that
  need a sourcing upgrade from Wikipedia to primary sources.
- **2026-05-15** Five concept pages written, closing the previous
  highest-priority list: `educational/aromatic-compounds-in-whisky`
  (substantial teaching page covering phenolic chemistry,
  fermentation aromatics, and wood-derived compounds);
  `equipment/shell-and-tube-condenser` (contrast case for the
  worm-tub page); `educational/copper-conversation` (sulphur-removal
  chemistry and the established-vs-convention split for character
  claims); `glossary/peating-block` and `glossary/phenol-ppm`
  (short glossary entries). 5 distinct dangling slugs resolved;
  6 new `covers:` references to as-yet-unwritten glossary entries
  introduced (the glossary backlog is now the project's main
  cleanup target).
- **2026-05-15** Methodology concept pages
  `methodology/harris-published-ppm` and
  `methodology/scotch-whisky-published-ppm` written. Resolves the
  last 3 dangling methodology references in existing data.
  Methodology concept count is now 3 (Bruichladdich, Harris, Scotch
  Whisky). Also added `safe-bulk-writes` skill at
  `/skills/safe-bulk-writes/SKILL.md` codifying the lesson from the
  cask-population NUL-bytes / truncation incident, and queued the
  `educational/cask-maturation-kinetics` page in the
  concept-pages-to-queue section.
- **2026-05-15** Cask schema v0.1 + 16 entries populated. All cask
  cross-references now resolve. Disclosure_status enum (with
  undisclosed-cask as a first-class entry) lands. Project v0.3.0.
- **2026-05-13** Audit-driven correctness pass and first reusable
  patterns: basis_concept slug normalisation (19 refs), PC Islay
  Barley 2014 SWA labelling-convention resolution, peat_origin enum
  extension, 10 bottling schema-header bumps, handover/README
  bottler-draft acknowledgment, `scripts/check_references.py`,
  `skills/voice-register/SKILL.md`. Project v0.2.1.
- **2026-05-13** Initial repository commit. Schema, 2 distilleries, 4
  production lines, 10 bottlings (migrated to v0.2), 3 concept pages,
  bottler schema stub, docs (handover, voice register, source
  conflict policy, schema design notes, contributing).
