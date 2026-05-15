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

Highest-priority concept pages, ordered by what cleans up the most
dangling references in existing data:

1. **`glossary/phenol`**, **`glossary/cresol`**, **`glossary/guaiacol`**,
   **`glossary/standard-seven-phenols`** — the foundational set of
   compound glossary entries. Each is referenced from `covers:` on
   `educational/aromatic-compounds-in-whisky` and from
   `related_concepts:` on `educational/peating-measurement-methods`.
   Short entries — summary text, body null. Together they resolve
   ~8 dangling references.
2. **`glossary/sulphur-in-new-make`** — referenced from
   `educational/copper-conversation` covers, from
   `educational/aromatic-compounds-in-whisky` covers, and from
   `equipment/worm-tub` related_concepts. Short summary; covered
   in body of copper-conversation.
3. **`glossary/lyne-arm`** — referenced from `equipment/worm-tub`
   related_concepts. Short equipment-component glossary entry.
4. **`glossary/classic-malts`** — referenced from
   `equipment/worm-tub` related_concepts. A historical Diageo
   marketing portfolio rather than a technical term; entry should
   define it factually as a brand/portfolio designation rather than
   adopting marketing framing.

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
- (Glossary entries previously listed here have been promoted to
  the highest-priority concept-pages-to-create section above, since
  they now constitute essentially all remaining dangling concept
  references.)

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
