# Glossary audit — under-developed entries (2026-06-15)

A content audit of all 52 `data/concepts/glossary/*.yml` entries, asking
which are *too thin to be useful* and what to do about each. This is a
plan, not content — no entry prose is written here.

> **Implementation status (2026-06-15): implemented in full.** Both
> promotions landed as `educational/yeast-strains` and
> `educational/oak-species` (distinct slugs from their kept, tightened
> glossary stubs); `marrying` was extended in place; the `bere`
> contradiction and the three see_also gaps were fixed. Gates pass
> (check_writes; check_references --strict). Logged in TODO.md Recently
> completed.

## Method and bar

Entries were judged on their actual `summary`/`body` text, not line
count (line count is dominated by sources/structure and is a poor
proxy). Glossary entries are **short by design**: the schema says the
`summary` is 1–2 sentences and is often the whole page, with `body`
usually null. So "short" is not "thin".

An entry is **too thin** only if it omits a core fact a reader meeting
the term in context would need. A separate question is whether a topic
is **rich enough to promote** to a full educational page — the precedent
being the known example: `glossary/char-and-toast` was *kept* as a tight
stub while `educational/cask-charring-and-toasting` was created to carry
the depth. (Note: the live glossary slug is `char-and-toast`, not
`charring-and-toasting`.)

Promotion therefore does **not** require the stub to be inadequate; it
requires the underlying topic to have genuine multi-section depth and no
existing deep page to hold it.

## Headline

The glossary is in good health. **49 of 52 entries are adequate and need
no change.** "Leave as-is" is the right call for the large majority.

- **Promote: 2 candidates** — `distillers-yeast` (clearest) and `oak`.
  Both meet the char-and-toast bar; both lack any existing educational
  page; both keep their glossary stub.
- **Extend in place: 1** — `marrying` (minor).
- **Leave: 49.**
- Plus **3 correctness/linkage issues** noticed in passing — not
  thinness, flagged not fixed (per the surgical-changes rule).

If you only want to act on one thing, it is the `distillers-yeast`
promotion, because almost all of its content already exists and the work
is restructuring, not research.

---

## Promotions

### 1. `distillers-yeast` → new `educational/distillers-yeast` (recommended)

**Criteria it meets.** The topic has clear multi-section depth:
distilling-vs-brewing strain selection, the named commercial yeast
houses, a datable industrial history (the M-type), wild/alternative
yeast, and a disclosure problem. It is `confidence: high` with a
peer-reviewed source already attached. Crucially, its `see_also` points
only to `glossary/fermentation` — there is **no deeper page to hand off
to**, so the stub is currently the terminus for a topic that wants more
room. The project already anticipates this depth: `TODO.md`
§Cross-cutting research has a standing "Yeast strains and fermentation
regimes" item (per-strain glossaries, peer-reviewed grounding, wild
yeast).

**Honest caveat.** Its summary is the longest in the glossary but only
modestly so (~1240 chars / ~7 sentences vs ~1000–1100 for `kiln`,
`bere`, `shell-and-tube`). So the case rests on topic-richness and
project direction, **not** on the stub bursting its format. "Leave" is
defensible if you don't want to expand the yeast topic now.

**Specific gaps a full page would close** (beyond what the stub states):

- The *mechanism* of why distilling strains differ from brewing strains
  — not just that they do. (Stub asserts the distinction; doesn't
  explain fermentation-kinetics/flavour trade-offs.)
- Wild/non-*cerevisiae* and house-strain experiments — e.g.
  Glenmorangie Allta's Cadboll wild strain — currently unmodelled and
  flagged in `glenmorangie.yml` SCHEMA-OBSERVATIONS. `[VERIFY]` the Allta
  strain details before asserting them.
- The flavour consequence of strain choice (ester development), tied to
  fermentation length and `lactic-acid-bacteria`.

**Rough structure:** distilling vs brewing strains (selection criteria);
named commercial houses + the M-type 1952 DCL hybrid history; wild and
experimental strains; the disclosure problem; effect on spirit
character. **Keep** a 1–2 sentence `glossary/distillers-yeast` stub with
`see_also` → the new page.

### 2. `oak` → new `educational/oak` (genuine, but more net-new work)

**Criteria it meets.** Oak-as-a-material is a multi-section topic —
species groups, wood anatomy, chemistry that differs *by* species,
provenance, and seasoning. It is even listed as a **prerequisite** of
`educational/cask-charring-and-toasting`, yet the prerequisite itself is
only a stub. No existing page fills this: `cooperage` covers cask
*making*, `cask-charring-and-toasting` covers *firing*,
`cask-maturation-kinetics` covers *extraction over time*, `maturation`
is the overview — **none** systematically compares the woods themselves.

