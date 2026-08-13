# -*- coding: utf-8 -*-
"""
ОБЩАЯ страница-шпаргалка по кабинетам Яндекс.Бизнеса — все три клиники
владельца на одной странице, переключаются вкладками (правило владельца,
13.08.2026: «чтобы всё было удобно в одном месте»).

Данные берутся из манифестов `_materials/yb-ads/ads.json` каждого репо —
их пишет скрипт клиники (`page-build.py` / `ads.py`), так что материалы
остаются в своём репозитории, а хаб только рендерит. Нет манифеста —
вкладка показывает, чего не хватает, вместо того чтобы молча пропасть.

Формат манифеста:
  {clinic, city, site, brand:{accent,accent2,bg,ink,line},
   sections:[{title, note, items:[{key,title,desc,price,link,img}]}]}

Запуск: python3 build-hub.py   → «Кабинеты-Яндекс-Бизнес.html»
"""
import json, html, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))   # /home/user
OUT = os.path.join(HERE, 'Кабинеты-Яндекс-Бизнес.html')

CLINICS = [
    ('versal',  'Версаль',    'Реутов',  'Versal-Dent-site'),
    ('angel',   'Ангел-Дент', 'Реутов',  'Angel-Dent-site'),
    ('venecia', 'Венеция',    'Мытищи',  'venecia-dent.ru'),
]

CSS = '''
*{box-sizing:border-box}
body{margin:0;background:#f2f3f5;color:#1d2226;font:16px/1.55 Manrope,system-ui,sans-serif}
.top{background:#fff;border-bottom:1px solid #e3e6ea;position:sticky;top:0;z-index:5}
.top__in{max-width:1080px;margin:0 auto;padding:16px 20px 0}
.top h1{font-size:20px;margin:0 0 3px}
.top p{margin:0 0 14px;color:#6c757d;font-size:14px}
.tabs{display:flex;gap:6px;flex-wrap:wrap}
.tab{border:0;background:transparent;padding:11px 18px;border-radius:10px 10px 0 0;cursor:pointer;
  font:600 15px Manrope,sans-serif;color:#6c757d;border-bottom:3px solid transparent}
.tab:hover{color:#1d2226}
.tab.on{color:#1d2226;background:var(--accent-soft);border-bottom-color:var(--accent)}
.tab i{font-style:normal;font-weight:400;color:#9aa3ab;font-size:13px;margin-left:6px}
.pane{display:none;max-width:1080px;margin:0 auto;padding:26px 20px 80px}
.pane.on{display:block}
.hd{display:flex;align-items:baseline;gap:12px;margin:0 0 6px}
.hd h2{margin:0;font-size:22px}
.hd a{color:var(--accent);font-size:14px;text-decoration:none}
.note{background:#fff;border:1px solid var(--line);border-left:4px solid var(--accent);
  padding:14px 16px;border-radius:10px;margin:14px 0 22px;font-size:15px}
.ad{display:grid;grid-template-columns:190px 1fr;gap:20px;background:#fff;border:1px solid var(--line);
  border-radius:14px;padding:18px;margin:0 0 14px;position:relative}
.ad__num{position:absolute;left:-11px;top:18px;width:26px;height:26px;border-radius:50%;
  background:var(--accent);color:#fff;font:700 13px Manrope,sans-serif;display:grid;place-items:center}
.ad__pic img{width:190px;height:190px;object-fit:cover;border-radius:10px;display:block}
.dl{display:block;width:190px;margin-top:8px;padding:8px 10px;border:1px solid var(--accent);
  border-radius:8px;background:#fff;color:var(--accent);font:600 12.5px/1.2 Manrope,sans-serif;
  cursor:pointer;transition:.15s}
.dl:hover{background:var(--accent);color:#fff}
.dl:disabled{opacity:.6;cursor:default}
.f{margin:0 0 11px}
.f__k{display:block;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:#8d949b;margin-bottom:4px}
.f__k em{font-style:normal;color:#b6bcc2}
.f__v{background:var(--soft);border:1px solid var(--line);border-radius:8px;padding:9px 12px;
  cursor:pointer;transition:.15s;font-size:15px}
.f__v:hover{border-color:var(--accent);background:#fff}
.f__v.copied{border-color:var(--accent);background:var(--accent-soft)}
.f__v i{color:#a4abb2}
.f2{display:grid;grid-template-columns:150px 1fr;gap:14px}
.empty{background:#fff;border:1px dashed #ccd2d8;border-radius:14px;padding:28px;color:#6c757d}
@media(max-width:720px){.ad{grid-template-columns:1fr}.ad__pic img{width:100%;height:auto}
  .dl{width:100%}.f2{grid-template-columns:1fr}}
'''

