# WhiskyBase bibliography

Curated catalogue of in-depth, technical, peer-reviewed, and
historical works cited or queued for citation by WhiskyBase entries.
Maintained as a single reference document to:

1. **Centralise bibliographic data.** Concept-page and entry sources
   that currently cite works in free-text form can point at this
   catalogue once a `literature_id:` source-field convention is
   adopted (deferred — see Status below).
2. **Document the project's sourcing standard.** The works listed
   here are the reference set the project aims to ground claims on.
   Popular consumer guides, marketing copy, and trade-press
   commentary are deliberately excluded.
3. **Make follow-up reading visible.** Several concept pages cite
   reference works without specific page numbers (see "Cited from"
   subsections under each entry). Grounding those citations against
   actual page references is queued research work.

## Status

This catalogue is a **bibliographic inventory**, not a reading
record. Inclusion of a work means it is recognised as a standard
reference for its subject matter; it does not warrant that the
project maintainers have read each work first-hand. Where a work
is cited from existing entries (Russell, Mosedale, Conner,
Theobald), those citations should be cross-checked against the
actual text when a copy becomes available — until then the
citing entry carries a `confidence: medium` marker and an
explicit hedge in its source notes.

## Sourcing standard for inclusion

A work qualifies for this catalogue if it meets one or more of:

- Peer-reviewed publication in a recognised academic journal.
- Authoritative reference text published by an academic or
  industry-recognised publisher (Academic Press, RSC, Wiley,
  Elsevier, ACS, Longman / Pearson Scientific & Technical,
  Nottingham University Press in the alcohol-textbook lineage).
- Institutional publication by a research body relevant to
  whisky (SWRI, Heriot-Watt's International Centre for Brewing
  and Distilling, EU-funded research consortia).
- Sustained historical or analytical writing on Scotch whisky
  by an author with primary-source research credentials,
  preferably with academic affiliation.

Disqualifying for inclusion:

- Consumer guides marketed for general-audience purchase advice.
- Distillery-funded promotional publications.
- Trade-press articles repeating producer marketing claims.
- Personal blogs or whisky-influencer writing.

These exclusions reflect the project's voice register and
sourcing policy (`docs/voice-register.md`,
`docs/source-conflict-policy.md`). Inclusion in this bibliography
does not mean a work is uncontested or definitive on every point
it covers — peer-reviewed papers disagree with one another, and
reference texts age. Multiple sources cited together is the
standard pattern for non-trivial claims.

---

## Technical reference books

### Russell (ed.), 2014 — Whisky: Technology, Production and Marketing

- **Editors:** Inge Russell, Graham Stewart (2nd edition);
  Inge Russell, Charles Bamforth, Graham Stewart (1st edition)
- **Title:** *Whisky: Technology, Production and Marketing*
- **Edition:** 2nd edition
- **Publisher:** Academic Press / Elsevier
- **Year:** 2014 (1st edition 2003)
- **ISBN:** 978-0-12-401735-1 (2nd edition); 978-0-12-374181-3
  (1st edition; also 9780080474854 for the Amsterdam print)
- **Series:** Handbook of Alcoholic Beverages

The standard multi-author technical reference for Scotch and
related whiskies. Chapters cover malting, brewing/mashing,
fermentation, distillation engineering, maturation chemistry,
blending, and quality analysis, written by senior researchers
and industry practitioners. Inge Russell was for many years
director of research at SWRI's predecessor; the book draws on
that institutional perspective. This is the volume most
commonly cited for "the producer-level technical consensus
view" of any given Scotch production stage.

**Third edition (2022) — held.** A 3rd edition, retitled *Whisky
and Other Spirits: Technology, Production and Marketing* (eds.
Inge Russell, Graham G. Stewart, Julie Kellershohn; Academic
Press / Elsevier; ISBN 978-0-12-822076-4), was acquired on
2026-05-20 and is held with the project. It is substantially
restructured, with new chapters on Japanese, Indian, Canadian,
craft, and Asia-region whiskies. It is the canonical Russell
edition for new entries. It does NOT, however, serve as an
independent second source for the 14 entries grounded against the
2nd edition: the 3rd-edition chapters covering those topics are
written by the same authors — Ch 10 raw materials (Bringhurst,
Harrison, Brosnan), Ch 12 distilling yeast and fermentation
(Russell, Stewart), Ch 14 batch distillation (Nicol), Ch 16
maturation (Conner). It is a currency upgrade, not multi-source
corroboration; the confidence blocker still needs a genuinely
independent source. See `docs/literature-scouting.md`.

