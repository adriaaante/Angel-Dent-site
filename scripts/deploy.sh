#!/usr/bin/env bash
# Angel-Dent — заливка сайта на хостинг reg.ru.
#
# Использование:
#   ./scripts/deploy.sh                  выкатить
#   ./scripts/deploy.sh --dry            показать, что выкатится, ничего не отправлять
#   ./scripts/deploy.sh --with-delete    выкатить и удалить на хостинге
#                                        файлы, которых нет в репо
#
# Перед первым запуском:
#   cp scripts/.deploy.env.example scripts/.deploy.env
#   $EDITOR scripts/.deploy.env   # заполнить хост, логин, пароль, путь
#                                 # и TELEGRAM_BOT_TOKEN (берётся текущий)
#
# Что делает:
#   1. Генерирует api/config.php из переменных .deploy.env (токен и chat_id).
#      Сам api/config.php в .gitignore — в репо не попадает.
#   2. Заливает всё на хостинг (rsync через SSH, либо lftp mirror через
#      FTP/SFTP) — выбор по DEPLOY_PROTO.
#   3. Из заливки исключены служебные вещи: .git, .github, .claude,
#      scripts/, CLAUDE.md, README.md, мастер-фото портфолио из _originals/.

set -euo pipefail

cd "$(dirname "$0")/.."

ENV_FILE="scripts/.deploy.env"
if [ ! -f "$ENV_FILE" ]; then
    cat >&2 <<EOF
✗ Не найден $ENV_FILE.
  Скопируйте scripts/.deploy.env.example в scripts/.deploy.env
  и заполните параметры хостинга и Telegram-бота.
EOF
    exit 1
fi

set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

require_var() {
    local name=$1
    if [ -z "${!name:-}" ]; then
        echo "✗ В $ENV_FILE не задано $name" >&2
        exit 1
    fi
}

require_var DEPLOY_PROTO
require_var REG_HOST
require_var REG_USER
require_var REG_PATH
require_var TELEGRAM_BOT_TOKEN
require_var TELEGRAM_CHAT_ID

DRY=0
WITH_DELETE=0
for arg in "$@"; do
    case "$arg" in
        --dry|--dry-run) DRY=1 ;;
        --with-delete)   WITH_DELETE=1 ;;
        -h|--help)
            sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *)
            echo "Неизвестный флаг: $arg (см. --help)" >&2
            exit 2
            ;;
    esac
done

# --- Готовим api/config.php (его в .gitignore, поэтому регенерируем каждый раз) ---
php_escape() {
    # Экранируем одинарные кавычки для PHP-литералов '...'.
    printf '%s' "$1" | sed "s/\\\\/\\\\\\\\/g; s/'/\\\\'/g"
}

TG_TOKEN_ESC=$(php_escape "$TELEGRAM_BOT_TOKEN")
TG_CHAT_ESC=$(php_escape "$TELEGRAM_CHAT_ID")

cat > api/config.php <<PHP
<?php
// Сгенерировано scripts/deploy.sh из scripts/.deploy.env.
// Не коммитить, не редактировать руками — перезатрётся при следующем деплое.

define('TELEGRAM_BOT_TOKEN', '${TG_TOKEN_ESC}');
define('TELEGRAM_CHAT_ID',  '${TG_CHAT_ESC}');
PHP

echo "→ api/config.php сгенерирован."

# --- Список исключений (одинаковый для rsync и lftp) ---
EXCLUDES=(
    '.git'
    '.github'
    '.claude'
    'scripts'
    'CLAUDE.md'
    'README.md'
    '.gitignore'
    '.deploy.env'
    'api/config.php.example'
    'assets/img/portfolio/_originals'
    'preview.html'
    '.DS_Store'
    'Thumbs.db'
)

case "$DEPLOY_PROTO" in
    ssh)
        PORT="${REG_PORT:-22}"
        RSYNC=(rsync -avz --human-readable)
        [ "$DRY" -eq 1 ]         && RSYNC+=(--dry-run --itemize-changes)
        [ "$WITH_DELETE" -eq 1 ] && RSYNC+=(--delete)
        for ex in "${EXCLUDES[@]}"; do RSYNC+=("--exclude=$ex"); done
        RSYNC+=(-e "ssh -p $PORT")
        RSYNC+=(./ "${REG_USER}@${REG_HOST}:${REG_PATH}/")
        echo "→ rsync на ${REG_USER}@${REG_HOST}:${REG_PATH}/ (порт $PORT)"
        "${RSYNC[@]}"
        ;;
    sftp|ftp)
        require_var REG_PASS
        if [ "$DEPLOY_PROTO" = sftp ]; then
            PORT="${REG_PORT:-22}"
            SCHEME=sftp
        else
            PORT="${REG_PORT:-21}"
            SCHEME=ftp
        fi
        if ! command -v lftp >/dev/null 2>&1; then
            echo "✗ Не найден lftp. Установите: brew install lftp / apt install lftp." >&2
            exit 1
        fi

        MIRROR_OPTS=(--reverse --parallel=4 --verbose)
        [ "$DRY" -eq 1 ]         && MIRROR_OPTS+=(--dry-run)
        [ "$WITH_DELETE" -eq 1 ] && MIRROR_OPTS+=(--delete)
        for ex in "${EXCLUDES[@]}"; do
            MIRROR_OPTS+=(--exclude-glob "$ex" --exclude-glob "$ex/*")
        done

        echo "→ lftp ($SCHEME) на ${REG_USER}@${REG_HOST}:${REG_PATH}/ (порт $PORT)"
        LFTP_PASSWORD="$REG_PASS" lftp -u "${REG_USER},$REG_PASS" \
            -p "$PORT" "${SCHEME}://${REG_HOST}" <<LFTP
set ssl:verify-certificate no
set ftp:passive-mode true
set sftp:auto-confirm yes
mirror ${MIRROR_OPTS[*]} . ${REG_PATH}
bye
LFTP
        ;;
    *)
        echo "✗ DEPLOY_PROTO='${DEPLOY_PROTO}' не поддерживается (ssh / sftp / ftp)" >&2
        exit 1
        ;;
esac

if [ "$DRY" -eq 1 ]; then
    echo "✓ Dry-run завершён, ничего не отправлено."
else
    echo "✓ Готово. Сайт обновлён на ${REG_HOST}."
fi
