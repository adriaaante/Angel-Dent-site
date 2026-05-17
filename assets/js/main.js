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

  // Form submit — sends a nicely formatted email to angel.dent@bk.ru
  // via FormSubmit.co (static-site mailer, no backend needed).
  // First submission triggers an activation email — recipient must
  // click the link once to enable real delivery.
  var LEAD_ENDPOINT = 'https://formsubmit.co/ajax/angel.dent@bk.ru';

  document.querySelectorAll('form[data-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var success = form.querySelector('[data-form-success]');
      var submitBtn = form.querySelector('button[type="submit"]');
      var formData = new FormData(form);

      // FormSubmit meta fields — subject line, pretty email template, anti-spam
      var page = location.pathname || '/';
      formData.append('_subject', 'Заявка с сайта Ангел-Дент · ' + page);
      formData.append('_template', 'table');
      formData.append('_captcha', 'false');
      formData.append('_honey', '');
      formData.append('Страница', page);
      if (document.title) formData.append('Раздел', document.title);

      if (submitBtn) { submitBtn.disabled = true; submitBtn.dataset._label = submitBtn.textContent; submitBtn.textContent = 'Отправляем…'; }

      fetch(LEAD_ENDPOINT, {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: formData
      })
      .then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function () {
        if (typeof ym === 'function') { try { ym(100658497, 'reachGoal', 'lead_submit'); } catch (e) {} }
        if (success) success.classList.add('is-active');
        form.reset();
        setTimeout(function () { if (success) success.classList.remove('is-active'); }, 6000);
      })
      .catch(function () {
        if (success) { success.textContent = 'Не удалось отправить. Позвоните, пожалуйста: +7 (910) 458-88-08'; success.classList.add('is-active'); }
      })
      .finally(function () {
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = submitBtn.dataset._label || 'Отправить'; }
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
})();
