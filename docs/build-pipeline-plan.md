# Build pipeline plan

Design document for the WhiskyBase static-site build pipeline.
Establishes the page-type taxonomy, URL routing, markdown-link
rewriting, component mapping, search and map strategy, and the
data-display decisions that the eventual implementation needs to
honour.

This document does NOT specify implementation details (template
syntax, component file structure, build commands) — those follow
from the design decisions here once an implementer starts work.

## Status

**Design draft v0.1, 2026-05-17.** Decisions marked "DECIDED" are
firm; "OPEN" decisions list the trade-offs and a recommended path.
Open decisions can be resolved as part of frontend implementation
or in a v0.2 revision of this document.

**Implementation progress (2026-05-18):** All 8 items of the
§Implementation sequencing list have landed.

- Items 1-3 (scaffolding, distillery rendering, markdown helper with
  entity-link rewriting + inline `[N]` citation resolution): shipped
  2026-05-17.
- Item 4 (other entity types — production lines, bottlings,
  bottlers, casks, suppliers; concept-block dispatch refined for all
  5 kinds): shipped 2026-05-17 alongside the Wikipedia-style UI
  refactor.
- Item 5 (Pagefind search): shipped 2026-05-18. `<main>` carries
  `data-pagefind-body`, BaseLayout takes optional `pagefindMeta`,
  detail pages emit per-entity-type meta for the filter chips,
  `/search/` page mounts PagefindUI, postbuild step runs
  `pagefind --site $outDir`.
- Item 6 (MapLibre map): shipped 2026-05-18 at `/map/` over Carto
  Positron tiles; pins fitted to extent on load.
- Item 7 (cross-cutting `/explore/` queries): shipped 2026-05-18.
  `/explore/by-region/`, `by-ownership/`, `by-peating/`,
  `by-presentation/`, `by-cask-category/` against the existing
  loaders.
- Item 8 (reference pages): shipped 2026-05-18 at `/reference/<slug>/`.
  Six entries: about, source-policy, voice-register, bibliography,
  schema-design-notes, contributing. Sources read at build time
  from `/docs/*.md` (leading h1 stripped).

Run `npm install && npm run build` from `/site/`. The build script
chains `astro build` and a `postbuild.mjs` helper that resolves the
output directory and runs Pagefind. End-to-end verification is
Windows-side: the Linux sandbox times out on a full build and the
bundled Pagefind binary segfaults in that environment; both work
on the developer host.

## Stack

**Astro** for the static-site generator. Rationale: handles the
project's data-driven page generation pattern cleanly (one page
per YAML entry, with shared components for cross-references);
fast incremental builds; markdown integration for the body fields
on concept pages; component-based rendering compatible with the
map and search overlays.

**Pagefind** for site search. Rationale: indexes statically-built
HTML output rather than the YAML source — preserves the
markdown-link rewriting and entity-cross-reference structure that
the build produces. No server-side search component required.

**MapLibre GL** for the distillery map. Rationale: open-source
(no Mapbox token / commercial dependency conflict with the
CC-BY-SA data licence); supports OpenStreetMap-derived tiles;
handles the 8-distillery present + future growth scale trivially.

**Licensing.** Per project README:
- Data and documentation under CC-BY-SA 4.0
- Code (build tooling, site source) under MIT
The build output bundles data into the page; the licensing
notice must appear in the site footer with both licences
named and linked.

---

## Page-type taxonomy

The site has these page types, one per entity-type plus
cross-cutting query pages:

### Per-entity-type pages

| Entity type | Source data | URL pattern | Notes |
|---|---|---|---|
| Distillery | `data/distilleries/*.yml` | `/distilleries/<slug>/` | One page per distillery |
| Production line | `data/production_lines/*.yml` | `/production-lines/<slug>/` | Note plural with hyphen |
| Bottling | `data/bottlings/*.yml` | `/bottlings/<slug>/` | One page per bottling |
| Bottler | `data/bottlers/*.yml` | `/bottlers/<slug>/` | One page per bottler |
| Cask | `data/casks/*.yml` | `/casks/<slug>/` | One page per cask type |
| Supplier | `data/suppliers/*.yml` | `/suppliers/<slug>/` | One page per supplier |
| Concept | `data/concepts/<kind>/*.yml` | `/concept/<kind>/<slug>/` | Per-kind subdirectory |

