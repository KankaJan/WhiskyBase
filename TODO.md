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

### Not yet drafted

- **Cask schema** and `/data/casks/` directory. Bottling and
  production_line entries currently reference cask slugs
  (`bourbon-barrel`, `oloroso-sherry-butt`, `pomerol-wine-cask`,
  `pauillac-wine-cask`, etc.) that have no backing entries.
  - Special case: `undisclosed-cask` needs to be a first-class
    entry, not a placeholder slug. Producer-secret cask information
    is information, distinct from unknown-but-discoverable. The cask
    schema should support a `disclosure_status` field with values
    `disclosed | partially_disclosed | undisclosed | unknown`.

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

Highest-priority concept pages, ordered by what cleans up the most
dangling references in existing data:

1. **`methodology/harris-published-ppm`** — sibling to
   `methodology/bruichladdich-published-ppm`. The Harris production
   line currently references this concept; the page does not exist.
2. **`methodology/scotch-whisky-published-ppm`** — referenced from
   the Harris production line; documents the methodology used by
   Scotch Whisky Whiskypedia structured spec sheets.
3. **`educational/aromatic-compounds-in-whisky`** — foundational
   educational page on phenols, cresols, guaiacols. Referenced from
   `educational/peating-measurement-methods` and many future
   entries. Will require structured glossary entries for individual
   compounds.
4. **`equipment/shell-and-tube-condenser`** — the alternative to
   worm tubs. Referenced from `equipment/worm-tub` as `alternatives:`.

### Concept pages to queue

These will be needed but are not currently blocking dangling
references:

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
- Glossary entries currently referenced from
  `educational/peating-measurement-methods`: `phenol`, `guaiacol`,
  `cresol`, `standard-seven-phenols`, `lyne-arm`,
  `sulphur-in-new-make`, `classic-malts`

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

- **2026-05-13** Initial repository commit. Schema, 2 distilleries, 4
  production lines, 10 bottlings (migrated to v0.2), 3 concept pages,
  bottler schema stub, docs (handover, voice register, source
  conflict policy, schema design notes, contributing).
