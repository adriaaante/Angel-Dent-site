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

**Формат фото в портфолио (важно — единый для всех работ)**:
Сетка карточек (`.pf-img`) показывает фото в соотношении **4:3** через
`object-fit: cover`. Все «обычные» фото портфолио — ровно `1200×896`
(4:3), поэтому заполняют плитку без пустых полей и без обрезки.

Если исходник **другого соотношения** (например, широкий внутриротовой
снимок), делаем **две версии**, чтобы и плитка была заполнена, и в
лайтбоксе фото показывалось целиком:
1. **Превью для сетки** — кадрируем по центру до 4:3, имя
   `<slug>-<кейс>.webp`. На него ссылаются поля `before`/`after`.
2. **Полная версия для лайтбокса** — необрезанная, имя
   `<slug>-<кейс>-full.webp`. На неё ссылаются поля
   `beforeFull`/`afterFull` (в `openLightbox` стоит `beforeFull || before`,
   так что для 4:3-фото эти поля не нужны — поведение прежнее).
   «До» и «После» приводим к **одному размеру** (общий холст, недостающее
   добиваем белым — в белом лайтбоксе поля не видны), чтобы пара
   смотрелась ровно.

Обе версии (и `_originals`, и `-full` оригинал) кладём в `_originals/` и
прогоняем через `apply-watermark.py` — знак везде остаётся в правом нижнем
углу. Пример готовой работы с двумя версиями: кейс MARPE у `drobkova`
в `assets/js/portfolio.js`.

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

## Яндекс.Метрика и цели для Директа

Счётчик `109369174` подключён в `<head>` **каждой** HTML-страницы
(если добавляешь новую — копируй блок `<!-- Yandex.Metrika counter -->`).
Параметры: webvisor, clickmap, trackLinks, accurateTrackBounce.

Программные цели (все определены в `assets/js/main.js` через helper
`trackGoal()`). Имена в кабинете Метрики должны быть **точно такие же**
(Настройка счётчика → Цели → JavaScript-событие, поле «Идентификатор»):

| Цель             | Тип    | Когда срабатывает                                  |
|------------------|--------|----------------------------------------------------|
| `lead_submit`    | макро  | Форма заявки успешно отправлена (200 от lead.php)  |
| `call_click`     | макро  | Клик по любой `tel:`-ссылке (шапка/футер/FAB/тело) |
| `whatsapp_click` | макро  | Клик по ссылке `wa.me/...`                         |
| `telegram_click` | макро  | Клик по ссылке `t.me/...`                          |
| `modal_open`     | микро  | Открытие модалки записи (`[data-modal-open]`)      |
| `form_start`     | микро  | Первый фокус в поле формы заявки (одноразово)     |

Каждая цель передаёт параметр `source` (`header` / `footer` / `fab` /
`modal` / `content`) — в Метрике видно в «Параметрах визитов», какой
блок страницы конвертирует лучше.

UTM-метки и `yclid` (клик-ID Директа) запоминаются в `sessionStorage`
при первом заходе и пробрасываются в `sendLead()` как поля `_utm_*`,
`_yclid`, `_gclid`, `_referrer`. `api/lead.php` выводит их в
Telegram-сообщение блоком «📊 Источник».

Для оптимизации кампаний Директа по конверсиям:
1. Завести в кабинете Метрики все 6 целей с теми же идентификаторами.
2. В кабинете Метрики дать доступ Директу (Настройка → Доступ).
3. В Директе выбрать `lead_submit` как ключевую цель (или составную:
   `lead_submit` + `call_click` с разными весами).
4. Если будут офлайн-конверсии — Метрика поддерживает загрузку по
   `yclid`, который сейчас попадает в Telegram-заявку.

## Форма заявки → PHP-прокси → Telegram Bot

Поток заявки в две стадии, токена бота в браузерном JS **нет**:

```
[браузер]  POST /api/lead.php  →  [reg.ru]  curl → api.telegram.org
 main.js (sendLead)               api/lead.php             ↑
                                       │           токен лежит здесь
                                       │              (config.php)
```

- `assets/js/main.js` функция `sendLead` шлёт `FormData` POST'ом на
  `/api/lead.php` (свой же домен). Помимо полей формы кладёт `_page`,
  `_referrer` и `_utm_*` / `_yclid` / `_gclid` из sessionStorage.
  Метрика-цель `lead_submit` дёргается при успехе (см. раздел «Цели»).
