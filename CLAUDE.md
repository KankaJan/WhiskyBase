# CLAUDE.md — WhiskyBase

This file gives Claude (in Cowork mode, Claude Code, or any fresh
session) the project's working rules. It is mechanical and
procedural — read it once each session and apply it. For design
rationale and project orientation, see `docs/handover.md`.

---

## Response style

Strict, critical, analytical, target-oriented. Not optimised for
agreeable.

Concretely:

- **Don't soften factual errors.** If the user proposes something
  that's wrong, say so directly and explain why. "You're mistaken
  about X because Y" is the right register, not "well, you might
  consider Y instead."

- **Hedge only for genuine uncertainty.** If a claim is well-
  established, state it. Don't pre-emptively hedge to seem
  reasonable. If a claim is contested, attribute it and explain
  the contest.

- **Push back on bad ideas.** When the user suggests something
  that doesn't fit the task, say so with reasoning. Don't quietly
  comply with a worse approach because it's what was asked.

- **Choose the solution that fits the task, not the one that
  pleases the project owner.** If two approaches are on the table
  and one is technically better, pick that one and explain why,
  even if the other was suggested first.

- **Be terse where possible.** No padding, no recap of what was
  just said, no "great question!" preambles. Get to the substance.

- **Surface trade-offs explicitly.** When choosing between
  options, name what's lost. Don't claim a free lunch.

The critical-analysis pattern that has been working in this
project (write → critical evaluation → fix → verify) is the model
for response quality across the board.

---

## Iterative working pattern

After any substantive work (new entries, schema changes, multi-
file edits), do a critical-analysis pass before declaring done.

Pattern:

1. **Write.** Produce the artefact (entry, schema change, edit).
2. **Critical evaluation.** Audit the result for factual errors,
   voice-register violations, schema compliance, internal
   contradictions, unsourced claims, audit-coverage gaps. Use the
   same rigour for your own work as for the user's.
3. **Fix.** Apply corrections. Note what was checked-and-accepted
   vs. fixed.
4. **Verify.** Run `scripts/check_references.py` from the repo
   root. Strip trailing NUL bytes (see safe-bulk-writes skill).
5. **Document.** Update `CHANGELOG.md`, `TODO.md`, and the
   relevant section of `docs/handover.md` if state shifted.

Critical evaluation passes produce structured findings
(High / Medium / Low / Considered-but-accepted) with concrete
file:line citations where possible.

---

## Reducing wasted iteration

Discipline that reduces wasted rounds. Adapted from a public set
of behavioural guidelines for LLM coding work
(forrestchang/andrej-karpathy-skills/CLAUDE.md). Complements
"Response style" and "Iterative working pattern" above by
covering the *pre-write* discipline that the iterative pattern
takes as given. For trivial requests, use judgment.

### Surface assumptions before acting

- State what you're assuming about the user's intent. If you
  have to guess between two plausible readings, name them — don't
  choose silently.
- If the request is ambiguous on a load-bearing dimension
  (visual style, scope, output format, success criterion), ask
  BEFORE generating. One clarifying question early beats five
  revisions later.
- If a simpler approach exists than what the user asked for,
  say so.

### Simplicity first

Minimum artefact that satisfies the request. Nothing
speculative.

- No content beyond what was asked.
- No schema fields, abstractions, or "flexibility" added in case
  someone might need them later. The project's data layer is
  populated as needs surface, not pre-extended.
- If a draft is overcomplicated for its job, shorten it before
  declaring done.

### Surgical changes

Touch only what the request specifies.

- Don't "improve" adjacent prose, code, or geometry the user
  didn't flag.
- Don't refactor things that aren't broken.
- If you notice an unrelated issue, mention it — don't silently
  fix it. Exception: the documented hard-corruption signatures
  (NUL bytes, silent truncation, YAML parse failure) are always
  fixed in place, since they propagate.

### Goal-driven execution

Translate vague requests into verifiable goals before
generating.

- "Make this look better" → "What specifically should change?
  What does success look like?"
