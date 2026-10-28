<p align="center"><img src="site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

**نظام تشغيل لفريق وكلاء الذكاء الاصطناعي.** أمر واحد يحوّل مجلدًا عاديًا إلى مكتب عمل منضبط: لوحة واحدة يعمل منها كل الوكلاء على أي منصة، وبوابة جودة مستقلة، وحوكمة قرارات، وأثر تدقيق، ومؤشرات أداء قابلة للتصدير بصيغة CSV، وموقع إدارة يعمل من ملف HTML واحد.

بايثون 3.9 فما فوق، بلا أي مكتبة خارجية، وبلا خادم. [English below](#english).

## التثبيت

سطر واحد يُلصق في الطرفية: يحمّل الأداة ويشغّلها ويسأل أربعة أسئلة ثم يفتح موقع الإدارة.

macOS وLinux:

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

أو نزّل `Project Forge 1.py` من صفحة الإصدارات وشغّله: `python3 -I "Project Forge 1.py"`. تفتح الأداة صفحة بسيطة في المتصفح: تكتب اسم مشروعك وهدفه، وتختار فريقك وتعدّل أدواره بالنقر، ثم تضغط «أنشئ المشروع». المشاريع تُنشأ في `Documents/Project Forge`.

## ما الذي يحله

المحادثات مع الذكاء الاصطناعي تنسى، وتتعارض، ولا تُقاس. هنا المجلد هو الذاكرة، واللوحة هي العقل المشترك، والأرقام هي الحكم:

| المشكلة | الحل |
| --- | --- |
| كل محادثة تبدأ من الصفر | `CLAUDE.md` وملف دور لكل وكيل يُقرأ من المجلد، لا من ذاكرة المحادثة |
| وكيلان يعملان على الشيء نفسه | لوحة واحدة بصفوف مرقمة، و«قيد التنفيذ» تحجز الصف، وبصمة تمنع الكتابة المتعارضة |
| مخرجات تصل إليك بلا فحص | رئيس ضمان الجودة يحكم «يمر أو لا يمر» قبل أن يصل أي مخرج إلى صاحب المشروع |
| قرارات معلقة تعطّل الفريق | سقف خمسة قرارات، ومهلة 48 ساعة تؤخذ بعدها التوصية، وسجل موسوم |
| لا أحد يعرف ما أُنجز | `report` يعطي نسبة التسليم وزمن الدورة ومرور الجودة والحمل، و`export` يصدّرها بصيغة CSV |
| من غيّر ماذا؟ | `Agents/Audit Log.md` يسجّل كل كتابة، و`Data/Status History.csv` كل تغيّر حالة |
| بيانات حساسة في أدوات خارجية | `Docs/Data Policy.md` ملزم: تصنيف البيانات والأدوات المعتمدة |

## قوالب الفرق

ثمانون تخصصًا في إحدى عشرة مجموعة، رُتبت على نسق تصنيفات الأعمال المعتمدة: وظائف المؤسسة (إدارة، مالية، موارد بشرية، تسويق، تقنية، عمليات) على غرار إطار APQC لتصنيف العمليات، والقطاعات على غرار التصنيف الصناعي الدولي ISIC، ثم البحث والتعليم والحياة الشخصية. لكل تخصص فريق من خمسة أدوار وأمثلة أهداف ومرادفات عامية، ومعها «مكتبة أدوار» من أكثر من 330 دورًا.

وفي الواجهة خانة «صف مشروعك بجملة»: تكتب وصفًا بلغتك («عندي كافيه صغير وأبغى أنظم الطلبات») فتقترح الأداة أقرب ثلاثة تخصصات، مرجّحةً الكلمات النادرة الدالة على المجال على الكلمات الشائعة.

| المجموعة | التخصصات |
| --- | --- |
| إدارة واستراتيجية | عام، شركة ناشئة، استشارات، مكتب إدارة مشاريع، جودة وتميز مؤسسي، ابتكار وبحث وتطوير، تدقيق داخلي، استراتيجية وتخطيط، إدارة التغيير، حوكمة ومجالس ولجان، إدارة المخاطر والاستمرارية |
| مالية وقانون وامتثال | مالية ومحاسبة، قانوني وامتثال، مشتريات ومنافسات، ضرائب وزكاة وفوترة، استثمار وتمويل |
| موارد بشرية وتطوير | موارد بشرية، تدريب وتطوير مؤسسي، استقطاب وتوظيف |
| تسويق ومبيعات وعملاء | تسويق وحملات، مبيعات، تجارة إلكترونية، دعم العملاء، علاقات عامة واتصال، علامة تجارية وهوية، إدارة حسابات التواصل، تجربة عميل وولاء |
| تقنية وبيانات | برمجي، تحول بالذكاء الاصطناعي، بيانات وذكاء أعمال، تطبيق جوال، حوكمة الأمن السيبراني، تطوير ألعاب، دعم وتشغيل تقني، إدارة منتج رقمي، بناء منتج ذكاء اصطناعي، أتمتة بلا كود |
| عمليات وإمداد وجودة | عمليات وأداء، سلاسل إمداد، تصنيع وإنتاج، مرافق وصيانة، سلامة وصحة مهنية |
| محتوى وإبداع وإعلام | محتوى، تصميم وإبداع، إنتاج إعلامي، فعاليات ومؤتمرات، تأليف كتاب، ترجمة وتعريب، إنتاج فيديو، صانع محتوى |
| قطاعات | مطاعم وضيافة، عقارات، خدمات صحية إدارية، تعليم وتدريب، خدمات حكومية وسياسات، جمعيات ومبادرات، مقاولات وإنشاءات، سياحة وسفر، مشروع صغير، متجر تجزئة، زراعة ومزارع، طاقة وترشيد، نقل وتوصيل، خدمات حج وعمرة، نادٍ رياضي ولياقة، صالون وتجميل |
| بحث وتعليم | بحث أكاديمي، رسالة ماجستير أو دكتوراه، صناعة دورة تدريبية، التحضير لشهادة مهنية، تعلم لغة |
| حياة شخصية | مسار مهني وبحث عن عمل، حياتي وإنتاجيتي، مالية شخصية، إدارة البيت والأسرة، تخطيط رحلة، زفاف ومناسبة عائلية، خطة قراءة ومعرفة، نادٍ طلابي ومبادرة جامعية |
| مخصص | فريق من الصفر |

مفاتيح القوالب للأمر `--preset`: general، software، transformation، operations، data، content، startup، consulting، pmo، finance، hr، legal، marketing، sales، ecommerce، support، hospitality، realestate، healthcare، education، government، nonprofit، supply، research، design، media، events، job، personal، mobile، cyber، construction، tourism، procurement، book، smallbiz، pr، excellence، innovation، audit، translation، games، strategy، change، governance، riskmgmt، tax، investment، training، recruitment، brand، social، crm، itops، product، aiproduct، nocode، manufacturing، facilities، safety، video، creator، retail، agriculture، energy، transport، hajj، sportsclub، salon، thesis، course، certification، language، pfinance، home، trip، wedding، reading، studentorg، blank.

## المنصة واللغة

عند الإنشاء تختار منصة المحادثات: **Claude** أو **ChatGPT** أو **Grok** أو **Gemini** للجميع، ثم تغيّر منصة كل موظف على حدة إن أردت (الكاتب في ChatGPT والمحلل في Claude مثلًا). وتختار **لغة العمل**: العربية أو English أو أي لغة تكتب اسمها، فيخاطبك الفريق ويكتب مخرجاته وتقاريره بها. وفي سطر الأوامر:

```
python3 -I "Project Forge 1.py" new "My Project" --goal "..." --platform chatgpt --language English
```

**كيف تُهيّأ كل منصة** (بحسب وثائقها المنشورة وقت الكتابة، وقد تتغير الواجهات):

| المنصة | ما تنشئه | كيف تضيف ملفات المشروع |
|---|---|---|
| Claude | مشروع (Project) | أرفق المجلد بالمحادثة أو أضفه إلى المشروع، فيقرأ الملفات ويكتب فيها |
| ChatGPT | مشروع (Project) | ارفع ملفات المجلد إلى المشروع |
| Grok | مشروع: Projects ثم New Project | أضف تعليمات المشروع وارفع الملفات من جهازك أو من Google Drive، فتتاح لكل محادثات المشروع |
| Gemini | Gem: Explore Gems ثم New Gem (من الموقع gemini.google.com) | ألصق الأمر في خانة التعليمات، وأضف الملفات من Knowledge ثم Add files من جهازك أو من Drive |

في كل المنصات ارفع الملفات من مجلد المشروع في مكانه الأصلي ولا تستخدم نسخة أخرى، وأعد رفع ما تغيّر. وعلى حد علمنا لا تكتب Grok وGemini في المجلد مباشرة، فانقل مخرجاتهما إلى المجلد بنفسك.

واجهة المعالج والموقع العام متاحان بـ**27 لغة**: العربية والإنجليزية و25 لغة مترجمة. وتشمل ترجمة المعالج مكتبة الأوامر الظاهرة فيه وأوامر بدء المحادثات. أسماء الأدوار والتخصصات والمهارات تظهر بالإنجليزية عند اختيار لغة واجهة غير العربية.

**حدود التعريب:** موقع الإدارة والملفات المولّدة على القرص، ومنها مكتبة الأوامر واللوحة وملفات التعليمات، ما زالت أساسًا بالعربية، مع توجيه الوكلاء إلى الكتابة بلغة العمل المختارة. أسماء الملفات والأوامر وقيم حالات اللوحة تبقى كما هي لأن الأداة تقرؤها حرفيًا. لا يعني اختيار لغة العمل أن جميع الملفات أو موقع الإدارة مترجمة إليها.

الترجمات مراجعة آليًا؛ لا ندّعي مراجعة ناطق أصلي لكل لغة. تفاصيل التغطية وحدودها في `Language Coverage.md`.

## المهارات ومكتبة الأوامر

مع كل مشروع 130 مهارة جاهزة في 18 مجموعة تختار منها (قياس قبل وبعد، تقرير تنفيذي، مراجعة جودة، تحليل السبب الجذري، ميثاق مشروع، سجل المخاطر، معالجة شكوى، مواصفة أمر لنموذج لغوي، تقييم وكيل آلي، إجراء تشغيل قياسي، توقع الطلب، محضر اجتماع وغيرها). المهارة ملف قصير في `Agents/Skills/` يحدد متى تُستعمل وخطواتها ومخرجها ومعيار قبولها، فيلتزم بها الموظف بدل الاجتهاد كل مرة. تضيف مهارة لاحقًا بأمر `add-skill` وتعرضها بأمر `skills`.

و`Agents/Commands Library.md` مكتبة أوامر جاهزة للنسخ: بدء المحادثات، وأوامر صاحب المشروع اليومية للبوصلة، وأوامر الجودة، والإغلاق والاستئناف، وأوامر الأداة. وتظهر نفسها في شاشة النجاح بعد الإنشاء مع زر نسخ لكل أمر.

## الأوامر

| الأمر | الوظيفة |
| --- | --- |
| `new` | ينشئ مشروعًا كاملًا |
| `build` | يعيد بناء موقع الإدارة من اللوحة |
| `watch` | يعيد البناء تلقائيًا عند تغيّر اللوحة |
| `rows` | يعرض الصفوف الجاهزة لدور |
| `add-row` | يضيف صفًا بأمان: رقم تلقائي ومنع للتعارض وسقف للمفتوح |
| `set-status` | يغيّر حالة صف؛ «معتمدة» و«ملغاة» بأمر صاحب المشروع فقط |
| `add-role` | يضيف دورًا ويحدّث القواعد والأوامر والموقع |
| `skills` | يعرض المهارات الجاهزة وما أُضيف منها |
| `add-skill` | يضيف مهارة جاهزة أو أكثر: `add-skill measure,deck` |
| `decide` | يسجّل قرارًا موسومًا في سجل القرارات |
| `status` | إحاطة سريعة من الطرفية: الأرقام وما ينتظر قرارك وما يحتاج انتباهًا (متأخر، راكد، محجوب، تبعية معطّلة). `--json` للآلة و`--strict` لرمز خروج 2 عند وجود بند عاجل |
| `report` | تقرير أداء: التسليم وزمن الدورة ومرور الجودة والحمل والقرارات المتأخرة |
| `export` | يصدّر اللوحة والفريق والقرارات والمؤشرات إلى ملفات CSV |
| `check` | يفحص المشروع: التسمية والترقيم وسلامة اللوحة ومهلة القرارات |
| `register` | يسجّل المشروع في سجل مركزي للمشاريع |
| `selftest` | يختبر الأداة على مشروع مؤقت |

رسائل التثبيت وسطر الأوامر بالإنجليزية، مستقلة عن لغة واجهة المعالج ولغة عمل الفريق. يحمّل أمر التثبيت الحزمة الحالية من الفرع `main`.

## حالة النسخة

الحزمة المحلية الموحّدة مرشحة للإصدار **1.1.0**؛ وجودها لا يعني نشر الإصدار أو نجاح CI على GitHub. تجربة Windows الفعلية لم تكتمل بعد. نتائج التحقق المحلي في `Verification Results.json`، وتفاصيل الدمج في `Release Notes.md`.

## للمطورين

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
```

```
forge/                حزمة الأداة (core.py) وقالب موقع الإدارة
tools/build-single.py يبني ملف الأداة الواحد المكتفي بنفسه في dist/
tools/build-site.py   يبني الموقع التعريفي site/index.html
tests/                اختبارات الوحدة واختبار المتصفح (Playwright)
site/                 الموقع التعريفي ومكتبة الأوامر وصورة المعاينة
```

الموقع يُنشر تلقائيًا على GitHub Pages عند الدفع إلى `main` (فعّل Pages من Settings ثم Source: GitHub Actions)، وأي وسم إصدار بصيغة `v*` يرفع ملف الأداة الواحد و`Project Forge.zip` إلى صفحة الإصدارات.

## الترخيص

MIT.

---

## English

**Project Forge is an operating system for a team of AI agents.** One command turns a plain folder into a disciplined office: a single board every agent works from (on any platform), an independent QA gate, decision governance, a full audit trail, performance metrics exported as CSV, and a management site that runs from a single HTML file.

Python 3.9+, no runtime dependencies. The creation wizard runs a temporary local server; the generated office is a standalone HTML file. The public site and wizard support **27 interface languages**. Generated project files and the office UI remain primarily Arabic; agents are instructed to use the selected working language. Role, preset and skill labels use English outside the Arabic interface. Translations have automated review, not a native-speaker guarantee. See `Language Coverage.md`.

**Install** (macOS/Linux):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

**What it solves**

- Chats forget: rules and role briefs live in the folder, not in chat memory.
- Agents collide: one numbered board, "in progress" locks a row, a checksum guard prevents conflicting writes.
- Unchecked output: a QA lead rules pass/fail before anything reaches the owner.
- Stalled decisions: a cap of five open decisions and a 48-hour rule after which the recommendation stands.
- Nothing is measured: `report` gives delivery rate, cycle time, QA pass rate and load per role; `export` writes CSV files.
- No accountability: every board write is logged with who, when and what.
- Sensitive data in external tools: a binding data policy with classification and approved tools.

**Catalog:** 80 team presets, 334 reusable roles, and 130 skills in 18 skill groups. Add any role with `add-role`.

**Commands:** `skills`, `add-skill`, `new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

MIT licensed.
