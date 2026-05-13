#!/usr/bin/env python3
"""
WhiskyBase cross-reference resolver.

Walks every YAML entry under /data/, builds a slug index across all entity
types (distilleries, production_lines, bottlings, bottlers, concepts by
kind), then reports references that don't resolve. Output is warn-only:
per handover §8 dangling references are expected during authoring and the
check should never block the build.

Run from the repository root:

    python3 scripts/check_references.py

Reports:
    - YAML parse failures (any file that doesn't load).
    - Index summary: counts per entity type.
    - Dangling cross-references, grouped by target type, with the slug
      and the list of referencing files.
    - Duplicate id declarations (same slug declared in more than one file).
    - Invalid `source_id` references inside `peating.measurements` blocks
      and source `methodology` blocks (id cited that doesn't exist in the
      entry's `sources:` list).
    - Inline `[N]` source-citation references in prose fields where N
      does not match any source `id` declared in the entry.

Exit code is always 0 — the script reports, the human decides.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Iterator

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required. Install with: pip install pyyaml")


REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"


# ---------------------------------------------------------------------------
# Reference field map.
#
# For each YAML key that represents a slug reference, declare what kind of
# target the slug resolves against. Categories:
#   "distillery", "production_line", "bottling", "bottler",
#   "concept" (kind inferred from <kind>/<slug> namespace), "cask".
#
# Values that look like `<a>/<b>` are treated as namespaced; for concepts
# the namespace is the kind, for bottler_series the namespace is the
# bottler slug.
# ---------------------------------------------------------------------------

SCALAR_REFS = {
    # bottling.yml
    "production_line": "production_line",
    "produced_at_distillery": "distillery",
    "bottled_by": "distillery_or_bottler",
    "bottler_series": "bottler_series",
    # production_line.yml
    "distillery": "distillery",
    # source.methodology.peating_ppm
    "basis_concept": "concept",
    # maturation/finish
    "cask_type": "cask",
}

LIST_REFS = {
    # distillery.yml
    "production_lines": "production_line",
    "also_used_by_blenders": "distillery",
    "distinctive_features": "concept",
    # production_line.yml
    "bottlings": "bottling",
    "typical_cask_program": "cask",
    # concept.yml
    "related_concepts": "concept",
    "used_by": "distillery_or_bottler",
    "used_at_distilleries": "distillery",
    "adopted_by": "distillery_or_bottler",
    "alternatives": "concept",
    "prerequisites": "concept",
    "covers": "concept",
    "see_also": "concept",
    "contrast_with": "concept",
}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def iter_yaml_files() -> Iterator[Path]:
    """Yield every .yml file under /data/, in sorted order."""
    yield from sorted(DATA_DIR.rglob("*.yml"))


def load_doc(path: Path) -> tuple[dict | None, str | None]:
    """Load a YAML doc. Returns (doc, error_message)."""
    try:
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f), None
    except yaml.YAMLError as exc:
        return None, str(exc)


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------

def classify_path(path: Path) -> tuple[str, str | None]:
    """Return (entity_kind, sub_kind). For concepts the sub_kind is the
    concept kind (methodology / educational / equipment / practice /
    glossary), derived from the directory layout."""
    rel = path.relative_to(DATA_DIR)
    top = rel.parts[0]
    if top == "concepts" and len(rel.parts) >= 3:
        return "concept", rel.parts[1]
    return {
        "distilleries": ("distillery", None),
        "production_lines": ("production_line", None),
        "bottlings": ("bottling", None),
        "bottlers": ("bottler", None),
    }.get(top, ("unknown", None))


def build_index(files: Iterable[Path]) -> tuple[dict, list, list]:
    """Walk every file once. Return (index, parse_errors, duplicate_ids).

    index structure:
        {
          "distillery":      {slug: [path, ...]},
          "production_line": {slug: [path, ...]},
          "bottling":        {slug: [path, ...]},
          "bottler":         {slug: [path, ...]},
          "concept":         {f"{kind}/{slug}": [path, ...]},
          "cask":            {slug: [path, ...]},   # always empty until /data/casks/ exists
        }
    """
    index: dict[str, dict[str, list[Path]]] = defaultdict(lambda: defaultdict(list))
    parse_errors = []
    docs = []

    for path in files:
        doc, err = load_doc(path)
        if err:
            parse_errors.append((path, err))
            continue
        if not isinstance(doc, dict):
            continue
        docs.append((path, doc))
        entity, sub_kind = classify_path(path)
        sid = doc.get("id")
        if not isinstance(sid, str):
            continue
        if entity == "concept":
            index["concept"][f"{sub_kind}/{sid}"].append(path)
        elif entity in {"distillery", "production_line", "bottling", "bottler"}:
            index[entity][sid].append(path)

    duplicates = []
    for entity, slugs in index.items():
        for slug, paths in slugs.items():
            if len(paths) > 1:
                duplicates.append((entity, slug, paths))

    return docs, index, parse_errors, duplicates


# ---------------------------------------------------------------------------
# Reference walking
# ---------------------------------------------------------------------------

def walk_refs(node: Any, refs: list, source_path: Path, breadcrumbs: list[str]):
    """Recurse through a YAML node, recording slug references."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key in SCALAR_REFS and isinstance(value, str) and value:
                refs.append((SCALAR_REFS[key], value, source_path, ".".join(breadcrumbs + [key])))
            elif key in LIST_REFS and isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, str) and item:
                        refs.append((LIST_REFS[key], item, source_path, f"{'.'.join(breadcrumbs + [key])}[{i}]"))
            walk_refs(value, refs, source_path, breadcrumbs + [str(key)])
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk_refs(item, refs, source_path, breadcrumbs + [f"[{i}]"])