**Cited by** (14 entries, all grounded 2026-05-19 against the 2nd
edition with chapter author + page range + subsection-level
pages for the specific claims):

- Ch 6 (Bringhurst & Brosnan, pp 49-121):
  - `data/concepts/glossary/kiln.yml` (peating + kilning, pp 58-59)
  - `data/concepts/glossary/mashing.yml` (pp 88-95)
  - `data/concepts/practice/floor-malting.yml` (pp 57-58)
  - `data/concepts/practice/external-malting.yml` (pp 59-61)
- Ch 7 (Russell & Stewart, pp 123-145):
  - `data/concepts/glossary/distillers-yeast.yml`
  - `data/concepts/glossary/fermentation.yml` (+ Ch 8 Wilson,
    pp 147-154, for LAB / secondary-fermentation chemistry)
- Ch 9 (Nicol, pp 155-177):
  - `data/concepts/equipment/direct-fired-still.yml`
    (pp 156-160 heating source)
  - `data/concepts/glossary/reflux.yml` (pp 158-161)
  - `data/concepts/glossary/shell-and-tube.yml` (pp 155, 161-162)
  - `data/concepts/glossary/wash-still.yml` (pp 165-169)
- Ch 11 (Conner, pp 199-219):
  - `data/concepts/educational/cask-fill-states.yml` (pp 206-210)
  - `data/concepts/educational/cask-maturation-kinetics.yml`
    (pp 199-219 whole chapter)
- Ch 14 (Aylott, pp 243-269) + Ch 18 (Mitchell, pp 315-326):
  - `data/concepts/educational/chill-filtering.yml` (Aylott
    p 231 chemistry; Mitchell p 257 packaging practice)
  - `data/concepts/educational/scotch-presentation-conventions.yml`
    (both chapters)

The grounding pass replaced the prior "page references to be
added when consulted" hedge with specific chapter + page-range
citations. The chapter authors are now attributed rather than
the editor.

### Miller, 2024 — Whisky Science: A Condensed Distillation

- **Author:** Gregory H. Miller (Professor Emeritus of Chemical
  Engineering, University of California, Davis)
- **Title:** *Whisky Science: A Condensed Distillation*
- **Edition:** 2nd edition (1st edition 2019)
- **Publisher:** Springer International Publishing
- **Year:** 2024
- **ISBN:** 978-3-031-50686-4 (print); 978-3-031-50687-1 (eBook)

A single-author technical reference covering the whisky
production chain — malting, mashing, fermentation, distillation,
maturation — from a physical-chemistry and chemical-engineering
standpoint. Genuinely independent of the Russell lineage:
different author, publisher, and institutional base, with no
shared editors. The 2nd edition adds over 350 citations and is
itself heavily primary-sourced. User-supplied; held by the
project from 2026-05-20 (see `docs/literature-scouting.md`).

Its value to the project is precisely as the independent second
academic source the confidence rubric requires for a `high`
promotion — a role a newer edition of Russell cannot fill.

**Cited by** (5 entries promoted to `high` on 2026-05-20, each
also citing Russell ed. 2014):

- `data/concepts/glossary/kiln.yml` (Ch 3 Malting, pp 151-152)
- `data/concepts/glossary/mashing.yml` (Ch 4 Mashing, pp 187-199)
- `data/concepts/glossary/fermentation.yml` (Ch 5 Fermentation,
  pp 219-241)
- `data/concepts/glossary/reflux.yml` (Ch 6, pp 253-255)
- `data/concepts/glossary/wash-still.yml` (Ch 6-7, Distillation)

Also cited by `data/concepts/glossary/distillers-yeast.yml`
(Ch 5, section 5.1), which remains `confidence: medium` — Miller
corroborates the distilling-strain core but not that entry's
named yeast-house list.

### Piggott, Sharp & Duncan (eds.), 1989 — The Science and Technology of Whiskies

- **Editors:** J. R. Piggott, R. Sharp, R. E. B. Duncan
- **Title:** *The Science and Technology of Whiskies*
- **Publisher:** Longman Scientific & Technical
- **Year:** 1989
- **ISBN:** 0-582-04128-3