**Specific gaps a full page would close:**

- *Why* American (`Quercus alba`) and European (`Q. robur`/`petraea`)
  oak give different spirit — the stub asserts "differ in grain, density
  and extractable-compound profile" without the mechanism. The page
  needs the chemistry: oak lactones (the coconut/sweet-oak note) higher
  in American oak; ellagitannins (astringency, colour) higher in
  European oak. `[VERIFY]` the directional lactone/ellagitannin claims
  against Mosedale & Puech 1998 before stating them.
- Wood anatomy: tyloses in *Q. alba* let it be sawn and stay watertight,
  while European oak must be split/quarter-sawn. `[VERIFY]` — I'm
  asserting this as a known cooperage fact but it should be sourced.
- Japanese Mizunara (`Q. crispula`/*mongolica*) as a third, minor
  cask wood. `[VERIFY]` species name and its porosity/leakage
  reputation.

**Rough structure:** the two dominant species groups; chemistry by
species; anatomy and why it dictates sawing; Mizunara and minor woods;
provenance/grain; seasoning before coopering. **Keep** the
`glossary/oak` stub; point its `see_also` and the charring page's
`prerequisites` at the new page.

**Trade-off:** lower priority than the yeast page because it requires
real wood-science research (the chemistry claims above are not yet in
the data), whereas the yeast page mostly restructures existing text.

---

## Extend in place

### `marrying` (minor)

Currently a serviceable 5-sentence definition. Genuinely missing core
facts, all small enough to stay in the glossary:

- The sharp distinction from its sibling terms — `vatting` is
  *combining* casks; `marrying` is *resting* the combination; finishing
  is a third thing. The stub blurs marrying and vatting.
- A concrete in-data example: Glenfiddich's 1998 Solera Vat (continuous
  marrying, already recorded in the Glenfiddich entry and handover).
- Typical duration. `[VERIFY]` — I do not have a confident standard
  figure (weeks to several months is cited variously); do not state one
  without a source.

This is the only clear extend-in-place. It is close to the leave
threshold; skipping it is reasonable.

---

## Considered and left as-is (representative)

- **`angels-share`** — borderline. Could add the Scotland-typical
  direction (in cool, humid warehouses strength falls slowly rather than
  rises) and that loss is front-loaded in the first year. Left because
  the stub already names the governing mechanism (temperature/humidity).
  `[VERIFY]` any rate (~2%/yr) or directional figure before adding.
- **`classic-malts`, `lyne-arm`, `standard-seven-phenols`** — content is
  adequate; each has `sources: []`. This is a **sourcing** gap, already
  tracked in `TODO.md` §Research requests / Empty sources — not a
  thinness gap, so not re-opened here.
- Chemical stubs (`phenol`, `guaiacol`, `cresol`), barley varieties
  (`concerto`, `optic`, `propino`), and the stage/equipment terms
  (`mashing`, `kiln`, `reflux`, `shell-and-tube`, `wash-still`, etc.)
  are all adequately scoped and already hand off to deeper pages where
  the depth exists. No change.

---

## Correctness / linkage issues noticed (not thinness — flagged, not fixed)

1. **`bere` internal contradiction.** The entry calls bere a "six-row
   landrace" (line 17) but then "*Hordeum vulgare* var. *distichum*"
   (line 20). `distichum` means **two-row**; six-row is
   `vulgare`/`hexastichon`. One side is wrong. `[VERIFY]` — bere is
   historically described as six-row, so `var. distichum` is the likely
   error, but confirm before editing.
2. **`see_also` depth-gradient gaps.** The schema's pattern is that a
   glossary stub points to its fuller page. Three do not:
   - `char-and-toast` → points to `educational/maturation` but **not**
     `educational/cask-charring-and-toasting` (its actual deep page).
   - `fermentation` → `see_also` is empty; `educational/fermentation`
     exists.
   - `mashing` → points to `glossary/fermentation`, not
     `educational/mashing` (which exists).
3. **If the two promotions proceed**, the new pages create two more
   stub→page links to add (`oak`, `distillers-yeast`), and the charring
   page's `prerequisites: [glossary/oak]` should retarget to
   `educational/oak`.

## What this audit deliberately does not do

No quota-filling. The remaining ~49 entries are adequate as written, and
expanding them would violate the project's simplicity-first and
voice/length discipline (length follows topic depth, not importance).
