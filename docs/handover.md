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
bottling operations) — schema drafted at v0.1 stub, awaiting a real
IB case; and **cask** for reusable cask-type references that bottlings
and production lines cite from their maturation programmes — schema
v0.1 with 16 entries populated, including the first-class
`undisclosed-cask` for deliberately-secret cask provenance. Data lives as YAML in a
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

- 2 distilleries: Harris (confidence: medium), Bruichladdich (high)
- 4 production lines: 3 Bruichladdich (high), 1 Harris (medium)
- 10 bottlings: 9 Bruichladdich, 1 Harris
- 10 concept pages: 3 methodology (Bruichladdich, Harris, Scotch
  Whisky), 3 educational (peating-measurement-methods,
  aromatic-compounds-in-whisky, copper-conversation), 2 equipment
  (worm-tub, shell-and-tube-condenser), 2 glossary (peating-block,
  phenol-ppm)
- 16 casks: 5 high confidence (bourbon-barrel, oloroso/fino sherry,
  virgin-oak, undisclosed-cask), 6 medium (wine-cask parent + 5 named
  appellations), 5 low (lesser-disclosed wine cases)

**Schema:**

- `schema/distillery.template.yml` — v0.1
- `schema/production_line.template.yml` — v0.2.1 (peating block,
  source methodology, `peat_origin: none`)
- `schema/bottling.template.yml` — v0.2 (IB discrimination)
- `schema/concept.template.yml` — v0.1 (kind discriminator, per-kind
  blocks)
- `schema/bottler.template.yml` — v0.1 (stub; series modelling
  speculative, awaiting first real IB case)
- `schema/cask.template.yml` — v0.1 (disclosure_status enum,
  parent/alternatives relations; 16 entries populated)

**Next priorities, in order of unblock value:**

1. **Pressure-test the bottler v0.1 stub schema** against a real
   IB case (Cadenhead's Authentic Collection or Signatory Cask
   Strength is the likely first case) and promote to v0.2. This
   is the schema model's last unproven dimension; the IB/OB
   discriminator in bottling v0.2 has never been exercised with
   real data.
2. **Glossary entries to close the remaining concept dangling
   refs**: `phenol`, `cresol`, `guaiacol`, `standard-seven-phenols`,
   `sulphur-in-new-make`, `lyne-arm`, `classic-malts`. Each is a
   short entry (summary text, body usually null). Together these
   resolve essentially all remaining concept dangling references
   in the data. See TODO.md for the active list.
3. **`educational/cask-maturation-kinetics`** — research-heavy
   teaching page distinguishing established cask-maturation
   chemistry from trade convention from open questions. Would let
   several existing cask entries cite a sourced summary instead of
   hedging in prose. Detailed scope in TODO.md.
4. **Third distillery** (Springbank, Lagavulin, Highland Park, or
   similar) — most likely to surface unknown schema gaps. Three is
   the magic-number threshold for distillery patterns to emerge
   from observation rather than guess.
4. Glossary entries; many are referenced from the existing educational
   page but unpopulated.
5. JSON Schema validation tooling. Currently the only check is
   `yaml.safe_load()` parse-passes. Validation against the templates
   would catch typos and shape drift.
6. Build pipeline (Astro + Pagefind, per earlier design conversation).

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
first. This handover is a higher-level orientation. If the templates
and this document disagree, the templates are correct and this
document needs updating.

The notes files (`<entity>.NOTES.md`) preserve decision rationale
that matters for specific entries.

`TODO.md` is the active backlog. `docs/schema-design-notes.md`
records why the schema is shaped the way it is.

When making non-trivial changes — adding a kind to the concept
taxonomy, breaking schema changes, new entity types — update this
document so the next handover has the latest picture.