The pre-Russell multi-author technical reference. Still widely
cited in the older peer-reviewed literature; covers the same
production-chain organisation that Russell (2003 / 2014) later
updated. Particularly useful for the late-1980s technical
consensus, which preserves several chapters on practices
(e.g., direct-fired distillation, traditional malting) that
Russell's 2014 edition treats only briefly. J. R. Piggott
(Strathclyde University) was the principal sensory-science
contributor; his subsequent peer-reviewed papers carry the
same analytical framework forward.

**Cited by:** None yet. Queued as a complement to Russell for
the legacy-practice details (direct-fired stills, traditional
malting, pre-2000s commercial supply chain).

### Piggott (ed.), 1983 — Flavour of Distilled Beverages

- **Editor:** J. R. Piggott
- **Title:** *Flavour of Distilled Beverages: Origin and Development*
- **Publisher:** Ellis Horwood / VCH (Verlag Chemie)
- **Year:** 1983
- **ISBN:** 0-85312-509-2

Early multi-author treatment of distilled-spirit flavour chemistry,
covering whisky, brandy, rum, and grain spirits. Pre-dates the
modern HPLC era for phenol measurement; useful for the
1970s-80s flavour-chemistry baseline and for documenting the
analytical methods that preceded the standard seven phenols
HPLC convention.

**Cited by:** None yet. Queued for the planned
`educational/cask-maturation-kinetics` page and for grounding
the flavour-development claims in glossary/reflux.

### Lyons & Hill (eds.) — The Alcohol Textbook

- **Editors:** T. P. Lyons, F. T. Hill, K. A. Jacques (varies by
  edition)
- **Title:** *The Alcohol Textbook: A Reference for the Beverage,
  Fuel and Industrial Alcohol Industries*
- **Publisher:** Nottingham University Press
- **Years:** Multiple editions from 1995; 5th edition 2009 is
  widely cited (978-1-904761-65-1).

Standard reference text for grain-alcohol production at industrial
scale. Covers fermentation, distillation, and downstream alcohol
processing across beverage and fuel applications; the Scotch-
specific content sits in dedicated chapters within a broader
treatment of grain spirits. Particularly useful for fermentation
kinetics, yeast strain selection, and washback-design
engineering questions that production_line entries currently
hedge on.

**Cited by:** None yet. Queued for fermentation and
distillation-engineering claims that go beyond Russell's
chapter coverage.

### Boulton & Quain, 2001 — Brewing Yeast and Fermentation

- **Authors:** Chris Boulton, David Quain
- **Title:** *Brewing Yeast and Fermentation*
- **Publisher:** Blackwell Science / Wiley
- **Year:** 2001 (reissued 2006)
- **ISBN:** 978-0-632-05475-4

The standard reference text for brewing and distilling yeast
biology and fermentation engineering. Covers Saccharomyces
cerevisiae strain selection, fermentation metabolism, wort
gravity tolerance, and ester profile development at depth.
Although ostensibly brewing-focused, the chapters on
distilling-yeast strains and high-gravity fermentation cover
the science that underlies Scotch fermentation practice.

**Cited by:** None yet, but flagged as a follow-up source in
`data/concepts/glossary/distillers-yeast.yml` for grounding the
strain-selection and ester-profile claims currently sourced to
Russell.

### Buxton & Hughes, 2014 — The Science and Commerce of Whisky

- **Authors:** Ian Buxton, Paul S. Hughes
- **Title:** *The Science and Commerce of Whisky*
- **Publisher:** Royal Society of Chemistry (RSC Publishing)
- **Year:** 2013 / 2014 (revised 2nd edition)
- **ISBN:** 978-1-84973-384-7

Paul Hughes is Professor of Brewing and Distilling at Oregon
State University, formerly at Heriot-Watt's International
Centre for Brewing and Distilling; Ian Buxton is a long-time
Scotch industry writer with primary-source research
credentials. The book is positioned between Russell's
technical reference and the more historical / commercial
literature: it covers the production-chain chemistry and
process technology but also the regulatory, economic, and
commercial dimensions of the industry. The RSC publishing
imprint and Hughes's academic affiliation place it in the
technical-reference category for the project's purposes.

