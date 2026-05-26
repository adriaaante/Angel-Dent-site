# Angel-Dent — сайт клиники

Статический сайт стоматологии «Ангел-Дент» (Реутов, ул. Победы 22).
Чистый HTML + CSS + JS, без сборки и зависимостей. Заливается куда
угодно — reg.ru, Beget, Cloudflare Pages и т.п.

Подробные заметки для разработки (как устроен сайт, контакты, формы,
структура, slug-и врачей, workflow пушей) — в [`CLAUDE.md`](CLAUDE.md).
Документ автоматически подхватывается агентом при старте сессии,
обновляйте его, если правите архитектурные вещи.

## Локальный запуск

```bash
python3 -m http.server 8080
# http://localhost:8080
```

## Что важно держать в актуальном состоянии

- **Реквизиты в подвале каждой страницы** — ИНН, ОГРН, лицензия. Сейчас
  стоят значения из договора; если что-то меняется, искать по числу
  (`5012090909` / `1145012004000` / `ЛО-50-01-009999`).
- **Цены** в прайс-таблицах на страницах услуг (`services/*.html`) и в
  карточках на главной/в акциях.
- **Метрика** — Яндекс.Метрика подключена с ID `109369174` в `<head>` каждой
  страницы и в `main.js` (`reachGoal('lead_submit')`).

## Деплой

Сейчас — ручной (FTP/SFTP с машины владельца). В планах — `scripts/deploy.sh`
для reg.ru. Подробности появятся в `CLAUDE.md` раздел «Деплой» как только
будет настроен.

Полезно для деплоя:
- 301-редиректы со старого домена `angel-dent.ru` → `angel-denta.ru` и
  со старых URL Tilda (`/hiryrgia`, `/breket`, `/chistka`, …) на новые
  (`/services/hirurgiya.html`, …). Настраивается в `.htaccess` или в
  панели хостинга.
- Файлы `robots.txt` и `sitemap.xml` лежат в корне, дополнительной
  настройки на хостинге не требуют.

## Структура

```
.
├── index.html, about.html, promotions.html, reviews.html, contacts.html,
│   legal.html, oferta.html, privacy.html, consent.html, cookies.html, 404.html
├── services/        — индекс + 9 страниц услуг
├── doctors/         — индекс + 5 страниц врачей (slug-и: drobkova,
│                       geworkyan, rustamli, rustamov, smolyakova)
├── blog/            — индекс + 6 SEO-статей
├── assets/
│   ├── css/styles.css
│   ├── js/main.js, cookies.js, portfolio.js
│   └── img/         — generated/ (фото), doctors/, portfolio/,
│                       watermark.png, favicon.*, logo.*
├── scripts/         — служебные скрипты (см. ниже)
├── .github/workflows/ — GitHub Actions
└── CLAUDE.md          — заметки для агента (источник правды)
```

## Служебные скрипты

| Скрипт | Что делает |
|---|---|
| `scripts/apply-watermark.py` | Применяет водяной знак клиники к фото портфолио из `_originals/`. Идемпотентен, всегда читает из мастер-копий. См. CLAUDE.md. |
| `scripts/prepare-doctor-photo.py` | Обрезает/готовит фото нового врача из сырого исходника. |
| `scripts/inject-upgrades.py` | Идемпотентно добавляет в HTML страницы блок FAB, прогресс-бар чтения, OG-баннер и preconnect-теги. Полезно при добавлении новой страницы. |
| `scripts/sync-higgsfield-images.sh` | Скачивает изображения с Higgsfield CDN в `assets/img/generated/` и патчит абсолютные URL в HTML на локальные. Запускается из GitHub Actions при изменении самого скрипта. |
| `scripts/download-license-from-yadisk.sh` | Качает скан лицензии из Я.Диска в `assets/docs/`. Тоже через GitHub Actions. |

## Лицензия

Контент и дизайн принадлежат ООО «Ангел-Дент». Все права защищены.
