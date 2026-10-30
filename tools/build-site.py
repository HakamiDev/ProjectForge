#!/usr/bin/env python3
"""يبني site/index.html: صفحة تعريف وتثبيت ومكتبة أوامر ومهارات وأدوات، من site/template.html.

    python3 -I tools/build-site.py [REPO_URL]
"""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
from forge import core  # noqa: E402

REPO = (sys.argv[1] if len(sys.argv) > 1 else "https://github.com/HakamiDev/ProjectForge").rstrip("/")
T = core.TOOL_NAME
RUN = 'python3 -I "%s"' % T
RUNP = 'python3 -I "Tools/%s"' % T  # أوامر المشروع تُشغَّل من جذره بنسخة الأداة التي في Tools، وهي بلغة المشروع

cli = [
    ("new", "ينشئ مشروعًا كاملًا: المجلدات والقواعد واللوحة وملفات الأدوار وأوامر البدء وموقع الإدارة.",
     RUN + ' new "اسم المشروع" --goal "هدف المشروع" --owner "الرئيس" --preset transformation --yes'),
    ("build", "يعيد بناء موقع الإدارة من اللوحة. أضف --open لفتحه.", RUNP + " build --open"),
    ("watch", "يعيد البناء تلقائيًا كلما تغيّرت اللوحة أو الفريق أو سجل القرارات.", RUNP + " watch"),
    ("rows", "يعرض الصفوف الجاهزة للبدء لدور معيّن (التي اكتملت متطلباتها).", RUNP + ' rows "رئيس المنتج"'),
    ("add-row", "يضيف صفًا إلى اللوحة بأمان: رقم تلقائي، ومنع للتعارض، وسقف للمفتوح.",
     RUNP + ' add-row --from "البوصلة" --to "رئيس المنتج" --task "كتابة المرجع" --inputs "—" --output "`Outputs/Reference.md`"'),
    ("set-status", "يغيّر حالة صف. «معتمدة» و«ملغاة» تشترطان --owner-order أي أمر صاحب المشروع.", RUNP + ' set-status 3 "مسلّمة" --note "تم"'),
    ("add-role", "يضيف دورًا جديدًا ويحدّث القواعد والأوامر والموقع.", RUNP + ' add-role "المحلل" --title "تحليل البيانات" --scope "التحليل والتقارير"'),
    ("decide", "يسجّل قرارًا في سجل القرارات بترقيم تلقائي.", RUNP + ' decide "اعتماد النسخة الأولى" --tag "قابل للتراجع"'),
    ("status", "إحاطة سريعة من الطرفية: الأرقام وما ينتظر قرارك وما يحتاج انتباهًا (متأخر أو راكد أو محجوب). أضف --json لمخرج الآلة.", RUNP + " status"),
    ("report", "تقرير أداء: نسبة التسليم وزمن الدورة ومرور الجودة والحمل على الأدوار والقرارات المتأخرة. يُحفظ في Docs/Reports.", RUNP + " report"),
    ("export", "يصدّر اللوحة والفريق والقرارات والمؤشرات إلى ملفات CSV بترميز UTF-8 مع BOM.", RUNP + " export"),
    ("check", "يفحص المشروع: التسمية والترقيم وسلامة اللوحة ومهلة القرارات ووجود رئيس ضمان الجودة.", RUNP + " check"),
    ("register", "يسجّل المشروع في سجل مركز البوصلات (Registry.md).", RUNP + " register"),
    ("selftest", "يختبر الأداة على مشروع مؤقت ويبلغ بنجاح كل خطوة.", RUN + " selftest"),
]