**Cited by:** None currently. Queued as a candidate companion
reference for the planned `educational/cask-maturation-kinetics`
page and the §Filtering techniques research item.

### Udo, 2006 — The Scottish Whisky Distilleries

- **Author:** Misako Udo
- **Title:** *The Scottish Whisky Distilleries*
- **Publisher:** Black Bottle Publishing
- **Year:** 2006 (first English-language edition; original
  Japanese editions earlier)
- **ISBN:** 978-1-905452-04-4

Detailed gazetteer of operating and historical Scotch
distilleries, drawn from extensive on-site visits and primary
research. Udo's coverage of operating distilleries includes
equipment specifications, production capacity, and ownership
detail at a level of granularity not consistently available in
other reference works. Particularly useful for cross-checking
the distillery-entry equipment fields (mash tun, washback,
still geometry, condenser type) and for historical context on
distilleries that have closed or been substantially
reconfigured.

**Cited by:** None yet. Queued as a cross-check reference for
distillery entries.

---

## Peer-reviewed papers

The bibliography lists representative author groupings rather
than exhaustive paper lists; the journals listed in the next
section are the natural search venue when grounding a specific
claim.

### Mosedale & Puech — oak extractives in spirit maturation

- **Authors:** J. R. Mosedale (University of Reading), J.-L.
  Puech (INRA, France)
- **Key paper:** Mosedale, J. R. & Puech, J.-L. (1998), "Wood
  maturation of distilled beverages", *Trends in Food Science
  & Technology*, 9(3), 95-101. DOI 10.1016/S0924-2244(98)00024-7.
- **Further papers:** Mosedale's earlier doctoral and post-doctoral
  work on oak-cooperage maturation kinetics (Reading, 1990s);
  Puech's extensive series on cognac/brandy oak chemistry,
  translatable to Scotch maturation contexts (1980s-2000s, in
  the French food-chemistry literature).

Standard review of oak-derived compounds in distilled-spirit
maturation: lignin breakdown products (vanillin and related
aromatics), oak lactones (cis- and trans-β-methyl-γ-octalactone),
tannins and ellagitannins, hemicellulosic sugars contributing
colour and sweetness. Cited extensively in subsequent whisky-
maturation literature; the project's treatment of cask-fill-state
depletion curves rests on analytical work of this kind.

**Cited by:**

- `data/concepts/educational/cask-fill-states.yml` — wood
  extractive depletion across successive fills

### Conner — whisky flavour chemistry (SWRI / Strathclyde)

- **Author:** James M. Conner, formerly senior scientist at
  the Scotch Whisky Research Institute (SWRI), frequent
  co-author with Strathclyde sensory chemistry group.
- **Selected representative papers:**
  - Conner, J. M., Paterson, A., Piggott, J. R. (1994),
    "Interactions between ethyl esters and aroma compounds in
    model spirit solutions", *Journal of Agricultural and Food
    Chemistry*, 42(10), 2231-2234. DOI 10.1021/jf00046a028.
  - Conner, J. M., Paterson, A., Piggott, J. R. (1992),
    "Changes in wood extractives from oak cask staves through
    maturation of Scotch malt whisky", *Journal of the Science
    of Food and Agriculture*, 60(3), 349-353.
  - Conner, J. M.; Birkmyre, L.; Paterson, A.; Piggott, J. R.
    (1998), "Headspace concentrations of ethyl esters at
    different alcoholic strengths", *Journal of the Science of
    Food and Agriculture*, 77(1), 121-126.
  - Several further papers in *JIB*, *JAFC*, and conference
    proceedings of the European Brewery Convention and
    Worldwide Distilled Spirits Conference series.

Conner's work bridges new-make spirit composition,
maturation chemistry, and sensory characterisation. The
SWRI affiliation positions these papers as industry-aligned
peer-reviewed publications — closer to producer reality than
purely academic models of fermentation or maturation.

**Cited by:**

- `data/concepts/glossary/reflux.yml` (forward reference to
  Conner papers for the reflux-ratio / new-make-character
  relationship; specific paper not yet identified)
- `docs/source-conflict-policy.md`

### Paterson & Piggott — Strathclyde flavour chemistry group

