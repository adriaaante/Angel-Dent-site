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

# Материалы, собранные до этой страницы, лежат на Google Диске владельца
# (инвентаризация 13.08.2026). В репозиториях их нет — раньше отдавали
# ссылками, поэтому здесь держим прямые входы в папки, чтобы всё было
# в одном месте. Формат: клиника → [(название, id папки/файла, что внутри)]
DRIVE = {
    'versal': [
        ('Акции ЯБ — карточки', 'folder/1ojHSLN4UmihEicYsAJSb5EkhN1uoaOxT',
         'баннеры акций 1800×960'),
        ('Витрина ЯБ — Версаль', 'folder/1biO8_-qiNfUHv4sE4gnaQpEmuEzgnOjN',
         'картинки позиций витрины 1200×1200'),
        ('История 1 — Не страшно', 'folder/1VxUTwPmPdO8MSW-RmoOceDJPnco3ocfL', 'слайды 1080×1920'),
        ('История 2 — Цены честно', 'folder/1wVH4QmkL0_RP2-SyqAWaqjxtg8RDklOd', 'слайды 1080×1920'),
        ('История 3 — Технологии', 'folder/1pHwgDIO9VkHWx-Bz2ypNjRTu-RsXADXt', 'слайды 1080×1920'),
        ('История 4 — Наши врачи', 'folder/1NJH0OF7MZavSPuaV3uROWtg99metwqfn', 'слайды 1080×1920'),
        ('История 5 — Первый визит', 'folder/1n6s_PICnDw9jlQZ3sNawh-TsaIeYneXR', 'слайды 1080×1920'),
        ('Публикации ЯБ Версаль — v1', 'document/d/1kx-zcGpEwvY6iQsc0psim5p-Fpdq9JcQjmpiTaCHjTI',
         'тексты 2 прежних постов'),
        ('Фото клиники и врачей', 'folder/16sRkQOeuk5TB0GuYURZPAaeip-HimR9J',
         'исходники интерьеров, «Врачи», «Картинки услуг», «Фотки работ»'),
    ],
    'angel': [
        ('Рекламные объявления — видео', 'folder/1MxkdpkSmkKVLHgmKOiIdA8tg0Tfd7-ja',
         '15 роликов по услугам: гигиена, импланты, брекеты, виниры, КТ, отбеливание'),
        ('Истории ЯБ', 'folder/1f2bpYeBBnOoRhb4tZnBR2VxeMbRtPOvv', 'слайды историй'),
        ('Фотографии внутри клиники', 'folder/1lvROa-aX-dLV3EoJXTRv8hUbbzqx8ZEH', 'реальные интерьеры'),
        ('Фотографии акций', 'folder/1-99LrVKEkg8z-WTvG0Qw8gx7CVW4Pw8W', 'кадры под акции'),
        ('Работы врачей', 'folder/1yPE4Yjq--06T0l-1RDp90NVD7yftSu3J', 'исходники «до/после»'),
    ],
    'venecia': [
        ('Венеция — Истории ЯБ v1', 'folder/1TxoepERg5fIhkx8u1TwXVXxVrD5J_Sk9',
         'слайды + документы с порядком заливки'),
        ('Истории ЯБ — порядок слайдов', 'document/d/1rfHKlCftp7UJ_1f6GEym7HNENmcuG9yGG1D6lAxScN8',
         'настройки: название ≤15, кнопка ≤15, ссылки'),
        ('Дополнение: истории 5 и 6', 'document/d/1ZYNJxQgW_oNx_t0r8Xn5Il9aDrQHVlGPy7w28nRGlZo',
         'тексты последних двух историй'),
        ('Фотографии клиники', 'folder/1q77x0l2jd7PzNyGXqD6YiDTutUxuaTxf',
         '14 исходников интерьеров'),
    ],
}

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
.post{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px;margin:0 0 14px}
.post h3{margin:0 0 10px;font-size:18px}
.post h3 span{color:#9aa3ab;font-weight:400;font-size:13px}
.post__gal{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 12px}
.post__gal figure{margin:0;width:150px}
.post__gal img{width:150px;height:96px;object-fit:cover;border-radius:8px;display:block}
.post__gal .dl{width:150px;font-size:11.5px;padding:6px 8px}
.post__txt{white-space:pre-wrap;background:var(--soft);border:1px solid var(--line);border-radius:8px;
  padding:12px 14px;cursor:pointer;font-size:15px;line-height:1.5}
.post__txt:hover{border-color:var(--accent);background:#fff}
.post__txt.copied{border-color:var(--accent);background:var(--accent-soft)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:0 0 22px}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.card h4{margin:0 0 8px;font-size:15px}
.card ul{margin:0;padding-left:18px;color:#5a6167;font-size:14.5px}
.card li{margin:3px 0}
.card a{color:var(--accent)}
.sec{margin:28px 0 12px;font-size:17px;font-weight:700}
@media(max-width:720px){.grid2{grid-template-columns:1fr}}
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


def render_items(items, prefix, labels=None, limits=None):
    """Карточка позиции кабинета. Подписи и лимиты полей задаёт секция:
    у объявлений это «Заголовок 56 / Описание 81», у акций — «Анонс 70 /
    Описание 200», у витрины описания нет вовсе. Пустые поля не рисуем."""
    labels = labels or {}
    limits = limits or {}
    lt = labels.get('title', 'Заголовок')
    ld = labels.get('desc', 'Описание')
    nt, nd = limits.get('title', 56), limits.get('desc', 81)
    out = []
    for i, it in enumerate(items, 1):
        price = html.escape(it['price']) if it['price'] else '<i>оставить пустым</i>'
        tail = ('<div class="f2">'
                f'<div class="f"><span class="f__k">Цена</span><div class="f__v" data-copy>{price}</div></div>'
                f'<div class="f"><span class="f__k">Ссылка</span><div class="f__v" data-copy>{it["link"]}</div></div>'
                '</div>') if it.get('link') else ''
        desc = (f'<div class="f"><span class="f__k">{ld} <em>{len(it["desc"])}/{nd}</em></span>'
                f'<div class="f__v" data-copy>{html.escape(it["desc"])}</div></div>'
                if it.get('desc') else '')
        out.append(f'''
<article class="ad">
  <div class="ad__num">{i}</div>
  <div class="ad__pic">
    <img src="{it['img']}" alt="" loading="lazy">
    <button class="dl" data-dl="{it['img']}" data-name="{prefix}-{it['key']}.jpg">Скачать картинку</button>
  </div>
  <div>
    <div class="f"><span class="f__k">{lt} <em>{len(it['title'])}/{nt}</em></span>
      <div class="f__v" data-copy>{html.escape(it['title'])}</div></div>
    {desc}
    {tail}
  </div>
</article>''')
    return ''.join(out)


def load_promo(repo):
    """Акции и витрина — материалы, собранные раньше и сведённые в манифест."""
    p = os.path.join(ROOT, repo, '_materials', 'yb-promo', 'promo.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None


def load_stories(repo):
    """Истории (сторис) — линейки, собранные раньше и перенесённые с Диска."""
    p = os.path.join(ROOT, repo, '_materials', 'yb-stories', 'stories.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None


def load_posts(repo):
    p = os.path.join(ROOT, repo, '_materials', 'yb-posts', 'posts.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None


def render_posts(items, prefix):
    """Публикация = текст + до 4 картинок. Текст копируется целиком по клику."""
    out = []
    for it in items:
        gal = ''.join(
            f'<figure><img src="{u}" alt="" loading="lazy">'
            f'<button class="dl" data-dl="{u}" data-name="{prefix}-{it["key"]}-{i}.jpg">Скачать</button>'
            f'</figure>' for i, u in enumerate(it['imgs'], 1))
        out.append(
            '<article class="post">'
            f'<h3>{html.escape(it["title"])} <span>{it["len"]} / 3000 символов</span></h3>'
            f'<div class="post__gal">{gal}</div>'
            f'<div class="post__txt" data-copy>{html.escape(it["text"])}</div>'
            '</article>')
    return ''.join(out)


def checklist(data, posts, promo=None, stories=None):
    """Что уже есть в кабинете и что осталось — чтобы ничего не потерялось."""
    ads = sum(len(s['items']) for s in data['sections']) if data else 0
    rows = [
        ('Свои объявления', f'{ads} готово' if ads else 'нет', bool(ads)),
        ('Публикации', f'{len(posts["items"])} готово' if posts else 'нет', bool(posts)),
        ('Товары и услуги', 'YML-фид на сайте, автозагрузка по ссылке', True),
        ('Акции', f'{len(promo["sections"][0]["items"])} карточек готово'
         if promo else 'состав — с promotions.html сайта', bool(promo)),
        ('Витрина', f'{len(promo["sections"][1]["items"])} позиций готово'
         if promo else 'позиции — с ceny.html', bool(promo)),
        ('Истории', f'{len(stories["items"])} собрано, слайды на странице'
         if stories else 'линейка v1 — файлы на Google Диске', bool(stories)),
        ('Фотографии карточки', 'реальные фото клиники', None),
    ]
    li = ''.join(
        f'<li><b>{t}</b> — {v}</li>' for t, v, _ in rows)
    return li


def build():
    tabs, panes = [], []
    for cid, name, city, repo in CLINICS:
        data = load(repo)
        posts = load_posts(repo)
        promo = load_promo(repo)
        stories = load_stories(repo)
        n = sum(len(s['items']) for s in data['sections']) if data else 0
        n += len(posts['items']) if posts else 0
        n += sum(len(s['items']) for s in promo['sections']) if promo else 0
        n += len(stories['items']) if stories else 0
        tabs.append(f'<button class="tab" data-id="{cid}">{name} <i>{city}'
                    + (f' · {n}' if n else ' · нет материалов') + '</i></button>')
        b = (data or {}).get('brand', {'accent': '#4b5563', 'bg': '#fff',
                                       'ink': '#1d2226', 'line': '#e3e6ea'})
        head = (f'<div class="hd"><h2>{name} — {city}</h2>'
                + (f'<a href="{data["site"]}" target="_blank" rel="noopener">{data["site"]}</a>' if data else '')
                + '</div>')
        if not data and not posts and not promo and not stories:
            # объявлений и публикаций ещё нет — но материалы с Диска показываем,
            # иначе вкладка выглядит пустой при живом архиве
            body = ('<div class="empty">Объявления и публикации для этой клиники ещё не собраны: '
                    'в репозитории лежат только скрипты и реестры. Скажите — соберу такой же '
                    'пакет, как у соседних клиник. Ниже — материалы, сделанные раньше.</div>')
            if promo:
                for sec in promo['sections']:
                    body += f'<div class="sec">{html.escape(sec["title"])}</div>'
                    body += f'<div class="note">{html.escape(sec.get("note", ""))}</div>'
                    body += render_items(sec['items'], cid,
                                         sec.get('labels'), sec.get('limits'))
            if DRIVE.get(cid):
                body += '<div class="sec">Готовые материалы на Google Диске</div><div class="grid2">'
                for title, path, what in DRIVE[cid]:
                    url = ('https://drive.google.com/' +
                           ('drive/folders/' + path.split('/')[1] if path.startswith('folder/')
                            else path + '/edit'))
                    body += (f'<div class="card"><h4><a href="{url}" target="_blank" '
                             f'rel="noopener">{html.escape(title)}</a></h4>'
                             f'<ul><li>{html.escape(what)}</li></ul></div>')
                body += '</div>'
        else:
            site = data['site'] if data else ''
            body = ('<div class="grid2">'
                    '<div class="card"><h4>Что уже готово к заливке</h4><ul>'
                    + checklist(data, posts, promo, stories) + '</ul></div>'
                    '<div class="card"><h4>Яндекс Директ</h4><ul>'
                    '<li>Метрика подключена, 6 целей заведены: <b>lead_submit</b>, call_click, '
                    'whatsapp_click, telegram_click, modal_open, form_start</li>'
                    '<li>Ключевая цель для оптимизации — <b>lead_submit</b> (+ call_click вторым весом)</li>'
                    '<li>Тексты объявлений ниже подходят и для Директа: заголовок ≤56 укладывается '
                    'в лимит Директа, описание расширяется до 81</li>'
                    '<li>Посадочные — те же ссылки, что в карточках, UTM подставляются автоматически '
                    'и уходят в заявку</li>'
                    '<li>Дисклеймер о противопоказаниях на креативах обязателен — он уже впечатан</li>'
                    '</ul></div></div>')
            if data:
                for s in data['sections']:
                    body += f'<div class="sec">{html.escape(s["title"])}</div>'
                    body += (f'<div class="note">{html.escape(s.get("note",""))}<br>'
                             'В поле «Цена» — только число, «от» кабинет не принимает; в заголовке цену '
                             'не дублируем. Срок размещения не ставим — объявления вечные.</div>')
                    body += render_items(s['items'], cid)
            if promo:
                for sec in promo['sections']:
                    body += f'<div class="sec">{html.escape(sec["title"])}</div>'
                    body += f'<div class="note">{html.escape(sec.get("note", ""))}</div>'
                    body += render_items(sec['items'], cid,
                                         sec.get('labels'), sec.get('limits'))
            if stories:
                body += '<div class="sec">Истории (сторис)</div>'
                body += ('<div class="note">Формат 1080×1920. В кабинете у истории свои поля: '
                         'название ≤15 символов и текст кнопки ≤15 — они указаны в каждой карточке. '
                         'Самая свежая история показывается первой, поэтому сильнейшую тему '
                         'заливаем последней. ⚠️ Фото «до/после» в сторис Яндекс отклоняет.</div>')
                for it in stories['items']:
                    gal = ''.join(
                        f'<figure><img src="{u}" alt="" loading="lazy">'
                        f'<button class="dl" data-dl="{u}" data-name="{cid}-{it["key"]}-{i}.jpg">'
                        f'Скачать</button></figure>' for i, u in enumerate(it['imgs'], 1))
                    body += ('<article class="post">'
                             f'<h3>{html.escape(it["title"])} '
                             f'<span>{len(it["imgs"])} слайда · название {len(it["title"])}/15 · '
                             f'кнопка «{html.escape(it["btn"])}» {len(it["btn"])}/15</span></h3>'
                             f'<div class="post__gal">{gal}</div>'
                             f'<div class="f"><span class="f__k">О чём история</span>'
                             f'<div class="f__v">{html.escape(it["about"])}</div></div>'
                             f'<div class="f"><span class="f__k">Ссылка кнопки</span>'
                             f'<div class="f__v" data-copy>{it["link"]}</div></div>'
                             '</article>')
            if DRIVE.get(cid):
                body += '<div class="sec">Готовые материалы на Google Диске</div>'
                body += ('<div class="note">Собрано раньше и в репозиториях не хранится — '
                         'открывается прямо на Диске. Скажите, какие из них нужны на этой '
                         'странице с превью и кнопкой скачивания, — перенесу.</div>'
                         '<div class="grid2">')
                for title, path, what in DRIVE[cid]:
                    url = ('https://drive.google.com/' +
                           ('drive/folders/' + path.split('/')[1] if path.startswith('folder/')
                            else path.replace('document/d/', 'document/d/') + '/edit'))
                    body += (f'<div class="card"><h4><a href="{url}" target="_blank" '
                             f'rel="noopener">{html.escape(title)}</a></h4>'
                             f'<ul><li>{html.escape(what)}</li></ul></div>')
                body += '</div>'
            if posts:
                body += '<div class="sec">Публикации</div>'
                body += ('<div class="note">Публикация — новость клиники, а не реклама: без дат и сезонов, '
                         'чтобы не устаревала. Лимит 3000 символов. Самая свежая показывается первой → '
                         'самую сильную тему заливаем последней. Публиковать хотя бы раз в месяц: '
                         'это влияет на локальное ранжирование карточки.</div>')
                body += render_posts(posts['items'], cid)
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