agents = [
    ("بدء محادثة موظف", "الصقه في محادثة جديدة. يعرّف الموظف بدوره ويحيله إلى ملف أمر التكليف.",
     "أنت «1. رئيس المنتج: المرجع والقرارات والخطة». اقرأ Agents/Roles/رئيس المنتج.md ثم تابع."),
    ("تشغيل محادثة قائمة", "كلمة واحدة تجعل الموظف يقرأ اللوحة وينفّذ صفوفه الجاهزة.", "تابع"),
    ("أمر الإغلاق", "قبل إغلاق محادثة طالت: يحفظ كل شيء في المجلد ويكتب ملف تسليم.", core.CLOSE_T),
    ("أمر الاستئناف", "في محادثة جديدة بدل المغلقة: يكمل من حيث توقف السلف.", core.RESUME_T),
    ("طلب حكم الجودة", "يطلب من رئيس ضمان الجودة حكمًا مستقلًا: يمر أو لا يمر.",
     "أنت «رئيس ضمان الجودة». افحص مخرج الصف [رقم] من المسار المذكور في اللوحة بمعايير القبول في المرجع، واكتب حكمك في Docs/QA/ بصيغة: يمر / لا يمر مع الأسباب مرتبة بالخطورة، ثم حدّث حالة الصف."),
    ("أول طلب إلى البوصلة", "بعد إنشاء المشروع: ابدأ بالبوصلة وحدها وهي توزع العمل.",
     "أنت «البوصلة: التوجيه العام». اقرأ CLAUDE.md ثم Agents/Board.md. هدفنا: [الهدف]. حوّله إلى صفوف مكتملة في اللوحة، واحدًا لكل مختص، وأخبرني برقم كل صف ومن أبدأ معه أولًا."),
    ("قياس قبل وبعد الأتمتة", "لمحلل العمليات: يقيس الإجراء قبل الأتمتة ليُقارن بعدها.",
     "أنت «محلل العمليات». اختر الإجراء المتكرر المذكور في صفك، وارسمه خطوة خطوة، وقِس لكل خطوة: الزمن، ومن ينفذها، وعدد مرات التكرار أسبوعيًا، والأخطاء الشائعة. احفظ النتيجة في Data/Before.csv بالأعمدة: step, owner, minutes, weekly runs, errors. ثم اكتب في «للتالي» الخطوات المرشحة للأتمتة بترتيب الأثر."),
    ("تصميم وكيل لإجراء", "لمهندس الأتمتة: يصمم الوكيل قبل بنائه بمواصفة تُراجَع.",
     "أنت «مهندس الأتمتة». صمّم وكيلًا للإجراء في صفك بمواصفة من ستة بنود: المدخلات ومصدرها، والمخرجات وشكلها، والقواعد التي لا يتجاوزها، ونقاط تدخّل الإنسان، وطريقة القياس بعد التشغيل، والأدوات المعتمدة من Docs/Data Policy.md. احفظها في Outputs/ وأحِل الصف إلى رئيس ضمان الجودة بحالة «بانتظار التدقيق»."),
    ("تقرير نهاية اليوم", "يلخص الحالة ويعرض ما ينتظر قرار صاحب المشروع.",
     "اقرأ Agents/Board.md وقدّم لي في خمسة أسطر: ما سُلّم اليوم، وما ينتظر التدقيق، وما ينتظر قراري مع توصيتك لكل قرار، وأهم عائق."),
]

tools = [
    ("Project Forge", "الأداة الأم: ملف بايثون واحد بلا مكتبات خارجية، يبني المشروع وفريقه وموقعه.", "python3 -I \"%s\" new" % T, "جاهز"),
    ("Project Office", "موقع إدارة يُولَّد لكل مشروع في ملف HTML واحد: الرئيسية والمتابعة والمهام والفريق والمخطط والأوامر والإعدادات.", RUNP + " build --open", "جاهز"),
    ("Start Office", "سكربت تشغيل يفتح الموقع ويبقيه محدّثًا تلقائيًا (macOS).", "Tools/Start Office.command", "جاهز"),
    ("Report", "تقرير أداء دوري من اللوحة وتاريخ الحالات: التسليم وزمن الدورة ومرور الجودة والحمل والقرارات.", RUNP + " report", "جاهز"),
    ("Export CSV", "أربعة ملفات CSV للتحليل وإعداد التقارير.", RUNP + " export", "جاهز"),
    ("Smoke test", "اختبار متصفح (Playwright) يفحص كل صفحة وتبويب في الفاتح والداكن والجوال.", "NODE_PATH=$(npm root -g) node tests/smoke.js \"Office/Project Office.html\" shots", "جاهز"),
]

