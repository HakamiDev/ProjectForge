import argparse
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from forge import core  # noqa: E402


def new_project(tmp, preset="general", owner="الرئيس"):
    return core.create_project(tmp, "مشروع اختبار", "هدف الاختبار", owner, preset, None, None, [])


class ForgeTests(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory(prefix="forge test ")
        self.tmp = Path(self._t.name)

    def tearDown(self):
        self._t.cleanup()

    def test_create_and_check(self):
        root = new_project(self.tmp)
        self.assertEqual(core.check_project(root), [])
        self.assertTrue((root / "Office" / core.OFFICE_FILE).is_file())
        self.assertFalse([p for p in root.rglob("*") if "_" in p.name])

    def test_presets(self):
        for preset in core.PRESETS:
            with tempfile.TemporaryDirectory(prefix="forge preset ") as d:
                root = core.create_project(d, "مشروع %s" % preset, "هدف", "الرئيس", preset, None, None, [])
                team = core.load_team(root)
                self.assertEqual(team["roster"][0]["name"], core.COMPASS)
                self.assertIn(core.QA_NAME, [r["name"] for r in team["roster"]])

    def test_site_data_schema(self):
        root = new_project(self.tmp)
        d = core.site_data(root)
        for k in ("q", "gen", "goal", "team", "tasks", "stc", "nt", "circs", "dec", "out", "tpl", "ico", "ei", "th", "png", "imgs", "nimg"):
            self.assertIn(k, d)
        self.assertEqual(len(d["ei"]), len(d["team"]))
        self.assertTrue(all(e in d["ico"] for e in d["ei"]))
        self.assertEqual(d["nt"], len(d["tasks"]))

    def test_rendered_site(self):
        root = new_project(self.tmp)
        html = (root / "Office" / core.OFFICE_FILE).read_text(encoding="utf-8")
        self.assertNotIn("@@", html)
        self.assertNotIn("Makkah", html)
        for bad in ("مكة", "Brand/Phase", "Invitation", "دعوتك", "الدعوات"):
            self.assertNotIn(bad, html, bad)
        m = re.search(r"var D=(\{.*?\});\nvar \$=", html, re.S)
        self.assertTrue(json.loads(m.group(1))["team"])

    def test_owner_and_hostile_names(self):
        with tempfile.TemporaryDirectory(prefix="forge own ") as d:
            root = core.create_project(d, "مشروع <b>x</b>", "هدف \"مقتبس\" </script>", "صاحب 'المشروع'", "general", None, None, [])
            html = (root / "Office" / core.OFFICE_FILE).read_text(encoding="utf-8")
            self.assertEqual(html.count("</script>"), html.count("<script"))
            self.assertNotIn("<b>x</b>", html.split("<script>")[0])

    def test_rows_status_flow(self):
        root = new_project(self.tmp)
        core.cmd_add_row(argparse.Namespace(root=str(root), frm="البوصلة", to="رئيس المنتج", task="مهمة", inputs="—", output="`Outputs/a.md`",
                                            after="1", due="—", next="—", cap=5, force=False))
        tasks = core.read_board(root)["tasks"]
        self.assertEqual([t["n"] for t in tasks], [1, 2])
        self.assertEqual(core.ready_tasks(tasks, "رئيس المنتج"), [])
        core.cmd_set_status(argparse.Namespace(root=str(root), n=1, status="مسلّمة", note=None, by=None, owner_order=False))
        self.assertEqual(len(core.ready_tasks(core.read_board(root)["tasks"], "رئيس المنتج")), 1)
        with self.assertRaises(SystemExit):
            core.cmd_set_status(argparse.Namespace(root=str(root), n=1, status="معتمدة", note=None, by=None, owner_order=False))
        q = core.site_data(root)["q"]["rows"]
        self.assertEqual([r["wait"] for r in q], [[], []])
        self.assertTrue(q[1]["ready"])

    def test_report_export_and_sla(self):
        root = new_project(self.tmp, preset="transformation")
        core.cmd_set_status(argparse.Namespace(root=str(root), n=1, status="مسلّمة", note=None, by=None, owner_order=False))
        core.cmd_decide(argparse.Namespace(root=str(root), text="قرار", tag=None, source=None))
        m = core.metrics(root)
        self.assertEqual((m["total"], m["done"], m["decisions"]), (1, 1, 1))
        self.assertIsNotNone(m["cycle_avg"])
        core.cmd_report(argparse.Namespace(root=str(root)))
        self.assertTrue(list((root / "Docs" / "Reports").glob("Report *.md")))
        core.cmd_export(argparse.Namespace(root=str(root)))
        for f in ("Board.csv", "Team.csv", "Decisions.csv", "Metrics.csv"):
            self.assertTrue((root / "Data" / f).read_text(encoding="utf-8").startswith("\ufeff"))
        self.assertIn("غيّر حالة الصف 1", (root / "Agents" / "Audit Log.md").read_text(encoding="utf-8"))
        # قرار معلق متأخر عن 48 ساعة يظهر في الفحص
        b = root / "Agents" / "Board.md"
        old = (core.now() - core.dt.timedelta(hours=60))
        text = b.read_text(encoding="utf-8").replace("(لا شيء)", "1. (%s) هل نعتمد الأداة؟ التوصية: نعم" % core.fmt_dt(old), 1)
        b.write_text(text, encoding="utf-8")
        self.assertTrue(any("تجاوز 48" in p for p in core.check_project(root)))

    def test_all_presets_have_qa(self):
        for preset, roles in core.PRESETS.items():
            self.assertIn(core.QA_NAME, [r[0] for r in roles], preset)
            self.assertFalse([r for r in roles if "_" in r[0]])

    def test_never_overwrites(self):
        root = new_project(self.tmp)
        f = root / "CLAUDE.md"
        f.write_text("مخصص", encoding="utf-8")
        core.write_new(f, "جديد", [])
        self.assertEqual(f.read_text(encoding="utf-8"), "مخصص")

    def test_customize_roles(self):
        base = core.PRESETS["operations"]
        r = core.customize_roles(base, ["محلل الأداء", core.QA_NAME], ["مراجع قانوني | الامتثال النظامي"])
        names = [x[0] for x in r]
        self.assertNotIn("محلل الأداء", names)
        self.assertIn("مراجع قانوني", names)
        self.assertIn(core.QA_NAME, names)
        r2 = core.customize_roles([("أ", "أ", "", "Claude")], [], [])
        self.assertIn(core.QA_NAME, [x[0] for x in r2])

    def test_wizard_template_and_defaults(self):
        w = core.load_wizard()
        self.assertIn("@@TOKEN@@", w)
        self.assertEqual(set(core.PRESET_LABELS), set(core.PRESETS))
        self.assertEqual(set(core.PRESET_BLURBS), set(core.PRESETS))

    def test_specializations_and_library(self):
        self.assertGreaterEqual(len(core.PRESETS), 30)
        lib = core.role_library()
        self.assertGreaterEqual(len(lib), 100)
        for k, roles in core.PRESETS.items():
            self.assertIn(core.QA_NAME, [r[0] for r in roles], k)
            self.assertTrue(all("_" not in r[0] for r in roles), k)
            self.assertIn(core.PRESET_META[k][3], core.PRESET_GROUPS, k)

    def test_shortcut_bundle(self):
        import os
        import plistlib
        from unittest import mock
        home = Path(self.tmp) / "home"
        (home / "Desktop").mkdir(parents=True)
        with mock.patch.dict(os.environ, {"HOME": str(home), "USERPROFILE": str(home)}), \
                mock.patch.object(core.sys, "platform", "darwin"), mock.patch.object(core.Path, "home", return_value=home):
            app = core.install_shortcut()
        self.assertTrue(app.name.endswith(".app"))
        run = app / "Contents" / "MacOS" / "ProjectForge"
        self.assertTrue(os.access(run, os.X_OK))
        info = plistlib.loads((app / "Contents" / "Info.plist").read_bytes())
        self.assertEqual(info["CFBundleExecutable"], "ProjectForge")
        icns = (app / "Contents" / "Resources" / "AppIcon.icns").read_bytes()
        self.assertEqual(icns[:4], b"icns")
        self.assertEqual(int.from_bytes(icns[4:8], "big"), len(icns))
        self.assertIn(b"\x89PNG", icns[:40])
        tool = home / "Library" / "Application Support" / "Project Forge" / core.TOOL_NAME
        compile(tool.read_text(encoding="utf-8"), "tool", "exec")

    def test_skills_and_library(self):
        self.assertGreaterEqual(len(core.SKILLS), 20)
        root = new_project(self.tmp)
        team = core.load_team(root)
        self.assertTrue(team["skills"])
        for k in team["skills"]:
            self.assertTrue((root / "Agents" / "Skills" / ("%s.md" % core.SKILLS[k][0])).is_file())
        self.assertTrue((root / "Agents" / "Skills" / "Read Me.md").is_file())
        lib = (root / "Agents" / "Commands Library.md").read_text(encoding="utf-8")
        self.assertIn("البوصلة", lib)
        self.assertIn("export", lib)
        groups = core.commands_library(team)
        self.assertGreaterEqual(len(groups), 5)
        self.assertTrue(all(it["text"] for g in groups for it in g["items"]))
        self.assertGreaterEqual(len(core.PRESETS), 70)
        self.assertTrue(all(core.preset_tags(k) for k in core.PRESETS))
        self.assertTrue(set(core.PRESET_SYNONYMS) <= set(core.PRESETS))
        for k in core.PRESETS:
            self.assertIn(k, core.GOAL_EXAMPLES)
            self.assertTrue(core.skills_for(k))

    def test_custom_team_has_no_missing_product_lead(self):
        roles = core.customize_roles(core.PRESETS["blank"], [], ["مدير المنتج والهندسة | تطوير | شيفرة", "مدير المحتوى | محتوى | موقع"])
        root = core.create_project(self.tmp, "فريق ثلاثي", "هدف", "الرئيس", "blank", roles, None, [])
        self.assertEqual(core.check_project(root), [])
        for f in root.rglob("*.md"):
            t = f.read_text(encoding="utf-8")
            self.assertNotIn("{{", t, f.name)
            self.assertNotIn("رئيس المنتج", t, f.name)
        ref = (root / "فريق ثلاثي Project Reference.md").read_text(encoding="utf-8")
        self.assertIn("مدير المنتج والهندسة وحده", ref)

    def test_demo_tasks_never_reach_agents(self):
        root = new_project(self.tmp)
        html = (root / "Office" / core.OFFICE_FILE).read_text(encoding="utf-8")
        self.assertIn("var DEMO=0", html)
        self.assertEqual(html.count("D.nt>3"), 1)
        for f in (root / "Agents").rglob("*"):
            if f.is_file():
                self.assertNotIn("مثال: ", f.read_text(encoding="utf-8", errors="ignore"), f.name)
        d = core.site_data(root)
        self.assertFalse([t for t in d["tasks"] if "مثال" in t["task"]])
        self.assertFalse([r for r in d["q"]["rows"] if "مثال" in r["task"]])

    def test_platform_and_language(self):
        roles = [("مدير", "إدارة", "إدارة", "ChatGPT"), ("كاتب", "كتابة", "كتابة", "Claude")]
        roles = core.customize_roles(roles, [], [])
        root = core.create_project(self.tmp, "خيارات", "هدف", "الرئيس", "blank", roles, None, [], None, "ChatGPT", "English")
        team = json.loads((root / "Agents" / "Team.json").read_text(encoding="utf-8"))
        self.assertEqual((team["platform"], team["language"]), ("ChatGPT", "English"))
        self.assertEqual({r["name"]: r["platform"] for r in team["roster"]}["مدير"], "ChatGPT")
        self.assertEqual({r["name"]: r["platform"] for r in team["roster"]}["كاتب"], "Claude")
        self.assertIn("English", (root / "CLAUDE.md").read_text(encoding="utf-8"))
        self.assertIn("English", (root / "Agents" / "Roles" / "كاتب.md").read_text(encoding="utf-8"))
        self.assertEqual(core.check_project(root), [])
        self.assertEqual(core.norm_platform("chatgpt"), "ChatGPT")
        self.assertEqual(core.norm_platform(None), "Claude")
        for raw, want in (("grok", "Grok"), ("غروك", "Grok"), ("Gemini", "Gemini"), ("Google Gemini", "Gemini"), ("جيميناي", "Gemini"), ("xyz", "Claude")):
            self.assertEqual(core.norm_platform(raw), want)
        roles2 = core.customize_roles([("مدير", "إدارة", "إدارة", "Grok"), ("كاتب", "كتابة", "كتابة", "Gemini")], [], [])
        root2 = core.create_project(self.tmp, "منصات", "هدف", "الرئيس", "blank", roles2, None, [], None, "Gemini", "English")
        plat = {r["name"]: r["platform"] for r in json.loads((root2 / "Agents" / "Team.json").read_text(encoding="utf-8"))["roster"]}
        self.assertEqual((plat["مدير"], plat["كاتب"]), ("Grok", "Gemini"))
        self.assertEqual(core.check_project(root2), [])
        self.assertTrue(all(d["plat"] in core.PLATFORMS for d in core.site_data(root2)["team"]))
        self.assertIn("العربية", core.lang_note(""))

    def test_attention_and_status(self):
        import datetime as dt
        root = new_project(self.tmp)
        self.assertEqual(core.attention(root), [])

        def add(to, task, after="—", due="—"):
            core.cmd_add_row(argparse.Namespace(root=str(root), frm="البوصلة", to=to, task=task, inputs="—", output="—", after=after, due=due, next="—", cap=5, force=False))

        add("رئيس المنتج", "كتابة المرجع", due="2026-10-01")
        add("رئيس المنتج", "مراجعة المرجع", after="2")
        add("رئيس المنتج", "مهمة معطلة", after="99")
        kinds = {(i["kind"], i["n"]) for i in core.attention(root)}
        self.assertIn(("overdue", 2), kinds)
        self.assertIn(("blocked", 3), kinds)
        self.assertIn(("dead", 4), kinds)
        later = core.now() + dt.timedelta(days=5)
        kinds = {(i["kind"], i["n"]) for i in core.attention(root, at=later)}
        self.assertIn(("stalled", 1), kinds)
        att = core.attention(root)
        self.assertEqual([i["sev"] for i in att], sorted(i["sev"] for i in att))
        d = core.site_data(root)
        self.assertEqual(len(d["att"]), len(att))
        self.assertIn("تجاوز موعده", core.report_md(core.metrics(root)))
        self.assertEqual(core.parse_due("٣٠ أكتوبر ٢٠٢٦").day, 30)
        self.assertEqual(core.parse_due("2026/11/05").month, 11)
        self.assertIsNone(core.parse_due("—"))
        self.assertEqual([core.human_span(h) for h in (0.2, 1, 2, 5, 30, 48, 72, 24 * 11)], ["أقل من ساعة", "ساعة", "ساعتان", "5 ساعات", "30 ساعة", "يومان", "3 أيام", "11 يومًا"])
        with self.assertRaises(SystemExit) as cm:
            core.cmd_status(argparse.Namespace(root=str(root), json=False, strict=True))
        self.assertEqual(cm.exception.code, 2)
        core.cmd_status(argparse.Namespace(root=str(root), json=True, strict=False))

    def test_no_private_traces(self):
        """المستودع عام: لا يجوز أن تتسرب أسماء ملفات أو مسارات أو قرارات داخلية إلى القوالب."""
        import re
        bad = ["مرسال", "Mersal", "Shared Assets", "Hyperiux", "Brand Tokens", "UI Motion Kit",
               "Glass Button 1", "Glass Extras", "Office Glass Element", "Framer Components", "رقم 1\\\""]
        pat = re.compile(r"القرار \d+(?![\d ]*ساعة)|Templates/")
        d = Path(core.__file__).parent / "templates"
        for f in d.iterdir():
            if f.suffix in (".html", ".css"):
                t = f.read_text(encoding="utf-8")
                for b in bad:
                    self.assertNotIn(b, t, (f.name, b))
                self.assertIsNone(pat.search(t), f.name)

    def test_single_file_build(self):
        src = core.single_source()
        self.assertIn('_TEMPLATE_Z = """', src)
        self.assertGreater(len(src), 100000)
        self.assertIn('_WIZARD_Z = """', src)
        compile(src, "single", "exec")

    def test_language_choices_have_complete_interface_translations(self):
        """Every advertised UI language must have translations on both surfaces."""
        def js_json(text, name):
            match = re.search(r"(?:var |,)" + name + r"\s*=\s*", text)
            self.assertIsNotNone(match, name)
            return json.JSONDecoder().raw_decode(text[match.end():])[0]

        wizard = core.load_wizard()
        site = (Path(core.__file__).parent.parent / "site" / "template.html").read_text(encoding="utf-8")
        choices = {row[0] for row in core.LANGUAGES}
        for surface in (wizard, site):
            codes = js_json(surface, "CODES")
            translations = js_json(surface, "TR")
            self.assertEqual(choices, {"العربية", "English"} | set(codes))
            self.assertEqual(set(codes.values()), set(translations))
            self.assertEqual(len(choices), 27)
            self.assertNotIn("he", translations)
            self.assertNotIn("Hebrew", surface)
            keys = set(next(iter(translations.values())))
            for code, strings in translations.items():
                self.assertEqual(set(strings), keys, code)
                self.assertTrue(all(isinstance(v, str) and v.strip() for v in strings.values()), code)
        self.assertEqual(js_json(wizard, "LANGS"), [list(row) for row in core.LANGUAGES])

    def test_wizard_language_list_comes_from_core(self):
        """The browser selector must follow the same registry as CLI/site builds."""
        from unittest import mock
        choices = [("العربية", "العربية", "العربية", "Arabic"), ("English", "English", "الإنجليزية", "English")]
        with mock.patch.object(core, "LANGUAGES", choices):
            wizard = core.load_wizard()
        match = re.search(r"LANGS\s*=\s*", wizard)
        actual = json.JSONDecoder().raw_decode(wizard[match.end():])[0]
        self.assertEqual(actual, [list(row) for row in choices])

    def test_standalone_preserves_integrated_templates_and_catalog(self):
        """A distributed tool must contain the same reviewed UI and data as source."""
        import runpy
        tool = self.tmp / core.TOOL_NAME
        tool.write_text(core.single_source(), encoding="utf-8")
        built = runpy.run_path(str(tool))
        for name in ("LANGUAGES", "SKILLS", "SKILL_GROUPS", "PRESETS"):
            self.assertEqual(built[name], getattr(core, name), name)
        self.assertEqual(built["load_wizard"](), core.load_wizard())
        self.assertEqual(built["load_template"](), core.load_template())
        self.assertEqual((len(built["PRESETS"]), len(built["role_library"]()), len(built["SKILLS"]), len(built["SKILL_GROUPS"])), (80, 334, 130, 18))
        for i, language in enumerate(built["LANGUAGES"]):
            root = built["create_project"](self.tmp, "Locale %d" % i, "Integration verification", "Test Owner", "general", None, None, [], None, "ChatGPT", language[0])
            self.assertEqual(built["load_team"](root)["language"], language[0])
            self.assertEqual(built["check_project"](root), [], language[0])
            self.assertIn('var DEMO=0', (root / "Office" / core.OFFICE_FILE).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
