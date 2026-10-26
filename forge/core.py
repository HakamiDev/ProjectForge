#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Forge 1: أداة بناء مشروع بفريق ذكاء اصطناعي وموقع إدارته.

بايثون 3.9 فما فوق، بلا أي مكتبة خارجية. تشغيلها: python3 -I "Project Forge 1.py" <أمر>

الأوامر:
  new        ينشئ مشروعًا كاملًا: المجلدات والقواعد واللوحة وملفات الأدوار والأوامر وموقع الإدارة.
  build      يعيد بناء موقع الإدارة من اللوحة (Office/Project Office.html).
  watch      يعيد البناء تلقائيًا كلما تغيّرت اللوحة أو الفريق أو سجل القرارات.
  rows       يعرض الصفوف الجاهزة لدور معيّن.
  add-row    يضيف صفًا إلى اللوحة بأمان (يحسب الرقم ويمنع التعارض).
  set-status يغيّر حالة صف. «معتمدة» و«ملغاة» تشترطان --owner-order.
  add-role   يضيف دورًا جديدًا ويحدّث القواعد والأوامر والموقع.
  decide     يسجّل قرارًا في سجل القرارات.
  report     تقرير أداء: نسبة التسليم وزمن الدورة ومرور الجودة والحمل والقرارات المتأخرة.
  export     يصدّر اللوحة والفريق والقرارات والمؤشرات إلى CSV جاهزة لـ Power BI وExcel.
  check      يفحص المشروع: التسمية والترقيم وسلامة اللوحة ومهلة القرارات ووجود رئيس ضمان الجودة.
  register   يسجّل المشروع في سجل مركز البوصلات (Registry.md).
  selftest   يختبر الأداة على مشروع مؤقت.

المشروع يحمل نسخة من الأداة في Tools/ فيكمل بناء نفسه منها.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import time
from pathlib import Path

VERSION = 1
TOOL_NAME = "Project Forge 1.py"
TZ = dt.timezone(dt.timedelta(hours=3))
MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
OFFICE_FILE = "Project Office.html"
STATUSES = ["محالة", "قيد التنفيذ", "مسلّمة", "بانتظار التدقيق", "أعيدت للتعديل", "بانتظار اعتماد", "معتمدة", "ملغاة", "مؤجلة"]
COLS = ["#", "من", "إلى", "المهمة", "المدخلات", "المخرج", "يبدأ بعد", "الموعد", "الحالة", "للتالي"]
TEAM_COLS = ["الدور", "الحالة", "آخر نشاط", "آخر تعميم مقروء", "ملاحظة"]
QA_NAME = "رئيس ضمان الجودة"
COMPASS = "البوصلة"
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif")

PRESETS = {
    "general": [
        ("رئيس المنتج", "المرجع والقرارات والخطة والأولويات", "المرجع، سجل القرارات، الخطة، معايير القبول، حراسة النطاق؛ يعدّل المرجع وحده", "Claude"),
        ("رئيس التنفيذ", "الإنتاج الفعلي", "إنتاج المخرجات الأساسية للمشروع وفق لوحة الصفوف", "Claude"),
        ("المدير الإبداعي", "الشكل والهوية والتجربة", "الأسلوب والهوية والتجربة والصياغة، والنقد البصري", "Claude"),
        (QA_NAME, "الاختبار المستقل والحكم", "الاختبار المستقل والحكم بيمر أو لا يمر على كل مخرج قبل أن يصل إلى صاحب المشروع", "Claude"),
        ("الرئيس التقني", "الأدوات والبنية والأتمتة", "الأدوات والبنية والأتمتة وموقع الإدارة", "Claude"),
    ],
    "software": [
        ("رئيس المنتج", "المرجع والقرارات والخطة", "المتطلبات والأولويات ومعايير القبول والمرجع", "Claude"),
        ("مهندس الواجهات", "الواجهة الأمامية", "بناء الواجهات والتفاعل والأداء", "Claude"),
        ("مهندس الخلفية", "الخادم والبيانات", "الخادم وقواعد البيانات والتكاملات", "Claude"),
        ("مصمم التجربة", "تجربة المستخدم والتصميم", "رحلة المستخدم والشاشات ودليل التصميم", "Claude"),
        (QA_NAME, "الاختبار المستقل والحكم", "الاختبار المستقل والحكم بيمر أو لا يمر على كل مخرج", "Claude"),
        ("رئيس العمليات والنشر", "النشر والمراقبة", "البناء والنشر والمراقبة والاستمرارية", "Claude"),
    ],
    "transformation": [
        ("رئيس التحول", "المرجع وخارطة الطريق والأولويات", "المرجع، وخارطة طريق التحول بالذكاء الاصطناعي، وحالات الاستخدام وأولوياتها، ومعايير القبول", "Claude"),
        ("محلل العمليات", "رسم العمليات وقياسها", "رسم العمليات الحالية والمستهدفة، وقياس الزمن والتكلفة والأخطاء قبل الأتمتة وبعدها", "Claude"),
        ("مهندس الأتمتة", "بناء الوكلاء والتدفقات", "تصميم وبناء الوكلاء وتدفقات الأتمتة وتكاملها مع الأنظمة المعتمدة", "Claude"),
        ("مسؤول البيانات والامتثال", "حوكمة البيانات والخصوصية", "تصنيف البيانات، وسياسة استعمال الأدوات الخارجية، والامتثال لمتطلبات الجهة", "Claude"),
        (QA_NAME, "الاختبار المستقل والحكم", "الاختبار المستقل والحكم بيمر أو لا يمر على كل وكيل وتدفق قبل أن يصل إلى صاحب المشروع", "Claude"),
        ("مدير التغيير والتبني", "التدريب والتبني والقياس", "خطة التبني، والتدريب، وقياس الاستعمال والأثر بعد الإطلاق", "Claude"),
    ],
    "operations": [
        ("رئيس العمليات", "المرجع والأولويات", "المرجع والإجراءات التشغيلية ومعايير القبول والأولويات", "Claude"),
        ("محلل الأداء", "المؤشرات والتقارير", "تعريف مؤشرات الأداء وقياسها وتقاريرها الدورية", "Claude"),
        ("مصمم الإجراءات", "تصميم العمليات", "رسم الإجراءات وتبسيطها وتوثيقها", "Claude"),
        ("مهندس الأتمتة", "الأتمتة والأدوات", "أتمتة العمل المتكرر بالأدوات المعتمدة", "Claude"),
        (QA_NAME, "الاختبار المستقل والحكم", "الاختبار المستقل والحكم بيمر أو لا يمر على كل مخرج", "Claude"),
    ],
    "data": [
        ("رئيس البيانات", "المرجع ونموذج البيانات", "المرجع، ونموذج البيانات، وتعريفات المؤشرات، ومعايير القبول", "Claude"),
        ("مهندس البيانات", "المصادر والتكامل", "جلب البيانات من مصادرها وتنظيفها وتكاملها", "Claude"),
        ("محلل ذكاء الأعمال", "اللوحات والتقارير", "بناء لوحات المؤشرات والتقارير وقياسات DAX", "Claude"),
        ("مسؤول جودة البيانات", "الصحة والاتساق", "فحص صحة البيانات واتساقها وتوثيق قواعدها", "Claude"),
        (QA_NAME, "الاختبار المستقل والحكم", "الاختبار المستقل والحكم بيمر أو لا يمر على كل لوحة وتقرير", "Claude"),
    ],
    "content": [
        ("رئيس التحرير", "المرجع والخطة التحريرية", "الخطة التحريرية والأولويات والمرجع ومعايير القبول", "Claude"),
        ("الكاتب الأول", "كتابة المحتوى", "كتابة المسودات والنصوص النهائية", "Claude"),
        ("الباحث", "البحث والمصادر", "جمع المصادر وتوثيقها والتحقق من الوقائع", "Claude"),
        ("المصمم البصري", "الصور والتصميم", "التصاميم والصور والهوية البصرية للمحتوى", "Claude"),
        (QA_NAME, "الاختبار المستقل والحكم", "المراجعة المستقلة والحكم بيمر أو لا يمر على كل مخرج", "Claude"),
        ("رئيس النمو والنشر", "النشر والقياس", "جدولة النشر والقنوات وقياس الأثر", "Claude"),
    ],
}

# ---------------------------------------------------------------- مساعدات


def now():
    return dt.datetime.now(TZ)


def fmt_date(d):
    return "%d %s %d" % (d.day, MONTHS[d.month - 1], d.year)


def fmt_dt(d):
    return "%s، %s" % (fmt_date(d), d.strftime("%H:%M"))


def fill(t, **kw):
    for k, v in kw.items():
        t = t.replace("{{" + k + "}}", str(v))
    return t


def clean_name(s):
    s = re.sub(r'[\\/:*?"<>|\x00-\x1f]', " ", s).replace("_", " ")
    return re.sub(r"\s+", " ", s).strip()


def norm(s):
    return re.sub(r"[\u064B-\u065F\u0640]", "", str(s or "")).strip()


def role_key(s):
    s = norm(s)
    s = re.sub(r"^\d+\.\s*", "", s)
    s = s.replace("«", "").replace("»", "").replace('"', "")
    return s.split(":")[0].strip()


def atomic_write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def write_new(path, text, report=None):
    """ينشئ الملف إن لم يوجد، ولا يكتب فوق موجود أبدًا."""
    path = Path(path)
    if path.exists():
        if report is not None:
            report.append(("تُرك", path))
        return False
    atomic_write(path, text)
    if report is not None:
        report.append(("أُنشئ", path))
    return True


def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def find_root(start=None):
    cands = []
    if start:
        cands.append(Path(start).resolve())
    cands.append(Path.cwd().resolve())
    cands.append(Path(__file__).resolve().parent)
    for c in cands:
        for p in [c] + list(c.parents):
            if (p / "Agents" / "Team.json").exists():
                return p
    die("لم أجد مشروعًا هنا (لا يوجد Agents/Team.json). شغّل الأمر من داخل مجلد المشروع أو مرّر --root.")


def load_team(root):
    return json.loads((root / "Agents" / "Team.json").read_text(encoding="utf-8"))


def save_team(root, team):
    atomic_write(root / "Agents" / "Team.json", json.dumps(team, ensure_ascii=False, indent=2) + "\n")


# ---------------------------------------------------------------- الجداول والأقسام


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    s = s.replace("\\|", "\x00")
    return [c.strip().replace("\x00", "|") for c in s.split("|")]


def esc_cell(v):
    return str(v).replace("|", "\\|").replace("\n", " ").strip() or "—"


def section_range(lines, n):
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"^##\s+%d\.\s" % n, ln):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"^##\s", lines[j]):
            end = j
            break
    return start, end


def parse_table(lines):
    rows, header = [], None
    for ln in lines:
        if not ln.strip().startswith("|"):
            continue
        cells = split_row(ln)
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        if header is None:
            header = cells
            continue
        rows.append(dict(zip(header, cells + [""] * (len(header) - len(cells)))))
    return rows


def parse_items(lines):
    items, cur = [], None
    for ln in lines:
        m = re.match(r"^(\d+)\.\s+(.*)$", ln)
        if m:
            cur = {"n": int(m.group(1)), "text": m.group(2).strip()}
            items.append(cur)
        elif cur is not None and ln[:1] in (" ", "\t") and ln.strip():
            cur["text"] += "\n" + ln.strip()
    return items


