<?php
// Отдача бланка из files/ — только после входа по PIN.
// Сама папка закрыта .htaccess, поэтому прямой ссылки на .docx не существует.
declare(strict_types=1);
session_start();

if (empty($_SESSION['docs_ok'])) {
    http_response_code(403);
    header('Content-Type: text/plain; charset=utf-8');
    echo 'Нужно войти по коду доступа.';
    exit;
}

$root = realpath(__DIR__ . '/files');
$rel = (string)($_GET['f'] ?? '');
$path = realpath($root . '/' . $rel);

// realpath разворачивает «..», поэтому достаточно проверить, что файл
// действительно лежит внутри files/ — выйти за неё нельзя.
if ($path === false || strncmp($path, $root . DIRECTORY_SEPARATOR, strlen($root) + 1) !== 0
        || !is_file($path) || basename($path) === 'page.html'
        || basename($path) === '.htaccess') {
    http_response_code(404);
    header('Content-Type: text/plain; charset=utf-8');
    echo 'Файл не найден.';
    exit;
}

$types = [
    'docx' => 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'pdf'  => 'application/pdf',
    'zip'  => 'application/zip',
];
$ext = strtolower(pathinfo($path, PATHINFO_EXTENSION));
if (!isset($types[$ext])) {
    http_response_code(404);
    echo 'Файл не найден.';
    exit;
}

// inline=1 — открыть PDF во вкладке (оттуда печатают), иначе скачивание.
$inline = ($ext === 'pdf') && (($_GET['inline'] ?? '') === '1');
$name = basename($path);

header('Content-Type: ' . $types[$ext]);
header('Content-Length: ' . filesize($path));
// Имя файла кириллицей: современные браузеры берут filename*, старым
// оставляем латинскую подстраховку — иначе они сохраняют «файл без имени».
$ascii = preg_replace('/[^A-Za-z0-9._-]+/', '-', $name);
$ascii = trim($ascii, '-') !== '' ? trim($ascii, '-') : ('document.' . $ext);
header('Content-Disposition: ' . ($inline ? 'inline' : 'attachment')
    . '; filename="' . $ascii . '"'
    . "; filename*=UTF-8''" . rawurlencode($name));
header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: private, max-age=300');
readfile($path);
