# About WhiskyBase

WhiskyBase is an open-source educational reference for Scotch whisky
production, tasting, and analysis. It is a structured-data project
first and a website second.

## What this is

A growing database of distilleries, production lines, bottlings,
bottlers, casks, suppliers, and reference concepts. Every entry is
written against a versioned YAML schema, and every claim is sourced.
The schemas live under `/schema/`; the data lives under `/data/`;
both are checked by `scripts/check_references.py` after every change.

Production-data prose follows a strict reference register that strips
marketing language. Educational concept pages follow a technical
teaching register. Both are documented at
[voice-register](/reference/voice-register/).

## What this is not

WhiskyBase is not a marketplace, a tasting-notes aggregator, or a
brand-positioning tool. It does not host independent tasting notes;
it cites producer-attributed claims with the producer named. It does
not compute composite scores, average source values, or smooth over
conflicting figures — when sources disagree, the disagreement is
preserved and explained.

## Scope

Currently covers single malt Scotch whisky production. Adjacent
categories (grain whisky, blended Scotch, world whisky) are not in
scope for the data layer but may appear as reference concepts when
needed to make the Scotch material make sense.

## Licensing

The data layer at `/data/` and `/schema/` is licensed
**CC-BY-SA 4.0**. Anyone may reuse, redistribute, or build on it as
long as they credit the project and license derivatives under the
same terms.

The site code at `/site/` is licensed **MIT** — separate license
because the rendering layer is a generic Astro application that
happens to consume the data, and there's no reason for downstream
users of the rendering code to be bound by share-alike.

## Status

Active, iterative buildout. Schemas are versioned and may change.
Counts and current backlog are tracked in the project's `TODO.md`
and `docs/handover.md` in the source repository.

## Verification and sourcing

The project's foundational principle is "every claim is sourced."
The [source-conflict-policy](/reference/source-policy/) page
describes the source-type vocabulary, conflict-resolution rules, and
how Wikipedia citations are treated as starting points to be
migrated to primary sources. The
[bibliography](/reference/bibliography/) catalogues the standing
reference works.
