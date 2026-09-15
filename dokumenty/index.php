<?php
// Страница «Документы клиники» — закрыта PIN-кодом.
//
// Сама страница (маршрут пациента, кнопки скачивания) лежит в
// files/page.html и собирается генератором
// _materials/dogovor-pacienta/package.py. Папка files/ закрыта
// .htaccess — и страница, и бланки отдаются только отсюда, после входа.
declare(strict_types=1);
require __DIR__ . '/config.php';

session_start();

$error = '';
$now = time();

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $pin = preg_replace('/\D+/', '', (string)($_POST['pin'] ?? ''));
    $tries = (int)($_SESSION['docs_tries'] ?? 0);
    $locked = (int)($_SESSION['docs_locked_until'] ?? 0);

    if ($locked > $now) {
        $error = 'Слишком много попыток. Подождите ' . ($locked - $now) . ' с.';
    } elseif ($pin !== '' && password_verify($pin, DOCS_PIN_HASH)) {
        session_regenerate_id(true);
        $_SESSION['docs_ok'] = true;
        $_SESSION['docs_tries'] = 0;
        header('Location: ' . strtok($_SERVER['REQUEST_URI'], '?'));
        exit;
    } else {
        $tries++;
        $_SESSION['docs_tries'] = $tries;
        if ($tries >= DOCS_MAX_TRIES) {
            $_SESSION['docs_locked_until'] = $now + DOCS_LOCK_SECONDS;
            $_SESSION['docs_tries'] = 0;
            $error = 'Слишком много попыток. Подождите минуту.';
        } else {
            $error = 'Неверный код. Попробуйте ещё раз.';
        }
    }
}

if (($_GET['exit'] ?? '') === '1') {
    $_SESSION = [];
    session_destroy();
    header('Location: ' . strtok($_SERVER['REQUEST_URI'], '?'));
    exit;
}

header('X-Robots-Tag: noindex, nofollow, noarchive');

if (!empty($_SESSION['docs_ok'])) {
    $page = __DIR__ . '/files/page.html';
    if (is_readable($page)) {
        header('Content-Type: text/html; charset=utf-8');
        readfile($page);
        exit;
    }
    http_response_code(500);
    echo 'Страница ещё не собрана: нет files/page.html.';
    exit;
}
?><!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Документы клиники — вход</title>
<link rel="icon" href="/favicon.ico">
<style>
:root{--ink:#16202b;--muted:#5d6b7a;--line:#e3e9f0;--accent:#1e5fb3;--accent-soft:#eaf2fc}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
     background:linear-gradient(160deg,#f2f7fd 0%,#eaf2fc 45%,#f7fafd 100%);color:var(--ink);
     font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
     padding:24px}
.card{background:#fff;border:1px solid var(--line);border-radius:22px;padding:38px 34px 30px;
      width:100%;max-width:440px;text-align:center;
      box-shadow:0 24px 60px -30px rgba(20,50,90,.35)}
.logo{width:86px;height:86px;object-fit:contain;margin-bottom:14px}
h1{margin:0 0 6px;font-size:22px;letter-spacing:-.02em}
p.sub{margin:0 0 26px;color:var(--muted);font-size:15px}
.pins{display:flex;gap:9px;justify-content:center;margin-bottom:18px}
.pins input{width:48px;height:60px;border:1.5px solid var(--line);border-radius:12px;
            text-align:center;font-size:26px;font-weight:600;color:var(--ink);background:#fbfdff;
            transition:border-color .15s,box-shadow .15s}
.pins input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 4px var(--accent-soft)}
.err{color:#b4231f;font-size:14.5px;min-height:22px;margin:0}
.hint{color:var(--muted);font-size:13.5px;margin:18px 0 0}
form.shake{animation:sh .35s}
@keyframes sh{25%{transform:translateX(-7px)}50%{transform:translateX(7px)}75%{transform:translateX(-4px)}}
@media(max-width:420px){.pins input{width:42px;height:54px;font-size:22px}}
</style>
</head>
<body>
<form class="card" method="post" autocomplete="off" id="gate">
  <img class="logo" src="/assets/img/logo.png" alt="Ангел-Дент">
  <h1>Документы клиники</h1>
  <p class="sub">Стоматология «Ангел-Дент» · служебная страница.<br>Введите код доступа.</p>
  <div class="pins" id="pins">
    <input type="password" inputmode="numeric" maxlength="1" autocomplete="off" aria-label="1">
    <input type="password" inputmode="numeric" maxlength="1" autocomplete="off" aria-label="2">
    <input type="password" inputmode="numeric" maxlength="1" autocomplete="off" aria-label="3">
    <input type="password" inputmode="numeric" maxlength="1" autocomplete="off" aria-label="4">
    <input type="password" inputmode="numeric" maxlength="1" autocomplete="off" aria-label="5">
    <input type="password" inputmode="numeric" maxlength="1" autocomplete="off" aria-label="6">
  </div>
  <input type="hidden" name="pin" id="pin">
  <p class="err"><?= htmlspecialchars($error, ENT_QUOTES, 'UTF-8') ?></p>
  <p class="hint">Страница закрыта от поисковиков. Код — у руководителя клиники.</p>
</form>
<script>
(function(){
  var form=document.getElementById('gate'), hidden=document.getElementById('pin'),
      boxes=[].slice.call(document.querySelectorAll('#pins input'));
  function value(){ return boxes.map(function(b){return b.value;}).join(''); }
  function submit(){
    hidden.value=value();
    if(hidden.value.length===boxes.length) form.submit();   // автовход на последней цифре
  }
  boxes.forEach(function(box,i){
    box.addEventListener('input',function(){
      box.value=box.value.replace(/\D/g,'').slice(0,1);
      if(box.value && i<boxes.length-1) boxes[i+1].focus();
      submit();
    });
    box.addEventListener('keydown',function(e){
      if(e.key==='Backspace' && !box.value && i>0){ boxes[i-1].focus(); boxes[i-1].value=''; e.preventDefault(); }
      if(e.key==='ArrowLeft' && i>0) boxes[i-1].focus();
      if(e.key==='ArrowRight' && i<boxes.length-1) boxes[i+1].focus();
    });
    box.addEventListener('paste',function(e){
      var t=(e.clipboardData||window.clipboardData).getData('text').replace(/\D/g,'');
      if(!t) return;
      e.preventDefault();
      boxes.forEach(function(b,j){ b.value=t[j]||''; });
      boxes[Math.min(t.length,boxes.length)-1].focus();
      submit();
    });
  });
  boxes[0].focus();
  if(document.querySelector('.err').textContent.trim()){
    form.classList.add('shake');
    setTimeout(function(){form.classList.remove('shake');},400);
  }
})();
</script>
</body>
</html>
