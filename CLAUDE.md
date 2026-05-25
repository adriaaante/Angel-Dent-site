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
