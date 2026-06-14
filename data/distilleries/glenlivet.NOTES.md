# The Glenlivet — population notes

Working notes for the 16th distillery entry (populated 2026-06-12).
Records the source-conflict resolutions and the sourcing limitations
behind the `confidence: medium` rating, per the project's
source-conflict policy ("never silently round, average, or smooth";
resolve to one disclosed figure with the conflict documented).

## 1. Capacity and still count — resolved (the load-bearing conflict)

The surveyed sources disagree because they describe the site at
different times:

- **Wikipedia** (article on The Glenlivet distillery, accessed
  2026-06-12) records **14 stills (7 wash @ 15,000 L + 7 spirit @
  10,000 L)** and **~10.5 million LPA**. These figures describe the
  **post-2010, pre-2024** plant: the 2010 Prince of Wales extension
  added a mash tun, eight washbacks and stills, taking the count to 14
  and raising capacity ~75% to ~10.5M LPA. Wikipedia also records
  "ground broken on a further expansion in 2015".
- **The Northern Scot** (regional newspaper, April 2024) reports the
  **new stillhouse opened in the 2024 bicentenary year**: **seven new
  pairs of stills added, total 28**, and capacity **doubled to 21
  million litres per year**.

**Resolution:** the entry records the **current** state — **28 stills,
~21M LPA** — citing the 2024 source, and documents the 2010 → 2024
progression in `equipment_changes`. Wikipedia's 14-still/10.5M figures
are retained in the source-1 note as the pre-2024 state, not discarded.
No figure was averaged or smoothed.

Two residual uncertainties, recorded as such in the entry:

- **Per-still capacity after 2024.** The 15,000 L wash / 10,000 L
  spirit figures are Wikipedia's pre-2024 spec. The 2024 stillhouse
  replicated the lantern geometry, so the per-still figures are
  *assumed continued* but not separately re-confirmed for the new
  pairs. Flagged inline.
- **"21 million litres" vs LPA.** The 2024 source says "21 million
  litres per year" without specifying litres of pure alcohol. LPA is
  the conventional capacity measure and is recorded; if a producer
  source later distinguishes total-litres from LPA, revisit.

## 2. Ownership dates — minor nuances

- **Seagram acquisition: 1977 vs 1978.** Wikipedia dates it 1977; some
  trade histories say 1978. The entry records 1977 (the surveyed
  source) and flags the alternative inline.
- **Pernod Ricard: 2000 vs 2001.** Wikipedia dates the change to 2000
  (the Seagram break-up announcement / Vivendi deal); Pernod Ricard's
  acquisition of Seagram's drinks business completed in December 2001.
  The entry records 2001 (completion) and notes the 2000 announcement
  date inline.

## 3. "Glenlivet" name legal case — date

Wikipedia frames the case as post-1871 (after George Smith's death)
but does not pin a single year in the fetched summary. Multiple trade
histories (scotchwhisky.com Whiskypedia, others) date it to a **1881
suit by George Smith Grant** and an **1884 compromise**. The entry
records the 1881/1884 dates and the "-Glenlivet" hyphenation outcome
(26 distilleries adopted it), citing Wikipedia as the primary with the
date corroborated by the trade histories.

## 4. Nàdurra Oloroso — spec sourcing limitation

Wikipedia lists the Nàdurra in the range (as the Nàdurra 16 Year Old)
but does not detail the **Oloroso Matured** variant. Its specifications
— cask strength (batch-varying ABV ~60-61%), non-chill-filtered,
natural colour, first-fill oloroso sherry, no age statement, September
2014 launch — are corroborated consistently across specialist-retailer
and review listings (Master of Malt batch OL1015 60.3%; The Whisky
Exchange batch OLO614; Distiller) found by web search on 2026-06-12.
Those pages return HTTP 403 to automated fetch, and the producer page
is JS-rendered / not directly fetchable. The specs are recorded with a
`trade_publication` citation and flagged for direct producer
confirmation. This is the weakest-sourced of the three bottlings.

## 5. Modelling decisions

- **The 12 Year Old's European oak.** The producer describes the 12 as
  a combination of American and European oak. The European-oak
  component is modelled with `oloroso-sherry-butt` (the project's
  species-agnostic European-oak sherry slug); the label does not
  specify the seasoning, so this is an interpretation, noted inline in
  the bottling.
- **The 15 French Oak Reserve's French oak** is modelled with
  `french-oak-cask` (virgin / new French oak), matching the producer's
  use of new Limousin oak. The Limousin specificity is the commonly
  cited description, flagged for producer confirmation.

## 6. Future cross-references

- `equipment/tall-narrow-neck-stills` is **queued** in TODO.md as a
  distillery-extension concept page. When it lands, add it to The
  Glenlivet's `distinctive_features` (currently empty to avoid a
  dangling reference) — the tall lantern stills with long necks are
  the natural anchor case for that page, alongside Glenmorangie and
  Old Pulteney.

## 7. Migration follow-ups (added to TODO.md Research Requests)

- Migrate the Wikipedia-sourced history, ownership and house-style
  claims to producer / scotchwhisky.com Whiskypedia primaries when
  those pages become fetchable.
- Confirm the post-2024 per-still capacities and washback count
  against a producer spec or the latest Malt Whisky Yearbook.
- Confirm the Nàdurra Oloroso and 15 French Oak Reserve specifications
  against producer-published sources.

## 8. Source-migration pass (2026-06-14)

Re-attempted the migration of the Wikipedia-sourced claims to producer /
scotchwhisky.com primaries. Outcome:

- **Still blocked:** theglenlivet.com (JS-rendered, no content to automated
  fetch), scotchwhisky.com Whiskypedia (HTTP 403), and the Wayback Machine
  (web.archive.org is not fetchable from this environment). The producer-
  primary migration remains pending.
- **Partial migration achieved:** added **Diffords Guide** (source 3,
  `trade_publication`) as an independent corroboration of the core
  identity/history claims — founding (1824, George Smith, first licence
  after the Excise Act), Pernod Ricard ownership, **Josie's Well** as the
  production-water source, unpeated malt, tall slim stills, and the **1884**
  "Glenlivet" trademark. This reduces the entry's sole-Wikipedia dependence
  on those claims.
- **New datum:** Diffords states **wooden washbacks** — recorded
  (`washbacks.material: wood`).
- **Conflict surfaced — global sales rank.** Wikipedia: second-biggest
  single malt globally (after Glenfiddich). Diffords: third. Both agree
  Glenlivet is the biggest single malt in the US. The ranking genuinely
  varies by year and measure (Glenfiddich, Glenlivet, Macallan, Singleton
  trade places); the description was softened to "second or third" with
  both sources cited rather than asserting one rank.
- **Conflict surfaced — county.** Diffords places the distillery in
  **Banffshire** (the historic county); the entry records **Moray** (the
  modern council area). Both are correct at different administrative layers;
  no change to the entry.
- **Confidence held at `medium`.** Diffords is a mid-tier trade guide, and
  the still count / capacity still rest on one trade source (Northern Scot)
  plus Wikipedia. The sourcing is stronger but not yet primary-grounded.
