#!/usr/bin/env python3
"""
Unit tests for the WhiskyBase guard-rail scripts.

Covers check_writes.scan (the hard-corruption signatures) and the pure
logic functions in check_references (reference resolution, duplicate
detection, allowlist loading, schema-version currency, and cross-file
consistency). These are the project's commit gates, so a small fixture
set guards against regressions in the checks themselves.

Run from the repo root:
    python3 -m unittest scripts.test_checks
    python3 scripts/test_checks.py
"""
import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cw = _load("check_writes")
cr = _load("check_references")
DATA = cr.DATA_DIR


class TestCheckWritesScan(unittest.TestCase):
    def _scan_bytes(self, data: bytes):
        with tempfile.NamedTemporaryFile("wb", suffix=".yml", delete=False) as fh:
            fh.write(data)
            path = fh.name
        try:
            return cw.scan(path)
        finally:
            os.unlink(path)

    def test_clean_file_has_no_findings(self):
        self.assertEqual(self._scan_bytes(b"id: x\nname: X\n"), [])

    def test_nul_bytes_detected(self):
        findings = self._scan_bytes(b"id: x\n\x00\x00")
        self.assertTrue(any("NUL byte" in f for f in findings))

    def test_missing_trailing_newline_detected(self):
        findings = self._scan_bytes(b"id: x\nname: X")
        self.assertTrue(any("trailing newline" in f for f in findings))

    def test_yaml_parse_failure_detected(self):
        # A NUL also makes YAML unparseable; assert the parse-failure signal too.
        findings = self._scan_bytes(b"id: x\n\x00\n")
        self.assertTrue(any("YAML parse failure" in f for f in findings))

    def test_empty_file_is_clean(self):
        self.assertEqual(self._scan_bytes(b""), [])


class TestResolve(unittest.TestCase):
    def setUp(self):
        self.index = {
            "distillery": {"harris": [1]},
            "production_line": {"harris-the-hearach": [1]},
            "bottling": {},
            "bottler": {"cadenheads": [1]},
            "cask": {"bourbon-barrel": [1]},
            "supplier": {},
            "concept": {"glossary/peat": [1]},
        }

    def test_distillery_resolves(self):
        self.assertTrue(cr.resolve("distillery", "harris", self.index))
        self.assertFalse(cr.resolve("distillery", "nope", self.index))

    def test_distillery_or_bottler(self):
        self.assertTrue(cr.resolve("distillery_or_bottler", "cadenheads", self.index))
        self.assertTrue(cr.resolve("distillery_or_bottler", "harris", self.index))
        self.assertFalse(cr.resolve("distillery_or_bottler", "nope", self.index))

    def test_cask_or_concept(self):
        self.assertTrue(cr.resolve("cask_or_concept", "bourbon-barrel", self.index))
        self.assertTrue(cr.resolve("cask_or_concept", "glossary/peat", self.index))

    def test_bottler_series_requires_slash_and_known_bottler(self):
        self.assertTrue(cr.resolve("bottler_series", "cadenheads/authentic", self.index))
        self.assertFalse(cr.resolve("bottler_series", "cadenheads", self.index))
        self.assertFalse(cr.resolve("bottler_series", "unknown/series", self.index))


class TestSchemaVersionCurrency(unittest.TestCase):
    def test_stale_version_flagged(self):
        docs = [(DATA / "bottlings" / "x.yml", {"id": "x", "schema_version": 0.1})]
        findings = cr.check_schema_versions(docs)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0][2], "0.1")   # declared
        self.assertEqual(findings[0][3], "0.2")   # expected for bottling

    def test_current_version_not_flagged(self):
        docs = [
            (DATA / "bottlings" / "x.yml", {"id": "x", "schema_version": 0.2}),
            (DATA / "production_lines" / "y.yml", {"id": "y", "schema_version": "0.2.1"}),
        ]
        self.assertEqual(cr.check_schema_versions(docs), [])


class TestConsistency(unittest.TestCase):
    def test_hard_contradiction_detected(self):
        docs = [
            (DATA / "production_lines" / "harris-the-hearach.yml",
             {"id": "harris-the-hearach", "distillery": "harris"}),
            (DATA / "bottlings" / "b.yml",
             {"id": "b", "production_line": "harris-the-hearach",
              "produced_at_distillery": "bruichladdich"}),
        ]
        hard, _soft = cr.check_consistency(docs, {})
        self.assertEqual(len(hard), 1)

    def test_consistent_pair_has_no_hard_finding(self):
        docs = [
            (DATA / "production_lines" / "harris-the-hearach.yml",
             {"id": "harris-the-hearach", "distillery": "harris"}),
            (DATA / "bottlings" / "b.yml",
             {"id": "b", "production_line": "harris-the-hearach",
              "produced_at_distillery": "harris"}),
        ]
        hard, _soft = cr.check_consistency(docs, {})
        self.assertEqual(hard, [])

    def test_mirroring_gap_is_soft(self):
        docs = [
            (DATA / "production_lines" / "l.yml", {"id": "l", "distillery": "harris"}),
            (DATA / "distilleries" / "bruichladdich.yml",
             {"id": "bruichladdich", "production_lines": ["l"]}),
        ]
        hard, soft = cr.check_consistency(docs, {})
        self.assertEqual(hard, [])
        self.assertEqual(len(soft), 1)


class TestAllowlist(unittest.TestCase):
    def test_allowlist_loads_real_file(self):
        allow = cr.load_allowlist()
        # The seeded worm-tub forward refs should be present.
        self.assertIn("distillery:talisker", allow)
        self.assertIn("distillery:mortlach", allow)


class TestClassifyPath(unittest.TestCase):
    def test_concept_kind_extracted(self):
        entity, sub = cr.classify_path(DATA / "concepts" / "glossary" / "peat.yml")
        self.assertEqual((entity, sub), ("concept", "glossary"))

    def test_entity_dirs(self):
        self.assertEqual(cr.classify_path(DATA / "distilleries" / "x.yml")[0], "distillery")
        self.assertEqual(cr.classify_path(DATA / "casks" / "x.yml")[0], "cask")


if __name__ == "__main__":
    unittest.main(verbosity=2)
