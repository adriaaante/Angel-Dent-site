(function () {
  'use strict';

  // Mobile nav toggle
  var burger = document.querySelector('[data-burger]');
  var nav = document.querySelector('[data-nav]');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      nav.classList.toggle('is-open');
    });
  }

  // Phone input mask: +7 (XXX) XXX-XX-XX
  function maskPhone(input) {
    input.addEventListener('input', function (e) {
      var digits = e.target.value.replace(/\D/g, '');
      if (digits.startsWith('8')) digits = '7' + digits.slice(1);
      if (!digits.startsWith('7')) digits = '7' + digits;
      digits = digits.slice(0, 11);
      var out = '+7';
      if (digits.length > 1) out += ' (' + digits.slice(1, 4);
      if (digits.length >= 5) out += ') ' + digits.slice(4, 7);
      if (digits.length >= 8) out += '-' + digits.slice(7, 9);
      if (digits.length >= 10) out += '-' + digits.slice(9, 11);
      e.target.value = out;
    });
    input.addEventListener('focus', function (e) {
      if (!e.target.value) e.target.value = '+7 (';
    });
  }
  document.querySelectorAll('input[type="tel"]').forEach(maskPhone);

  // Lead submission — sent in parallel to e-mail (via Web3Forms) and to
  // a Telegram chat (via Bot API). Either channel succeeding is enough
  // to show "Спасибо!" to the visitor; both failing falls back to the
  // phone number.
  // ---------------------------------------------------------------
  //
  // Setup steps (one-time, ~5 minutes total):
  //
  // 1) E-MAIL — Web3Forms (https://web3forms.com)
  //    • Открыть web3forms.com, ввести e-mail клиники (например info@angel-denta.ru)
  //    • Нажать «Create Access Key» — на почту придёт длинный access_key
  //    • Подставить его ниже в WEB3FORMS_KEY (заменить __WEB3FORMS_KEY__)
  //    • Готово. Письма приходят на тот же e-mail, никакого signup-а
  //
  // 2) TELEGRAM — собственный бот
  //    a. Открыть @BotFather в Telegram → /newbot → дать имя
  //       (например «Ангел-Дент заявки») и username (например
  //       angeldent_leads_bot). Получите BOT_TOKEN вида 1234567890:AAH…
  //       Подставить в TELEGRAM_BOT_TOKEN ниже.
  //    b. Получить CHAT_ID куда отправлять:
  //       • Личный чат: @userinfobot → /start → пришлёт ваш chat_id.
  //         Затем напишите своему боту /start (иначе он не сможет вам
  //         написать первым).
  //       • Группа: добавить бота в группу, написать там любое сообщение,
  //         открыть https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
  //         и найти "chat":{"id":-1001234567890}. Минус — обязательная
  //         часть chat_id супергруппы.
  //       Подставить в TELEGRAM_CHAT_ID ниже.
  //    c. Готово. Заявки летят в Telegram через 1-2 секунды.

  var WEB3FORMS_KEY     = '__WEB3FORMS_KEY__';     // TODO: access_key с web3forms.com
  var TELEGRAM_BOT_TOKEN = '8682361398:AAEkEqOgAIFubhfX8oId7UIk4R0vt13Qd2g'; // TODO: токен от @BotFather
  var TELEGRAM_CHAT_ID   = '8327691755';           // TODO: chat_id куда слать

  var LEAD_ENDPOINT = 'https://api.web3forms.com/submit';
  var TG_ENDPOINT   = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage';

  function sendEmail(form) {
    if (!WEB3FORMS_KEY || WEB3FORMS_KEY.indexOf('__') === 0) return Promise.reject('no key');
    var fd = new FormData(form);
    fd.append('access_key', WEB3FORMS_KEY);
    fd.append('subject', 'Заявка с сайта Ангел-Дент · ' + (location.pathname || '/'));
    fd.append('from_name', 'Сайт angel-denta.ru');
    fd.append('Страница', location.pathname || '/');
    if (document.title) fd.append('Раздел', document.title);
    fd.append('botcheck', ''); // honeypot
    return fetch(LEAD_ENDPOINT, { method: 'POST', body: fd, headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.json().then(function (d) { return r.ok && d && d.success ? d : Promise.reject(d); }); });
  }

  function sendTelegram(form) {
    if (!TELEGRAM_BOT_TOKEN || TELEGRAM_BOT_TOKEN.indexOf('__') === 0) return Promise.reject('no token');
    var fd = new FormData(form);
    var lines = ['🦷 *Заявка с сайта Ангел-Дент*', ''];
    fd.forEach(function (val, key) {
      if (!val) return;
      var label = ({ name: 'Имя', phone: 'Телефон', service: 'Услуга', message: 'Комментарий' })[key] || key;
      lines.push('*' + label + ':* ' + String(val).replace(/[*_`[]/g, '\\$&'));
    });
    lines.push('');
    lines.push('_Страница: ' + (location.pathname || '/') + '_');
    var text = lines.join('\n');
    return fetch(TG_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: TELEGRAM_CHAT_ID, text: text, parse_mode: 'Markdown', disable_web_page_preview: true })
    }).then(function (r) { return r.json().then(function (d) { return d && d.ok ? d : Promise.reject(d); }); });
  }

  document.querySelectorAll('form[data-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var success = form.querySelector('[data-form-success]');
      var submitBtn = form.querySelector('button[type="submit"]');
      var origLabel = submitBtn ? submitBtn.textContent : 'Отправить';

      var done = function (ok, label) {
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = origLabel; }
        if (success) {
          success.textContent = label;
          success.classList.add('is-active');
          setTimeout(function () { success.classList.remove('is-active'); }, 9000);
        }
        if (ok) {
          form.reset();
          if (typeof ym === 'function') { try { ym(100658497, 'reachGoal', 'lead_submit'); } catch (e) {} }
        }
      };

      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Отправляем…'; }

      // Send to both channels in parallel; succeed if at least one returns OK.
      var promises = [
        sendEmail(form).then(function () { return 'email'; }, function (err) { console.warn('[lead] email failed', err); return null; }),
        sendTelegram(form).then(function () { return 'tg'; }, function (err) { console.warn('[lead] telegram failed', err); return null; })
      ];

      Promise.all(promises).then(function (results) {
        var anyOk = results.some(Boolean);
        done(anyOk, anyOk
          ? 'Спасибо! Мы перезвоним за 15 минут.'
          : 'Не удалось отправить. Позвоните, пожалуйста: +7 (910) 458-88-08');
      });
    });
  });

  // Modal (callback request)
  var modal = document.querySelector('[data-modal]');
  document.querySelectorAll('[data-modal-open]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      if (modal) modal.classList.add('is-open');
    });
  });
  if (modal) {
    modal.addEventListener('click', function (e) {
      if (e.target === modal || e.target.matches('[data-modal-close]') || e.target.closest('[data-modal-close]')) {
        modal.classList.remove('is-open');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') modal.classList.remove('is-open');
    });
  }

  // Highlight active nav link (compare resolved pathnames so relative hrefs work)
  var path = location.pathname.replace(/\/+$/, '') || '/';
  document.querySelectorAll('[data-nav] a').forEach(function (a) {
    try {
      var linkPath = new URL(a.href).pathname.replace(/\/+$/, '') || '/';
      if (linkPath === path) a.classList.add('is-active');
    } catch (e) {}
  });

  // Smooth-scroll for in-page anchors only
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href').slice(1);
      if (!id) return;
      var el = document.getElementById(id);
      if (!el) return;
      e.preventDefault();
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      if (nav && nav.classList.contains('is-open')) nav.classList.remove('is-open');
    });
  });

  // Hero promotions carousel
  document.querySelectorAll('[data-carousel]').forEach(function (root) {
    var slides = Array.prototype.slice.call(root.querySelectorAll('.hero__slide'));
    var dots = Array.prototype.slice.call(root.querySelectorAll('[data-carousel-dot]'));
    var prevBtn = root.querySelector('[data-carousel-prev]');
    var nextBtn = root.querySelector('[data-carousel-next]');
    var track = root.querySelector('[data-carousel-slides]');
    if (slides.length < 2) return;

    var idx = 0;
    var INTERVAL = 7000;
    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var timer = null;
    var paused = false;

    function show(i) {
      idx = (i + slides.length) % slides.length;
      slides.forEach(function (s, k) {
        var active = k === idx;
        s.classList.toggle('is-active', active);
        s.setAttribute('aria-hidden', active ? 'false' : 'true');
      });
      dots.forEach(function (d, k) {
        var active = k === idx;
        d.classList.toggle('is-active', active);
        d.setAttribute('aria-selected', active ? 'true' : 'false');
      });
    }
    function next() { show(idx + 1); }
    function prev() { show(idx - 1); }
    function start() {
      if (reduceMotion || paused) return;
      stop();
      timer = setInterval(next, INTERVAL);
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function restart() { stop(); start(); }

    dots.forEach(function (d, k) {
      d.addEventListener('click', function () { show(k); restart(); });
    });
    if (nextBtn) nextBtn.addEventListener('click', function () { next(); restart(); });
    if (prevBtn) prevBtn.addEventListener('click', function () { prev(); restart(); });

    root.addEventListener('mouseenter', function () { paused = true; stop(); });
    root.addEventListener('mouseleave', function () { paused = false; start(); });
    root.addEventListener('focusin', function () { paused = true; stop(); });
    root.addEventListener('focusout', function () { paused = false; start(); });

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) stop(); else if (!paused) start();
    });

    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); prev(); restart(); }
      if (e.key === 'ArrowRight') { e.preventDefault(); next(); restart(); }
    });

    var touchX = null;
    if (track) {
      track.addEventListener('touchstart', function (e) {
        touchX = e.touches[0].clientX;
        paused = true; stop();
      }, { passive: true });
      track.addEventListener('touchend', function (e) {
        if (touchX === null) return;
        var dx = e.changedTouches[0].clientX - touchX;
        if (Math.abs(dx) > 40) { (dx < 0 ? next : prev)(); }
        touchX = null;
        paused = false; start();
      });
    }

    start();
  });

  // Scroll reveal animations (no library, no jank)
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !reduceMotion) {
    var revealTargets = document.querySelectorAll(
      '.section h2, .section__lead, .service-card, .doctor-card, .review-quote, .rating-card, .usp, .faq__item, .pf-card, .related__card, .prices-table'
    );
    revealTargets.forEach(function (el) { el.classList.add('js-reveal'); });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });

    revealTargets.forEach(function (el) { io.observe(el); });
  }

  // Reading progress bar (top of viewport)
  var progress = document.querySelector('[data-scroll-progress]');
  if (progress) {
    var ticking = false;
    var updateProgress = function () {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      var pct = max > 0 ? (h.scrollTop / max) * 100 : 0;
      progress.style.width = pct.toFixed(1) + '%';
      ticking = false;
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(updateProgress); ticking = true; }
    }, { passive: true });
    updateProgress();
  }

  // Floating contact widget (WhatsApp / Telegram / Phone)
  var fab = document.querySelector('[data-fab]');
  if (fab) {
    var fabToggle = fab.querySelector('[data-fab-toggle]');
    var openFab = function () { fab.classList.add('is-open'); fabToggle.setAttribute('aria-expanded', 'true'); };
    var closeFab = function () { fab.classList.remove('is-open'); fabToggle.setAttribute('aria-expanded', 'false'); };
    if (fabToggle) {
      fabToggle.addEventListener('click', function (e) {
        e.preventDefault();
        if (fab.classList.contains('is-open')) closeFab(); else openFab();
      });
    }
    document.addEventListener('click', function (e) {
      if (!fab.contains(e.target)) closeFab();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeFab();
    });
    // Show after small delay (less intrusive on first impression)
    setTimeout(function () { fab.classList.add('is-ready'); }, 800);
  }
})();
