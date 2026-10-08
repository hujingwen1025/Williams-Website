/* Native scrolling, local interactions, no network requests or dependencies. */
(() => {
  'use strict';
  const root = document.documentElement;
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = window.matchMedia('(max-width: 700px)');
  const menu = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('.navigation');
  const language = document.querySelector('.language-link');
  const progress = document.querySelector('.reading-progress span');
  root.classList.add('has-js');

  // A normal hyperlink remains useful if JavaScript is unavailable.
  const readingSections = [...document.querySelectorAll('main > section[id], .story-step[id], .feature-card[id]')];
  const updateLanguageLink = (keepReadingPosition = false) => {
    const target = new URL(language.getAttribute('href'), location.href);
    target.hash = location.hash;
    if (keepReadingPosition) {
      let current = 'top';
      readingSections.forEach(section => {
        if (section.getBoundingClientRect().top <= window.innerHeight * 0.5) current = section.id;
      });
      target.hash = current === 'top' ? '' : `#${current}`;
    }
    language.href = target.href;
  };
  updateLanguageLink();
  window.addEventListener('hashchange', () => updateLanguageLink());
  language.addEventListener('click', () => updateLanguageLink(true));

  menu.hidden = false;
  const closeMenu = (restoreFocus = false) => {
    navigation.classList.remove('is-open');
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', menu.dataset.openLabel);
    if (restoreFocus) menu.focus();
  };
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? menu.dataset.closeLabel : menu.dataset.openLabel);
    navigation.classList.toggle('is-open', open);
  });
  navigation.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') closeMenu(true);
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  const onMediaChange = (query, handler) => {
    if (query.addEventListener) query.addEventListener('change', handler);
    else if (query.addListener) query.addListener(handler);
  };
  onMediaChange(mobile, () => closeMenu());

  // Only hide enhancement controls until handlers exist; every project starts visible.
  const controls = document.querySelector('.directory-controls');
  const search = document.querySelector('#project-search');
  const cards = [...document.querySelectorAll('.repo-card')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const result = document.querySelector('.result-count');
  const empty = document.querySelector('.empty-state');
  const reset = document.querySelector('.reset-search');
  let category = 'all';
  const normalize = text => text.normalize('NFKC').toLocaleLowerCase();
  const searchText = cards.map(card => normalize(card.textContent));
  const filterProjects = () => {
    const query = normalize(search.value.trim());
    let visible = 0;
    cards.forEach((card, i) => {
      const matchesCategory = category === 'all' || card.dataset.tags.split(' ').includes(category);
      const matchesSearch = query.split(/\s+/).every(term => searchText[i].includes(term));
      card.hidden = !(matchesCategory && matchesSearch);
      if (!card.hidden) visible += 1;
    });
    const template = visible === 1 ? result.dataset.singular : result.dataset.template;
    result.textContent = template.replace('{count}', String(visible));
    empty.hidden = visible !== 0;
  };
  filters.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    filters.forEach(filter => {
      const selected = filter === button;
      filter.classList.toggle('is-selected', selected);
      filter.setAttribute('aria-pressed', String(selected));
    });
    filterProjects();
  }));
  search.addEventListener('input', filterProjects);
  reset.addEventListener('click', () => {
    search.value = '';
    filters[0].click();
    search.focus();
  });
  controls.hidden = false;

  // Reveals are opt-in. A failure in animation setup leaves all text readable.
  let revealObserver;
  const revealAll = () => {
    root.classList.remove('motion-ready');
    if (revealObserver) revealObserver.disconnect();
  };
  const configureReveals = () => {
    revealAll();
    if (motion.matches || !('IntersectionObserver' in window)) return;
    try {
      revealObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.08, rootMargin: '0px 0px 36px 0px' });
      document.querySelectorAll('[data-reveal]').forEach(element => revealObserver.observe(element));
      document.querySelectorAll('.feature-grid, .interests-grid').forEach(grid => {
        [...grid.children].forEach((child, i) => child.style.setProperty('--reveal-delay', `${(i % 3) * 65}ms`));
      });
      root.classList.add('motion-ready');
    } catch {
      revealAll();
    }
  };
  configureReveals();

  // Short, once-per-visit performances start only when the artwork is in view.
  const illustrations = [...document.querySelectorAll('.hero-piano, .vinyl, .code-note, .project-art, .exabyte-mark, .interest-visual')];
  const playedIllustrations = new WeakSet();
  const visibleIllustrations = new Set();
  const illustrationTimers = new Map();
  let illustrationObserver;
  document.querySelectorAll('.piano-keys').forEach(keys => {
    [...keys.children].forEach((key, i) => key.style.setProperty('--key-delay', `${((i * 5) % 14) * 45}ms`));
  });
  const playVisibleIllustrations = () => {
    if (motion.matches || document.hidden) return;
    visibleIllustrations.forEach(element => {
      if (playedIllustrations.has(element)) return;
      const panel = element.closest('.scene-panel');
      if (panel && !panel.classList.contains('is-active')) return;
      const rect = element.getBoundingClientRect();
      // Hidden mobile/desktop variants must keep their first performance.
      if (!rect.width || !rect.height || rect.bottom <= 72 || rect.top >= window.innerHeight) return;
      playedIllustrations.add(element);
      element.classList.add('is-playing');
      illustrationObserver.unobserve(element);
      visibleIllustrations.delete(element);
      illustrationTimers.set(element, window.setTimeout(() => {
        element.classList.remove('is-playing');
        illustrationTimers.delete(element);
      }, 4400));
    });
  };
  const configureIllustrations = () => {
    if (illustrationObserver) illustrationObserver.disconnect();
    visibleIllustrations.clear();
    illustrationTimers.forEach((timer, element) => {
      clearTimeout(timer);
      element.classList.remove('is-playing');
    });
    illustrationTimers.clear();
    if (motion.matches || !('IntersectionObserver' in window)) return;
    try {
      illustrationObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting && entry.intersectionRatio >= 0.25) visibleIllustrations.add(entry.target);
          else visibleIllustrations.delete(entry.target);
        });
        playVisibleIllustrations();
      }, { threshold: 0.25, rootMargin: '-72px 0px 0px 0px' });
      illustrations.forEach(element => {
        if (!playedIllustrations.has(element)) illustrationObserver.observe(element);
      });
    } catch {
      // Static illustrations remain complete if observation is unsupported.
      visibleIllustrations.clear();
    }
  };
  configureIllustrations();
  document.addEventListener('visibilitychange', playVisibleIllustrations);

  // A single frame per scroll burst. Work is bounded to three scenes and four links.
  const steps = [...document.querySelectorAll('[data-scene]')];
  const panels = [...document.querySelectorAll('[data-panel]')];
  const markers = [...document.querySelectorAll('.scene-markers i')];
  const navLinks = [...navigation.querySelectorAll('a')];
  const navSections = navLinks.map(a => document.querySelector(a.getAttribute('href')));
  const scene = document.querySelector('.scene-stack');
  let queued = false;
  let activeScene = -1;
  let activeNav = -1;
  const renderScroll = () => {
    queued = false;
    const height = window.innerHeight;
    const fullHeight = Math.max(1, document.documentElement.scrollHeight - height);
    progress.style.transform = `scaleX(${Math.min(1, Math.max(0, window.scrollY / fullHeight))})`;
    let currentNav = -1;
    navSections.forEach((section, i) => {
      if (section.getBoundingClientRect().top <= height * 0.4) currentNav = i;
    });
    if (currentNav !== activeNav) {
      activeNav = currentNav;
      navLinks.forEach((a, i) => {
        if (i === currentNav) a.setAttribute('aria-current', 'location');
        else a.removeAttribute('aria-current');
      });
    }
    if (mobile.matches || motion.matches) {
      playVisibleIllustrations();
      return;
    }
    let nearest = 0;
    let distance = Infinity;
    steps.forEach((step, i) => {
      const rect = step.getBoundingClientRect();
      const d = Math.abs(rect.top + rect.height / 2 - height / 2);
      if (d < distance) { distance = d; nearest = i; }
    });
    if (nearest !== activeScene) {
      activeScene = nearest;
      panels.forEach((panel, i) => panel.classList.toggle('is-active', i === nearest));
      markers.forEach((marker, i) => marker.classList.toggle('is-active', i === nearest));
      steps.forEach((step, i) => step.classList.toggle('is-current', i === nearest));
    }
    // Inactive sticky scenes overlap geometrically, but only the active one plays.
    playVisibleIllustrations();
    // No ongoing animation loop; movement stops when native scrolling stops.
    if (distance < height) {
      const rect = steps[nearest].getBoundingClientRect();
      const shift = Math.max(-1, Math.min(1, (rect.top + rect.height / 2 - height / 2) / height));
      scene.style.setProperty('--scene-shift', shift.toFixed(3));
    }
  };
  const scheduleScroll = () => {
    if (!queued) { queued = true; requestAnimationFrame(renderScroll); }
  };
  window.addEventListener('scroll', scheduleScroll, { passive: true });
  window.addEventListener('resize', scheduleScroll, { passive: true });
  onMediaChange(motion, () => { configureReveals(); configureIllustrations(); scheduleScroll(); });
  renderScroll();
  // Deep links and a language switch must expose their destination without a fade delay.
  const exposeHashTarget = () => {
    if (!location.hash) return;
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (target) {
      target.classList.add('is-visible');
      target.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('is-visible'));
    }
  };
  window.addEventListener('hashchange', exposeHashTarget);
  exposeHashTarget();
})();
