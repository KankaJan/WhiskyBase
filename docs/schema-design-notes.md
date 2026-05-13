# Schema design notes

This document records *why* the schemas are shaped the way they are.
The schema templates themselves describe *what* each field does; this
document explains the design decisions behind the structure, so
future contributors can evaluate proposed changes against the
project's original reasoning.

---

## Three-entity production model

**Decision.** Production is modelled as three separate entity types:
distillery, production_line, bottling. Each lives in its own
directory, has its own schema, and is referenced from the others by
slug.

**Why not collapse them.** Earlier drafts had a single "whisky"
entity that held distillery info, recipe info, and release info
together. This worked for distilleries with one recipe and few
releases. It broke when applied to Bruichladdich (three production
lines from the same equipment) and to any distillery with many
releases (recipe data duplicated across every bottling).

The three-entity split is the minimum that captures the production
hierarchy honestly. Distillery is stable across decades (equipment
doesn't change often); production line is stable across years
(recipe changes are rare and worth documenting when they happen);
bottling is per-release.

**Why not more granularity.** A four-entity model adding "batch" or
"cask program" was considered. Rejected because the data doesn't
yet need it: per-batch variation lives in the bottling entry's
`maturation:` and `notes:` fields, and cask programmes are
adequately captured as references to cask slugs. If a real case
arises where this proves insufficient — e.g. a distillery releases
the same recipe under two unrelated branding lines — revisit.

---

## Peating: the structured measurement block

**Decision.** Peating is recorded on production_line entries as a
structured block:

```yaml
peating:
  measurements:
    - stage: spec
      value: 40
      unit: ppm
      method: hplc
      compounds: standard_7
      source_id: 1
```

Earlier drafts had a flat `peating_ppm: 40` field. This is documented
in v0.1 of `production_line.template.yml` and migrated in v0.2.

**Why the change.** PPM is not a single number. It depends on
(a) what stage was measured (kilned malt, new make, bottle), (b)
what analytical method was used (HPLC, 4-AAP, GC-MS,
Folin-Ciocalteu), and (c) which compounds were summed (the standard
seven, an extended set, individual compounds reported separately).
The flat field lost all of this information and produced a falsely
comparable number across releases that may have been measured very
differently.

The structured block makes the measurement contextual. Octomore 8.3
at 309.1 ppm via HPLC (standard 7) is a different claim from
Octomore 8.3 at 309.1 ppm via 4-AAP (total recoverable), and the
schema can now distinguish them.

**The breakthrough that validated this.** Bruichladdich's 2017
release of Octomore 8.3 included an explicit producer statement:
"Using HPLC (high performance liquid chromatography), the readings
came back at 309.1 ppm... the ppm level can vary depending on
whether a colorimetric reading or one from HPLC is taken, the
latter producing higher figures." The schema was designed to
capture this exact distinction. Subsequent population of the
Bruichladdich production lines confirmed the schema does what it
needs to do.

---

## Source-level methodology declaration

**Decision.** Sources can carry a `methodology:` block declaring how
they measure specific quantities:

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
```

Field-level measurements citing `source_id: 1` resolve their method
through the source's methodology block. This avoids repeating
`method: hplc, compounds: standard_7` on every measurement when the
source's methodology is consistent.

**The alternative considered.** Field-level methodology declaration —
every measurement carries its full method information regardless of
source. Rejected because it produces enormous repetition with no
information gain when a single source has a consistent methodology.

**The alternative also considered.** Hybrid — source declares
methodology, field-level overrides allowed. Deferred until a real
case forces it. As of 2026-05, no encountered source needs
field-level override.

---

## Concept layer: single template, kind discriminator

**Decision.** All concept pages — methodology, educational,
equipment, practice, glossary — share one template with a `kind`
discriminator field and per-kind structured blocks at the top level.

**The alternatives considered.**

- *Multiple templates, one per kind.* More structurally pure but
  more maintenance: five schemas instead of one, classification
  disputes ("is 'long fermentation' equipment or practice?"),
  harder onboarding.
- *One template, generous schema with all fields optional.* Lowest
  friction but no structural enforcement; methodology pages drift
  toward essay length, glossary entries become awkwardly long, the
  schema becomes a kitchen sink.

**Why the chosen design.** Single template ensures one rendering
pipeline and one cross-reference mechanism. Per-kind blocks at
top level (not nested under a generic `details:`) mean the schema
enforces appropriate structure per kind while remaining separable
by design: if a future split partitions concepts by kind into
separate top-level entity types, the per-kind block lifts cleanly
into a per-type schema with no field surgery.

**Why slugs use `<kind>/<slug>` namespacing.** Public slug form is
`concept/methodology/bruichladdich-published-ppm`. If we later move
`/data/concepts/methodology/` to `/data/methodologies/`, file paths
change but slugs stay stable. Cross-references survive the refactor.
This is "separable by design, not as last resort" — a contributor
choice from earlier conversation.

---

## Bottler discrimination at the bottling level

**Decision.** Bottling v0.2 schema discriminates OB vs IB at the
bottling level:

```yaml
produced_at_distillery: bruichladdich   # source distillery
bottled_by: cadenheads                  # commercial bottler
bottler_type: independent_bottler       # discriminator
bottler_series: cadenheads/authentic-collection
```

**The alternatives considered.**

- *IBs as distilleries.* Reject because IBs aren't physical
  production sites; most distillery fields (mash tun, stills,
  warehouses) are inapplicable.
- *Single unified bottler entity covering OBs and IBs.* Rejected
  because OBs are operationally part of their distillery; forcing
  them through a separate bottler entity adds a layer with no
  information gain.
- *Bottlers as a separate top-level entity type, bottling references
  one or the other.* Chosen. Distilleries are physical production
  sites with equipment; bottlers are commercial/curatorial entities.
  They are genuinely different things and the schema reflects that.

**Why discrimination is at the bottling level, not inferred.** The
`bottler_type` field is redundant — given `bottled_by`, you can
look up the entity to find out whether it's a distillery or a
bottler. Storing the type on the bottling avoids the lookup for
common queries ("show me all IB Bruichladdich" = `produced_at_distillery:
bruichladdich AND bottler_type: independent_bottler`). The
redundancy is a deliberate trade for query simplicity.

**Comparison emerges from filtering, not from schema opinion.** The
schema does not flag IB and OB pairs as "comparable" or otherwise.
Readers can filter on production_line, age, cask type, peating
spec, etc. and find their own comparisons. The build pipeline
(eventually) makes filtering easy; the schema does not bake in
opinions.

---

## Status field: confidence and last_reviewed

**Decision.** Every entity carries `confidence: stub | low | medium |
high` and `last_reviewed: YYYY-MM-DD`.

**Why.** Different fields in the same entry can have different
underlying confidence levels. A confidence rollup at the entry level
is a shorthand for "would this entry survive a careful audit" rather
than a per-field annotation. `last_reviewed` lets readers (and the
build pipeline) flag entries that haven't been touched in a long
time, useful when the underlying facts (ownership, prices,
discontinuations) change.

**The alternative considered.** Per-field confidence and provenance,
where every individual figure carries its own metadata. Deferred —
adds enormous markup overhead for marginal gain when the entry-level
rollup plus inline source citations already cover most needs. The
TODO list (item: "field-level provenance") records this as a future
consideration.

---

## What the schema deliberately does not record

- **Marketing positioning.** No "philosophy", "ethos", "passion",
  "journey" fields. See `voice-register.md` for the broader
  no-marketing rule.
- **Current secondary-market prices.** Out of scope, deliberately.
  `rrp.amount` records the release price as permanent reference
  data; auction values and current resale prices are not tracked.
- **Tasting tours and visitor information.** Out of scope.
- **Awards.** Mentioned in passing if relevant to provenance ("the
  PMC:01 release won X") but not tracked as a structured field.
  The schema is not an awards database.
- **Reader recommendations.** The project does not record "good for
  beginners" or "comparable to X if you liked Y" judgements. Readers
  decide what they want; the schema gives them the data to decide
  with.

---

## What is deferred

Recorded in `TODO.md`. Brief summary:

- Cask schema and `/data/casks/` directory.
- Bottler schema and `/data/bottlers/` population (directory exists
  empty).
- Concept page expansion (more glossary, more methodology, more
  equipment, more educational).
- Multiple warehouses per distillery (current schema has single
  `warehouse:` block; will need to become a list eventually).
- Per-batch child entries for transparent-batch SKUs like
  Bruichladdich Classic Laddie. Deferred until a clear pattern
  emerges from multiple such cases.
- JSON Schema validation tooling.
- Build pipeline (Astro + Pagefind).

The TODO is the active backlog. This document is the design rationale
for what already exists.

---

## When the schema needs to change

Breaking schema changes (renaming fields, removing fields, changing
field semantics) are expensive once data is populated. Before making
one:

1. Check whether the existing schema already accommodates the case
   under a less obvious interpretation. The flat `peating_ppm` field
   went through this — for several entries it worked fine; only at
   the Octomore 8.3 case did the case for change become unambiguous.
2. Document the change in `CHANGELOG.md` with a migration note.
3. Bump the affected schema's `schema_version`.
4. Migrate existing entries in the same commit. Don't leave entries
   straddling versions.

Non-breaking changes (adding optional fields, extending enums)
are cheap and can ship without a major version bump. Just record
them in `CHANGELOG.md` so future readers know when something appeared.
