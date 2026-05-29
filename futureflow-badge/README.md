# Бейдж «Сделано в FutureFlow»

Самодостаточный значок для подвала любого сайта. Не зависит от стилей
проекта — всё (иконка-чип + градиентная надпись) лежит прямо в коде.

## Файлы

- `index.html` — демо-страница: предпросмотр на светлом и тёмном фоне
  + три готовых сниппета с кнопками «Скопировать». **Открой её в браузере
    и просто копируй нужный вариант.**
- `futureflow-badge.svg` — версия-картинка (190×36), если нужен `<img>`.

## Как вставить (быстро)

Скопируй этот блок в любое место страницы — больше ничего подключать
не нужно:

```html
<a href="https://futureflow.ru" target="_blank" rel="noopener" aria-label="Сделано в FutureFlow"
   style="display:inline-flex;align-items:center;gap:8px;padding:7px 14px 7px 11px;border-radius:100px;background:#0f1f3a;border:1px solid rgba(255,255,255,.14);color:rgba(255,255,255,.78);text-decoration:none;font:600 12.5px/1 system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif">
  <svg width="20" height="20" viewBox="0 0 32 32" fill="none" stroke="url(#ffGrad)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <defs><linearGradient id="ffGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c8dcf4"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#f5a623"/></linearGradient></defs>
    <rect x="8" y="8" width="16" height="16" rx="2.5"/>
    <path d="M12 8V4M16 8V4M20 8V4 M12 28V24M16 28V24M20 28V24 M8 12H4M8 16H4M8 20H4 M28 12H24M28 16H24M28 20H24"/>
  </svg>
  <span>Сделано в&nbsp;<span style="font-weight:700;background:linear-gradient(90deg,#c8dcf4,#fff 50%,#f5a623);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent">FutureFlow</span></span>
</a>
```

## Настройка

- **Ссылка** — `href="https://futureflow.ru"`.
- **Фон пилюли** — `background:#0f1f3a` (тёмный универсален; смотрится и на
  светлом, и на тёмном фоне).
- **Цвет надписи** — градиент `linear-gradient(90deg,#c8dcf4,#fff,#f5a623)`.

> Тот же бейдж уже стоит в подвале сайта Angel-Dent (`.ff-credit` в
> `assets/css/styles.css`) — эта папка лишь делает его переносимым.