def collect_source_ids(doc: dict) -> set[int]:
    """Return the set of declared source IDs in the entry's sources block."""
    sources = doc.get("sources") or []
    ids = set()
    if isinstance(sources, list):
        for s in sources:
            if isinstance(s, dict) and isinstance(s.get("id"), int):
                ids.add(s["id"])
    return ids


def walk_source_id_refs(node: Any, refs: list, source_path: Path, breadcrumbs: list[str]):
    """Find every `source_id:` field used in measurement / methodology blocks."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "source_id" and isinstance(value, int):
                refs.append((value, source_path, ".".join(breadcrumbs + [key])))
            walk_source_id_refs(value, refs, source_path, breadcrumbs + [str(key)])
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk_source_id_refs(item, refs, source_path, breadcrumbs + [f"[{i}]"])


# ---------------------------------------------------------------------------
# Inline [N] source citation scan
# ---------------------------------------------------------------------------

PROSE_FIELDS = {"description", "body", "summary", "notes", "limitations",
                "consequences", "distinguishing_features", "notes_official",
                "climate_notes"}

INLINE_CITE_RE = re.compile(r"\[(\d+)\]")


def walk_prose_citations(node: Any, hits: list, source_path: Path, breadcrumbs: list[str]):
    if isinstance(node, dict):
        for key, value in node.items():
            if key in PROSE_FIELDS and isinstance(value, str):
                for m in INLINE_CITE_RE.finditer(value):
                    hits.append((int(m.group(1)), source_path, ".".join(breadcrumbs + [key])))
            walk_prose_citations(value, hits, source_path, breadcrumbs + [str(key)])
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk_prose_citations(item, hits, source_path, breadcrumbs + [f"[{i}]"])


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------

def resolve(target_kind: str, slug: str, index: dict) -> bool:
    """Return True if `slug` resolves to a real entry of `target_kind`."""
    if target_kind == "distillery":
        return slug in index["distillery"]
    if target_kind == "production_line":
        return slug in index["production_line"]
    if target_kind == "bottling":
        return slug in index["bottling"]
    if target_kind == "bottler":
        return slug in index["bottler"]
    if target_kind == "cask":
        return slug in index["cask"]
    if target_kind == "distillery_or_bottler":
        return slug in index["distillery"] or slug in index["bottler"]
    if target_kind == "concept":
        # Expect `<kind>/<slug>` form. Bare slugs are also accepted but
        # reported as "shape" issues.
        return slug in index["concept"]
    if target_kind == "bottler_series":
        if "/" not in slug:
            return False
        bottler, _series = slug.split("/", 1)
        return bottler in index["bottler"]
    return False


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def print_section(title: str):
    print()
    print(title)
    print("-" * len(title))


def main() -> int:
    files = list(iter_yaml_files())
    docs, index, parse_errors, duplicates = build_index(files)

    print(f"WhiskyBase reference check")
    print(f"==========================")
    print(f"Files scanned: {len(files)}")

    if parse_errors:
        print_section(f"YAML parse failures ({len(parse_errors)})")
        for path, err in parse_errors:
            print(f"  {rel(path)}: {err}")

    print_section("Index summary")
    print(f"  Distilleries:     {len(index['distillery'])}")
    print(f"  Production lines: {len(index['production_line'])}")
    print(f"  Bottlings:        {len(index['bottling'])}")
    print(f"  Bottlers:         {len(index['bottler'])}")
    print(f"  Concepts:         {len(index['concept'])}")
    concept_by_kind = defaultdict(int)
    for namespaced in index["concept"]:
        kind = namespaced.split("/", 1)[0]
        concept_by_kind[kind] += 1
    for kind in sorted(concept_by_kind):
        print(f"    {kind:13} {concept_by_kind[kind]}")

    if duplicates:
        print_section(f"Duplicate IDs ({len(duplicates)})")
        for entity, slug, paths in duplicates:
            print(f"  {entity}: {slug}")
            for p in paths:
                print(f"    - {rel(p)}")

    # ------------------------------------------------------------------
    # Cross-reference resolution
    # ------------------------------------------------------------------
    all_refs = []
    for path, doc in docs:
        walk_refs(doc, all_refs, path, [])

    dangling_by_kind: dict[str, dict[str, list[tuple[Path, str]]]] = defaultdict(lambda: defaultdict(list))
    resolved = 0
    for target_kind, slug, source_path, field in all_refs:
        if resolve(target_kind, slug, index):
            resolved += 1
        else:
            dangling_by_kind[target_kind][slug].append((source_path, field))

    total_dangling = sum(len(slugs) for slugs in dangling_by_kind.values())

    print_section("Cross-reference resolution")
    print(f"  Resolved:  {resolved}")
    print(f"  Dangling:  {sum(len(refs) for slugs in dangling_by_kind.values() for refs in slugs.values())} "
          f"({total_dangling} distinct slugs)")

    for kind in sorted(dangling_by_kind):
        slugs = dangling_by_kind[kind]
        print_section(f"Dangling {kind} references ({len(slugs)} slugs)")
        for slug in sorted(slugs):
            refs = slugs[slug]
            print(f"  {slug}   ({len(refs)} ref{'s' if len(refs) != 1 else ''})")
            seen_paths = set()
            for path, field in refs:
                if path in seen_paths:
                    continue
                seen_paths.add(path)
                print(f"    from {rel(path)} :: {field}")

    # ------------------------------------------------------------------
    # source_id integrity
    # ------------------------------------------------------------------
    bad_source_ids = []
    bad_inline_citations = []
    for path, doc in docs:
        declared = collect_source_ids(doc)
        sid_refs = []
        walk_source_id_refs(doc, sid_refs, path, [])
        for sid, p, field in sid_refs:
            if sid not in declared:
                bad_source_ids.append((p, field, sid, sorted(declared)))
        inline_refs = []
        walk_prose_citations(doc, inline_refs, path, [])
        for sid, p, field in inline_refs:
            if sid not in declared:
                bad_inline_citations.append((p, field, sid, sorted(declared)))

    print_section(f"Structured source_id integrity ({len(bad_source_ids)} bad)")
    if not bad_source_ids:
        print("  All structured `source_id:` references resolve.")
    else:
        for path, field, sid, declared in bad_source_ids:
            print(f"  {rel(path)} :: {field} cites {sid} (declared: {declared})")

    print_section(f"Inline [N] citation integrity ({len(bad_inline_citations)} bad)")
    if not bad_inline_citations:
        print("  All inline `[N]` prose citations resolve.")
    else:
        for path, field, sid, declared in bad_inline_citations:
            print(f"  {rel(path)} :: {field} cites [{sid}] (declared: {declared})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