The concept URL pattern (`/concept/<kind>/<slug>/`) **DECIDED**
follows the convention already used in the project's markdown-
link form (`concept/<kind>/<slug>` per
`schema/concept.template.yml`). Other entity-type URL patterns
are **DECIDED** here as the most natural rendering of the
file-system organisation, with hyphen-separated multi-word
directory names (`production-lines`, not `production_lines`).

### Index pages

| Page | URL | Generated from |
|---|---|---|
| Home | `/` | Hand-authored; landing |
| Distilleries index | `/distilleries/` | All distillery slugs, sorted by name |
| Production lines index | `/production-lines/` | All line slugs |
| Bottlings index | `/bottlings/` | All bottling slugs |
| Bottlers index | `/bottlers/` | All bottler slugs |
| Casks index | `/casks/` | All cask slugs |
| Suppliers index | `/suppliers/` | All supplier slugs |
| Concepts index | `/concept/` | All concepts, sub-indexed by kind |
| Methodology subindex | `/concept/methodology/` | Methodology entries |
| Educational subindex | `/concept/educational/` | Educational entries |
| Equipment subindex | `/concept/equipment/` | Equipment entries |
| Practice subindex | `/concept/practice/` | Practice entries |
| Glossary subindex | `/concept/glossary/` | Glossary entries |

### Cross-cutting query pages

The analytical-payoff pages — these distinguish WhiskyBase from a
flat wiki. **DECIDED** to start with the following set; more can
be added as the data justifies them:

| Query page | URL | Contents |
|---|---|---|
| Distilleries by region | `/explore/by-region/` | Map + table grouped by SWA region (formal vs informal Islands split) |
| Distilleries by ownership | `/explore/by-ownership/` | Grouped by current corporate / family owner — Diageo / Edrington / etc. clusters |
| Production lines by peating | `/explore/by-peating/` | Sorted by spec ppm: unpeated → light → moderate → heavy → extreme |
| Bottlings by presentation | `/explore/by-presentation/` | Cross-tabulated by chill-filter / NCF / natural-colour / cask-strength |
| Casks by category | `/explore/by-cask-category/` | bourbon / sherry / wine / virgin etc. |

The /explore/ prefix isolates analytical pages from the
per-entity primary pages.

### Reference pages

| Page | URL | Source |
|---|---|---|
| About | `/about/` | Adapted from README |
| Bibliography | `/bibliography/` | Rendered from `docs/bibliography.md` |
| Source policy | `/sources/` | Rendered from `docs/source-conflict-policy.md` |
| Voice register | `/voice/` | Rendered from `docs/voice-register.md` |
| Schema design notes | `/schema/` | Rendered from `docs/schema-design-notes.md` |
| Handover (developer) | `/handover/` | Rendered from `docs/handover.md` |
| Licence | `/licence/` | LICENSE-data + LICENSE-code content |

---

## Slug → URL routing

**DECIDED** routing rules:

- Entity-type slugs: `<slug>` → `/<entity-type-plural>/<slug>/`.
  Entity-type-plural directories use kebab-case (hyphen-
  separated).
- Concept slugs: `<kind>/<slug>` → `/concept/<kind>/<slug>/`.
- Trailing slash on all URLs (canonical form).
- No file extension (`.html` suppressed; Astro default).
- Slugs are lowercase-hyphenated, ASCII; no transliteration
  needed in current data set.

---

## Markdown-link rewriting

The project's existing convention (documented in
`schema/concept.template.yml`) writes inter-entity references in
prose as markdown links:

```
[guaiacol](concept/glossary/guaiacol)
[cask maturation kinetics](concept/educational/cask-maturation-kinetics)
[Highland Park 12](bottling/highland-park-12)
```

**DECIDED** the build pipeline rewrites these to absolute site
URLs at build time:

