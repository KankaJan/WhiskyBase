# Ardbeg — source conflicts and methodology notes

Companion notes to `data/distilleries/ardbeg.yml`,
`data/production_lines/ardbeg.yml` and the Ardbeg bottlings.
Records the source conflicts resolved in those entries, per the
project's source-conflict policy (`docs/source-conflict-policy.md`).

## Founding date — illicit vs commercial

Distilling is reported on the Ardbeg site from roughly 1794 as an
illicit operation; 1815 is the licensed-commercial founding under
John McDougall. The entry records `founded: 1815` (the commercial
date, consistent with how the project dates the other Islay
distilleries) and notes the earlier illicit activity in prose.

## Peating — 50 ppm spec vs ~55 ppm as delivered

Trade sources give Ardbeg's malt peating specification as about
50 ppm, while also reporting the malt as delivered to average
closer to 55 ppm phenols. Both figures are recorded — the 50 ppm
specification and the ~55 ppm as-delivered average — rather than
smoothed to a single number. The malt is bought in (Ardbeg does
not floor-malt on site).

## Still count — the 2019 doubling

Before 2019 Ardbeg operated a single pair of stills (one wash,
one spirit). A new still house completed in 2019 doubled the
count to two pairs (2 wash + 2 spirit). The entry records the
current post-2019 configuration; the pre-2019 single pair is
noted in `equipment_changes`.

## Annual capacity — left null

Trade sources give a pre-2019 annual capacity on the order of
1.4 million LPA. The 2019 still house was built explicitly to
double Ardbeg's distilling capacity, which would put the current
figure on the order of ~2.4 million LPA — but no clean
producer-published post-expansion capacity figure was found in
the surveyed sources. `annual_capacity_lpa` is therefore left
`null` rather than recording either a stale pre-expansion number
or an un-sourced derived estimate. Update when a producer figure
surfaces.

## Mothballed period — recorded as one span

Production was halted in 1981, ran intermittently at a low level
from 1989 to 1996, and the distillery was then idle until the
June 1997 revival. This is recorded as a single mothballed span
(1981-1997) with the intermittent 1989-1996 runs described in the
`notes`, rather than split into several micro-periods.
