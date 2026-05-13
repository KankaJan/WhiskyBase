# Harris Entry — Field Notes & Source Discrepancies

A summary of fields where I had to make judgement calls, where data
conflicted across sources, or where the entries are deliberately
incomplete pending verification. Read this alongside the three YAML
files.

## Source-conflict resolutions

These are the points where reasonable, independent sources disagreed
and a call had to be made.

**Mash tun grist weight.** Five sources state 1.2 tonnes, one
(whisky.com) states 1.5 tonnes. Resolved to 1.2 t. The 1.2 figure
is corroborated by a distiller's own interview describing a single
mash, which makes it the most authoritative.

**Washback count.** Three sources (Scotch Whisky, Visitors' Guide,
Two Whisky Bros) say 5 washbacks; two (whisky.com, Distilando) say 8.
Resolved to 5 with an explicit note. The 5-figure is in the most
structured spec sheet (Scotch Whisky Whiskypedia) and is consistent
with an in-person visit account. Worth confirming by direct contact
with the distillery if Harris remains a high-confidence reference
entry.

**Washback material.** Oregon pine vs Douglas fir. Resolved to Oregon
pine — the species call from whisky.com (Douglas fir) is a single
discrepant source and is likely an error.

**Annual capacity.** Three figures appear: 230,000 lpa (Scotch Whisky,
Two Whisky Bros, recent), 400,000 lpa stated capacity with ~200,000
operational (Distilando), and 180,000 lpa (older Whiskipedia entry).
Used 230,000 as the current figure with a note acknowledging the
range.

**Still shape.** Scotch Whisky Whiskypedia describes both stills as
"onion"; one earlier source described "lantern". The categorical
boundary between onion and lantern is fuzzy in practice (lanterns are
a type of onion with a more pronounced waist). I used "onion" since
it appears in the more recent structured spec.

**New-make ABV.** 69% per the structured Scotch Whisky entry; 69.5%
implied by some secondary writing. Used 69%.

## Fields left null pending verification

These entries are honest gaps rather than research failures — the
information either isn't publicly disclosed, isn't yet captured in
the sources I consulted, or is producer-private.

**Distillery:**
- `wikidata_qid` — Wikipedia entry exists; QID lookup deferred.
- `coordinates` — approximated; should be verified against an
  authoritative geographic source (OSM, official data).
- `warehouse.type` — dunnage vs racked not consistently reported.

**Production line:**
- `fermentation.yeast` — not publicly disclosed; this is normal,
  most distilleries don't publish yeast strain.
- `distillation.spirit_cut.start_abv` and `.end_abv` — Harris cuts
  by nose, not to fixed ABV triggers, so these may never be
  populatable in numeric form. The `notes` field captures the
  qualitative practice.
- `external_ids.whiskybase_id` — to locate.

**Bottling:**
- `batch_or_cask.outturn_bottles` — Batch 1 outturn not publicly
  disclosed at release. Batch 5 figure (12,326) given as comparator.
- `maturation[*].proportion` — specific Batch 1 cask split not
  disclosed; Batch 5 split (85/11/4) given as comparator.
- `maturation[*].duration_years` — not disclosed per cask.
- `rrp.amount` — known to be sub-£100, exact figure not in current
  source set. Worth a single targeted lookup.
- `notes_independent[*]` nose/palate/finish split — the one
  independent review I cited covers Batch 1 but doesn't cleanly
  separate nose/palate/finish in a way that maps to the schema's
  fields. Captured as a summary instead.

## Voice / register notes

Two places where the source material's tone made the discipline
notably hard:

**Distillery `description` field.** The producer's own writing about
Harris is unusually marketing-heavy — Gulf Stream, machair flowers,
"oldest rocks on earth", "softest water of any Scottish distillery".
The description was deliberately stripped of all evaluative language
and reduced to: founding date, founders, funding source, equipment,
ownership, water source, and physical climate. The "oldest rocks"
geology fact was kept because the geological age of Lewisian gneiss
is verifiable and has a relevant production consequence (low
mineralisation of source water). The "softest water of any Scottish
distillery" claim was *not* kept because it's an unverified
superlative.

**Producer tasting notes.** The Head Blender's notes are quite
romantic in style ("island home fires", "machair flowers"). I
preserved them as attributed quotation rather than restating them
as fact, which is the right discipline — these are one informed
person's subjective impressions, not properties of the liquid.
The schema's separation of `notes_official` vs `notes_independent`
makes this clean.

## What this exercise revealed about the schema

Three small refinements worth considering before populating a
second distillery:

1. **`peating_ppm` as a list `[min, max]` works well**, but a
   third value is sometimes useful: the *measured* PPM for a
   specific batch, separate from the disclosed spec range. For
   Harris, spec is 12–14 ppm but Batch 5 was measured at ~12.1.
   This may live more naturally on the bottling than the line.
   Worth deciding before adding the next peated line.

2. **`maturation` on bottlings would benefit from a `share_of_total`
   field at the top level**, alongside the per-cask proportions, to
   distinguish "85% bourbon" (where bourbon is one bucket) from
   "21% Heaven Hill bourbon, 64% Buffalo Trace bourbon" (where
   bourbon splits into two cooperage-distinct buckets that are
   logically grouped). Current schema handles this via separate
   list entries with a shared `cask_type`, which works but doesn't
   express the logical grouping.

3. **The `warehouse` field on distillery is too thin.** Harris has
   one on-site warehouse and one off-site warehouse on a sea loch.
   Different distilleries split inventory across many warehouses
   with different microclimates. A list of warehouse objects would
   model this better than the current single object. Defer until
   a second distillery makes the case.

None of these block the v0.1 schema. Note them and revisit after
2–3 more distilleries are populated.

## Recommended next steps

- Decide which distillery to populate second. A well-documented
  Speyside or Islay site (Glenfarclas, Springbank, Laphroaig)
  would stress-test the schema against rich-history, multi-line,
  multi-decade content.
- Begin sketching the `concept` schema. Several Harris fields
  reference concepts that don't yet exist (community-employer model,
  locally-cut peat, soft water sources). Even three or four concept
  pages would let the cross-link mechanism start earning its keep.
- Locate Whiskybase IDs for the line and bottling. Even without
  using their content, having the IDs stored is the foundation for
  all future enrichment.
