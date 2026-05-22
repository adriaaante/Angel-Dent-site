/* Angel-Dent — Cookie consent banner & Yandex.Metrika gated loader
 * Compliant with 152-ФЗ / 149-ФЗ approach: analytics fires only after explicit consent.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'ad_cookies_consent';
  var YM_ID = 109369174;

  // ----- Yandex.Metrika loader (mirrors the official snippet, with one guard) -----
  function loadYandexMetrika() {
    if (window.__ad_ym_loaded) return;
    window.__ad_ym_loaded = true;
    (function (m, e, t, r, i, k, a) {
      m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); };
      m[i].l = 1 * new Date();
      for (var j = 0; j < e.scripts.length; j++) { if (e.scripts[j].src === r) { return; } }
      k = e.createElement(t);
      a = e.getElementsByTagName(t)[0];
      k.async = 1;
      k.src = r;
      a.parentNode.insertBefore(k, a);
    })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js?id=' + YM_ID, 'ym');
    try {
      window.ym(YM_ID, 'init', {
        ssr: true,
        webvisor: true,
        clickmap: true,
        ecommerce: 'dataLayer',
        referrer: document.referrer,
        url: location.href,
        accurateTrackBounce: true,
        trackLinks: true
      });
    } catch (e) { /* noop */ }
  }

  // ----- Consent helpers -----
  function getConsent() {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }
  function setConsent(value) {
    try { localStorage.setItem(STORAGE_KEY, value); } catch (e) { /* noop */ }
  }

  // ----- DOM: banner -----
  function buildBanner() {
    var wrap = document.createElement('div');
    wrap.className = 'cookie-banner';
    wrap.setAttribute('role', 'dialog');
    wrap.setAttribute('aria-label', 'Согласие на использование cookies');
    wrap.innerHTML = ''
      + '<div class="cookie-banner__inner">'
      +   '<div class="cookie-banner__text">'
      +     'Мы используем cookies для работы сайта и анализа посещаемости (Яндекс.Метрика). '
      +     'Подробнее — в <a href="' + linkPath('cookies.html') + '">Cookie-политике</a> и '
      +     '<a href="' + linkPath('privacy.html') + '">Политике конфиденциальности</a>.'
      +   '</div>'
      +   '<div class="cookie-banner__actions">'
      +     '<button type="button" class="btn btn--ghost" data-cookie-essential>Только необходимые</button>'
      +     '<button type="button" class="btn btn--primary" data-cookie-all>Принять все</button>'
      +   '</div>'
      + '</div>';
    return wrap;
  }

  function buildToggle() {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'cookie-toggle';
    btn.setAttribute('aria-label', 'Настройки cookies');
    btn.title = 'Настройки cookies';
    btn.innerHTML = ''
      + '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
      +   '<path d="M21.6 12.4c-1.3.3-2.6-.5-2.9-1.8-.1-.5-.5-.8-1-.8-1.4 0-2.5-1.1-2.5-2.5 0-.5-.3-.9-.8-1-1.3-.3-2.1-1.6-1.8-2.9.1-.5-.2-1-.7-1.1A9.7 9.7 0 0 0 12 2a10 10 0 1 0 10 10c0-.4-.4-.7-.4-.6Z"/>'
      +   '<circle cx="8" cy="13" r="1"/><circle cx="13" cy="17" r="1"/><circle cx="16" cy="11" r="1"/>'
      + '</svg>'
      + '<span>Cookies</span>';
    return btn;
  }

  // Compute relative path to root assets. Pages live either in root or one subfolder deep (/doctors/, /services/).
  function linkPath(file) {
    var depth = (window.location.pathname.replace(/\/[^\/]*$/, '/').match(/\//g) || []).length - 1;
    var prefix = depth > 0 ? '../'.repeat(depth) : '';
    return prefix + file;
  }

  // ----- Show / hide -----
  var bannerEl = null;
  var toggleEl = null;

  function showBanner() {
    if (!bannerEl) {
      bannerEl = buildBanner();
      document.body.appendChild(bannerEl);
      bannerEl.querySelector('[data-cookie-all]').addEventListener('click', function () {
        setConsent('all');
        hideBanner();
        loadYandexMetrika();
      });
      bannerEl.querySelector('[data-cookie-essential]').addEventListener('click', function () {
        setConsent('essential');
        hideBanner();
      });
    }
    // Force reflow then show
    requestAnimationFrame(function () { bannerEl.classList.add('is-visible'); });
  }

  function hideBanner() {
    if (bannerEl) bannerEl.classList.remove('is-visible');
  }

  function ensureToggle() {
    if (toggleEl) return;
    toggleEl = buildToggle();
    document.body.appendChild(toggleEl);
    toggleEl.addEventListener('click', showBanner);
  }

  // ----- Bootstrap -----
  function init() {
    ensureToggle();
    var consent = getConsent();
    if (consent === 'all') {
      loadYandexMetrika();
    } else if (consent === null) {
      showBanner();
    }
    // 'essential' — do nothing, Metrika stays off
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
