"""Verify the artifacts that are actually packaged, after both build commands."""
import json
import re
import runpy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from forge import core


def js_json(text, name):
    match = re.search(r"(?:var |,)" + name + r"\s*=\s*", text)
    if match is None:
        raise AssertionError("Missing JavaScript data: " + name)
    return json.JSONDecoder().raw_decode(text[match.end():])[0]


class ReleaseChecks(unittest.TestCase):
    def test_built_tool_matches_source(self):
        path = ROOT / "dist" / core.TOOL_NAME
        self.assertEqual(path.read_text(encoding="utf-8"), core.single_source())
        self.assertEqual((ROOT / core.TOOL_NAME).read_text(encoding="utf-8"), path.read_text(encoding="utf-8"))
        built = runpy.run_path(str(path))
        self.assertEqual(built["load_wizard"](), core.load_wizard())
        self.assertEqual(built["load_template"](), core.load_template())
        for name in ("LANGUAGES", "SKILLS", "SKILL_GROUPS", "PRESETS"):
            self.assertEqual(built[name], getattr(core, name), name)

    def test_built_site_languages_and_catalog(self):
        html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        self.assertEqual(js_json(html, "LANGS"), [list(row) for row in core.LANGUAGES])
        source = (ROOT / "site" / "template.html").read_text(encoding="utf-8").replace("@@NSK@@", str(len(core.SKILLS)))
        for name in ("CODES", "TR"):
            self.assertEqual(js_json(html, name), js_json(core.load_wizard(), name) if name == "CODES" else js_json(source, name))
        self.assertNotRegex(html, r"@@[A-Z]+@@")
        self.assertTrue('%d skills' % len(core.SKILLS) in html)
        self.assertNotIn("Hebrew", html)
        for skin in ("fonts.css", "skin site.css"):
            self.assertIn((ROOT / "forge" / "templates" / skin).read_text(encoding="utf-8"), html)

    def test_coverage_document_matches_registry(self):
        document = (ROOT / "Language Coverage.md").read_text(encoding="utf-8")
        for row in core.LANGUAGES:
            self.assertIn("| " + row[0] + " |", document)
        self.assertEqual(len(core.LANGUAGES), 8)
        self.assertEqual((len(core.PRESETS), len(core.role_library()), len(core.SKILLS), len(core.SKILL_GROUPS)), (80, 334, 130, 18))


if __name__ == "__main__":
    unittest.main()
