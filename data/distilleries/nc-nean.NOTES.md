# Nc'nean — population notes

21st distillery; first of the 2026-06-14 new-wave batch. Confidence medium
(Wikipedia + producer/trade references; producer pages JS-rendered to
automated fetch).

- **STR red-wine casks modelled as `wine-cask`.** The flagship is led by
  STR (shaved, toasted, re-charred) red-wine casks. The project has no
  STR-specific cask slug, so the generic `wine-cask` is used with a note. If
  STR maturation recurs across distilleries, consider an `str` flag or a
  dedicated cask entry.
- **Organic / net-zero / B Corp** are distillery-level sustainability and
  certification claims with no schema field; captured in the description.
  If a `certifications` / `sustainability` field is ever wanted, Nc'nean is
  the driving example.
- **Single stills, ~100,000 LPA** — among the smallest in the data set.
- Coordinates left null; add from a producer / OS source.

Migration follow-ups (TODO Research Requests): migrate to producer
primaries; confirm cask proportions, barley variety, and coordinates.
