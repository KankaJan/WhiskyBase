# Handover

This document is written for a future Claude instance (in Claude Code,
Cowork, or a fresh chat) picking up the WhiskyBase project, or for a
new human contributor doing the same. It is a structured briefing on
*why* the project is shaped the way it is — the design decisions are
load-bearing and not always self-evident from the data alone.

Read this once; refer back when in doubt.

---

## 1. The project in one paragraph

WhiskyBase is a structured, queryable, fact-grounded reference for
Scotch whisky production. It is organised around three durable entity
types — **distillery** (physical production site), **production line**
(a specific recipe produced at a distillery), and **bottling** (a
specific commercial release) — plus a **concept** layer for reference
content (methodology, educational, equipment, practice, glossary).
Two additional top-level entity types extend the model: **bottler**
for commercial bottling entities (independent bottlers, distillery
bottling operations) — schema at v0.2 with 2 entries populated
(Cadenhead's, Signatory Vintage); and **cask** for reusable cask-
type references that bottlings and production lines cite from their
maturation programmes — schema v0.1 with 18 entries populated,
including the first-class `undisclosed-cask` for deliberately-
secret cask provenance. Data lives as YAML in a
Git repository; cross-references between entities use slugs; the
build pipeline (not yet implemented) will turn the data into a static
site.

---

## 2. Why three entity types, not one

Earlier drafts had a single "whisky" entity that conflated distillery,
recipe, and release. This collapsed under the first real data: one
distillery may produce multiple distinct recipes (Bruichladdich runs
three lines — Bruichladdich unpeated, Port Charlotte at 40 ppm,
Octomore at 80+ ppm — on the same equipment), and one recipe produces
many bottlings (Octomore alone has dozens). Forcing this into one
entity meant duplicating equipment specs across every release and
losing the distinction between "how the spirit was made" and "how
this bottle was finished and presented."

The three-entity split is the minimum that captures the production
hierarchy without forcing the data into shapes that don't fit.

---

## 3. Why the peating schema is the way it is

The single most important schema decision in the project is how PPM
(peating phenol concentration) is recorded. Here is why it matters
and how it works.

**PPM is not a single number.** A figure reported as "40 ppm" depends
on (a) what stage of production was measured — kilned malt, new make
spirit, or bottled liquid — (b) what analytical method was used — HPLC,
4-aminoantipyrine colorimetry, GC-MS, Folin-Ciocalteu — and (c) which
compounds were summed. Different combinations of these produce
different numbers for the same physical sample.

**The producer occasionally tells us.** Bruichladdich's 2017 release
of Octomore 8.3 included an explicit producer statement: "Using HPLC
(high performance liquid chromatography), the readings came back at
309.1 ppm... the ppm level can vary depending on whether a colorimetric
reading or one from HPLC is taken, the latter producing higher
figures." This is the only level of methodological detail we
routinely get, and the schema is designed around capturing it
honestly.

**The schema's `peating` block on production_line entries.** It looks
like this:

```yaml
peating:
  measurements:
    - stage: spec              # spec | malt_delivered | new_make | in_bottle
      value: 40                # or [min, max] for a disclosed range
      unit: ppm
      method: hplc             # hplc | 4_aminoantipyrine | gc_ms | folin_ciocalteu | unspecified
      compounds: standard_7    # standard_7 | extended | individual | unspecified
      source_id: 1
      notes: |
        ...
```

`standard_7` is the seven-compound HPLC sum that has become the
industry default (phenol, three cresols, guaiacol, 4-methylguaiacol,
4-ethylguaiacol).

**Source-level methodology declaration.** To avoid repeating method
information on every measurement, sources can carry a methodology
block:

```yaml
sources:
  - id: 1
    type: official_website
    url: https://...
    methodology:
      peating_ppm:
        method: hplc
        compounds: standard_7
        basis_concept: methodology/bruichladdich-published-ppm
        notes: |
          Bruichladdich's published PPM uses HPLC and the standard 7
          phenolic compounds. Field-level measurements resolve method
          via this declaration rather than restating per-figure.
```

When a measurement cites `source_id: 1`, it inherits the source's
methodology unless overridden. This kept the data clean while
preserving full traceability — we don't write `method: hplc,
compounds: standard_7` on every Bruichladdich measurement.

**The `unspecified` enum value is a positive claim, not a default.**
Use it when a source genuinely does not disclose method. Many older
trade-press citations end up classified this way when traced back.

**The educational concept page.** `concept/educational/peating-measurement-methods`
explains all of this in human-readable form for site visitors.
Methodology concept pages (e.g. `methodology/bruichladdich-published-ppm`)
attest *who* uses *which* method. The two layers serve different
audiences — machines and humans — and the redundancy is intentional.

---

## 4. Voice register

Two registers, both rejecting marketing language.

**Strict reference register** for distillery / production_line /
bottling descriptions. Disallowed words (extend as needed):
celebrated, renowned, iconic, legendary, beloved, rugged, wild,
windswept, ancient, philosophy, ethos, passion, journey, soul,
heart, masterpiece, gem, jewel, hidden, secret.

Discipline test for reference register: strip every adjective. Do
the facts still stand? If yes, the description is doing its job.

**Technical-teaching register** for educational concept pages. Same
disallowed-words list, but plain instructive sentences are permitted:
"Phenols deposit on the husk during kilning, then partition into the
wort during mashing." Discipline test for teaching register: strip
every claim that isn't either definitional or sourced. Does what
remains still teach?

Length follows topic depth, not topic importance. Worm tubs warrant
~1500 words; a glossary term for "wash" gets one sentence.
Pre-publication check on every educational page: "What does this
page do that a Wikipedia article doesn't?" If the answer is nothing,
the page should not exist yet.

Full rules in `docs/voice-register.md`.

---

## 5. Source conflicts

Treat source disagreement as data, not noise. The rules:

1. **Resolve to one figure in the entry.** Pick the most reliable
   source given the type of claim and document the choice in an
   inline comment.
2. **Preserve the conflict in `<entity>.NOTES.md`.** The notes file
   sits beside the entry (`bruichladdich.NOTES.md` next to
   `bruichladdich.yml`) and records what disagreed, why we chose
   what we chose, and what would change our mind.
3. **Never silently round, average, or smooth across sources.**
   If two sources give 17,500 L and 12,500 L for a still capacity,
   the entry records one of those figures, not 15,000 L.

**Wikipedia volatility (added 2026-05-15).** Wikipedia is treated
as a volatile source: entries change without notification, and
their citation graphs evolve as editors come and go. Wikipedia is
demoted from tier 2 to tier 3 in the source reliability hierarchy.
Primary databases are preferred where available: PubChem
(`chemistry_database` type) for compound chemistry, ecfr.gov
(`regulatory_text` type) for US distilled-spirits regulation,
INAO regulatory text for French wine appellations, Consejo
Regulador for sherry. Wikipedia citations are acceptable for
historical facts and non-load-bearing context but flagged for
upgrade in the Research Requests section of `TODO.md` where a
primary source exists. See `docs/source-conflict-policy.md` for
the full policy and source-type vocabulary.

Real examples in the existing data:

- Bruichladdich wash still capacity: Diffords says 12,500 L; Wikipedia
  says 11,500 L; Scotch Whisky structured says 17,500 L (size) with
  11,500 L (charge). Resolved to Scotch Whisky's figures because they
  are the only set internally consistent across size-vs-charge axes.
  Documented in `bruichladdich.NOTES.md`.
- Harris washback count: 5 in some sources, 8 in others. Resolved
  to 5 (Scotch Whisky Whiskypedia plus an independent visit account);
  the 8-figure remains in two secondary sources but is not adopted.
  Documented in `harris.NOTES.md`.
- Octomore 8.2 ABV: 58.4% per producer-aligned sources; 58.7% per one
  outlier (The Whisky Club). Resolved to 58.4% with the outlier
  flagged in the entry's source notes.

Full rules in `docs/source-conflict-policy.md`.

---

## 6. Slug conventions

- Lowercase, hyphenated.
- Distilleries: just the name (`bruichladdich`, `harris`).
- Production lines: `<distillery>-<descriptor>` (`bruichladdich-port-charlotte`,
  `harris-the-hearach`).
- Bottlings: for OBs, `<distillery>-<release-name>`
  (`bruichladdich-octomore-8-3`). For IBs (planned),
  `<bottler>-<distillery>-<descriptor>` (`cadenheads-bruichladdich-2004-20yo`).
- Bottlers: just the name (`cadenheads`, `signatory-vintage`).
- Concepts: `<kind>/<slug>` form for structured references
  (`methodology/bruichladdich-published-ppm` in `related_concepts` or
  `basis_concept` fields); the file lives at
  `/data/concepts/<kind>/<slug>.yml`. Markdown body links use the
  URL-friendly variant `concept/<kind>/<slug>` (which the build
  pipeline will rewrite to site URLs).
- Casks: bare slug, lowercase-hyphenated, descriptive
  (`bourbon-barrel`, `pomerol-wine-cask`, `undisclosed-cask`). Bare
  form matches the convention for other top-level entity types;
  concept-style kind prefixing is reserved for `/data/concepts/`
  entries. Naming conventions: `<prior-contents>-<vessel>` for
  named-provenance casks; `<category>-<vessel>` for generic types;
  `<feature>-<vessel>` for special cases (`virgin-oak`,
  `undisclosed-cask`).

**Why concept slugs use `<kind>/<slug>` namespacing.** If we later
split `/data/concepts/<kind>/` into `/data/methodologies/`,
`/data/equipment/`, etc., file paths change but public slugs stay
stable. Cross-references survive the refactor.

---

## 7. Independent bottlers

Bottlings v0.2 schema discriminates at the bottling level:

```yaml
produced_at_distillery: bruichladdich   # where the spirit was distilled
bottled_by: cadenheads                  # who bottled it
bottler_type: independent_bottler       # distillery | independent_bottler
bottler_series: cadenheads/authentic-collection   # optional series slug
```

For official bottlings (OBs), `bottled_by` equals (or is the
commercial arm of) `produced_at_distillery`, and `bottler_type:
distillery`. For independent bottlings (IBs), `bottled_by` references
a bottler entity under `/data/bottlers/`, and `bottler_type:
independent_bottler`.

**The schema makes IB and OB filterable without joining tables.**
"Show me all IB Bruichladdich" is a query over `produced_at_distillery:
bruichladdich AND bottler_type: independent_bottler`. No lookup
required to find out what kind of entity the bottler is.

**Comparison emerges from filtering, not from schema opinion.** The
schema does not flag IB vs OB pairs as "comparable" or otherwise; the
build pipeline (eventually) supports filtering, and readers decide
what they want to compare.

Bottler entity schema is drafted at **v0.1 (stub)** at
`schema/bottler.template.yml`. `/data/bottlers/` is still empty; the
schema's series modelling in particular is speculative and will firm
up once the first real IB release is populated (likely a Cadenhead's
or Signatory bottling). The next schema-work priority is pressure-
testing the stub against a real case and promoting to v0.2.

---

## 8. Forward references

Cross-references to concepts or casks that don't exist yet are common
and expected. The convention:

- The build pipeline **warns**, does not fail, on dangling references.
- Inline markdown links to missing concepts render as plain text with
  a tooltip ("concept page not yet written").
- Structured field references to missing concepts render as the slug
  in monospace with the same tooltip.

This lets data authoring run ahead of concept-page authoring without
breaking site builds. The warning output is the working list of
"concept pages that need writing."

`scripts/check_references.py` is the current implementation of this
warn-not-fail check (since the build pipeline is still deferred).
Run it from the repo root to surface dangling references, duplicate
IDs, invalid `source_id` references, and inline `[N]` citations
that don't match an entry's declared sources. The script's output
is informational — it never blocks commit.

---

## 9. What is out of scope

Decided explicitly, not yet:

- Tasting tours, visitor centres, gift shops.
- Awards, medals, scoring sites.
- Current secondary-market prices (RRP at release is permanent
  reference data and is captured; auction values are not).
- "Philosophy", "story", "ethos", "passion" — marketing-tier content.
- Recommendations to readers about what to buy or drink.

If a request feels like it falls into one of these categories, push
back rather than absorbing it into the data model.

---

## 10. Current state and immediate priorities

**Populated:**

- 20 distilleries: Harris (confidence: medium), Bruichladdich (high),
  Springbank (medium — drove the distillery v0.1 → v0.2 promotion
  for multi-warehouse support), Glenmorangie (medium — Highland-
  region single-line, LVMH ownership, first use of `still.height_m`
  as load-bearing data), Lagavulin (medium — heavily peated Islay,
  Diageo ownership, resolves the `glossary/classic-malts`
  reference target as one of the original six Classic Malts),
  Highland Park (medium — Orkney site, Edrington ownership, first
  populated distillery with `region: Islands` informal-trade
  designation per `educational/swa-regional-designations`; first
  distillery with `distinctive_features: [practice/floor-malting]`
  cross-reference as a populated distillery practitioner of partial
  on-site floor malting), Bunnahabhain (medium — north-east Islay,
  Distell/Heineken ownership, lightly-peated default production
  contrasting with the heavily-peated south-Islay cluster; five-
  stage ownership history exercises the
  `ownership.history` field densely; **resolved the 2 forward refs
  from cadenheads-bunnahabhain-stub**), Glenfarclas (medium —
  Speyside, **first populated distillery in the formal SWA
  Speyside region**; J. & G. Grant family-owned in unbroken
  succession since 1865; **first populated distillery exercising
  `heating: direct_fire` schema enum value** — all six pot stills
  direct-fired, contrasting with the `indirect_steam` default used
  by the prior seven populated distilleries),
  Caol Ila (medium — east-coast Islay, Diageo-owned, founded 1846;
  one of Islay's largest distilleries by capacity with the
  majority of output historically going to Diageo blends; **resolved
  the 2 remaining IB-stub forward refs** from
  signatory-caol-ila-stub; introduced the Distillers Edition
  cross-distillery series pattern across a second populated
  distillery — Lagavulin DE was the first),
  Glenkinchie (medium — East Lothian, Diageo-owned, founded 1825 by
  the Rate brothers as the Milton Distillery and licensed under the
  Glenkinchie name 1837; **first populated Lowland-region
  distillery in the data set**, exercising the formal SWA Lowlands
  designation under the Scotch Whisky Regulations 2009; **first
  populated distillery with `condenser: worm_tub`** — a single
  cast-iron worm tub cools both stills, the producer-attributed
  "largest wash still in the industry" at a published 30,963 L
  capacity; 1853-1881 sawmill-conversion mothballing exercises an
  unusually long single mothballed period; resolves the
  forward ref from `equipment/worm-tub` to Glenkinchie. Diageo's
  "Lowland Home of Johnnie Walker" since the 2020 £185M
  brand-home redevelopment),
  Auchentoshan (medium — Dalmuir / Clydebank, Suntory Global Spirits-
  owned, founded 1817 by John Bulloch as the Duntocher Distillery and
  licensed under the Auchentoshan name 1823; **first populated
  distillery with `distillation.regime: triple` as the default**
  and the **only Scottish distillery whose entire output is
  triple-distilled** (the Hazelburn line at Springbank is
  triple-distilled but coexists with double and 2.5x lines at
  that site); second populated Lowland-region distillery,
  pair-comparable with Glenkinchie on regime (triple vs double),
  cask programme (double-cask sherry vs ex-bourbon-only) and
  output direction (single-malt-led vs blend-supply-led);
  1941-1948 wartime mothballing from German bomb damage during
  the Clyde shipyard raids),
  Laphroaig (medium — south-coast Islay, Suntory Global Spirits-
  owned, founded 1815 by the Johnston brothers; third populated
  south-Islay heavily-peated entry alongside Lagavulin and
  Caol Ila — completes the "Kildalton" cluster minus Ardbeg;
  **asymmetric 3-wash + 4-spirit-still configuration** with
  unusually tall ascending lyne arms; **two-stream malt supply**
  blending ~20% on-site floor-malted barley (50-60 ppm) with
  ~80% Simpsons Malt commercial supply (45 ppm) — second
  populated floor-malting practitioner after Highland Park;
  internal supply chain disclosed for cask supply: ex-bourbon
  casks from sister Suntory Global Spirits site Maker's Mark in
  Kentucky; Royal Warrant from HRH The Prince of Wales / King
  Charles III since 1994),
  Glenfiddich (medium — Dufftown, Speyside, William Grant & Sons,
  founded 1886 / first spirit 1887; second populated Speyside
  distillery; **the distillery most associated with the creation
  of the modern marketed single-malt category** — the 1963
  decision to actively market single malt outside Scotland;
  unbroken family ownership since founding, a structural parallel
  to the unrelated-Grant-family Glenfarclas; very large scale
  (~21M LPA, 43 stills as 16 wash + 27 spirit, 15 spirit stills
  partly direct-fired; 48 Douglas-fir washbacks); the 1998
  Solera Vat — a continuous-marrying vatting vessel — underpins
  the 15 Year Old),
  Ardbeg (medium — Port Ellen, south-coast Islay; the fourth and
  final south-Islay heavily-peated entry, completing the
  "Kildalton" cluster with Laphroaig, Lagavulin and Caol Ila;
  founded 1815, mothballed 1981 and rescued by Glenmorangie plc
  in 1997, now LVMH / Moet Hennessy; a purifier on the
  spirit-still lyne arm — uncommon on Islay — is the distinctive
  equipment feature; ~50 ppm peating; the 2019 still house
  doubled the still count from one pair to two, with the
  post-expansion annual capacity left null pending a producer
  figure, see ardbeg.NOTES.md),
  Macallan (medium — Easter Elchies, Craigellachie, Speyside,
  Edrington-owned via The Robertson Trust charitable structure;
  founded 1824 by Alexander Reid under the Excise Act 1823;
  third populated Speyside entry after Glenfarclas and
  Glenfiddich; **defining sherry-cask-led house style** — the
  Sherry Oak core range matured exclusively in oloroso-seasoned
  oak sherry casks from Jerez, the 2004 Fine Oak range (renamed
  Triple Cask Matured in 2018) added American-oak ex-bourbon
  casks alongside; Edrington's September 2023 acquisition of
  the Vasyma cooperage in Jerez vertically integrated the
  sherry-cask supply chain; new 2018 still house (Rogers Stirk
  Harbour + Partners, £140m) holds 36 stills as 12 wash + 24
  spirit, with the spirit stills at 3,900 L charge volume —
  among the smallest in Scotland and a long-standing piece of
  the brand's positioning; ~15M LPA; **Wikipedia is the only
  directly-fetched source** in the entry, the producer's own
  pages and scotchwhisky.com Whiskypedia did not return content
  at fetch time and are queued for migration in
  `TODO.md` Research Requests),
  Glenlivet (medium — Minmore, Ballindalloch, Speyside (Moray),
  Chivas Brothers / Pernod Ricard; founded 1824 by George Smith,
  the first licensed distiller in the glen under the Excise Act
  1823; fourth populated Speyside entry and the other half of the
  Glenfiddich-vs-Glenlivet best-seller pair (biggest single malt in
  the US, second globally after Glenfiddich); **light, floral,
  fruity house style on tall lantern-shaped stills**, the deliberate
  contrast to Macallan's short-still sherry weight; the 1881/1884
  "Glenlivet" name legal case secured "The Glenlivet" as the sole
  unhyphenated user; a 2024 bicentenary stillhouse doubled capacity
  to ~21M LPA across 28 stills; **two directly-fetched sources**
  (Wikipedia + a 2024 trade-press report) with the capacity / still-
  count conflict resolved in `glenlivet.NOTES.md`),
  Talisker (medium — Carbost, Isle of Skye; Diageo, one of the six
  Classic Malts; the project's first Skye entry and third populated
  Classic Malt after Lagavulin and Glenkinchie; founded 1830 by the
  MacAskill brothers; **medium-peated (~18-22 ppm) peppery maritime
  house style**; distinctive equipment — an asymmetric five-still set
  (2 wash + 3 spirit) with U-shaped lye-pipe purifier loops and
  **worm-tub condensers on all five stills**, resolving the
  equipment/worm-tub forward ref; ~3.5M LPA; bottlings 10 Year Old
  (45.8% flagship), Distillers Edition (amoroso finish) and Storm (NAS);
  Wikipedia-primary with bottling specs from specialist-retailer
  listings, see talisker.NOTES.md),
  Cameronbridge (medium — Cameron Bridge, Fife, Lowlands; Diageo; the
  project's **first grain distillery** and first Lowland grain. Founded
  1824 by John Haig; a founding DCL grain distillery (1877). **Continuous
  (column / Coffey) distillation** from a wheat-led cereal bill, not batch
  pot stills — the first `regime: continuous` line; ~136M LPA, one of
  Europe's largest. Single-grain bottlings Cameron Brig and the Haig Club
  range. The malt-centric schema does not yet structure column stills or
  the cereal bill — captured in prose, with SCHEMA-OBSERVATIONS in
  cameronbridge.NOTES.md for structuring at the second grain distillery.
  Schema change: additive `distillation.regime: continuous`, CHANGELOG
  [0.8.6]),
  North British (medium — Gorgie, Edinburgh, Lowlands; the project's
  **second grain distillery** and the confirming example for the
  grain-schema structuring. Founded 1885 by the blenders Usher, Sanderson
  and Crabbie to break the DCL grain monopoly; now owned **50:50 by Diageo
  and Edrington** (Lothian Distillers JV) — the first co-ownership in the
  data set. Continuous Coffey-still distillation to ~94.5% ABV from a
  **maize-led** bill (85% maize / 15% malted barley), the contrast to
  Cameronbridge's wheat that justified the structured `cereal_bill` field;
  ~65M LPA. A pure blending-grain supplier — no own single-grain bottling
  (`bottlings: []`), the first such entry; single grains reach market via
  IBs. Schema: `stills.column_stills` + `cereal_bill` added and
  Cameronbridge retrofitted, CHANGELOG [0.8.7]),
  Aberlour (medium — Charlestown of Aberlour, Speyside (Moray); Pernod
  Ricard / Chivas; founded 1879 by James Fleming. Fifth populated Speyside
  and the second sherry-led Chivas malt (with Glenlivet). Sherry-influenced
  **double-cask house style** (ex-bourbon + oloroso); ~3.9M LPA on 2 wash +
  2 spirit stills (the spirit pair differing in size, 20,000 / 15,456 L).
  Bottlings: A'bunadh (cask-strength first-fill oloroso, NCF, natural
  colour, NAS — `abv` null as it is batch-variable), 12 and 16 Double Cask
  Matured. Water-source conflict (St Drostan's Well vs Wikipedia's
  Birkenbush / Target spring) noted in aberlour.NOTES.md).
- 25 production lines: 3 Bruichladdich (high), 1 Harris (medium),
  3 Springbank (medium — Springbank 2.5×, Longrow double, Hazelburn
  triple), 1 Glenmorangie (medium — main line; Signet/Allta
  deferred), 1 Lagavulin (medium — heavily-peated Islay single
  line), 1 Highland Park (medium — moderately peated heather-
  peat single line, sherry-cask-heavy maturation programme),
  2 Bunnahabhain (medium — lightly-peated `bunnahabhain-traditional`
  default at 1-2 ppm spec + peated `bunnahabhain-toiteach` sub-line
  at 35-40 ppm spec, exercising multi-line modelling at smaller
  scale than Springbank),
  1 Glenfarclas (medium — single line, unpeated Speyside, sherry-
  cask-led house style, direct-fired distillation throughout),
  1 Caol Ila (medium — heavily-peated Islay default at 30-35 ppm
  spec; Port Ellen Maltings supply chain shared with Lagavulin),
  1 Glenkinchie (medium — unpeated Lowland default; the project's
  first `peat_origin: none` worm-tub production line and the
  ~90% blend-supply / 10% single-malt split that anchors the
  Johnnie Walker Lowland component),
  1 Auchentoshan (medium — unpeated Lowland default with
  `regime: triple` and producer-disclosed third-pass spirit
  strength of 81% ABV; the project's first `regime: triple`
  default line; single-malt-led output direction),
  1 Laphroaig (medium — heavily-peated south-Islay default
  with two-stream malt supply: 20% on-site floor-malted at
  50-60 ppm + 80% Simpsons commercial supply at 45 ppm,
  blended into the mash; producer-disclosed late spirit cuts
  at 45 / 60 minutes; 63.5% ABV fill strength; predominantly
  Maker's Mark ex-bourbon maturation through the
  Suntory Global Spirits internal supply chain),
  1 Glenfiddich (medium — unpeated Speyside default at very
  large scale; ~74-hour fermentation in 48 Douglas-fir
  washbacks; the core 12 / 14 / 15 / 18 / 21 expressions are
  one production line routed through different cask and
  Solera-Vat vatting processes, not separate recipes),
  1 Ardbeg (medium — heavily-peated Islay default; long
  fermentation; the spirit-still purifier),
  1 Macallan (medium — unpeated Speyside default; sherry-cask-
  led cask programme as the defining feature, with the 2004
  Fine Oak / 2018 Triple Cask Matured range as the only
  ex-bourbon component in the core Macallan range; the
  producer-stated "curiously small" spirit stills at 3,900 L
  charge volume),
  1 Glenlivet (medium — unpeated, light Speyside default on tall
  lantern-shaped stills with long necks (high reflux); American-oak
  ex-bourbon-led core, with a European-oak sherry component in the
  12 Year Old, selective new French/Limousin oak in the 15 French
  Oak Reserve, and first-fill oloroso at cask strength in the
  Nàdurra Oloroso; malt bought in from Crisp at Portgordon),
  1 Talisker (medium — medium-peated Skye default ~18-22 ppm; the
  asymmetric five-still set with U-shaped purifiers and worm tubs;
  American-oak-led core with an amoroso-sherry route in the Distillers
  Edition; malt bought in from a mainland Diageo maltings),
  1 Cameronbridge (medium — the project's first grain line:
  `regime: continuous` column/Coffey distillation from a wheat-led
  cereal bill; unpeated; American-oak maturation; high-strength grain
  new make),
  1 North British (medium — second grain line: `regime: continuous`
  Coffey distillation to ~94.5% ABV from a maize-led `cereal_bill` (85%
  maize / 15% malted barley); unpeated; no own bottlings),
  1 Aberlour (medium — unpeated Speyside default; double-cask programme
  ex-bourbon + oloroso, plus first-fill oloroso for A'bunadh).
- 85 concept pages: 3 methodology, 17 educational, 8 equipment,
  5 practice, 52 glossary. The 2026-05-21 production-chain
  coverage build added 34 pages across three tiers; a master
  overview (`whisky-production`) and three stage wrappers
  (`malting`, `mashing`, `fermentation`) were then added to
  complete the wrapper layer, so every production stage has one
  overview page. Together these complete the technical backbone (distillation, malting, mashing,
  fermentation, maturation, blending, and the supporting
  glossary terms). See the TODO "production-chain coverage
  queue" and the per-kind concept sub-indexes for the full list.
- 2 suppliers: Bairds Malt Ltd
  (`data/suppliers/bairds-malt.yml`, populated 2026-05-17 against
  supplier v0.1 as the first pressure-test, type=maltster) and
  Heaven Hill Distilleries Inc.
  (`data/suppliers/heaven-hill.yml`, populated 2026-05-17 as the
  second pressure-test, type=cooperage_source — exercising the
  second branch of the supplier type enum). Multi-site shape
  exercised across both entries. SCHEMA-GAPS / SCHEMA-OBSERVATIONS
  blocks in both entries document the v0.1 schema as adequate for
  current data; no v0.2 promotion driven. The supplier schema
  has covered 2 of 5 enum branches; further pressure-tests (yeast
  supplier, barley breeder) deferred. All previously-tracked concept dangling references
  now resolve; only the 20 worm-tub `used_at_distilleries` forward
  refs remain (expected per §8), plus 2 forward refs from the
  Cadenhead's IB pressure-test stub (`bunnahabhain` distillery and
  its `bunnahabhain-traditional` production_line — not yet
  populated).
- 2 bottlers: Cadenhead's (`data/bottlers/cadenheads.yml`,
  confidence medium, populated 2026-05-15 against bottler v0.1)
  and Signatory Vintage (`data/bottlers/signatory.yml`,
  confidence medium, populated 2026-05-15 against bottler v0.2).
  The Signatory pressure-test confirmed the hypothesis from the
  Cadenhead's SCHEMA-GAPS block and drove the bottler v0.2
  promotion (presentation_defaults and parent fields). Cadenhead's
  entry was bumped to schema v0.2 but does not use the new
  features (its series have less formal presentation
  enforcement).
- 57 bottlings: 57 working entries (10 Bruichladdich/Harris + 3
  Springbank + 3 Glenmorangie + 3 Lagavulin + 3 Highland Park +
  2 Bunnahabhain + 3 Glenfarclas + 2 Caol Ila + 2 Glenkinchie +
  2 Auchentoshan + 2 Laphroaig + 2 Glenfiddich + 3 Ardbeg +
  3 Macallan + 3 Glenlivet + 3 Talisker + 3 Cameronbridge +
  3 Aberlour + 2 worked-example
  IB releases: `cadenheads-bunnahabhain` + `signatory-caol-ila`).
  Glenlivet bottlings (12 Year Old, 15 French Oak Reserve, Nàdurra
  Oloroso) added 2026-06-12; Talisker bottlings (10 Year Old,
  Distillers Edition, Storm) added 2026-06-14. Cameronbridge single
  grains (Cameron Brig, Haig Club, Haig Club Clubman) added 2026-06-14.
  North British (19th, grain) carries no own single-grain bottling, so it
  adds none — its `bottlings` list is empty by design. Aberlour bottlings
  (A'bunadh, 12 & 16 Double Cask Matured) added 2026-06-14.
  Macallan bottlings (Sherry Oak 12, Double Cask 12, Triple Cask
  Matured 15) were migrated from a pre-v0.2 flat field shape to the
  v0.2 schema on 2026-06-11; see CHANGELOG [0.8.4].
  **No IB pressure-test stubs remain.** Both IB-release entries
  are now worked-example representations rather than placeholders,
  with Cadenhead's house defaults (500ml, Cask Strength /
  Authentic Collection programme) and Signatory house defaults
  (700ml, Cask Strength Collection programme) populated.
  Glenfarclas bottlings: 10 Year Old (40% chill-filtered
  entry-level), 15 Year Old (46% NCF natural-colour — unusual in
  combining a 15-year age statement with the higher-ABV NCF
  natural-colour pattern that other producers adopted only in
  the 2010s), 25 Year Old (43% chill-filtered luxury core
  reaching the slow-exchange maturation phase per
  educational/cask-maturation-kinetics).
  Caol Ila bottlings: 12 Year Old (43% chill-filtered flagship,
  the 2002 Hidden Malts launch release), Distillers Edition
  (Moscatel-finished annual recurring — companion to the
  Lagavulin Distillers Edition's PX finish, exercising the
  cross-distillery Distillers Edition pattern at the bottling
  level). The
  `cadenheads-bunnahabhain-stub` was superseded 2026-05-17 by the
  worked-example `cadenheads-bunnahabhain` (slug renamed, confidence
  promoted stub → medium; the old stub file overwritten with empty
  YAML pending physical deletion from Windows). Bunnahabhain
  bottlings: 12 Year Old (46.3% NCF natural-colour flagship), Toiteach
  (peated NAS core at 46.3% NCF natural-colour). Highland Park
  bottlings: 12 Year Old (40% chill-filtered), 18 Year Old (43%),
  Cask Strength (annual NCF natural-colour at 60-65% ABV).
  `cadenheads-bunnahabhain` is the first non-stub IB-release entry
  in populated data, exercising the bottling v0.2 IB discriminator
  fields against a real distillery (Bunnahabhain) and a real
  bottler series (Cadenhead's Authentic Collection). Cask-identifier
  fields remain template-form with explicit notes pending
  specific-release verification.
  Both IB stubs marked `confidence: stub`; their purpose is
  exercising the bottling v0.2 IB discriminator fields and
  surfacing schema gaps. Specific release details (vintage, age,
  ABV, outturn, cask number) are null pending substitution with
  verifiable real releases.
- 17 casks: 5 high confidence (bourbon-barrel, oloroso/fino sherry,
  virgin-oak, undisclosed-cask), 7 medium (wine-cask parent + 5 named
  appellations + pedro-ximenez-sherry-butt), 5 low (lesser-disclosed
  wine cases). The `pedro-ximenez-sherry-butt` entry landed
  2026-05-19 alongside the Auchentoshan Three Wood entry, which
  exercises it as the third stage of its bourbon -> oloroso -> PX
  maturation sequence.

**Schema:**

- `schema/distillery.template.yml` — v0.2 (warehouses as list,
  data-driven from Springbank pressure-test; mothballed_periods
  canonised on `from`/`to`/`note` per JSON Schema audit; `washbacks.material`
  gained `wood` [0.8.5]; `stills.column_stills` added for grain [0.8.7])
- `schema/production_line.template.yml` — v0.2.1 (peating block,
  source methodology, `peat_origin: none`; `distillation.regime: continuous`
  [0.8.6]; `cereal_bill` added for grain [0.8.7])
- `schema/bottling.template.yml` — v0.2 (IB discrimination)
- `schema/concept.template.yml` — v0.1 (kind discriminator, per-kind
  blocks)
- `schema/bottler.template.yml` — v0.2 (presentation_defaults
  and parent fields added, data-driven from Signatory pressure-test)
- `schema/cask.template.yml` — v0.1 (disclosure_status enum,
  parent/alternatives relations; 18 entries populated)
- `schema/supplier.template.yml` — v0.1 DRAFT (maltster /
  cooperage_source / yeast_supplier / barley_breeder / other;
  sites list, ownership, products, supplies_to; 0 entries
  populated, awaiting first pressure-test)

**Validation tooling (2026-05-16):**

- `/schema/json/` holds draft-07 JSON Schemas for every entity type
  plus a shared `_common.schema.json` for slugs, sources, ABVs, etc.
- `scripts/check_references.py` runs JSON Schema validation as a
  warn-only pass alongside reference resolution. Cross-file refs to
  `_common` are merged into each entity schema at load time
  (jsonschema 3.2.0 cross-file `$ref` is brittle). YAML dates are
  coerced to ISO strings before validation. Current state: 0
  findings across all 85 files.

**Reference documents:**

- `docs/bibliography.md` — curated literature catalogue
  (2026-05-16, expanded). 767-line inventory covering 33 entries
  across 7 sections: technical reference books (Russell 2014,
  Piggott 1989 and 1983, Lyons & Hill, Boulton & Quain 2001,
  Buxton & Hughes 2014, Udo 2006), peer-reviewed paper authors
  / groups (Mosedale & Puech, Conner, Paterson & Piggott
  Strathclyde, Wanikawa Suntory, Aylott, SWRI staff), industry /
  academic journals (JIB, JSFA, Food Chemistry, JAFC, J Cereal
  Sci, Trends in Food Sci & Tech, Food Res Intl, LWT, Chem
  Senses, Flavour & Fragrance), institutional sources (SWRI,
  ICBD, SWA, HMRC, Worshipful Company of Distillers), annual
  publications (Malt Whisky Yearbook, Whisky Magazine), and
  historical / contextual works (MacLean, Moss & Hume 1981,
  Weir on DCL). Documents the project's positive sourcing
  standard and the exclusion criteria. Ten concept entries
  currently cite Russell ed. 2014 with `confidence: medium`
  hedges (listed under Russell's Cited-by subsection in the
  bibliography); grounding those against actual page references
  is queued research work.

**Build-pipeline status (2026-05-18):** all 8 items of the
build-pipeline-plan §Implementation sequencing have landed.
Items 1-4 (scaffolding, distillery rendering, markdown-link
rewriting, full entity-type rendering coverage) shipped through
2026-05-17. Items 5-8 (Pagefind search, MapLibre map, /explore/
cross-cutting query pages, reference pages) shipped 2026-05-18.
The /site/ source builds via `npm install && npm run build` from
`/site/`; postbuild step runs Pagefind against the Astro output.
Verification of the full chain is Windows-side (the Linux sandbox
times out on a full build and Pagefind's bundled binary segfaults
in the sandbox; both work on the developer host).

**Site index pages — grouped layout (2026-05-20):** the
`/production-lines/` and `/bottlings/` index pages were rewritten
from a single flat table to a list grouped under parent-distillery
`h2` sub-headings (distilleries alphabetical, each heading linking
to the distillery page; multi-entry distilleries carry a count).
production-lines groups on the line's `distillery` field; bottlings
groups on `produced_at_distillery` and drops the now-redundant
per-row Distillery column. Both tables use `table-layout: fixed`
with explicit widths on the narrow columns (Peating/Confidence;
ABV/Age/Type) so column edges align across every group. A dropdown
and an alphabet jump-bar were both rejected — JS-dependent, hide
content from Pagefind body-indexing, against the content-first
design. The grouped-list pattern matches `casks/index` and the
concept sub-indexes. This is the established pattern for any future
flat-table index that outgrows readability.

**Educational-page diagrams (2026-05-26):** the diagram pipeline
is proven and a full set of 10 deterministic SVGs lives in
`data/diagrams/`, attached to their concept pages via the
optional `diagrams:` schema field. Three visual registers,
codified in `docs/diagram-style.md`:

- **Sketch** (turbulence + displacement filter): pot-still
  schematic, production-chain flowchart, peating-measurement
  matrix.
- **Strict** (no filter, precise axes, full grid, plotted from a
  sourced figure): the two data graphs `spirit-cut` (Miller Fig.
  6.7) and `cask-maturation-kinetics` (Miller Fig. 8.11), emitted
  by `scripts/gen_data_diagrams.py`.
- **Technical-schematic** (new in 2026-05-26, blueprint
  conventions: `stroke="currentColor"` throughout, double-walled
  vessels with diagonal section hatching, dashed annotation
  leaders with filled-dot terminations, short solid pipe-nozzle
  stubs at inlets/outlets, dashed hidden lines for occluded
  parts): mash-tun, washback, worm-tub, shell-and-tube-condenser,
  coffey-still, spirit-safe. Conventions settled in the
  2026-05-26 pilot on mash-tun, then rolled out to the other
  five.

CHANGELOG [0.8.3].

**Next priorities, in order of unblock value:**

1. **Data-layer growth — 21st distillery.** Aberlour landed 2026-06-14 as
   the 20th — a second sherry-led Chivas Speyside (double-cask house style;
   the cask-strength A'bunadh) — after the two grain distilleries (North
   British 19th, Cameronbridge 18th). The queued next move is a set of
   **small new-wave distilleries**: **Nc'nean** (organic / net-zero, west
   Highland), **Ardnamurchan** (Adelphi-owned, radical cask transparency,
   peated + unpeated) and **Ardnahoe** (Hunter Laing, Islay, worm tubs — in
   the expected-dangling allowlist, so populating it clears that forward
   ref). These add new dimensions (sustainability, cask transparency,
   independent-bottler-owned distilleries) beyond the established-major
   pattern. New entries lean on Wikipedia at population; see TODO.md
   Research Requests for the outstanding producer-primary migrations.
2. **Residual sourcing follow-ups — glossary confidence blockers
   RESOLVED (2026-06-12).** The two remaining medium-confidence
   glossary entries were promoted to `high`: `distillers-yeast`
   (the named yeast-house list — MX/Kerry, Pinnacle/Mauri-AB Biotek,
   DistilaMax/Lallemand, and the DCL "M"-strain origin — is now
   corroborated by Daute, Jack & Walker 2024, *FEMS Yeast Research*,
   an SWRI-coauthored open-access paper) and `shell-and-tube` (the
   copper/DMTS condenser mechanism is now corroborated by Harrison
   et al. 2011, *J. Inst. Brew.*, an SWRI peer-reviewed paper). All
   seven of the original medium-confidence production-chain glossary
   entries are now `high`. Remaining sourcing work is currency-level:
   the Russell 2nd→3rd edition citation migration (16 entries) and
   the per-entry Wikipedia→primary migrations in TODO.md Research
   Requests.
3. **Audit follow-ups (2026-06-11) are landed; watch the new gate.**
   The empty-YAML stub tombstones are gone, the Macallan files are
   migrated to schema, and `scripts/check_references.py --strict` is
   now wired into the pre-commit hook (gate 2) alongside the
   hard-corruption scanner. Genuine forward references must be added
   to `scripts/expected_dangling.txt` or they will fail the strict
   gate; conversely, when a forward-referenced entity is populated its
   allowlist line must be removed (done 2026-06-12: `distillery:glenlivet`
   removed when Glenlivet landed). See `docs/audit-2026-06-11.md` and
   CHANGELOG [0.8.4].

**Completed since the last handover revision:**

- `concept/practice/triple-distillation` — LANDED 2026-05-19.
  Cited against Nicol Ch 9 p 173; cross-referenced from the
  Auchentoshan and Springbank `distinctive_features` lists.
- `pedro-ximenez-sherry-butt` cask entry — LANDED 2026-05-19.
- **Confidence-level review on the 14 Russell-grounded concept
  entries — DONE 2026-05-19. Conclusion: no promotions.** The
  Russell grounding improved source *quality* and removed the
  "page refs TBA" hedge, but did not change the confidence
  landscape. The 7 single-source glossary entries (kiln,
  mashing, distillers-yeast, fermentation, reflux,
  shell-and-tube, wash-still) remain `medium` because `high`
  requires multi-source corroboration. The multi-source
  educational pages (cask-maturation-kinetics, chill-filtering)
  remain `medium` because each carries explicit documented
  hedges / contested-claim sections — textbook `medium` per the
  rubric. external-malting is the closest `high` candidate but
  is held at `medium` for consistency with its contrast-pair
  sibling floor-malting. Confidence levels should not move on
  source-formatting improvements alone. (Superseded for five of
  the seven glossary entries by the 2026-05-20 Miller grounding —
  see next.)
- **Miller grounding pass — DONE 2026-05-20.** Miller, *Whisky
  Science: A Condensed Distillation*, 2nd ed. (2024) — an
  academic reference genuinely independent of the Russell lineage
  (different author, publisher, institution) — was grounded
  against the seven medium-confidence glossary entries. Five
  promoted to `high`: kiln, mashing, fermentation, reflux,
  wash-still, each now carrying Russell + Miller with page-level
  corroboration. Two held at `medium`: `distillers-yeast` (Miller
  corroborates the distilling-strain core but not the named
  yeast-house list) and `shell-and-tube` (Miller does not treat
  condenser types at all). One source conflict surfaced and
  preserved per policy: Miller's first-mashing-water temperature
  (ca. 70 °C) versus Russell's first-water strike (63.5-64 °C).

**Full active queue:** see `TODO.md`.

---

## 11. How to add a new distillery (high-level)

1. Research using producer sources, Scotch Whisky Whiskypedia, trade
   press, Wikipedia, and independent visit accounts. Aim for 5+
   sources for a confidence:high entry.
2. Resolve conflicts per `docs/source-conflict-policy.md`.
3. Start with the distillery entry. Then production lines. Then
   bottlings (typically 3 per line as a starting set; pick releases
   that exercise the schema — core, vintage/provenance, and an
   edge case).
4. Write a `<distillery>.NOTES.md` for any source conflicts,
   methodology assumptions, or fields left null with reasons.
5. Validate every file parses (`python3 -c "import yaml; yaml.safe_load(open('...'))"`).
6. PR.

The Harris and Bruichladdich entries are the working pattern; copy
their structure rather than starting fresh.

---

## 12. When in doubt

The schema templates have the most current rules — read them
first. This handover is a higher-level orientation.

**Document precedence (when sources conflict).** Highest authority
first: (1) the JSON Schemas in `/schema/json/` for anything they
validate — they are what the resolver actually enforces, so for the
source-type enum, field shapes, and required fields they win; (2) the
`schema/*.template.yml` templates for field semantics, conventions,
and authoring guidance not captured by the JSON Schemas; (3) the
policy docs (`docs/voice-register.md`, `docs/source-conflict-policy.md`);
(4) this handover. If a lower tier disagrees with a higher one, the
higher tier is correct and the lower one needs updating.

The notes files (`<entity>.NOTES.md`) preserve decision rationale
that matters for specific entries.

`TODO.md` is the active backlog. `docs/schema-design-notes.md`
records why the schema is shaped the way it is.

When making non-trivial changes — adding a kind to the concept
taxonomy, breaking schema changes, new entity types — update this
document so the next handover has the latest picture.

---

## 13. Project tooling and skills

Resources for ongoing authoring:

- **`scripts/check_references.py`** — cross-reference resolver and
  JSON Schema validator. Run from the repo root. Reports dangling
  references (split into allowlisted forward references vs unexpected
  ones, via `scripts/expected_dangling.txt`), duplicate IDs, invalid
  `source_id` refs, unresolved inline `[N]` citations, stale
  `schema_version` declarations, and cross-file consistency
  contradictions. Default output is warn-only; `--strict` exits
  non-zero on hard problems and is the second pre-commit gate.
- **`scripts/check_writes.py`** — hard-corruption scanner (NUL
  bytes, truncation, YAML parse failure); the first pre-commit gate.
- **`scripts/test_checks.py`** — unit tests for the two gate scripts
  (`python3 scripts/test_checks.py`).
- **`/skills/voice-register/SKILL.md`** — voice rules as a
  project-local Claude skill (mirrors `docs/voice-register.md`).
  Triggers when authoring prose for any entry.
- **`/skills/safe-bulk-writes/SKILL.md`** — operating procedure
  for writing many files in one turn. Codifies the lesson learned
  in the cask-population session: parallel Write batches of 5+
  files have produced NUL-byte padding and silent truncation;
  single Writes of files larger than ~10 KB have also truncated.
  Caps parallel batches at ≤4 and recommends verification via
  `check_references.py` after each batch, with a bash-mediated
  repair pattern for the truncation case.

Load-bearing docs (in addition to this one):

- `docs/voice-register.md` — canonical voice rules.
- `docs/source-conflict-policy.md` — source reliability hierarchy,
  Wikipedia-volatility policy, source-type vocabulary.
- `docs/schema-design-notes.md` — schema design rationale.
- `docs/diagram-style.md` — authoring spec for the deterministic
  SVG diagrams (theme-driven, sourced, version-controlled as
  text). The concept schema carries an optional `diagrams:` list;
  files live in `data/diagrams/`.
- `TODO.md` — active backlog. The Research Requests section
  catalogues entries currently citing Wikipedia where a primary
  source upgrade is available.
- `CHANGELOG.md` — schema changes and notable project additions.
