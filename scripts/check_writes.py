#!/usr/bin/env python3
"""
check_writes.py -- hard-corruption scanner for WhiskyBase.

Detects the file-corruption signatures produced by the Windows <-> Linux
mount-sync race: embedded NUL bytes, silent truncation (a text file not
ending in a newline), and YAML parse failure.

Usage:
  python3 scripts/check_writes.py [FILE ...]

With no arguments it scans a default text-file set (data/, docs/,
schema/, scripts/, top-level *.md). With arguments it scans exactly
those files -- the pre-commit hook passes the staged files.

Exit status:
  0  no hard corruption
  1  hard corruption found  (the pre-commit hook blocks on this)

This is a HARD-corruption gate only. Soft findings -- dangling
cross-references, JSON Schema warnings -- belong to check_references.py,
which is deliberately warn-only and never blocks a commit.
"""
import os
import sys
import glob

try:
    import yaml
except ImportError:
    yaml = None

TEXT_EXT = {".yml", ".yaml", ".md", ".py", ".astro", ".txt",
            ".json", ".ts", ".js", ".css"}

DEFAULT_GLOBS = [
    "data/**/*.yml",
    "docs/**/*.md",
    "schema/**/*.yml",
    "schema/**/*.json",
    "scripts/**/*.py",
    "*.md",
]


def scan(path):
    """Return a list of hard-corruption findings for one file."""
    findings = []
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return ["unreadable: %s" % exc]
    if data == b"":
        return findings
    nul = data.count(b"\x00")
    if nul:
        findings.append("%d NUL byte(s) present" % nul)
    if not data.endswith(b"\n"):
        findings.append("no trailing newline (truncation suspect)")
    if path.lower().endswith((".yml", ".yaml")) and yaml is not None:
        try:
            yaml.safe_load(data)
        except Exception as exc:
            findings.append("YAML parse failure: %s"
                             % str(exc).splitlines()[0])
    return findings


def collect_default():
    out = set()
    for pat in DEFAULT_GLOBS:
        out.update(glob.glob(pat, recursive=True))
    return sorted(out)


def main(argv):
    files = argv[1:] if len(argv) > 1 else collect_default()
    bad = {}
    scanned = 0
    for path in files:
        if os.path.splitext(path)[1].lower() not in TEXT_EXT:
            continue
        if not os.path.isfile(path):
            continue
        scanned += 1
        findings = scan(path)
        if findings:
            bad[path] = findings
    print("check_writes: %d text file(s) scanned" % scanned)
    if bad:
        print("HARD CORRUPTION in %d file(s):" % len(bad))
        for path in sorted(bad):
            for finding in bad[path]:
                print("  %s :: %s" % (path, finding))
        return 1
    print("  no hard corruption found.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
