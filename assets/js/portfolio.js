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
     ortodont      → Дробкова Кристина Олеговна (главврач, стоматолог-ортодонт)
     aram          → Геворкян Санатрук Иванович (ген. директор, стоматолог-хирург, имплантолог)
     rustam        → Рустамли Руслан Рустамович (стоматолог-хирург, имплантолог)
     emil-mamedov  → Рустамов Эмиль Дилгамович (стоматолог-ортопед)
     smolyakova    → Смолякова Радана Сергеевна (стоматолог-терапевт)
     kartlykov     → Картлыков Омар Хасанбиевич (стоматолог-терапевт)
     stepanenko    → Степаненко Владислав Евгеньевич (стоматолог-терапевт)
   ============================================================ */

window.AD_PORTFOLIO = {

  // === Дробкова Кристина Олеговна — главврач, стоматолог-ортодонт ===
  'ortodont': [
    {
      title: 'Исправление скученности брекетами Damon Q',
      description: 'Самолигирующая система Damon Q на обе челюсти. Без удаления зубов, по завершении установлен несъёмный ретейнер.',
      services: ['Брекеты', 'Damon Q', 'Ретейнер'],
      duration: '18 месяцев',
      date: '12.2024',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Элайнеры Star Smile у взрослого пациента',
      description: 'Скученность нижнего ряда и лёгкая ротация резцов. 24 каппы по графику смены раз в 10 дней, без удалений.',
      services: ['Элайнеры', 'Star Smile'],
      duration: '8 месяцев',
      date: '02.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Коррекция дистального прикуса у подростка',
      description: 'Лечение керамическими брекетами Clarity с межчелюстными тягами. Получен стабильный физиологичный прикус.',
      services: ['Брекеты Clarity', 'Подросток', 'Дистальный прикус'],
      duration: '22 месяца',
      date: '05.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Исправление мезиального прикуса у взрослого',
      description: 'Комбинированное лечение брекетами Damon Q с использованием микроимплантов для опоры. Прикус нормализован без хирургии.',
      services: ['Брекеты', 'Damon Q', 'Мезиальный прикус'],
      duration: '24 месяца',
      date: '09.2024',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    }
  ],

  // === Геворкян Санатрук Иванович — ген. директор, стоматолог-хирург, имплантолог ===
  'aram': [
    {
      title: 'All-on-4 — полное восстановление верхней челюсти',
      description: 'Установка четырёх имплантов Straumann и временного несъёмного протеза за один день. Через 4 месяца — постоянная конструкция.',
      services: ['All-on-4', 'Straumann', 'Имплантация'],
      duration: '4 месяца',
      date: '03.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Открытый синус-лифтинг с одномоментной имплантацией',
      description: 'Восстановление костного объёма верхней челюсти материалом Geistlich Bio-Oss и установка импланта AnyRidge за одну операцию.',
      services: ['Синус-лифтинг', 'Bio-Oss', 'AnyRidge'],
      duration: '5 месяцев',
      date: '11.2024',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Удаление ретинированной восьмёрки с костной пластикой',
      description: 'Сложное хирургическое удаление горизонтально расположенного зуба мудрости с сохранением объёма кости для будущей имплантации.',
      services: ['Хирургия', 'Восьмёрки', 'Костная пластика'],
      duration: '1 визит',
      date: '01.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Имплантация в эстетически значимой зоне',
      description: 'Установка импланта Straumann на место центрального резца с временной коронкой в день операции. Сохранён контур десны.',
      services: ['Имплантация', 'Straumann', 'Эстетика'],
      duration: '4 месяца',
      date: '06.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    }
  ],

  // === Рустамли Руслан Рустамович — стоматолог-хирург, имплантолог ===
  'rustam': [
    {
      title: 'Имплантация двух зубов SNUCONE на нижней челюсти',
      description: 'Малоинвазивный хирургический протокол по системе Implantium & SuperLine. Через 3 месяца установлены постоянные коронки.',
      services: ['Имплантация', 'SNUCONE'],
      duration: '3 месяца',
      date: '04.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Одномоментная имплантация Osstem после удаления',
      description: 'Удаление разрушенного жевательного зуба и установка импланта Osstem в ту же лунку. Сокращение общего срока лечения вдвое.',
      services: ['Одномоментная имплантация', 'Osstem'],
      duration: '3 месяца',
      date: '02.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Костная пластика материалом Bio-Oss',
      description: 'Восстановление объёма альвеолярного гребня перед имплантацией. Биоматериал Geistlich Bio-Oss и резорбируемая мембрана.',
      services: ['Костная пластика', 'Bio-Oss'],
      duration: '4 месяца',
      date: '10.2024',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Сложное удаление зуба мудрости',
      description: 'Удаление горизонтально расположенного зуба мудрости с минимальной травмой соседних структур. По авторскому протоколу из курса.',
      services: ['Хирургия', 'Зубы мудрости'],
      duration: '1 визит',
      date: '07.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    }
  ],

  // === Рустамов Эмиль Дилгамович — стоматолог-ортопед ===
  'emil-mamedov': [
    {
      title: 'Виниры E.max на 8 передних зубов',
      description: 'Цифровое моделирование улыбки по протоколу Digital Smile Design, керамические виниры E.max минимальной толщины. Естественный результат.',
      services: ['Виниры', 'E.max', 'DSD'],
      duration: '6 недель',
      date: '03.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Циркониевые коронки на жевательную группу',
      description: 'Сканирование 3Shape Trios, моделирование в CAD/CAM, четыре коронки из диоксида циркония с точной посадкой по цифровому слепку.',
      services: ['Коронки Zr', 'CAD/CAM', '3Shape Trios'],
      duration: '3 недели',
      date: '05.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Мостовидный протез из диоксида циркония',
      description: 'Восстановление трёх единиц мостовидной конструкцией на основе циркония. Цифровая фиксация прикуса и эстетичный результат.',
      services: ['Мост Zr', 'Протезирование'],
      duration: '4 недели',
      date: '12.2024',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Протезирование на двух имплантах — циркониевые коронки',
      description: 'Снятие цифрового слепка 3Shape Trios с имплантов, изготовление индивидуальных абатментов и коронок Zr. Идеальная окклюзия.',
      services: ['Коронки на имплантах', 'Zr', '3Shape Trios'],
      duration: '5 недель',
      date: '08.2024',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    }
  ],

  // === Смолякова Радана Сергеевна — стоматолог-терапевт ===
  'smolyakova': [
    {
      title: 'Художественная реставрация переднего зуба',
      description: 'Восстановление скола центрального резца композитом Estelite Asteria с послойным нанесением оттенков. Реставрация неотличима от соседних зубов.',
      services: ['Реставрация', 'Estelite Asteria', 'Эстетика'],
      duration: '1 визит',
      date: '04.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Лечение пульпита под микроскопом',
      description: 'Эндодонтическое лечение трёхканального моляра под микроскопом Carl Zeiss с инструментами ProTaper. Каналы запломбированы герметично.',
      services: ['Эндодонтия', 'Микроскоп Zeiss', 'ProTaper'],
      duration: '2 визита',
      date: '02.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Лечение глубокого кариеса с сохранением пульпы',
      description: 'Бережное препарирование под микроскопом, лечебная прокладка и реставрация композитом Estelite Asteria. Зуб сохранён живым.',
      services: ['Кариес', 'Микроскоп', 'Estelite Asteria'],
      duration: '1 визит',
      date: '11.2024',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Перелечивание корневых каналов под микроскопом',
      description: 'Распломбировка и повторная обработка двухканального премоляра с устранением очага инфекции. Контроль КЛКТ через 6 месяцев — норма.',
      services: ['Эндодонтия', 'Перелечивание', 'Микроскоп Zeiss'],
      duration: '3 визита',
      date: '06.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    }
  ],

  // === Картлыков Омар Хасанбиевич — стоматолог-терапевт ===
  'kartlykov': [
    {
      title: 'Лечение клиновидных дефектов на 4 зубах',
      description: 'Восстановление пришеечных дефектов нанокомпозитом с подбором оттенка по шкале Vita. Устранена гиперчувствительность.',
      services: ['Клиновидный дефект', 'Реставрация'],
      duration: '1 визит',
      date: '03.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Лечение гиперчувствительности зубов',
      description: 'Комплексная терапия с десенситайзерами и реминерализирующими аппликациями. Пациент вернулся к холодным и горячим напиткам без боли.',
      services: ['Чувствительность', 'Реминерализация'],
      duration: '3 визита',
      date: '01.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Эндодонтическое лечение четырёхканального моляра',
      description: 'Поиск и прохождение четвёртого канала с использованием ProTaper Next. Полная герметизация и постановка постоянной пломбы в одно посещение.',
      services: ['Эндодонтия', 'ProTaper Next'],
      duration: '2 визита',
      date: '10.2024',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Реставрация жевательной поверхности после кариеса',
      description: 'Препарирование по принципам минимальной инвазии и моделирование анатомии бугров композитом. Восстановлены контактные пункты.',
      services: ['Кариес', 'Реставрация'],
      duration: '1 визит',
      date: '07.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    }
  ],

  // === Степаненко Владислав Евгеньевич — стоматолог-терапевт ===
  'stepanenko': [
    {
      title: 'Отбеливание зубов системой ZOOM',
      description: 'Профессиональное отбеливание ZOOM 4 за один визит. Осветление эмали на 6 тонов по шкале Vita с сохранением структуры зуба.',
      services: ['Отбеливание', 'ZOOM'],
      duration: '1 визит',
      date: '05.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Защитные каппы при бруксизме',
      description: 'Диагностика бруксизма и изготовление индивидуальных ночных капп по слепкам. Снижение нагрузки на зубы и жевательные мышцы.',
      services: ['Бруксизм', 'Каппы'],
      duration: '2 недели',
      date: '02.2025',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Реставрация скола режущего края резца',
      description: 'Воссоздание анатомии переднего зуба после травмы композитом с применением силиконового ключа. Эстетика восстановлена за один приём.',
      services: ['Реставрация', 'Травма', 'Эстетика'],
      duration: '1 визит',
      date: '09.2024',
      before: '../assets/img/portfolio/placeholder-before.svg',
      after: '../assets/img/portfolio/placeholder-after.svg'
    },
    {
      title: 'Лечение скрытого кариеса под микроскопом',
      description: 'Обнаружение и лечение апроксимального кариеса между зубами под микроскопом. Сохранены максимально объёмы здоровых тканей.',
      services: ['Кариес', 'Микроскоп'],
      duration: '1 визит',
      date: '12.2024',
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
