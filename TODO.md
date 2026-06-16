# TODO

Active queue for the WhiskyBase project.

**Structure (revised 2026-06-15).** Public beta **shipped
2026-06-15**: the site is live at
`https://kankajan.github.io/WhiskyBase/` and the **Beta-readiness**
must-do set is cleared (that section is kept as a shipped record;
the former BLOCKERs are marked resolved inline). With beta shipped,
the active track is data growth: adding distilleries, production
lines and bottlings (see `docs/handover.md` section 10, Next
priorities). Everything below Beta-readiness is that ongoing
data-growth work or post-beta / deferred quality work (sourcing
upgrades, schema refinements, distillery-specific concept pages,
residual site polish) — none of it blocked beta. Add new items to
the appropriate section.

---

## Beta-readiness — SHIPPED 2026-06-15

**Public beta is live** at `https://kankajan.github.io/WhiskyBase/`
(GitHub Pages via the GitHub Actions deploy on push to master). The
must-do set that gated beta is cleared: the technical / educational
concept backbone (89 concept pages), the deploy pipeline, the
public-facing docs, and the core site hygiene all landed. The
subsections below are kept as a record of what was required, with
the two former BLOCKERs marked resolved inline. Residual,
**non-blocking** site polish moved to Frontend follow-ups.

### Deployment and CI

