# Source conflict policy

When sources disagree — and they do, often — the project treats the
disagreement as data rather than smoothing it away. This document
records how.

---

## Core rules

1. **Resolve to one figure in the entry.** Pick the most reliable
   source for the type of claim being made and write that figure
   into the entry.

2. **Document the choice inline.** A YAML comment next to the
   chosen figure explains briefly which sources disagreed and why
   the chosen one wins. Keep this short — detail goes in (3).

3. **Preserve the conflict in `<entity>.NOTES.md`.** A markdown
   notes file sibling to the YAML records the conflict in full:
   which sources said what, what the resolution was, what would
   change our mind. Future contributors can re-evaluate without
   re-doing the research.

4. **Never silently round, average, or smooth.** If two sources
   give 17,500 L and 12,500 L, the entry records one of those
   figures. It does not record 15,000 L. Averaging produces a
   number that no source supports.

5. **Wrong sources stay cited.** If Source X gives a figure we
   reject, the entry still lists X in `sources:` with a note
   explaining why we don't use its figure. Removing the source
   would erase the reason the resolution happened.

---

## Source reliability hierarchy

Not strict — exceptions exist — but a useful default.

| Tier | Source type | Notes |
|---|---|---|
| 1 | Primary database (PubChem, NIST WebBook, IUPAC, INAO regulatory text, Code of Federal Regulations, ChemSpider) | Authoritative for chemical compound identity, appellation regulations, distilled-spirits regulatory rules. Stable and citable by anchor ID where applicable. |
| 1 | Producer's structured spec sheet | Best for current equipment, recipe, malt spec |
| 2 | Producer-authored prose page | Authoritative on intent, sometimes loose on numbers |
| 2 | Peer-reviewed journal paper (Journal of the Institute of Brewing, food chemistry, oak chemistry) | Authoritative for whisky-chemistry claims. Underused in current data; see TODO Research Requests. |
| 3 | Scotch Whisky Whiskypedia structured page | Excellent for current production specs, well-curated |
| 3 | Diffords Guide / Whisky.com / Master of Malt | Mixed; reliable when consistent with tier 1-2, suspect when alone |
| 3 | Reputable independent reviewer with named author | Good for personal observations and tasting notes; less reliable for equipment numbers |
| 3 | Wikipedia entry | **Volatile source** — entries change without notification. Use as a starting point but prefer the primary sources Wikipedia itself cites where available. See "Wikipedia volatility caveat" below. |
| 4 | Retailer product pages | Often copies producer text but sometimes introduces errors |
| 4 | Independent reviewer without named author | Use with caution |
| 5 | Forum posts, social media, AI-generated content | Avoid as primary source; treat only as pointer to real source |

## Wikipedia volatility caveat

Wikipedia is treated as a volatile source: entries change without
notification, can be subject to vandalism between revisions, and
their citation graphs evolve as editors come and go. The project
prefers more solid resources where they are available and
accessible.

Specifically:

- **For chemical compound identity** (formula, structure, IUPAC
  nomenclature, CAS number), cite **PubChem**
  (`pubchem.ncbi.nlm.nih.gov/compound/<CID>`) or another primary
  chemistry database (NIST WebBook, ChemSpider). PubChem entries
  are anchored to a Compound ID (CID) that does not change; the
  underlying data is curated against authoritative chemistry
  references. Use `type: chemistry_database` for source classification.
- **For appellation/AOC regulations** (Pomerol, Pauillac, Sauternes,
  etc.), cite the appellation council's technical publication or
  the INAO regulatory text rather than the Wikipedia summary.
- **For US distilled-spirits regulation** (the bourbon new-oak
  rule etc.), cite the Code of Federal Regulations directly
  (`ecfr.gov`).
- **For Scotch industry technical claims** (peating methods,
  fermentation effects, copper-catalysis chemistry), cite the
  primary research literature (SWRI publications, papers in the
  Journal of the Institute of Brewing, Conner et al. on flavour
  chemistry) rather than Wikipedia secondaries.

Where Wikipedia is currently cited and a better source has been
identified, the entry should be migrated. Where a better source
has NOT been identified, the entry remains with the Wikipedia
citation and a corresponding "research request" item appears in
`TODO.md` under the Research Requests section.

Wikipedia citations remain acceptable for:

- Historical facts about a distillery's ownership lineage where
  Wikipedia is itself drawing on documented sources and the claim
  is non-contentious.
- Geographic and administrative facts that are well-established
  and not subject to revision (e.g. that Pauillac is in the
  Médoc).
- General context where the claim is non-load-bearing for the
  entry's value.

## Source-type vocabulary

The `type:` field on source entries uses the following vocabulary:

- `official_website` — producer's own website or other
  first-party publication
- `trade_publication` — third-party Scotch industry coverage
  (Scotch Whisky magazine, Diffords, Whisky.com, etc.)
- `wikipedia` — Wikipedia entry. Volatile (see above).
- `chemistry_database` — primary chemistry database (PubChem,
  NIST WebBook, etc.). Type introduced 2026-05-15.
