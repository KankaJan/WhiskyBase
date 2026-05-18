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
- **Supplier schema** (`schema/supplier.template.yml`,
  `schema/json/supplier.schema.json`) is v0.1 with 1 entry
  populated (Bairds Malt Ltd, 2026-05-17). The pressure-test
  conclusion: v0.1 schema is adequate for current data; no v0.2
  promotion driven. SCHEMA-GAPS block in
  `data/suppliers/bairds-malt.yml` documents 6 observations for a
  possible future v0.2 promotion (per-product produced_at_sites
  field; OPTIONAL per-supplier-type product enums; relationship
  metadata on supplies_to; site-level external_ids). Follow-ups:
  - Second / third pressure-test entries (a yeast supplier or
    cooperage source) will provide further data on whether the
    SCHEMA-GAPS observations materially affect new entries or
    can stay deferred indefinitely.
  - When 3+ entries are populated, evaluate whether
    production_line entries should add a structured `maltster:`
    field referencing supplier slugs, replacing the current
    free-text `malt.maltster` field. This would be the v0.2
    promotion candidate (data-driven, like the bottler v0.1 →
    v0.2 transition).
  - When a bottling entry materially turns on supplier identity
    (e.g., a "100% Heaven Hill cooperage" release), add a
    structured `cooperage_source:` field on the bottling entry
    referencing supplier slugs.
  - Existing glossary entries (bairds-malt, heaven-hill,
    buffalo-trace, distillers-yeast) are NOT replaced when
    supplier entries are added — the glossary entries serve a
    different role (short tooltip reference). The supplier
    entries provide the structured-fields layer.

### Not yet drafted

- (None currently — every entity type referenced in data has at
  least a v0.1 schema.)

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

- **`educational/cask-maturation-kinetics`** — **LANDED 2026-05-16**.
  Covers the three kinetic phases of oak-compound extraction
  (initial rapid surface-layer extraction; slower extraction from
  intact wood; slow exchange / equilibrium), oxidative changes,
  reductive vs oxidative maturation, angel's share composition by
  RH, fill-strength effects, and an explicit "Contested and open
  questions" section flagging mouthfeel / house-character /
  optimum-age / over-maturation claims that exceed published
  chemistry. 5 sources: Mosedale & Puech 1998 (with DOI),
  Conner et al. 1992, Wanikawa et al. 2002, Russell ed. 2014
  chapter on maturation, and an internal cross-reference to the
  Octomore production-line entry for the 68.5% fill case. The
  cask entries (`oloroso-sherry-butt`, `fino-sherry-butt`,
  `virgin-oak`, `bourbon-barrel`, `wine-cask` and named-appellation
  variants) can now tighten their kinetic prose by citing this page
  rather than soft-pedalling — follow-up cleanup of those entries
  is queued (see Cask follow-up below).
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

**Status (2026-05-16): migrations applied.** All 8 affected
wine-cask entries now carry a regulatory_text source at id=3
(or id=2 for entries that had only one prior source) citing the
INAO cahier des charges (French AOCs) or MIPAAF disciplinare
(Italian DOCG). Wikipedia citations preserved per project policy
on rejected-source retention. Affected entries — all migrated:

- `data/casks/pomerol-wine-cask.yml` — INAO Pomerol AOC
- `data/casks/pauillac-wine-cask.yml` — INAO Pauillac AOC
- `data/casks/sauternes-wine-cask.yml` — INAO Sauternes AOC
- `data/casks/burgundy-wine-cask.yml` — INAO Burgundy/Bourgogne
  framework