def read_board(root):
    text = (root / "Agents" / "Board.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    out = {"text": text, "lines": lines, "tasks": [], "decisions": [], "circulars": [], "team": []}
    r = section_range(lines, 1)
    if r:
        out["decisions"] = parse_items(lines[r[0] + 1:r[1]])
    r = section_range(lines, 2)
    if r:
        out["circulars"] = parse_items(lines[r[0] + 1:r[1]])
    r = section_range(lines, 3)
    if r:
        for d in parse_table(lines[r[0] + 1:r[1]]):
            num = re.sub(r"\D", "", d.get("#", ""))
            if num:
                out["tasks"].append({
                    "n": int(num), "from": d.get("من", ""), "to": d.get("إلى", ""), "task": d.get("المهمة", ""),
                    "inputs": d.get("المدخلات", ""), "output": d.get("المخرج", ""), "after": d.get("يبدأ بعد", ""),
                    "due": d.get("الموعد", ""), "status": d.get("الحالة", ""), "next": d.get("للتالي", "")})
    r = section_range(lines, 4)
    if r:
        out["team"] = parse_table(lines[r[0] + 1:r[1]])
    return out


def is_done(status):
    s = norm(status)
    return s.startswith("مسلم") or s.startswith("معتمد")


def ready_tasks(tasks, role):
    by_n = {t["n"]: t for t in tasks}
    res = []
    for t in tasks:
        if role_key(t["to"]) != role_key(role) or norm(t["status"]) != "محالة":
            continue
        deps = [int(x) for x in re.findall(r"\d+", t["after"] or "")]
        if all(d in by_n and is_done(by_n[d]["status"]) for d in deps):
            res.append(t)
    return res


def touch_updated(text, by):
    return re.sub(r"^\*\*آخر تحديث:\*\*.*$", "**آخر تحديث:** %s، %s" % (fmt_dt(now()), by), text, count=1, flags=re.M)


# ---------------------------------------------------------------- القوالب العربية

CLAUDE_T = """# تعليمات العمل في {{project}}

أنت تعمل على {{project}}: {{goal}}. صاحب المشروع: {{owner}}.

## 1. قبل أي عمل

1. اقرأ النسخة الحالية من الملفات من هذا المجلد، لا من ذاكرة المحادثة. أي تغيير تجده فيها يُعامل على أنه تغيير {{owner}}؛ احفظه وابنِ عليه ولا تلغه دون طلبه (`AGENTS.md`).
2. `{{project}} Project Reference.md` هو المرجع الوحيد المعتمد. اقرأ منه القسم الذي تحتاجه مهمتك، وكاملًا مرة واحدة في أول محادثة.
3. لتعرف صفوفك الجاهزة شغّل `python3 -I "Tools/{{tool}}" rows "اسمك"`، ثم اقرأ ملف دورك في `Agents/Roles/` والأقسام التي تسمّيها خانة المدخلات فقط.
4. لا تُعد أي بند من قائمة «المستبعد صراحة» في المرجع إلا بقرار مكتوب من {{owner}}.

## 2. نظام الفريق

ثلاثة ملفات فقط، ولا نسخ ولا لصق بين المحادثات:

| الملف | الغرض |
| --- | --- |
| هذا الملف | القواعد |
| `Agents/Board.md` | العمل كله: القرارات والتعميمات والمهام وحالة الفريق |
| `Agents/Roles/[الاسم].md` | أمر التكليف. يُقرأ مرة واحدة في أول محادثة |

<!-- team:start -->
{{team_table}}
<!-- team:end -->

**السلاسل:** كل مخرج يمر على {{qa}} قبل أن يصل إلى {{owner}}. ولا يصل مخرج إلى «بانتظار اعتماد {{owner}}» إلا بحكم {{qa}}.

**جولة الموظف** عند أي رسالة من {{owner}}، ومنها «تابع»:
1. اقرأ اللوحة وحدها. لا تُعد قراءة ملف دورك ولا المرجع إلا إن تغيّر.
2. نفّذ مهامك الجاهزة بترتيب أرقامها. المهمة جاهزة إن كانت باسمك وحالتها «محالة» وما في «يبدأ بعد» مسلَّم أو معتمد.
3. عند البدء اجعل حالتها «قيد التنفيذ». وعند التسليم احفظ المخرج في مساره، واجعل حالتها «مسلّمة»، أو «بانتظار التدقيق» إن كان {{qa}} هو التالي، واكتب في «للتالي» ما يحتاجه من يليك.
4. تحتاج شيئًا من زميل؟ أضف صفًا جديدًا (`add-row`) باسمك في «من» واسمه في «إلى». وما يلزم المرجع صفٌّ إلى رئيس المنتج. وما يحتاج قرار {{owner}} بندٌ في القسم 1 من اللوحة.
5. حدّث صفك في «حالة الفريق».
6. اقرأ من ملفات المدخلات ما تحتاجه المهمة فقط، ولا تنسخ محتواها في ردك.
7. ردك على {{owner}} ثلاثة أسطر: ما نفّذت، وما ينتظر غيرك، وما تحتاجه منه. وإن لم تجد مهمة جاهزة فاكتب «لا مهام جاهزة».

## 3. قواعد اللوحة

1. أعد قراءة اللوحة قبل الكتابة فيها مباشرة، وعدّل صفوفك فقط، ولا تعِد كتابة الملف كاملًا. استعمل `add-row` و`set-status`.
2. الحالات: محالة، قيد التنفيذ، مسلّمة، بانتظار التدقيق، أعيدت للتعديل، بانتظار اعتماد {{owner}}، معتمدة، ملغاة، مؤجلة. «معتمدة» و«ملغاة» بأمر {{owner}} الصريح فقط. ولا تُستعمل صيغ مركّبة؛ تُكتب الحالة المعتمدة والقيد في «للتالي».
3. سقف الصفوف المفتوحة لكل موظف خمسة. واللوحة لا تتجاوز صفحتين؛ تنقل البوصلة المسلَّم إلى `Archive/`.
4. المهمة في اللوحة تفويض من {{owner}} ضمن نطاقها داخل المجلد. النشر والدفع والتواصل مع أي جهة خارجية بأمر {{owner}} المباشر فقط.
5. طلب {{owner}} المباشر من موظف نافذ. نبّهه في سطر قبل التنفيذ إن خالف المرجع أو مسّ مهمة مفتوحة أو اختصاص زميل، ثم سجّله صفًا في اللوحة باسمك.
6. ما يخص بنية الفريق وأوامره يُحال إلى البوصلة. ما يخص المرجع يُحال إلى رئيس المنتج.
7. موظف جديد لا يرد اسمه في الجدول: يُضاف بـ`add-role`، ولا يعمل قبل ذلك.
8. إن لم يكن المجلد موصولًا بالمحادثة فقل ذلك صراحة، ولا تدّعِ أنك حفظت ملفًا.

## 4. القرارات

1. تحسم البوصلة القرارات بتوصيتها وتخبر {{owner}}، وتجمعها في **بطاقة قرار واحدة كل مساء**.
2. ما لم يجب عنه {{owner}} خلال **48 ساعة** يؤخذ بالتوصية، ويمضي الفريق بها وينقض {{owner}} ما لا يعجبه بعد رؤيته. **لا تسري هذه القاعدة** على ما لا رجعة فيه، ولا على تغيير جوهري في هوية المشروع، ولا على أي مصروف جديد لم يفوَّض به صراحة.
3. يُوسم كل قرار **قابلًا للتراجع** أو **غير قابل للتراجع**.
4. سقف القرارات المفتوحة **خمسة**.
5. الخيارات التصميمية تُعرض **صورًا لا وصفًا**.
6. يُحفظ السجل في `Docs/Decision Log.md` بأمر `decide`.

## 5. الاستمرارية بين المحادثات والمنصات

1. الموظف الذي له أكثر من محادثة، في أكثر من منصة، يكمل من أي منها، وأساس ذلك صلاحيته على هذا المجلد وحدها: اللوحة وملف دوره والمخرجات. لا اعتماد على ذاكرة محادثة.
2. عند كل بداية: اقرأ اللوحة وآخر تعميمين وملف دورك، ثم «للتالي» في صفك. قبل أي توقف: اكتب في «للتالي» ما أنجزت وما بقي.
3. «قيد التنفيذ» تحجز الصف، فلا تنفّذ محادثتان من الموظف نفسه الصف نفسه.
4. **الإغلاق والاستئناف:** المحادثة التي طالت تُغلق بـ«أمر الإغلاق» فيكتب الموظف ملف تسليم في `Agents/Handoffs/` ويرد «آمن للإغلاق»، ثم تُفتح بديلة بـ«أمر الاستئناف». الأمران في `Agents/Handoff Commands.md`.
5. ما لا تقدر عليه منصة يبقى للمنصة القادرة ولا يُدّعى تنفيذه.

## 6. قواعد ثابتة

1. أسماء الملفات والمجلدات: مسافة بين الكلمات، ولا شرطة سفلية أبدًا. والترقيم يبدأ من 1.
2. اللغة: عربية فصحى قوية وواضحة في كل نص يقرؤه العميل أو الجمهور. والكتابة لـ{{owner}} مباشرة ومختصرة ورسمية، تبدأ بالخلاصة، دون حشو.
3. لا تحذف ملفًا. انقل القديم إلى `Archive/`، ولا تكتب فوق ملف يخص موظفًا آخر دون نسخه أولًا.
4. لا نقل لملف مربوط قبل أن يعرف الناقل كل ما يرتبط به ويحدّث كل رابط ومسار في الجولة نفسها. عند الشك لا ينقل.
5. كل ما يطلب {{owner}} نسخه (أمر أو كود أو مسار أو نص) يُكتب في صندوق نسخ مستقل في الرد.
6. المال والامتثال والتراخيص مسؤولية {{owner}} وحده، ولا تُكتب فيها مهام.
7. المخرجات في `Outputs/` ما لم تحدد المهمة مسارًا آخر، ويُحدَّث جدول Data المعني بعد أي عمل.
8. سياسة البيانات في `Docs/Data Policy.md` ملزمة: لا بيانات شخصية أو سرية في أي أداة غير معتمدة.
"""

AGENTS_T = """# قاعدة التغييرات في {{project}}

هذا المجلد هو مجلد العمل المعتمد. أي تغيير فيه يُعامل على أنه تغيير {{owner}}، سواء أجراه بنفسه أو أجراه مساعد بطلبه.

1. اقرأ الملف الحالي قبل أي تعديل، لا نسخة سابقة في ذاكرتك.
2. احفظ التغيير وابنِ عليه، ولا تلغه أو تعد الملف إلى حاله السابقة دون طلب {{owner}}.
3. القواعد الكاملة في `CLAUDE.md`، والعمل في `Agents/Board.md`.
"""

README_T = """# {{project}}

{{goal}}

**صاحب المشروع:** {{owner}} · **أُنشئ:** {{date}} · **الأداة:** {{tool}}

## خريطة المجلد

| المسار | الغرض |
| --- | --- |
| `CLAUDE.md` | القواعد الثابتة وجدول الفريق |
| `AGENTS.md` | قاعدة التغييرات |
| `{{project}} Project Reference.md` | المرجع الوحيد المعتمد |
| `Agents/Board.md` | اللوحة: القرارات والتعميمات والمهام وحالة الفريق |
| `Agents/Roles/` | أمر تكليف كل موظف |
| `Agents/Team.json` | قائمة الفريق للآلة (تولّد منها الجداول والموقع) |
| `Agents/Start Commands.md` | أوامر بدء المحادثات |
| `Agents/Handoff Commands.md` | أمرا الإغلاق والاستئناف |
| `Agents/Handoffs/` | ملفات التسليم عند إغلاق المحادثات |
| `Agents/Row Drafts/` | مسودات الصفوف عند تعارض الكتابة |
| `Docs/Decision Log.md` | سجل القرارات |
| `Docs/Data Policy.md` | سياسة البيانات والأدوات المعتمدة |
| `Docs/Reports/` | تقارير الأداء الدورية (`report`) |
| `Agents/Audit Log.md` | سجل التدقيق: كل كتابة في اللوحة |
| `Data/Status History.csv` | تاريخ تغيّر الحالات (لحساب زمن الدورة) |
| `Outputs/` | المخرجات |
| `Data/` | الجداول والبيانات |
| `Archive/` | كل قديم. لا يُحذف شيء |
| `Office/{{office}}` | موقع الإدارة (يُولَّد من اللوحة) |
| `Tools/` | الأداة نفسها، تبني المشروع وتضيف إليه |

## التشغيل اليومي

1. افتح `Office/{{office}}` في المتصفح. لتحديثه تلقائيًا شغّل `python3 -I "Tools/{{tool}}" watch` أو انقر `Tools/Start Office.command` على الماك.
2. كلّم البوصلة وحدها في البداية، فهي بابك الأول وتوزّع العمل.
3. في أي محادثة جديدة: انسخ أمر البدء من صفحة «الأوامر» في الموقع.

## أوامر الأداة

```
python3 -I "Tools/{{tool}}" rows "رئيس المنتج"
python3 -I "Tools/{{tool}}" add-row --from "رئيس المنتج" --to "رئيس التنفيذ" --task "..." --inputs "..." --output "..."
python3 -I "Tools/{{tool}}" set-status 3 "مسلّمة" --note "..."
python3 -I "Tools/{{tool}}" add-role "اسم الدور" --title "المسمى" --scope "الاختصاص"
python3 -I "Tools/{{tool}}" decide "نص القرار" --tag "قابل للتراجع"
python3 -I "Tools/{{tool}}" report
python3 -I "Tools/{{tool}}" export
python3 -I "Tools/{{tool}}" build
python3 -I "Tools/{{tool}}" check
```
"""

REF_T = """# {{project}}: المرجع الشامل للمشروع

**آخر تحديث:** {{date}}
**المالك:** {{owner}}

هذا الملف هو المرجع الوحيد المعتمد. كل قرار يُقاس عليه، ويُحدَّث مع كل قرار أو إنجاز. عند التعارض مع أي وثيقة أقدم يُعتمد ما هنا. يعدّله رئيس المنتج وحده.

## 1. التعريف

{{goal}}

## 2. الهدف الحالي

(اكتب الهدف الواحد الذي يخدمه كل صف الآن)

## 3. النطاق

1. ما هو داخل النطاق:
2. ما هو خارجه:

## 4. المستبعد صراحة

لا يعود أي بند هنا إلا بقرار مكتوب من {{owner}}:

1. (لا شيء بعد)

## 5. معيار النجاح

| المرحلة | المؤشر |
| --- | --- |
| (المرحلة 1) | (كيف نعرف أنها نجحت) |

## 6. المعالم والجدول

| # | المعلم | يكتمل عند | التقدير |
| --- | --- | --- | --- |
| 1 | (المعلم الأول) | | |

## 7. المخاطر

| الخطر | المعالجة |
| --- | --- |
| (أكبر خطر) | |

## 8. سجل التحديثات

| التاريخ | التحديث |
| --- | --- |
| {{date}} | إنشاء المرجع بأداة {{tool}} |
"""

BOARD_T = """# لوحة الفريق

**آخر تحديث:** {{stamp}}، {{by}}
**النظام:** أُنشئ بأداة {{tool}} في {{date}}. القواعد في `CLAUDE.md`.

الملف المشترك الوحيد للعمل. شغّل `python3 -I "Tools/{{tool}}" rows "اسمك"` من جذر المشروع لتعرف صفوفك، وعدّل صفوفك فقط، وأعد قراءة اللوحة قبل الكتابة مباشرة.

## 1. ما ينتظر قرار {{owner}}

(لا شيء)

## 2. تعميمات

اقرأها قبل مهامك، واكتب رقم آخر تعميم قرأته في صفك في القسم 4.

(لا تعميمات)

## 3. المهام المفتوحة

{{tasks}}

## 4. حالة الفريق

{{team}}
"""

DATA_POLICY_T = """# سياسة البيانات والأدوات في {{project}}

ملزمة لكل موظف، وتُراجع قبل أي مهمة تمس بيانات.

## 1. تصنيف البيانات

| المستوى | أمثلة | أين يجوز معالجتها |
| --- | --- | --- |
| عام | نصوص منشورة، وقوالب، وأمثلة مصطنعة | أي أداة |
| داخلي | إجراءات العمل، والمؤشرات المجمّعة بلا أسماء | الأدوات المعتمدة من {{owner}} فقط |
| شخصي أو سري | أسماء الأفراد وبياناتهم، والعقود، وأي بيانات مشاركين | لا تخرج من أنظمة الجهة أبدًا، ولا تُلصق في أي محادثة |

## 2. القواعد

1. لا تُدخل بيانات شخصية أو سرية في أي أداة خارجية. استبدلها ببيانات مصطنعة أو مُقنَّعة، وسجّل ذلك في «للتالي».
2. الأدوات المعتمدة هي ما يحدده {{owner}} في هذا الملف. وما ليس فيه غير معتمد.
3. كل مخرج يذكر مصدر بياناته ونطاقها وتاريخها.
4. القياس قبل الأتمتة وبعدها: الزمن، والتكرار، والأخطاء، والتكلفة. تُسجَّل الأرقام في `Data/` ويُبنى عليها تقرير `report`.
5. ما يمس الامتثال أو الترخيص أو المال فمسؤولية {{owner}} وحده، ولا تُكتب فيه مهام.

## 3. الأدوات المعتمدة

| الأداة | الاستعمال المسموح | اعتمدها |
| --- | --- | --- |
| (أضف هنا) | | {{owner}} |
"""

AUDIT_T = """# سجل التدقيق

كل كتابة في اللوحة أو سجل القرارات تُسجَّل هنا تلقائيًا. لا يُعدَّل يدويًا.

| التاريخ | من | الإجراء |
| --- | --- | --- |
"""

HISTORY_HEAD = "n,status,by,at\n"

DECISION_LOG_T = """# سجل القرارات

القرارات بأرقام تبدأ من 1. يضيفها الأمر `decide`. كل قرار يُوسم قابلًا للتراجع أو غير قابل.

| # | التاريخ | القرار | الوسم | المصدر |
| --- | --- | --- | --- | --- |
"""

HANDOFF_T = """# أمرا الإغلاق والاستئناف

## أمر الإغلاق

```
أمر الإغلاق: اكتب ملف تسليم في Agents/Handoffs/[اسم دورك] [رقم].md فيه: ما أنجزت، وما بقي، وأين مخرجاتك، وأي قيد أو قرار معلق، وما يلزم من يخلفك أن يعرفه. حدّث «للتالي» في صفوفك. ثم ردّ بكلمة واحدة: «آمن للإغلاق».
```

## أمر الاستئناف

```
أمر الاستئناف: أنت [اسم المحادثة] في محادثة بديلة. اقرأ Agents/Roles/[اسم دورك].md، ثم أحدث ملف تسليم لك في Agents/Handoffs/، ثم صفوفك في اللوحة فقط، وتابع من حيث توقف سلفك.
```
"""

ROLE_T = """# {{name}}: أمر التكليف

اسم المحادثة: «{{chat}}». المنصة: {{platform}}. المسمى الوظيفي: {{title}}.

> **نفاذ:** `CLAUDE.md` يعلو على ما يخالفه هنا. جدول الفريق الحالي فيه.

## 1. من أنت

أنت «{{name}}» في {{project}}: {{goal}}. تعمل مع {{owner}} ضمن فريق في ملفات هذا المجلد، وتكمل عملك من أي محادثة لأن أساس عملك الملفات لا الذاكرة.

## 2. اختصاصك

{{scope}}

## 3. ما لا تفعله

1. لا تنفّذ عمل زميل ولا تكتب بدلًا منه؛ أحِل إليه صفًا.
2. لا تنشر ولا تدفع ولا تتواصل مع جهة خارجية دون أمر {{owner}} المباشر.
3. لا تعدّل المرجع (رئيس المنتج وحده)، ولا تعد بندًا من «المستبعد».
4. لا تحذف ملفًا؛ انقله إلى `Archive/`.

## 4. كيف تعمل

1. في أول محادثة اقرأ: `CLAUDE.md`، ثم هذا الملف، ثم اللوحة.
2. في كل جولة: اللوحة وحدها، ثم صفوفك الجاهزة (`rows "{{name}}"`).
3. مخرجاتك في `Outputs/` أو المسار الذي يحدده الصف.
4. قبل أي توقف اكتب في «للتالي» ما أنجزت وما بقي.

## 5. أسلوب الرد

عربية فصحى موجزة، في ثلاثة أسطر: ما نفّذت، وما ينتظر غيرك، وما تحتاجه من {{owner}}. الترقيم يبدأ من 1، وأسماء الملفات بمسافات دون شرطة سفلية.

أكّد اسمك ومسماك في سطر واحد.
"""

QA_EXTRA = """
## 6. حكمك

1. تختبر باستقلال؛ لا تراجع عمل نفسك، ولا يراجع غيرك عملك.
2. حكمك «يمر» أو «لا يمر» أو «يمر بشروط»، بأسبابه وأدلته في ملف حكم في `Docs/QA/`، وسطر في «للتالي».
3. لا يصل أي مخرج إلى «بانتظار اعتماد {{owner}}» إلا بحكمك.
4. ترصد انطباع المتلقي الأول (الضيف أو العميل أو القارئ) رأيًا مستقلًا بلا حلول.
"""

COMPASS_T = """# البوصلة: أمر التكليف

اسم المحادثة: «البوصلة: التوجيه العام». المسمى الوظيفي: مدير مكتب {{owner}} (Chief of Staff). المنصة: Claude.

> **نفاذ:** `CLAUDE.md` يعلو على ما يخالفه هنا.

## 1. من أنت

أنت «البوصلة» في {{project}}: {{goal}}. مكتب القيادة، وبابُ {{owner}} الأول. يخاطبك أنت، وأنت توجّه العمل إلى الموظفين وتجمعه منهم. تضم دور المعماري: تصميم الفريق وصيانة أوامره وتشخيص الأداء.

## 2. دورك

1. **الاستقبال:** تستقبل طلب {{owner}}، وتفهمه في سطر، وتحدد المختص، وتكتب له صفًا مكتملًا المدخلات والمخرج (`add-row`)، وتخبر {{owner}} برقم الصف ومن يتابع معه. لا تنفّذ عمل غيرك إلا بأمره المباشر.
2. **المتابعة:** تتابع التسليم وتحرك العالق، وتنقل المسلَّم إلى `Archive/` لتبقى اللوحة في صفحتين.
3. **القرارات:** تحسم بتوصيتها وتخبر {{owner}}، وتجمع المعلق في بطاقة مسائية واحدة، وتسجّل كل قرار (`decide`) وتوسمه بقابلية التراجع. القواعد في `CLAUDE.md` القسم 4.
4. **الفريق:** تضيف الأدوار (`add-role`) وتدمج ما لا عمل له، وتصون أوامر التكليف. لا دور جديد إلا لعمل يتكرر.
5. **المكتب:** تنفّذ «حفظ التغييرات» التي ينسخها {{owner}} من موقع الإدارة، وتسجّلها في `Office/Office Changes Log.md`.
6. **المشاريع الأخرى:** إن وُجد مركز بوصلات (`Compass Network/`) فسجّل مشروعك فيه (`register`) وتعاون بالطلب والرد لا بالأمر.

## 3. أسلوب الرد

عربية فصحى موجزة. في كل رد: ما نفّذت، ومن عنده مهمة جاهزة، وما تحتاجه من {{owner}}. وإن طلبت من {{owner}} تشغيل أكثر من محادثة فاذكر صراحة: معًا أم واحدة بعد الأخرى، ومن ينتظر من.
"""

# ---------------------------------------------------------------- بناء الفريق والملفات


def make_roster(preset_roles, project, goal, owner):
    roster = [{
        "id": "compass", "n": 0, "name": COMPASS, "title": "مدير المكتب", "scope": "التوجيه العام: تستقبل الطلبات وتوزعها وتتابعها وتحسم القرارات بتوصيتها",
        "platform": "Claude", "chat": "البوصلة: التوجيه العام"}]
    for i, (name, title, scope, platform) in enumerate(preset_roles, 1):
        name = clean_name(name)
        roster.append({"id": "r%d" % i, "n": i, "name": name, "title": title, "scope": scope, "platform": platform,
                       "chat": "%d. %s: %s" % (i, name, title)})
    return roster


def start_cmd(r):
    return "أنت «%s». اقرأ Agents/Roles/%s.md ثم تابع." % (r["chat"], r["name"])


def resume_cmd(r):
    return ("أمر الاستئناف: أنت «%s» في محادثة بديلة. اقرأ Agents/Roles/%s.md ثم أحدث ملف تسليم لك في Agents/Handoffs/ "
            "ثم صفوفك في اللوحة فقط، وتابع من حيث توقف سلفك." % (r["chat"], r["name"]))


def team_table(roster):
    head = "| # | اسم المحادثة | الاختصاص | المنصة | الحالة |\n| --- | --- | --- | --- | --- |\n"
    rows = ""
    for r in roster:
        rows += "| %s | %s | %s | %s | فعّال |\n" % ("—" if not r["n"] else r["n"], esc_cell(r["chat"]), esc_cell(r["scope"]), r["platform"])
    return head + rows.rstrip("\n")


def md_table(header, rows):
    out = "| " + " | ".join(header) + " |\n| " + " | ".join(["---"] * len(header)) + " |\n"
    for r in rows:
        out += "| " + " | ".join(esc_cell(c) for c in r) + " |\n"
    return out.rstrip("\n")


def role_doc(team, r):
    t = fill(COMPASS_T if r["id"] == "compass" else ROLE_T, name=r["name"], chat=r["chat"], platform=r["platform"], title=r["title"],
             scope=r["scope"], project=team["project"], goal=team["goal"], owner=team["owner"])
    if r["name"] == QA_NAME:
        t += fill(QA_EXTRA, owner=team["owner"])
    return t


def start_commands_md(team):
    out = "# أوامر بدء المحادثات\n\nانسخ الأمر إلى محادثة جديدة للموظف. الاستئناف بعد الإغلاق في `Agents/Handoff Commands.md`.\n\n"
    for r in team["roster"]:
        out += "## %s\n\n```\n%s\n```\n\n" % (r["chat"], start_cmd(r))
    out += "## للتشغيل اليومي\n\nفي أي محادثة قائمة اكتب: «تابع».\n"
    return out


def board_text(team, tasks=None, by=None):
    stamp = fmt_dt(now())
    owner = team["owner"]
    if tasks is None:
        tasks = [[1, owner, COMPASS, "تهيئة المشروع: اقرأ المرجع واملأ الهدف والنطاق والمستبعد ومعيار النجاح بالتشاور مع %s، ثم وزّع أول دفعة صفوف على الفريق" % owner,
                  "`%s Project Reference.md`, `CLAUDE.md`" % team["project"], "`%s Project Reference.md` محدَّثًا" % team["project"], "—", "—", "محالة", "—"]]
    team_rows = [[r["name"], "فعّال", "—", "0", "—"] for r in team["roster"]]
    return fill(BOARD_T, stamp=stamp, by=by or COMPASS, tool=TOOL_NAME, date=fmt_date(now()), owner=owner,
                tasks=md_table(COLS, tasks), team=md_table(TEAM_COLS, team_rows)) + "\n"


def command_script(tool_rel):
    return ('#!/bin/bash\n# يفتح موقع الإدارة ويعيد بناءه تلقائيًا كلما تغيّرت اللوحة.\ncd "$(dirname "$0")/.." || exit 1\n'
            'python3 -I "Tools/%s" build --open\nexec python3 -I "Tools/%s" watch\n' % (tool_rel, tool_rel))


def create_project(parent, name, goal, owner, preset, roles, accent, report):
    project = clean_name(name)
    root = Path(parent).resolve() / project
    if (root / "Agents" / "Team.json").exists():
        die("المشروع موجود أصلًا في: %s" % root)
    for d in ["Agents/Roles", "Agents/Handoffs", "Agents/Row Drafts", "Docs/QA", "Docs/Reports", "Outputs", "Data", "Archive", "Office", "Tools"]:
        (root / d).mkdir(parents=True, exist_ok=True)
    preset_roles = roles if roles else PRESETS[preset]
    roster = make_roster(preset_roles, project, goal, owner)
    team = {"version": VERSION, "project": project, "goal": goal, "owner": owner, "accent": accent, "created": fmt_date(now()), "roster": roster}
    save_team(root, team)
    report.append(("أُنشئ", root / "Agents" / "Team.json"))
    qa = QA_NAME
    write_new(root / "CLAUDE.md", fill(CLAUDE_T, project=project, goal=goal, owner=owner, tool=TOOL_NAME, qa=qa, team_table=team_table(roster)), report)
    write_new(root / "AGENTS.md", fill(AGENTS_T, project=project, owner=owner), report)
    write_new(root / "Read Me.md", fill(README_T, project=project, goal=goal, owner=owner, date=fmt_date(now()), tool=TOOL_NAME, office=OFFICE_FILE), report)
    write_new(root / ("%s Project Reference.md" % project), fill(REF_T, project=project, goal=goal, owner=owner, date=fmt_date(now()), tool=TOOL_NAME), report)
    write_new(root / "Agents" / "Board.md", board_text(team), report)
    write_new(root / "Agents" / "Start Commands.md", start_commands_md(team), report)
    write_new(root / "Agents" / "Handoff Commands.md", HANDOFF_T, report)
    write_new(root / "Docs" / "Decision Log.md", DECISION_LOG_T, report)
    write_new(root / "Docs" / "Data Policy.md", fill(DATA_POLICY_T, project=project, owner=owner), report)
    write_new(root / "Agents" / "Audit Log.md", AUDIT_T, report)
    write_new(root / "Data" / "Status History.csv", HISTORY_HEAD + ",".join(csv_cell(x) for x in (1, "محالة", owner, now().isoformat(timespec="minutes"))) + "\n", report)
    write_new(root / "Office" / "Office Changes Log.md", "# سجل تغييرات المكتب\n\nتسجّل البوصلة هنا كل «حفظ تغييرات» ينسخه %s من موقع الإدارة، بتاريخه ورقمه.\n" % owner, report)
    for r in roster:
        write_new(root / "Agents" / "Roles" / ("%s.md" % r["name"]), role_doc(team, r), report)
    # الأداة نفسها
    dst = root / "Tools" / TOOL_NAME
    if Path(__file__).resolve() != dst.resolve():
        atomic_write(dst, single_source())
        report.append(("أُنشئ", dst))
    cmd = root / "Tools" / "Start Office.command"
    if write_new(cmd, command_script(TOOL_NAME), report):
        cmd.chmod(cmd.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    build_site(root, report)
    return root


# ---------------------------------------------------------------- موقع الإدارة

# ---------------------------------------------------------------- موقع الإدارة
# القالب شيفرة موقع الإدارة الأصلي حرفيًا (التصميم والإعدادات والحركة)، وتُحقن فيه بيانات المشروع.
_TEMPLATE_Z = None  # تملؤه tools/build-single.py في نسخة الملف الواحد


def load_template():
    p = Path(__file__).resolve().parent / "templates" / "office.html"
    if p.is_file():
        return p.read_text(encoding="utf-8")
    if _TEMPLATE_Z:
        import base64
        import zlib
        return zlib.decompress(base64.b64decode(_TEMPLATE_Z)).decode("utf-8")
    die("قالب الموقع غير موجود")


def single_source():
    """نص الأداة كملف واحد مكتفٍ بنفسه (القالب مضغوط بداخله)."""
    src = Path(__file__).resolve().read_text(encoding="utf-8")
    if _TEMPLATE_Z:
        return src
    marker = "_TEMPLATE_Z = None" + "  # تملؤه tools/build-single.py في نسخة الملف الواحد"
    if marker not in src:
        return src
    import base64
    import textwrap
    import zlib
    z = base64.b64encode(zlib.compress(load_template().encode("utf-8"), 9)).decode("ascii")
    return src.replace(marker, '_TEMPLATE_Z = """\n%s\n"""' % "\n".join(textwrap.wrap(z, 110)), 1)


CLOSE_T = ("سأغلق هذه المحادثة وأفتح بدلها محادثة جديدة لك تكمل العمل نفسه. المحادثة الجديدة لن ترى شيئًا من هنا؛ مرجعها المجلد وحده، "
           "فكل ما لا تكتبه الآن في المجلد يضيع. نفّذ بالترتيب دون أن تسألني:\n\n"
           "1. أوقف أي عمل جارٍ عند أقرب نقطة سليمة، واحفظ كل مخرج ناقص في مساره باسم يدل على أنه مسودة. لا يبقى شيء في المحادثة وحدها.\n"
           "2. اكتب ملف التسليم `Agents/Handoffs/[اسم دورك] [رقم].md`، وفيه: ما أنجزته بمسار كل ملف، والعمل الجاري (رقم الصف والخطوة التالية بالضبط)، "
           "وما قاله صاحب المشروع في هذه المحادثة ولم يُكتب بعد، وما جرّبته ففشل ولماذا، والأسئلة المفتوحة، وما يجب أن تقرأه المحادثة الجديدة أولًا.\n"
           "3. ما كان قاعدة دائمة فاكتبه صفًا إلى البوصلة، وما يحتاج قرار صاحب المشروع فسطرًا في القسم 1 من اللوحة.\n"
           "4. حدّث «للتالي» في كل صف مفتوح باسمك، وحدّث صفك في «حالة الفريق».\n"
           "5. تحقق بقراءة الملفات من القرص أن كل ما سبق محفوظ فعلًا.\n"
           "6. ردّك سطران: مسار ملف التسليم، ثم «آمن للإغلاق» أو ما يمنعه. وإن لم يكن المجلد موصولًا فاكتب «غير آمن للإغلاق: المجلد غير موصول».")
RESUME_T = ("أنت «[اسم المحادثة كاملًا كما في جدول الفريق]»، تستأنف عمل محادثة سابقة لك أُغلقت. لا ترى تلك المحادثة؛ مرجعك المجلد وحده. نفّذ بالترتيب دون أن تسألني:\n\n"
            "1. اقرأ `CLAUDE.md`.\n"
            "2. اقرأ `Agents/Roles/[اسم دورك].md`، وثوابته نافذة طوال المحادثة.\n"
            "3. اقرأ أحدث ملف لك في `Agents/Handoffs/` كاملًا، ثم ما يسمّيه فقط.\n"
            "4. اقرأ صفوفك في `Agents/Board.md` و«للتالي» فيها، وآخر تعميمين في القسم 2.\n"
            "5. إن تعارض ملف التسليم مع اللوحة فاللوحة أحدث وهي النافذة، ونبّهني في سطر.\n"
            "6. أكمل العمل الجاري من «الخطوة التالية» دون إعادة ما أُنجز، ثم بقية صفوفك الجاهزة بترتيب أرقامها.\n"
            "7. إن لم يكن المجلد موصولًا فقل ذلك في سطر، ولا تدّعِ أنك قرأت شيئًا.\n\n"
            "ردّك: سطر يؤكد من أين تستأنف، ثم ثلاثة أسطر: ما نفّذت، وما ينتظر غيرك، وما تحتاجه مني.")

ICONS = {
 "orn": "<path d=\"M12 3l2.2 4.8L19 6l-1.8 4.8L22 12l-4.8 1.2L19 18l-4.8-1.8L12 21l-2.2-4.8L5 18l1.8-4.8L2 12l4.8-1.2L5 6l4.8 1.8z\"/><circle cx=\"12\" cy=\"12\" r=\"2\"/>",
 "heart": "<path d=\"M12 20s-7-4.5-7-10a4 4 0 017-2.5A4 4 0 0119 10c0 5.5-7 10-7 10z\"/>",
 "build": "<path d=\"M3 21h18M5 21V9l7-5 7 5v12M9 21v-6h6v6M9 11h.01M15 11h.01\"/>",
 "clap": "<rect x=\"3\" y=\"9\" width=\"18\" height=\"11\" rx=\"2\"/><path d=\"M3 9l2.5-5 4 1.5L7 9M11 5.5l4 1.5-2 3M16 7l4 1-1.5 1\"/>",
 "box": "<path d=\"M12 3l8 4v10l-8 4-8-4V7z\"/><path d=\"M4 7l8 4 8-4M12 11v10\"/>",
 "scene": "<path d=\"M3 19h18\"/><path d=\"M4 19l5-9 4 6 3-4 4 7\"/><circle cx=\"17\" cy=\"6\" r=\"1.8\"/>",
 "window": "<rect x=\"3\" y=\"4\" width=\"18\" height=\"16\" rx=\"2\"/><path d=\"M3 9h18M8 13h8M8 16h5\"/>",
 "nib": "<path d=\"M12 3l5 8-5 10-5-10z\"/><circle cx=\"12\" cy=\"11\" r=\"1.3\"/><path d=\"M12 12.3V21\"/>",
 "camera": "<path d=\"M4 8h3l2-3h6l2 3h3v11H4z\"/><circle cx=\"12\" cy=\"13\" r=\"3.5\"/>",
 "moon": "<path d=\"M20 14.5A8 8 0 019.5 4 8 8 0 1020 14.5z\"/><path d=\"M17 4v3M15.5 5.5h3\"/>",
 "compass": "<circle cx=\"12\" cy=\"12\" r=\"9\"/><path d=\"M15.5 8.5l-2 5-5 2 2-5z\"/>",
 "motion": "<path d=\"M3 17c3 0 3-10 6-10s3 10 6 10 3-6 6-6\"/><circle cx=\"20\" cy=\"11\" r=\"1.2\"/>",
 "mega": "<path d=\"M4 10v4h3l7 4V6L7 10z\"/><path d=\"M17 9a4 4 0 010 6\"/>",
 "star": "<path d=\"M12 3l2.6 5.6 6.1.8-4.5 4.2 1.1 6.1L12 16.8 6.7 19.7l1.1-6.1L3.3 9.4l6.1-.8z\"/>",
 "cube": "<path d=\"M12 2l9 5v10l-9 5-9-5V7z\"/><path d=\"M3 7l9 5 9-5M12 12v10\"/><path d=\"M7.5 4.5l9 5\" opacity=\".5\"/>",
 "search": "<circle cx=\"11\" cy=\"11\" r=\"6.5\"/><path d=\"M16 16l5 5\"/>",
 "layers": "<path d=\"M12 3l9 5-9 5-9-5z\"/><path d=\"M3 13l9 5 9-5M3 17.5l9 5 9-5\"/>",
 "shield": "<path d=\"M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z\"/><path d=\"M9 12l2 2 4-4\"/>",
 "eye": "<path d=\"M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z\"/><circle cx=\"12\" cy=\"12\" r=\"3\"/>",
 "code": "<path d=\"M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 6l-3 12\"/>",
 "clipboard": "<rect x=\"6\" y=\"4\" width=\"12\" height=\"17\" rx=\"2\"/><path d=\"M9 4h6v3H9zM9 13l2 2 4-4\"/>",
 "scissors": "<circle cx=\"6\" cy=\"7\" r=\"2.5\"/><circle cx=\"6\" cy=\"17\" r=\"2.5\"/><path d=\"M8 8.5L20 18M8 15.5L20 6\"/>",
 "pen": "<path d=\"M4 20l3-1 11-11-2-2L5 17z\"/><path d=\"M14 6l2 2M4 20l1-3\"/><circle cx=\"19\" cy=\"5\" r=\"1.2\"/>",
 "user": "<circle cx=\"12\" cy=\"8\" r=\"3.5\"/><path d=\"M5 20c0-4 3-6 7-6s7 2 7 6\"/>",
 "lock": "<rect x=\"5\" y=\"11\" width=\"14\" height=\"9\" rx=\"2\"/><path d=\"M8 11V8a4 4 0 018 0v3M12 15v2\"/>",
 "sparkle": "<path d=\"M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z\"/>"
}

ICON_RULES = [("بوصلة", "compass"), ("مدير المكتب", "compass"), ("جودة", "shield"), ("اختبار", "shield"), ("تقني", "code"), ("خلفية", "code"),
              ("مهندس", "code"), ("واجه", "window"), ("إبداع", "star"), ("تصميم", "pen"), ("مصمم", "pen"), ("كاتب", "nib"), ("تحرير", "clipboard"),
              ("منتج", "clipboard"), ("باحث", "search"), ("بحث", "search"), ("نشر", "mega"), ("نمو", "mega"), ("عمليات", "build"), ("تنفيذ", "build"),
              ("حركة", "motion"), ("بصري", "eye"), ("صور", "camera")]
ICON_CYCLE = ["layers", "cube", "scene", "orn", "box", "sparkle", "scissors", "clap"]


def pick_icon(r, i):
    s = "%s %s" % (r["name"], r.get("title", ""))
    for kw, ic in ICON_RULES:
        if kw in s:
            return ic
    return ICON_CYCLE[i % len(ICON_CYCLE)]


def parse_stamp(s):
    """«26 أكتوبر 2026، 22:10» إلى ISO بتوقيت الرياض، أو None."""
    m = re.search(r"(\d+)\s+(%s)\s+(\d{4})[،,]?\s*(\d+):(\d+)" % "|".join(MONTHS), s or "")
    if not m:
        return None
    return "%04d-%02d-%02dT%02d:%02d:00+03:00" % (int(m.group(3)), MONTHS.index(m.group(2)) + 1, int(m.group(1)), int(m.group(4)), int(m.group(5)))


def clip(s, n):
    s = re.sub(r"\s+", " ", (s or "")).strip()
    return s if len(s) <= n else s[:n].rstrip() + "…"


def dash(s):
    s = (s or "").strip()
    return "" if s in ("—", "-", "") else s


def split_names(cell):
    return [x.strip() for x in re.split(r"[،,+/]| و(?=[^\s])", cell or "") if x.strip() and x.strip() != "—"]


def site_data(root):
    """يبني كائن البيانات بالبنية التي يقرؤها قالب موقع الإدارة."""
    team = load_team(root)
    b = read_board(root)
    owner = team["owner"]
    tasks = b["tasks"]
    status_rows = {role_key(r.get("الدور", "")): r for r in b["team"]}
    by_n = {t["n"]: t for t in tasks}
    names = {role_key(r["name"]): r["name"] for r in team["roster"]}

    def role_of(cell):
        return names.get(role_key(cell), clean_name(cell) if cell else "")

    D_tasks, q_rows, stc = [], [], {}
    for t in tasks:
        st = t["status"].strip() or "محالة"
        if norm(st).startswith("بانتظار اعتماد"):
            st = "بانتظار اعتماد %s" % owner
        stc[st] = stc.get(st, 0) + 1
        deps = [int(x) for x in re.findall(r"\d+", t["after"] or "") if int(x) in by_n]
        open_deps = [d for d in deps if not is_done(by_n[d]["status"])]
        D_tasks.append({"id": t["n"], "frm": role_of(t["from"]) if role_key(t["from"]) in names else t["from"], "to": role_of(t["to"]),
                        "task": clip(t["task"], 600), "due": dash(t["due"]), "st": st, "nxt": clip(dash(t["next"]), 700),
                        "inp": clip(dash(t["inputs"]), 300), "out": clip(dash(t["output"]), 300), "after": dash(t["after"])})
        q_rows.append({"id": t["n"], "to": [role_of(t["to"])], "frm": role_of(t["from"]), "st": st, "task": clip(t["task"], 160),
                       "wait": open_deps, "ready": norm(st) == "محالة" and not open_deps})

    D_team, ei = [], []
    for i, r in enumerate(team["roster"]):
        mine = [t for t in D_tasks if role_key(t["to"]) == role_key(r["name"])]
        sr = status_rows.get(role_key(r["name"]), {})
        doing = [t for t in mine if t["st"] == "قيد التنفيذ"]
        ready = [t for t in mine if t["st"] == "محالة" and next(q for q in q_rows if q["id"] == t["id"])["ready"]]
        waiting = [t for t in D_tasks if t["st"].startswith("بانتظار اعتماد") and role_key(t["to"]) == role_key(r["name"])]
        last = dash(sr.get("آخر نشاط", ""))
        D_team.append({
            "name": r["name"], "title": r["title"], "spec": r["scope"], "gpt": r["platform"].strip().lower() not in ("claude", "كلود"),
            "last": last, "at": parse_stamp(last),
            "now": clip("; ".join("الصف %d: %s" % (t["id"], t["task"]) for t in doing[:2]) or dash(sr.get("الحالة", "")) or "", 260),
            "nxt": clip("; ".join("الصف %d" % t["id"] for t in ready[:5]), 260),
            "need": clip("؛ ".join(["اعتماد الصف %d" % t["id"] for t in waiting] + ([dash(sr.get("ملاحظة", ""))] if dash(sr.get("ملاحظة", "")) else [])), 220),
            "cmd": start_cmd(r), "full": r["chat"]})
        ei.append(pick_icon(r, i))

    circs = []
    for c in b["circulars"]:
        txt = c["text"]
        m = re.match(r"\*\*\((.*?)\)\s*(.*?)\*\*\s*(.*)", txt, re.S)
        if m:
            when, title, body = m.group(1), m.group(2).strip().rstrip(":"), m.group(3).strip()
        else:
            first = re.split(r"(?<=[.:؛؟!])\s", txt, 1)[0]
            when, title, body = "", clip(first, 90), txt
        circs.append({"n": c["n"], "when": when, "title": title, "text": clip(body or txt, 900)})

    dec = []
    logf = root / "Docs" / "Decision Log.md"
    if logf.exists():
        for d in parse_table(logf.read_text(encoding="utf-8").splitlines()):
            if d.get("#", "").strip().isdigit():
                dec.append({"n": int(d["#"]), "when": d.get("التاريخ", ""), "text": clip(d.get("القرار", ""), 900), "ref": dash(d.get("الوسم", ""))})

    pend = [clip(re.sub(r"\s+", " ", x["text"]), 220) for x in b["decisions"]]

    out, seen = [], set()
    skip_top = {"Office", "Tools", "Archive", ".git"}
    nimg, imgs = 0, {}
    for dp, dn, fn in os.walk(root):
        rel = Path(dp).relative_to(root)
        dn[:] = [d for d in dn if not d.startswith(".") and not (rel == Path(".") and d in skip_top)]
        for f in fn:
            if f.startswith("."):
                continue
            p = Path(dp) / f
            try:
                stt = p.stat()
            except OSError:
                continue
            r = p.relative_to(root).as_posix()
            out.append([r, stt.st_size, int(stt.st_mtime)])
            if f.lower().endswith(IMG_EXT):
                nimg += 1
                g = r.split("/")[0] if "/" in r else "الجذر"
                imgs[g] = imgs.get(g, 0) + 1
    out.sort(key=lambda x: -x[2])
    out = out[:2500]

    gen = now().isoformat(timespec="minutes")
    return {
        "q": {"ts": int(now().timestamp() * 1000), "at": gen, "rows": q_rows},
        "gen": gen, "goal": team["goal"], "goalNow": team["goal"], "feat": "",
        "team": D_team, "tasks": D_tasks, "stc": stc, "nt": len(D_tasks), "nc": len(circs),
        "circs": circs, "dec": dec, "pend": pend,
        "ideas": [], "ch": [], "labels": {}, "dropped": [], "disc": [],
        "imgs": imgs, "nimg": nimg, "th": [], "png": [], "out": out, "links": {},
        "tpl": {"close": CLOSE_T, "resume": RESUME_T}, "ico": ICONS, "ei": ei}


def safe_name(s):
    return re.sub(r"[\\<>\"'`\u2028\u2029]", "", s or "").strip()


def render_site(root):
    team = load_team(root)
    data = site_data(root)
    project = safe_name(team["project"])
    owner = safe_name(team["owner"])
    title = "مكتب إدارة %s" % project
    prefix = "of%s." % hashlib.sha256(project.encode("utf-8")).hexdigest()[:6]
    html = load_template()
    # بدائل نصية داخل شيفرة JS: تُحقن بعد إزالة الرموز المخلة بالنصوص
    for k, v in (("@@TITLE@@", title), ("@@PROJECT@@", project), ("@@OWNER@@", owner), ("@@COMPASSCHAT@@", next((r["chat"] for r in team["roster"] if r["id"] == "compass"), COMPASS)),
                 ("@@COMPASS@@", COMPASS), ("@@PREFIX@@", prefix), ("@@ROOTURI@@", root.resolve().as_uri() + "/")):
        html = html.replace(k, v.replace("&", "&amp;").replace("<", "&lt;") if k in ("@@TITLE@@",) else v)
    if team.get("accent"):
        html = html.replace("#2F6BE0", team["accent"])
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/").replace("<!--", "<\\!--").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return html.replace("@@DATA@@", payload)


def build_site(root, report=None, open_it=False):
    out = root / "Office" / OFFICE_FILE
    atomic_write(out, render_site(root))
    if report is not None:
        report.append(("بُني", out))
    if open_it:
        import webbrowser
        webbrowser.open(out.as_uri())
    return out


# ---------------------------------------------------------------- الأوامر


def cmd_new(a):
    interactive = sys.stdin.isatty() and not a.yes

    def ask(prompt, default=""):
        if not interactive:
            return default
        v = input("%s%s: " % (prompt, (" [%s]" % default) if default else "")).strip()
        return v or default

    name = a.name or ask("اسم المشروع")
    if not name:
        die("اسم المشروع مطلوب: new \"الاسم\" --goal \"الهدف بجملة\"")
    goal = a.goal or ask("هدف المشروع بجملة واحدة")
    if not goal:
        die("هدف المشروع مطلوب: --goal \"...\"")
    owner = a.owner or ask("كيف تحب أن يخاطبك الفريق", "الرئيس")
    preset = a.preset
    if not preset:
        names = list(PRESETS)
        labels = {"general": "عام", "software": "برمجي", "transformation": "تحول بالذكاء الاصطناعي", "operations": "عمليات وأداء", "data": "بيانات وذكاء أعمال", "content": "محتوى"}
        if interactive:
            print("نوع الفريق:  " + "   ".join("%d) %s" % (i, labels.get(k, k)) for i, k in enumerate(names, 1)))
            pick = ask("اختر الرقم", "1")
            preset = names[int(pick) - 1] if pick.isdigit() and 1 <= int(pick) <= len(names) else (pick if pick in PRESETS else "general")
        else:
            preset = "general"
    if preset not in PRESETS and not a.roles_file:
        die("نوع الفريق غير معروف: %s. المتاح: %s" % (preset, ", ".join(PRESETS)))
    roles = None
    if a.roles_file:
        data = json.loads(Path(a.roles_file).read_text(encoding="utf-8"))
        roles = [(r["name"], r.get("title", r["name"]), r.get("scope", ""), r.get("platform", "Claude")) for r in data]
    parent = a.dest or (str(Path.home() / "Documents" / "Project Forge") if interactive else str(Path.cwd()))
    report = []
    root = create_project(parent, name, goal, owner, preset, roles, a.accent, report)
    if a.register:
        try_register(root, a.registry)
    if interactive:
        compass = next(r for r in load_team(root)["roster"] if r["id"] == "compass")
        print("\nتم إنشاء مشروعك بنجاح (%d ملفًا)." % len(report))
        print("المكان: %s\n" % root)
        print("الخطوات التالية:")
        print("1. سيفتح موقع الإدارة الآن في المتصفح (وهو أيضًا في Office/%s)." % OFFICE_FILE)
        print("2. افتح محادثة جديدة في Claude أو ChatGPT، وأرفق مجلد المشروع إن أمكن.")
        print("3. ألصق هذا الأمر في المحادثة لتبدأ مع البوصلة:\n")
        print("    " + start_cmd(compass))
    else:
        print("تم إنشاء المشروع: %s\n" % root)
        for k, p in report:
            try:
                rel = p.relative_to(root)
            except ValueError:
                rel = p
            print("  %s  %s" % (k, rel))
        print("\nالخطوة التالية: افتح Office/%s ثم كلّم البوصلة وحدها." % OFFICE_FILE)
    if interactive:
        try:
            import webbrowser
            webbrowser.open((root / "Office" / OFFICE_FILE).as_uri())
        except Exception:
            pass


def cmd_build(a):
    root = find_root(a.root)
    out = build_site(root, None, a.open)
    print("بُني: %s" % out)


def mtimes(root):
    files = [root / "Agents" / "Board.md", root / "Agents" / "Team.json", root / "Docs" / "Decision Log.md"]
    return tuple(f.stat().st_mtime if f.exists() else 0 for f in files)


def cmd_watch(a):
    root = find_root(a.root)
    last = None
    print("أراقب %s (إيقاف: Ctrl+C)" % root)
    try:
        while True:
            m = mtimes(root)
            if m != last:
                last = m
                build_site(root)
                print("%s  أُعيد بناء الموقع" % now().strftime("%H:%M:%S"))
            time.sleep(a.every)
    except KeyboardInterrupt:
        print("\nتوقفت المراقبة.")


def cmd_rows(a):
    root = find_root(a.root)
    b = read_board(root)
    mine = [t for t in b["tasks"] if role_key(t["to"]) == role_key(a.role)]
    ready = ready_tasks(b["tasks"], a.role)
    print("صفوف «%s»: %d جاهزة من %d" % (a.role, len(ready), len(mine)))
    for t in ready:
        print("\n%d. %s\n   من: %s | المدخلات: %s\n   المخرج: %s" % (t["n"], t["task"], t["from"], t["inputs"], t["output"]))
    cont = [t for t in mine if norm(t["status"]).startswith("قيد التنفيذ") or norm(t["status"]).startswith("اعيدت") or norm(t["status"]).startswith("أعيدت")]
    for t in cont:
        print("\n(%s) %d. %s\n   للتالي: %s" % (t["status"], t["n"], t["task"], t["next"]))
    if not ready and not cont:
        print("لا مهام جاهزة")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def board_write(root, mutate, by):
    """يقرأ اللوحة، يطبق التعديل، ويتحقق أنها لم تتغير أثناء ذلك؛ وإلا يحفظ مسودة ولا يكتب."""
    p = root / "Agents" / "Board.md"
    before = sha(p)
    text = p.read_text(encoding="utf-8")
    new = mutate(text.splitlines())
    new = touch_updated("\n".join(new) + "\n", by)
    if sha(p) != before:
        draft = root / "Agents" / "Row Drafts" / ("Draft %s.md" % now().strftime("%Y-%m-%d %H%M%S"))
        atomic_write(draft, new)
        die("تغيّرت اللوحة أثناء الكتابة؛ لم أكتب شيئًا. حُفظت المسودة في: %s" % draft, 2)
    atomic_write(p, new)


def audit(root, by, action):
    p = root / "Agents" / "Audit Log.md"
    text = p.read_text(encoding="utf-8") if p.exists() else AUDIT_T
    atomic_write(p, text.rstrip("\n") + "\n| %s | %s | %s |\n" % (fmt_dt(now()), esc_cell(by), esc_cell(action)))


def history_add(root, n, status, by):
    p = root / "Data" / "Status History.csv"
    text = p.read_text(encoding="utf-8") if p.exists() else HISTORY_HEAD
    atomic_write(p, text.rstrip("\n") + "\n" + ",".join(csv_cell(x) for x in (n, status, by, now().isoformat(timespec="minutes"))) + "\n")


def csv_cell(v):
    s = str(v)
    return '"%s"' % s.replace('"', '""') if re.search(r'[",\n]', s) else s


def read_history(root):
    p = root / "Data" / "Status History.csv"
    if not p.exists():
        return []
    import csv
    import io
    rows = list(csv.DictReader(io.StringIO(p.read_text(encoding="utf-8-sig"))))
    out = []
    for r in rows:
        try:
            out.append({"n": int(r["n"]), "status": r["status"], "by": r["by"], "at": dt.datetime.fromisoformat(r["at"])})
        except (KeyError, ValueError):
            continue
    return out


def cmd_add_row(a):
    root = find_root(a.root)
    team = load_team(root)
    names = {role_key(r["name"]) for r in team["roster"]} | {role_key(team["owner"])}
    for f in (a.frm, a.to):
        if role_key(f) not in names:
            die("اسم غير معروف في الفريق: «%s». المتاح: %s" % (f, "، ".join(sorted(names))))
    b = read_board(root)
    dup = [t for t in b["tasks"] if t["task"].strip() == a.task.strip() and role_key(t["to"]) == role_key(a.to) and not is_done(t["status"])]
    if dup:
        die("صف مطابق موجود: %d. لم أضف شيئًا." % dup[0]["n"])
    opened = [t for t in b["tasks"] if role_key(t["to"]) == role_key(a.to) and not (is_done(t["status"]) or norm(t["status"]).startswith(("ملغ", "مؤجل")))]
    if len(opened) >= a.cap and not a.force:
        die("«%s» عنده %d صفوف مفتوحة (السقف %d). أغلق منها أو أضف --force." % (a.to, len(opened), a.cap))
    n = max([t["n"] for t in b["tasks"]] + [0]) + 1
    row = [n, a.frm, a.to, a.task, a.inputs, a.output, a.after, a.due, "محالة", a.next]
    line = "| " + " | ".join(esc_cell(c) for c in row) + " |"

    def mutate(lines):
        r = section_range(lines, 3)
        if not r:
            die("لا يوجد القسم 3 في اللوحة")
        last = None
        for i in range(r[0] + 1, r[1]):
            if lines[i].strip().startswith("|"):
                last = i
        if last is None:
            die("لا يوجد جدول مهام في القسم 3")
        return lines[:last + 1] + [line] + lines[last + 1:]

    board_write(root, mutate, a.frm)
    audit(root, a.frm, "أضاف الصف %d إلى %s: %s" % (n, a.to, a.task))
    history_add(root, n, "محالة", a.frm)
    build_site(root)
    print("أُضيف الصف %d: %s ← %s" % (n, a.frm, a.to))


def cmd_set_status(a):
    root = find_root(a.root)
    team = load_team(root)
    owner = team["owner"]
    st = a.status.strip()
    canon = [s.replace("بانتظار اعتماد", "بانتظار اعتماد %s" % owner) if s == "بانتظار اعتماد" else s for s in STATUSES]
    match = [s for s in canon if norm(s) == norm(st)]
    if not match:
        die("حالة غير معتمدة: «%s». المتاح: %s" % (st, "، ".join(canon)))
    st = match[0]
    if norm(st) in ("معتمدة", "ملغاة") and not a.owner_order:
        die("«%s» بأمر %s الصريح فقط. أضف --owner-order إن أمر بذلك." % (st, owner), 3)
    def mutate(lines):
        r = section_range(lines, 3)
        hdr = None
        hit = False
        out = list(lines)
        for i in range(r[0] + 1, r[1]):
            ln = lines[i]
            if not ln.strip().startswith("|"):
                continue
            cells = split_row(ln)
            if hdr is None:
                hdr = cells
                continue
            if re.fullmatch(r"\d+", cells[0].strip()) and int(cells[0]) == a.n:
                cells += [""] * (len(hdr) - len(cells))
                cells[hdr.index("الحالة")] = st
                if a.note:
                    cells[hdr.index("للتالي")] = a.note
                out[i] = "| " + " | ".join(esc_cell(c) for c in cells) + " |"
                hit = True
        if not hit:
            die("لا يوجد صف بالرقم %d" % a.n)
        return out

    board_write(root, mutate, a.by or COMPASS)
    audit(root, a.by or COMPASS, "غيّر حالة الصف %d إلى «%s»%s" % (a.n, st, (": " + a.note) if a.note else ""))
    history_add(root, a.n, st, a.by or COMPASS)
    build_site(root)
    print("الصف %d ← %s" % (a.n, st))


def regenerate_claude_table(root, team):
    p = root / "CLAUDE.md"
    if not p.exists():
        return
    t = p.read_text(encoding="utf-8")
    new = re.sub(r"<!-- team:start -->.*?<!-- team:end -->", lambda m: "<!-- team:start -->\n%s\n<!-- team:end -->" % team_table(team["roster"]), t, flags=re.S)
    atomic_write(p, new)


def cmd_add_role(a):
    root = find_root(a.root)
    team = load_team(root)
    name = clean_name(a.name)
    if any(role_key(r["name"]) == role_key(name) for r in team["roster"]):
        die("الدور موجود: %s" % name)
    n = max(r["n"] for r in team["roster"]) + 1
    r = {"id": "r%d" % n, "n": n, "name": name, "title": a.title or name, "scope": a.scope or "(اكتب الاختصاص)", "platform": a.platform,
         "chat": "%d. %s: %s" % (n, name, a.title or name)}
    team["roster"].append(r)
    save_team(root, team)
    write_new(root / "Agents" / "Roles" / ("%s.md" % name), role_doc(team, r))
    atomic_write(root / "Agents" / "Start Commands.md", start_commands_md(team))
    regenerate_claude_table(root, team)

    def mutate(lines):
        rg = section_range(lines, 4)
        last = max(i for i in range(rg[0] + 1, rg[1]) if lines[i].strip().startswith("|"))
        row = "| " + " | ".join(esc_cell(c) for c in [name, "فعّال", "—", "0", "—"]) + " |"
        return lines[:last + 1] + [row] + lines[last + 1:]

    board_write(root, mutate, COMPASS)
    build_site(root)
    print("أُضيف الدور %d. %s وحُدّثت القواعد والأوامر واللوحة والموقع." % (n, name))


def cmd_decide(a):
    root = find_root(a.root)
    team = load_team(root)
    p = root / "Docs" / "Decision Log.md"
    text = p.read_text(encoding="utf-8") if p.exists() else DECISION_LOG_T
    nums = [int(d["#"]) for d in parse_table(text.splitlines()) if d.get("#", "").strip().isdigit()]
    n = max(nums + [0]) + 1
    tag = a.tag or "قابل للتراجع"
    line = "| %d | %s | %s | %s | %s |" % (n, fmt_date(now()), esc_cell(a.text), esc_cell(tag), esc_cell(a.source or team["owner"]))
    atomic_write(p, text.rstrip("\n") + "\n" + line + "\n")
    audit(root, a.source or team["owner"], "سجّل القرار %d (%s): %s" % (n, tag, a.text))
    build_site(root)
    print("سُجّل القرار %d (%s)" % (n, tag))


# ---------------------------------------------------------------- التقارير والتصدير

DECISION_SLA_HOURS = 48
OPEN_CAP = 5


def decision_age_hours(text):
    """عمر البند المعلق بالساعات إن ورد فيه تاريخ ووقت، وإلا None."""
    iso = parse_stamp(text)
    if not iso:
        m = re.search(r"(\d+)\s+(%s)\s+(\d{4})" % "|".join(MONTHS), text)
        if not m:
            return None
        iso = "%04d-%02d-%02dT00:00:00+03:00" % (int(m.group(3)), MONTHS.index(m.group(2)) + 1, int(m.group(1)))
    return (now() - dt.datetime.fromisoformat(iso)).total_seconds() / 3600


def metrics(root):
    team = load_team(root)
    b = read_board(root)
    tasks = b["tasks"]
    hist = read_history(root)
    st = {}
    for t in tasks:
        k = norm(t["status"])
        st[k] = st.get(k, 0) + 1
    done = sum(v for k, v in st.items() if k.startswith(("مسلم", "معتمد")))
    returned = st.get(norm("أعيدت للتعديل"), 0)
    waiting = sum(v for k, v in st.items() if k.startswith("بانتظار"))
    doing = st.get(norm("قيد التنفيذ"), 0)
    assigned = st.get(norm("محالة"), 0)
    closed_by_qa = done + returned
    qa_rate = (done / closed_by_qa * 100) if closed_by_qa else None
    # زمن الدورة: من أول «محالة» إلى أول «مسلّمة/معتمدة» لكل صف
    first_open, first_done = {}, {}
    for h in sorted(hist, key=lambda x: x["at"]):
        s = norm(h["status"])
        if s == "محالة" and h["n"] not in first_open:
            first_open[h["n"]] = h["at"]
        elif s.startswith(("مسلم", "معتمد")) and h["n"] not in first_done:
            first_done[h["n"]] = h["at"]
    cycles = [(first_done[n] - first_open[n]).total_seconds() / 3600 for n in first_done if n in first_open and first_done[n] >= first_open[n]]
    cycle_avg = sum(cycles) / len(cycles) if cycles else None
    week_ago = now() - dt.timedelta(days=7)
    delivered_week = len({h["n"] for h in hist if norm(h["status"]).startswith(("مسلم", "معتمد")) and h["at"] >= week_ago})
    load = []
    for r in team["roster"]:
        mine = [t for t in tasks if role_key(t["to"]) == role_key(r["name"])]
        open_n = sum(1 for t in mine if not (is_done(t["status"]) or norm(t["status"]).startswith(("ملغ", "مؤجل"))))
        load.append({"name": r["name"], "open": open_n, "done": sum(1 for t in mine if is_done(t["status"])), "over": open_n > OPEN_CAP})
    pend = []
    for d in b["decisions"]:
        age = decision_age_hours(d["text"])
        pend.append({"n": d["n"], "text": clip(d["text"], 160), "age": age, "late": age is not None and age > DECISION_SLA_HOURS})
    logf = root / "Docs" / "Decision Log.md"
    ndec = 0
    if logf.exists():
        ndec = sum(1 for d in parse_table(logf.read_text(encoding="utf-8").splitlines()) if d.get("#", "").strip().isdigit())
    nout = sum(1 for p in (root / "Outputs").rglob("*") if p.is_file() and not p.name.startswith(".")) if (root / "Outputs").exists() else 0
    return {"project": team["project"], "owner": team["owner"], "goal": team["goal"], "at": fmt_dt(now()), "total": len(tasks), "done": done,
            "doing": doing, "waiting": waiting, "assigned": assigned, "returned": returned, "qa_rate": qa_rate, "cycle_avg": cycle_avg,
            "cycle_n": len(cycles), "delivered_week": delivered_week, "load": load, "pending": pend, "circulars": len(b["circulars"]),
            "decisions": ndec, "outputs": nout, "team": len(team["roster"])}


def report_md(m):
    pct = lambda v: "—" if v is None else "%d%%" % round(v)
    hrs = lambda v: "—" if v is None else ("%.1f ساعة" % v if v < 48 else "%.1f يوم" % (v / 24))
    out = ["# تقرير أداء %s" % m["project"], "", "**التاريخ:** %s · **الهدف:** %s" % (m["at"], m["goal"]), "", "## 1. الخلاصة", ""]
    out += ["| المؤشر | القيمة |", "| --- | --- |",
            "| المهام الكلية | %d |" % m["total"], "| المسلّمة والمعتمدة | %d (%s) |" % (m["done"], pct(m["done"] / m["total"] * 100 if m["total"] else None)),
            "| قيد التنفيذ | %d |" % m["doing"], "| بانتظار التدقيق أو الاعتماد | %d |" % m["waiting"], "| محالة ولم تبدأ | %d |" % m["assigned"],
            "| أُعيدت للتعديل | %d |" % m["returned"], "| نسبة المرور من ضمان الجودة | %s |" % pct(m["qa_rate"]),
            "| متوسط زمن الدورة (من الإحالة إلى التسليم) | %s |" % ("—" if m["cycle_avg"] is None else "%s، محسوب على %s" % (hrs(m["cycle_avg"]), "صف واحد" if m["cycle_n"] == 1 else "صفين" if m["cycle_n"] == 2 else "%d صفوف" % m["cycle_n"] if m["cycle_n"] <= 10 else "%d صفًا" % m["cycle_n"])),
            "| المسلّم في آخر 7 أيام | %d |" % m["delivered_week"], "| القرارات المسجلة | %d |" % m["decisions"],
            "| القرارات المعلقة | %d (السقف %d) |" % (len(m["pending"]), OPEN_CAP), "| التعميمات | %d |" % m["circulars"],
            "| الفريق | %d دورًا |" % m["team"], "| ملفات المخرجات | %d |" % m["outputs"]]
    out += ["", "## 2. الحمل على الفريق", "", "| الدور | المفتوحة | المسلّمة | ملاحظة |", "| --- | --- | --- | --- |"]
    for r in m["load"]:
        out.append("| %s | %d | %d | %s |" % (r["name"], r["open"], r["done"], "تجاوز السقف" if r["over"] else ""))
    out += ["", "## 3. ما ينتظر قرار %s" % m["owner"], ""]
    if not m["pending"]:
        out.append("(لا شيء)")
    for d in m["pending"]:
        age = "بلا تاريخ" if d["age"] is None else ("متأخر: %s" % hrs(d["age"]) if d["late"] else "منذ %s" % hrs(d["age"]))
        out.append("%d. %s (%s)" % (d["n"], d["text"], age))
    out += ["", "## 4. التنبيهات", ""]
    alerts = [("%s تجاوز سقف الصفوف المفتوحة" % r["name"]) for r in m["load"] if r["over"]]
    alerts += ["القرار المعلق %d تجاوز %d ساعة؛ يؤخذ بالتوصية" % (d["n"], DECISION_SLA_HOURS) for d in m["pending"] if d["late"]]
    if len(m["pending"]) > OPEN_CAP:
        alerts.append("القرارات المعلقة تجاوزت السقف")
    if m["returned"] > m["done"] and m["returned"]:
        alerts.append("المعاد للتعديل أكثر من المسلّم: راجع وضوح المهام ومعايير القبول")
    out += ["- " + a for a in alerts] or ["(لا تنبيهات)"]
    return "\n".join(out) + "\n"


def cmd_report(a):
    root = find_root(a.root)
    m = metrics(root)
    text = report_md(m)
    out = root / "Docs" / "Reports" / ("Report %s.md" % now().strftime("%Y-%m-%d"))
    out.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(out, text)
    print(text)
    print("حُفظ في: %s" % out.relative_to(root))


def cmd_export(a):
    """يصدّر اللوحة والفريق والقرارات والمؤشرات إلى CSV (بعلامة BOM ليفتحها Excel وPower BI مباشرة)."""
    root = find_root(a.root)
    team = load_team(root)
    b = read_board(root)
    d = root / "Data"
    d.mkdir(exist_ok=True)

    def write(name, header, rows):
        lines = [",".join(csv_cell(h) for h in header)] + [",".join(csv_cell(c) for c in r) for r in rows]
        atomic_write(d / name, "﻿" + "\n".join(lines) + "\n")
        return d / name

    hist = read_history(root)
    first = {}
    for h in sorted(hist, key=lambda x: x["at"]):
        s = norm(h["status"])
        if s == "محالة":
            first.setdefault((h["n"], False), h["at"].isoformat(timespec="minutes"))
        elif s.startswith(("مسلم", "معتمد")):
            first.setdefault((h["n"], True), h["at"].isoformat(timespec="minutes"))
    files = [write("Board.csv", ["n", "from", "to", "task", "inputs", "output", "after", "due", "status", "next", "assigned at", "delivered at"],
                   [[t["n"], t["from"], t["to"], t["task"], t["inputs"], t["output"], t["after"], t["due"], t["status"], t["next"],
                     first.get((t["n"], False), ""), first.get((t["n"], True), "")] for t in b["tasks"]])]
    files.append(write("Team.csv", ["n", "name", "title", "scope", "platform", "open", "done"],
                       [[r["n"], r["name"], r["title"], r["scope"], r["platform"],
                         sum(1 for t in b["tasks"] if role_key(t["to"]) == role_key(r["name"]) and not (is_done(t["status"]) or norm(t["status"]).startswith(("ملغ", "مؤجل")))),
                         sum(1 for t in b["tasks"] if role_key(t["to"]) == role_key(r["name"]) and is_done(t["status"]))] for r in team["roster"]]))
    logf = root / "Docs" / "Decision Log.md"
    decs = [d for d in parse_table(logf.read_text(encoding="utf-8").splitlines()) if d.get("#", "").strip().isdigit()] if logf.exists() else []
    files.append(write("Decisions.csv", ["n", "date", "decision", "tag", "source"], [[x["#"], x.get("التاريخ", ""), x.get("القرار", ""), x.get("الوسم", ""), x.get("المصدر", "")] for x in decs]))
    m = metrics(root)
    files.append(write("Metrics.csv", ["metric", "value"], [["total", m["total"]], ["done", m["done"]], ["doing", m["doing"]], ["waiting", m["waiting"]],
                                                            ["assigned", m["assigned"]], ["returned", m["returned"]], ["qa pass rate", "" if m["qa_rate"] is None else round(m["qa_rate"], 1)],
                                                            ["cycle hours avg", "" if m["cycle_avg"] is None else round(m["cycle_avg"], 1)], ["delivered last 7 days", m["delivered_week"]],
                                                            ["pending decisions", len(m["pending"])], ["decisions", m["decisions"]], ["outputs", m["outputs"]], ["generated at", m["at"]]]))
    for f in files:
        print("صُدّر: %s" % f.relative_to(root))
    print("افتح المجلد Data في Power BI أو Excel؛ الملفات UTF-8 مع BOM.")


def check_project(root):
    problems = []
    for p in root.rglob("*"):
        if "_" in p.name and ".git" not in p.parts:
            problems.append("اسم فيه شرطة سفلية: %s" % p.relative_to(root))
    team = load_team(root)
    if not any(r["name"] == QA_NAME for r in team["roster"]):
        problems.append("لا يوجد %s في الفريق: لا يمكن ضمان أن مخرجًا يصل إلى %s بحكم مستقل" % (QA_NAME, team["owner"]))
    for r in team["roster"]:
        if not (root / "Agents" / "Roles" / ("%s.md" % r["name"])).exists():
            problems.append("ملف الدور ناقص: %s" % r["name"])
    b = read_board(root)
    nums = [t["n"] for t in b["tasks"]]
    if nums != sorted(set(nums)):
        problems.append("ترقيم اللوحة مكرر أو غير مرتب")
    if nums and min(nums) < 1:
        problems.append("الترقيم يجب أن يبدأ من 1")
    known = {role_key(r["name"]) for r in team["roster"]} | {role_key(team["owner"])}
    canon = {norm(s) for s in STATUSES} | {norm("بانتظار اعتماد %s" % team["owner"])}
    for t in b["tasks"]:
        for f in (t["from"], t["to"]):
            if role_key(f) not in known:
                problems.append("الصف %d: اسم غير معروف «%s»" % (t["n"], f))
        if norm(t["status"]) not in canon:
            problems.append("الصف %d: حالة غير معتمدة «%s»" % (t["n"], t["status"]))
        for d in re.findall(r"\d+", t["after"] or ""):
            if int(d) not in nums:
                problems.append("الصف %d: يبدأ بعد صف غير موجود %s" % (t["n"], d))
    for r in team["roster"]:
        n = sum(1 for t in b["tasks"] if role_key(t["to"]) == role_key(r["name"]) and not (is_done(t["status"]) or norm(t["status"]).startswith(("ملغ", "مؤجل"))))
        if n > 5:
            problems.append("%s: %d صفوف مفتوحة (السقف 5)" % (r["name"], n))
    if len(b["decisions"]) > OPEN_CAP:
        problems.append("القرارات المعلقة %d (السقف %d)" % (len(b["decisions"]), OPEN_CAP))
    for d in b["decisions"]:
        age = decision_age_hours(d["text"])
        if age is not None and age > DECISION_SLA_HOURS:
            problems.append("القرار المعلق %d تجاوز %d ساعة: يؤخذ بالتوصية ويُسجَّل بـ decide" % (d["n"], DECISION_SLA_HOURS))
    return problems


def cmd_check(a):
    root = find_root(a.root)
    pr = check_project(root)
    if not pr:
        print("سليم: لا ملاحظات.")
        return
    print("%d ملاحظة:" % len(pr))
    for i, p in enumerate(pr, 1):
        print("%d. %s" % (i, p))
    sys.exit(1)


def try_register(root, registry=None):
    reg = Path(registry) if registry else None
    if reg is None:
        for p in [root.parent] + list(root.parents):
            c = p / "Compass Network" / "Registry.md"
            if c.exists():
                reg = c
                break
    if reg is None or not reg.exists():
        print("لم أجد Registry.md لمركز البوصلات؛ مرّر --registry أو شغّل register لاحقًا.")
        return False
    team = load_team(root)
    text = reg.read_text(encoding="utf-8")
    rel = "%s/%s" % (reg.parent.parent.name, os.path.relpath(root, reg.parent.parent))
    if "`%s`" % rel in text:
        print("المشروع مسجّل في %s" % reg)
        return True
    nums = [int(m.group(1)) for m in re.finditer(r"^\|\s*(\d+)\s*\|", text, re.M)]
    n = max(nums + [0]) + 1
    row = "| %d | %s | `%s` | %s | فعّال | %s | %s |" % (n, team["project"], rel, esc_cell(team["goal"]), fmt_date(now()), fmt_dt(now()))
    atomic_write(reg, text.rstrip("\n") + "\n" + row + "\n")
    print("سُجّل في %s (الرقم %d)" % (reg, n))
    return True


def cmd_register(a):
    try_register(find_root(a.root), a.registry)


def cmd_selftest(a):
    tmp = Path(tempfile.mkdtemp(prefix="forge selftest "))
    ok = True

    def step(name, cond):
        nonlocal ok
        print("%s  %s" % ("ناجح" if cond else "فشل ", name))
        ok = ok and bool(cond)

    try:
        rep = []
        root = create_project(tmp, "مشروع تجريبي", "اختبار الأداة", "الرئيس", "general", None, None, rep)
        step("إنشاء المشروع والملفات", (root / "CLAUDE.md").exists() and (root / "Agents" / "Board.md").exists() and (root / "Office" / OFFICE_FILE).exists())
        step("نسخة الأداة داخل المشروع", (root / "Tools" / TOOL_NAME).exists())
        step("لا شرطة سفلية في الأسماء", not [p for p in root.rglob("*") if "_" in p.name])
        step("الفحص سليم عند الإنشاء", check_project(root) == [])
        ns = argparse.Namespace(root=str(root), frm="البوصلة", to="رئيس المنتج", task="كتابة المرجع", inputs="—", output="`Outputs/x.md`", after="1", due="—", next="—", cap=5, force=False)
        cmd_add_row(ns)
        b = read_board(root)
        step("إضافة صف برقم متسلسل", [t["n"] for t in b["tasks"]] == [1, 2])
        step("المهمة غير جاهزة قبل تسليم السابقة", ready_tasks(b["tasks"], "رئيس المنتج") == [])
        cmd_set_status(argparse.Namespace(root=str(root), n=1, status="مسلّمة", note="تم", by=None, owner_order=False))
        step("تصبح جاهزة بعد التسليم", len(ready_tasks(read_board(root)["tasks"], "رئيس المنتج")) == 1)
        try:
            cmd_set_status(argparse.Namespace(root=str(root), n=1, status="معتمدة", note=None, by=None, owner_order=False))
            blocked = False
        except SystemExit as e:
            blocked = e.code == 3
        step("«معتمدة» ممنوعة دون أمر الصاحب", blocked)
        cmd_add_role(argparse.Namespace(root=str(root), name="المحلل", title="محلل البيانات", scope="التحليل", platform="Claude"))
        step("إضافة دور تحدّث الجدول والموقع", "المحلل" in (root / "CLAUDE.md").read_text(encoding="utf-8") and (root / "Agents" / "Roles" / "المحلل.md").exists())
        cmd_decide(argparse.Namespace(root=str(root), text="اختبار قرار", tag=None, source=None))
        html = (root / "Office" / OFFICE_FILE).read_text(encoding="utf-8")
        step("الموقع يحمل البيانات", "اختبار قرار" in html and "كتابة المرجع" in html and "المحلل" in html)
        step("الفحص سليم بعد التعديلات", check_project(root) == [])
        step("لا رموز قالب متبقية في الموقع", "@@" not in html)
        m = re.search(r"var D=(\{.*?\});\nvar \$=", html, re.S)
        try:
            d = json.loads(m.group(1)) if m else None
        except ValueError:
            d = None
        step("بيانات الموقع JSON سليمة وتحمل الفريق والمهام", bool(d) and len(d["team"]) >= 7 and d["nt"] == 2 and d["dec"][0]["text"] == "اختبار قرار")
        tool_copy = (root / "Tools" / TOOL_NAME).read_text(encoding="utf-8")
        step("نسخة الأداة داخل المشروع مكتفية بنفسها", '_TEMPLATE_Z = """' in tool_copy and len(tool_copy) > 100000)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\n" + ("كل الاختبارات ناجحة" if ok else "فيه اختبارات فاشلة"))
    sys.exit(0 if ok else 1)


def main(argv=None):
    ap = argparse.ArgumentParser(prog=TOOL_NAME, description="Project Forge: أداة بناء مشروع بفريق ذكاء اصطناعي وموقع إدارته")
    ap.add_argument("--root", help="جذر المشروع (يُكتشف تلقائيًا)")
    sp = ap.add_subparsers(dest="cmd", required=True)

    p = sp.add_parser("new", help="إنشاء مشروع كامل")
    p.add_argument("name", nargs="?")
    p.add_argument("--goal")
    p.add_argument("--owner")
    p.add_argument("--preset", choices=list(PRESETS))
    p.add_argument("--roles-file", help="ملف JSON بقائمة أدوار: [{name,title,scope,platform}]")
    p.add_argument("--dest", help="المجلد الأب الذي يُنشأ فيه المشروع")
    p.add_argument("--accent", help="لون أساسي بصيغة #RRGGBB للوضع الفاتح")
    p.add_argument("--register", action="store_true", help="سجّل المشروع في مركز البوصلات")
    p.add_argument("--registry", help="مسار Registry.md")
    p.add_argument("--yes", action="store_true", help="بلا أسئلة")
    p.set_defaults(fn=cmd_new)

    p = sp.add_parser("build", help="بناء موقع الإدارة")
    p.add_argument("--open", action="store_true")
    p.set_defaults(fn=cmd_build)
    p = sp.add_parser("watch", help="إعادة البناء تلقائيًا")
    p.add_argument("--every", type=float, default=2.0)
    p.set_defaults(fn=cmd_watch)
    p = sp.add_parser("rows", help="الصفوف الجاهزة لدور")
    p.add_argument("role")
    p.set_defaults(fn=cmd_rows)

    p = sp.add_parser("add-row", help="إضافة صف إلى اللوحة")
    p.add_argument("--from", dest="frm", required=True)
    p.add_argument("--to", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--inputs", default="—")
    p.add_argument("--output", default="—")
    p.add_argument("--after", default="—")
    p.add_argument("--due", default="—")
    p.add_argument("--next", default="—")
    p.add_argument("--cap", type=int, default=5)
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_add_row)

    p = sp.add_parser("set-status", help="تغيير حالة صف")
    p.add_argument("n", type=int)
    p.add_argument("status")
    p.add_argument("--note")
    p.add_argument("--by")
    p.add_argument("--owner-order", action="store_true")
    p.set_defaults(fn=cmd_set_status)

    p = sp.add_parser("add-role", help="إضافة دور")
    p.add_argument("name")
    p.add_argument("--title")
    p.add_argument("--scope")
    p.add_argument("--platform", default="Claude")
    p.set_defaults(fn=cmd_add_role)

    p = sp.add_parser("decide", help="تسجيل قرار")
    p.add_argument("text")
    p.add_argument("--tag")
    p.add_argument("--source")
    p.set_defaults(fn=cmd_decide)

    sp.add_parser("report", help="تقرير أداء: المؤشرات والحمل والقرارات المتأخرة").set_defaults(fn=cmd_report)
    sp.add_parser("export", help="تصدير اللوحة والفريق والقرارات والمؤشرات إلى CSV لـ Power BI").set_defaults(fn=cmd_export)
    sp.add_parser("check", help="فحص المشروع").set_defaults(fn=cmd_check)
    p = sp.add_parser("register", help="تسجيل في مركز البوصلات")
    p.add_argument("--registry")
    p.set_defaults(fn=cmd_register)
    sp.add_parser("selftest", help="اختبار ذاتي").set_defaults(fn=cmd_selftest)

    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
