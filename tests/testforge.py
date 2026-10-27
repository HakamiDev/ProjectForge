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
        self.assertIn("العربية", core.lang_note(""))

    def test_single_file_build(self):
        src = core.single_source()
        self.assertIn('_TEMPLATE_Z = """', src)
        self.assertGreater(len(src), 100000)
        self.assertIn('_WIZARD_Z = """', src)
        compile(src, "single", "exec")


if __name__ == "__main__":
    unittest.main()
