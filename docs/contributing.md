# Contributing

This is a stub. Will be expanded as the project develops the contribution
workflow. For now, the essentials:

## Reading before contributing

In order:

1. `README.md` — what the project is
2. `docs/handover.md` — design rationale and current state
3. `docs/voice-register.md` — how to write entries
4. `docs/source-conflict-policy.md` — how to handle disagreements between sources
5. `docs/schema-design-notes.md` — why the schemas are shaped the way they are
6. The schema template for the entity type you're adding

## Making a change

1. Fork the repository.
2. Branch from `main`.
3. Make your change. Validate that any YAML files you touch parse cleanly:
   ```
   python3 -c "import yaml; yaml.safe_load(open('path/to/file.yml'))"
   ```
4. If your change touches multiple sources or involves source conflicts,
   add or update a `<entity>.NOTES.md` sibling file.
5. Commit with a clear message.
6. Open a pull request.

## What makes a good entry

- Multiple sources cited and referenced inline via `[1]`, `[2]`.
- Source conflicts resolved with reasoning, both the resolution and
  the rejected sources documented.
- Reference register (no marketing language); see `docs/voice-register.md`.
- All required schema fields populated; optional fields populated
  where data exists, null where it doesn't.
- `confidence:` field set honestly.
- `last_reviewed:` set to the date of your work.
- `sources:` block populated with type, URL, and access date for every
  source referenced.

## What gets rejected

- Marketing copy. See the disallowed-words list in
  `docs/voice-register.md`.
- Single-source claims for contested facts without acknowledgement.
- Averaging across disagreeing sources.
- Tasting notes presented as the project's voice rather than as
  attributed reviewer notes.
- Removing source citations that contradict the chosen figure —
  if you reject a source's figure, the source still stays cited with
  a note explaining why.

## Questions

If you're unsure about anything, open an issue and ask before
spending significant time on a PR. The project's design has a lot
of "we considered X and chose Y" decisions; it's faster to align on
those upfront than to negotiate them in code review.