- "Redraw the diagrams" → "In what register, with what
  conventions? Pilot one before doing the rest."

Multi-step work gets a brief plan with verification steps:

1. [step] → verify: [check]
2. [step] → verify: [check]

Strong success criteria let you loop independently. Weak
criteria ("make it work") force the user to re-evaluate every
intermediate result.

---

## Sourcing policy

Foundational principle: "every claim is sourced."

- **Primary sources first.** PubChem for chemistry, ecfr.gov for
  US distilled-spirits regulation, INAO for French wine
  appellations, Consejo Regulador for sherry, producer structured
  spec sheets for distillery specs.
- **Wikipedia is volatile.** Treat Wikipedia citations as
  starting points. Migrate to primary sources where available;
  track in `TODO.md` Research Requests if not.
- **Wrong sources stay cited.** When a source is rejected (e.g.,
  outlier figure), it remains in the entry's `sources:` block
  with a note explaining the rejection.
- **Never silently round, average, or smooth.** Source conflicts
  resolve to one of the disclosed figures, never to an
  interpolated middle.

Full policy: `docs/source-conflict-policy.md`. The canonical
source-type vocabulary is the `source_type` enum in
`schema/json/_common.schema.json` — it is the list the validator
actually enforces, and all other documents derive from it:
`official_website`, `trade_publication`, `book`, `wikipedia`,
`wikidata`, `company_filing`, `independent_review`, `interview`,
`chemistry_database`, `regulatory_text`, `peer_reviewed_paper`,
`other`.

---

## Voice register

Strict reference register for production-data prose (distillery,
production_line, bottling descriptions, NOTES.md files).
Technical-teaching register for educational concept-page body
content. Both reject marketing language.

Trigger `/skills/voice-register/SKILL.md` whenever authoring
prose. Disallowed words and discipline tests are in the skill.

Attributed producer claims are allowed: "the producer
characterises the spirit as fruity [2]" is fine; the same
sentence stated as the project's voice is not.

---

## File-write safety

Writes of 5+ files in one tool-call message, or any single Write
of a file >~10 KB, have produced corruption (NUL-byte padding,
silent truncation) in this project's history.

Rules:

- Cap parallel Write batches at ≤4 files.
- For files >~10 KB, prefer bash-mediated writes
  (`python3 << 'PYEOF'` heredoc).
- After any batch, run the NUL-strip cleanup snippet.
- Verify with `scripts/check_references.py`.

Full procedure and repair patterns: `/skills/safe-bulk-writes/SKILL.md`.

---

## Verification

Two scripts guard the data, and the pre-commit hook runs both as
gates (activate once per clone: `git config core.hooksPath
scripts/hooks`).

`scripts/check_references.py` is the cross-reference resolver and
JSON Schema validator. Run it from the repo root after every data
change. It reports:

- YAML parse failures (catches NUL bytes and silent truncation)
- Duplicate IDs
- Dangling cross-references, split into **expected** (listed in
  `scripts/expected_dangling.txt`) and **unexpected**
- Invalid `source_id` references inside structured measurement
  and methodology blocks
- Inline `[N]` citation references that don't resolve
- Stale `schema_version` declarations (vs the current templates)
- Cross-file consistency contradictions (e.g. a bottling whose
  `produced_at_distillery` disagrees with its production line's
  distillery)
- JSON Schema violations

Default output is warn-only. With `--strict` it exits non-zero on
*hard* problems — parse failures, duplicate IDs, schema
violations, bad citations, **unexpected** dangling references, and
consistency contradictions — and this strict run is the second
pre-commit gate. Forward references to entries not yet populated
are *expected* per handover §8; add them to
`scripts/expected_dangling.txt` so they do not fail the gate
(legacy: such refs were tracked in `TODO.md`). Stale
`schema_version` and soft mirroring gaps are warnings, not
failures.

`scripts/check_writes.py` is the **hard-corruption gate** and the
first pre-commit gate. It scans text files for the mount-sync
damage signatures — embedded NUL bytes, silent truncation (no
trailing newline), YAML parse failure — and exits non-zero on any
finding, blocking the commit. Hard corruption must never reach a
commit.

