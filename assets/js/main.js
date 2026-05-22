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

  // Lead submission via Web3Forms (https://web3forms.com)
  // ---------------------------------------------------------------
  // Why Web3Forms instead of FormSubmit:
  //   * No "first submission captcha wall" — works on attempt #1
  //   * Native CORS — plain fetch() returns proper JSON
  //   * Simple one-time setup: generate access_key on web3forms.com
  //     (recipient email gets the key immediately, no signup needed)
  //   * Pretty HTML email out of the box (table layout, branded subject)
  //
  // The visitor never sees anything about activation/confirmation —
  // only "Спасибо…" on success or the fallback phone number on error.
  //
  // ACCESS_KEY belongs to the clinic; emails go to whatever address
  // was used to generate the key on web3forms.com.
  var LEAD_ENDPOINT = 'https://api.web3forms.com/submit';
  var ACCESS_KEY = '__WEB3FORMS_KEY__'; // TODO: replace with real access_key from web3forms.com

  document.querySelectorAll('form[data-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var success = form.querySelector('[data-form-success]');
      var submitBtn = form.querySelector('button[type="submit"]');
      var origLabel = submitBtn ? submitBtn.textContent : 'Отправить';
      var fail = function (logMsg, err) {
        if (logMsg) console.warn('[lead]', logMsg, err || '');
        if (success) {
          success.textContent = 'Не удалось отправить. Позвоните, пожалуйста: +7 (910) 458-88-08';
          success.classList.add('is-active');
          setTimeout(function () { success.classList.remove('is-active'); }, 9000);
        }
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = origLabel; }
      };

      // Build payload — Web3Forms reads access_key + free-form fields
      var fd = new FormData(form);
      fd.append('access_key', ACCESS_KEY);
      fd.append('subject', 'Заявка с сайта Ангел-Дент · ' + (location.pathname || '/'));
      fd.append('from_name', 'Сайт angel-denta.ru');
      fd.append('Страница', location.pathname || '/');
      if (document.title) fd.append('Раздел', document.title);
      fd.append('botcheck', ''); // honeypot

      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Отправляем…'; }

      var ctrl = ('AbortController' in window) ? new AbortController() : null;
      var timeoutId = setTimeout(function () { if (ctrl) ctrl.abort(); }, 15000);

      fetch(LEAD_ENDPOINT, {
        method: 'POST',
        body: fd,
        headers: { 'Accept': 'application/json' },
        signal: ctrl ? ctrl.signal : undefined
      })
      .then(function (res) {
        return res.json().then(function (data) { return { ok: res.ok, data: data }; });
      })
      .then(function (r) {
        clearTimeout(timeoutId);
        if (r.ok && r.data && r.data.success) {
          if (typeof ym === 'function') { try { ym(109369174, 'reachGoal', 'lead_submit'); } catch (e) {} }
          if (success) {
            success.textContent = 'Спасибо! Мы перезвоним за 15 минут.';
            success.classList.add('is-active');
            setTimeout(function () { success.classList.remove('is-active'); }, 9000);
          }
          form.reset();
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = origLabel; }
        } else {
          fail('Web3Forms rejected', r.data);
        }
      })
      .catch(function (err) {
        clearTimeout(timeoutId);
        fail('network/abort', err);
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
})();
