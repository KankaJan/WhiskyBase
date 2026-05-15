---
name: safe-bulk-writes
description: Operating procedure for writing multiple new files in a single conversational turn. Triggers any time Claude is about to create or rewrite 3 or more files in one turn — particularly common when populating a new entity type (e.g. /data/casks/, /data/bottlers/, /data/distilleries/, /data/concepts/<kind>/), scaffolding multiple new schema/template files, generating a batch of test cases, or rewriting several files after a critical-analysis pass. Encodes the lesson from the 2026-05-15 cask-population session, where a parallel batch of seven Write tool calls in a single message produced trailing NUL-byte padding on most files and silent mid-content truncation on two of them.
---

# Safe bulk-writes — WhiskyBase

## The rule

When you need to create or rewrite 3 or more files via the Write tool
in a single conversational turn:

1. **Cap parallel batches at 4 files.** Writes in batches of 5 or more
   have produced corruption (trailing NUL-byte padding, occasional
   silent mid-content truncation). 1–4 in a batch has been reliable.
2. **Verify after every batch.** Don't let multiple unverified batches
   accumulate. Run `scripts/check_references.py` after each batch and
   read the output before issuing the next.
3. **For YAML data files specifically, run the cleanup pass after every
   bulk-write session** to strip any trailing NUL padding that slipped
   through:

   ```python
   import glob
   for fn in glob.glob('data/**/*.yml', recursive=True):
       with open(fn, 'rb') as f:
           data = f.read()
       cleaned = data.rstrip(b'\x00')
       if len(cleaned) != len(data):
           with open(fn, 'wb') as f:
               f.write(cleaned)
   ```

   The cleanup is lossless — NUL bytes only appear as trailing padding,
   never inside content.

4. **For truncated files, re-write serially (one Write call at a
   time).** The truncation failure mode is rarer than padding but
   harder to recover from, because the file content is genuinely
   missing. Files where the YAML parses but the schema-level
   structure is incomplete (e.g. `sources:` missing entirely on a
   file that should have sources) need a fresh single-call Write.

5. **For files larger than ~10 KB, prefer bash-mediated writes.**
   The Write tool has produced silent truncation on single Writes
   of files in the 11–18 KB range. The reliable workaround is to
   write via bash using Python or a heredoc. Example pattern to
   repair a truncated tail:

   ```bash
   python3 << 'PYEOF'
   fn = 'data/path/to/file.yml'
   with open(fn) as f:
       content = f.read()
   idx = content.rfind('schema_version:')
   if idx > 0:
       fixed = content[:idx] + """schema_version: 0.1
   confidence: medium
   last_reviewed: 2026-05-15
   contributors: []
   """
       with open(fn, 'w') as f:
           f.write(fixed)
   PYEOF
   ```

   For new large files: write the structural skeleton via Write
   (small, reliable), then bash-append the body content in chunks.
   Or write the entire file via a bash heredoc up front.

## Why this rule exists

In the 2026-05-15 cask-population session, a single tool-call message
containing seven Write operations produced two simultaneous failure
modes:

- **Trailing NUL-byte padding** on 6 of 7 files. Content intact, but
  YAML parse failed on the `\x00` characters appended at end-of-file.
  Stripping the NULs (rstrip(b'\x00')) recovered the files losslessly.
- **Silent mid-content truncation** on 2 of 7 files. `fino-sherry-
  butt.yml` ended at `used_by:` with no sources or metadata block;
  `wine-cask.yml` ended mid-sentence in the description. These
  required complete re-writes.

Subsequent re-writes in batches of ≤4 succeeded without corruption.

A separate corruption pattern was observed later in the same
session and in the 2026-05-15 concept-page session:

- **Large-file truncation in single Writes.** Files larger than
  approximately 11 KB have been silently truncated by the Write
  tool even when written individually (not in a batch). The
  truncation point on `aromatic-compounds-in-whisky.yml` was
  exactly the same — 10964 bytes, mid-word in the final metadata
  block — on two consecutive Write attempts of the same content.
  Repairing the tail by appending the missing bytes via bash
  recovered the file.
  
  Tentative threshold: single Writes have produced corruption-free
  files up to roughly 10 KB; files between ~11 KB and ~18 KB have
  shown truncation in observed cases; files above ~18 KB have not
  been attempted as single Writes in this project. The threshold
  may move; treat any file over ~10 KB as a candidate for the
  bash-write workaround below.

## Verification routine

After any Write-heavy turn, run the resolver:

```bash
python3 scripts/check_references.py
```

The script's first output section is `YAML parse failures (N)`. If
`N > 0`, every named file needs attention before declaring the turn
complete. The most common failure modes after bulk writes:

| Failure | Cause | Fix |
|---|---|---|
| `unacceptable character #x0000` | Trailing NUL padding | Run rstrip-cleanup snippet above |
| `could not find expected ':'` | Mid-content truncation, key/value parse confusion | Re-Write the file with single Write call |
| `mapping values are not allowed here` | YAML syntax error in content | Read the file, find and fix the syntax error |

The script's later sections also catch structural truncation that
parses but is incomplete — if a cask entry's `sources_count` is 0
when it should be 2, the resolver will report inline `[N]` citations
as dangling because the source IDs they reference were never indexed.

## Pre-completion checklist

Before reporting a Write-heavy turn as complete:

- [ ] All Writes done in batches of ≤4?
- [ ] After each batch, `scripts/check_references.py` produced zero
      parse failures?
- [ ] After the last batch, ran the rstrip-cleanup snippet as a
      precaution?
- [ ] Final resolver run produces the expected dangling-reference
      counts (no surprise dangling refs from truncation)?

If any of the above is "no," resolve before moving on.

## What this rule does not cover

- **Edit tool**. The corruption described above is specific to the
  Write tool. The Edit tool has produced its own occasional issues
  (NUL bytes have been observed there too on rare occasions), but
  the volume is lower and the cleanup is the same.
- **Single Writes**. A single Write in isolation, or a single Write
  per turn, has not been observed to corrupt.
- **Non-YAML files**. The verification routine for Python scripts is
  `python -m py_compile <file>`; for Markdown, visual review by
  reading the rendered file. The batching rule still applies.

## See also

- `scripts/check_references.py` — the verification routine.
- `docs/contributing.md` — broader contributor guidance (currently
  a stub; this skill predates a fuller version of that doc).
