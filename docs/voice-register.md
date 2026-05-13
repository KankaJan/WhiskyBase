# Voice register

This document records the voice and writing discipline rules for
WhiskyBase entries. The rules exist because whisky writing has a
strong default register — celebratory marketing prose with thick
adjective coverage and very thin factual content — and this project
deliberately rejects that register in favour of something more
useful.

Two registers, with shared discipline and different latitudes.

---

## Strict reference register

Used for: distillery, production_line, and bottling **descriptions**
and prose fields.

**Rule:** strip every adjective. If the facts still stand, the
description works. If stripping the adjectives leaves nothing behind,
the description is doing marketing, not reference.

**Disallowed words.** Extend this list when new examples come up;
err toward inclusion. The point is not the specific words but the
register they signal.

- *Praise terms*: celebrated, renowned, iconic, legendary, beloved,
  acclaimed, prestigious, esteemed, revered, world-class,
  award-winning (unless naming a specific award with a citation),
  best-known.
- *Picturesque terms*: rugged, wild, windswept, ancient, timeless,
  pristine, untouched, dramatic, breathtaking, stunning.
- *Mystical/storytelling terms*: philosophy, ethos, passion, journey,
  soul, heart, spirit (in the metaphorical sense), magic, alchemy,
  craft (when used as a noun meaning "the craft"), artistry.
- *Hyperbole*: masterpiece, gem, jewel, hidden, secret, unparalleled,
  unmatched, definitive.
- *Producer-voice tics*: "we believe", "we are committed to", "our
  promise", "our story", "our heritage".

**Local context is allowed only when it has production consequences.**
"Maritime climate" gets in if maritime exposure affects maturation
character. "Stunning scenery" does not get in.

**Producer claims are allowed when attributed.** "The producer
characterises the spirit as fruity and floral [2]" is fine. "Fruity
and floral" stated as the project's voice is not.

---

## Technical-teaching register

Used for: educational concept pages, methodology concept pages,
equipment pages with explanatory body content.

**Same disallowed-words list applies.** The latitude is different in
*kind*, not in marketing tolerance.

**Plain instructive sentences are permitted.** "Phenols deposit on
the husk during kilning, then partition into the wort during
mashing" is appropriate in an educational page. The same sentence
would be over-explanatory in a distillery description, where the
reader is presumed to have arrived already understanding the
production basics.

**Discipline test:** strip every claim that isn't either definitional
or sourced. Does what remains still teach? If teaching content
survives the strip, the register is working. If only assertions
without grounding survive, the writing has drifted into opinion.

**Length follows topic depth, not topic importance.** Worm tubs are
a contained topic with a clear stake (heavier spirit, sulphur
character, ~16 distilleries in the population) and warrant ~1500
words. A glossary entry for "wash" gets one or two sentences.
Resist length-for-its-own-sake.

**Pre-publication check on every educational page:** "What does this
page do that a Wikipedia article doesn't?" If the answer is "nothing,"
the page should not exist yet, even if the topic is important. A page
that just recapitulates available reference material is filler and
should be removed.

The educational page is useful when it:

- Connects a topic specifically to the data model used in this project
  (e.g. linking PPM measurement methods to the `method` and
  `compounds` enums in `production_line.template.yml`).
- Synthesises across sources that haven't been brought together
  before.
- Provides a comparative view of multiple distilleries / techniques /
  products that a single-source article would not.
- Resolves a confusion that exists in primary sources.

If none of those, the page is filler.

---

## Examples

### Reference register, bad

> "Bruichladdich is a celebrated Islay distillery known for its
> innovative spirit and rugged maritime character. Founded by the
> Harvey brothers in 1881, it has long been a beloved jewel of the
> Hebridean whisky scene, with a passion for terroir and craftsmanship
> that sets it apart."

What's wrong: every load-bearing word is praise or atmosphere.
Strip the adjectives and almost nothing remains: "Bruichladdich is
an Islay distillery. Founded by the Harvey brothers in 1881." The
rest is colour. The reader learns the founding year and the location
— which the structured fields above already record.

### Reference register, good

> "Founded in 1881 by the Harvey brothers — William, John, and
> Robert — on the western shore of Loch Indaal on the Rinns of Islay
> [1][2]. The distillery operated under several owners through the
> 20th century before being mothballed by Whyte and Mackay in 1994
> [1]. It was acquired in December 2000 by a private investor group
> led by Mark Reynier of Murray McDavid, with Jim McEwan hired from
> Bowmore as master distiller, and resumed production in May 2001
> [1][2]."

Why it works: every sentence carries facts that wouldn't be derivable
from the structured fields alone (the brothers' first names, the
ownership transition story, the connection between the new investor
group and an existing independent bottler). Adjectives are absent
because they would not survive the strip test.

### Teaching register, bad

> "Worm tubs are an old and traditional way of condensing spirit,
> beloved by distillers who care about authenticity. The character
> of the resulting whisky is rich, complex, and full of soul, which
> is why discerning enthusiasts seek out these special drams."

What's wrong: same problem as before, but the teaching context makes
it worse — the page promised explanation, then delivered praise.
"Old and traditional", "beloved", "authenticity", "rich, complex,
full of soul", "discerning enthusiasts", "special drams" are all
inhabitants of the marketing register, and none of them teach
anything.

### Teaching register, good

> "A worm tub leaves more sulphur in the spirit. This shows up
> sensorily as weight, meatiness, and what some writers call 'funk'
> — a quality variously described as savoury, rustic, or even
> slightly eggy at the new-make stage [6]. After maturation the
> sulphur character integrates and is rarely unpleasant; it
> manifests as the meaty Mortlach character, the structured
> Cragganmore profile, the weight of Talisker and Old Pulteney."

Why it works: the page is explaining a chemical mechanism (sulphur
retention) and connecting it to perceived character with specific
named examples. Adjectives appear ("savoury", "rustic", "meaty",
"structured") but they're characterising producer outputs, not
praising them, and they're attributed where necessary ("what some
writers call").

---

## When the rules need updating

If a new entry surfaces a register edge case that this document
doesn't cover, update this document with the example. The rules are
descriptive of the project's accumulated practice, not handed down
from outside. Adding a banned word should be common; relaxing one
should require a concrete example and a discussion.
