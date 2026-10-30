#!/usr/bin/env python3
"""Builds site/index.html, the public site, from this generator and tools/site/{i18n.py, atom.js}.

    python3 -I tools/build-site.py [REPO_URL] [SITE_URL]

The page opens in English, offers the eight interface languages and localizes every string from tools/site/i18n.py.
"""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "tools" / "site"))
from forge import core  # noqa: E402
from i18n import U, KEYS  # noqa: E402

REPO = (sys.argv[1] if len(sys.argv) > 1 else "https://github.com/HakamiDev/ProjectForge").rstrip("/")
SITE = (sys.argv[2].rstrip("/") + "/") if len(sys.argv) > 2 else ""
RAW = "https://raw.githubusercontent.com/" + "/".join(REPO.split("/")[-2:]) + "/main/"
NPR, NRO, NSK = len(core.PRESETS), len(core.role_library()), len(core.SKILLS)
for _lang, _t in U.items():  # the catalogue numbers quoted in every language must match the registry
    assert all(str(n) in " ".join(_t.values()) for n in (NPR, NRO, NSK)), (_lang, NPR, NRO, NSK)
ORDER = ["Arabic", "English", "Macedonian", "Spanish", "German", "Portuguese", "Russian", "Chinese"]  # approved order of the language bar
_BY_EN = {row[3]: row for row in core.LANGUAGES}
assert sorted(_BY_EN) == sorted(ORDER) and set(ORDER) == set(U), (sorted(_BY_EN), sorted(U))
LANGS = [[_BY_EN[name][1], name] for name in ORDER]
for _l,_v in {"Arabic":"الأقسام","English":"Sections","Spanish":"Secciones","German":"Bereiche","Portuguese":"Secções","Russian":"Разделы","Chinese":"栏目","Macedonian":"Делови"}.items(): U[_l]["navl"]=_v
html='''<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Project Forge</title>
<meta name="description" content="Open-source tool that turns a project folder into a managed office for a team of AI agents: clear roles, a shared board, measurable progress. Python only, no libraries.">
<meta property="og:type" content="website">
<meta property="og:title" content="Project Forge: your team of AI agents under one management">
<meta property="og:description" content="One board, clear ownership for every task, review before delivery, and progress you can measure. One line installs everything.">
<meta property="og:image" content="'''+SITE+'''og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="logo/logo.svg">
<link rel="apple-touch-icon" href="icon-192.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* تخطيط: عمود واحد هادئ بعرض مقروء؛ ترتيب القراءة: ما هو، ماذا يعطيك، كيف يعمل، التثبيت، المكتبة */
:root{
  --bg:#FFFFFF;--soft:#F4F5F7;--fg:#0B0C0E;--mute:#586070;--line:rgba(11,12,14,.12);
  --blue:#1F6FEB;--blue-ink:#FFFFFF;--blue-text:#1F6FEB;
  --font:"IBM Plex Sans Arabic","IBM Plex Sans",system-ui,"PingFang SC","Microsoft YaHei","Noto Sans SC",-apple-system,"Segoe UI",sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0B0C0E;--soft:#14161A;--fg:#F4F5F7;--mute:#9AA2B0;--line:rgba(244,245,247,.14);
  --blue:#2C6CE5;--blue-text:#6EA2F8;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0B0C0E;--soft:#14161A;--fg:#F4F5F7;--mute:#9AA2B0;--line:rgba(244,245,247,.14);--blue:#2C6CE5;--blue-text:#6EA2F8;color-scheme:dark}
:root{direction:rtl}:root[dir="ltr"]{direction:ltr}
*{box-sizing:border-box}
html,body{overflow-x:clip}html{scroll-behavior:smooth;scroll-padding-top:72px}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.8 var(--font);-webkit-font-smoothing:antialiased;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
a{color:inherit}
.wrap{max-width:860px;margin:0 auto}
:focus{outline:none}:focus-visible{outline:1.5px solid var(--mute);outline-offset:2px}input:focus-visible{outline:none;border-color:var(--mute)}

/* الرأس */
header{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--line)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
.bar{max-width:860px;margin:0 auto;height:60px;display:flex;align-items:center;gap:20px}
.brand{font-weight:700;font-size:18px;text-decoration:none;letter-spacing:-.01em;margin-inline-end:auto;direction:ltr}
nav{display:flex;gap:22px;font-size:15px}
nav a{text-decoration:none;color:var(--mute)}nav a:hover{color:var(--fg)}
.tg{width:42px;height:24px;border-radius:99px;border:1px solid var(--line);background:var(--soft);position:relative;cursor:pointer;padding:0}
.tg::after{content:"";position:absolute;top:2px;inset-inline-start:2px;width:18px;height:18px;border-radius:50%;background:var(--fg);transition:inset-inline-start .2s}
.tg[aria-checked="true"]::after{inset-inline-start:20px}
@media(max-width:640px){nav{display:none}}

/* القسم الأول */
.hero{padding:72px 0 56px}
.hero h1{font-size:clamp(34px,6vw,54px);line-height:1.25;margin:0 0 20px;font-weight:700;letter-spacing:-.01em;text-wrap:balance}
.hero p.lead{font-size:20px;color:var(--mute);margin:0 0 32px;max-width:36em}
.btns{display:flex;gap:12px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;height:48px;padding:0 26px;border-radius:12px;font:600 16px var(--font);text-decoration:none;border:1px solid var(--line);color:var(--fg);background:transparent;cursor:pointer}
.btn.pri{background:var(--blue);border-color:var(--blue);color:var(--blue-ink)}
.btn:hover{filter:brightness(1.06)}
.facts{display:flex;gap:10px 22px;flex-wrap:wrap;margin:36px 0 0;padding:0;list-style:none;color:var(--mute);font-size:15px}
.facts li::before{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--blue);margin-inline-end:8px;vertical-align:middle}

/* الأقسام */
section{padding:64px 0;border-top:1px solid var(--line)}
h2{font-size:30px;line-height:1.3;margin:0 0 12px;font-weight:700;letter-spacing:-.01em}
.sub{color:var(--mute);margin:0 0 36px;max-width:38em}
.list{display:grid;grid-template-columns:1fr 1fr;gap:30px 44px;margin:0;padding:0;list-style:none}
.list h3{font-size:18px;margin:0 0 4px;font-weight:600}
.list p{margin:0;color:var(--mute);font-size:16px;line-height:1.75}
@media(max-width:640px){.list{grid-template-columns:1fr}}
.steps{margin:0;padding:0;list-style:none;display:grid;gap:28px;counter-reset:s}
.steps li{display:grid;grid-template-columns:44px 1fr;gap:16px;align-items:start}
.steps li::before{counter-increment:s;content:counter(s);width:44px;height:44px;border-radius:50%;border:1.5px solid var(--blue);color:var(--blue-text);display:grid;place-items:center;font:600 18px var(--font)}
.steps h3{font-size:19px;margin:6px 0 4px;font-weight:600}
.steps p{margin:0;color:var(--mute)}
code.i{font:15px var(--mono);background:var(--soft);padding:2px 7px;border-radius:6px;direction:ltr;unicode-bidi:isolate}

/* التثبيت والمكتبة */
.opt{display:grid;gap:22px;margin:0 0 28px}
.opt label,.opt .l{display:block;font-weight:600;font-size:15px;margin-bottom:8px}
.chips{display:flex;gap:8px;flex-wrap:wrap}
.chips button,.seg button{font:500 15px var(--font);color:var(--fg);background:transparent;border:1px solid var(--line);border-radius:10px;padding:8px 16px;cursor:pointer}
.chips button[aria-pressed="true"],.seg button[aria-selected="true"]{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.seg{display:flex;gap:8px;flex-wrap:wrap}
.hint{margin:0 0 12px;color:var(--mute);font-size:15px}
.cw{position:relative;margin:0}
pre.code{margin:0;background:var(--soft);border:1px solid var(--line);border-radius:12px;padding:18px 84px 18px 20px;font:14px/1.8 var(--mono);direction:ltr;text-align:left;white-space:pre-wrap;word-break:break-word}
pre.code.pr{font-family:var(--font);font-size:15px}
pre.code.ar{direction:rtl;text-align:right;font-family:var(--font);font-size:15px;padding:18px 20px 18px 84px}
pre.code.ar+.copy{left:10px;right:auto}
.copy{position:absolute;top:10px;right:10px;font:500 13px var(--font);padding:6px 14px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--fg);cursor:pointer}
.copy.ok{background:var(--blue);border-color:var(--blue);color:var(--blue-ink)}
.after{margin-top:18px;color:var(--mute);font-size:16px}
.libbar{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-bottom:22px}
.search{flex:1;min-width:200px;height:42px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--fg);padding:0 14px;font:15px var(--font)}
.lib{display:grid;gap:26px}
.item{display:grid;grid-template-columns:150px 1fr;gap:6px 22px;padding-top:26px;border-top:1px solid var(--line)}
.item:first-child{border-top:0;padding-top:0}
.nm{font-weight:600}.nm.m{font-family:var(--mono);font-size:15px;unicode-bidi:isolate;text-align:start}
.d{margin:0 0 10px;color:var(--mute);font-size:16px}
.empty{color:var(--mute)}
@media(max-width:640px){.item{grid-template-columns:1fr}}
footer{border-top:1px solid var(--line);padding:32px 0 56px;color:var(--mute);font-size:15px}
footer .wrap{display:flex;gap:12px;flex-wrap:wrap;justify-content:space-between}
.toast{position:fixed;bottom:max(24px,env(safe-area-inset-bottom,0px));left:50%;transform:translate(-50%,20px);background:var(--fg);color:var(--bg);padding:10px 20px;border-radius:10px;font-size:15px;opacity:0;pointer-events:none;transition:.25s}
.toast.show{opacity:1;transform:translate(-50%,0)}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}

/* تحسينات التصميم */
body{background:radial-gradient(70% 560px at 72% 0,color-mix(in srgb,var(--blue) 15%,transparent),transparent 70%) no-repeat,var(--bg)}
header{margin:0 -16px;padding:0 16px}

.logo{display:block;flex:none;width:30px;height:30px;border-radius:24%}
.brand{display:flex;align-items:center;gap:10px}
header{background:color-mix(in srgb,var(--bg) 86%,transparent);-webkit-backdrop-filter:saturate(1.4) blur(14px);backdrop-filter:saturate(1.4) blur(14px)}
.hero{padding:56px 0 36px}
.kick{display:inline-flex;align-items:center;gap:8px;font:600 14px var(--font);color:var(--blue-text);background:color-mix(in srgb,var(--blue) 10%,transparent);border:1px solid color-mix(in srgb,var(--blue) 22%,transparent);padding:4px 14px;border-radius:99px;margin-bottom:22px}
.nums{display:flex;gap:0;margin:44px 0 0;padding:0;list-style:none;border:1px solid var(--line);border-radius:16px;background:var(--soft);overflow:hidden}
.nums li{flex:1;padding:18px 20px;text-align:center;border-inline-start:1px solid var(--line)}
.nums li:first-child{border-inline-start:0}
.nums b{display:block;font:700 30px/1.2 var(--font);letter-spacing:-.01em}
.nums span{color:var(--mute);font-size:14px}
.eyebrow{display:block;font:600 13px var(--font);letter-spacing:.08em;color:var(--blue-text);margin-bottom:10px}
.list{gap:16px}
.list li{background:var(--soft);border:1px solid var(--line);border-radius:16px;padding:24px 24px 22px}
.list h3{font-size:18px;margin:0 0 6px}
.steps{position:relative;gap:16px}
.steps li{background:var(--soft);border:1px solid var(--line);border-radius:16px;padding:22px 24px;align-items:center}
.steps li::before{background:var(--blue);border-color:var(--blue);color:var(--blue-ink)}
.steps h3{margin:0 0 4px}
.btn.pri{box-shadow:0 8px 24px color-mix(in srgb,var(--blue) 35%,transparent)}
.btn{transition:transform .15s,filter .15s}.btn:hover{transform:translateY(-1px)}
section{border-top:0;padding:72px 0}
section+section{border-top:1px solid var(--line)}
@media(max-width:720px){.hero{padding:36px 0 36px}.nums b{font-size:24px}.nums li{padding:14px 8px}}
.langbar{border-bottom:1px solid var(--line);background:var(--soft);margin:0 -16px;padding:0 16px}
.bar2{max-width:860px;margin:0 auto;display:flex;align-items:center;gap:14px;min-height:56px;padding:8px 0}
.bar2 .l{font-weight:600;font-size:14px;color:var(--mute);white-space:nowrap}
.bar2 .chips{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;padding:2px}
.bar2 .chips::-webkit-scrollbar{display:none}
.bar2 .chips button{white-space:nowrap;padding:6px 14px;font-size:14px;background:var(--bg)}
.bar2 .chips button[aria-pressed="true"]{background:var(--fg);color:var(--bg)}
.hero{padding-top:56px}

/* ===== زجاج موقع الإدارة: خلفية متدرجة بإضاءتين، وبطاقات زجاجية شفافة بضبابية وحافة واحدة وظل ناعم، ورأس كبسولة عائمة ===== */
:root{--pg1:#EEF3FB;--pg2:#DAE6F8;--g:rgba(255,255,255,.66);--gl:rgba(20,55,120,.14);--gs:rgba(31,80,170,.22);--gb:rgba(255,255,255,.82)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--pg1:#0B0C0E;--pg2:#181A1F;--g:rgba(255,255,255,.045);--gl:rgba(244,245,247,.12);--gs:rgba(0,0,0,.55);--gb:rgba(20,22,27,.72)}}
:root[data-theme="dark"]{--pg1:#0B0C0E;--pg2:#181A1F;--g:rgba(255,255,255,.045);--gl:rgba(244,245,247,.12);--gs:rgba(0,0,0,.55);--gb:rgba(20,22,27,.72)}
html{background:var(--pg2)}
body{background:radial-gradient(60% 520px at 90% -6%,color-mix(in srgb,var(--blue) 22%,transparent),transparent 70%),radial-gradient(55% 460px at -4% 14%,color-mix(in srgb,var(--blue) 16%,transparent),transparent 70%),linear-gradient(182deg,var(--pg1),var(--pg2)) fixed;background-attachment:fixed}
body::before{background:transparent}
header{margin:10px auto 0;max-width:900px;padding:0 20px;border:1px solid var(--gl);border-radius:22px;background:var(--gb);-webkit-backdrop-filter:blur(18px) saturate(1.5);backdrop-filter:blur(18px) saturate(1.5);box-shadow:0 18px 40px -22px var(--gs);top:calc(env(safe-area-inset-top,0px) + 10px)}
.langbar{margin:10px auto 0;max-width:900px;padding:0 20px;border:1px solid var(--gl);border-radius:22px;background:var(--g);-webkit-backdrop-filter:blur(14px) saturate(1.4);backdrop-filter:blur(14px) saturate(1.4);box-shadow:0 18px 40px -24px var(--gs)}
.bar2 .chips button{background:var(--g)}
.list li,.steps li,pre.code{background:var(--g);border:1px solid var(--gl);-webkit-backdrop-filter:blur(2.5px) saturate(1.3);backdrop-filter:blur(2.5px) saturate(1.3);box-shadow:0 22px 40px -22px var(--gs)}
.list li,.steps li{border-radius:18px}
.chips button,.seg button,.btn:not(.pri){background:var(--g);border-color:var(--gl);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.copy{background:var(--gb);border-color:var(--gl)}
code.i{background:var(--g);border:1px solid var(--gl)}
section+section{border-top-color:var(--gl)}
footer{border-top-color:var(--gl)}
/* ===== رأس موقع الإدارة بالضبط: كبسولة زجاجية بانكسار وخط سفلي، بلا شفق ===== */
:root{--gfill:rgba(255,255,255,.66);--hi:.35;--shd:rgba(31,80,170,.2);--s1:#0B0C0E;--s2:#1F6FEB}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--gfill:rgba(255,255,255,0);--hi:.06;--shd:rgba(0,0,0,.5);--s1:#F4F5F7}}
:root[data-theme="dark"]{--gfill:rgba(255,255,255,0);--hi:.06;--shd:rgba(0,0,0,.5);--s1:#F4F5F7}
header{position:sticky;isolation:isolate;overflow:hidden;border:0;border-radius:999px;margin:10px auto 0;max-width:900px;padding:0 20px;top:calc(env(safe-area-inset-top,0px) + 10px);
background:linear-gradient(90deg,transparent,#83B1F6,#88B4F6,#84B2F6,#75A8F5,#94BCF7,transparent) 50% calc(100% - 1px)/66% .3px no-repeat,var(--gfill);
-webkit-backdrop-filter:blur(2.5px) saturate(1.3);backdrop-filter:blur(2.5px) saturate(1.3);backdrop-filter:url(#orf) blur(2.5px) saturate(1.3);
box-shadow:inset 0 0 0 1px rgba(255,255,255,.2),inset 0 2px 2px rgba(255,255,255,var(--hi)),inset 0 -3px 8px rgba(255,255,255,calc(var(--hi)*.35)),inset 5px 0 14px -6px rgba(255,255,255,calc(var(--hi)*.55)),0 22px 40px -18px var(--shd)}
header>*{position:relative;z-index:1}
@media(max-width:640px){header{margin-inline:-6px;padding:0 14px}.langbar{margin-inline:-6px;border-radius:18px;padding:0 14px}}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="orf" color-interpolation-filters="sRGB" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.005" numOctaves="1" seed="4" result="n0"/><feGaussianBlur in="n0" stdDeviation="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="56" xChannelSelector="R" yChannelSelector="G" result="d"/><feGaussianBlur in="d" stdDeviation="1.1"/></filter></svg>
<header><div class="bar">
  <a class="brand" href="#top"><i class="logo" aria-hidden="true"></i>Project Forge</a>
  <nav aria-label="الأقسام"><a href="#install">التثبيت</a><a href="#features">ماذا يعطيك</a><a href="#how">كيف يعمل</a><a href="'''+REPO+'''" target="_blank" rel="noopener">GitHub</a></nav>
  <button class="tg" id="theme" type="button" role="switch" aria-checked="false" aria-label="الوضع الداكن"></button>
</div></header>
<div class="langbar"><div class="bar2"><span class="l">اللغة</span><div class="chips" id="langs" role="group" aria-label="اللغة"></div></div></div>

<main id="top">
<div class="wrap">
  <div class="hero">
    <div>
    <h1>فريقك من وكلاء الذكاء الاصطناعي، تحت إدارة واحدة.</h1>
    <p class="lead">حوّل مجلد مشروعك إلى مكتب عمل واضح الأدوار: تُوزَّع فيه المهام، وتُراجَع المخرجات، ويظهر التقدم بالأرقام.</p>
    <div class="btns"><a class="btn pri" href="#install">ابدأ التثبيت</a></div>
    <ul class="facts"><li>مفتوح المصدر</li><li>بايثون وحده، بلا مكتبات خارجية</li><li>يعمل مع Claude وChatGPT وGemini وGrok</li></ul>
    </div>
  </div>

  <section id="install">
    <span class="eyebrow">البداية</span><h2>التثبيت</h2>
    <p class="sub">سطر واحد تلصقه في Terminal فيُنزّل الأداة ويفتح صفحة الإنشاء في متصفحك. وفي المرات التالية يكفي السطر نفسه. إن لم يوجد Python على جهازك فسيُطلب تثبيته تلقائيًا.</p>
    <div class="opt">
      <div><span class="l">نظام جهازك</span><div class="seg" id="os"><button type="button" aria-selected="true">Mac</button><button type="button" aria-selected="false">Windows</button><button type="button" aria-selected="false">للمطورين</button></div></div>
      <div><span class="l">منصة الذكاء الاصطناعي</span><div class="chips" id="plat"><button type="button" aria-pressed="true">Claude</button><button type="button" aria-pressed="false">ChatGPT</button><button type="button" aria-pressed="false">Gemini</button><button type="button" aria-pressed="false">Grok</button></div></div>
    </div>
    <p class="hint" id="osHint"></p>
    <div id="inst"></div>
    <p class="after">بعد الإنشاء افتح <code class="i">Office/Project Office.html</code> ثم كلّم البوصلة وحدها، وهي توزّع العمل على الفريق.</p>
  </section>

  <section id="features">
    <span class="eyebrow">المزايا</span><h2>ماذا يعطيك</h2>
    <p class="sub">من أول تكليف إلى آخر قرار، يعرف كل عضو في الفريق ما عليه، وتعرف أنت ما أُنجز وما ينتظر مراجعتك.</p>
    <ul class="list">
      <li><h3>بوصلة تجمع عمل الفريق</h3><p>توزّع المهام على المختصين، وتتابع التسليم، وتحرّك العمل العالق من لوحة واحدة.</p></li>
      <li><h3>استمرارية تتجاوز المحادثة</h3><p>تُحفظ التعليمات والأدوار والقرارات في ملفات المشروع، فيرجع إليها الوكلاء عند استئناف العمل.</p></li>
      <li><h3>مسؤولية واضحة لكل مهمة</h3><p>تعرف من يتولى كل مهمة، وما المطلوب تسليمه، وما الذي ينتظر إنجاز مهمة أخرى.</p></li>
      <li><h3>مراجعة قبل أن يصلك المخرج</h3><p>يُفحص كل تسليم بمعايير القبول في المرجع، ويُعاد ما يحتاج إلى تعديل قبل عرضه عليك.</p></li>
      <li><h3>تقدّم تراه بالأرقام</h3><p>نسبة التسليم، وزمن الإنجاز، والحمل على الأدوار، والقرارات المتأخرة، مع تصدير بصيغة CSV.</p></li>
      <li><h3>فريق قابل للتخصيص</h3><p>ابدأ من 80 تخصصًا و334 دورًا و130 مهارة جاهزة، ثم عدّل الفريق بما يناسب مشروعك.</p></li>
    </ul>
  </section>

  <section id="how">
    <span class="eyebrow">الآلية</span><h2>كيف يعمل</h2>
    <p class="sub">ثلاث خطوات، ثم يستمر العمل من اللوحة.</p>
    <ol class="steps">
      <li><div><h3>أنشئ المشروع</h3><p>أربعة أسئلة: الاسم، والهدف، وكيف تُخاطَب، ووصف المشروع بجملة. تقترح الأداة أقرب تخصص من 80، وتعدّل الأدوار والمهارات بالنقر.</p></div></li>
      <li><div><h3>افتح محادثة لكل موظف</h3><p>انسخ أمر البدء من موقع الإدارة. يقرأ الموظف دوره من المجلد ويعمل على اللوحة.</p></div></li>
      <li><div><h3>تابع وقِس</h3><p>موقع الإدارة يعرض ما ينتظرك ومن يعمل الآن. وفي نهاية الأسبوع: <code class="i">report</code> للتقرير و<code class="i">export</code> لملفات CSV.</p></div></li>
    </ol>
  </section>


</div>
</main>
<footer><div class="wrap"><span>Project Forge · رخصة MIT</span><a href="'''+REPO+'''" target="_blank" rel="noopener">'''+REPO.replace('https://','')+'''</a></div></footer>
<div class="toast" id="toast" role="status">تم النسخ</div>

<script>
(function(){
"use strict";
var REPO="'''+REPO+'''";
var RAW="'''+RAW+'''";
var LANGS='''+json.dumps(LANGS,ensure_ascii=False)+''';
var CODE={Arabic:"ar",English:"en",Spanish:"es",German:"de",Portuguese:"pt",Russian:"ru",Chinese:"zh-Hans",Macedonian:"mk"};
var GITC={Arabic:"للتحديث لاحقًا",English:"To update later",Spanish:"Para actualizar más adelante",German:"Zum späteren Aktualisieren",Portuguese:"Para atualizar mais tarde",Russian:"Для обновления позже",Chinese:"以后更新时运行",Macedonian:"За подоцнежно ажурирање"};
var I18N='''+json.dumps(U,ensure_ascii=False)+''';

function $(s){return document.querySelector(s)}
function E(t){return String(t).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
var root=document.documentElement,tb=$("#theme");
function isDark(){var t=root.getAttribute("data-theme");if(t)return t==="dark";return matchMedia("(prefers-color-scheme: dark)").matches}
function syncTheme(){tb.setAttribute("aria-checked",String(isDark()))}
tb.addEventListener("click",function(){var d=!isDark();root.setAttribute("data-theme",d?"dark":"light");try{localStorage.setItem("pf-theme",d?"dark":"light")}catch(e){}syncTheme()});
try{var st=localStorage.getItem("pf-theme");if(st)root.setAttribute("data-theme",st)}catch(e){}
syncTheme();
var toastT;
function toast(){var t=$("#toast");t.textContent=TX("toast");t.classList.add("show");clearTimeout(toastT);toastT=setTimeout(function(){t.classList.remove("show")},1500)}
function done(btn){toast();if(btn){btn.classList.add("ok");btn.textContent=TX("cpd");setTimeout(function(){btn.classList.remove("ok");btn.textContent=TX("cp")},1300)}}
function fallback(t,btn){var a=document.createElement("textarea");a.value=t;a.style.position="fixed";a.style.opacity="0";document.body.appendChild(a);a.select();try{document.execCommand("copy");done(btn)}catch(e){}a.remove()}
function copy(t,btn){try{navigator.clipboard.writeText(t).then(function(){done(btn)},function(){fallback(t,btn)})}catch(e){fallback(t,btn)}}
document.addEventListener("click",function(e){var b=e.target.closest(".copy");if(b)copy(decodeURIComponent(b.getAttribute("data-c")),b)});
function block(t){var pr=!/^python3|^curl|^irm|^\\$env|^git/.test(t),ar=pr&&LANG==="Arabic";return'<div class="cw"><pre class="code'+(pr?" pr":"")+(ar?" ar":"")+'">'+E(t)+'</pre><button class="copy" type="button" data-c="'+E(encodeURIComponent(t))+'">'+TX("cp")+'</button></div>'}
function seg(id,cb){var g=$(id);g.addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;g.querySelectorAll("button").forEach(function(x){x.setAttribute("aria-selected",String(x===b))});cb(b)})}
var PLAT="Claude",LANG="Arabic",OS=/Win/i.test(navigator.platform||navigator.userAgent||"")?1:0;
var lg=$("#langs");
function TX(k){return(I18N[LANG]||I18N.Arabic)[k]}
lg.innerHTML=LANGS.map(function(l){return'<button type="button" aria-pressed="false" data-v="'+l[1]+'" lang="'+CODE[l[1]]+'">'+E(l[0])+'</button>'}).join("");
lg.addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;setLang(b.getAttribute("data-v"),true)});
var pl=$("#plat");pl.addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;PLAT=b.textContent.trim();pl.querySelectorAll("button").forEach(function(x){x.setAttribute("aria-pressed",String(x===b))});inst()});
function envs(){var o=[];if(PLAT!=="Claude")o.push(["FORGE_PLATFORM",PLAT]);if(LANG!=="Arabic")o.push(["FORGE_LANGUAGE",LANG]);return o}
function cmd(i){
  if(i===0){var e=envs().map(function(x){return x[0]+'="'+x[1]+'"'}).join(" ");return"curl -fsSL "+RAW+"install.sh | "+(e?e+" ":"")+"bash"}
  if(i===1){return envs().map(function(x){return"$env:"+x[0]+'="'+x[1]+'"; '}).join("")+"irm "+RAW+"install.ps1 | iex"}
  return"git clone "+REPO+".git\\ncd ProjectForge\\npython3 -m forge\\n\\n# "+GITC[LANG]+"\\ngit pull";
}
function inst(){$("#inst").innerHTML=block(cmd(OS));$("#osHint").textContent=TX("hint"+OS)}
var osb=$("#os").querySelectorAll("button");osb.forEach(function(b,i){b.setAttribute("aria-selected",String(i===OS))});
seg("#os",function(b){OS=Array.prototype.indexOf.call(osb,b);inst()});

function setLang(v,save){
  LANG=I18N[v]?v:"Arabic";
  var rtl=LANG==="Arabic";root.setAttribute("dir",rtl?"rtl":"ltr");root.setAttribute("lang",CODE[LANG]);
  document.querySelectorAll("[data-i]").forEach(function(n){var t=TX(n.getAttribute("data-i"));if(t!=null)n.textContent=t});
  document.querySelectorAll("[data-h]").forEach(function(n){var t=TX(n.getAttribute("data-h"));if(t!=null)n.innerHTML=t});
  document.querySelectorAll("[data-ph]").forEach(function(n){n.setAttribute("placeholder",TX(n.getAttribute("data-ph")))});
  document.querySelectorAll("[data-al]").forEach(function(n){n.setAttribute("aria-label",TX(n.getAttribute("data-al")))});
  lg.querySelectorAll("button").forEach(function(x){x.setAttribute("aria-pressed",String(x.getAttribute("data-v")===LANG))});
  if(save){try{localStorage.setItem("pf-lang",LANG)}catch(e){}}
  inst();
}
setLang("English",false);
})();
</script>
'''
import re as _re
cut=html.index('\n<script>\n(function')
head,tail=html[:cut],html[cut:]
HK={'after','s3p'}
ar=U['Arabic']
order=[k for k in KEYS if k not in ('nl','b2','le','lh','lsub','t1','t2','t3','kick','dark','ph','hint0','hint1','hint2','nores','cp','cpd','toast')]
for k in order:
    a=ar[k]; pat='>'+a+'<'
    assert pat in head,(k,a[:40])
    head=head.replace(pat,'>\x01'+k+'\x02<',1)
for k in order:
    a=ar[k]
    head=head.replace('\x01'+k+'\x02','<span data-%s="%s">%s</span>'%('h' if k in HK else 'i',k,a))
head=head.replace('aria-label="الوضع الداكن"','aria-label="الوضع الداكن" data-al="dark"')
head=head.replace('placeholder="ابحث في المكتبة" aria-label="بحث في المكتبة"','placeholder="ابحث في المكتبة" aria-label="بحث في المكتبة" ')
head=head.replace('role="group" aria-label="اللغة"','role="group" aria-label="اللغة" data-al="langlbl"')
head=head.replace('<nav aria-label="الأقسام">','<nav aria-label="الأقسام" data-al="navl">')
html=head+tail
html+=(root / 'tools' / 'site' / 'atom.js').read_text(encoding='utf-8')
html+='\n</body></html>\n'
out = root / 'site' / 'index.html'
out.write_text(html, encoding='utf-8')
print('Built', out, out.stat().st_size, 'bytes')
