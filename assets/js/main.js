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

  // Lead submission via FormSubmit.co
  // ---------------------------------------------------------------
  // Free-tier FormSubmit needs a one-time "Confirm" click inside an
  // activation email it sends to the recipient after the very first
  // submission. Until that click, no real emails arrive.
  //
  // Strategy:
  //   * First submission ever (localStorage flag absent) — open
  //     FormSubmit's page in a popup window. The user there sees
  //     the captcha + "Activation email sent" notice, and can spot
  //     the confirmation email immediately. We flip the flag.
  //   * Subsequent submissions — silent POST into a hidden iframe.
  //
  // Once the recipient confirms once, both paths deliver mail
  // directly with no further user interaction.
  var LEAD_EMAIL = 'adriaaante@gmail.com';
  var ACTIVATED_KEY = 'ad_lead_activated_v1';

  function buildPayload(form) {
    var fd = new FormData(form);
    fd.append('_subject', 'Заявка с сайта Ангел-Дент · ' + (location.pathname || '/'));
    fd.append('_template', 'table');
    fd.append('_captcha', 'false');
    fd.append('_honey', '');
    fd.append('_next', location.origin + location.pathname + '?lead=ok');
    fd.append('Страница', location.pathname || '/');
    if (document.title) fd.append('Раздел', document.title);
    return fd;
  }

  function showSuccess(form, html) {
    var success = form.querySelector('[data-form-success]');
    if (!success) return;
    if (html != null) success.innerHTML = html;
    success.classList.add('is-active');
    setTimeout(function () { success.classList.remove('is-active'); }, 9000);
  }

  function activated() {
    try { return localStorage.getItem(ACTIVATED_KEY) === '1'; } catch (e) { return false; }
  }
  function markActivated() {
    try { localStorage.setItem(ACTIVATED_KEY, '1'); } catch (e) {}
  }

  document.querySelectorAll('form[data-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var submitBtn = form.querySelector('button[type="submit"]');
      var origLabel = submitBtn ? submitBtn.textContent : 'Отправить';
      var fd = buildPayload(form);

      // === First-ever submission: hidden iframe + clear instructions ===
      if (!activated()) {
        if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Отправляем…'; }

        var ifr = document.createElement('iframe');
        ifr.setAttribute('name', '_lead_iframe_' + Date.now());
        ifr.setAttribute('aria-hidden', 'true');
        ifr.style.cssText = 'position:absolute;width:0;height:0;border:0;left:-9999px;';
        document.body.appendChild(ifr);

        var tmp = document.createElement('form');
        tmp.method = 'POST';
        tmp.action = 'https://formsubmit.co/' + LEAD_EMAIL;
        tmp.target = ifr.getAttribute('name');
        tmp.acceptCharset = 'UTF-8';
        fd.forEach(function (v, k) {
          var inp = document.createElement('input');
          inp.type = 'hidden'; inp.name = k; inp.value = v;
          tmp.appendChild(inp);
        });
        document.body.appendChild(tmp);

        var doneFirst = false;
        var finishFirst = function () {
          if (doneFirst) return; doneFirst = true;
          markActivated();
          if (typeof ym === 'function') { try { ym(100658497, 'reachGoal', 'lead_submit'); } catch (e) {} }
          showSuccess(form,
            'Заявка отправлена. <strong>Чтобы письма приходили моментально</strong>, ' +
            'однократно подтвердите получателя: в почте <em>adriaaante@gmail.com</em> ' +
            'найдите письмо от <strong>no-reply@formsubmit.co</strong> ' +
            '(возможно во вкладке «Промоакции» или папке «Спам») и нажмите «Confirm». ' +
            'Все следующие заявки будут приходить без задержки.');
          form.reset();
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = origLabel; }
          if (tmp.parentNode) tmp.parentNode.removeChild(tmp);
          setTimeout(function () { if (ifr.parentNode) ifr.parentNode.removeChild(ifr); }, 2500);
        };
        ifr.addEventListener('load', finishFirst);
        setTimeout(finishFirst, 8000); // safety: FormSubmit's response page may not fire load reliably
        tmp.submit();
        return;
      }

      // === Activated path: silent iframe POST ===
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Отправляем…'; }
      var ifr2 = document.createElement('iframe');
      ifr2.setAttribute('name', '_lead_iframe_' + Date.now());
      ifr2.style.cssText = 'position:absolute;width:0;height:0;border:0;left:-9999px;';
      document.body.appendChild(ifr2);

      var tmp2 = document.createElement('form');
      tmp2.method = 'POST';
      tmp2.action = 'https://formsubmit.co/' + LEAD_EMAIL;
      tmp2.target = ifr2.getAttribute('name');
      fd.forEach(function (v, k) {
        var inp = document.createElement('input');
        inp.type = 'hidden'; inp.name = k; inp.value = v;
        tmp2.appendChild(inp);
      });
      document.body.appendChild(tmp2);

      var done2 = false;
      var finish2 = function () {
        if (done2) return; done2 = true;
        if (typeof ym === 'function') { try { ym(100658497, 'reachGoal', 'lead_submit'); } catch (e) {} }
        showSuccess(form, 'Спасибо! Мы перезвоним за 15 минут.');
        form.reset();
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = origLabel; }
        if (tmp2.parentNode) tmp2.parentNode.removeChild(tmp2);
        setTimeout(function () { if (ifr2.parentNode) ifr2.parentNode.removeChild(ifr2); }, 2500);
      };
      ifr2.addEventListener('load', finish2);
      setTimeout(function () {
        if (done2) return;
        done2 = true;
        showSuccess(form, 'Не удалось отправить. Позвоните, пожалуйста: +7 (910) 458-88-08');
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = origLabel; }
        if (tmp2.parentNode) tmp2.parentNode.removeChild(tmp2);
        if (ifr2.parentNode) ifr2.parentNode.removeChild(ifr2);
      }, 15000);

      tmp2.submit();
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
