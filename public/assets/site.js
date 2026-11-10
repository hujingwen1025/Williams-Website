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
  const readingSections = [...document.querySelectorAll('main > section[id], .feature-card[id], .repo-card[id], .interest-card[id]')];
  const updateLanguageLink = (keepReadingPosition = false) => {
    const target = new URL(language.getAttribute('href'), location.href);
    target.hash = location.hash;
    if (keepReadingPosition) {
      let current = 'top';
      let anchored = null;
      try { anchored = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch { /* A malformed hash is still a usable URL. */ }
      readingSections.forEach(section => {
        if (!section.hidden && section.getClientRects().length && section.getBoundingClientRect().top <= window.innerHeight * 0.5) current = section.id;
      });
      if (anchored) {
        const box = anchored.getBoundingClientRect();
        if (box.top >= 0 && box.top < window.innerHeight && box.bottom > 0) current = anchored.id;
      }
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

  // The page is composed and visible by default. Only the glyph field moves.
  const canvas = document.querySelector('#ascii-field');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    const sample = document.createElement('canvas');
    const ink = sample.getContext('2d', { willReadFrequently: true });
    const hero = canvas.closest('.hero');
    const glyphs = ' .:+*#%@';
    let cells = [], width = 0, height = 0, visible = true, frame = 0;
    let lens = null;
    let started = performance.now();
    let last = 0;
    const style = getComputedStyle(root);
    const palette = [1, 2, 3, 4].map(i => style.getPropertyValue(`--color-glyph-${i}`).trim());
    const draw = (time = 0) => {
      if (!ctx || !ink) return;
      ctx.clearRect(0, 0, width, height);
      ctx.font = `12px ${style.getPropertyValue('--font-outlier')}`;
      ctx.textBaseline = 'top';
      const small = width < 701;
      cells.forEach(cell => {
        const distance = lens ? Math.hypot(cell.x - lens.x, cell.y - lens.y) : Infinity;
        const phase = Math.sin(cell.x * 0.017 + cell.y * 0.009 + time * 0.0004);
        const density = Math.min(1, cell.density + (distance < 100 ? 0.15 * (1 - distance / 100) : 0));
        const shade = small ? Math.min(1, Math.floor(density * 3)) : Math.min(3, Math.floor(density * 3));
        ctx.fillStyle = palette[shade];
        const index = Math.max(1, Math.min(glyphs.length - 1, Math.floor(density * 6 + phase * 0.7)));
        ctx.fillText(glyphs[index], cell.x, cell.y);
      });
      canvas.dataset.ready = 'true';
    };
    const resize = () => {
      if (!ctx || !ink) return;
      width = Math.round(hero.clientWidth);
      height = Math.round(hero.clientHeight);
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      sample.width = width;
      sample.height = height;
      const small = width < 701;
      const size = small ? Math.min(height * 0.8, 500) : Math.min(width * 0.5, height * 0.82);
      ink.font = `600 ${size}px ${style.getPropertyValue('--font-display')}`;
      ink.textAlign = 'center';
      ink.textBaseline = 'middle';
      ink.fillText('W', width * (small ? 0.94 : 0.77), height * 0.48);
      const pixels = ink.getImageData(0, 0, width, height).data;
      cells = [];
      for (let y = 16; y < height - 16; y += 16) {
        for (let x = Math.floor(width * (small ? 0.58 : 0.52) / 8) * 8; x < width; x += 8) {
          const a = pixels[(y * width + x) * 4 + 3] / 255;
          const wave = Math.sin(x * 0.007) * 32;
          const contour = Math.min(...[0.28, 0.5, 0.72].map(band => Math.abs(y - height * band - wave)));
          if (a > 0.15) cells.push({ x, y, density: 0.35 + a * 0.35 + ((x + y) % 37) / 150 });
          else if (contour < 24) cells.push({ x, y, density: 0.05 + (1 - contour / 24) * 0.14 });
        }
      }
      draw(motion.matches ? 0 : Math.min(performance.now() - started, 4000));
    };
    const animate = time => {
      frame = 0;
      const elapsed = time - started;
      if (motion.matches || !visible || document.hidden || elapsed > 4000) return;
      if (time - last >= 1000 / 30) { draw(elapsed); last = time; }
      frame = requestAnimationFrame(animate);
    };
    const resume = () => {
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
      if (!motion.matches && visible && !document.hidden && performance.now() - started <= 4000) frame = requestAnimationFrame(animate);
      else draw(0);
    };
    if (ctx && ink) {
      resize();
      document.fonts.ready.then(() => { started = performance.now(); resize(); resume(); });
      if ('ResizeObserver' in window) new ResizeObserver(resize).observe(hero);
      else window.addEventListener('resize', resize, { passive: true });
      if ('IntersectionObserver' in window) new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; resume(); }).observe(hero);
      hero.addEventListener('pointermove', event => {
        if (motion.matches || !visible) return;
        const box = hero.getBoundingClientRect();
        lens = { x: event.clientX - box.left, y: event.clientY - box.top };
        if (!frame) draw(4000);
      }, { passive: true });
      hero.addEventListener('pointerleave', () => { lens = null; if (!frame) draw(0); });
      onMediaChange(motion, () => { lens = null; resume(); });
      document.addEventListener('visibilitychange', resume);
    }
  }

  // Track native reading position without changing scroll behavior.
  const navLinks = [...navigation.querySelectorAll('a[href^="#"]')];
  const navSections = navLinks.map(a => document.getElementById(a.hash.slice(1)));
  let queued = false;
  const renderScroll = () => {
    queued = false;
    const fullHeight = Math.max(1, root.scrollHeight - window.innerHeight);
    progress.style.transform = `scaleX(${Math.min(1, Math.max(0, window.scrollY / fullHeight))})`;
    let current = -1;
    navSections.forEach((section, i) => {
      if (section && section.getBoundingClientRect().top <= window.innerHeight * 0.4) current = i;
    });
    navLinks.forEach((a, i) => {
      if (i === current) a.setAttribute('aria-current', 'location');
      else a.removeAttribute('aria-current');
    });
  };
  const scheduleScroll = () => {
    if (!queued) { queued = true; requestAnimationFrame(renderScroll); }
  };
  window.addEventListener('scroll', scheduleScroll, { passive: true });
  window.addEventListener('resize', scheduleScroll, { passive: true });
  renderScroll();

  // Existing project deep links open their native disclosure and stay visible.
  const exposeHashTarget = () => {
    if (!location.hash) return;
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    if (target.classList.contains('repo-card')) {
      if (target.hidden) { search.value = ''; filters[0].click(); }
      target.querySelector('details').open = true;
      requestAnimationFrame(() => target.scrollIntoView({ block: 'start', behavior: 'instant' }));
    }
  };
  window.addEventListener('hashchange', exposeHashTarget);
  exposeHashTarget();
})();
