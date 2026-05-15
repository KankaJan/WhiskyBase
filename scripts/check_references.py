#!/usr/bin/env python3
"""
WhiskyBase cross-reference resolver.

Walks every YAML entry under /data/, builds a slug index across all entity
types (distilleries, production_lines, bottlings, bottlers, casks, concepts
by kind), then reports references that don't resolve. Output is warn-only:
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


SCALAR_REFS = {
    "production_line": "production_line",
    "produced_at_distillery": "distillery",
    "bottled_by": "distillery_or_bottler",
    "bottler_series": "bottler_series",
    "distillery": "distillery",
    "basis_concept": "concept",
    "cask_type": "cask",
    # `parent` is handled specially in walk_refs (context-dependent — only
    # a slug reference when it appears under `related:` on a cask entry;
    # `ownership.parent` on a distillery is a company name, not a slug).
}

LIST_REFS = {
    "production_lines": "production_line",
    "also_used_by_blenders": "distillery",
    "distinctive_features": "concept",
    "bottlings": "bottling",
    "typical_cask_program": "cask",
    "related_concepts": "concept",
    "used_by": "distillery_or_bottler",
    "used_at_distilleries": "distillery",
    "adopted_by": "distillery_or_bottler",
    "alternatives": "cask_or_concept",
    "prerequisites": "concept",
    "covers": "concept",
    "see_also": "concept",
    "contrast_with": "concept",
}


def iter_yaml_files() -> Iterator[Path]:
    yield from sorted(DATA_DIR.rglob("*.yml"))


def load_doc(path: Path):
    try:
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f), None
    except yaml.YAMLError as exc:
        return None, str(exc)


def classify_path(path: Path):
    rel = path.relative_to(DATA_DIR)
    top = rel.parts[0]
    if top == "concepts" and len(rel.parts) >= 3:
        return "concept", rel.parts[1]
    return {
        "distilleries": ("distillery", None),
        "production_lines": ("production_line", None),
        "bottlings": ("bottling", None),
        "bottlers": ("bottler", None),
        "casks": ("cask", None),
    }.get(top, ("unknown", None))


def build_index(files: Iterable[Path]):
    index = defaultdict(lambda: defaultdict(list))
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
        elif entity in {"distillery", "production_line", "bottling", "bottler", "cask"}:
            index[entity][sid].append(path)

    duplicates = []
    for entity, slugs in index.items():
        for slug, paths in slugs.items():
            if len(paths) > 1:
                duplicates.append((entity, slug, paths))

    return docs, index, parse_errors, duplicates


def walk_refs(node, refs, source_path, breadcrumbs):
    if isinstance(node, dict):
        for key, value in node.items():
            if key in SCALAR_REFS and isinstance(value, str) and value:
                refs.append((SCALAR_REFS[key], value, source_path, ".".join(breadcrumbs + [key])))
            elif key == "parent" and isinstance(value, str) and value and breadcrumbs and breadcrumbs[-1] == "related":
                # Context-sensitive: `related.parent` is a cask slug
                # reference; `ownership.parent` is a company name string,
                # not a slug.
                refs.append(("cask", value, source_path, ".".join(breadcrumbs + [key])))
            elif key in LIST_REFS and isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, str) and item:
                        refs.append((LIST_REFS[key], item, source_path, f"{'.'.join(breadcrumbs + [key])}[{i}]"))
            walk_refs(value, refs, source_path, breadcrumbs + [str(key)])
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk_refs(item, refs, source_path, breadcrumbs + [f"[{i}]"])


def collect_source_ids(doc):
    sources = doc.get("sources") or []
    ids = set()
    if isinstance(sources, list):
        for s in sources:
            if isinstance(s, dict) and isinstance(s.get("id"), int):
                ids.add(s["id"])
    return ids


def walk_source_id_refs(node, refs, source_path, breadcrumbs):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "source_id" and isinstance(value, int):
                refs.append((value, source_path, ".".join(breadcrumbs + [key])))
            walk_source_id_refs(value, refs, source_path, breadcrumbs + [str(key)])
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk_source_id_refs(item, refs, source_path, breadcrumbs + [f"[{i}]"])


PROSE_FIELDS = {"description", "body", "summary", "notes", "limitations",
                "consequences", "distinguishing_features", "notes_official",
                "climate_notes"}

INLINE_CITE_RE = re.compile(r"\[(\d+)\]")


def walk_prose_citations(node, hits, source_path, breadcrumbs):
    if isinstance(node, dict):
        for key, value in node.items():
            if key in PROSE_FIELDS and isinstance(value, str):
                for m in INLINE_CITE_RE.finditer(value):
                    hits.append((int(m.group(1)), source_path, ".".join(breadcrumbs + [key])))
            walk_prose_citations(value, hits, source_path, breadcrumbs + [str(key)])
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk_prose_citations(item, hits, source_path, breadcrumbs + [f"[{i}]"])


def resolve(target_kind, slug, index):
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
    if target_kind == "cask_or_concept":
        return slug in index["cask"] or slug in index["concept"]
    if target_kind == "concept":
        return slug in index["concept"]
    if target_kind == "bottler_series":
        if "/" not in slug:
            return False
        bottler, _series = slug.split("/", 1)
        return bottler in index["bottler"]
    return False


def rel(p):
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def print_section(title):
    print()
    print(title)
    print("-" * len(title))


def main():
    files = list(iter_yaml_files())
    docs, index, parse_errors, duplicates = build_index(files)

    print("WhiskyBase reference check")
    print("==========================")
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
    print(f"  Casks:            {len(index['cask'])}")
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

    all_refs = []
    for path, doc in docs:
        walk_refs(doc, all_refs, path, [])

    dangling_by_kind = defaultdict(lambda: defaultdict(list))
    resolved = 0
    for target_kind, slug, source_path, field in all_refs:
        if resolve(target_kind, slug, index):
            resolved += 1
        else:
            dangling_by_kind[target_kind][slug].append((source_path, field))

    total_dangling_slugs = sum(len(slugs) for slugs in dangling_by_kind.values())
    total_dangling_refs = sum(len(refs) for slugs in dangling_by_kind.values() for refs in slugs.values())

    print_section("Cross-reference resolution")
    print(f"  Resolved:  {resolved}")
    print(f"  Dangling:  {total_dangling_refs} ({total_dangling_slugs} distinct slugs)")

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
        print("  All inline source citations resolve.")
    else:
        for path, field, sid, declared in bad_inline_citations:
            citation = "[" + str(sid) + "]"
            print(f"  {rel(path)} :: {field} cites {citation} (declared: {declared})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