# أوامر الطرفية ونصوص أوامر الموظفين بكل لغة، بأسماء الأدوار والحالات كما تكتبها نسخة الأداة بتلك اللغة
LANG_ARG = {"en": "English", "es": "Spanish", "mk": "Macedonian", "de": "German", "zh": "Chinese", "pt": "Portuguese", "ru": "Russian"}
EX = {  # أمثلة لا مفتاح لها في حزمة اللغات
    "اسم المشروع": {"en": "Project name", "es": "Nombre del proyecto", "mk": "Име на проектот", "de": "Projektname", "zh": "项目名称", "pt": "Nome do projeto", "ru": "Название проекта"},
    "هدف المشروع": {"en": "Project goal", "es": "Objetivo del proyecto", "mk": "Цел на проектот", "de": "Projektziel", "zh": "项目目标", "pt": "Objetivo do projeto", "ru": "Цель проекта"},
    "تحليل البيانات": {"en": "Data analysis", "es": "Análisis de datos", "mk": "Анализа на податоци", "de": "Datenanalyse", "zh": "数据分析", "pt": "Análise de dados", "ru": "Анализ данных"},
    "التحليل والتقارير": {"en": "Analysis and reports", "es": "Análisis e informes", "mk": "Анализи и извештаи", "de": "Analysen und Berichte", "zh": "分析与报告", "pt": "Análises e relatórios", "ru": "Анализ и отчёты"},
    "اعتماد النسخة الأولى": {"en": "Approve the first version", "es": "Aprobar la primera versión", "mk": "Одобрување на првата верзија", "de": "Erste Version freigeben", "zh": "批准第一个版本", "pt": "Aprovar a primeira versão", "ru": "Утвердить первую версию"},
}
AG = {  # أوامر الموظفين 5 إلى 9: {qa} {compass} {pa} {ae} {review} {next}
    "en": ['You are the "{qa}". Review the output of row [number] at the path stated on the board against the acceptance criteria in the reference, write your verdict in Docs/QA/ in the form: pass / fail with the reasons ordered by severity, then update the row status.',
           'You are "{compass}". Read CLAUDE.md, then Agents/Board.md. Our goal: [goal]. Turn it into complete rows on the board, one per specialist, and tell me each row number and whom to start with first.',
           'You are the "{pa}". Choose the recurring process named in your row, map it step by step, and measure for each step: the time, who performs it, how many times it repeats each week, and the common errors. Save the result in Data/Before.csv with the columns: step, owner, minutes, weekly runs, errors. Then write in "{next}" the steps that are candidates for automation, ordered by impact.',
           'You are the "{ae}". Design an agent for the process in your row with a six-part specification: the inputs and their source, the outputs and their form, the rules it never breaks, the points of human intervention, how it is measured after launch, and the approved tools from Docs/Data Policy.md. Save it in Outputs/ and hand the row to the {qa} with the status "{review}".',
           'Read Agents/Board.md and give me in five lines: what was delivered today, what awaits review, what awaits my decision with your recommendation for each, and the main blocker.'],
    "es": ['Eres el «{qa}». Revisa el resultado de la fila [número] en la ruta indicada en el tablero según los criterios de aceptación de la referencia, escribe tu dictamen en Docs/QA/ con la forma: aprobado / rechazado, con los motivos ordenados por gravedad, y luego actualiza el estado de la fila.',
           'Eres «{compass}». Lee CLAUDE.md y luego Agents/Board.md. Nuestro objetivo: [objetivo]. Conviértelo en filas completas en el tablero, una por especialista, y dime el número de cada fila y con quién empezar primero.',
           'Eres el «{pa}». Elige el proceso recurrente indicado en tu fila, represéntalo paso a paso y mide en cada paso: el tiempo, quién lo realiza, cuántas veces se repite por semana y los errores habituales. Guarda el resultado en Data/Before.csv con las columnas: step, owner, minutes, weekly runs, errors. Después escribe en «{next}» los pasos candidatos a automatizar, ordenados por impacto.',
           'Eres el «{ae}». Diseña un agente para el proceso de tu fila con una especificación de seis apartados: las entradas y su origen, las salidas y su forma, las reglas que nunca incumple, los puntos de intervención humana, cómo se mide tras ponerlo en marcha y las herramientas aprobadas en Docs/Data Policy.md. Guárdala en Outputs/ y pasa la fila al {qa} con el estado «{review}».',
           'Lee Agents/Board.md y dame en cinco líneas: lo que se entregó hoy, lo que espera revisión, lo que espera mi decisión con tu recomendación para cada caso y el principal obstáculo.'],
    "mk": ['Ти си „{qa}“. Прегледај го излезот од редот [број] на патеката наведена на таблата според критериумите за прифаќање во референцата, запиши ја својата пресуда во Docs/QA/ во облик: поминува / не поминува, со причините подредени по сериозност, па ажурирај го статусот на редот.',
           'Ти си „{compass}“. Прочитај CLAUDE.md, па Agents/Board.md. Нашата цел: [цел]. Претвори ја во целосни редови на таблата, по еден за секој специјалист, и кажи ми го бројот на секој ред и со кого да почнам прво.',
           'Ти си „{pa}“. Избери ја повторливата постапка наведена во твојот ред, опиши ја чекор по чекор и за секој чекор измери: времето, кој го извршува, колку пати неделно се повторува и честите грешки. Зачувај го резултатот во Data/Before.csv со колоните: step, owner, minutes, weekly runs, errors. Потоа во „{next}“ запиши ги чекорите што се кандидати за автоматизација, подредени по влијание.',
           'Ти си „{ae}“. Дизајнирај агент за постапката во твојот ред со спецификација од шест точки: влезовите и нивниот извор, излезите и нивната форма, правилата што никогаш не ги прекршува, точките на човечка интервенција, начинот на мерење по пуштањето во работа и одобрените алатки од Docs/Data Policy.md. Зачувај ја во Outputs/ и предај го редот на {qa} со статус „{review}“.',
           'Прочитај Agents/Board.md и дај ми во пет реда: што е предадено денес, што чека преглед, што чека моја одлука со твоја препорака за секоја, и најголемата пречка.'],
    "de": ['Du bist der „{qa}“. Prüfe das Ergebnis der Zeile [Nummer] unter dem auf der Tafel genannten Pfad anhand der Abnahmekriterien in der Referenz, schreibe dein Urteil in Docs/QA/ in der Form: bestanden / nicht bestanden, mit den Gründen nach Schwere geordnet, und aktualisiere dann den Status der Zeile.',
           'Du bist „{compass}“. Lies CLAUDE.md und dann Agents/Board.md. Unser Ziel: [Ziel]. Mache daraus vollständige Zeilen auf der Tafel, eine pro Fachkraft, und nenne mir die Nummer jeder Zeile und mit wem ich zuerst beginne.',
           'Du bist der „{pa}“. Wähle den wiederkehrenden Ablauf aus deiner Zeile, bilde ihn Schritt für Schritt ab und miss für jeden Schritt: die Zeit, wer ihn ausführt, wie oft er sich pro Woche wiederholt und die häufigen Fehler. Speichere das Ergebnis in Data/Before.csv mit den Spalten: step, owner, minutes, weekly runs, errors. Schreibe dann unter „{next}“ die Schritte, die sich zur Automatisierung eignen, nach Wirkung geordnet.',
           'Du bist der „{ae}“. Entwirf einen Agenten für den Ablauf in deiner Zeile mit einer Spezifikation aus sechs Punkten: die Eingaben und ihre Quelle, die Ausgaben und ihre Form, die Regeln, die er nie bricht, die Punkte menschlichen Eingreifens, wie er nach dem Start gemessen wird, und die freigegebenen Werkzeuge aus Docs/Data Policy.md. Speichere sie in Outputs/ und übergib die Zeile an den {qa} mit dem Status „{review}“.',
           'Lies Agents/Board.md und nenne mir in fünf Zeilen: was heute geliefert wurde, was auf Prüfung wartet, was auf meine Entscheidung wartet, jeweils mit deiner Empfehlung, und das größte Hindernis.'],
    "zh": ['你是“{qa}”。根据参考文档中的验收标准，检查看板上所列路径中第 [编号] 行的成果，并在 Docs/QA/ 中写下你的结论，格式为：通过 / 不通过，原因按严重程度排列，然后更新该行状态。',
           '你是“{compass}”。先阅读 CLAUDE.md，再阅读 Agents/Board.md。我们的目标：[目标]。把它拆成看板上的完整行，每位专员一行，并告诉我每行的编号以及应先从谁开始。',
           '你是“{pa}”。选择你这一行中提到的重复流程，逐步梳理，并为每一步测量：耗时、执行人、每周重复次数和常见错误。把结果保存到 Data/Before.csv，列为：step, owner, minutes, weekly runs, errors。然后在“{next}”中写下适合自动化的步骤，按影响排序。',
           '你是“{ae}”。为你这一行中的流程设计一个智能体，规格包含六部分：输入及其来源、输出及其形式、绝不违反的规则、人工介入点、上线后的衡量方式，以及 Docs/Data Policy.md 中批准的工具。把规格保存到 Outputs/，并将该行以“{review}”状态交给{qa}。',
           '阅读 Agents/Board.md，用五行告诉我：今天交付了什么、什么在等待审核、什么在等待我决定（每项附上你的建议），以及最大的障碍。'],
    "pt": ['És o «{qa}». Revê o resultado da linha [número] no caminho indicado no quadro com base nos critérios de aceitação da referência, escreve o teu parecer em Docs/QA/ na forma: aprovado / reprovado, com os motivos ordenados por gravidade, e depois atualiza o estado da linha.',
           'És a «{compass}». Lê CLAUDE.md e depois Agents/Board.md. O nosso objetivo: [objetivo]. Transforma-o em linhas completas no quadro, uma por especialista, e diz-me o número de cada linha e com quem começar primeiro.',
           'És o «{pa}». Escolhe o procedimento recorrente indicado na tua linha, descreve-o passo a passo e mede em cada passo: o tempo, quem o executa, quantas vezes se repete por semana e os erros habituais. Guarda o resultado em Data/Before.csv com as colunas: step, owner, minutes, weekly runs, errors. Depois escreve em «{next}» os passos candidatos a automatização, ordenados por impacto.',
           'És o «{ae}». Concebe um agente para o procedimento da tua linha com uma especificação de seis pontos: as entradas e a sua origem, as saídas e a sua forma, as regras que nunca infringe, os pontos de intervenção humana, como é medido depois de entrar em funcionamento e as ferramentas aprovadas em Docs/Data Policy.md. Guarda-a em Outputs/ e passa a linha ao {qa} com o estado «{review}».',
           'Lê Agents/Board.md e dá-me em cinco linhas: o que foi entregue hoje, o que aguarda revisão, o que aguarda a minha decisão com a tua recomendação para cada caso e o principal obstáculo.'],
    "ru": ['Вы — «{qa}». Проверьте результат строки [номер] по пути, указанному на доске, на соответствие критериям приёмки из справочника, запишите своё заключение в Docs/QA/ в виде: принято / не принято, с причинами по степени серьёзности, затем обновите статус строки.',
           'Вы — «{compass}». Прочитайте CLAUDE.md, затем Agents/Board.md. Наша цель: [цель]. Превратите её в полные строки на доске, по одной на каждого специалиста, и сообщите мне номер каждой строки и с кого начать.',
           'Вы — «{pa}». Выберите повторяющийся процесс, указанный в вашей строке, опишите его шаг за шагом и измерьте для каждого шага: время, исполнителя, сколько раз в неделю он повторяется и типичные ошибки. Сохраните результат в Data/Before.csv со столбцами: step, owner, minutes, weekly runs, errors. Затем запишите в «{next}» шаги, подходящие для автоматизации, по убыванию эффекта.',
           'Вы — «{ae}». Спроектируйте агента для процесса из вашей строки по спецификации из шести пунктов: входные данные и их источник, результаты и их форма, правила, которые он никогда не нарушает, точки вмешательства человека, способ измерения после запуска и утверждённые инструменты из Docs/Data Policy.md. Сохраните её в Outputs/ и передайте строку сотруднику «{qa}» со статусом «{review}».',
           'Прочитайте Agents/Board.md и дайте мне в пяти строках: что сдано сегодня, что ожидает проверки, что ожидает моего решения с вашей рекомендацией по каждому пункту, и главное препятствие.'],
}


