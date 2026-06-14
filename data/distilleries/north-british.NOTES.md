# North British — population notes

Working notes for the 19th distillery and the project's SECOND grain
distillery (populated 2026-06-14). North British is the confirming example
that turned the deferred grain-schema SCHEMA-OBSERVATIONS into structure.

## 1. Sourcing

Wikipedia is the only directly-fetched source for the distillery and line;
scotchwhisky.com Whiskypedia and producer pages were not fetched (403 / JS)
and are cited where they corroborate a figure, flagged for confirmation.
Confidence: medium.

## 2. Grain-schema structuring — CONFIRMED here

Cameronbridge (grain #1) introduced grain whisky and recorded its column
stills and cereal bill in prose, with SCHEMA-OBSERVATIONS to structure once
a second grain distillery confirmed the shape. North British is that second
example, and it confirmed the shapes — so the structured fields were added
(CHANGELOG [0.8.7]) and used here:

- `stills.column_stills: { count, still_type, notes }` — North British
  records `count: 4, still_type: coffey`.
- `cereal_bill: [{ cereal, proportion, malted, notes }]` — North British
  records the disclosed **maize 0.85 / malted_barley 0.15** split.

The **maize-vs-wheat contrast** between North British and Cameronbridge is
the substantive reason a structured cereal field was warranted rather than
a single free-text note: the two grain distilleries differ on their primary
cereal, and that difference is now queryable. Cameronbridge was retrofitted
from prose to the same fields in the same pass.

## 3. Ownership — 50:50 Diageo / Edrington joint venture

North British is co-owned in equal shares by Diageo and Edrington through
the Lothian Distillers Ltd joint venture — two competing majors sharing a
grain supplier. Recorded as `current: The North British Distillery Company
Ltd`, `parent: Lothian Distillers Ltd`, with the JV explained inline. This
is the first such co-ownership in the data set.

## 4. Source conflicts / gaps

- **Still count: three vs four.** Sources differ; recorded as four per
  Master of Malt, with the conflict noted inline. Confirm against a
  producer figure.
- **Capacity** (~65M LPA) is a 2007 Wikipedia figure quoted in "litres";
  recorded as LPA on convention. Confirm currency.
- **Coordinates and water source** left null; add from a producer / OS
  source.
- **Cereal proportions / new-make strength** (85/15, ~94.5% ABV) are from
  trade references (scotchwhisky.com), flagged for producer confirmation.

## 5. Bottlings — none (blending-grain supplier)

North British carries **no standing official single-grain bottling**, so
the production line's `bottlings` list is empty — the first populated
distillery with zero bottlings, and an honest reflection of a pure
blending-grain supplier. Its spirit reaches market as single grain mainly
through **independent bottlers** (Signatory, Hunter Laing, Lady of the
Glen, That Boutique-y Whisky Company's B10 25 Year Old), plus a 2018
official bottling released in collaboration with Douglas Laing.

**Follow-up:** add an IB single-grain worked example (e.g. a Signatory
North British, since the Signatory bottler entry exists) when a verifiable
specific release — vintage, cask, ABV — is identified. This would also be
the project's first independent-bottler GRAIN release.

## 6. Migration follow-ups (added to TODO.md Research Requests)

- Migrate distillery/line claims to scotchwhisky.com Whiskypedia and
  producer primaries when fetchable.
- Confirm the still count, cereal proportions, new-make strength, capacity
  currency, coordinates and water source.
- Add an IB single-grain worked example when a verifiable release surfaces.