| Markdown source | Rewrites to |
|---|---|
| `(concept/<kind>/<slug>)` | `(/concept/<kind>/<slug>/)` |
| `(distillery/<slug>)` | `(/distilleries/<slug>/)` |
| `(production_line/<slug>)` | `(/production-lines/<slug>/)` |
| `(bottling/<slug>)` | `(/bottlings/<slug>/)` |
| `(bottler/<slug>)` | `(/bottlers/<slug>/)` |
| `(cask/<slug>)` | `(/casks/<slug>/)` |
| `(supplier/<slug>)` | `(/suppliers/<slug>/)` |

The currently-used `concept/<kind>/<slug>` form is the only
inter-entity markdown link convention the data uses. The other
entity types are written as straight prose with the entity
name; the rewriting rules above are forward-looking for cases
where future entries adopt explicit cross-reference markdown.

Implementation: a build-time markdown-it / unified plugin that
runs on every prose field before rendering. Verification: the
build should warn (not fail) on a markdown link whose target slug
doesn't resolve to a populated entry.

### Glossary auto-resolution

The `concept.template.yml` mentions that bare-term mentions of
glossary terms in prose should auto-resolve to hover-tooltips.

**OPEN.** Two implementation options:

(a) **Text-mining.** Scan every prose field for bare mentions of
known glossary terms; auto-wrap in tooltip / hover markup. Pro:
no markup discipline required from authors. Con: prone to
false-positive matches (e.g., "abv" is too short and too
common; "phenol" appears in many compound names). Requires a
denylist or word-boundary tightening.

(b) **Explicit markup.** Authors mark glossary references
explicitly with the markdown-link convention. Pro: no
false-positives; transparent. Con: requires consistent author
discipline; existing prose mostly uses bare-term mentions.

**Recommendation: (b) with selective (a) for high-value
glossary terms.** Start with explicit-markup-only and extend
to text-mining for a curated set of unambiguous glossary terms
(e.g., the named phenol compounds — guaiacol, cresol — that
are unlikely to occur in prose for unrelated reasons).

---

## Data → component mapping

Each entity type renders through a shared base layout plus an
entity-specific component that handles structured-field display.

### Shared base components

- `<EntityHeader>`: name + slug + entity-type label + status
  (operating / closed / etc.) + confidence badge (high / medium
  / low / stub)
- `<SourcesBlock>`: numbered source list with inline-citation
  resolution (the `[N]` notation in prose gets linked to the
  corresponding source-list entry)
- `<RelatedConcepts>`: list of related_concepts cross-references
- `<MetadataFooter>`: schema_version, last_reviewed,
  contributors, license attribution

### Per-entity-type components

| Entity | Key components |
|---|---|
| Distillery | `<LocationBlock>` (region, sub_region, coordinates → small map); `<OwnershipHistory>` (timeline view); `<EquipmentSpec>` (mash tun + washbacks + stills + warehouses); `<ProductionLinesList>`; `<DistinctiveFeatures>` (concept refs) |
| Production line | `<PeatingDisplay>` (measurement table with stage / method / compounds breakdown); `<DistillationRegime>`; `<MaturationCaskProgram>`; `<BottlingsList>` |
| Bottling | `<PresentationStrip>` (ABV / age / NCF / natural-colour / cask-strength badges); `<MaturationDetail>` (per-cask-type table); `<RrpDisplay>` (with "as of" date and caveat); `<TastingNotesBlock>` (when populated) |
| Bottler | `<BottlerTypeBadge>` (distillery / IB); `<SeriesList>` with `<SeriesDetail>` for each |
| Cask | `<CaskCategoryBadge>`; `<PriorContentsDisplay>`; `<DisclosureStatus>` |
| Supplier | `<SupplierTypeBadge>`; `<SitesList>`; `<ProductsList>`; `<SuppliesTo>` (resolved to distillery links) |
| Concept | `<ConceptKindBadge>`; `<SummaryRender>`; `<BodyRender>` (markdown); per-kind block render |

---

## Search index scope (Pagefind)

**DECIDED** the search index covers:

- Page title
- Entity name(s) and aliases
- Summary fields (concepts) and descriptions (distilleries,
  bottlings, etc.)