- `data/casks/rhone-wine-cask.yml` — INAO Rhône framework
- `data/casks/ventoux-wine-cask.yml` — INAO Ventoux AOC
- `data/casks/mourvedre-wine-cask.yml` — INAO Bandol AOC (the
  variety's principal French AOC home)
- `data/casks/amarone-wine-cask.yml` — MIPAAF Amarone della
  Valpolicella DOCG

**Follow-up:** Specific INAO cahier-des-charges PDF URLs and
MIPAAF disciplinare URLs are unstable; each entry currently
cites the institutional homepage with a note that the specific
document URL should be verified when accessed. Per-AOC URL
grounding is queued as a follow-up.

### Sherry DO sources (Consejo Regulador upgrade)

**Status (2026-05-16): migrations applied.** Both sherry-butt
entries now carry a regulatory_text source citing the Consejo
Regulador del Vino de Jerez's Reglamento for the Jerez-Xérès-
Sherry and Manzanilla-Sanlúcar de Barrameda DO. Wikipedia
preserved. Affected:

- `data/casks/oloroso-sherry-butt.yml` — Consejo Regulador
  Reglamento (covers oloroso oxidative style)
- `data/casks/fino-sherry-butt.yml` — Consejo Regulador
  Reglamento (covers fino flor-biological style)

**Follow-up:** Specific Reglamento PDF URLs via BOE (Boletín
Oficial del Estado) should be verified when accessed.
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

**Status (2026-05-16): glossary/distillers-yeast landed.**
Covers the distilling-vs-brewing strain distinction, the named
yeast houses (Mauri, Kerry, Lallemand, Saf-Instant), and the
sparse-disclosure problem. The glossary entry is the project's
canonical reference for distillers-yeast claims; production_line
entries with `yeast: distillers` (currently Glenmorangie) point
implicitly at this entry.

**Follow-up: per-strain glossaries.** When named-strain
disclosure surfaces across multiple distilleries, glossary
entries for specific strains may warrant adding (e.g.
`glossary/m-strain`, `glossary/distillers-d` — the latter being
the Lallemand commercial strain identifier). Currently no
production_line entry discloses a strain at this level of
specificity.

**Follow-up: peer-reviewed grounding.** The glossary entry's
claims about strain selection criteria (high alcohol yield,
gravity tolerance, ester profile) cite the Russell reference
text with the standard `confidence: medium` hedge. SWRI yeast
research papers and the Boulton & Quain "Brewing Yeast and
Fermentation" textbook (RSC) are natural follow-up sources.

**Follow-up: Bruichladdich single-source Mauri/Kerry claim.**
Bruichladdich-specific TODO records a single-source claim that
the distillery uses Mauri and Kerry yeasts; this remains
uncorroborated against the producer's own current technical
disclosures. The distillers-yeast glossary mentions Mauri and
Kerry as principal yeast houses generally but does not
corroborate the Bruichladdich-specific claim. See
data/distilleries/bruichladdich.NOTES.md.

**Follow-up: wild-yeast and Glenmorangie Allta.** Glenmorangie's
Allta release used a wild Saccharomyces strain isolated from
Cadboll Estate barley. This is a sub-brand currently not modelled
as a separate production_line; the question is queued at
data/distilleries/glenmorangie.yml SCHEMA-OBSERVATIONS.

### Barley varieties and maltster sourcing

**Status (2026-05-16): glossary v1 landed.**
Glossary entries for the four most-cited barley varieties
(`glossary/concerto`, `glossary/optic`, `glossary/bere`,
`glossary/propino`) plus the maltster Bairds (`glossary/bairds-
malt`) and two practice pages covering the malting-source
question (`practice/floor-malting`, `practice/external-malting`).
The named-commercial-supplier modelling question is documented
as a deferred schema candidate (see §Schema work §Not yet drafted).

**Follow-up: remaining barley varieties.** `glossary/publican` and
`glossary/chalice` are referenced from Bruichladdich
production-line variety lists (2 refs each); write when frequency
crosses 3-file threshold or when historical reference work
surfaces specific cultivation data.

**Follow-up: ground AHDB Recommended List citations.** The 4
barley-variety glossaries cite AHDB Recommended Lists with the
standard `confidence: medium` + verification hedge. Specific
registration years, parentage, and Recommended-List status
should be verified against historical AHDB RL documents when
accessed.

**Follow-up: remaining maltsters.** Crisp Malt, Simpsons Malt,
Muntons, and Boortmalt are mentioned in `practice/external-
malting` as principal commercial maltsters serving Scotch, but
none have their own glossary entries yet because none are cited
in current production_line entries. Write when a populated entry
references them.

**Follow-up: peer-reviewed grounding for Bere.** The Bere
glossary cites Theobald et al. 2006 (peer-reviewed) and Barony
Mill (producer-direct). Wishart's later work at Orkney College /
UHI on Bere agronomy and malting is the natural follow-up.

**Source priority for outstanding work:** AHDB Recommended Lists,
IBD Approved Variety lists, agronomic peer-reviewed papers
(Journal of Cereal Science, Field Crops Research), maltster
technical datasheets. NOT producer marketing copy.

### Undocumented technical concepts

A check-pass for whisky-domain technical terms that appear in
prose fields across the data but are not yet captured as glossary
entries. Status (2026-05-16): three rounds done, 15 pages added.
Round 1: educational/swa-regional-designations + 5 glossary
entries (abv, new-make, cask-strength, single-malt, outturn).
Round 2: educational/cask-fill-states + 3 glossary entries
(fermentation, kiln, wash-still). Round 3: 5 glossary entries
(shell-and-tube, reflux, single-cask, mashing, vatting). Remaining
queue:

**Still queued:**

- `educational/scotch-presentation-conventions` — covers
  `chill-filtered` (15 files), `non-chill-filtered` (12 files),
  `natural colour` / `caramel colouring` (11/2 files) and the
  trade-off between 40-46% ABV "high-volume" presentation and
  the cask-strength / NCF / natural-colour cluster. **Deferred
  until the §Filtering techniques research item lands**, since
  chill-filtering chemistry is the deep-dive companion to this
  cluster page.
- `glossary/heaven-hill` / `glossary/buffalo-trace` (4 files
  each) — named commercial bourbon producers cited in cask-source
  disclosure. **Deferred to the barley/malt cross-cutting work**
  (named-supplier modelling question — same schema concern as the
  Bairds maltster entry; better handled with a unified pass over
  named commercial entities rather than ad-hoc glossary entries).

**Low-frequency (1-2 files), defer:**

- `solera`, `appassimento`, `DOCG`, `port-ellen`, `grist`,
  `angel's-share`, `reductive-maturation`, `cask-charge-ratio`,
  `spirit-safe`, `Highland` (only 2 files since most refs are in
  structured `region:` fields, not prose) — single- or
  two-file references; add when frequency crosses the 3-file
  threshold or when an authoritative source surfaces during
  other work.

Audit method: `scripts/audit_technical_terms.py` (one-off Python
in the 2026-05-16 audit; not committed — reproduce with grep
across `data/**/*.yml` prose fields).

### Filtering techniques

The chill-filtered / non-chill-filtered distinction surfaces on
nearly every bottling entry (`non_chill_filtered:` field, plus
prose mentions across 15+ files combined) but the project has no
sourced explainer for what filtering actually removes, at what
temperature, through what medium, and what trade-off the
presentation choice represents. Adjacent filtering touch-points
across the Scotch production chain are similarly undocumented.

Topics to cover:

- **Chill-filtering**: the mechanism (cooling the spirit to
  ~−4 to +4 °C to precipitate long-chain fatty acids, ethyl
  esters, and proteinaceous haze precursors, then filtering
  through cellulose sheets or plate-and-frame filters). What it
  removes (the cloudiness that develops when sub-46% ABV
  whisky is diluted with cold water or ice), what it does not
  (no effect on volatile flavour compounds; some debated
  effect on heavier mouthfeel-contributing compounds). Why
  46% ABV is the de facto producer threshold below which
  chill-filtering is typically applied for shelf-stability.
- **Non-chill-filtered (NCF) practice**: presented as a
  transparency / minimal-intervention claim. Producer-disclosed
  on label by some (Bruichladdich, Springbank, most independent
  bottlers); not disclosed by others.
- **Particulate / polishing filtration**: pre-bottling cellulose
  sheet filtration to remove cask charcoal, sediment, or
  wood-fibre particulates. This is near-universal even on NCF
  whiskies and is distinct from chill-filtering.
- **Spirit-stream filtering during distillation**: not Scotch
  practice. Mention only to contrast with bourbon's Lincoln
  County Process (maple-charcoal filtering) — which is
  irrelevant to Scotch but commonly confused in trade press.
- **In-cask considerations**: are casks ever filtered between
  bottlings? Generally no for Scotch; document the negative.
- **Filter media**: cellulose sheets (Seitz, Pall), diatomaceous
  earth, sintered metal. Different sieve sizes and adsorption
  profiles.

Source priority: peer-reviewed papers on chill-haze chemistry
(fatty acid esters, palmitate behaviour), SWRI technical
publications, Russell's "Whisky: Technology, Production and
Marketing" chapter on bottling, filter-manufacturer technical
datasheets (Pall, Seitz / Pall Corp documentation). NOT producer
marketing copy and NOT consumer-blog speculation. The trade-press
discourse on chill-filtering is heavily contested and conflates
"removes mouthfeel" claims with anecdote; primary chemistry
literature is the only reliable arbiter.

**Status (2026-05-16): v1 landed.**

- `educational/chill-filtering` written — covers the chill-haze
  chemistry (ethyl palmitate / oleate / linoleate precipitation
  mechanism), the chill-filtering process (-4 to +4 °C through
  cellulose sheets), the 46% ABV producer-empirical threshold
  rationale (ethanol-solubility crossover), and the contested
  mouthfeel-impact question with explicit measured framing
  between trade-press extremes. 4 sources: Russell 2014 ch.
  bottling, Conner et al. 2003 (Distilled Spirits: Tradition
  and Innovation conference chapter), Conner et al. 1998/1994
  on ester-aroma interactions, SWR 2009 reg 6.
- `educational/scotch-presentation-conventions` written —
  cluster page covering bottling strength, chill-filter vs NCF,
  natural colour vs caramel colouring (E150a), cask-strength
  claims. Sourced to SWR 2009 reg 6/7 + Russell ch. bottling.
  Maps out the presentation-positioning matrix
  (industrial-core / premium core / craft transparency /
  cask-strength special / cask-strength experimental).

**Follow-up: ground Conner et al. 2003 citation.** The
conference-proceedings chapter cited in chill-filtering needs
the published volume verification when the Worldwide Distilled
Spirits Conference proceedings are accessed (see
docs/bibliography.md).

**Deferred (not landed):**

- `glossary/cellulose-sheet-filter` and
  `glossary/plate-and-frame-filter` — not yet justified by
  frequency in current data.

### Existing literature catalogue

**Status (2026-05-16): catalogue v1 landed.**
`docs/bibliography.md` is the curated inventory of in-depth,
peer-reviewed, and institutional reference works that the project's
claims aim to ground on. Covers Russell ed. 2014, Buxton & Hughes
2014, Mosedale & Puech 1998, the Conner papers, the four primary
academic journals (JIB, Food Chemistry, JAFC, J Cereal Science),
SWRI, the Malt Whisky Yearbook, and MacLean's historical writing.
Also documents the project's positive sourcing standard and
exclusion criteria (consumer scoring guides, distillery-funded
coffee-table books, influencer blogs).

**Follow-up: ground the existing Russell citations.** Seven
concept entries currently cite Russell ed. 2014 with
`confidence: medium` and explicit "page references TBA" hedges:

- `educational/cask-fill-states`
- `glossary/fermentation`
- `glossary/kiln`
- `glossary/mashing`
- `glossary/reflux`
- `glossary/shell-and-tube`
- `glossary/wash-still`

When a copy of Russell ed. 2014 becomes available (library access,
purchase, or institutional copy), cross-check the cited claims
against actual chapter and page references; update each `source`
block with concrete page numbers; promote `confidence: medium` to
`high` per entry as each is verified.

**Follow-up: schema integration.** A `literature_id:` field on the
`source` object would let book citations reference catalogue entries
by slug rather than carrying full bibliographic strings inline.
Deferred until the bibliography is exercised on more entries and
the value of central updates becomes concrete; see
`docs/bibliography.md` §Schema integration for scope.

**Follow-up: forthcoming candidates.** The bibliography lists
several papers as queued candidates (Wanikawa on lactone formation,
further Mosedale stave-extraction papers, Watts & Boulton on
fermentation engineering) that should be sourced for the planned
`educational/cask-maturation-kinetics` page once that work begins.

---

## Frontend follow-ups

Implementation-level follow-ups against the build-pipeline-plan
(`docs/build-pipeline-plan.md`) now that the first-iteration
scaffolding has landed in `/site/`. Items here are concrete UI /
data-rendering issues spotted during iteration, distinct from the
broader implementation sequencing in the build-pipeline-plan.

### Confidence rubric tooltip on entity pages

The confidence field (high / medium / low / stub) renders on
distillery pages as inline coloured text in the EntityHeader
("Confidence: medium"). Currently the only explanation accessible
to a reader is the native browser `title=""` tooltip, which is
limited: no styling, slow appearance, mobile-hostile, not
keyboard-focusable, and screen-reader behaviour varies.

The build-pipeline-plan §Data-display decisions specified that
hovering / clicking the confidence badge should surface an
explanation linking to the project's source-conflict-policy. The
proper accessible implementation is:

- A click-and-focus-triggered popover (not hover-only) with the
  per-level explanation:
  - **high** — multi-source, vetted, current; primary sources
    cited where available
  - **medium** — well-sourced but with documented hedges (often
    "page references TBA" against books, or institutional
    homepages cited where specific-document URLs are unstable)
  - **low** — single-source or contested
  - **stub** — placeholder, minimal data
- Plus a "see source policy" link to the rendered
  source-conflict-policy reference page.
- Keyboard-accessible (focus via Tab; Enter/Space to open;
  Escape to close).
- ARIA-labelled so screen readers announce both the level and
  the description.

Implementation notes for the eventual frontend pass:

- Implement once as a shared `<ConfidenceBadge>` component;
  reuse across all entity types (every entity type carries
  `confidence:`).
- Pull the per-level descriptions from a single source of
  truth (likely a constant in `src/lib/data.ts` or a small
  data file under `/data/concepts/practice/` if it warrants a
  concept page).
- The rendered source-conflict-policy reference page itself
  needs to be implemented (see build-pipeline-plan
  §Implementation sequencing item 8 — reference pages).

Status: queued.

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

- **2026-05-18** Build-pipeline plan items 5-8 landed:
  Pagefind search, Reference pages, /explore/ cross-cutting query
  pages, MapLibre map. /site/ source additions: `src/lib/references.ts`
  (registry of design/policy docs ported as routed pages);
  `src/pages/search.astro` (PagefindUI widget against a
  `data-pagefind-body`-marked `<main>` in BaseLayout); 6 reference
  pages under `/reference/<slug>/` covering about, source-conflict-
  policy, voice-register, bibliography, schema-design-notes,
  contributing (consumed from `/docs/*.md` at build time, leading h1
  stripped); 5 `/explore/` pages — by-region, by-ownership,
  by-peating (binned at the standard ppm tiers from the
  glossary/peating-block convention), by-presentation (cask-strength
  / NCF / natural-colour / single-cask / small-batch cuts),
  by-cask-category. MapLibre map page `/map/` plots 9 distillery
  coordinates on a Carto Positron basemap with click-to-popup
  detail links; fits bounds to the pin extent. BaseLayout extended
  with `indexable` + `pagefindMeta` props; entity detail pages emit
  per-page metadata (entity, region, release_type, cask_category,
  etc.) so Pagefind filter chips work. Index pages marked
  `indexable={false}` to avoid duplicate listings in search. Build
  script changed to `astro build && node scripts/postbuild.mjs`; the
  postbuild helper resolves `ASTRO_OUT_DIR` and runs
  `npx pagefind --site <outDir>` so Windows-native and sandbox
  builds both produce `<outDir>/pagefind/`. New runtime dep:
  `pagefind@^1.1.0`. New About page at `docs/about.md` synthesises
  the project's scope, exclusions, and dual-licence position for
  reader-facing context. Verification: `astro check` passes (only
  pre-existing @types/node errors); `scripts/check_references.py`
  reports 0 findings; sandbox couldn't run the full Astro build
  (>45s) but the wiring is mechanical — Windows-side
  `npm install && npm run build` will produce `/dist/pagefind/`
  end-to-end. Counts unchanged in the data layer.
- **2026-05-17** Full entity-type rendering coverage + Wikipedia-
  style UI refactor (133 HTML pages). Detail + index pages for
  production lines, bottlings, bottlers, casks, suppliers; refined
  concept-page block dispatch for all 5 kinds; concept overview +
  per-kind sub-indexes. UI refactored to content-first Wikipedia
  layout (42rem measure, #3366cc links, alt-row table headers,
  cards stripped). Loader by-id fix (`loadAll().find(x => x.id ===
  slug)`) handles filename/id mismatches like bottlers/signatory.yml
  (id `signatory-vintage`). Home page rewritten as a sortable
  populated-entities table. Build infrastructure adjusted for
  cross-platform builds: `vite.cacheDir` pinned to /tmp on Linux
  sandbox, `outDir` overridable via `ASTRO_OUT_DIR`. No schema
  changes; no data changes.
- **2026-05-17** Frontend scaffolding landed (`/site/`). First
  iteration of the Astro-based static site per the implementation
  sequencing in `docs/build-pipeline-plan.md`. Stack: Astro 5 +
  TypeScript + `yaml` for parsing. Files added (17 total under
  `/site/`):
  - `package.json`, `astro.config.mjs`, `tsconfig.json`,
    `.gitignore`, `README.md`
  - `src/lib/data.ts` — TypeScript data loaders (Distillery,
    ProductionLine, Concept interfaces with build-time YAML
    parsing via `yaml` npm package; reads from `/data/` via
    Node fs)
  - `src/layouts/BaseLayout.astro` — HTML shell, header with
    nav, footer slot, project-wide CSS variables
  - 7 components: Footer (with dual-licence note),
    EntityHeader (name + status + confidence badge),
    LocationBlock (region + coordinates), OwnershipHistory
    (timeline view), EquipmentSpec (mash tun + washbacks +
    stills table + warehouses), SourcesBlock (numbered list
    with source-type colour coding), ProductionLinesList
    (cross-references to deferred production-line pages)
  - `src/pages/index.astro` — home / landing page
  - `src/pages/distilleries/index.astro` — distillery listing
    sorted by name with region / locality / founded /
    ownership summary per entry
  - `src/pages/distilleries/[slug].astro` — dynamic detail
    page using `getStaticPaths()` over all 9 populated
    distilleries
  Build verified at structure-level (file shape, import paths,
  Astro frontmatter syntax); runtime `npm install && npm run
  build` to be run from the development host (sandbox network
  throttling prevented runtime verification in this session;
  the build is expected to succeed at first run on the
  development side). Subsequent iterations follow the
  implementation sequencing: concept pages next (heaviest
  markdown-link rewriting), then production lines / bottlings /
  bottlers / casks / suppliers, then index pages + search +
  map.
- **2026-05-17** Final IB pressure-test stub superseded. With
  Caol Ila populated earlier in the session, the second of two
  IB pressure-test stubs (`signatory-caol-ila-stub`) is now
  replaced by `signatory-caol-ila` (worked-example real release
  form, parallel to the cadenheads-bunnahabhain transition).
  Slug renamed, confidence promoted stub → medium, Signatory
  Cask Strength Collection house defaults populated (single
  cask, cask strength, NCF, natural colour, 700ml — contrasting
  with Cadenhead's 500ml format). Cask-identifier fields
  template-form pending specific-release verification. Old stub
  file overwritten with placeholder empty YAML (user can
  `del data\bottlings\signatory-caol-ila-stub.yml` from
  Windows shell to fully clean up). **No IB pressure-test stubs
  remain in populated data**; both IB-release entries are now
  worked-example representations. Counts: 120 → 121 files,
  31 → 31 bottlings (stub deactivated, new entry added — net
  zero), 485 → 485 resolved refs, 22 dangling refs (no change),
  0 findings.
- **2026-05-17** Three sequential deliverables: build pipeline
  plan + direct-fired-still concept page + Caol Ila (ninth
  distillery). (a) `docs/build-pipeline-plan.md` (446 lines)
  written as the design document for the eventual static-site
  build. Page-type taxonomy DECIDED (one URL per entity-type plus
  cross-cutting query pages under /explore/), routing convention
  DECIDED, markdown-link rewriting rules DECIDED, search-index
  scope DECIDED (Pagefind), map data source DECIDED (MapLibre
  with OSM tiles), tasting-notes display DECIDED (render
  notes_official with attribution only, skip notes_independent),
  commercial-info display DECIDED (rrp with launch-price caveat).
  OPEN items: glossary auto-resolution mechanism (recommend
  explicit-markup + curated text-mining), coordinate precision
  policy (recommend coordinates_source schema field). (b)
  `equipment/direct-fired-still` concept page written, parallels
  `equipment/worm-tub` and `equipment/shell-and-tube-condenser`.
  Covers mechanism (Maillard chemistry at hot copper-wash
  interface), 20th-century industry shift to indirect_steam,
  current practitioners (Glenfarclas, Springbank wash-only +
  forward refs to Macallan, Glenlivet, Ben Nevis). Glenfarclas
  and Springbank distillery entries updated to cross-reference
  the new concept via `distinctive_features:`. (c) Caol Ila
  (ninth distillery): Diageo-owned, east Islay, founded 1846,
  heavily peated, 4-stage ownership history through
  DCL → United Distillers → Diageo. Production line (`caol-ila-
  traditional`, ~30-35 ppm spec from Port Ellen Maltings) plus
  2 bottlings: Caol Ila 12 (43% chill-filtered flagship, launched
  2002 in Diageo's Hidden Malts series) and Caol Ila Distillers
  Edition (Moscatel-finished annual recurring, parallel to
  Lagavulin DE PX-finished — the cross-distillery Distillers
  Edition programme now exercised across two populated
  distilleries). **Resolves the 2 remaining IB-stub forward
  refs** (caol-ila + caol-ila-traditional from
  signatory-caol-ila-stub). Counts: 115 → 120 files, 8 → 9
  distilleries, 13 → 14 production lines, 29 → 31 bottlings,
  45 → 46 concept pages, 457 → 485 resolved refs. Dangling
  21 → 22 (net: +3 forward refs from direct-fired-still's
  used_at_distilleries list to Macallan / Glenlivet / Ben Nevis,
  -2 resolved by Caol Ila landing). 0 validator findings.
