---
name: voice-register
description: WhiskyBase writing register rules. Triggers any time prose is being authored or edited for a distillery, production_line, bottling, or concept page entry — including description fields, NOTES.md files, and the body / summary fields of concept pages. Encodes the disallowed-words list, the two-register distinction (strict reference vs. technical-teaching), the discipline tests, and worked examples.
---

# Voice register — WhiskyBase

The canonical rules live in `docs/voice-register.md`. This skill is the
fast reference, used while drafting. If the two ever disagree, the
canonical doc wins and this skill should be updated.

## When to apply

Apply whenever:

- Writing or editing any `description:` field on a distillery,
  production_line, or bottling YAML entry.
- Writing any `summary:` or `body:` field on a concept page.
- Writing any prose in a `<entity>.NOTES.md` file.
- Adding inline YAML comments that include sentences (one-liner field
  comments are not in scope).
- Writing or reviewing tasting notes that the project authors itself
  (attributed `notes_independent` quotations from reviewers are out of
  scope and preserved verbatim).

## Two registers

| Register | Used for | Latitude |
|---|---|---|
| **Strict reference** | Distillery / production_line / bottling descriptions; NOTES.md prose | Strip every adjective; what remains must still teach |
| **Technical-teaching** | Concept page `body` content (educational, methodology, equipment, practice) | Plain instructive sentences allowed; strip every claim that isn't either definitional or sourced |

The **disallowed-words list applies to both**.

## Disallowed words

Categorised, but the point is the register they signal, not the
specific words. Extend the list when new examples surface.

- **Praise terms**: celebrated, renowned, iconic, legendary, beloved,
  acclaimed, prestigious, esteemed, revered, world-class,
  award-winning (unless naming a specific award with a citation),
  best-known.
- **Picturesque terms**: rugged, wild, windswept, ancient, timeless,
  pristine, untouched, dramatic, breathtaking, stunning.
- **Mystical / storytelling terms**: philosophy, ethos, passion,
  journey, soul, heart, spirit (in the metaphorical sense), magic,
  alchemy, craft (as a noun meaning "the craft"), artistry.
- **Hyperbole**: masterpiece, gem, jewel, hidden, secret, unparalleled,
  unmatched, definitive.
- **Producer-voice tics**: "we believe", "we are committed to", "our
  promise", "our story", "our heritage".

## Discipline tests

Run one of these silently on every prose field before saving.

**For the strict reference register:** strip every adjective. Do the
remaining facts still stand on their own? If almost nothing survives,
the prose is doing marketing, not reference.

**For the technical-teaching register:** strip every claim that isn't
either *definitional* or *sourced*. Does what survives still teach?
If only ungrounded assertions remain, the writing has drifted into
opinion.

## Permitted exceptions

These are not violations — note them for completeness.

- **Local context with production consequences.** "Maritime climate"
  is admissible when maritime exposure affects maturation character.
  "Stunning scenery" is not.
- **Attributed producer claims.** "The producer characterises the
  spirit as fruity and floral [2]" is fine. The same sentence stated
  in the project's voice is not.
- **Direct reviewer quotations** in `notes_independent` preserve the
  reviewer's voice verbatim, even if florid. Add an inline comment
  noting that the prose is attributed rather than the project's voice.
- **Specific named awards** with a citation: "won a Trophy at the
  IWSC 2022 [N]" is admissible; "award-winning" is not.

## Length discipline

- **Strict reference register:** length follows information density.
  A distillery description with 5 substantive facts is appropriate
  at ~150 words; padding to 300 words is overreach.
- **Teaching register:** length follows topic depth. Worm tubs warrant
  ~1500 words; a glossary entry for "wash" gets one sentence.

**Pre-publication check on every educational page**: "What does this
page do that a Wikipedia article doesn't?" The page is useful when it
either connects the topic to this project's data model, synthesises
across sources, provides a comparative view, or resolves a confusion
in primary sources. If none of those, the page is filler — do not
publish.

## Worked examples

### Bad (strict reference)

> "Bruichladdich is a celebrated Islay distillery known for its
> innovative spirit and rugged maritime character. Founded by the
> Harvey brothers in 1881, it has long been a beloved jewel of the
> Hebridean whisky scene, with a passion for terroir and craftsmanship
> that sets it apart."

Strip the adjectives → "Bruichladdich is an Islay distillery. Founded
by the Harvey brothers in 1881." The rest is colour. The reader
learned the founding year and the location — already in the
structured fields.

### Good (strict reference)

> "Founded in 1881 by the Harvey brothers — William, John, and
> Robert — on the western shore of Loch Indaal on the Rinns of Islay
> [1][2]. The distillery operated under several owners through the
> 20th century before being mothballed by Whyte and Mackay in 1994
> [1]. It was acquired in December 2000 by a private investor group
> led by Mark Reynier of Murray McDavid, with Jim McEwan hired from
> Bowmore as master distiller, and resumed production in May 2001
> [1][2]."

Every sentence carries facts that aren't derivable from the structured
fields alone (the brothers' first names, the ownership transition
story, the new investor group's connection to Murray McDavid).
Adjectives are absent because they would not survive the strip test.

### Bad (teaching)

> "Worm tubs are an old and traditional way of condensing spirit,
> beloved by distillers who care about authenticity. The character
> of the resulting whisky is rich, complex, and full of soul, which
> is why discerning enthusiasts seek out these special drams."

The page promised explanation; it delivered praise. None of "old and
traditional", "beloved", "authenticity", "rich, complex, full of soul",
"discerning enthusiasts", "special drams" teach anything.

### Good (teaching)

> "A worm tub leaves more sulphur in the spirit. This shows up
> sensorily as weight, meatiness, and what some writers call 'funk' —
> a quality variously described as savoury, rustic, or even slightly
> eggy at the new-make stage [6]. After maturation the sulphur
> character integrates and is rarely unpleasant; it manifests as the
> meaty Mortlach character, the structured Cragganmore profile, the
> weight of Talisker and Old Pulteney."

The page explains a chemical mechanism (sulphur retention) and
connects it to perceived character with named examples. Adjectives
appear, but they characterise producer outputs rather than praising
them, and they're attributed where necessary.

## Quick fail patterns

If you catch yourself writing one of these patterns, rewrite:

- "X is a [praise term] [region] distillery known for…" → restart
  with the founding date or the production fact you were about to
  insert next.
- "The result is a [emotion-word] whisky with…" → the project does
  not describe whiskies in emotional terms in its own voice.
- "Following the [legendary / iconic / celebrated] reopening…" →
  drop the adjective. The reopening date and ownership transition are
  the load-bearing facts.

## When the list needs to grow

If a real entry surfaces a word that signals the wrong register and
is not in the list above, add it to `docs/voice-register.md` (and
mirror here). Adding entries should be routine; removing one should
require a concrete example and a discussion.

## See also

- `docs/voice-register.md` — canonical rules.
- `docs/source-conflict-policy.md` — how to handle source disagreements
  while writing (rules complement each other when writing NOTES.md
  prose).
- `scripts/check_references.py` — cross-reference resolver; not voice-
  related but the sibling tooling that lives in this repo for
  authoring discipline.
