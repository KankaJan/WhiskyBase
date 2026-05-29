# Diagram style spec — WhiskyBase

Diagrams in WhiskyBase are deterministic, hand-authored or
data-driven SVG. They are version-controlled as text, carry no
baked-in colour, and inherit the site theme. AI image generation
is not used: it is unsourceable, hallucination-prone, and cannot
plot real data — see `TODO.md` Beta-readiness for the rationale.

This document is the authoring spec. The reference
implementation is `data/diagrams/pot-still.svg`.

## Three visual registers

WhiskyBase diagrams use **three** registers, chosen by what the
diagram is doing.

**External-assembly schematics** — the pot still, the
production-chain flowchart, the peating-measurement matrix — use
a deliberate **hand-drawn sketch** register: the look of an
expert sketching on paper to illustrate "this is the thing we
are discussing." The wobble breathes against parts that are
spatially distinct and have margin between them.

**Cross-section schematics** — the mash tun, the washback, the
worm tub, the shell-and-tube condenser, the Coffey-still
columns, the spirit safe — use a **technical-schematic**
register: clean lines, no filter, same theme tokens as the other
registers. Cross-sections show things-inside-things, and the
sketch register's displacement filter smears interior strokes
(tube bundles, perforation marks, internal coils, switcher arms)
into the walls that contain them. Clean lines keep the interior
legible.

**Technical data graphs** — the spirit cut, cask-maturation
kinetics — use a **strict** register: precise axes, real tick
values, no wobble filter. Where a diagram plots data it must be
plotted *exactly* from a sourced figure (see "Data graphs"
below).

Rule of thumb for picking a register: distinct parts laid out
spatially → sketch. A slice through equipment with interior
detail → technical-schematic. Plotted data → strict.

The choice of register is not only aesthetic — it is honest
about what the diagrams are. A concept-page schematic (the pot
still, the mash tun) is generic and indicative, not to scale.
Pot stills vary enormously between distilleries, and that
variation is itself a teaching point; there is no single
canonical geometry to draw. A crisp dimensioned blueprint would
signal a precision the drawing does not have, and would require
measurements the project does not hold: the distillery `stills`
data carries volumes (`capacity_litres`) sparsely and almost no
geometry (`height_m` is null for nearly every entry;
`lyne_arm_angle` is descriptive — "ascending" / "descending" —
not a numeric angle). A measured blueprint would therefore mean
fabricating numbers, which the sourcing policy forbids.

What signals "indicative, not metrological" is the **absence of
dimensions** — no millimetre annotations, no scale bar, no
hatching that implies material specification, no tolerances.
Both the sketch and the technical-schematic registers honour
that by carrying none of those. The sketch register adds a
wobble on top as an aesthetic cue that says "this is
indicative", which reads well when parts are spatially separate.
The technical-schematic register relies on the absence alone,
which is the readable choice when interior detail must stay
legible.

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

This applies to the **sketch register only**. Technical-schematic
diagrams and strict data graphs carry no filter.

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

## Technical-schematic conventions

Applies to cross-section diagrams only — the mash tun, the
washback, the worm tub, the shell-and-tube condenser, the
Coffey-still columns, the spirit safe. The conventions below were
settled in the 2026-05-26 blueprint pilot on mash-tun.svg, then
rolled out to the other five.

### No filter

The root `<svg>` has no `<defs>` block carrying a
turbulence/displacement filter, and no `filter=` attribute on
any element. Strokes are clean.

### Stroke color: currentColor everywhere

Every stroke uses `stroke="currentColor"`. **Do not use
`stroke="var(--muted-color)"`** — some SVG viewers do not resolve
CSS variables when applied as `stroke` (only as `fill`), so
`var()`-stroked leaders render invisibly in those viewers.
`currentColor` resolves reliably to the inherited text colour.

Fills may still use `fill="var(--muted-color)"` for dots, labels
or filled shapes — the var() resolution problem is `stroke`-only
in observed cases. Equivalently, using `fill="currentColor"`
throughout is the safer default.

### Double-walled vessel outlines with section hatching

The vessel walls are drawn as two parallel outlines (outer + inner)
about 4 user-units apart. The cut surface between them is filled
with diagonal section hatching:

```xml
<defs>
  <pattern id="cut-hatch-<slug>" patternUnits="userSpaceOnUse"
           width="5" height="5" patternTransform="rotate(45)">
    <line x1="0" y1="0" x2="0" y2="5"
          stroke="currentColor" stroke-width="0.5"/>
  </pattern>
</defs>

<!-- Wall material: outer and inner closed paths in one path
     element, even-odd fill gives hatching only in the band. -->
<path d="M outer-closed-path Z
         M inner-closed-path Z"
      fill="url(#cut-hatch-<slug>)" fill-rule="evenodd"
      stroke="none"/>

<!-- Wall outlines (visible edges) -->
<g fill="none" stroke="currentColor" stroke-width="1.4"
   stroke-linejoin="round" stroke-linecap="butt">
  <path d="M outer-closed-path Z"/>
  <path d="M inner-closed-path Z"/>
</g>
```