- Body content (concepts with `body:` populated)
- Cross-reference anchor text (so a search for
  "shell-and-tube" matches both the equipment concept page and
  the bottlings that mention it)

**Excluded** from the search index:

- Footer / metadata text
- Source citation prose (the `notes:` field on individual
  source entries) — too noisy
- SCHEMA-OBSERVATIONS / SCHEMA-GAPS comment blocks — these
  exist for project maintainers, not site visitors

Faceted search filters:

- Entity type (distillery / line / bottling / concept / etc.)
- Region (for distilleries and lines)
- Peating level (for production lines and bottlings)
- Cask category (for casks)

---

## Map (MapLibre)

**DECIDED** the map renders distillery coordinates from the
`coordinates:` field on each distillery entry. Currently all 8
populated distilleries have `coordinates:` populated.

- Base tiles: OpenStreetMap-derived (CartoDB Positron or
  similar permissively-licensed tile source)
- Pin per distillery; click → distillery page link
- Region overlays for the SWA formal regions (Highland,
  Lowland, Speyside, Islay, Campbeltown) — visually
  distinguished from the informal "Islands" cluster
- Map scope: Scotland-centred; clip to UK + adjacent waters

**OPEN: coordinate precision policy.** Current coordinates are
approximate (to ~3 decimal places, ~110m accuracy). Map pins are
visible at this precision but cannot be used for surveying-level
work. The project's `coordinates:` field is not source-cited; the
values are derived from public mapping data without a primary
source recorded.

