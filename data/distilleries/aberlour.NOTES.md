# Aberlour — population notes

Working notes for the 20th distillery entry (populated 2026-06-14).

## 1. Sourcing

Wikipedia is the only directly-fetched source for the distillery and line;
bottling specs are corroborated by specialist-retailer listings (Master of
Malt, whisky.com). Producer pages were not fetched. Confidence: medium.

## 2. Source conflicts / decisions

- **Water source — conflict.** Recorded `St Drostan's Well`, the source
  long associated with Aberlour in the producer's account and whisky
  references. Wikipedia's infobox instead lists "Birkenbush / Target
  spring". Both are recorded (entry value + inline note); confirm against a
  producer source. (St Drostan's Well is the widely-cited name but was not
  in the single fetched source, hence flagged.)
- **Founding date.** Recorded 1879 (James Fleming's rebuild, the founding
  date of record) [1]; an earlier distillery occupied the site from 1826.
- **Spirit stills differ in size.** Two spirit stills at 20,000 L and
  15,456 L [1]; the `still` schema holds a single `capacity_litres`, so the
  spirit-still `capacity_litres` is left null and both sizes are given in
  `stills.notes`. (A future schema could model per-still capacities, but a
  single asymmetric pair does not justify it — note for if it recurs.)
- **Banffshire vs Moray.** Charlestown of Aberlour is in the historic
  county of Banffshire; the entry records the modern council area, Moray.

## 3. A'bunadh — no single ABV

A'bunadh is cask strength and genuinely batch-variable (~59-61% ABV across
its numbered batches), with no fixed value, so `abv` is recorded null with
the range in the field note rather than inventing a representative figure.
`cask_strength: true`, `non_chill_filtered: true`, `natural_colour: true`,
first-fill oloroso, NAS.

## 4. Migration follow-ups (added to TODO.md Research Requests)

- Migrate the Wikipedia-sourced history/equipment to producer primaries
  when fetchable; resolve the water-source conflict (St Drostan's Well vs
  Birkenbush / Target spring).
- Add coordinates from a producer / OS source (left null).
- Confirm the bottling specs (A'bunadh first-fill-oloroso / cask strength;
  12 and 16 Double Cask ABV and cask mix) against producer sources.