JS = '''
document.querySelectorAll('.tab').forEach(function(t){
  t.addEventListener('click', function(){
    document.querySelectorAll('.tab').forEach(function(x){ x.classList.remove('on'); });
    document.querySelectorAll('.pane').forEach(function(x){ x.classList.remove('on'); });
    t.classList.add('on');
    var pane = document.getElementById('pane-' + t.dataset.id);
    pane.classList.add('on');
    document.documentElement.style.setProperty('--accent', pane.dataset.accent);
    document.documentElement.style.setProperty('--accent-soft', pane.dataset.accentSoft);
    document.documentElement.style.setProperty('--line', pane.dataset.line);
    document.documentElement.style.setProperty('--soft', pane.dataset.soft);
    localStorage.setItem('kab-tab', t.dataset.id);
  });
});
var saved = localStorage.getItem('kab-tab');
var start = (saved && document.querySelector('.tab[data-id="'+saved+'"]')) || document.querySelector('.tab');
if (start) start.click();

// Скачивание: атрибут download на чужой домен браузер игнорирует, поэтому
// тянем файл через fetch (CDN отдаёт Access-Control-Allow-Origin: *) и
// сохраняем blob под понятным именем. Не вышло — открываем в новой вкладке.
document.querySelectorAll('[data-dl]').forEach(function(btn){
  btn.addEventListener('click', function(){
    var url = btn.dataset.dl, name = btn.dataset.name, txt = btn.textContent;
    btn.disabled = true; btn.textContent = 'Скачиваю…';
    fetch(url).then(function(r){ return r.blob(); }).then(function(b){
      var u = URL.createObjectURL(b), a = document.createElement('a');
      a.href = u; a.download = name; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function(){ URL.revokeObjectURL(u); }, 4000);
      btn.textContent = 'Готово ✓';
      setTimeout(function(){ btn.textContent = txt; btn.disabled = false; }, 1400);
    }).catch(function(){ window.open(url, '_blank'); btn.textContent = txt; btn.disabled = false; });
  });
});
document.querySelectorAll('[data-copy]').forEach(function(el){
  el.addEventListener('click', function(){
    navigator.clipboard.writeText(el.innerText.trim()).then(function(){
      el.classList.add('copied');
      setTimeout(function(){ el.classList.remove('copied'); }, 900);
    });
  });
});
'''


def soft(hex_color, alpha=0.12):
    """тот же акцент, но полупрозрачный — для подложек вкладки и полей"""
    h = hex_color.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f'rgba({r},{g},{b},{alpha})'


def load(repo):
    p = os.path.join(ROOT, repo, '_materials', 'yb-ads', 'ads.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None


def render_items(items, prefix):
    out = []
    for i, it in enumerate(items, 1):
        price = html.escape(it['price']) if it['price'] else '<i>оставить пустым</i>'
        out.append(f'''
<article class="ad">
  <div class="ad__num">{i}</div>
  <div class="ad__pic">
    <img src="{it['img']}" alt="" loading="lazy">
    <button class="dl" data-dl="{it['img']}" data-name="{prefix}-{it['key']}.jpg">Скачать картинку</button>
  </div>
  <div>
    <div class="f"><span class="f__k">Заголовок <em>{len(it['title'])}/56</em></span>
      <div class="f__v" data-copy>{html.escape(it['title'])}</div></div>
    <div class="f"><span class="f__k">Описание <em>{len(it['desc'])}/81</em></span>
      <div class="f__v" data-copy>{html.escape(it['desc'])}</div></div>
    <div class="f2">
      <div class="f"><span class="f__k">Цена</span><div class="f__v" data-copy>{price}</div></div>
      <div class="f"><span class="f__k">Ссылка</span><div class="f__v" data-copy>{it['link']}</div></div>
    </div>
  </div>
</article>''')
    return ''.join(out)


def build():
    tabs, panes = [], []
    for cid, name, city, repo in CLINICS:
        data = load(repo)
        n = sum(len(s['items']) for s in data['sections']) if data else 0
        tabs.append(f'<button class="tab" data-id="{cid}">{name} <i>{city}'
                    + (f' · {n}' if n else ' · нет материалов') + '</i></button>')
        b = (data or {}).get('brand', {'accent': '#4b5563', 'bg': '#fff',
                                       'ink': '#1d2226', 'line': '#e3e6ea'})
        head = (f'<div class="hd"><h2>{name} — {city}</h2>'
                + (f'<a href="{data["site"]}" target="_blank" rel="noopener">{data["site"]}</a>' if data else '')
                + '</div>')
        if not data:
            body = ('<div class="empty">Материалы для кабинета этой клиники пока не собраны: '
                    'в репозитории лежат только скрипты и реестры, самих картинок нет. '
                    'Скажите — соберу такой же пакет объявлений, и вкладка заполнится.</div>')
        else:
            body = ''
            for s in data['sections']:
                body += (f'<div class="note"><b>{html.escape(s["title"])}.</b> {html.escape(s.get("note",""))}<br>'
                         'В поле «Цена» — только число, «от» кабинет не принимает; в заголовке цену '
                         'не дублируем. Срок размещения не ставим — объявления вечные.</div>')
                body += render_items(s['items'], cid)
        panes.append(f'''<section class="pane" id="pane-{cid}"
  data-accent="{b['accent']}" data-accent-soft="{soft(b['accent'])}"
  data-line="{b['line']}" data-soft="{soft(b['accent'], 0.05)}">{head}{body}</section>''')

    doc = f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Кабинеты Яндекс.Бизнеса — три клиники</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="top"><div class="top__in">
  <h1>Материалы для кабинетов Яндекс.Бизнеса</h1>
  <p>Три клиники в одном месте. Клик по полю копирует текст, кнопка — скачивает картинку.</p>
  <div class="tabs">{''.join(tabs)}</div>
</div></div>
{''.join(panes)}
<script>{JS}</script>
</body></html>'''
    open(OUT, 'w', encoding='utf-8').write(doc)
    print('готово:', OUT)


if __name__ == '__main__':
    build()