def tr(text, code):
    return EX[text][code] if text in EX else core.loc_tr(text, code)


cli_l, ag_l = {}, {}
for code in ("en", "es", "mk", "de", "zh", "pt", "ru"):
    q = lambda v: '"%s"' % tr(v, code)
    cli_l[code] = {
        "new": RUN + ' new %s --goal %s --owner %s --preset transformation --language %s --yes' % (q("اسم المشروع"), q("هدف المشروع"), q("الرئيس"), LANG_ARG[code]),
        "rows": RUNP + " rows " + q("رئيس المنتج"),
        "add-row": RUNP + ' add-row --from %s --to %s --task %s --inputs "—" --output "`Outputs/Reference.md`"' % (q("البوصلة"), q("رئيس المنتج"), q("كتابة المرجع")),
        "set-status": RUNP + " set-status 3 %s --note %s" % (q("مسلّمة"), q("تم")),
        "add-role": RUNP + " add-role %s --title %s --scope %s" % (q("المحلل"), q("تحليل البيانات"), q("التحليل والتقارير")),
        "decide": RUNP + " decide %s --tag %s" % (q("اعتماد النسخة الأولى"), q("قابل للتراجع")),
    }
    v = dict(qa=tr(core.QA_NAME, code), compass=tr("البوصلة: التوجيه العام", code), pa=tr("محلل العمليات", code), ae=tr("مهندس الأتمتة", code),
             review=tr("بانتظار التدقيق", code), next=tr("للتالي", code))
    head = tr("رئيس المنتج", code)
    ag_l[code] = [tr("أنت «%s». اقرأ Agents/Roles/%s.md ثم تابع.", code) % ("1. %s: %s" % (head, tr("المرجع والقرارات والخطة", code)), head),
                  tr("تابع", code), tr(core.CLOSE_T, code), tr(core.RESUME_T, code)] + [t.format(**v) for t in AG[code]]