- **Authors:** A. Paterson, J. R. Piggott (University of
  Strathclyde, Glasgow). Frequent co-authorship with J. M.
  Conner; the trio is the dominant Scotch sensory / flavour
  chemistry research group of the 1990s-2000s.
- **Scope:** Ester chemistry, aroma compound interactions in
  ethanol-water systems, sensory descriptor development for
  whisky, headspace gas chromatography for flavour analysis.
- **Selected paper:** Piggott, J. R. & Conner, J. M. (1995),
  "Whiskies", in *Fermented Beverage Production* (eds. A. G. H.
  Lea & J. R. Piggott), Chapman & Hall — chapter-length
  treatment.

The Strathclyde group's work is the connective tissue between
the SWRI-affiliated technical literature and the food-chemistry
literature published in JAFC, JSFA, and FRI. Many Conner papers
cited above carry Paterson and Piggott as co-authors.

**Cited by:** None yet directly; the Conner co-authorships are
the indirect path.

### Wanikawa, Hosoi & Suntory whisky chemistry group

- **Authors:** A. Wanikawa, K. Hosoi (Suntory Research Centre,
  Japan), with various co-authors.
- **Scope:** Oak lactone (β-methyl-γ-octalactone) cis/trans
  isomer ratios as a function of cask origin and toast level;
  the chemistry that distinguishes American-oak from European-oak
  cask flavour profiles in mature whisky.
- **Selected paper:** Wanikawa, A.; Hosoi, K.; Kato, T.;
  Nakagawa, K. (2002), "Identification of green note compounds
  in malt whisky using multidimensional gas chromatography",
  *Flavour and Fragrance Journal*, 17(3), 207-211.

Suntory's research output is industry-aligned but published
in international peer-reviewed venues, making it citable for
the project's purposes. Particularly relevant for the planned
`educational/cask-maturation-kinetics` page and for grounding
claims about American-vs-European oak character differences in
the cask-category entries.

**Cited by:** None yet. Queued for cask-maturation-kinetics.

### Aylott — whisky authenticity and analytical chemistry

- **Author:** R. I. Aylott (Diageo / SWRI, analytical chemistry)
- **Scope:** Whisky authenticity (detecting adulteration,
  verifying age statements), analytical methods development for
  the industry, congener profile characterisation.
- **Selected paper:** Aylott, R. I. & MacKenzie, W. M. (2010),
  "Analytical strategies to confirm the generic authenticity
  of Scotch whisky", *Journal of the Institute of Brewing*,
  116(3), 215-229.

Aylott's chapters in Russell ed. 2014 cover the analytical
quality-assurance side of the industry. Particularly useful
for grounding age-statement and authenticity claims, and as
a cross-reference when discussing the analytical infrastructure
that underlies producer ppm disclosures.

**Cited by:** None yet. Queued as a reference for any future
work on whisky authentication or analytical methodology.

### SWRI staff publications: Bringhurst, Brookes, Brosnan

- **Affiliations:** Scotch Whisky Research Institute (SWRI),
  Heriot-Watt University.
- **Authors / scope:**
  - T. A. Bringhurst — yeast and fermentation, mash extraction
    efficiency.
  - P. R. Brookes — distillation engineering and copper
    interaction chemistry.
  - J. Brosnan — fermentation and distillation operations,
    energy efficiency, congener formation.
- **Publication venues:** JIB, JAFC, JSFA, and SWRI-funded
  conference proceedings.

The SWRI staff peer-reviewed paper line is the natural source
when grounding industry-aligned process-engineering claims.
Most papers are accessible via the journals listed below.

**Cited by:** None yet. Queued for grounding process-engineering
claims in production_line and distillery entries.

### Forthcoming candidates (not yet queued as citations)

- **Mosedale, J. R.** further papers on stave-extraction
  kinetics, beyond the 1998 review.
- **Watts, D. A.; Boulton, R. J.** (UC Davis, not the brewing
  Boulton), papers in the fermentation-engineering literature
  relevant to washback fermentation modelling.
- **Pollnitz, A. P.; Pardon, K. H.; Sefton, M. A.** (AWRI,
  Australian Wine Research Institute) — oak chemistry papers
  primarily on wine but with direct relevance to wine-cask
  finishes in Scotch.

These would be sourced for the planned cask-maturation-kinetics
page once that work begins.

---

## Industry / academic journals

