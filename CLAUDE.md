# Angel-Dent — заметки для агента

## Водяной знак на фото портфолио

Все клинические фото «до/после» в портфолио врачей должны иметь водяной
знак клиники — чтобы фото нельзя было утащить с сайта без следа.

**Файловая раскладка**:
- `assets/img/watermark.png` — мастер-копия знака (RGBA, прозрачный фон).
- `assets/img/portfolio/_originals/<name>.webp` — оригиналы без знака.
  Источник правды, **никогда не отображаются** на сайте.
- `assets/img/portfolio/<name>.webp` — водмаркнутые версии, на которые
  ссылается `assets/js/portfolio.js`.

**Как добавить новое фото в портфолио**:
1. Положить оригинал в `assets/img/portfolio/_originals/<имя>.webp`.
2. Запустить: `python3 scripts/apply-watermark.py <имя>.webp`
   (без аргументов — обработает все оригиналы; идемпотентно, т.к. всегда
   читает из `_originals/`).
3. Закоммитить и оригинал, и водмаркнутую версию.

Параметры знака (см. `scripts/apply-watermark.py`): 32% ширины фото,
правый нижний угол, прозрачность 75%.

## Google Drive — у меня есть прямой доступ

В этом окружении подключён MCP-сервер Google Drive владельца репо
(`adriaaante@gmail.com`). Не надо просить меня «куда положить файл»
или ждать, пока я не смогу скачать с `drive.google.com` — я качаю
напрямую через MCP. Просто пришлите ссылку или название файла.

Инструменты (префикс `mcp__1624bf30-03e8-412d-a7be-4be3657f5851__`):
- `search_files` — поиск по title/fullText/parentId/mimeType/owner.
- `list_recent_files` — последние изменённые (`recency` / `lastModified` /
  `lastModifiedByMe`).
- `get_file_metadata` — метаданные по `fileId`.
- `download_file_content` — содержимое в base64 (для бинарей сохранять
  результат в файл и декодировать; для Google-нативных типов нужен
  `exportMimeType`).
- `read_file_content` — текстовое представление (для документов).

Папка клиники в Drive: «Ангел Дент»
(`fileId = 1d-C5xkYolyn0vsiZZnQgvgTtBwFxWEwV`).
Водяной знак: «Водяной знак.png»
(`fileId = 1huMLYbATwyCIV61nD-rIJG6yVsvM6Gws`).

Типичный паттерн скачать бинарь по ссылке вида
`https://drive.google.com/file/d/<ID>/view`:
1. Достать `<ID>` из URL.
2. `get_file_metadata(fileId=<ID>)` — проверить `mimeType` и размер.
3. `download_file_content(fileId=<ID>)` — придёт base64 (если файл
   крупный, harness сохранит его в tool-results файл).
4. Python: `base64.b64decode(payload['content'])` → записать в нужное
   место в репо.

## Контакты и соцсети клиники

Единственный источник правды (если правят — править во всех местах):
- Телефон: **+7 (910) 458-88-08** (`tel:+79104588808`)
- Адрес: **МО, г. Реутов, ул. Победы, 22** (10 мин от м. Новокосино)
- График: **ежедневно 10:00–20:00**, без выходных
- Email: **angel.dent@bk.ru**
- Домен: **angel-denta.ru**
- Единый ник во всех каналах — **`stomangeldent`**:
  - Telegram — `https://t.me/stomangeldent`
  - VK — `https://vk.com/stomangeldent`
  - WhatsApp — `https://wa.me/79104588808`
- Дзен — `https://dzen.ru/angeldent` (другой ник, исторически)

Места, где эти данные обычно меняют: `index.html`, `contacts.html`,
футер всех страниц, FAB-виджет в конце `<body>`, JSON-LD
`LocalBusiness` в `<head>` главной, топбар на главной.

## Форма заявки → Telegram Bot (не Web3Forms)

Заявки уходят **прямым `fetch` на Telegram Bot API** из `assets/js/main.js`
(функция `sendTelegram`, строки ~44–108). Никакого бэкенда и сторонних
форм-сервисов нет. Метрика-цель `lead_submit` дёргается при успехе
(`ym(109369174, 'reachGoal', 'lead_submit')`).

Зашиты в JS:
- `TELEGRAM_BOT_TOKEN` — токен бота от @BotFather
- `TELEGRAM_CHAT_ID = '-5176309139'` — ID группы (отрицательный = группа)
- Шаблон сообщения берёт поля формы по словарю `FIELD_LABELS`
  (`name → Имя`, `phone → Телефон`, `service → Услуга`,
  `message → Комментарий`), добавляет URL страницы.