for code, cmds in cli_l.items():
    for c in cmds.values():
        assert not re.search(r"[\u0600-\u06FF]", c), (code, c)
for code, cmds in ag_l.items():
    for c in cmds:
        assert not re.search(r"[\u0600-\u06FF]", c), (code, c[:80])

lib = {"repo": REPO, "tool": T, "cli": [dict(n=a, d=b, c=c) for a, b, c in cli],
       "agents": [dict(n=a, d=b, c=c) for a, b, c in agents],
       "tools": [dict(n=a, d=b, c=c, s=s) for a, b, c, s in tools], "cliL": cli_l, "agL": ag_l}
html = (root / "site" / "template.html").read_text(encoding="utf-8")
# الخط وطبقة التصميم الجديدة (سبيكة) تُحقن في آخر وسم style، وخط Cairo القديم يُحذف
_tp = root / "forge" / "templates"
html = re.sub(r'@font-face\{font-family:"Cairo"[^}]*\}\s*', "", html).replace('"Cairo",', '"Forge Sans",')
_extra = "".join((_tp / f).read_text(encoding="utf-8") for f in ("fonts.css", "skin site.css") if (_tp / f).is_file())
_i = html.rfind("</style>")
if _extra and _i >= 0:
    html = html[:_i] + "\n" + _extra + html[_i:]
payload = json.dumps(lib, ensure_ascii=False).replace("</", "<\\/")
out = root / "site" / "index.html"
site_url = (sys.argv[2] if len(sys.argv) > 2 else "").rstrip("/") + ("/" if len(sys.argv) > 2 else "")
en = (root / "site" / "en.json").read_text(encoding="utf-8")
langs = json.dumps([list(x) for x in core.LANGUAGES], ensure_ascii=False)
html = html.replace("@@EN@@", en.replace("</", "<\\/")).replace("@@LANGS@@", langs).replace("@@NSK@@", str(len(core.SKILLS)))
out.write_text(html.replace("@@LIB@@", payload).replace("@@SITEURL@@", site_url), encoding="utf-8")
print("Built", out, out.stat().st_size, "bytes")
