# Cameronbridge — population notes

Working notes for the 18th distillery entry and the project's FIRST grain
distillery (populated 2026-06-14). Records the sourcing limitations and —
importantly — the schema observations that grain whisky surfaces, so the
malt-centric schema can be extended deliberately once a second grain
distillery confirms the right shapes.

## 1. Sourcing

Wikipedia is the only directly-fetched source for the distillery and
production line. scotchwhisky.com Whiskypedia (Cameronbridge 1997; Cameron
Brig 1996) and producer/Diageo pages were not fetched (403 / JS-rendered);
they are cited where they corroborate a bottling spec, flagged for direct
confirmation. Confidence: medium, consistent with the other
Wikipedia-primary distillery entries.

## 2. SCHEMA-OBSERVATIONS — grain whisky vs a malt-centric schema

The distillery / production_line schemas were designed around batch
pot-still malt production. Grain whisky differs in three structural ways.
Per the project's pressure-test-then-structure practice (how the bottler
and supplier schemas evolved), the necessary regime change was made at
population; the column-still and cereal-bill structures were then added
2026-06-14 when North British (the second grain distillery) landed and
confirmed the shapes (CHANGELOG [0.8.7]). This entry has been retrofitted
to use them.

1. **Distillation regime — DONE (additive).** `distillation.regime` gained
   `continuous` (column / Coffey), CHANGELOG [0.8.6]. This was necessary:
   grain distillation is not any of the batch pot-still regimes, so the
   entry could not validate without it.

2. **Column / Coffey stills — DONE (structured 2026-06-14).** Added
   `stills.column_stills: { count, still_type: coffey|patent|other, notes }`
   (the pot-still slots remain null for grain). Cameronbridge records
   `count: 3, still_type: coffey`.

3. **Cereal / grain bill — DONE (structured 2026-06-14).** Added
   `cereal_bill: [{ cereal, proportion, malted, notes }]` on the production
   line. Cameronbridge records wheat (malted: false) + malted_barley
   (malted: true), proportions null (not sourced); North British — the
   confirming example — records the disclosed maize / malted-barley 85/15
   split.

## 3. Other observations

- **Capacity "litres" vs LPA.** Wikipedia states ~136 million litres;
  `annual_capacity_lpa` records 136,000,000 on the convention that
  distillery capacity is quoted in LPA. Confirm against a producer figure.
- **Coordinates left null.** Not captured in the surveyed sources; add from
  a producer / OS source. (Cameronbridge is a production site, not a visitor
  distillery.)
- **Grain-bill proportions** (wheat vs malted barley) are general
  grain-whisky practice, not Cameronbridge-specific in the surveyed sources.
- **Bottling colour / chill-filtration.** Cameron Brig is a standard 40%
  single grain (conventionally chill-filtered and coloured), but the
  surveyed sources do not state this firmly, so `non_chill_filtered` /
  `natural_colour` are left null rather than asserted.

## 4. Migration follow-ups (added to TODO.md Research Requests)

- Migrate distillery/line claims to scotchwhisky.com Whiskypedia and
  producer/Diageo primaries when fetchable.
- Confirm the column-still count/type, the wheat/malted-barley grain-bill
  proportions, the new-make distillation strength, and the capacity basis.
- Confirm the bottling specs (Cameron Brig colour/filtration; Haig Club /
  Clubman cask and launch details) against producer sources.
