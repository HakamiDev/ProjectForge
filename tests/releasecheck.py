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
        sys.path.insert(0, str(ROOT / "tools" / "site"))
        import i18n
        langs = js_json(html, "LANGS")
        self.assertEqual(sorted(name for _, name in langs), sorted(row[3] for row in core.LANGUAGES))
        self.assertEqual([name for _, name in langs][:3], ["Arabic", "English", "Macedonian"])
        self.assertEqual(sorted(js_json(html, "I18N")), sorted(name for _, name in langs))
        self.assertEqual(set(js_json(html, "I18N")), set(i18n.U))
        for name, strings in i18n.U.items():
            self.assertEqual(sorted(strings), sorted(i18n.KEYS), name)
            self.assertTrue(all(v.strip() for v in strings.values()), name)
            for n in (len(core.PRESETS), len(core.role_library()), len(core.SKILLS)):
                self.assertIn(str(n), " ".join(strings.values()), name)
        for name in js_json(html, "I18N"):  # every FORGE_LANGUAGE value the site emits is accepted by the tool
            self.assertIn(core.loc_code(name), [None] + list(core.LOC_NAMES), name)
        self.assertNotRegex(html, r"@@[A-Z]+@@")
        self.assertNotIn("Hebrew", html)
        self.assertNotIn("claude:", html)
        self.assertIn('setLang("English",false)', html)
        self.assertIn("https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/", html)
        for needle in ("install.sh", "install.ps1", "python3 -m forge", "FORGE_LANGUAGE", "FORGE_PLATFORM"):
            self.assertIn(needle, html)
        self.assertTrue((ROOT / "forge" / "__main__.py").is_file())

    def test_coverage_document_matches_registry(self):
        document = (ROOT / "Language Coverage.md").read_text(encoding="utf-8")
        for row in core.LANGUAGES:
            self.assertIn("| " + row[0] + " |", document)
        self.assertEqual(len(core.LANGUAGES), 8)
        self.assertEqual((len(core.PRESETS), len(core.role_library()), len(core.SKILLS), len(core.SKILL_GROUPS)), (80, 334, 130, 18))


if __name__ == "__main__":
    unittest.main()
