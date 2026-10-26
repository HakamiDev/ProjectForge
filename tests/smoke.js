// اختبار دخان للموقع المولَّد: لا أخطاء، لا تمرير أفقي، كل الأقسام والتبويبات تُرسم.
// الاستعمال: NODE_PATH=$(npm root -g) node tests/smoke.js "Project Office.html" shots
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
const file = path.resolve(process.argv[2]); const out = process.argv[3] || 'shots';
fs.mkdirSync(out, { recursive: true });
const SECS = ['command','room','project','team','library','comms','fav','settings'];
const TABS = { room:['overview','decisions','pulse'], team:['cards','graph','queue'], comms:['circs','cmds'], settings:['general','look','buttons','glass','fonts','tools'] };
(async () => {
  const b = await chromium.launch(); let bad = 0; const errs = [];
  for (const [w,h,scheme] of [[1440,900,'light'],[1440,900,'dark'],[390,844,'light'],[390,844,'dark']]) {
    const ctx = await b.newContext({ viewport:{width:w,height:h}, colorScheme:scheme });
    const pg = await ctx.newPage();
    pg.on('pageerror', e => errs.push(`${w}${scheme} pageerror: ${e.message}`));
    pg.on('console', m => { if (m.type()==='error' && !/fonts\.googleapis|ERR_|Failed to load resource/.test(m.text())) errs.push(`${w}${scheme} console: ${m.text()}`); });
    
    for (const s of SECS) for (const t of (TABS[s] || [null])) {
      await pg.goto('about:blank');
      await pg.goto('file://' + file + '#' + s + '/' + (t||'x') + '/notour', { waitUntil: 'load' });
      await pg.reload(); await pg.waitForTimeout(700);
      const r = await pg.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, len: document.querySelector('#main').innerText.length }));
      const tag = `${w}${scheme} ${s}/${t||''}`;
      if (r.sw > r.cw + 1) { errs.push(`${tag}: تمرير أفقي ${r.sw}>${r.cw}`); }
      if (r.len < 20) errs.push(`${tag}: محتوى فارغ`);
      if (scheme==='light' || w===390) await pg.screenshot({ path: `${out}/${w}-${scheme}-${s}-${t||'x'}.png` });
    }
    await ctx.close();
  }
  // تفاعل: البطاقة الجانبية ولوحة الأوامر وتبديل السمة
  {
    const ctx = await b.newContext({ viewport:{width:1440,height:900} }); const pg = await ctx.newPage();
    pg.on('pageerror', e => errs.push('interaction pageerror: ' + e.message));
    await pg.goto('file://' + file + '#project/x/notour'); await pg.waitForTimeout(800);
    await pg.click('[data-o^="task:"]'); await pg.waitForTimeout(500);
    if ((await pg.getAttribute('#dr','aria-hidden')) === 'true') errs.push('البطاقة الجانبية لم تُفتح');
    await pg.keyboard.press('Escape'); await pg.waitForTimeout(300);
    await pg.keyboard.press('Control+k'); await pg.waitForTimeout(400);
    if (!(await pg.evaluate(() => document.querySelector('#pal').classList.contains('on') || getComputedStyle(document.querySelector('#pal')).display !== 'none'))) errs.push('لوحة الأوامر لم تُفتح');
    await pg.keyboard.press('Escape');
    const before = await pg.evaluate(() => document.documentElement.dataset.theme || '');
    await pg.click('#th'); await pg.waitForTimeout(300);
    const after = await pg.evaluate(() => document.documentElement.dataset.theme || '');
    if (before === after) errs.push('تبديل السمة لا يعمل');
    await ctx.close();
  }
  await b.close();
  console.log(errs.length ? errs.join('\n') : 'OK بلا أخطاء');
  process.exit(errs.length ? 1 : 0);
})();