The project does not cite individual papers from these journals
exhaustively; the journals are listed here as the recognised
publication venues for whisky-relevant peer-reviewed work, and
as the natural search target when grounding a specific claim
against primary literature.

### Journal of the Institute of Brewing (JIB)

- **Publisher:** Wiley, on behalf of the Institute of Brewing
  and Distilling
- **ISSN:** 0046-9750 (print), 2050-0416 (online)
- **Scope:** Peer-reviewed research on brewing and distilling
  science, including malting, fermentation, distillation, and
  flavour chemistry of beers and spirits including Scotch
  whisky. The most direct disciplinary venue for the project's
  range of subject matter.

### Journal of the Science of Food and Agriculture (JSFA)

- **Publisher:** Wiley, on behalf of the Society of Chemical
  Industry
- **ISSN:** 0022-5142
- **Scope:** Broad food / agricultural science with regular
  whisky-relevant papers; Conner et al.'s 1992 and 1998 cask
  extractive and headspace papers appeared here. Particularly
  useful for cask-maturation chemistry that sits between food
  chemistry and agricultural processing.

### Food Chemistry

- **Publisher:** Elsevier
- **ISSN:** 0308-8146
- **Scope:** Broad food-chemistry journal; whisky-relevant
  papers appear regularly on phenolic compounds, ester
  formation, oak extractives, and flavour analysis.

### Journal of Agricultural and Food Chemistry (JAFC)

- **Publisher:** American Chemical Society (ACS Publications)
- **ISSN:** 0021-8561
- **Scope:** Strong representation of whisky and brandy
  maturation chemistry, including the Conner and Mosedale
  papers cited above. The journal's analytical-chemistry
  emphasis makes it the natural venue for HPLC/GC-MS-based
  characterisation studies of spirit composition.

### Journal of Cereal Science

- **Publisher:** Elsevier
- **ISSN:** 0733-5210
- **Scope:** Cereal-science research relevant to malting
  barley (variety performance, kilning effects, phenol
  precursors in the husk). Particularly useful for the
  upstream end of the production chain.

### Trends in Food Science & Technology

- **Publisher:** Elsevier
- **ISSN:** 0924-2244
- **Scope:** Review-article journal; Mosedale & Puech 1998
  (cited above) appeared here. Useful for review-level
  treatment of maturation chemistry.

### Food Research International

- **Publisher:** Elsevier
- **ISSN:** 0963-9969
- **Scope:** Cross-disciplinary food science; covers
  fermentation, sensory analysis, and analytical methods
  relevant to whisky. Less whisky-specific than JIB or JSFA
  but a common venue for cross-disciplinary papers.

### LWT — Food Science and Technology

- **Publisher:** Elsevier (under International Union of Food
  Science and Technology auspices)
- **ISSN:** 0023-6438
- **Scope:** Applied food science, including alcohol
  beverages. Useful for analytical-methods papers and applied
  sensory work.

### Chemical Senses

- **Publisher:** Oxford University Press
- **ISSN:** 0379-864X
- **Scope:** Sensory science journal — flavour perception,
  olfactory chemistry, taste physiology. Relevant for the
  sensory-evidence side of disputed flavour-impact claims
  (e.g., the chill-filtering mouthfeel debate noted in
  TODO §Filtering techniques).

### Flavour and Fragrance Journal

- **Publisher:** Wiley
- **ISSN:** 0882-5734
- **Scope:** Flavour chemistry and aroma analysis; Wanikawa
  Suntory papers on green-note compounds and oak lactones
  appear here.

---

## Institutional publications

### Scotch Whisky Research Institute (SWRI)

- **Affiliation:** Heriot-Watt University, Edinburgh
- **Type:** Industry-funded research institute serving Scotch
  whisky producers; publishes both peer-reviewed papers (in the
  journals listed above) and technical reports for member
  distilleries.
- **Web:** https://www.swri.co.uk/

SWRI is the central research body for Scotch and one of the
most authoritative sources for industry-aligned technical
information. Public-access SWRI material is limited (much of
the work is published for paying member companies), but
SWRI staff publish individual papers under their own names in
the open peer-reviewed literature (see Conner, Bringhurst,
Brookes, Brosnan, Aylott above).

### Heriot-Watt University International Centre for Brewing and Distilling (ICBD)

