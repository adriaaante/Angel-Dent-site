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

  // Form submit — posts via a hidden <iframe> to bypass CORS on
  // FormSubmit.co. Works from any origin (including localhost /
  // github.io) and the very first time, without requiring the
  // recipient to pre-activate. FormSubmit will still send one
  // confirmation email on first submission — the recipient must
  // click "Confirm" inside it once; after that delivery is direct.
  var LEAD_EMAIL = 'adriaaante@gmail.com';

  document.querySelectorAll('form[data-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var success = form.querySelector('[data-form-success]');
      var submitBtn = form.querySelector('button[type="submit"]');
      var origLabel = submitBtn ? submitBtn.textContent : 'Отправить';

      // Build the payload
      var fd = new FormData(form);
      fd.append('_subject', 'Заявка с сайта Ангел-Дент · ' + (location.pathname || '/'));
      fd.append('_template', 'table');
      fd.append('_captcha', 'false');
      fd.append('_honey', '');
      fd.append('_next', location.href + '?lead=ok'); // benign redirect inside the hidden iframe
      fd.append('Страница', location.pathname || '/');
      if (document.title) fd.append('Раздел', document.title);

      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Отправляем…'; }

      // Hidden iframe target
      var ifr = document.createElement('iframe');
      ifr.name = '_lead_target_' + Date.now();
      ifr.style.display = 'none';
      document.body.appendChild(ifr);

      // Temporary form posting to FormSubmit's non-AJAX endpoint
      var tmp = document.createElement('form');
      tmp.method = 'POST';
      tmp.action = 'https://formsubmit.co/' + LEAD_EMAIL;
      tmp.target = ifr.name;
      tmp.style.display = 'none';
      fd.forEach(function (v, k) {
        var inp = document.createElement('input');
        inp.type = 'hidden';
        inp.name = k;
        inp.value = v;
        tmp.appendChild(inp);
      });
      document.body.appendChild(tmp);

      var done = false;
      var cleanup = function () {
        if (tmp.parentNode) tmp.parentNode.removeChild(tmp);
        // Keep the iframe a bit longer so the request completes server-side
        setTimeout(function () { if (ifr.parentNode) ifr.parentNode.removeChild(ifr); }, 1500);
      };

      ifr.addEventListener('load', function () {
        if (done) return;
        done = true;
        if (typeof ym === 'function') { try { ym(100658497, 'reachGoal', 'lead_submit'); } catch (e) {} }
        if (success) success.classList.add('is-active');
        form.reset();
        setTimeout(function () { if (success) success.classList.remove('is-active'); }, 6000);
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = origLabel; }
        cleanup();
      });

      // Hard timeout — fallback message
      setTimeout(function () {
        if (done) return;
        done = true;
        if (success) {
          success.textContent = 'Не удалось отправить. Позвоните, пожалуйста: +7 (910) 458-88-08';
          success.classList.add('is-active');
        }
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = origLabel; }
        cleanup();
      }, 15000);

      tmp.submit();
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
})();
