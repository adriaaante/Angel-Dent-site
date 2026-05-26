<?php
/**
 * Angel-Dent — приём заявок с сайта и пересылка в Telegram.
 *
 * Главная задача — не светить токен бота в публичном JS.
 * Браузер шлёт сюда POST с полями формы, PHP уже сам дёргает Telegram
 * API серверной curl-сессией. Токен живёт в api/config.php рядом
 * (его в git нет — заливается через scripts/deploy.sh из локального
 * scripts/.deploy.env).
 */

declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

function reply(int $code, array $body): void {
    http_response_code($code);
    echo json_encode($body, JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    reply(405, ['ok' => false, 'error' => 'method_not_allowed']);
}

$config = __DIR__ . '/config.php';
if (!is_file($config)) {
    reply(500, ['ok' => false, 'error' => 'config_missing']);
}
require $config;

if (!defined('TELEGRAM_BOT_TOKEN') || !defined('TELEGRAM_CHAT_ID')
    || TELEGRAM_BOT_TOKEN === '' || TELEGRAM_CHAT_ID === '') {
    reply(500, ['ok' => false, 'error' => 'config_incomplete']);
}

// Honeypot: поле "company" скрыто от людей, боты его обычно заполняют.
// Если пришло непустым — молча подтверждаем и ничего не шлём.
if (!empty($_POST['company'] ?? '')) {
    reply(200, ['ok' => true]);
}

$labels = [
    'name'    => 'Имя',
    'phone'   => 'Телефон',
    'service' => 'Услуга',
    'message' => 'Комментарий',
];

$lines = ['🦷 *Заявка с сайта Ангел-Дент*', ''];
foreach ($_POST as $key => $value) {
    if ($key === 'company' || $key[0] === '_') continue;
    $value = trim((string)$value);
    if ($value === '') continue;
    $label = $labels[$key] ?? $key;
    // Экранируем markdown-метасимволы, чтобы заявка не сломала форматирование.
    $escaped = preg_replace('/([*_`\[])/u', '\\\\$1', $value);
    $lines[] = '*' . $label . ':* ' . $escaped;
}

$page = trim((string)($_POST['_page'] ?? ''));
if ($page !== '') {
    $lines[] = '';
    $lines[] = '_Страница: ' . preg_replace('/[*_`\[]/u', '', $page) . '_';
}

$payload = json_encode([
    'chat_id'                  => TELEGRAM_CHAT_ID,
    'text'                     => implode("\n", $lines),
    'parse_mode'               => 'Markdown',
    'disable_web_page_preview' => true,
], JSON_UNESCAPED_UNICODE);

$url = 'https://api.telegram.org/bot' . TELEGRAM_BOT_TOKEN . '/sendMessage';
$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => $payload,
    CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
    CURLOPT_TIMEOUT        => 10,
    CURLOPT_CONNECTTIMEOUT => 5,
]);
$response = curl_exec($ch);
$httpCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlErr  = curl_error($ch);
curl_close($ch);

if ($httpCode >= 200 && $httpCode < 300 && $response !== false) {
    $decoded = json_decode($response, true);
    if (is_array($decoded) && !empty($decoded['ok'])) {
        reply(200, ['ok' => true]);
    }
}

// Логируем в error_log, но клиенту деталей не отдаём.
error_log('[angel-dent lead] telegram failed: http=' . $httpCode
    . ' err=' . $curlErr . ' resp=' . substr((string)$response, 0, 500));
reply(502, ['ok' => false, 'error' => 'telegram_unreachable']);
