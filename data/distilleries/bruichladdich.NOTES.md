# Bruichladdich Entries — Field Notes & Source Discrepancies

A summary of decisions made during research, source conflicts, and
observations about how the schema held up during this larger
populated-data exercise.

## Source-conflict resolutions on the distillery entry

**Mash tun grist weight: 7 tonnes vs 6.2 vs 6.63.** The 7-tonne figure
is consistent across the producer's own communications, Diffords, and
Wikipedia. The 6.63-tonne figure in the Scotch Whisky structured spec
sheet is the working grist charge per mash, not vessel capacity. The
6.2-tonne figure in one secondary source appears to be an error.
Resolved to 7 tonnes capacity with a comment.

**Wash still capacity.** Genuinely contested between sources:
- Diffords: 12,500 L each (2 stills)
- Scotch Whisky structured: 17,500 L size with 11,500 L charge
- Wikipedia: 23,000 L total (i.e. 11,500 L each)
- Whisky.com: ~12,000 L each
- Maltspedia: ~12,000 L

The most likely explanation: 17,500 L is total vessel capacity per
still; 11,500 L is typical working charge. Sources reporting "12,500"
or "12,000" appear to be conflating capacity and charge. Resolved to
the Scotch Whisky figures with explicit explanation in the entry.

**Spirit still capacity.** Same problem, even larger spread:
- Diffords: 7,100 L each
- Scotch Whisky: 12,500 L size with 9,000 L charge
- Wikipedia: 21,000 L total (~10,500 L each)
- Whisky.com: ~11,000 L each

Resolved to Scotch Whisky figures (12,500 L size / 9,000 L charge).
The Diffords 7,100 L figure is suspicious — likely a transcription or
unit confusion.

**Washback construction species.** Wikipedia notes that "Oregon pine"
and "Douglas fir" are sometimes used interchangeably in industry
parlance for the same species (Pseudotsuga menziesii). This is a
naming, not a material, discrepancy and the entry treats them as
equivalent.

**Mothballed period exact dates.** Wikipedia gives the closure as 1994
("shut down as being surplus to requirements"). Scotch Whisky and
other sources sometimes cite 1995 for the actual cessation of
production. The entry uses 1994-2001 as the conservative closure
window, with the December 2000 acquisition date noted separately.

## Source-conflict on Octomore 8.2 ABV

58.4% per producer-aligned sources (Whisky Saga, Spirit Radar,
Drinkhacker — the last gives 116.8 proof which converts to 58.4%).
The Whisky Club source gives 58.7%. Resolved to 58.4% with a note;
the Whisky Club figure is treated as a minor error.

## Schema observations from this exercise

