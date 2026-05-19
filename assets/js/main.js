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

  // Lead submission — Telegram bot only.
  // Setup: @BotFather → /newbot → токен → TELEGRAM_BOT_TOKEN.
  // CHAT_ID: личный (@userinfobot → /start) или группа
  // (добавить бота, https://api.telegram.org/bot<TOKEN>/getUpdates → chat.id).
  var TELEGRAM_BOT_TOKEN = '8682361398:AAEkEqOgAIFubhfX8oId7UIk4R0vt13Qd2g';
  var TELEGRAM_CHAT_ID   = '-5176309139';
  var TG_ENDPOINT = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage';

  var FIELD_LABELS = { name: 'Имя', phone: 'Телефон', service: 'Услуга', message: 'Комментарий' };

  function sendTelegram(form) {
    var fd = new FormData(form);
    var lines = ['🦷 *Заявка с сайта Ангел-Дент*', ''];
    fd.forEach(function (val, key) {
      if (!val) return;
      var label = FIELD_LABELS[key] || key;
      lines.push('*' + label + ':* ' + String(val).replace(/[*_`[]/g, '\\$&'));
    });
    lines.push('', '_Страница: ' + (location.pathname || '/') + '_');
    return fetch(TG_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: TELEGRAM_CHAT_ID,
        text: lines.join('\n'),
        parse_mode: 'Markdown',
        disable_web_page_preview: true
      })
    }).then(function (r) {
      return r.json().then(function (d) { return d && d.ok ? d : Promise.reject(d); });
    });
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

      sendTelegram(form).then(
        function () { done(true,  'Спасибо! Мы перезвоним за 15 минут.'); },
        function (err) {
          console.warn('[lead] telegram failed', err);
          done(false, 'Не удалось отправить. Позвоните, пожалуйста: +7 (910) 458-88-08');
        }
      );
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
