# Talisker — population notes

Working notes for the 17th distillery entry (populated 2026-06-14).
Records sourcing limitations and modelling decisions behind the
`confidence: medium` rating.

## 1. Sourcing

- **Distillery + production line:** Wikipedia is the only directly-
  fetched source. The producer pages (malts.com / talisker.com) are
  JS-rendered and returned no content to automated fetch; scotchwhisky.com
  Whiskypedia returned HTTP 403. Migration to producer primaries is queued
  in TODO.md Research Requests.
- **Bottling specs** (45.8% ABV across the range; the Distillers Edition's
  ~6-month ex-amoroso finish; Storm's 2013 NAS launch and wider cask mix):
  Wikipedia lists the range members but not these specifics. They are
  corroborated consistently across specialist-retailer listings (The
  Whisky Exchange, Master of Malt, Comptoir Irlandais) found by web search
  on 2026-06-14. Those pages return 403 to automated fetch, so the specs
  carry a `trade_publication` citation and are flagged for direct producer
  confirmation. The 45.8% strength is one of the most universally-listed
  facts about Talisker and is treated as reliable.

## 2. Region — Islands vs Highland

Recorded as `region: Islands`, the customary trade grouping, matching
Highland Park and Harris. Under the Scotch Whisky Regulations 2009 Skye
falls within the **Highland** region; "Islands" has no formal status. The
inline comment records this.

## 3. Distinctive equipment

Talisker's character rests on a combination recorded in the description:
an asymmetric five-still set (two wash, three spirit), U-shaped lye-pipe
**purifier loops** that raise reflux, and **worm-tub** condensing on all
five stills. The purifiers push toward a lighter spirit while the worm
tubs (less copper contact) push toward a heavier, more sulphury one — the
two effects in tension are the signature. `distinctive_features` cross-
references `equipment/worm-tub` (Talisker is now a populated practitioner,
resolving that page's forward ref) and `glossary/reflux` (the purifier is
a reflux device, same class as Ardbeg's spirit-still purifier).
`distillery:talisker` was removed from `scripts/expected_dangling.txt`.

## 4. Modelling decisions

- **Amoroso finish → `oloroso-sherry-butt`.** The Distillers Edition
  finishes in ex-amoroso casks. Amoroso is a sweetened oloroso style; the
  project has no separate amoroso cask slug, so it is modelled with
  `oloroso-sherry-butt`, noted in the bottling's `finish` block. (The
  Lagavulin DE made the analogous call for its PX finish before the
  `pedro-ximenez-sherry-butt` slug existed.)
- **`peat_origin: mainland_scotland`.** Talisker does not malt on Skye;
  the malt is bought in from a Diageo mainland maltings (Glen Ord is the
  commonly-cited site, not confirmed in the surveyed sources), so the peat
  is mainland Scottish rather than island peat. The maltster field is left
  null pending confirmation.
- **Coordinates** (57.3017, -6.3537) are third-party-published values for
  Carbost, rounded to four places and marked approximate; migrate to a
  producer / OS source.

## 5. Ownership lineage

Wikipedia gives the milestones (MacAskill 1830; R. Kemp & Co. 1879;
Distillers Company 1925; United Distillers 1987; Diageo 1998). The
1879-1925 period passed through several owners (including the 1898
Dailuaine-Talisker merger in the wider literature); the entry keeps to the
sourced milestones and notes the period was multi-owner rather than
detailing each transfer.

## 6. Migration follow-ups (added to TODO.md Research Requests)

- Migrate the Wikipedia-sourced history, ownership and equipment claims to
  producer / scotchwhisky.com primaries when fetchable.
- Confirm the maltster (Glen Ord?), washback count/material, and mash-tun
  type against a producer spec or the latest Malt Whisky Yearbook.
- Confirm the bottling specs (45.8% ABV; DE amoroso finish; Storm cask
  mix) against producer-published sources.
