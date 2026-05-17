/* ============================================================
   ПОРТФОЛИО ВРАЧЕЙ — данные и рендеринг
   ============================================================

   КАК ДОБАВИТЬ НОВУЮ РАБОТУ:
   1. Положите фото "до" и "после" в /assets/img/portfolio/<slug-врача>/
      Имена удобнее давать по порядку: case-01-before.jpg, case-01-after.jpg
   2. Найдите ниже массив для нужного врача (по ключу slug)
   3. Скопируйте один блок { ... } и заполните свои данные
   4. Сохраните файл — на странице врача работа появится автоматически

   Поля:
     title       — короткое название случая
     description — 1–2 предложения о работе
     services    — массив тегов (видимые «бейджи» под фото)
     duration    — срок лечения (необязательно)
     before      — путь к фото "до" (если нет — оставьте плейсхолдер)
     after       — путь к фото "после"
     date        — дата работы в формате 'MM.YYYY' (необязательно)

   Slug-и врачей соответствуют именам HTML-файлов в /doctors/:
     emil-mamedov  → Зурначян Арам Арамович (главврач, имплантолог)
     aram          → Геворкян Санатрук Иванович (хирург, ортопед, имплантолог)
     rustam        → Рустамли Руслан Рустамович (хирург, имплантолог)
     ortodont      → Дробкова Кристина Олеговна (ортодонт)
   ============================================================ */

