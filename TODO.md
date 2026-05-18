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
- **2026-05-17** Eighth distillery (Glenfarclas) populated.
  First populated distillery in the formal SWA Speyside region —
  Glenmorangie is geographically northern Highland, not Speyside,
  so the project's region coverage now includes Speyside as well
  as Highlands / Islay / Islands / Campbeltown. First populated
  distillery exercising the schema's `heating: direct_fire`
  enum value (all prior populated distilleries use
  `indirect_steam`); the JSON Schema validator confirmed the
  enum value works. Family-owned by J. & G. Grant in unbroken
  succession since 1865 — unusual at industry scale where most
  Scotch distilleries have passed through corporate-acquisition
  cycles. Six direct-fired pot stills (3 wash + 3 spirit), the
  largest pot stills in Speyside. Single production line
  (`glenfarclas`, unpeated, sherry-cask-led). Three bottlings:
  Glenfarclas 10 (40% chill-filtered entry-level core),
  Glenfarclas 15 (46% NCF natural-colour premium core — unusual
  in combining a 15-year age statement with the higher-ABV NCF
  natural-colour pattern that other producers adopted only in
  the 2010s), Glenfarclas 25 (43% chill-filtered luxury core).
  All three cross-reference `educational/cask-maturation-kinetics`
  for the maturation-phase framework (10 in phase 2, 25 in
  the slow-exchange phase). Critical-eval fix: removed
  self-referential project-state claim from the distillery
  description prose ("the first formally-Speyside distillery in
  WhiskyBase's populated data set" was a category error — the
  data-set membership isn't a fact about the distillery).
  Counts: 111 → 115 files, 7 → 8 distilleries, 12 → 13
  production lines, 26 → 29 bottlings, 437 → 457 resolved refs,
  21 dangling refs (no change), 0 findings.
- **2026-05-17** Three sequential deliverables: Bunnahabhain
  Toiteach + first non-stub IB pressure-test + second supplier
  pressure-test. (a) Bunnahabhain Toiteach peated sub-line added
  (`bunnahabhain-toiteach` production_line at 35-40 ppm spec
  range + `bunnahabhain-toiteach` core bottling at 46.3% NCF
  natural colour). The Bunnahabhain distillery entry's
  production_lines list updated to include both lines;
  SCHEMA-OBSERVATIONS Toiteach note marked RESOLVED. Tests
  multi-line modelling on Bunnahabhain at smaller scale than
  Springbank's three lines. (b) IB pressure-test
  `cadenheads-bunnahabhain-stub` replaced with
  `cadenheads-bunnahabhain` (worked-example real release form):
  slug renamed, confidence promoted stub → medium, presentation
  conventions populated with Cadenhead's house defaults (single
  cask, cask strength, NCF, natural colour, 500ml bottle).
  Cask-identifier fields (cask number, vintage, outturn, exact
  ABV) remain null with explicit "template-form pending
  specific-release verification" notes — honest stance vs
  fabricating cask-identifier data. Old stub file overwritten
  with placeholder empty YAML (resolver ignores; user needs to
  `del` the file from Windows shell to fully clean up).
  (c) Second supplier entry: Heaven Hill (data/suppliers/
  heaven-hill.yml) at `type: cooperage_source`, the second
  branch of the supplier type enum. Three sites (Bardstown HQ,
  Bernheim Distillery, Cox's Creek warehouses), three product
  types, Shapira-family ownership lineage since 1935.
  SCHEMA-OBSERVATIONS block confirms v0.1 schema is adequate
  for the non-maltster supplier-type case; no v0.2 promotion
  driven. **Supplier schema now has 2 entries covering 2 of 5
  enum branches (maltster + cooperage_source).** Counts: 107 →
  111 files, 11 → 12 production lines, 25 → 26 bottlings,
  1 → 2 suppliers, 428 → 437 resolved refs, 21 → 21 dangling
  refs (no new dangling), 0 findings.
- **2026-05-17** Seventh distillery (Bunnahabhain) populated.
  North-east Islay (geographically and stylistically separate from
  the south-coast peated cluster), founded 1881 to supply the
  Greenlees brothers' Claymore blend. Five-stage ownership history
  (Highland Distilleries → Edrington → Burn Stewart → Distell →
  Heineken/Distell) populated cleanly via `ownership.history`.
  Lightly-peated default production at ~1-2 ppm spec — exercises
  the low end of the peating spectrum (contrast to Lagavulin's
  ~35 ppm and Octomore's 167-258 ppm). Peat-free water source
  from the Margadale River. Onion-shape stills, shell-and-tube
  condensers. Single production line populated
  (`bunnahabhain-traditional`); the separate Toiteach/Moine
  peated sub-line is documented in SCHEMA-OBSERVATIONS but
  deferred from this round. One flagship bottling populated:
  Bunnahabhain 12 Year Old (46.3% ABV, NCF natural colour since
  2010) — exercises the "craft transparency" presentation cluster
  from `educational/scotch-presentation-conventions` at a
  high-volume core release point (one of the early industry
  transitions from 40% chill-filtered E150a to 46.3% NCF natural
  colour for a core release). **Resolves 2 dangling forward refs**
  (cadenheads-bunnahabhain-stub → bunnahabhain and
  bunnahabhain-traditional). Counts: 104 → 107 files, 6 → 7
  distilleries, 10 → 11 production lines, 24 → 25 bottlings,
  416 → 428 resolved refs, 23 → 21 dangling refs, 0 findings.
- **2026-05-17** Sixth distillery (Highland Park) populated.
  Orkney, founded 1798, Edrington-owned (since 1999 via the
  Highland Distillers acquisition). Single production line
  (`highland-park`) with partial on-site floor-malting (~20% per
  producer disclosure) using local Hobbister Moor peat;
  exercises `practice/floor-malting` cross-reference. Region
  recorded as `Islands` per trade convention with explicit note
  in the entry that the formal SWA region (Scotch Whisky
  Regulations 2009) is Highland — pressure-tests the
  `educational/swa-regional-designations` formal-vs-informal
  framing. Sherry-cask-heavy maturation programme (oloroso
  ex-sherry butts predominantly + ex-bourbon supplement); cross-
  references `educational/cask-maturation-kinetics` for the
  phase-2 extraction framework in the Highland Park 18 entry.
  Three bottlings populated: Highland Park 12 (40% ABV chill-
  filtered, modern "Viking Honour" rebrand of the long-standing
  flagship), Highland Park 18 (43% ABV chill-filtered, "Viking
  Pride" rebrand), Highland Park Cask Strength (annual recurring
  series, NCF natural-colour at 60-65% ABV — exercises the
  cask-strength / NCF / natural-colour cluster from
  `educational/scotch-presentation-conventions`). Critical-eval
  fixes: removed `famous-grouse` slug from `also_used_by_blenders`
  (blends not modelled as project entity type; empty list with
  comment matches project convention used in lagavulin /
  glenmorangie / bruichladdich / springbank); generalised two
  producer-URL paths to homepage to avoid URL-hallucination risk.
  Counts: 99 → 104 files, 5 → 6 distilleries, 9 → 10 production
  lines, 21 → 24 bottlings, 394 → 416 resolved refs, 0 findings.
- **2026-05-17** Supplier schema v0.1 pressure-test. First supplier
  entry — `data/suppliers/bairds-malt.yml` — written against the
  v0.1 DRAFT schema, mirroring the bottler v0.1 → v0.2 pattern
  (Cadenhead's then Signatory). Multi-site coverage (Inverness,
  Pencaitland, Witham) tests the `sites:` list shape; HPLC phenol
  measurement capability tests the per-site `capabilities:` field;
  `products:` list covers peated + unpeated malt; `supplies_to:`
  resolves to harris and bruichladdich slugs (resolver count 392
  → 394). SCHEMA-GAPS block at the end of the entry documents
  6 observations for a possible future v0.2 promotion (per-product
  produced_at_sites field; OPTIONAL per-supplier-type product
  enums; relationship metadata on supplies_to; site-level
  external_ids). **Conclusion: v0.1 is adequate for current data;
  no promotion needed.** Schema stays at v0.1 with Bairds as its
  first populated entry. Next pressure-test (yeast supplier or
  cooperage source) will provide further data. Critical-eval fix
  applied: source-type mismatch on the internal cross-reference
  source (trade_publication → other). Project counts: 99 files
  scanned, 1 supplier, 394 resolved refs, 0 validator findings.
- **2026-05-16** Filtering deep dive + presentation conventions
  + appellation migrations + supplier schema. Three substantial
  deliverables in one pass. (a) `educational/chill-filtering` and
  `educational/scotch-presentation-conventions` written, closing
  the filtering research item and the presentation-conventions
  cluster page that has been queued since round 2. Chill-haze
  chemistry (ethyl ester precipitation), 46% ABV producer-empirical
  threshold rationale, the contested mouthfeel-impact question
  framed between trade-press extremes. Presentation cluster maps
  the 4-decision matrix (strength / chill-filter / colour / cask-
  strength) against the producer positioning landscape. (b) All
  10 appellation cask entries migrated from Wikipedia-primary to
  regulatory-text-primary sourcing: 7 INAO French AOCs (Pauillac,
  Pomerol, Sauternes, Burgundy framework, Rhône framework,
  Ventoux, Bandol for Mourvèdre), 1 MIPAAF Italian DOCG (Amarone),
  2 Consejo Regulador del Vino de Jerez (oloroso, fino).
  Wikipedia citations preserved per project policy on
  rejected-source retention. (c) `supplier` entity type schema
  drafted at v0.1: `schema/supplier.template.yml` (171 lines) +
  `schema/json/supplier.schema.json` parallels the bottler entity
  for upstream commercial parties (maltster | cooperage_source |
  yeast_supplier | barley_breeder | other), with sites, ownership,
  products, supplies_to fields. Resolver and JSON Schema validator
  updated to know about `data/suppliers/`; entity-schema dict in
  `scripts/check_references.py` gains the supplier mapping; new
  `supplies_to` LIST_REF target added. Schema is DRAFT until a
  pressure-test entry is added; existing glossary entries
  (bairds-malt, heaven-hill, buffalo-trace, distillers-yeast) are
  NOT migrated — they coexist with future supplier entries.
  Concept count 43 → 45 (8 educational + 30 glossary + 2 practice
  + 2 equipment + 3 methodology). Resolved refs 379 → 392. 0
  validator findings.
- **2026-05-16** Cask-entry prose cleanup against the new
  cask-maturation-kinetics page. Three entries had hedging prose
  about kinetic claims that the new educational page now grounds:
  oloroso-sherry-butt (the "not stated here as project voice"
  hedge replaced with a concrete cis-/trans-lactone-isomer claim
  cross-referenced to the kinetics page); fino-sherry-butt (the
  "trade attribution rather than universal property" hedge
  rewritten to attribute the prior-contents-chemistry difference
  while keeping spirit-side flavour-contribution claims
  attribution-required); virgin-oak (the "immediately-soluble
  wood compounds" claim tightened to "surface-layer extractives"
  with a cross-reference to the kinetic-phase model). All three
  cross-references use markdown-link form
  (`[cask maturation kinetics](concept/educational/cask-maturation-kinetics)`)
  per the concept template's inline-reference convention. No
  schema changes; prose-only edits.
- **2026-05-16** Two more cross-cutting deliverables landed.
  (1) Bibliography completeness pass: docs/bibliography.md expanded
  from 388 to 767 lines, adding 5 reference texts (Piggott 1989 and
  1983, Lyons & Hill *The Alcohol Textbook*, Boulton & Quain
  *Brewing Yeast and Fermentation*, Udo *Scottish Whisky
  Distilleries*), 5 peer-reviewed author groups (Paterson/Piggott
  Strathclyde group, Wanikawa/Hosoi Suntory, Aylott authenticity,
  SWRI staff Bringhurst/Brookes/Brosnan), 4 journals (JSFA, Food
  Research International, LWT, Chemical Senses, Flavour & Fragrance
  Journal), 3 institutional sources (Heriot-Watt ICBD, SWA,
  Worshipful Company of Distillers, HMRC), and 2 historical-
  industrial references (Moss & Hume 1981, Weir on DCL). The audit
  shifted the catalogue from "covers entries I already wrote" to
  "covers the field". (2) `educational/cask-maturation-kinetics`
  written — the flagship research-heavy teaching page that the
  TODO has carried since the cask schema landed. Covers the three
  kinetic phases of extraction, oxidative changes, reductive vs
  oxidative maturation, angel's share composition by RH, fill-
  strength effects, and an explicit section on contested /
  trade-attributed claims that exceed the published chemistry.
  5 sources (Mosedale & Puech 1998 with DOI, Conner et al. 1992,
  Wanikawa et al. 2002, Russell chapter, internal cross-reference
  to the Octomore production-line entry for the 68.5% fill).
  Concept count 42 → 43. URL-hallucination caught and replaced in
  critical-eval pass (initial draft cited a Bruichladdich URL I
  couldn't verify; replaced with internal-data cross-reference).
- **2026-05-16** Cross-cutting research rounds 4-5: barley
  varieties + maltster practice + commercial-entity glossaries +
  distillers yeast (10 new pages). Barley: glossary/{concerto,
  optic, bere, propino}. Maltster practice pages:
  practice/{floor-malting, external-malting}. Named commercial
  entities: glossary/{bairds-malt, heaven-hill, buffalo-trace}.
  Yeast: glossary/distillers-yeast. Concept count 32 → 42 (5
  educational + 2 equipment + 30 glossary + 3 methodology + 2
  practice — first practice-kind entries). Resolved refs 355 → 372.
  Named-supplier schema question (would parallel the bottler entity
  type) documented as a deferred candidate in §Schema work §Not
  yet drafted; defer until 5+ named maltsters accumulate OR a
  bottling materially turns on supplier identity. Source pattern
  continues: AHDB / IBD framework citations at confidence medium
  with verification hedges; CFR §5.143(c) for the bourbon-barrel
  supply chain at confidence medium; Russell + Theobald 2006 for
  the technical and Bere claims.
- **2026-05-16** Literature catalogue v1 landed
  (`docs/bibliography.md`). Curated inventory of in-depth,
  peer-reviewed, and institutional references covering the
  works cited (Russell ed. 2014, Mosedale & Puech 1998, Conner
  papers) and the works queued for future grounding (Buxton &
  Hughes 2014, MacLean, Malt Whisky Yearbook, SWRI, four
  primary academic journals). Documents the project's positive
  sourcing standard (peer-review / academic publisher /
  institutional research body / primary-source historical
  writing) and the exclusion criteria for non-qualifying
  material (consumer scoring guides, distillery-funded books,
  influencer blogs). Follow-up: cross-check the seven
  Russell-citing concept entries against actual page references
  when a copy becomes available; schema-integration via
  `literature_id:` field is deferred (see §Existing literature
  catalogue follow-ups).
- **2026-05-16** Cross-cutting research round 3: 5 medium-frequency
  glossary entries. `glossary/shell-and-tube` (tooltip pointing to
  the existing equipment page), `glossary/reflux` (distillation
  physics; cross-references lyne-arm and copper-conversation),
  `glossary/single-cask` (industry convention, not SWR2009-regulated
  — explicit), `glossary/mashing` (production stage, ties to
  mash_tun.type field), `glossary/vatting` (combination step,
  paired with single-cask). Concept count 27 → 32 (22 glossary
  entries). Russell-textbook citation pattern continued on 3 of
  the 5 with the same `confidence: medium` + "page refs TBA" hedge;
  the regulatory entries (single-cask, vatting) cite SWR 2009 at
  `confidence: high`. Deferred this round: heaven-hill / buffalo-
  trace (named-commercial-entity question better handled with the
  barley/malt cross-cutting work; same schema-thought issue as
  Bairds maltster).
- **2026-05-16** Cross-cutting research round 2: 4 more concept
  pages from the audit follow-up queue.
  `educational/cask-fill-states` (first-fill / refill / fill_number
  mechanics, ex-bourbon / ex-sherry shorthand, seasoned vs transport
  sherry butts — sourced to SWA Regulations 2009 and Russell ed.
  textbook), `glossary/fermentation` (washback fermentation, 7-9% ABV
  wash, secondary bacterial activity in long fermentations),
  `glossary/kiln` (malt drying, peating mechanism, surviving
  floor-malting practice with qualified named examples),
  `glossary/wash-still` (bulk concentration step, capacity ratios,
  copper conversation tie-in). Concept count 23 → 27 (5 educational
  + 17 glossary). Four entries cite the Russell textbook with
  `confidence: medium` and explicit notes that specific page
  references await the §Existing literature catalogue work — those
  citations should be cross-checked when the catalogue lands.
- **2026-05-16** Cross-cutting research round 1: undocumented
  technical concepts audit + 6 new pages. Audit greps all prose
  fields across `/data/`, frequency-ranks candidate technical
  terms. Round 1 outputs: `educational/swa-regional-designations`
  (resolves Highland/Lowland/Speyside/Islay/Campbeltown/Islands
  references — sourced to Scotch Whisky Regulations 2009),
  `glossary/abv`, `glossary/new-make`, `glossary/cask-strength`,
  `glossary/single-malt` (sourced to SWA Regulations 2009),
  `glossary/outturn` (industry-usage term, no primary regulatory
  citation, confidence medium). Concept count 17 → 23. Audit
  surfaced a follow-up queue documented in §Cross-cutting research
  (cask-fill-states, presentation conventions, kiln, fermentation,
  wash-still, etc.).
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