**The new `peating` block earned its complexity in the Octomore line.**
Without it, the 309.1 ppm Octomore 8.3 measurement would have been
indistinguishable from a 309.1 ppm in-bottle measurement, or a 309.1
ppm by 4-aminoantipyrine. The explicit method declaration ("Using
HPLC...") in the Bruichladdich press materials is exactly the kind
of detail that the schema can now record cleanly. For the
Bruichladdich and Port Charlotte lines (single fixed PPM specs) the
schema is more verbose than necessary, but the verbosity is harmless
and the consistency is valuable.

**Source-level methodology declaration is the right pattern.** The
Bruichladdich entries demonstrate this clearly: every measurement
from Bruichladdich-derived sources resolves method via the source's
methodology block, without restating it per-figure. This kept the
measurement entries uncluttered while preserving full traceability.

**The "deliberately undisclosed" case (Black Art) needs a first-class
concept slug.** Currently the bottling uses `cask_type:
undisclosed-cask` as a placeholder. This is information, not
absence — the producer has actively chosen to withhold the data. The
cask schema (TODO) should include an `undisclosed` cask type as a
named concept distinct from `null` (unknown). This will let the
build report "X bottlings have undisclosed cask provenance" as a
distinct category from "X bottlings lack data we should track down".

**Re-cask vs finish boundary is fuzzy.** Port Charlotte PMC:01 spent
4 years in bourbon and 5 years in Pomerol — the Pomerol phase is
longer than the bourbon phase. Calling it a "finish" feels wrong;
the schema's `maturation` (multi-stage) field represents this better
than `finish` does. Octomore 8.2's 6+2 split is genuinely ambiguous —
producer calls the 2-year Amarone phase a finish, but two years is
substantial. The schema accommodates both interpretations; the
documentation should explicitly note that "finish" is reserved for
shorter terminal cask exposure (typically <12 months) and longer
secondary maturations should use additional `maturation` entries.

**Multi-line distilleries work cleanly.** The three Bruichladdich
production lines reference shared equipment via the parent
distillery, with distinct recipe variables (peating, cask programme)
on each line. This was the biggest unproven dimension of the schema
and it held up well. Most fields on the lines are similar (same
fermentation, same distillation, same equipment) which would invite
copy-paste — but separation is correct because future divergences
(e.g. Octomore distilled with different cuts to handle high-PPM
spirit) need a place to land.

**Annual-edition releases worked.** The three Octomore 8.x bottlings
are sibling entries under the same line, with each recording its
own peating, cask programme, and ABV. Slug convention
`<distillery>-<line>-<edition>-<variant>` (e.g.
`bruichladdich-octomore-8-3`) is sortable and predictable. Should
extend cleanly to the rest of the Octomore series and to other
edition-numbered releases (Lagavulin Distillers Edition, Glenfarclas
Family Casks, etc.).

## Fields left null pending follow-up

These are honest gaps. None block the entries; all are documented
above as TODO inline.

**Bruichladdich distillery:**
- `wikidata_qid`
- `mothballed_periods[0]` (the 1929-1936 period — exact dates need
  verification against a primary historical source rather than
  inferred from secondary references)

**Bruichladdich line:**
- `fermentation.yeast` — Mauri/Kerry strains reported by single
  source only; not corroborated.

**Port Charlotte line:**
- No significant gaps.

**Octomore line:**
- `distillation.new_make_abv` — assumed 68.5% from site-level fill
  strength, not separately verified for Octomore.

**Bottlings:**
- Several `outturn_bottles` figures unknown (Octomore 8.1, Classic
  Laddie batches).
- Several Whiskybase IDs not yet located for Bruichladdich line
  releases.
- Classic Laddie RRP varies by market and batch; an averaged figure
  used.
- Bruichladdich Islay Barley 2014 UK GBP RRP not in current source
  set.

## Recommended next steps

- Build the concept schema (`/data/concepts/`) and create the four
  highest-priority concept pages (see TODO.md).
- Build the cask schema (`/data/casks/`) with `undisclosed-cask` as
  an explicit first-class entry.
- Locate Whiskybase IDs for the Bruichladdich line bottlings.
- Decide whether Classic Laddie should remain a single bottling
  entry or be split into per-batch child entries. Recommend deferring
  this decision until at least one other transparent-batch SKU is
  encountered (e.g. Springbank Local Barley releases, Glenfarclas
  Family Casks).

## Port Charlotte Islay Barley 2014 — label age vs elapsed maturation

The bottling is labelled "Aged 7 Years" but was distilled in 2014 and
bottled 26 July 2023 — an elapsed period of approximately 9 years. This
is not an arithmetic error in the data. Bruichladdich (and Scotch
labelling generally) follows the SWA minimum-age convention: the stated
age is the age of the youngest cask in the vatting, not the elapsed
time from vintage. The producer does not publish a youngest/oldest
breakdown for this release; the component casks were filled in 2014 and
emptied 26 July 2023.

Resolution in the entry:
- `age_statement: 7` (producer label).
- `vintage: 2014` (producer label).
- `release_date: 2023-07` (producer-stated bottling date).
- `duration_years: 9` per cask (actual elapsed maturation rather than
  label age). The maturation block carries an inline comment recording
  the convention.

Sources verifying the producer's published facts: bruichladdich.com
product page, Whiskybase #226735, Whisky Exchange, Master of Malt,
Drinkhacker (2 Jul 2023 review), The Whiskey Wash, Dramface, The Whisky
Barrel — all align on vintage 2014, age 7, bottled 26 July 2023.