- **Affiliation:** Heriot-Watt University, Edinburgh
- **Type:** University-based teaching and research centre
  covering brewing and distilling science at undergraduate,
  master's, and doctoral level. Hughes (co-author of *The
  Science and Commerce of Whisky*) and many SWRI staff have
  ICBD affiliations.
- **Web:** https://www.hw.ac.uk/uk/research/icbd/

ICBD publishes PhD theses (publicly accessible through the
university's research portal) and hosts the Worldwide
Distilled Spirits Conference series proceedings periodically.
The PhD thesis literature is a useful primary source for
research-quality work that has not yet appeared in
journal-length papers.

### Scotch Whisky Association (SWA)

- **Affiliation:** Industry trade association representing
  the majority of Scotch whisky producers.
- **Type:** Trade association; publications include the
  Scotch Whisky Regulations interpretive guidance, technical
  files for protected-geographical-indication purposes,
  annual statistics, and policy / position papers.
- **Web:** https://www.scotch-whisky.org.uk/

SWA publications are the natural reference for industry-wide
statistical data (production volumes, export figures, sector
employment) and for guidance on regulatory matters that fall
short of statutory text. Treat SWA position papers as the
industry's own framing, not as a neutral analytical source.

### HMRC (Her Majesty's Revenue and Customs)

- **Affiliation:** UK government tax authority
- **Type:** Regulatory authority for spirits duty and
  bonded warehousing; publishes the alcoholometry rules used
  in the UK and EU framework, age-statement guidance, and
  related regulatory notices.
- **Web:** https://www.gov.uk/government/organisations/hm-revenue-customs

The Alcoholic Liquor Duties Act 1979 and subsequent HMRC
notices (Notice 39 on spirits, Excise Notice 226 on beer
duty applied analogously, etc.) define the technical
framework underlying age statements, ABV measurement, and
warehouse-stored spirit accounting.

**Cited by:**

- `data/concepts/glossary/abv.yml` (Alcoholic Liquor Duties
  Act 1979)

### Worshipful Company of Distillers (London livery company)

- **Affiliation:** City of London livery company, chartered 1638.
- **Type:** Historical guild structure; archive material
  includes early distilling-trade records that predate modern
  regulatory frameworks. Of interest for early-history claims.
- **Web:** https://www.distillers.org.uk/

Primary archive access is via City of London archives;
secondary references via institutional historians of the
spirits trade.

**Cited by:** None yet; queued as a source for any future
work on the pre-1900 history of Scotch distilling.

---

## Annual industry publications

### The Malt Whisky Yearbook

- **Editor:** Ingvar Ronde
- **Publisher:** MagDig Media Ltd
- **Frequency:** Annual since 2005
- **Web:** https://www.maltwhiskyyearbook.com/

Annual reference covering distillery production figures,
ownership changes, equipment specifications, and new
releases. The Yearbook is closer to trade-reference than
peer-reviewed work; it occupies a useful niche between
producer marketing and academic literature. Useful as a
cross-check on annual capacity figures and ownership-history
disclosures.

**Caveat:** Distillery-supplied figures occasionally drift
between editions or reflect updated equipment changes
incompletely. Cross-check against producer-direct sources
where the difference is material.

**Cited by:**

- `data/concepts/practice/external-malting.yml`
- `data/concepts/practice/floor-malting.yml`

### Whisky Magazine

- **Publisher:** Paragraph Publishing Ltd
- **Frequency:** Bi-monthly
- **Web:** https://whiskymag.com/

Listed here because it occasionally publishes deeper-than-
trade-press reporting (long-form interviews with master
distillers, technical site visits with equipment detail).
Treat individual articles case-by-case: most issues are
consumer-facing and do not qualify under the project's
sourcing standard, but specific articles may carry useful
primary information disclosed by named producers under
controlled conditions.

---

## Historical / contextual works

### MacLean, Charles — analytical writing on Scotch whisky

- **Selected works:**
  - MacLean, C. (2003), *Scotch Whisky: A Liquid History*,
    Cassell Illustrated. ISBN 1-84403-078-4.
  - MacLean, C. (ed.) (2008), *Whisky: The World's Greatest
    Distilleries, Distillers and Drinks*, Dorling Kindersley.
  - MacLean, C. (2016), *Scotch Whisky: A Liquid History*
    (revised), Reaktion Books.

MacLean is a long-tenured Scotch whisky writer and historian
with documented primary-source research on distillery records
and historical context. His historical writing fills a gap
between purely commercial sources (which tend to elide
inconvenient ownership-history details) and the peer-reviewed
chemistry literature (which has no historical mandate). The
*Liquid History* title in particular is the most commonly
cited single-volume historical reference for Scotch.

**Cited by:** None currently. Queued as a candidate source for
distillery historical-section grounding.

### Moss & Hume, 1981 — The Making of Scotch Whisky

- **Authors:** Michael S. Moss, John R. Hume
- **Title:** *The Making of Scotch Whisky: A History of the
  Scotch Whisky Distilling Industry*
- **Publisher:** James & James, Edinburgh
- **Year:** 1981 (reissued 2000 with revisions)
- **ISBN:** 0-907383-00-7

The standard industrial-history of Scotch from the late 18th
century through the late 20th. Moss (Glasgow University
archivist) and Hume (industrial historian) draw on company
archives and primary records that consumer-oriented histories
cannot match. The book is the principal authority on
ownership consolidation, the late-19th-century building boom,
and the post-1900 industry restructuring.

**Cited by:** None yet. Queued as the primary historical
reference for ownership-history sections on distillery
entries.

### Weir, R. B. — academic economic history of Scotch

- **Author:** Ronald B. Weir (University of York, economic
  historian)
- **Selected works:**
  - Weir, R. B. (1995), *The History of the Distillers
    Company, 1877-1939: Diversification and Growth in Whisky
    and Chemicals*, Clarendon Press / Oxford University Press.
    ISBN 0-19-820173-4.
  - Various academic papers in business history journals.

Weir's work is the principal academic-economic-history
treatment of the Distillers Company Limited (DCL) and its
trajectory, which is the structural backbone of the modern
Scotch industry's corporate ownership patterns. Particularly
useful for grounding ownership-history claims on Diageo-
heritage distilleries (Lagavulin, Talisker, Caol Ila, Oban,
Cragganmore, etc., all descended from DCL ownership).

**Cited by:** None yet. Queued for distillery entry
ownership-history grounding, particularly for the Diageo /
DCL succession.

---

## Excluded from this bibliography

Three categories of widely-circulated whisky writing are
deliberately not included:

1. **Consumer scoring guides.** Annual ratings publications
   (Murray's annual *Whisky Bible*, Hansell's *Malt Advocate*
   ratings, etc.) and review aggregators have a defined audience
   purpose that does not match the project's sourcing standard.
   Reviewer notes from individual reviewers may appear on
   bottling entries under `notes_independent`, attributed to the
   reviewer, but the underlying scoring frameworks are not
   project sources.

2. **Distillery-funded coffee-table books.** Many distilleries
   commission glossy histories of themselves for visitor-centre
   sale. These are marketing artefacts and do not satisfy the
   project's sourcing standard, even where they contain factually
   accurate material.

3. **Whisky-influencer blogs and YouTube.** Personal sites by
   enthusiasts, however knowledgeable, do not satisfy the
   peer-review / institutional-publication criterion. The
   exceptions are personal sites maintained by named industry
   researchers who publish elsewhere under peer-review
   (rare; flag for case-by-case evaluation).

## Schema integration (deferred)

A future schema enhancement could add a `literature_id:` field
to source entries, letting source citations reference catalogue
entries by slug instead of carrying full bibliographic strings
inline. This would centralise updates (a single bibliographic
correction propagates to all citing entries) and enable
build-time validation that book citations resolve to known
catalogue entries.

Scope of the schema change:

- Add `literature_id:` (optional string slug) to the `source`
  object definition in `schema/json/_common.schema.json`.
- Define slugs for catalogue entries (e.g. `russell-2014`,
  `mosedale-puech-1998`, `boulton-quain-2001`).
- Update existing source blocks that cite books to reference
  the slug, retaining the `citation:` field as a human-readable
  display string.
- Extend the cross-reference resolver to validate
  `literature_id:` against the catalogue.

Deferred until the catalogue is exercised with a few more entries
and the value of central updates is concrete. The bibliography
as-is (markdown) already serves the project's primary need: a
visible, curated inventory of citable references.
