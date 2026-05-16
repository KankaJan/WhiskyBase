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

Full policy: `docs/source-conflict-policy.md`. Source-type
vocabulary: `official_website`, `trade_publication`, `wikipedia`,
`chemistry_database`, `regulatory_text`, `independent_review`,
`peer_reviewed_paper`.

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

`scripts/check_references.py` is the load-bearing check for the
project. Run it from the repo root after every data change.
Output is warn-only — never blocks commit.

It reports:

- YAML parse failures (catches NUL bytes and silent truncation)
- Duplicate IDs
- Dangling cross-references grouped by target type
- Invalid `source_id` references inside structured measurement
  and methodology blocks
- Inline `[N]` citation references that don't resolve

Dangling references to entries not yet populated are *expected*
per handover §8 (forward references) — they're tracked in
`TODO.md` rather than fixed.

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
  JSON Schema validator (warn-only).
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
- `TODO.md` — active backlog and Research Requests.
- `CHANGELOG.md` — schema changes and notable additions.