- `regulatory_text` — government or appellation-council
  regulatory publication (US Code of Federal Regulations, INAO
  *cahier des charges*, Consejo Regulador del Vino de Jerez DO
  text, Italian DOC/DOCG ministerial publications). Type
  introduced 2026-05-15.
- `independent_review` — named-author tasting notes or visit
  accounts
- `peer_reviewed_paper` — journal paper. Reserved for future use
  as research-request items are resolved.

**Trade press writers can be wrong.** Drinkhacker, Whisky Advocate,
The Whiskey Wash, Scotch Whisky magazine all employ professional
writers who fact-check, but individual articles still contain
transcription errors. When trade press disagrees with the producer,
default to the producer for current production specs and to the
trade press for context, history, and reception.

**The producer can be wrong about their own equipment.** Marketing
copy sometimes uses figures (still height, washback count) that
don't match working specs. Where a producer's marketing page
disagrees with their own structured spec sheet, the structured
spec sheet wins.

---

## Worked examples from existing entries

### Bruichladdich still capacity

The data:

- Diffords Guide: wash 12,500 L each, spirit 7,100 L each
- Scotch Whisky structured: wash 17,500 L size / 11,500 L charge;
  spirit 12,500 L size / 9,000 L charge
- Wikipedia: 23,000 L wash total; 21,000 L spirit total (i.e.
  ~11,500 L and ~10,500 L per still)
- Whisky.com: wash ~12,000 L, spirit ~11,000 L
- Maltspedia: wash ~12,000 L, spirit ~11,000 L

The resolution: Scotch Whisky figures (17,500 L size / 11,500 L
charge for wash; 12,500 L size / 9,000 L charge for spirit). Why:
they're the only set internally consistent across size-vs-charge.
The "12,500 L" wash figure from Diffords is plausibly a charge
figure mislabelled as capacity. The "7,100 L" spirit figure from
Diffords is unexplained and suspicious. The Wikipedia totals match
the Scotch Whisky charge figures (11,500 × 2 = 23,000), supporting
the hypothesis that other sources are confusing capacity and
charge.

In `bruichladdich.yml`, inline:

```yaml
capacity_litres: 17500        # Per Scotch Whisky structured spec [3].
                              # NOTE: still capacity figures conflict
                              # significantly between sources. See
                              # bruichladdich.NOTES.md for full
                              # reconciliation.
```

In `bruichladdich.NOTES.md`, the full breakdown above.

### Harris washback count

Three sources give 5 washbacks; two give 8. Resolved to 5: the
Scotch Whisky Whiskypedia structured spec sheet and an independent
visit account both report 5, and the producer-aligned distiller
interview in Scottish Field is consistent with the 5-washback layout.
The two secondary sources reporting 8 (Distilando and whisky.com)
are not adopted; the discrepancy is treated as inherited error rather
than evidence of a real expansion.

### Octomore 8.2 ABV

Five sources give 58.4%; one (The Whisky Club) gives 58.7%. Resolved
to 58.4%; the outlier is treated as a transcription error and the
source is retained in `sources:` with a note.

---

## When to escalate confidence: low → medium → high

A `confidence` field on every entry takes values `stub | low |
medium | high`. The rules:

- **stub.** Identity fields only; most content placeholder. Useful
  for known-incomplete entries that need to exist for cross-reference
  reasons.
- **low.** Some content but major gaps, single-source dependencies,
  or unresolved conflicts that block confident reporting.
- **medium.** Multiple sources consulted, conflicts resolved with
  reasoning, fields mostly populated but with documented gaps. The
  Harris distillery entry sits here because some equipment figures
  rely on one source only.
- **high.** 5+ sources, all major conflicts resolved with reasoning,
  no significant gaps, the entry would survive a careful audit. The
  Bruichladdich distillery entry sits here.

`confidence: high` is not "we're sure." It's "we've done the work
and could defend every decision in the entry against a serious
reviewer." Don't claim it lightly.

---

## When sources don't disagree, they're still uncertain

Some figures are quoted from a single source because no other source
discusses the field. These are *not* conflict cases, but they're
also not high-confidence facts. Record the single source and treat
the figure as provisional until a second source either confirms or
contradicts.

The two-yeast-strains claim in the Bruichladdich production line
entry is an example: one source (finedrams.com) reports "Mauri and
Kerry" yeast strains; no other source corroborates. The figure is
in the entry with a `TODO: verify` note.

---

## What this policy doesn't cover

- Tasting notes from different reviewers will give different
  impressions. That's the nature of sensory assessment, not a
  source conflict. Multiple notes go in `notes_independent` as a
  list; the schema accommodates disagreement directly.
- The producer's own characterisation of a release ("fruity and
  floral") can coexist with independent reviewers' contradictory
  notes; both go in the entry, attributed.
- Auction prices and current secondary-market values are out of
  scope entirely; this policy does not apply.