- **Enable GitHub Pages — RESOLVED 2026-06-15.** GitHub Pages is on
  (Settings → Pages → Build and deployment → Source = "GitHub
  Actions") and the site is public at
  `https://kankajan.github.io/WhiskyBase/`. Subpath hosting works as
  designed (links base-aware, `deploy.yml` supplies
  `BASE_PATH=/WhiskyBase`); the 2026-06-15 `concurrency:
  cancel-in-progress` fix stops an older commit's deploy finishing
  last and reverting the live site. This was the last deploy
  blocker.
- **Full site build verified (2026-06-11).** 217 pages build clean
  at both the root and `/WhiskyBase/` subpath bases. Pagefind index
  step runs in CI (`npm ci` installs the binary); not runnable on
  the Windows dev box, which lacks the pagefind binary locally.
- CI checks on push already exist: `validate.yml` runs
  `check_writes.py`, `check_references.py --strict`, and the gate
  unit tests, plus a root-base site build.

### Public-facing docs and site hygiene

- **`docs/contributing.md` — DONE.** No longer a stub: a full
  contribution guide (what to read, entity types and file
  locations, setup, adding/changing an entry, forward-reference
  registration, running the gates, what gets a PR rejected).
- **About page — DONE.** `site/src/pages/about.astro` renders the
  `/about` route.
- **Site hygiene — partly done.** Landed: 404 page (`404.astro`),
  favicon (`public/favicon.svg`), meta / OpenGraph + canonical tags
  (`BaseLayout.astro`), and the footer adult-audience /
  trademark-independence notices. **Still open (non-blocking, moved
  to Frontend follow-ups):** a privacy note, `robots.txt`, a sitemap
  (no `@astrojs/sitemap` integration installed), and a
  mobile-layout pass.

### Educational-page diagrams

- **Status (2026-05-26): all 10 diagrams settled.** Three visual
  registers documented in `docs/diagram-style.md`:
  - **Sketch** (turbulence + displacement filter): pot-still
    schematic, production-chain flowchart, peating-measurement
    matrix.
  - **Strict** (no filter, precise axes, full grid, plotted from
    a sourced figure): `spirit-cut` (DMTS through the run, after
    Miller Fig. 6.7) and `cask-maturation-kinetics` (solids
    extraction vs cask age, after Miller Fig. 8.11), emitted by
    `scripts/gen_data_diagrams.py` from digitised data points.
  - **Technical-schematic** (clean blueprint conventions:
    `stroke="currentColor"` throughout, double-walled vessels
    with diagonal section hatching, dashed annotation leaders
    with filled-dot terminations, short solid pipe-nozzle stubs
    at inlets/outlets, dashed hidden lines for occluded parts):
    mash-tun, washback, worm-tub, shell-and-tube-condenser,
    coffey-still, spirit-safe. The blueprint conventions were
    settled in the 2026-05-26 pilot on mash-tun and rolled out
    to the other five.
- **AI image generation rejected** for technical diagrams:
  unsourceable, hallucination-prone, cannot plot real data.
- **Photographs** (distilleries, stills, casks) deferred:
  copyright / CC-licensing complexity. A beta ships text +
  diagrams; photographs are post-beta enrichment via CC-licensed
  sources (Wikimedia Commons, Geograph).

### Data sweep (minor — not blockers)

- (none open — the `french-oak-cask` cask entry and the
  `signatory-caol-ila-stub` tombstone removal were completed
  2026-06-11; see Recently completed.)

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

### Production-chain coverage queue (2026-05-20)

A 2026-05-20 audit mapped the 47 existing concept pages against
the full whisky production chain. Decision: complete the
technical-backbone concept pages before resuming distilleries
(14th = Ardbeg, parked) — distillery entries are largely
cross-references into this backbone plus site-specific detail, so
finishing the backbone first stops the same gaps being
rediscovered per distillery. Sourcing is not a constraint:
Russell 3rd ed. and Miller 2024 both cover every item, so each
page can land at `high`. New pages cite Russell 3rd ed.

**Status (2026-05-21):** COMPLETE — all three tiers, 34 concept
pages; the production-chain coverage queue is done. Tier 3 (10):
water, grain-whisky, peat, pneumatic-malting, saccharification,
lautering, lactic-acid-bacteria, marrying, regauging,
age-statement. A coverage audit (2026-05-21) confirms the
technical backbone is comprehensively covered — every stage from
raw materials through malting, milling, mashing, fermentation,
distillation, maturation and blending/bottling now has concept
pages (81 concept pages total). Remaining gaps are minor and
peripheral — production co-products (draff, pot ale, spent lees),
reduction-to-bottling-strength as a standalone term, the "batch"
term — and none are load-bearing; pick them up opportunistically.
Distillery-specific equipment pages
(`equipment/tall-narrow-neck-stills`, `equipment/lomond-still`,
`equipment/victorian-rake-and-plough-mash-tun`) remain queued
above as distillery-extension items. Distilleries can now
resume — Ardbeg (14th distillery) is the next data-layer item.

**Tier 1 — load-bearing spine** (every distillery references
these):

- `educational/distillation` — CLUSTER WRAPPER. A concise
  overview of the process — what distillation is and does
  (volatility, boiling points, vapour-liquid equilibrium,
  ethanol-water separation, the azeotrope), pot vs continuous,
  the wash -> low wines -> spirit batch sequence — that links out
  to the detailed pages rather than absorbing them. Carries the
  narrative arc; depth lives in the referenced pages.
- `educational/spirit-cut` — the cut as a process: foreshots/
  heads, middle cut/heart, feints/tails, defined by collection
  strength and driven by congener volatility distribution;
  liquid / vapour temperatures through a run; relation to
  aromatic-compound character; copper cross-reference. The
  natural home for a congener-by-cut diagram.
- `glossary/spirit-still`, `glossary/low-wines`, `glossary/wash`,
  `glossary/wort` — the missing intermediate stills and liquids
  (wash-still and new-make already exist).
- `equipment/pot-still` — the general pot-still concept.
- `equipment/washback`, `equipment/mash-tun` — the fermentation
  and mashing vessels.
- `educational/maturation` — general maturation overview
  (cask-maturation-kinetics and cask-fill-states already cover
  the kinetics and fill states).
- `educational/warehousing` — dunnage / racked / palletised
  warehouse types and their maturation effect.
- `educational/blending` — blended Scotch and blended malt as
  categories, and the blender's craft.

**Tier 2 — completes the technique picture:**

- `equipment/coffey-still` — continuous / column distillation
  (all of grain-whisky distillation).
- `glossary/germination` (green malt), `glossary/steeping`,
  `glossary/milling` (grist), `glossary/diastatic-power` (with
  the malt amylase enzymes).
- `glossary/oak` — American vs European oak species.
- `glossary/char-and-toast` — cask charring and toasting.
- `practice/cask-finishing` — wood finish / double maturation.
- `equipment/spirit-safe`.
- `glossary/congener`, `glossary/angels-share`,
  `glossary/caramel-colouring` (E150a).

**Tier 3 — supporting detail:**

- `glossary/water` (process water), grain-whisky cereals
  (wheat / maize), `glossary/saccharification`,
  `glossary/lautering`, `glossary/marrying`,
  `glossary/regauging`, `glossary/age-statement` (with NAS),
  `glossary/single-grain`, `glossary/lactic-acid-bacteria`,
  drum / Saladin mechanised malting, `glossary/peat` (the
  material / fuel itself).

Architecture note (2026-05-20, user steer): favour focused
single-topic pages linked from a wrapping overview page, not long
composite pages. `educational/distillation` is such a wrapper — a
short process overview linking to the detailed pages; the depth
lives in `educational/spirit-cut`, `equipment/pot-still`,
`glossary/spirit-still`, `glossary/low-wines` and the rest. The
same model applies to the other stage overviews
(`educational/maturation` wraps the cask / oak / warehouse pages;
a malting overview would wrap kiln / steeping / germination).
Focused pages are individually linkable and confidence-rated,
give better Pagefind search granularity, and leave room for
per-topic tables and diagrams; the wrapper carries the narrative.

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

### Macallan Wikipedia migrations (2026-05-26)

The 15th distillery entry, Macallan, cites only two Wikipedia
sources (The_Macallan_distillery + Edrington). Migrate the
load-bearing claims to primaries when the upstream sources
become accessible:

- Producer pages: `themacallan.com/en/inside-the-macallan/our-estate`
  and `themacallan.com/en/explore-our-single-malts` (returned
  empty at fetch time 2026-05-26 — JS-rendered or CSP-blocked).
- Scotchwhisky.com Whiskypedia page on The Macallan (returned
  empty at fetch time 2026-05-26).
- whisky.com database entry (returned empty at fetch time
  2026-05-26).
- The book sources Wikipedia indexes for Macallan: Kindersley
  2008 (Whisky, Dorling Kindersley); MacLean 2008 (Eyewitness
  Companions: Whiskey, DK); Bowman 2017 (The Pocket Guide to
  Whisky, Birlinn). All are general-interest references rather
  than the academic Russell / Miller lineage; useful as a
  triangulation step before migrating to Master of Malt /
  trade-press citations.
- Specific Wikipedia-internal inconsistency to resolve in
  migration: the article credits the new 2018 still house to
  "Norman Foster" in one paragraph and to "Rogers Stirk Harbour
  + Partners" in the infobox + Stirling-Prize-2019 citation; the
  project recorded RSHP per the better-attributed source, but
  this should be confirmed against the producer's own page or
  the RIBA practice portfolio.

### Glenlivet Wikipedia migrations

**Status (2026-06-14): partial migration done.** Diffords Guide was
added as source 3 on the distillery entry, independently corroborating
founding, owner, Josie's Well water, unpeated malt, tall stills and the
1884 name trademark, and supplying the wooden-washbacks datum. Two
conflicts surfaced (global sales rank: Wikipedia 2nd vs Diffords 3rd;
county: Banffshire historic vs Moray modern) — recorded in
`glenlivet.NOTES.md` §8. The producer-primary migration is still
outstanding. Remaining targets:

- Producer pages: theglenlivet.com (JS-rendered) and scotchwhisky.com
  Whiskypedia on The Glenlivet (HTTP 403) — both re-attempted and still
  blocked 2026-06-14; web.archive.org is not fetchable from the dev
  environment either.
- Confirm the post-2024 plant spec — per-still capacities for the
  new pairs, current washback count, mash-tun type — against a
  producer spec or the latest Malt Whisky Yearbook (the 15,000 L
  wash / 10,000 L spirit figures are Wikipedia's pre-2024 spec,
  assumed continued for the 2024 pairs).
- Confirm ownership-date nuances: Seagram 1977 vs 1978; Pernod
  Ricard 2000 (announcement) vs December 2001 (completion). See
  `glenlivet.NOTES.md`.
- Confirm the Nàdurra Oloroso and 15 French Oak Reserve
  specifications (cask strength / NCF / natural colour / first-fill
  oloroso; new Limousin oak) against producer-published sources —
  the specialist-retailer listings used return 403 to automated
  fetch.
- The "Glenlivet" name legal case (1881 suit / 1884 compromise):
  corroborate against a primary historical / legal source beyond
  Wikipedia and trade histories.

### Talisker Wikipedia migrations (2026-06-14)

The 17th distillery entry, Talisker, is grounded on Wikipedia plus
specialist-retailer listings for the bottling specs. Migrate when
accessible:

- Producer pages: malts.com / talisker.com (JS-rendered, no content to
  automated fetch); scotchwhisky.com Whiskypedia (403).
- Confirm the maltster (Glen Ord is commonly cited but unconfirmed),
  washback count/material, and mash-tun type against a producer spec or
  the latest Malt Whisky Yearbook.
- Confirm the bottling specs against producer sources: the 45.8% ABV
  across the range; the Distillers Edition's ex-amoroso (~6-month)
  finish; Storm's 2013 launch and cask mix. Specialist-retailer listings
  (The Whisky Exchange, Master of Malt) corroborate these but return 403
  to automated fetch.
- Coordinates (57.3017, -6.3537) are third-party-published; confirm
  against a producer / OS source.

### Cameronbridge migrations + grain-schema follow-ups (2026-06-14)

The 18th distillery and first grain distillery, Cameronbridge, is grounded
on Wikipedia (+ trade listings for the single-grain bottlings). Follow-ups:

- Producer / scotchwhisky.com Whiskypedia (Cameronbridge 1997; Cameron Brig
  1996) and Diageo pages were not fetched (403 / JS). Migrate when fetchable.
- Confirm: column-still count/type, the wheat/malted-barley grain-bill
  proportions, the new-make distillation strength, the capacity basis
  (litres vs LPA), and coordinates (left null).
- Confirm bottling specs (Cameron Brig colour/filtration; Haig Club /
  Clubman cask + launch detail) against producer sources.
- **Grain-schema structuring — DONE (2026-06-14).** Resolved when North
  British (grain distillery #2) landed and confirmed the shapes. Added
  `stills.column_stills: {count, still_type, notes}` and
  `cereal_bill: [{cereal, proportion, malted, notes}]` (CHANGELOG [0.8.7]);
  Cameronbridge was retrofitted from prose to both fields.

### North British migrations + IB worked example (2026-06-14)

The 19th distillery and second grain distillery, North British, is grounded
on Wikipedia + trade references. Follow-ups:

- Migrate to scotchwhisky.com Whiskypedia (2006/north-british) and producer
  primaries when fetchable (403 / JS at population time).
- Confirm the Coffey-still count (three vs four — recorded four), the cereal
  proportions (85/15 maize / malted barley), the ~94.5% ABV new-make
  strength, the capacity currency (~65M LPA, 2007), coordinates and water
  source.
- **Add an IB single-grain worked example.** North British has no own OB
  single grain (`bottlings: []`); its single grains are independent
  bottlings (Signatory, Hunter Laing, Lady of the Glen, That Boutique-y B10
  25yo) plus a 2018 Douglas Laing OB collaboration. Add a worked example
  (e.g. a Signatory North British) when a verifiable release — vintage,
  cask, ABV — is identified; it would be the project's first IB grain
  release.

### Aberlour migrations (2026-06-14)

The 20th distillery, Aberlour, is grounded on Wikipedia + trade listings.
Follow-ups:

- Migrate to producer primaries when fetchable; **resolve the water-source
  conflict** — St Drostan's Well (producer-associated, recorded) vs
  Wikipedia's infobox Birkenbush / Target spring.
- Add coordinates (left null).
- Confirm bottling specs (A'bunadh first-fill-oloroso / cask strength; 12 &
  16 Double Cask ABV and cask mix) against producer sources.

### New-wave distilleries migrations (2026-06-14)

Nc'nean (21st), Ardnamurchan (22nd) and Ardnahoe (23rd) are grounded on
Wikipedia + specialist-retailer references (producer pages JS-rendered to
automated fetch). Follow-ups:

- Migrate each to producer primaries when fetchable; add coordinates (all
  left null).
- **Nc'nean:** confirm cask proportions and barley variety. If STR
  red-wine maturation recurs across distilleries, consider an STR cask
  slug / flag (currently modelled as generic `wine-cask`). Nc'nean is also
  the driving example if a `certifications` / sustainability field is ever
  wanted (organic, B Corp, net-zero are in prose only).
- **Ardnamurchan:** confirm the peated-campaign ppm and cask proportions.
  Candidate concept page `practice/cask-composition-transparency` (the "AD"
  codes), alongside Bruichladdich's bottle-code transparency already queued.
- **Ardnahoe:** confirm founding/first-spirit dates (2018 opening vs
  Wikipedia 2019 vs ~2019 first fill) and the peat origin (Islay vs
  mainland; `peat_origin: unknown`).

### Literature-resource scouting (user can supply digital copies)

Catalogue moved to `docs/literature-scouting.md` — the standing
list of reference works worth acquiring, with ISBNs, access
status, and what each unblocks. Held as of 2026-05-20: Miller,
*Whisky Science* 2nd ed. (2024) — the independent academic source
that resolves the confidence blocker; Russell 3rd ed. (2022) —
currency upgrade only, same chapter authors as the 2nd edition;
the la Grange-Nel 2003 yeast thesis — supplementary /
bibliography-mining source. Still worth acquiring: Piggott, Sharp
& Duncan (1989), now a third corroborating voice rather than
load-bearing. Open-access sources usable now: *Beverages* (MDPI)
and the Journal of the Institute of Brewing.

Task-2 status: DONE (2026-05-20). The Miller grounding pass is
complete. Five of the seven medium-confidence glossary entries —
kiln, mashing, fermentation, reflux, wash-still — were promoted
to `high`, each now citing Russell + Miller with page-level
corroboration. Both remaining entries were resolved 2026-06-12: `distillers-yeast`
promoted to `high` (named yeast-house list corroborated by Daute,
Jack & Walker 2024, *FEMS Yeast Research* foae017 — an open-access,
SWRI-coauthored paper) and `shell-and-tube` promoted to `high`
(copper/DMTS condenser mechanism corroborated by Harrison, Fagnen,
Jack & Brosnan 2011, *J. Inst. Brew.* 117(1) — SWRI). All seven of
the original production-chain glossary entries are now `high`.
Update `docs/literature-scouting.md` after each future scouting pass.

### Russell 2nd -> 3rd edition citation migration

Sixteen concept entries cite Russell ed. 2014 (the 2nd edition):
the glossary entries kiln, mashing, fermentation,
distillers-yeast, reflux, shell-and-tube, wash-still, lyne-arm;
the educational pages cask-fill-states, cask-maturation-kinetics,
chill-filtering, scotch-presentation-conventions; the practice
pages floor-malting, external-malting, triple-distillation; and
equipment/direct-fired-still.

The 3rd edition (Russell, Stewart & Kellershohn, 2022) is now
held and is the citation of record for new entries (Ardbeg
onward). That leaves the project split across two editions of the
same work, which is inconsistent and should eventually be
reconciled onto the 3rd edition.

DEFERRED WORK: re-ground all sixteen entries against the 3rd
edition. This is NOT a find-and-replace - the 3rd edition is
rechaptered and repaginated. Known chapter remapping: 2nd-ed Ch 6
raw materials -> 3rd-ed Ch 10; Ch 7 yeast/fermentation -> Ch 12;
Ch 8 contamination -> Ch 13; Ch 9 batch distillation -> Ch 14;
Ch 11 maturation -> Ch 16 (Aylott's analytical chapters map to
the 3rd-ed Ch 18-19 region, to be confirmed during the pass).
Each cited claim must be relocated in the held 3rd-edition PDF
and its chapter + page reference rewritten. Currency-only: it
changes no claim and moves no confidence level. Lower priority
than data-layer growth; run as a single dedicated pass.

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

### Residual site hygiene (post-beta, non-blocking)

Carried over from Beta-readiness when public beta shipped
2026-06-15. None of these gate anything — the site is already
live — but they are the natural next polish:

- **Privacy note.** No `privacy` content exists anywhere in
  `site/src`. Add a short static page (data sources; tracking /
  analytics statement as applicable) and wire it into the footer.
- **`robots.txt` + sitemap.** Neither is emitted today
  (`postbuild.mjs` runs only Pagefind; no `@astrojs/sitemap`
  integration). The deploy already sets the `SITE` var for absolute
  URLs, so adding the sitemap integration plus a `robots.txt`
  pointing at it is small.
- **Mobile-layout pass.** Verify the grouped index tables and the
  entity pages on a narrow viewport.

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

Status: **LANDED 2026-05-18**. `<ConfidenceBadge>` component
implemented at `site/src/components/ConfidenceBadge.astro` with
keyboard-accessible popover (Tab to focus, Enter/Space/click to
open, Escape to close, click-outside to dismiss), ARIA
`aria-expanded` / `aria-controls` plumbing, and a link to
`/reference/source-policy/`. Used in `EntityHeader.astro`,
`pages/distilleries/index.astro`, and
`pages/production-lines/index.astro`. Per-level rubric is the
single source of truth inside the component.

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

- **2026-06-15** Yeast educational page renamed for findability, and the
  fermentation page deepened. The distillers-yeast promotion was renamed
  `educational/yeast-strains` (it could not be `educational/distillers-yeast`
  without duplicating the glossary id). `educational/fermentation-overview`
  was expanded from a short stage-wrapper into a substantive stage page
  (washback; pitching and the fermentation curve; the two-phase yeast +
  lactic-acid-bacteria fermentation; fermentation time as a flavour lever),
  sourced to Russell 2022 + Miller 2024, confidence medium. Slug kept as
  `fermentation-overview`.
- **2026-06-15** Fixed the `*/fermentation` duplicate `id`: the
  educational stage-wrapper was renamed `educational/fermentation` ->
  `educational/fermentation-overview` (the glossary term keeps the bare
  `fermentation` slug), its 7 inbound references were updated, and the
  handover wrapper mention corrected. Note `educational/mashing` still
  shares its `id` with `glossary/mashing` — the same fix is available
  on request.
- **2026-06-15** Glossary audit implemented (plan:
  `docs/glossary-audit-2026-06-15.md`). Two entries promoted to
  educational pages, glossary stubs kept and tightened:
  `distillers-yeast` -> `educational/yeast-strains`
  and `oak` -> `educational/oak-species` (concept pages 87 -> 89,
  educational 19 -> 21). `marrying` extended in place (vatting-vs-
  marrying distinction + the Glenfiddich Solera example). Fixed the
  `bere` six-row / `var. distichum` contradiction. Added see_also
  depth-gradient links (`char-and-toast`, `fermentation`, `mashing`
  to their educational pages; charring prerequisite retargeted to
  `oak-species`). The other ~47 glossary entries were assessed and
  left as adequate.
- **2026-06-15** Public beta SHIPPED. GitHub Pages enabled (Source =
  "GitHub Actions"); the site is live at
  `https://kankajan.github.io/WhiskyBase/` — the last Beta-readiness
  blocker cleared. Confirmed already-done (the docs were stale):
  `docs/contributing.md`, the `/about` route, the 404 page, favicon,
  and OpenGraph/canonical tags. Residual non-blocking polish moved
  to Frontend follow-ups. No schema or policy change, so no CHANGELOG
  entry.
- **2026-06-14** Cask wood concept pages — two educational pages on the
  cooperage/maturation backbone: `educational/cooperage` (making and
  refurbishing casks: oak selection, stave seasoning, raising and firing,
  rebuilding ex-bourbon barrels into hogsheads, sherry seasoning, and the
  de-char/re-char rejuvenation cycle) and `educational/cask-charring-and-
  toasting` (why the interior is fired, toasting vs charring, char levels
  #1-4 / alligator, the lignin/hemicellulose chemistry, and the dual
  additive/subtractive effect incl. activated-carbon sulphur removal).
  Both sourced to Russell ed. 2022 Ch 16 (Conner) + Miller 2024 Ch 8 +
  Mosedale & Puech 1998, with a Czech trade reference for the char-level
  specifics; confidence medium. The existing glossary stubs (`glossary/
  char-and-toast`, `glossary/oak`) now cross-link to these as their deep
  companions. Concept pages 85 → 87 (educational 17 → 19).
- **2026-06-14** New-wave batch — Nc'nean (21st), Ardnamurchan (22nd),
  Ardnahoe (23rd). 3 distilleries + 3 production lines + 3 flagship
  bottlings + 3 NOTES. New dimensions for the data set: **Nc'nean**
  (Drimnin, Morvern, Highlands; 2017; organic / net-zero / B Corp; first
  organic whisky and first wine-cask-led core malt — STR red wine modelled
  as `wine-cask`); **Ardnamurchan** (Glenbeg, Highlands; 2014;
  Adelphi-owned independent-bottler distillery; peated + unpeated on one
  line, core ~50:50; "AD" cask-transparency); **Ardnahoe** (Islay, near
  Port Askaig; 2018; Hunter Laing; worm-tub condensers + long lye pipes,
  ~40 ppm — resolved the equipment/worm-tub forward ref and was removed
  from expected_dangling.txt). All three are independent/owner-led or
  IB-owned, contrasting the established majors. Counts: 20→23 distilleries,
  25→28 production lines, 57→60 bottlings. Not validated locally (no
  Python); relies on the CI strict gate.
- **2026-06-14** Aberlour — 20th distillery. 1 distillery + 1 production
  line + 3 bottlings + NOTES. Charlestown of Aberlour, Speyside (Moray);
  Pernod Ricard / Chivas; founded 1879 by James Fleming. Fifth Speyside,
  second sherry-led Chivas malt (with Glenlivet). Sherry-influenced
  double-cask house style; ~3.9M LPA on 2 wash + 2 spirit stills (spirit
  pair differing in size, 20,000 / 15,456 L). Bottlings: A'bunadh
  (cask-strength first-fill oloroso, NCF, natural colour, NAS; `abv` null
  as batch-variable ~59-61%), 12 and 16 Double Cask Matured. Water-source
  conflict (St Drostan's Well vs Wikipedia Birkenbush/Target spring)
  documented. Counts: 19→20 distilleries, 24→25 production lines, 54→57
  bottlings. Not validated locally (no Python); relies on the CI strict gate.
- **2026-06-14** North British — 19th distillery, the project's SECOND
  grain distillery, and the confirming example that turned the deferred
  grain-schema observations into structure. 1 distillery + 1 production
  line + NOTES (no bottlings — a pure blending-grain supplier; first
  populated distillery with `bottlings: []`). Gorgie, Edinburgh (Lowlands);
  founded 1885 by Usher/Sanderson/Crabbie to break the DCL grain monopoly;
  owned 50:50 by Diageo and Edrington (Lothian Distillers JV — first
  co-ownership in the data). Continuous Coffey distillation to ~94.5% ABV
  from a MAIZE-led bill (85% maize / 15% malted barley) — the contrast to
  Cameronbridge's wheat. Schema [0.8.7]: added `stills.column_stills` and
  `cereal_bill`, used here and retrofitted onto Cameronbridge. Counts:
  18→19 distilleries, 23→24 production lines (54 bottlings unchanged). Not
  validated locally (no Python on the dev box); relies on the CI strict gate.
- **2026-06-14** Cameronbridge — 18th distillery and the project's FIRST
  grain distillery. 1 distillery + 1 production line + 3 single-grain
  bottlings + NOTES. Cameron Bridge, Fife (Lowlands); Diageo; founded 1824
  by John Haig, a founding DCL grain distillery (1877). Continuous
  (column/Coffey) distillation from a wheat-led cereal bill; ~136M LPA (one
  of Europe's largest). Bottlings: Cameron Brig (long-standing single
  grain), Haig Club (2014 premium), Haig Club Clubman. distinctive_features
  → equipment/coffey-still + glossary/grain-whisky. Schema: added the
  additive `distillation.regime: continuous` value (CHANGELOG [0.8.6]);
  column stills + cereal bill captured in prose with SCHEMA-OBSERVATIONS in
  cameronbridge.NOTES.md (structure deferred to grain distillery #2). Not
  validated locally (no Python on the dev box); relies on the CI strict gate.
- **2026-06-14** Talisker — 17th distillery. 1 distillery + 1 production
  line + 3 bottlings + NOTES. Carbost, Isle of Skye; Diageo; the
  project's first Skye entry and third populated Classic Malt (after
  Lagavulin, Glenkinchie). Founded 1830 by the MacAskill brothers.
  Distinctive: asymmetric five-still set (2 wash + 3 spirit), U-shaped
  lye-pipe purifier loops, and worm-tub condensers on all five stills —
  resolving the equipment/worm-tub forward ref and removing
  `distillery:talisker` from expected_dangling.txt. Medium-peated
  (~18-22 ppm), peppery/maritime; ~3.5M LPA. Bottlings: 10 Year Old
  (45.8% flagship), Distillers Edition (amoroso finish, continuing the
  cross-distillery DE series after Lagavulin/Caol Ila/Glenkinchie), and
  Storm (NAS). Wikipedia-primary; bottling specs (45.8% etc.) from
  specialist-retailer listings, flagged for producer confirmation.
  Counts: 16 → 17 distilleries, 21 → 22 production lines, 48 → 51
  bottlings. Not validated locally (no Python on the dev box); relies on
  the CI strict gate.
- **2026-06-14** Glenlivet source-migration (partial). Added Diffords
  Guide as source 3 on the distillery entry — independent corroboration
  of founding / owner / Josie's Well / unpeated / tall-stills /
  1884-name-case, plus the wooden-washbacks datum
  (`washbacks.material: wood`). Surfaced and documented two conflicts
  (sales rank 2nd vs 3rd; Banffshire vs Moray) and softened the ranking
  claim. Producer + scotchwhisky.com + web.archive.org all unfetchable,
  so the producer-primary migration stays open. See glenlivet.NOTES.md
  §8.
- **2026-06-12** Glenlivet — 16th distillery. 1 distillery +
  1 production line + 3 bottlings + a NOTES.md. Minmore,
  Ballindalloch, Speyside (Moray); Chivas Brothers / Pernod Ricard.
  Founded 1824 by George Smith, the first licensed distiller in the
  glen under the Excise Act 1823 — the other half of the
  Glenfiddich-vs-Glenlivet best-seller pair and the light,
  lantern-still Speyside contrast to Macallan's short-still sherry
  weight. Records the 1881/1884 "Glenlivet" name legal case.
  Bottlings: 12 Year Old (40%, American + European oak), 15 French
  Oak Reserve (new French/Limousin oak), Nàdurra Oloroso
  (cask-strength, NCF, natural-colour, first-fill oloroso). The
  capacity / still-count source conflict is resolved in
  `glenlivet.NOTES.md`: Wikipedia's 14-still / 10.5M-LPA figure is
  the pre-2024 state; the 2024 bicentenary stillhouse doubled it to
  28 stills / ~21M LPA (The Northern Scot, April 2024).
  `distillery:glenlivet` removed from `scripts/expected_dangling.txt`
  (now populated; the `direct-fired-still` forward ref resolves).
  Counts: 15 → 16 distilleries, 20 → 21 production lines,
  45 → 48 bottlings. NOT validated locally — no Python on the dev
  box; relies on the CI strict gate (`validate.yml`).
- **2026-06-12** Sourcing — last two production-chain glossary
  entries promoted to `high`. `glossary/distillers-yeast`: the
  named yeast-house list (MX/Kerry, Pinnacle/Mauri-AB Biotek,
  DistilaMax/Lallemand) and the DCL "M"-strain origin (1952) are
  corroborated by Daute, Jack & Walker 2024 (*FEMS Yeast Research*,
  foae017) — an open-access, SWRI-coauthored paper, the
  producer/SWRI cross-check the entry had lacked; the muddled
  supplier prose was corrected to match the source. `glossary/
  shell-and-tube`: the copper/DMTS condenser mechanism is
  corroborated by Harrison, Fagnen, Jack & Brosnan 2011
  (*J. Inst. Brew.* 117(1), 106-112) — an SWRI peer-reviewed paper.
  All seven original medium-confidence production-chain glossary
  entries are now `high`. Data-only change; no CHANGELOG entry per
  the file's policy.
- **2026-06-11** Astro 5 → 6 migration (closes the failing
  Dependabot astro-6.x PRs). Two real blockers, neither an Astro
  API break: (1) `lib/data.ts` and `lib/references.ts` resolved the
  repo root via `import.meta.url + ../../..` from the *compiled
  chunk's* location — Astro 5 happened to place prerender chunks
  three levels below the root, Astro 6 places them four
  (`site/.astro/.prerender/chunks/`), silently breaking the path.
  Replaced with a marker-directory walk-up from `process.cwd()`
  (new `lib/repo-root.ts`). (2) Astro 6 requires Node ≥ 22.12.0;
  workflows bumped from Node 20 to 22, `engines` updated. Verified:
  full builds (Astro + Pagefind) green at root and subpath bases,
  217 pages — exact parity with the Astro 5 output, zero unbased
  links.

- **2026-06-11** GitHub Pages subpath hosting: internal links made
  base-aware. Nav, page/component markup, dynamic hrefs, the
  markdown content-link rewriter (`lib/markdown.ts`), nav hrefs
  (`lib/data.ts`), the map popup, and the Pagefind UI bundle path
  now prefix `import.meta.env.BASE_URL`, so the site builds correctly
  under the project-repo subpath `/WhiskyBase/`. `deploy.yml` now
  supplies `BASE_PATH=/WhiskyBase` and a default `SITE` on push;
  `astro.config.mjs` reads both from env (unchanged). Verified: 217
  pages build at both the root base (`/`, local/validate parity
  preserved) and the subpath base, with zero unbased internal links
  and no double-prefixes. This fixed the failing `deploy` workflow's
  root cause on the links side. Remaining manual blocker: enable
  GitHub Pages (Settings → Pages → Source = "GitHub Actions").

- **2026-06-11** Audit remediation (`docs/audit-2026-06-11.md`).
  Migrated the Macallan production line + 3 bottlings from a
  pre-v0.2 flat shape to the v0.2 schema; added the
  `french-oak-cask` entry (resolving the last genuine dangling
  ref); renamed `bruichladdich-islay-barley-2023` →
  `…-2014`; reconciled the source-type vocabulary to the canonical
  `_common.schema.json` enum across policy doc, CLAUDE.md and
  templates; strengthened concept per-kind enforcement in
  `concept.schema.json`. Tooling: `check_references.py` gained
  `--strict`, an expected-dangling allowlist
  (`scripts/expected_dangling.txt`), a schema-version currency
  check, and cross-file consistency checks; the pre-commit hook now
  runs `--strict` as a second gate; added `scripts/test_checks.py`.
  Resolver clean: 0 schema findings, 0 unexpected dangling, 0
  consistency contradictions.

- **2026-05-26** 15th distillery: Macallan. Edrington-owned
  Speyside via the Robertson Trust charitable structure; founded
  1824 by Alexander Reid under the Excise Act 1823 at the Easter
  Elchies estate, Craigellachie, Moray. Defining sherry-cask-led
  house style — Sherry Oak core exclusively in oloroso-seasoned
  oak sherry casks from Jerez; the 2004 Fine Oak (renamed Triple
  Cask Matured 2018) added American-oak ex-bourbon casks
  alongside European- and American-oak sherry casks; Edrington's
  Sept 2023 acquisition of the Vasyma cooperage in Jerez
  vertically integrated the sherry supply chain. The new 2018
  still house (Rogers Stirk Harbour + Partners, £140m) holds 36
  stills as 12 wash + 24 spirit, with the spirit stills at
  3,900 L charge — among the smallest in Scotland and a
  long-standing piece of the brand's positioning. ~15M LPA.
  Three bottlings: Sherry Oak 12 (canonical sherry-only),
  Double Cask 12 (European- and American-oak sherry blend),
  Triple Cask Matured 15 (sherry + sherry + ex-bourbon — the
  former Fine Oak 15). Wikipedia is the only directly-fetched
  source — themacallan.com, scotchwhisky.com Whiskypedia, and
  whisky.com all returned empty at fetch time; queued for
  migration in Research Requests below.

- **2026-05-26** Diagram register split + blueprint cross-sections.
  `docs/diagram-style.md` extended from two registers to three:
  the new **technical-schematic** register (for cross-section
  diagrams) sits between the existing sketch and strict registers.
  Within the technical-schematic register, the spec documents the
  blueprint conventions settled in the 2026-05-26 pilot on
  mash-tun: `stroke="currentColor"` throughout (CSS variables do
  not resolve reliably for stroke in all viewers), double-walled
  vessel outlines with generic diagonal section hatching via SVG
  pattern + even-odd fill, dashed annotation leaders (5 3) ending
  in filled-circle dots at the part-end, short solid pipe-nozzle
  stubs at every inlet and outlet, dashed hidden lines (3 2) for
  occluded parts, no flow-direction arrowheads. The six
  cross-section SVGs (mash-tun, washback, worm-tub,
  shell-and-tube-condenser, coffey-still, spirit-safe) re-authored
  to the new register; six equipment concept alt-texts updated.
  No schema changes. CHANGELOG [0.8.3]. The `safe-bulk-writes`
  skill is updated with two new lessons from the same session:
  Write tool truncates at ~3 KB (revised down from ~10 KB); Edit
  tool corrupts multi-line block replacements on existing data
  files. CLAUDE.md gains a "Reducing wasted iteration" section
  adapted from karpathy-skills behavioural guidelines.

- **2026-05-22** Educational-page diagrams — the diagram set for
  the educational and equipment concept pages. The pipeline
  (optional `diagrams:` schema field, `attachDiagramSvg` loader
  inlining, `<figure>` rendering on the concept detail page) was
  proven earlier; this wave authored the full set of 10 SVGs in
  `data/diagrams/` and attached them to their concept entries.
  Two visual registers, codified in `docs/diagram-style.md`:
  hardware / process schematics use a hand-drawn sketch register
  (pure-SVG `feTurbulence` + `feDisplacementMap` wobble filter,
  no JavaScript, fixed seed for determinism); data graphs use a
  strict register — no filter, precise axes, full grid, plotted
  exactly from a sourced figure. The two strict graphs —
  `spirit-cut` (DMTS through the spirit-still run, after Miller
  Fig. 6.7) and `cask-maturation-kinetics` (solids extraction vs
  cask age, after Miller Fig. 8.11) — are emitted by the new
  committed `scripts/gen_data_diagrams.py` from data points
  digitised off the cited figures. Settled: pot-still, the
  production-chain flowchart, the peating-measurement matrix,
  both strict graphs. The 6 hardware schematics (mash-tun,
  washback, worm-tub, shell-and-tube-condenser, coffey-still,
  spirit-safe) are committed as first-draft checkpoints — a
  redraw is queued under Beta-readiness. The concept schema
  gained the optional `diagrams` field (additive within v0.1);
  CHANGELOG [0.8.2].
- **2026-05-21** Master overview + stage wrappers — 4 educational
  pages closing the wrapper-layer gap. `educational/whisky-production`
  is the master "How Scotch whisky is made" overview: it sequences
  the entire production chain (raw materials -> malting -> milling
  -> mashing -> fermentation -> distillation -> maturation ->
  blending/bottling) and links every stage. Plus the three stage
  wrappers that were missing — `educational/malting`,
  `educational/mashing`, `educational/fermentation` (distillation
  and maturation already had wrappers). The wrapper layer is now
  complete and symmetric: every production stage has one overview
  page, and the master ties them together. Densely cross-linked
  per the brief — every referenceable concept linked inline — and
  the distillation / maturation / blending wrappers were given
  back-links up to the master so the hierarchy is navigable both
  ways. Also fixed a stale "(queued)" reference in
  `educational/distillation`: the Coffey-still page exists (Tier 2)
  and is now linked. All four new pages `confidence: high`
  (Russell 3rd ed. + Miller). check_references clean (181 files,
  0 schema findings). Concept-page total 81 -> 85.
- **2026-05-21** Ardbeg — 14th distillery. 1 distillery +
  1 production line + 3 bottlings + a NOTES.md. Port Ellen,
  south-coast Islay; completes the four-distillery south-Islay
  heavily-peated "Kildalton" cluster (Ardbeg / Laphroaig /
  Lagavulin / Caol Ila). Founded 1815; one of the most turbulent
  closure/revival histories in the industry — mothballed 1981,
  intermittent 1989-1996, rescued by Glenmorangie plc in 1997,
  to LVMH / Moet Hennessy in 2004. Distinctive feature: a
  purifier on the spirit-still lyne arm (uncommon on Islay),
  cross-referenced to glossary/reflux. Bottlings: 10 Year Old
  (46% NCF natural-colour core), Uigeadail (NAS oloroso-sherry
  vatting, 54.2%), Corryvreckan (NAS French-oak component,
  57.1%). Source conflicts disclosed in ardbeg.NOTES.md (peating
  50 vs 55 ppm; the 2019 still-house doubling from one still pair
  to two; annual capacity left null absent a clean post-expansion
  figure). Critical eval caught and fixed an unsourced
  "1959 Distillers Company" ownership entry and a malt.source
  enum error before verify. Introduces one forward reference —
  `french-oak-cask`, a French-oak cask entry not yet written
  (cited from ardbeg-corryvreckan; populate when convenient).
  Counts: 13 -> 14 distilleries, 18 -> 19 production lines,
  39 -> 42 bottlings. check_references clean (177 files, 0 schema
  findings).
- **2026-05-21** Pre-commit hard-corruption gate added.
  `scripts/check_writes.py` (new) scans text files for the
  Windows <-> Linux mount-sync damage signatures — embedded NUL
  bytes, silent truncation (no trailing newline), YAML parse
  failure — and exits non-zero on any finding.
  `scripts/hooks/pre-commit` (new) runs it against the staged
  files and blocks the commit; activate per clone with
  `git config core.hooksPath scripts/hooks`. The project's first
  commit-blocking check; `check_references.py` stays warn-only
  for soft findings (dangling refs, schema warnings). The gate
  immediately caught a real pre-existing bug — README.md had been
  committed truncated (commit 7c212f2 lost the last table row and
  the closing sentence); repaired here, and its stale
  Current-state counts refreshed (13 distilleries, 18 production
  lines, 39 bottlings, 81 concept pages, 2 bottlers, 17 casks,
  2 suppliers; build pipeline marked implemented). Docs: CLAUDE.md
  Verification section + tooling pointers; CHANGELOG.md [0.8.1].
  Full-repo scan clean (202 text files, 0 findings).
- **2026-05-21** Tier 3 of the production-chain coverage queue
  COMPLETED, and the coverage queue closed. Ten pages: glossary
  water, grain-whisky (cereals + the single-grain category,
  consolidated), peat, saccharification, lautering,
  lactic-acid-bacteria, marrying, regauging, age-statement; and
  practice/pneumatic-malting (drum / Saladin mechanised malting).
  Grounded on Russell 3rd ed. (Ch 10, 11, 13, 15, 16, 17) +
  Miller (Ch 3, 4, 5, 10) + SWR 2009. Confidence: all `high`
  except marrying (`medium` — single-source and carrying Russell's
  own "cannot be explained through chemical analysis" hedge) and
  age-statement (`medium` — single regulatory source, cited at
  instrument level rather than fabricating a regulation number).
  A production-chain coverage audit followed: 81 concept pages
  now cover every stage of the chain; remaining gaps are minor
  and peripheral (co-products, reduction term, batch term) and
  none load-bearing. The technical backbone is complete;
  distilleries can resume (Ardbeg next). check_references clean
  (172 files validated, 0 schema findings).
- **2026-05-21** Tier 2 of the production-chain coverage queue
  COMPLETED — 12 pages. equipment/coffey-still (continuous /
  column distillation for grain whisky) and equipment/spirit-safe;
  the malting-detail glossary entries steeping, germination,
  milling and diastatic-power; the maturation-detail entries
  glossary/oak, glossary/char-and-toast, practice/cask-finishing
  and glossary/angels-share; and glossary/congener and
  glossary/caramel-colouring. Grounded on Russell 3rd ed.
  (Ch 10, 12, 14, 15, 16) + Miller (Ch 3, 4, 5, 7, 8) + SWR 2009
  reg 3. All `confidence: high` except caramel-colouring
  (`medium` — the regulatory fact is single-sourced to SWR 2009;
  the fuller treatment is in scotch-presentation-conventions).
  Critical eval: a raw concept path was removed from the
  caramel-colouring tooltip; the congener summary's
  new-make-vs-matured claim was softened from an absolute to a
  proportionate statement. check_references clean (162 files
  validated, 0 schema findings). Tiers 1 and 2 of the queue now
  complete (24 pages); Tier 3 next.
- **2026-05-21** Tier 1 of the production-chain coverage queue
  COMPLETED. Five pages added to close out Tier 1 after the
  distillation cluster: `equipment/washback` and
  `equipment/mash-tun` (the fermentation and mashing vessels);
  `educational/maturation` (a wrapper overview — the cask's
  additive / subtractive / oxidative action, the SWR 2009
  three-year legal minimum); `educational/warehousing` (dunnage /
  racked / palletised warehouse types and the angel's-share
  effect); and `educational/blending` (the five SWR 2009
  categories, blended Scotch, the blender's craft). All
  `confidence: high`, grounded on Russell 3rd ed. (Ch 10, 12, 16,
  17) + Miller (Ch 4, 5, 8) + SWR 2009 reg 3. Critical eval:
  Miller Ch 8 added to the maturation wrapper so its cask-action
  claims carry two independent sources; an inline Miller citation
  added to warehousing. check_references clean (150 files, 0
  schema findings). Tier 1 of the queue is now complete
  (12 pages); Tier 2 next.
- **2026-05-21** Distillation concept cluster — 7 pages landed.
  Following the 2026-05-20 production-chain coverage audit, the
  distillation cluster was written as the first Tier-1 batch:
  `educational/distillation` (a wrapper / overview page),
  `educational/spirit-cut` (foreshots/heart/feints, the demisting
  test, the spirit safe, congener volatility, run temperatures),
  `equipment/pot-still`, and glossary entries `spirit-still`,
  `low-wines`, `wash` and `wort`. All seven at `confidence: high`,
  each citing Russell 3rd ed. Ch 14 (Nicol, pp 247-271) + Miller
  Ch 6-7 as two independent sources. Architecture: focused pages
  linked from the wrapper, not one long page (user steer — better
  linkability, per-page confidence, search granularity). Critical
  eval: the low-wines strength was softened from a hard
  "~20-25% ABV" to "low-twenties percent" because Russell Ch 14
  grounds only the combined spirit-still charge (<30% ABV), not a
  low-wines-alone figure. check_references clean (145 files
  validated, 0 schema findings). Edit-tool NUL corruption hit
  low-wines.yml and distillation.yml during the wave; both
  rebuilt via heredoc and verified.
- **2026-05-20** Miller grounding pass — task 2 resolved.
  Miller, *Whisky Science: A Condensed Distillation*, 2nd ed.
  (2024), an academic reference independent of the Russell
  lineage, was grounded against the seven medium-confidence
  glossary entries. Five promoted `medium` -> `high`: kiln
  (Miller Ch 3 pp 151-152), mashing (Ch 4 pp 187-199),
  fermentation (Ch 5 pp 219-241), reflux (Ch 6 pp 253-255),
  wash-still (Ch 6-7). Each now carries Russell + Miller as two
  independent sources with page-level notes. Two held at
  `medium`: distillers-yeast (Miller corroborates the
  distilling-strain core — the Distillers Company "M" strain,
  high attenuation, distilling-vs-brewing distinction — but not
  the named yeast-house list, which still needs producer / SWRI
  cross-check) and shell-and-tube (Miller does not treat
  condenser types anywhere in the book, so no second source was
  added). One source conflict surfaced and preserved per policy:
  Miller's first-mashing-water temperature (ca. 70 C) vs
  Russell's first-water strike (63.5-64 C). check_references
  clean (138 files validated, 0 schema findings). Edit-tool
  truncation hit mashing.yml during the wave; repaired and
  verified.
- **2026-05-20** `/production-lines/` and `/bottlings/` index
  pages regrouped. Both rewritten from a single flat table to a
  list grouped under parent-distillery `h2` sub-headings
  (distilleries alphabetical, each heading linking to the
  distillery page). production-lines groups on the line's
  `distillery` field; multi-line distilleries carry a "N lines"
  count. bottlings groups on `produced_at_distillery`, drops the
  now-redundant per-row Distillery column (it is the group
  heading), carries a "N releases" count on multi-release
  distilleries, and retains the OB/IB type column. Rationale: a
  flat table does not scale (bottlings had reached 39 rows); a
  dropdown was rejected (JS-dependent, hides content, invisible
  to Pagefind body-indexing) and an alphabet jump-bar as
  overkill. Matches the casks/index and concept sub-index
  pattern. Both tables use `table-layout: fixed` with explicit
  widths on the narrow columns (Peating/Confidence; ABV/Age/Type)
  so column edges align across every distillery group instead of
  each table sizing independently. astro check clean (only the
  pre-existing @types/node errors). Edit-tool truncation hit both
  index files repeatedly during the wave; both rebuilt via
  heredoc and verified.
- **2026-05-19** Glenfiddich (13th distillery, second Speyside).
  1 distillery + 1 production line + 2 bottlings. Dufftown,
  Speyside; William Grant & Sons, in unbroken family ownership
  since the 1886 founding (a structural parallel to the
  unrelated Grant family's Glenfarclas). Founded 1886 / first
  spirit Christmas Day 1887; original stills were second-hand
  equipment from Cardhu. The distillery most associated with
  the creation of the modern marketed single-malt category —
  the 1963 decision (Sandy Grant Gordon) to actively market
  single malt outside Scotland. Very large scale: ~21M LPA,
  48 Douglas-fir washbacks, 43 stills (16 wash + 27 spirit,
  15 spirit stills direct-fired by gas), on-site coppersmiths
  (since 1957) and cooperage (since 1959), 1M+ casks in
  warehouse. Bottlings: 12 Year Old (40% bourbon+oloroso
  flagship) + 15 Year Old Solera (**first populated bottling
  exercising a solera-style continuous-marrying vatting
  stage** — the 1998 Solera Vat, never drained below
  half-full, inspired by the Spanish sherry solera).
  Critical-eval fix: the "world's largest-selling single malt"
  claim softened to "among the world's best-selling single
  malts" with an explicit note that Glenfiddich and Glenlivet
  trade the top-selling position depending on market and
  measure — the absolute claim is contestable. Edit-tool
  truncation hit glenfiddich.yml and glenfiddich-12.yml during
  the critical-eval edits; both metadata footers restored.
  Counts: 135 -> 139 files, 12 -> 13 distilleries,
  17 -> 18 production lines, 37 -> 39 bottlings,
  547 -> 563 resolved refs, 21 dangling unchanged, 0 schema
  findings.
- **2026-05-19** Triple-distillation concept page +
  pedro-ximenez-sherry-butt cask + confidence-level review.
  (a) `concept/practice/triple-distillation` written —
  documents the three-still regime (wash -> low-wines ->
  spirit), the strong/weak fraction splits, the strength
  consequence (double ~68-72% ABV vs triple approaching
  90% ABV), the lowland / Irish-practice distribution.
  Grounded against Nicol Ch 9 p 173 (Russell ed. 2014)
  plus the Auchentoshan producer page. Cross-referenced
  from the Auchentoshan and Springbank `distinctive_features`
  lists (Auchentoshan: full triple; Springbank: the Hazelburn
  line only). (b) `data/casks/pedro-ximenez-sherry-butt.yml`
  created — PX is the sweetest Jerez style (raisined grapes,
  ~400-500 g/L residual sugar); the Auchentoshan Three Wood
  third maturation stage updated from the prior
  `oloroso-sherry-butt` hedge to reference the new
  `pedro-ximenez-sherry-butt` slug; oloroso and fino
  `related.alternatives` updated to list it. (c) Confidence-
  level review on the 14 Russell-grounded concept entries:
  **conclusion — no promotions.** Single-source glossary
  entries stay `medium` (high requires multi-source); the
  multi-source educational pages stay `medium` because each
  carries documented contested-claim sections. The single
  blocker to several medium -> high promotions is a second
  peer-reviewed academic source; a literature-resource
  scouting item was added to §Research requests so the user
  can prioritise which works to supply (Piggott et al. 1989
  the highest-value acquisition). Bibliography cross-check:
  no Russell citations outside the 14 concept entries; no
  "page refs TBA" hedges remain anywhere in data/. Counts:
  133 -> 135 files, 16 -> 17 casks, 46 -> 47 concepts,
  537 -> 547 resolved refs, 21 dangling unchanged, 0 schema
  findings. Edit-tool NUL corruption / truncation hit
  auchentoshan.yml, auchentoshan-three-wood.yml,
  oloroso-sherry-butt.yml, springbank.yml during the wave;
  all repaired (NUL-strip + git-restore-and-re-apply).
- **2026-05-19** Russell ed. 2014 grounding pass — 14 concept-entry
  citations migrated from the "page references to be added when
  consulted" hedge to specific chapter-author + page-range
  citations against the 2nd edition (ISBN 978-0-12-401735-1).
  User uploaded a digital copy; the project's TOC extraction
  established the 6 chapter ranges covering the 14 entries.
  Chapters: Bringhurst & Brosnan Ch 6 (pp 49-121, "Scotch
  whisky: raw material selection and processing", 4 entries:
  kiln / mashing / floor-malting / external-malting) — Russell &
  Stewart Ch 7 (pp 123-145, "Distilling yeast and fermentation",
  2 entries: distillers-yeast / fermentation) + Wilson Ch 8
  (pp 147-154, "Contamination", cross-ref from fermentation) —
  Nicol Ch 9 (pp 155-177, "Batch distillation", 4 entries:
  direct-fired-still / reflux / shell-and-tube / wash-still) —
  Conner Ch 11 (pp 199-219, "Maturation", 2 entries:
  cask-fill-states / cask-maturation-kinetics) — Aylott Ch 14
  (pp 243-269, "Whisky analysis") + Mitchell Ch 18 (pp 315-326,
  "Whisky global packaging developments", 2 entries:
  chill-filtering / scotch-presentation-conventions). Each
  entry's citation block now names the chapter author rather
  than just the editor, includes the chapter page range, and
  carries a subsection-level notes block pointing at the
  specific pages for the claim (e.g. mashing temperature
  63.5-64 °C at p 88; kilning temperature 72 °C at p 58; cask
  rejuvenation at p 224; LAB secondary-fermentation pathway
  at pp 149-151). docs/bibliography.md updated to (a) include
  both editions' ISBNs and the correct multi-editor team for
  each edition and (b) reorganise the Cited-by list by
  chapter. Pre-existing edition note kept (1st edition 2003;
  2nd edition 2014). Counts: 133 files unchanged; 537 resolved
  refs unchanged; 0 schema findings. Verification clean.
- **2026-05-18** Laphroaig (12th distillery, third south-Islay
  heavily-peated). 1 distillery + 1 production line + 2
  bottlings + 1 concept-page cross-ref update. Completes the
  south-Islay "Kildalton" heavily-peated cluster minus Ardbeg.
  South-coast Islay, Suntory Global Spirits-owned, founded
  1815 (Donald & Alexander Johnston). Notable structural
  features: **asymmetric 3-wash + 4-spirit-still
  configuration**, unusually tall ascending lyne arms,
  producer-disclosed late spirit cuts (45 / 60 minutes — the
  late first cut is producer-claimed as the industry's
  latest), 63.5% ABV cask-fill strength, predominantly
  ex-bourbon maturation from Maker's Mark in Kentucky (an
  internal-supply-chain relationship within the Suntory
  Global Spirits portfolio). **Two-stream malt supply**:
  ~20% on-site floor-malted at 50-60 ppm + ~80% Simpsons
  Malt commercial supply at 45 ppm, blended into the mash —
  the first populated production line exercising the
  two-stream malt pattern, requiring two `peating.measurements`
  entries with different `stage: malt_delivered` values.
  Royal Warrant from HRH The Prince of Wales (now King
  Charles III) since 1994. Bottlings: 10 Year Old (40%
  chill-filtered flagship core) + Quarter Cask (48% NCF
  natural-colour, **first populated bottling exercising
  small-cask / firkin maturation** as a structural feature
  — ~7-month secondary in ~125 L quarter casks accelerates
  wood-derived extraction kinetics via higher
  surface-area-to-volume ratio). Concept-page update:
  `practice/floor-malting` `adopted_by:` list populated with
  springbank / highland-park / laphroaig (previously empty).
  Schema findings cleaned: production_line compounds
  `total_phenols` → `unspecified` (enum). A truncation
  repair was applied to `floor-malting.yml` — Edit-tool
  trailing drop hit the file mid-source-notes; restored
  via bash heredoc per safe-bulk-writes pattern. Counts:
  129 → 133 files, 11 → 12 distilleries, 16 → 17 production
  lines, 35 → 37 bottlings, 518 → 537 resolved refs,
  21 dangling (unchanged), 0 schema findings.
- **2026-05-18** Auchentoshan (11th distillery, second Lowland,
  triple-distilled). 1 distillery + 1 production line + 2
  bottlings. **First populated `distillation.regime: triple`** as
  a distillery's default — the Hazelburn line at Springbank is
  triple-distilled but coexists with double / 2.5x lines at that
  site, so Auchentoshan is the only Scottish distillery where
  every drop is triple-distilled. Direct pair-test for
  Glenkinchie under the same Lowlands regional designation
  (triple vs double, double-cask vs ex-bourbon-only, single-
  malt-led vs blend-supply-led). Dalmuir / Clydebank,
  Suntory Global Spirits, founded 1817 (Bulloch as Duntocher),
  licensed 1823, renamed 1834 (Hart & Filshie). 1941-1948
  wartime mothballing from German bomb damage during the Clyde
  shipyard raids. Producer-disclosed equipment: 3 pot stills
  (wash 17,500 L + intermediate 8,200 L + spirit 11,500 L);
  spirit cut runs to 81% ABV per producer disclosure. Default
  unpeated. Bottlings: 12 Year Old (40% double cask bourbon +
  oloroso) + Three Wood (43% NAS, bourbon → oloroso → PX
  three-cask sequence, **first populated bottling exercising
  a three-stage primary maturation sequence**). Sources:
  auchentoshan.com (history + process), scotchwhisky.com
  Whiskypedia, whisky.com trade database, SWR2009 reg. 10
  for the Lowlands grounding. Counts: 125 → 129 files,
  10 → 11 distilleries, 15 → 16 production lines, 33 → 35
  bottlings, 501 → 518 resolved refs, 21 dangling (no change),
  0 schema findings.
- **2026-05-18** Glenkinchie (10th distillery, first Lowland) +
  ConfidenceBadge popover + 10 cask sourcing migrations. Three
  workstreams in one pass. (a) `<ConfidenceBadge>` component
  added at `site/src/components/ConfidenceBadge.astro` with
  accessible popover (button + ARIA aria-expanded/aria-controls,
  Tab-focus / Enter-Space / Escape / click-outside semantics).
  Per-level rubric (high / medium / low / stub) is the
  single source of truth in the component; popover links to
  `/reference/source-policy/`. Wired into EntityHeader,
  distilleries/index, and production-lines/index. (b) 10 cask
  entries migrated from institutional homepages to specific
  document URLs: 7 INAO product pages (Pauillac, Pomerol,
  Sauternes, Bourgogne regional, Côtes du Rhône node/237,
  Ventoux, Bandol), 1 MIPAAF catalogo-viti entry (Amarone della
  Valpolicella DOCG), 2 Consejo Regulador Pliego de Condiciones
  PDF (oloroso, fino — same consolidated 2024 file). Hedge
  "specific URL should be verified when accessed" replaced with
  positive claim where applicable; access dates updated to
  2026-05-18. (c) **Glenkinchie populated as the 10th
  distillery** — East Lothian / Pencaitland, Diageo-owned,
  founded 1825 (Milton) / 1837 (Glenkinchie), 1853-1881 sawmill
  conversion mothballing as a single 28-year gap, SMD →
  DCL → United Distillers → Diageo lineage, original 1988
  Classic Malts member, 2020 "Lowland Home of Johnnie Walker"
  brand-home redevelopment. **First populated Lowland-region
  distillery** under SWA Regulations 2009. **First populated
  distillery with `condenser: worm_tub`** — the
  `equipment/worm-tub` concept page's used_at_distilleries
  forward ref to Glenkinchie now resolves. 1 production line
  (unpeated, double-distilled, `peat_origin: none`) + 2
  bottlings (12 Year Old flagship + Distillers Edition
  Amontillado finish — third populated DE after Lagavulin /
  Caol Ila, exercising the third secondary-cask style in the
  cross-distillery DE pattern). Critical-eval fixes applied:
  fabricated "Major-Bell" syndicate name removed (not in
  sources), DCL Lowland-rationalisation dates corrected
  (St Magdalene 1983, Inverleven 1991, Rosebank 1993),
  unsourced editorial about Bladnoch comparison removed,
  coordinates-source claim honestly hedged, 2007 transition
  year for 12 Year Old softened (not pinned to a primary
  source). Schema-validator findings cleaned: region
  "Lowland" → "Lowlands", washbacks material "wood" →
  "larch" (dominant of the mixed Oregon-pine + Canadian-larch
  construction), DE availability "annual_recurring" → "core".
  Counts: 121 → 125 files, 9 → 10 distilleries, 14 → 15
  production lines, 31 → 33 bottlings, 485 → 501 resolved refs.
  Dangling 22 → 21 (the worm-tub forward ref to Glenkinchie
  resolved, leaving the 21 distillery forward refs the worm-tub
  page still carries to unpopulated distilleries). 0 schema
  findings.
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
  implementation sequencing: concept pages first, then other
  entity types, then search and map (both landed 2026-05-18 —
  see top of Recently completed).