The hatch pattern is **generic** — no material specification. It
signals "this is a cut surface", not "this is steel" or "this is
wood". That distinction matters: ANSI/ISO material hatching
implies a material property the project does not source.

### No dimensions, no scale bar

A cross-section in this register MUST NOT carry millimetre
annotations, a north arrow, a scale bar, dimensional tolerances,
or "section A-A" plane indicators. Generic section hatching is
allowed; material-specific hatching is not.

### Generic indicative proportions

Aspect ratios, plate counts, tube counts, coil turns and similar
are illustrative, not numerically faithful to any specific named
vessel.

### Stroke-weight hierarchy

- **1.4** — outer + inner wall outlines
- **1.2** — internal primary structure (rake shaft + arm, gearbox,
  switcher motor, mullions, stand legs, tube bundle wrapper)
- **1.0** — internal secondary structure (rake teeth, plate edges,
  worm-coil ellipses, single tubes, hidden-line dashes); also
  annotation-leader stroke
- **0.7 – 0.8** — fine internal detail (slot ticks on perforated
  plates, gear cross-marks, grain-bed stippled hatching, hydrometer
  stems)
- **0.5** — the diagonal lines inside the section-hatch pattern
- **`stroke-linecap="butt"`** on lines with arrowheads or dashed
  endings (avoids the round-cap half-circle artifact at line ends)

### Annotation leaders

Every label connects to its part via a **dashed** leader (no flow
arrows, no triangle arrowheads):

```xml
<g fill="none" stroke="currentColor" stroke-width="1.0"
   stroke-linecap="butt" stroke-dasharray="5 3">
  <path d="..."/>
</g>
```

The leader terminates at the part with a **filled circle dot**
(no arrowhead). Annotation dots are `r="2.4"`; nozzle-endpoint
dots (where a substance enters or exits the vessel) are slightly
larger at `r="2.6"`. Dots use `fill="currentColor"`,
`stroke="none"`.

Leaders should not cross label text. If a leader's natural route
collides with the label, reposition the label or the leader (an
L-shape with one bend is acceptable) until there is clear margin
between them.

### Inlet and outlet pipe nozzles

Wherever a pipe enters or exits the vessel, draw a short solid
three-sided rectangular **pipe nozzle stub** at the vessel
surface. The open side faces the vessel interior (for inlets)
or the vessel wall (for outlets and side fittings). Typical
dimensions: ~20-40 user units wide, ~20-40 deep. The nozzle is
drawn in solid currentColor at the same stroke-width as other
structural detail (1.2).

The annotation leader for the substance terminates at the nozzle
(dot at one of the nozzle edges), not at a bare point on the
vessel surface. Without the nozzle the dashed leader points at
nothing visible.

### Hidden lines for occluded parts

Use dashed lines (`stroke-dasharray="3 2"`, stroke 1.0) for parts
that would be hidden in cross-section but are visualisable behind
a foreground feature — for example, the rake teeth on the far
side of the rotating arm. The 3-2 dash spacing distinguishes
hidden-lines from the 5-3 annotation-leader dashes.

### Cross-section cuts

Vessel walls are treated as cut surfaces. By engineering
convention a leader to an interior part may pass through the cut
to terminate at the part inside the vessel. Leaders to exterior
parts still avoid crossing any drawn line, per the shared markup
conventions.

### Disallowed

- **Flow arrows / triangle arrowheads.** Direction-of-flow is
  carried by the label text ("Cooled wort and yeast", "Wort, to
  the washback"). Mixing flow arrows on pipes with dot
  terminations on annotation leaders produced unreadable double-
  arrow appearances in the pilot iteration — settled on dots
  everywhere, no arrows.
- **Wobble filter.** If you find yourself wanting the sketch
  register's displacement filter, the diagram is in the wrong
  register — promote it to sketch.
- **Scale bars or dimensions.** As above.

## Sourcing

A diagram is a claim like any other. Its schematic content must
be grounded in the cited source; `source_id` on the diagram
entry points at the concept's `sources:` block. Document the
grounding in an XML comment in the SVG header.

Note: XML comments cannot contain a double hyphen. Write CSS
variable names in comments without the leading punctuation, or
reword to avoid it.

## Diagram types

- **External-assembly schematics** — sketch register.
  Examples: the pot still, the production-chain flowchart, the
  peating-measurement-methods matrix.
- **Cross-section schematics** — technical-schematic register
  (clean lines, no filter, generic indicative proportions).
  Examples: the mash tun, the washback, the worm tub, the
  shell-and-tube condenser, the Coffey-still columns, the
  spirit safe.
- **Data graphs** — strict register, no filter. Plotted
  *exactly* from a sourced figure: the data points are digitised
  from the cited work and held in
  `scripts/gen_data_diagrams.py`, which emits the SVG. Re-run
  that script after any data change. The spirit-cut and
  cask-maturation graphs reproduce Miller, Whisky Science 2nd
  ed. (2024), Figs. 6.7 and 8.11 respectively.

  Every data graph must carry, without exception: a described
  label on **every** axis (the quantity *and* its unit, e.g.
  "Cask age [months]"); tick labels on every axis; and a **full
  grid** — gridlines at every tick in both directions, not just
  the horizontal. A figure attribution line names the source.
