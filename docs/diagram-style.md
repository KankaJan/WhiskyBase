# Diagram style spec — WhiskyBase

Diagrams in WhiskyBase are deterministic, hand-authored or
data-driven SVG. They are version-controlled as text, carry no
baked-in colour, and inherit the site theme. AI image generation
is not used: it is unsourceable, hallucination-prone, and cannot
plot real data — see `TODO.md` Beta-readiness for the rationale.

This document is the authoring spec. The reference
implementation is `data/diagrams/pot-still.svg`.

## Two visual registers

WhiskyBase diagrams use **two** registers, chosen by what the
diagram is.

**Hardware and process schematics** — the pot still, mash tun,
washback, worm tub, the production-chain flowchart — use a
deliberate **hand-drawn sketch** register: the look of an expert
sketching on paper to illustrate "this is the thing we are
discussing." They are explicitly **not** precision blueprints.

**Technical data graphs** — the spirit cut, cask-maturation
kinetics — use a **strict** register: precise axes, real tick
values, no wobble filter. Where a diagram plots data it must be
plotted *exactly* from a sourced figure (see "Data graphs"
below). Rule of thumb: hand-drawn is fine for hardware, but where
a diagram gets technical, keep it strict.

The rest of this section concerns the hand-drawn schematics.

This is not only an aesthetic choice — it is honest about what
the diagrams are. A concept-page schematic (the pot still, the
mash tun) is generic and indicative, not to scale. Pot stills
vary enormously between distilleries, and that variation is
itself a teaching point; there is no single canonical geometry
to draw. A crisp dimensioned blueprint would signal a precision
the drawing does not have, and would require measurements the
project does not hold: the distillery `stills` data carries
volumes (`capacity_litres`) sparsely and almost no geometry
(`height_m` is null for nearly every entry; `lyne_arm_angle` is
descriptive — "ascending" / "descending" — not a numeric angle).
A measured blueprint would therefore mean fabricating numbers,
which the sourcing policy forbids. The wobbly sketch line is the
register that matches the evidence: indicative, not metrological.

A true measured blueprint is only defensible for a *specific
named still* backed by sourced dimensions — not for the generic
concept-page diagrams. It is not planned for beta.

## Where files live

- SVG files: `data/diagrams/<slug>.svg`.
- A concept entry declares its diagrams in the `diagrams:` list
  (`file`, `alt`, `caption`, `source_id`) — see
  `schema/concept.template.yml`.
- The loader (`site/src/lib/data.ts`, `attachDiagramSvg`) inlines
  the SVG markup at build time; the concept detail page renders a
  `<figure>` with caption and source citation.

## Markup conventions

- Root `<svg>` carries a `viewBox` and **no** fixed `width` or
  `height`, so it scales to the container. Add `class="wb-diagram"`.
- Accessibility: a `<title>` and `<desc>`, referenced from the
  root via `aria-labelledby`. `<desc>` should describe the
  diagram in plain prose.
- Structural outlines: `stroke="currentColor"`, `fill="none"`,
  `stroke-width="2.5"`, round joins and caps. `currentColor`
  resolves to the page text colour.
- Labels and leader lines: the `--muted-color` theme token
  (`fill="var(--muted-color)"` for text,
  `stroke="var(--muted-color)"` for leaders).
- No baked-in hex colours anywhere. The diagram must read
  correctly in both light and dark theme.
- Label text: `font-size="14"`, no font family (inherits the
  page body font).
- **Label placement.** Every label sits *outside* the figure's
  bounding box, in the surrounding margin — never overlaid on
  the drawing. A leader line connects label to part. The leader
  travels only through clear margin and terminates *at* the
  edge of its part; it must never cross any other drawn line.
  Size the `viewBox` to leave margin on all four sides for the
  labels, and check that no `<text>` is clipped at a viewBox
  edge — long captions need the width budgeted for them.

## The sketch filter

This applies to hardware and process schematics only; the
strict data graphs carry no filter.

The hand-drawn finish is produced by a pure-SVG filter — no
library, no JavaScript. A `feTurbulence` node generates a fixed
fractal-noise field; a `feDisplacementMap` node pushes every
stroke sideways by an amount sampled from that noise:

```xml
<filter id="sketch-<slug>" x="-15%" y="-15%"
        width="130%" height="130%">
  <feTurbulence type="fractalNoise" baseFrequency="0.014"
                numOctaves="2" seed="9" result="noise"/>
  <feDisplacementMap in="SourceGraphic" in2="noise" scale="6"/>
</filter>
```

- `scale` is the wobble amplitude. The project standard is
  **6** (the "heavy sketch" level).
- `baseFrequency` is the wobble wavelength — `0.014` gives long,
  relaxed waves rather than fine jitter.
- `seed` is fixed, so the result is fully deterministic and
  reproducible — the SVG remains a stable text artefact.
- The filter operates after paint, so `currentColor` and the
  theme tokens still resolve; the diagram still recolours with
  light / dark mode.
- Apply the filter to the structural line-work, the leader
  lines, and any incidental marks — but **never to `<text>`**.
  Filtered text smears and loses legibility; labels stay crisp,
  outside the filter.
- Give the filter a **per-file id** (`sketch-<slug>`). Several
  diagrams may be inlined into one page; a shared `id` would
  collide.

## Sourcing

A diagram is a claim like any other. Its schematic content must
be grounded in the cited source; `source_id` on the diagram
entry points at the concept's `sources:` block. Document the
grounding in an XML comment in the SVG header.

Note: XML comments cannot contain a double hyphen. Write CSS
variable names in comments without the leading punctuation, or
reword to avoid it.

## Diagram types

- **Schematics** (pot still, mash tun) — hand-authored outline
  drawings with labelled components.
- **Data graphs** (the spirit cut, cask-maturation kinetics) —
  strict register, no sketch filter. Plotted *exactly* from a
  sourced figure: the data points are digitised from the cited
  work and held in `scripts/gen_data_diagrams.py`, which emits
  the SVG. Re-run that script after any data change. The
  spirit-cut and cask-maturation graphs reproduce Miller, Whisky
  Science 2nd ed. (2024), Figs. 6.7 and 8.11 respectively.

  Every data graph must carry, without exception: a described
  label on **every** axis (the quantity *and* its unit, e.g.
  "Cask age [months]"); tick labels on every axis; and a **full
  grid** — gridlines at every tick in both directions, not just
  the horizontal. A figure attribution line names the source.