window.AD_PORTFOLIO = {

  // === Зурначян Арам Арамович — главный врач, имплантолог, стоматолог-хирург ===
  'emil-mamedov': [
    {
      title: 'Имплантация двух жевательных зубов на нижней челюсти',
      description: 'Установлены импланты премиум-класса. Через 3 месяца — постоянные коронки из диоксида циркония. Пациент жуёт привычно.',
      services: ['Имплантация', 'Коронки Zr'],
      duration: '3 месяца',
      date: '03.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Синус-лифтинг и одномоментная имплантация',
      description: 'Восстановление костного объёма верхней челюсти материалом Geistlich Bio-Oss с одновременной установкой импланта.',
      services: ['Синус-лифтинг', 'Костная пластика', 'Имплантация'],
      duration: '4 месяца',
      date: '01.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'All-on-4 — полное восстановление нижней челюсти',
      description: 'Установка четырёх имплантов и временного несъёмного протеза за 1 день. Через 4 месяца — постоянный протез.',
      services: ['All-on-4', 'Имплантация', 'Протезирование'],
      duration: '4 месяца',
      date: '11.2024',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    }
  ],

  // === Геворкян Санатрук Иванович — стоматолог-хирург, ортопед, имплантолог ===
  'aram': [
    {
      title: 'Имплантация в эстетически значимой зоне',
      description: 'Установка импланта на место передного зуба с временной коронкой в день операции. Через 4 месяца — постоянная циркониевая коронка.',
      services: ['Имплантация', 'Эстетика', 'Zr-коронка'],
      duration: '4 месяца',
      date: '02.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Протезирование на двух имплантах — мостовидный протез',
      description: 'Сканер 3Shape Trios, моделирование в CAD/CAM, циркониевый мост на трёх единицах. Точная посадка по цифровому слепку.',
      services: ['Протезирование', 'Импланты', 'CAD/CAM'],
      duration: '6 недель',
      date: '04.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Удаление ретинированного зуба мудрости с одномоментной костной пластикой',
      description: 'Сложное хирургическое удаление горизонтально расположенного зуба мудрости с сохранением объёма кости для будущей имплантации.',
      services: ['Хирургия', 'Костная пластика'],
      duration: '1 визит',
      date: '03.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    }
  ],

  // === Рустамли Руслан Рустамович — стоматолог-хирург, имплантолог ===
  'rustam': [
    {
      title: 'Установка двух имплантов SNUCONE на нижней челюсти',
      description: 'Малоинвазивный хирургический протокол, через 3 месяца установлены постоянные коронки. Пациент вернулся к привычному рациону.',
      services: ['Имплантация', 'SNUCONE'],
      duration: '3 месяца',
      date: '03.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Удаление ретинированного зуба мудрости',
      description: 'Сложное удаление горизонтально расположенного зуба с минимальной травмой соседних структур. По протоколу из курса в Санкт-Петербурге.',
      services: ['Хирургия', 'Зубы мудрости'],
      duration: '1 визит',
      date: '04.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Костная пластика материалом Geistlich Bio-Oss',
      description: 'Восстановление объёма альвеолярного гребня перед имплантацией. Биоматериал Bio-Oss обеспечивает прогнозируемый результат.',
      services: ['Костная пластика', 'Bio-Oss'],
      duration: '4 месяца',
      date: '01.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    }
  ],

  // === Дробкова Кристина Олеговна — стоматолог-ортодонт ===
  // (страница /doctors/ortodont.html — slug сохранён)
  'ortodont': [
    {
      title: 'Исправление прикуса брекетами Damon Q',
      description: 'Самолигирующая система Damon. Лечение завершено за 18 месяцев, установлен несъёмный ретейнер.',
      services: ['Брекеты', 'Damon Q'],
      duration: '18 месяцев',
      date: '12.2024',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Элайнеры Star Smile — взрослый пациент',
      description: 'Скученность нижнего ряда. 24 каппы по графику смены раз в 10 дней. Без удалений.',
      services: ['Элайнеры', 'Star Smile'],
      duration: '8 месяцев',
      date: '02.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    }
  ]

};

/* ============================================================
   РЕНДЕРИНГ — не трогайте, если просто добавляете работы
   ============================================================ */
(function () {
  'use strict';

  function escapeHTML(str) {
    return String(str || '').replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function renderCard(item, idx) {
    var tags = (item.services || []).map(function (s) {
      return '<span class="pf-tag">' + escapeHTML(s) + '</span>';
    }).join('');
    var meta = [];
    if (item.duration) meta.push('<span class="pf-meta__item">⏱ ' + escapeHTML(item.duration) + '</span>');
    if (item.date) meta.push('<span class="pf-meta__item">📅 ' + escapeHTML(item.date) + '</span>');

    return (
      '<article class="pf-card" data-pf-index="' + idx + '">' +
        '<div class="pf-card__images">' +
          '<figure class="pf-img"><img loading="lazy" src="' + escapeHTML(item.before) + '" alt="До лечения — ' + escapeHTML(item.title) + '"><figcaption>До</figcaption></figure>' +
          '<figure class="pf-img pf-img--after"><img loading="lazy" src="' + escapeHTML(item.after) + '" alt="После лечения — ' + escapeHTML(item.title) + '"><figcaption>После</figcaption></figure>' +
        '</div>' +
        '<div class="pf-card__body">' +
          '<h3 class="pf-card__title">' + escapeHTML(item.title) + '</h3>' +
          (item.description ? '<p class="pf-card__desc">' + escapeHTML(item.description) + '</p>' : '') +
          (tags ? '<div class="pf-tags">' + tags + '</div>' : '') +
          (meta.length ? '<div class="pf-meta">' + meta.join('') + '</div>' : '') +
        '</div>' +
      '</article>'
    );
  }

  function renderEmpty() {
    return (
      '<div class="pf-empty">' +
        '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="M21 15l-5-5L5 21"/></svg>' +
        '<p>Работы врача скоро появятся здесь. Хотите посмотреть кейсы прямо сейчас? Запишитесь на консультацию — покажем на приёме.</p>' +
      '</div>'
    );
  }

  function openLightbox(item) {
    var lb = document.querySelector('[data-pf-lightbox]');
    if (!lb) return;
    lb.querySelector('[data-pf-lb-before]').src = item.before;
    lb.querySelector('[data-pf-lb-after]').src = item.after;
    lb.querySelector('[data-pf-lb-title]').textContent = item.title || '';
    lb.querySelector('[data-pf-lb-desc]').textContent = item.description || '';
    lb.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    var lb = document.querySelector('[data-pf-lightbox]');
    if (!lb) return;
    lb.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  function mount() {
    var nodes = document.querySelectorAll('[data-portfolio]');
    if (!nodes.length) return;

    // Inject lightbox once
    if (!document.querySelector('[data-pf-lightbox]')) {
      var lb = document.createElement('div');
      lb.className = 'pf-lightbox';
      lb.setAttribute('data-pf-lightbox', '');
      lb.innerHTML =
        '<button class="pf-lightbox__close" data-pf-lb-close aria-label="Закрыть">×</button>' +
        '<div class="pf-lightbox__inner">' +
          '<div class="pf-lightbox__images">' +
            '<figure><img data-pf-lb-before alt=""><figcaption>До</figcaption></figure>' +
            '<figure><img data-pf-lb-after alt=""><figcaption>После</figcaption></figure>' +
          '</div>' +
          '<h3 data-pf-lb-title></h3>' +
          '<p data-pf-lb-desc></p>' +
        '</div>';
      document.body.appendChild(lb);
      lb.addEventListener('click', function (e) {
        if (e.target === lb || e.target.closest('[data-pf-lb-close]')) closeLightbox();
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeLightbox();
      });
    }

    nodes.forEach(function (node) {
      var slug = node.getAttribute('data-portfolio');
      var items = (window.AD_PORTFOLIO && window.AD_PORTFOLIO[slug]) || [];
      if (!items.length) {
        node.innerHTML = renderEmpty();
        return;
      }
      node.innerHTML = items.map(renderCard).join('');
      node.addEventListener('click', function (e) {
        var card = e.target.closest('[data-pf-index]');
        if (!card) return;
        var idx = parseInt(card.getAttribute('data-pf-index'), 10);
        if (!isNaN(idx) && items[idx]) openLightbox(items[idx]);
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