**Recommendation:** add a `coordinates_source:` field to the
distillery schema as an optional sub-field, capturing where the
coordinate values came from (e.g., "WGS84 derived from
OpenStreetMap node N123456"). This would lift coordinate precision
into the project's sourcing standard. Deferred until a frontend
implementation actively uses the field.

---

## Data-display decisions

### Tasting-notes display

**DECIDED** the build does NOT render `notes_independent`
content. The project's voice register explicitly avoids
subjective scoring; including reviewer tasting-notes would
reintroduce that voice into a project that has carefully kept
it out.

`notes_official` (producer-disclosed tasting notes) is rendered
with explicit "producer-disclosed" attribution if populated.
Currently no populated bottling entry has `notes_official:`
populated.

### Commercial-info display

**DECIDED** the build renders `rrp` content with the following
treatment:

- Prefix: "Approximate launch price"
- Display: "{currency} {amount} (as of {as_of})"
- Caveat: "Indicative only; real-world prices vary by market
  and time."

The project's README explicitly says it is not a market-price
tracker; the `rrp` field exists because release pricing is part
of the product's permanent record at the time of release, not
because the site claims to track current prices.

### Confidence badge display

The `confidence:` field (high / medium / low / stub) renders as
a small visual badge on each entry:

- **high**: green / "well-sourced"
- **medium**: amber / "see sources for hedges"
- **low**: orange / "single-source or contested"
- **stub**: red / "placeholder"

Hovering / clicking the badge surfaces an explanation linking to
the project's source-conflict-policy.

---

## Cross-reference resolution at build time

The existing `scripts/check_references.py` resolver already
catalogues every entity slug and concept slug. The build pipeline
runs an extended version of this resolver that:

1. Validates every cross-reference resolves (re-uses the resolver's
   existing logic).
2. For each `[N]` inline citation in prose, generates an HTML
   anchor to the corresponding source list entry.
3. For each `concept/<kind>/<slug>` markdown link, rewrites to
   `/concept/<kind>/<slug>/`.
4. For prose mentions of glossary terms in the auto-resolve
   curated set, wraps in a `<dfn>` element with hover-tooltip
   markup.
5. For dangling references (per handover §8 forward refs), renders
   them as plain text (not as broken links) and emits a build
   warning.

---

## Build performance considerations

- 115 source files (current state); 8 distilleries / 13 lines /
  29 bottlings / 2 bottlers / 16 casks / 2 suppliers / 45
  concepts = ~115 entity pages + ~15 index/explore/reference
  pages = ~130 total pages. Astro builds this in well under a
  second on modern hardware.
- The search index (Pagefind) typically adds <100ms to the
  build pipeline at this scale.
- The map is a single page with one MapLibre instance plus the
  distillery list as GeoJSON; trivial.

Growth projection: the project could plausibly grow to 50+
distilleries × ~3 production lines × ~5 bottlings each = ~750
bottling pages, plus 100+ concept pages. This is still well
within static-site-generator capacity (Astro handles thousands of
pages routinely).

---

## Pre-implementation checklist

Before frontend implementation begins, the following items must
be resolved or explicitly deferred:

| Item | Status | Notes |
|---|---|---|
| Page-type taxonomy | DECIDED | This document |
| URL routing convention | DECIDED | This document |
| Markdown-link rewriting rules | DECIDED | This document |
| Tasting-notes display | DECIDED | Render notes_official only with attribution; skip notes_independent |
| Commercial-info display | DECIDED | Render `rrp` with launch-price caveat |
| Confidence badge UX | DECIDED | Visual badge with hover-explanation link |
| Glossary auto-resolution | OPEN | Recommend explicit-markup + curated text-mining set |
| Coordinate precision policy | OPEN | Recommend coordinates_source schema field; defer until frontend uses it |
| Site visual style | OPEN | Outside the scope of this document — implementation-time decision |
| Internationalisation | DEFERRED | English-only; not in scope |
| CI / automated validation | DEFERRED | Post-frontend |
| Contribution flow / PR template | DEFERRED | Post-frontend |

---

## Pre-frontend data checklist

Items in the data that should be addressed before publication:

| Item | Status | Notes |
|---|---|---|
| `signatory-caol-ila-stub` replacement | OPEN | Once Caol Ila is populated, this becomes a worked-example IB release following the cadenheads-bunnahabhain pattern |
| Russell-textbook citation grounding (10 entries) | OPEN | Citations carry `confidence: medium` and explicit hedges; the build pipeline renders these honestly even pre-grounding |
| Specific INAO / MIPAAF / Consejo Regulador document URLs (10 entries) | OPEN | Same as Russell — institutional homepages cited with verification hedges; renders honestly |
| Distillery `coordinates_source` field (8 entries × 2 fields) | OPEN | Tied to the coordinate precision policy above |

None of the OPEN items strictly block the frontend launch; they
all render honestly as confidence-medium content with sourcing
hedges in the existing entries. They form the post-launch
content-quality backlog.

---

## Implementation sequencing

All items below are LANDED (last updated 2026-05-18). Order
preserved as a historical record of the planned sequence.

1. **Static site scaffolding** — Astro project skeleton, base
   layout, footer with licensing. **LANDED 2026-05-17.**
2. **Distillery pages** (9 entries × ~1 page) — the most
   information-dense entity type; getting these right validated
   the component design. **LANDED 2026-05-17.**
3. **Concept pages** (46 entries × ~1 page) — the second
   information-dense entity type, exercises markdown-link
   rewriting heavily. **LANDED 2026-05-17.**
4. **Other entity types** (production lines, bottlings, bottlers,
   casks, suppliers). **LANDED 2026-05-17.**
5. **Index pages and search** — Pagefind, indexes `<main>` content
   with `data-pagefind-body`, per-entity meta for filter chips;
   `/search/` page mounts PagefindUI. **LANDED 2026-05-18.**
6. **Map** — MapLibre GL at `/map/`, Carto Positron basemap,
   pins fitted to extent. **LANDED 2026-05-18.**
7. **Cross-cutting query pages** — `/explore/` index plus
   by-region, by-ownership, by-peating, by-presentation,
   by-cask-category. **LANDED 2026-05-18.**
8. **Reference pages** — `/reference/` index plus about,
   source-policy, voice-register, bibliography,
   schema-design-notes, contributing. Source docs read from
   `/docs/*.md` at build time. **LANDED 2026-05-18.**

---

## Document maintenance

This document is design intent, not implementation specification.
Implementation choices that diverge from these decisions are
acceptable if documented as updates here. The build-pipeline-plan
should be re-reviewed against the actual built site after the
first publication cycle to capture lessons.
