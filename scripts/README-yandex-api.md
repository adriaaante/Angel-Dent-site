# Доступ к API Яндекс.Вебмастера и Метрики (для SEO-выгрузки)

Скрипт `scripts/yandex-webmaster.py` тянет из API реальные данные: ИКС,
индексацию, поисковые запросы с позициями, трафик/поведение из Метрики.
Токен в репозитории **не хранится** — читается из переменной окружения.

## Как получить токен (один раз, живёт ~6 мес.)
1. `oauth.yandex.ru/client/new` (под аккаунтом с доступом к Вебмастеру).
2. «Для авторизации пользователей» → платформа «Веб-сервисы»,
   Redirect URI: `https://oauth.yandex.ru/verification_code`.
3. Доступы (Дополнительные): `webmaster:hostinfo` и `metrika:read` (только чтение).
4. Скопировать **ClientID**, затем открыть в браузере:
   `https://oauth.yandex.ru/authorize?response_type=token&client_id=CLIENTID`
   → скопировать `access_token`.

## Куда положить токен (постоянный доступ)
Токен — секрет (как пароль). Задаётся **переменной окружения**
`YANDEX_WEBMASTER_TOKEN` в настройках окружения Claude Code (не в репозиторий!).
Обновить при истечении (ошибка `INVALID_OAUTH_TOKEN` / 401) — повторить п.4.

## Запуск
```
YANDEX_WEBMASTER_TOKEN=xxxx python3 scripts/yandex-webmaster.py
```
Счётчик Метрики зашит в скрипте (`METRIKA_COUNTER = 109369174`).