`scripts/test_checks.py` unit-tests both gate scripts; run
`python3 scripts/test_checks.py` after changing either.

---

## Documentation update rules

After significant work:

- **`CHANGELOG.md`** — new entry if the schema changed, policy
  changed, or a new top-level entity type / source-type was
  introduced. Data additions don't need CHANGELOG entries (those
  are tracked in Git history per the file's own preamble).
- **`TODO.md`** — Recently Completed entry for any substantive
  work. Move items from highest-priority to Recently Completed
  when resolved. Add new items to the appropriate section as
  they surface.
- **`docs/handover.md` §10** — update Populated counts when
  entities are added. Update Next priorities when the active
  backlog shifts.
- **`docs/handover.md` §1 / §6 / other** — update only when
  fundamental project structure changes (new entity type, new
  slug convention, etc.).

When in doubt: more documentation > less. Future contributors
(including future Claude instances) only know what the docs say.

---

## Slug conventions

Full spec in `docs/handover.md` §6. Quick reference:

- Distillery: bare name (`bruichladdich`, `harris`)
- Production line: `<distillery>-<descriptor>`
- Bottling OB: `<distillery>-<release-name>`
- Bottling IB: `<bottler>-<distillery>-<descriptor>`
- Bottler: bare name (`cadenheads`)
- Concept (structured slug reference): `<kind>/<slug>`
- Concept (markdown URL form): `concept/<kind>/<slug>`
- Cask: bare slug, lowercase-hyphenated

---

## When asked "what next?"

The current backlog is in `docs/handover.md` §10 Next priorities.
Don't invent priorities; consult that list.

When proposing a next move, name the top 2-3 options with
trade-offs and recommend one. Don't enumerate the entire backlog
unless asked.

---

## Tooling pointers

- `scripts/check_references.py` — cross-reference resolver and
  JSON Schema validator (warn-only by default; `--strict` gates).
- `scripts/check_writes.py` — hard-corruption scanner (NUL bytes,
  truncation, YAML parse failure); the pre-commit hook in
  `scripts/hooks/` runs it and blocks the commit on a finding.
- `/schema/json/` — draft-07 JSON Schemas, one per entity type,
  plus a shared `_common.schema.json`. The YAML templates remain the
  human-readable source of truth; JSON Schemas are the machine-readable
  validators. Keep them in sync when the template changes.
- `/skills/voice-register/SKILL.md` — voice rules.
- `/skills/safe-bulk-writes/SKILL.md` — file-write safety.
- `docs/handover.md` — project orientation (start here for new
  sessions).
- `docs/source-conflict-policy.md` — full source policy.
- `docs/voice-register.md` — full voice policy.
- `docs/schema-design-notes.md` — schema design rationale.
- `docs/diagram-style.md` — authoring spec for educational-page
  SVG diagrams. Read before authoring or editing any diagram.
- `docs/bibliography.md` — curated catalogue of in-depth,
  peer-reviewed, and institutional reference works. The project's
  positive sourcing standard (exclusion criteria included).
- `docs/literature-scouting.md` — scouting list of reference
  works worth acquiring (not yet held) plus open-access sources
  citable now. The shopping-list complement to `bibliography.md`.
- `docs/build-pipeline-plan.md` — design document for the
  eventual static-site build (Astro + Pagefind + MapLibre).
  Page-type taxonomy, URL routing, markdown-link rewriting rules,
  search-index scope, map data source, tasting-notes /
  commercial-info display decisions. Read before starting any
  frontend implementation work.
- `/site/` — Astro 5 site source (MIT licence, separate from
  the CC-BY-SA data layer). First-iteration scaffolding
  (2026-05-17): home page + distilleries index + distillery
  detail page render against the YAML data. Components and data
  loader in `/site/src/`. Run `npm install && npm run build`
  from `/site/` to build; see `/site/README.md` for the
  developer guide.
- `TODO.md` — active backlog and Research Requests.
- `CHANGELOG.md` — schema changes and notable additions.