**Известный риск**: токен лежит в публичном JS, его может выдрать любой
посетитель. Если начнётся спам в группу — единственное лечение через
@BotFather: `/revoke` старого токена и перевыпуск + замена в `main.js`.
Долгосрочно правильно — проксировать отправку через бэкенд (своя
function на хостинге или Cloudflare Worker), но это отдельная задача.

Маска телефона (`+7 (XXX) XXX-XX-XX`) — `maskPhone` в `main.js`, вешается
на все `input[type="tel"]`. Валидация — только нативная HTML5 (`required`).
Уведомление «Спасибо» — блок `[data-form-success]` в каждой форме,
добавляется класс `is-active`; в модалке очищается при закрытии
(`closeModal` → снимает `is-active`).

## Workflow пушей

Разработка идёт на ветке **`claude/gifted-cannon-xApI7`** (см. инструкции
сессии). После коммита **пушим в обе ветки сразу** — фичевую и
`main` фастфорвардом:

```
git push -u origin claude/gifted-cannon-xApI7
git push origin claude/gifted-cannon-xApI7:main
```

Без второй команды правка не доедет до прода. Это договорённость
владельца — не «по умолчанию», поэтому в новой сессии надо помнить.
PR не создаём, если не попросили явно.

## Структура сайта и slug-и

Плоская статика — никакого шаблонизатора. **Массовая правка хедера /
футера / FAB = трогаем каждый HTML-файл** (или пишем `sed`/Python-патч
в `scripts/`).

Корень — все «листовые» страницы:
`index.html`, `about.html`, `promotions.html`, `reviews.html`,
`contacts.html`, `legal.html`, `oferta.html`, `privacy.html`,
`consent.html`, `cookies.html`, `404.html`.

Подпапки:
- `services/` — `index.html` + страницы услуг: `implantaciya`,
  `ortodontiya`, `terapiya`, `hirurgiya`, `protezirovanie`,
  `parodontologiya`, `viniry`, `gigiena`, `detskaya`.
- `doctors/` — `index.html` + страницы врачей по slug-ам:
  - `drobkova` — Дробкова Кристина Олеговна (главврач, ортодонт)
  - `geworkyan` — Геворкян Санатрук Иванович (ген. директор, хирург, имплантолог)
  - `rustamli` — Рустамли Руслан Рустамович (хирург, имплантолог)
  - `rustamov` — Рустамов Эмиль Дилгамович (ортопед)
  - `smolyakova` — Смолякова Радана Сергеевна (терапевт)
- `blog/` — `index.html` + 6 статей.

Те же slug-и врачей — ключи объекта `window.AD_PORTFOLIO` в
`assets/js/portfolio.js` (там данные «до/после» для каждого).

## FAB-виджет (WhatsApp / Telegram / Позвонить)

Разметка `<div class="fab" data-fab>…</div>` должна быть **на каждой
странице сайта** — обычно в самом конце `<body>`, рядом со скриптами.
Без неё виджет не покажется. Инициализация лежит в `main.js`,
оборачивается в `DOMContentLoaded`, поэтому порядок «FAB до скрипта /
после скрипта» не важен — можно ставить где удобно.

Если добавляешь новую страницу: скопируй блок FAB с любой существующей
(например, `index.html` ~ строка 820) или прогони `scripts/inject-upgrades.py`
(он умеет вставлять FAB + progress-bar + preconnect идемпотентно).

## Деплой на reg.ru

Когда настроим — здесь будет команда. Сейчас деплой ручной (`scp`/FTP
с машины владельца). Запланировано: `scripts/deploy.sh` с конфигом в
`scripts/.deploy.env` (gitignored). Из этого контейнера деплоить не
получится — нет сетевого доступа к reg.ru, выкладывает владелец.

## Что НЕ нужно делать без явной просьбы

- Не править токен/chat_id Telegram-бота (рабочий канал заявок).
- Не пересоздавать водмаркнутые `assets/img/portfolio/*.webp` руками —
  только через `scripts/apply-watermark.py` из `_originals/`.
- Не удалять плейсхолдеры в `index.html:493` и `doctors/index.html:104`
  (`assets/img/doctors/placeholder.svg`) — это намеренные заглушки
  для «Все врачи клиники» и для рентгенолога без фото.
- Не пушить только в `claude/gifted-cannon-xApI7` — забыть про `main` =
  правка не доедет до прода.
