# Contributing

WhiskyBase is a structured, fact-grounded reference for Scotch whisky
production. Contributions are proposed as pull requests against the
YAML data layer. This page is the practical guide: what to read, how to
add or change an entry, how the validation gates work, and what gets a
PR rejected.

The data layer is licensed CC-BY-SA-4.0; the site code under `/site/`
is MIT. By contributing you agree your contribution is released under
the licence of the part of the repository you are changing.

## Read these first

In order — the first time, read all of them; afterwards, the schema
template for the entity you are touching is usually enough:

1. `README.md` — what the project is.
2. `docs/handover.md` — design rationale and current state. Section 12
   states **document precedence** when two documents disagree: the JSON
   Schemas in `/schema/json/` win, then the `schema/*.template.yml`
   templates, then the policy docs, then the handover.
3. `docs/voice-register.md` — how entry prose must read.
4. `docs/source-conflict-policy.md` — how to handle disagreeing sources,
   and the canonical source-type vocabulary.
5. `docs/schema-design-notes.md` — why the schemas are shaped the way
   they are.
6. The `schema/*.template.yml` for the entity type you are adding. The
   template is the authoritative field-by-field guide.

## Entity types and where files live

| Entity | Directory | Template | Slug convention |
|---|---|---|---|
| Distillery | `data/distilleries/` | `schema/distillery.template.yml` | bare name (`bruichladdich`) |
| Production line | `data/production_lines/` | `schema/production_line.template.yml` | `<distillery>-<descriptor>` |
| Bottling | `data/bottlings/` | `schema/bottling.template.yml` | OB `<distillery>-<release>`; IB `<bottler>-<distillery>-<descriptor>` |
| Bottler | `data/bottlers/` | `schema/bottler.template.yml` | bare name (`cadenheads`) |
| Cask | `data/casks/` | `schema/cask.template.yml` | bare, hyphenated (`oloroso-sherry-butt`) |
| Supplier | `data/suppliers/` | `schema/supplier.template.yml` | bare name |
| Concept | `data/concepts/<kind>/` | `schema/concept.template.yml` | referenced as `<kind>/<slug>` |

Full slug rules are in `docs/handover.md` section 6.

## Setup

Two tools validate the data. Install their Python dependencies once:

```
pip install pyyaml jsonschema
```

Then activate the pre-commit hook (once per clone) so commits are
checked locally before they ever reach CI:

```
git config core.hooksPath scripts/hooks
```

The hook runs two gates and blocks the commit if either fails. The
same gates run in CI (`.github/workflows/validate.yml`) on every push
and pull request.

## Adding or changing an entry

1. Fork the repository and branch from `master`.
2. Copy the relevant `schema/*.template.yml` as your starting point.
   The template's inline comments document every field, its enum
   values, and what belongs where.
3. Fill it in. Use explicit `null` for unknown values rather than
   omitting keys — the tooling and the site prefer present-but-null.
4. Research against the source hierarchy in
   `docs/source-conflict-policy.md`: primary databases and producer
   spec sheets first, trade press next, Wikipedia treated as volatile.
   Aim for 5+ independent sources for a `confidence: high` entry.
5. Resolve any source conflicts per the policy — pick one disclosed
   figure (never an average), document the choice in an inline comment,
   and record the full conflict in a sibling `<entity>.NOTES.md`.
6. Cite every prose claim inline with `[1]`, `[2]`, matching the entry's
   numbered `sources:` block.
7. Set `confidence:` honestly (the rubric is in the source policy) and
   `last_reviewed:` to the date of your work.
8. Run the gates (below). Fix anything they report.
9. Commit with a clear message and open a pull request.

### Cross-references and forward references

Entries reference each other by slug (a bottling names its
`produced_at_distillery`, a production line lists its `bottlings`, and
so on). A reference to an entry that does not exist yet is a *forward
reference* and is allowed — but it must be registered so the strict
gate does not treat it as a typo. Add it to
`scripts/expected_dangling.txt` in `<kind>:<slug>` form (e.g.
`distillery:glenlivet`) with a comment, and remove the line once the
entry is populated. An unregistered dangling reference fails the gate.

## Running the gates

From the repo root:

```
python3 scripts/check_writes.py            # hard-corruption scan
python3 scripts/check_references.py         # full report (warn-only)
python3 scripts/check_references.py --strict # the gating run
python3 scripts/test_checks.py              # unit tests for the gates
```

- **`check_writes.py`** scans for the mount-sync damage signatures —
  embedded NUL bytes, missing trailing newline (truncation), and YAML
  parse failure. It blocks the commit on any finding.
- **`check_references.py`** is the cross-reference resolver and JSON
  Schema validator. Default output is warn-only and informational.
  **`--strict`** exits non-zero on *hard* problems — parse failures,
  duplicate IDs, schema violations, bad `source_id` / inline `[N]`
  citations, unexpected dangling references, and cross-file consistency
  contradictions — and is the second pre-commit gate. Stale
  `schema_version` declarations and soft mirroring gaps are warnings,
  not failures.

Your PR will not be merged until `check_references.py --strict` passes
and the CI build is green.

## A note on editing files safely

This repository has a documented history of file corruption when many
files are written at once or when large block-edits are applied (NUL-byte
padding, silent truncation), caused by a Windows/Linux mount-sync race.
If you are using an automated tool to write files, read
`skills/safe-bulk-writes/SKILL.md` first: cap batches at four files,
prefer whole-file writes over large in-place edits, and re-run
`check_writes.py` after every batch.

## What makes a good entry

- Multiple sources, cited and referenced inline.
- Source conflicts resolved with reasoning; both the resolution and the
  rejected sources documented (rejected sources stay cited, with a note).
- Reference register — no marketing language. See
  `docs/voice-register.md` and its disallowed-words list.
- All required schema fields present; optional fields populated where
  data exists, `null` where it does not.
- `confidence:` and `last_reviewed:` set honestly.

## What gets rejected

- Marketing copy (see the disallowed-words list).
- Single-source claims for contested facts without acknowledgement.
- Averaging or smoothing across disagreeing sources.
- Tasting notes written in the project's own voice rather than as
  attributed reviewer quotations.
- Removing a source citation because its figure was not chosen — the
  rejected source stays cited with an explanatory note.
- Out-of-scope content: tour/visitor info, awards and medals,
  secondary-market prices, "philosophy/ethos/story" marketing tiers
  (see `docs/handover.md` section 9).

## Questions

If you are unsure about anything, open an issue and ask before spending
significant time on a PR. The project has many deliberate
"we considered X and chose Y" decisions; aligning upfront is faster
than negotiating them in review.
