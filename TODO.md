# TODO

Active queue for the WhiskyBase project. Items roughly ordered by what
unblocks the most downstream work. Add new items at the bottom of the
relevant section.

---

## Schema work

### Drafted but not finalised

- **Bottler schema** (`schema/bottler.template.yml`) is v0.2 with
  2 entries populated (Cadenhead's, Signatory Vintage). The v0.1 →
  v0.2 promotion (2026-05-15) added optional `parent:` and
  `presentation_defaults:` fields on the series shape, data-driven
  from the Signatory pressure-test. Schema is mature for current
  scope. Follow-ups:
  - First non-stub IB bottling release to replace one of the
    schema-pressure-test stubs (`cadenheads-bunnahabhain-stub`,
    `signatory-caol-ila-stub`) with verifiable real release data.
  - Signatory founding-circumstances research (Research Requests).
  - Resolver script extension to validate the series-id part of
    `bottler_series` references (currently only validates the
    bottler-slug part).
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
- **Multiple warehouses per distillery** — RESOLVED 2026-05-15.
  Distillery schema v0.2 changed `warehouse:` single block to
  `warehouses:` list, data-driven from the Springbank pressure-test.
  See Recently Completed.
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
is a research-time task rather than an authoring-time task; this
section is the active backlog.

---

## Cross-cutting research

These are not file-specific source upgrades (those are in Research
Requests above). They are broader research tasks that would
strengthen the project's overall coverage. Source priority for all
four: in-depth technical / historical / peer-reviewed literature
rather than popular guides — see the "Existing literature
catalogue" item.

### Yeast strains and fermentation regimes

Yeast disclosure is sparse across the populated production lines.
Most entries currently have `yeast: null` (Bruichladdich's three
lines, Harris, Springbank's three lines). Glenmorangie's main line
records `yeast: distillers` per the producer's standard claim.
Bruichladdich has a single-source claim for Mauri / Kerry strains
not yet corroborated (also in Bruichladdich-specific TODOs).

Task: systematically gather published yeast-strain information
across distilleries; identify whether a glossary or educational
concept on yeast types (distiller's yeast vs brewer's yeast vs
wild yeast as in Glenmorangie Allta vs Saccharomyces species more
generally) is worth adding. Source priority: SWRI publications,
peer-reviewed journal papers on yeast metabolism in Scotch
fermentation. NOT popular trade press.

### Barley varieties and maltster sourcing

Current populated coverage shows the same handful of varieties
recurring (Concerto across 5 lines; Optic across 4-5; Bere and
Propino in specific releases; Publican and Chalice in one or two
lines). Bairds of Inverness is named as the maltster for Harris
and Bruichladdich; other distilleries don't consistently disclose
the maltster.

Task: verify maltster sourcing per distillery (commercial vs
in-house); consider adding barley varieties as glossary entries
(`glossary/concerto`, `glossary/optic`, `glossary/bere`,
`glossary/propino`); consider a `practice/external-malting`
concept (Bairds is referenced from multiple distilleries, would
warrant its own page). Source priority: agronomic literature,
HGCA / AHDB barley variety reports, maltster technical
publications. NOT producer marketing copy.

### Undocumented technical concepts

A check-pass for whisky-domain technical terms that appear in
prose fields across the data but are not yet captured as glossary
entries. Candidates noticed during current population work:

- Distillation: foreshots, heart cut, feints, low wines, new
  make, spirit safe, swan neck, reflux
- Fermentation: wort, wash, lautering, sparging
- Maturation: reductive vs oxidative maturation, angel's share,
  cask-charge ratio
- Equipment-state distinctions: direct fire vs indirect steam
  heating
- Regional: Highland, Lowland, Speyside, Islay, Campbeltown,
  Islands designations (the SWA classification scheme; currently
  in distillery `region:` fields without concept backing)

Task: grep all populated prose fields for these and similar
terms; prioritise glossary entries for terms referenced from 3+
entries; defer terms appearing once. The SWA regional
classification is a good candidate for `concept/practice/swa-
regional-designations` since it's referenced from every
distillery entry's `region:` field.

### Existing literature catalogue

The project would benefit from a curated bibliography of in-depth
references for cross-referencing prose claims. Priority candidates
(NOT popular guides; in-depth technical, historical, or
peer-reviewed):

- **Russell, I. (ed.) "Whisky: Technology, Production and
  Marketing"** (Academic Press). Standard technical reference
  covering malting, brewing, distillation, maturation, analysis.
- **Buxton, I. & Hughes, P. "The Science and Commerce of Whisky"**
  (RSC Publishing).
- **MacLean, C.** analytical works ("Scotch Whisky: A Liquid
  History" for historical context).
- **The Malt Whisky Yearbook** series — annual industry
  statistics, production figures, capacity tables.
- Industry / academic journals:
  - *Journal of the Institute of Brewing*
  - *Food Chemistry*
  - *Journal of Agricultural and Food Chemistry*
  - *Journal of Cereal Science*
- **SWRI publications** (Scotch Whisky Research Institute) — both
  peer-reviewed papers and industry-trade reports.
- **Mosedale, J. R. & Puech, J.-L.** papers on oak extractives.
- **Conner, J. M.** on whisky flavour chemistry.

Task: build a `docs/bibliography.md` or
`data/sources/literature.yml` catalogue. Exclude popular books /
consumer guides. Goal is a citable reference set for the
educational pages, methodology concept pages, and the planned
`educational/cask-maturation-kinetics` page — all of which
currently soft-pedal claims that could be sourced to in-depth
literature.

---

## Process

- **Validate every entry against schema before commit.** Once JSON
  Schema tooling is in place, this should be a CI step. Until then,
  the YAML parseability check (run via `scripts/check_references.py`)
  is the minimum safety net.
- **JSON Schema validation tooling** — deferred per project
  thresholds ("5+ distilleries, 50+ bottlings" per current
  guideline). With Glenmorangie populated and Lagavulin planned
  next, the 5-distillery threshold will be reached; bottlings
  remain well below the 50-bottling threshold (currently 18).
  Evaluate after Lagavulin lands.
- **Build pipeline.** Astro + Pagefind + MapLibre + CC-BY-SA data
  layer, MIT code layer. Deferred until enough data exists to
  justify the work.

---

## Recently completed

(Move items here when done, with the date and a one-line note. Trim
to the most recent five entries; older completions are tracked in
Git history.)

- **2026-05-16** JSON Schema validation tooling landed. Hand-authored
  draft-07 schemas in `/schema/json/` for all six entity types,
  wired into `scripts/check_references.py` as a warn-only pass. The
  new pass surfaced ten silently-truncated files from earlier
  sessions (5 cask entries, 5 concept entries) — all restored from
  last committed version. Distillery `mothballed_periods` item shape
  canonised on `from`/`to`/`note` matching the ownership.history
  convention; Bruichladdich's two `start`/`end` entries migrated.
  Schema permissiveness gaps surfaced and patched: integer years,
  integer/string IDs, string schema_version (`0.2.1`), nullable
  equipment_changes.year, YYYY-MM string for rrp.as_of and
  notes_independent.date. Project v0.7.0.
- **2026-05-15** Fifth distillery (Lagavulin) populated. Heavily
  peated Islay distillery; Diageo-owned. Single production line
  (lagavulin) with malt sourced from Port Ellen Maltings at ~35
  ppm spec; methodology assigned to
  `methodology/scotch-whisky-published-ppm` since Lagavulin
  doesn't separately attribute the measurement. Pear-shaped
  stills, slow distillation, coastal dunnage maturation at
  Lagavulin Bay. Three representative bottlings: Lagavulin 16
  (flagship; resolves `glossary/classic-malts` as one of the six
  originals via prose-level markdown link), Distillers Edition
  (PX-finished, annual recurring — exercises bottling.finish
  block plus a SCHEMA-OBSERVATION about cross-distillery Diageo
  series), 12 Year Old Cask Strength (Special Releases — CS +
  NCF + natural colour combo). With this fifth distillery, the
  project crosses the TODO-deferred threshold for JSON Schema
  validation tooling ("5+ distilleries, 50+ bottlings"); the
  bottlings threshold (21 vs 50) is not yet crossed but the
  distillery threshold is, making JSON Schema validation a
  defensible next move. Pure data addition with no schema change
  — distillery v0.2's multi-warehouse list (single-element for
  Lagavulin) was already established by the Springbank work.
- **2026-05-15** Fourth distillery (Glenmorangie) populated.
  Highland-region single-line operation; pure data addition with
  no schema change (Springbank's earlier multi-warehouse pressure-
  test already lifted distillery v0.2). First use of the
  `still.height_m` field as load-bearing data (5.14 m / 16'10"
  for Glenmorangie's tall stills). Signet and Allta flagged as
  candidate separate production_line entries in the distillery
  entry's SCHEMA-OBSERVATIONS block; deferred until usage
  justifies modelling them as distinct lines. Three representative
  bottlings populated: The Original 10 (40% ABV chill-filtered
  with caramel — different presentation tradition than the 46%
  NCF natural-colour core of Springbank/Bruichladdich/Harris),
  18 Year Old (15+3 ex-bourbon-then-partial-oloroso maturation —
  exercises the secondary-maturation-not-finish convention), and
  Quinta Ruban 14 (port-finished — exercises the bottling
  schema's `finish:` block). Total bottlings now 18 (16 OB + 2
  IB stubs).
- **2026-05-15** Third distillery (Springbank) populated, driving
  distillery schema v0.1 → v0.2 promotion. Springbank is structurally
  the most complex distillery in the data so far: three production
  lines (Springbank 2.5×, Longrow double, Hazelburn triple) sharing
  one set of equipment; multi-warehouse layout; floor-malted barley
  in-house; direct-fired wash still with worm-tub condensation paired
  with indirect-steam spirit stills using shell-and-tube. The v0.1
  pressure-test surfaced the warehouse-as-list gap (resolved in v0.2:
  `warehouse:` → `warehouses:` list shape, with Springbank's three
  distinct on-site / adjacent warehouses now properly represented).
  Existing distilleries (Harris, Bruichladdich) migrated to v0.2 with
  single-element warehouses lists preserving all prior fields.
  Bottlings: 3 representative Springbank-line entries (Springbank 10,
  Longrow Peated, Hazelburn 10), one per line, confidence medium.
  Project v0.6.0.
- **2026-05-15** Bottler schema v0.1 → v0.2 promotion. Signatory
  pressure-test confirmed the Cadenhead's SCHEMA-GAPS hypotheses
  with real data: series with consistent presentation rules
  (Signatory's CSC, UCF, 100 Proof) need a `presentation_defaults:`
  block on the series shape, and sub-series like the Decanter
  Collection need an OPTIONAL `parent:` field. Both added to
  bottler v0.2. `data/bottlers/signatory.yml` populated (confidence
  medium) using both new features. `data/bottlings/signatory-
  caol-ila-stub.yml` populated as schema-pressure-test placeholder.
  Cadenhead's entry bumped to schema_version 0.2 but does not use
  the new features (its series have less formal presentation
  enforcement). Project v0.5.0.
- **2026-05-15** Bottler IB pressure-test completed against
  Cadenhead's Authentic Collection. Created
  `data/bottlers/cadenheads.yml` and
  `data/bottlings/cadenheads-bunnahabhain-stub.yml`. All four IB
  discriminator fields resolve cleanly. SCHEMA-GAPS block in the
  bottling stub documents 5 observations that subsequently fed
  into bottler v0.2.
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