- `api/lead.php` парсит поля по словарю `name/phone/service/message`,
  собирает Markdown-сообщение и серверной curl-сессией шлёт в Telegram
  API. Honeypot-поле `company` (если придёт непустым — молча игнорим).
- Токен и chat_id — в `api/config.php`, **в репо его нет** (`.gitignore`).
  Генерируется автоматически из `scripts/.deploy.env` при каждом запуске
  `scripts/deploy.sh` (см. раздел «Деплой»).
- `api/.htaccess` дополнительно блокирует прямое скачивание `config.php`
  через браузер на случай, если упадёт PHP-обработчик.

Текущий `TELEGRAM_CHAT_ID = -5176309139` (отрицательный = группа).

Маска телефона (`+7 (XXX) XXX-XX-XX`) — `maskPhone` в `main.js`, вешается
на все `input[type="tel"]`. Валидация — только нативная HTML5 (`required`).
Уведомление «Спасибо» — блок `[data-form-success]` в каждой форме,
добавляется класс `is-active`; в модалке очищается при закрытии
(`closeModal` → снимает `is-active`).

**Если бот перестал отвечать или начался спам**: @BotFather → `/mybots`
→ выбрать → `Revoke current token` → новый токен в `scripts/.deploy.env`
→ `./scripts/deploy.sh`. В JS / репо ничего менять не надо.

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

Деплой идёт **с самого сервера**, не с локальной машины. Репозиторий
склонирован на reg.ru в `~/Angel-Dent-site/`, скрипт делает `git pull`
и `rsync` из репо в `~/www/angel-denta.ru/` (это публичная папка
Apache, то, что отдаётся посетителям).

Скрипт: `scripts/deploy.sh` в репо. На сервере существует симлинк
`~/deploy.sh → ~/Angel-Dent-site/scripts/deploy.sh`, поэтому любая
правка скрипта в git автоматом «обновляется» на сервере после
`git pull` — отдельно поддерживать ничего не надо.

Запуск из Shell-клиента ISPmanager
(<https://server292.hosting.reg.ru:1500/> → раздел «Shell-клиент»):

```
~/deploy.sh           # выкатить
~/deploy.sh --dry     # показать план, ничего не менять
```

Что попадает на хостинг: всё, кроме `.git/`, `.github/`, `.claude/`,
`scripts/`, `CLAUDE.md`, `README.md`, `.gitignore`, оригиналов фото
портфолио (`assets/img/portfolio/_originals/`), внутренних материалов
клиники (`_materials/` — объявления, буклеты, паспорт имплантов) и
`api/config.php.example`.

`api/config.php` (токен Telegram-бота и chat_id) лежит **только на
сервере**, в `.gitignore`. Создаётся один раз вручную при первом
сетапе из `api/config.php.example`, `git pull` его не трогает.
Если перевыпускаете токен — правите `api/config.php` прямо на сервере
через Shell-клиент или файловый менеджер ISPmanager.

**Из этого контейнера деплоить не получится** — нет сетевого доступа
к reg.ru, выкладывает владелец через Shell-клиент.

**Первичный сетап сервера** (если когда-нибудь придётся повторить):
1. SSH/Shell-клиент → `cd ~`
2. `git clone https://github.com/adriaaante/angel-dent-site.git Angel-Dent-site`
3. Скопировать шаблон конфига и заполнить токен:
   `cp Angel-Dent-site/api/config.php.example Angel-Dent-site/api/config.php`
   и отредактировать `Angel-Dent-site/api/config.php`.
4. Симлинк короткой команды: `ln -s ~/Angel-Dent-site/scripts/deploy.sh ~/deploy.sh`
5. `~/deploy.sh --dry` (посмотреть план) → `~/deploy.sh` (выкатить).

## Что НЕ нужно делать без явной просьбы

- Не править токен/chat_id Telegram-бота (рабочий канал заявок).
- Не пересоздавать водмаркнутые `assets/img/portfolio/*.webp` руками —
  только через `scripts/apply-watermark.py` из `_originals/`.
- Не удалять плейсхолдеры в `index.html:493` и `doctors/index.html:104`
  (`assets/img/doctors/placeholder.svg`) — это намеренные заглушки
  для «Все врачи клиники» и для рентгенолога без фото.
- Не пушить только в `claude/gifted-cannon-xApI7` — забыть про `main` =
  правка не доедет до прода.
