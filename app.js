(() => {
  'use strict';

  const $ = (selector, root = document) => root?.querySelector(selector) ?? null;
  const $$ = (selector, root = document) => [...(root?.querySelectorAll(selector) ?? [])];
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const mobileMenu = matchMedia('(max-width: 760px)');
  const connection = navigator.connection;
  const storageKey = 'ma-cakr-motion';
  const motionButton = $('.motion-toggle');
  const memory = navigator.deviceMemory || 8;
  const cores = navigator.hardwareConcurrency || 8;
  const constrainedDevice = memory <= 4 || cores <= 4;
  let preference = null;

  for (const kind of ['localStorage', 'sessionStorage']) {
    try {
      const saved = window[kind].getItem(storageKey);
      if (saved === 'on' || saved === 'off') { preference = saved; break; }
    } catch (_) { /* The site also works when browser storage is unavailable. */ }
  }

  const automaticallyPaused = () => Boolean(connection?.saveData || memory <= 2 || cores <= 2);
  const effectsAllowed = () => !reduce.matches && (preference ? preference === 'on' : !automaticallyPaused());
  const animate = () => effectsAllowed() && !document.hidden;
  const pointerAllowed = () => animate() && finePointer.matches;
  const watchMedia = (query, callback) => {
    if (query.addEventListener) query.addEventListener('change', callback);
    else query.addListener(callback);
  };

  // The small-screen navigation remains a keyboard-operable disclosure.
  const menuButton = $('.menu-toggle');
  const menu = $('#navigation');
  function setMenu(open) {
    if (!menuButton || !menu) return;
    menuButton.setAttribute('aria-expanded', String(open));
    menu.classList.toggle('is-open', open);
    menu.inert = mobileMenu.matches && !open;
    if (mobileMenu.matches && !open) menu.setAttribute('aria-hidden', 'true');
    else menu.removeAttribute('aria-hidden');
  }
  const closeMenu = () => setMenu(false);
  menuButton?.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
  $$('a', menu).forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menuButton.focus();
    }
  });
  document.addEventListener('click', event => {
    if (event.target instanceof Element && !event.target.closest('.site-header')) closeMenu();
  });
  watchMedia(mobileMenu, closeMenu);
  closeMenu();

  // Content is visible by default, including when observers are unsupported.
  const reveals = $$('.reveal');
  let revealObserver = null;
  function revealEverything() {
    revealObserver?.disconnect();
    reveals.forEach(element => element.classList.add('is-visible'));
  }
  if ('IntersectionObserver' in window && effectsAllowed()) {
    try {
      revealObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        });
      }, { threshold: 0.04, rootMargin: '0px 0px -12px 0px' });
      document.documentElement.classList.add('js-ready');
      reveals.forEach(element => revealObserver.observe(element));
    } catch (_) { revealEverything(); }
  } else revealEverything();

  // Search uses the page language so Turkish dotted/dotless I behave naturally.
  const language = document.documentElement.lang || 'en';
  const normalize = text => String(text || '').toLocaleLowerCase(language)
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ı/g, 'i');
  const search = $('#note-search');
  const noteCards = $$('.note-card');
  const topics = $$('.topic-filter');
  const countLabel = $('.result-count');
  const clearSearch = $('.clear-search');
  const noResults = $('.no-results');
  let activeTopic = 'all';
  function filterNotes() {
    if (!search) return;
    const words = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    let count = 0;
    noteCards.forEach(card => {
      const matches = (activeTopic === 'all' || card.dataset.topic === activeTopic)
        && words.every(word => normalize(card.dataset.search || card.textContent).includes(word));
      card.hidden = !matches;
      if (matches) { card.classList.add('is-visible'); count += 1; }
    });
    if (countLabel) {
      const unit = count === 1 && language.startsWith('en') ? 'note' : (countLabel.dataset.unit || 'notes');
      countLabel.textContent = count + ' ' + unit;
    }
    if (noResults) noResults.hidden = count !== 0;
    if (clearSearch) clearSearch.hidden = search.value.length === 0;
    scrollDirty = true;
    scheduleFrame();
  }
  search?.addEventListener('input', filterNotes);
  clearSearch?.addEventListener('click', () => {
    search.value = '';
    filterNotes();
    search.focus();
  });
  topics.forEach(button => button.addEventListener('click', () => {
    activeTopic = button.dataset.topic;
    topics.forEach(other => {
      const active = other === button;
      other.classList.toggle('is-active', active);
      other.setAttribute('aria-pressed', String(active));
    });
    filterNotes();
  }));

  const spotlight = $('.pointer-glow');
  const progress = $('.scroll-progress');
  const header = $('.site-header');
  const canvas = $('#ambient-trail');
  let context = null;
  try { context = canvas?.getContext('2d', { alpha: true }) ?? null; } catch (_) {}
  const cards = $$('.project-card, .note-card, .portrait-frame, .about-portrait, .cv-strip, [data-tilt]');
  const magneticControls = $$('.magnetic');
  const navSections = $$('a[href*="#"]', menu).map(link => {
    const url = new URL(link.href, location.href);
    if (url.origin !== location.origin || url.pathname !== location.pathname || !url.hash) return null;
    let target;
    try { target = document.getElementById(decodeURIComponent(url.hash.slice(1))); } catch (_) {}
    return target ? { link, target } : null;
  }).filter(Boolean);
  let width = innerWidth;
  let height = innerHeight;
  let nodes = [];
  let frame = null;
  let lastPaint = 0;
  let sizeDirty = true;
  let scrollDirty = true;
  let currentCard = null;
  let currentMagnet = null;
  const pointer = { x: width / 2, y: height / 2, drawnX: width / 2, drawnY: height / 2, visible: false };

  function resetCard(element) {
    if (!element) return;
    element.style.setProperty('--tilt-x', '0deg');
    element.style.setProperty('--tilt-y', '0deg');
    element.style.setProperty('--glow-x', '50%');
    element.style.setProperty('--glow-y', '50%');
  }
  function resetMagnet(element) {
    if (!element) return;
    element.style.setProperty('--magnetic-x', '0px');
    element.style.setProperty('--magnetic-y', '0px');
  }
  function clearPointer() {
    pointer.visible = false;
    spotlight?.style.setProperty('--pointer-opacity', '0');
    resetCard(currentCard);
    resetMagnet(currentMagnet);
    currentCard = currentMagnet = null;
  }
  function resizeCanvas() {
    width = innerWidth;
    height = innerHeight;
    if (context) {
      const ratio = Math.min(devicePixelRatio || 1, 1.5);
      canvas.width = Math.round(width * ratio);
      canvas.height = Math.round(height * ratio);
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      const count = Math.min(constrainedDevice ? 18 : 32, width <= 760 ? 14 : width <= 1100 ? 24 : 32);
      nodes = Array.from({ length: count }, () => ({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 13,
        vy: (Math.random() - 0.5) * 13,
        radius: Math.random() * 0.8 + 1,
      }));
    }
    sizeDirty = false;
    scrollDirty = true;
  }
  function updateScroll() {
    const top = Math.max(0, window.scrollY);
    const maximum = Math.max(0, document.documentElement.scrollHeight - height);
    progress?.style.setProperty('--scroll-progress', String(maximum ? clamp(top / maximum, 0, 1) : 0));
    header?.classList.toggle('is-scrolled', top > 18);
    let active = null;
    const boundary = Math.min(height * 0.36, 240);
    navSections.forEach(section => {
      if (section.target.getBoundingClientRect().top <= boundary) active = section;
    });
    if (maximum > 0 && maximum - top < 6) active = navSections.at(-1) || active;
    navSections.forEach(section => {
      const selected = section === active;
      section.link.classList.toggle('is-active', selected);
      if (selected) section.link.setAttribute('aria-current', 'location');
      else section.link.removeAttribute('aria-current');
    });
    scrollDirty = false;
  }
  function updateHover(delta) {
    if (!pointerAllowed() || !pointer.visible) return false;
    const ease = Math.min(1, delta * 12);
    pointer.drawnX += (pointer.x - pointer.drawnX) * ease;
    pointer.drawnY += (pointer.y - pointer.drawnY) * ease;
    spotlight?.style.setProperty('--pointer-x', pointer.drawnX.toFixed(1) + 'px');
    spotlight?.style.setProperty('--pointer-y', pointer.drawnY.toFixed(1) + 'px');
    spotlight?.style.setProperty('--pointer-opacity', '1');
    if (currentCard) {
      const box = currentCard.getBoundingClientRect();
      const x = clamp((pointer.x - box.left) / box.width, 0, 1);
      const y = clamp((pointer.y - box.top) / box.height, 0, 1);
      currentCard.style.setProperty('--tilt-x', ((0.5 - y) * 4).toFixed(2) + 'deg');
      currentCard.style.setProperty('--tilt-y', ((x - 0.5) * 4).toFixed(2) + 'deg');
      currentCard.style.setProperty('--glow-x', (x * 100).toFixed(1) + '%');
      currentCard.style.setProperty('--glow-y', (y * 100).toFixed(1) + '%');
    }
    if (currentMagnet) {
      const box = currentMagnet.getBoundingClientRect();
      const x = clamp((pointer.x - box.left - box.width / 2) * 0.06, -3, 3);
      const y = clamp((pointer.y - box.top - box.height / 2) * 0.07, -3, 3);
      currentMagnet.style.setProperty('--magnetic-x', x.toFixed(2) + 'px');
      currentMagnet.style.setProperty('--magnetic-y', y.toFixed(2) + 'px');
    }
    return Math.abs(pointer.x - pointer.drawnX) + Math.abs(pointer.y - pointer.drawnY) > 0.5;
  }
  function drawNetwork(delta) {
    if (!context) return;
    context.clearRect(0, 0, width, height);
    const reach = width <= 760 ? 135 : 175;
    const interactive = pointer.visible && finePointer.matches;
    nodes.forEach(node => {
      node.x += node.vx * delta;
      node.y += node.vy * delta;
      if (node.x < -12) node.x = width + 12;
      if (node.x > width + 12) node.x = -12;
      if (node.y < -12) node.y = height + 12;
      if (node.y > height + 12) node.y = -12;
    });
    context.lineWidth = 0.65;
    for (let index = 0; index < nodes.length; index += 1) {
      const node = nodes[index];
      for (let next = index + 1; next < nodes.length; next += 1) {
        const other = nodes[next];
        const distance = Math.hypot(node.x - other.x, node.y - other.y);
        if (distance >= reach) continue;
        context.strokeStyle = 'rgba(100,165,239,' + ((1 - distance / reach) * 0.19).toFixed(3) + ')';
        context.beginPath();
        context.moveTo(node.x, node.y);
        context.lineTo(other.x, other.y);
        context.stroke();
      }
      const nearby = interactive ? Math.hypot(node.x - pointer.x, node.y - pointer.y) : Infinity;
      if (nearby < 185) {
        context.strokeStyle = 'rgba(95,200,239,' + ((1 - nearby / 185) * 0.24).toFixed(3) + ')';
        context.beginPath();
        context.moveTo(node.x, node.y);
        context.lineTo(pointer.x, pointer.y);
        context.stroke();
      }
      context.fillStyle = nearby < 185 ? 'rgba(130,218,252,0.65)' : 'rgba(116,166,230,0.31)';
      context.beginPath();
      context.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
      context.fill();
    }
  }
  function scheduleFrame() {
    if (frame === null && !document.hidden) frame = requestAnimationFrame(renderFrame);
  }
  function renderFrame(now) {
    frame = null;
    if (document.hidden) return;
    if (lastPaint && now - lastPaint < 1000 / 30) { scheduleFrame(); return; }
    const delta = lastPaint ? Math.min((now - lastPaint) / 1000, 0.08) : 1 / 30;
    lastPaint = now;
    if (sizeDirty) resizeCanvas();
    if (scrollDirty) updateScroll();
    const pointerMoving = updateHover(delta);
    if (animate()) drawNetwork(delta);
    if ((context && animate()) || pointerMoving) scheduleFrame();
  }

  cards.forEach(element => {
    element.addEventListener('pointerenter', event => {
      if (!pointerAllowed() || event.pointerType === 'touch') return;
      resetCard(currentCard);
      currentCard = element;
    });
    element.addEventListener('pointerleave', () => {
      resetCard(element);
      if (currentCard === element) currentCard = null;
    });
  });
  magneticControls.forEach(element => {
    element.addEventListener('pointerenter', event => {
      if (!pointerAllowed() || event.pointerType === 'touch') return;
      resetMagnet(currentMagnet);
      currentMagnet = element;
    });
    const reset = () => {
      resetMagnet(element);
      if (currentMagnet === element) currentMagnet = null;
    };
    element.addEventListener('pointerleave', reset);
    element.addEventListener('blur', reset);
  });
  document.addEventListener('pointermove', event => {
    if (!pointerAllowed() || event.pointerType === 'touch') return;
    pointer.x = event.clientX;
    pointer.y = event.clientY;
    if (!pointer.visible) { pointer.drawnX = pointer.x; pointer.drawnY = pointer.y; }
    pointer.visible = true;
    scheduleFrame();
  }, { passive: true });
  document.addEventListener('pointerleave', clearPointer);
  window.addEventListener('blur', clearPointer);
  watchMedia(finePointer, clearPointer);
  window.addEventListener('scroll', () => { scrollDirty = true; scheduleFrame(); }, { passive: true });
  window.addEventListener('resize', () => { sizeDirty = true; scheduleFrame(); }, { passive: true });
  window.addEventListener('load', () => { scrollDirty = true; scheduleFrame(); }, { once: true });
  document.fonts?.ready.then(() => { scrollDirty = true; scheduleFrame(); });

  // This is the real local time in Istanbul, never simulated activity.
  const clockElements = $$('[data-clock]');
  let clockTimer = null;
  let clockFormat = null;
  try {
    clockFormat = new Intl.DateTimeFormat(language, {
      timeZone: 'Europe/Istanbul', hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
    });
  } catch (_) {}
  function updateClock() {
    if (clockTimer !== null) clearTimeout(clockTimer);
    clockTimer = null;
    if (document.hidden || !clockElements.length || !clockFormat) return;
    const now = new Date();
    clockElements.forEach(element => {
      element.textContent = clockFormat.format(now);
      if (element.tagName === 'TIME') element.dateTime = now.toISOString();
    });
    clockTimer = setTimeout(updateClock, 60000 - (Date.now() % 60000) + 50);
  }

  function syncMotion() {
    const off = !effectsAllowed();
    document.body.classList.toggle('motion-paused', off);
    document.body.classList.toggle('page-hidden', document.hidden);
    document.body.classList.toggle('effects-lite', constrainedDevice && preference !== 'on');
    if (motionButton) {
      motionButton.setAttribute('aria-pressed', String(off));
      motionButton.disabled = reduce.matches;
      const label = reduce.matches ? motionButton.dataset.reduced
        : off ? motionButton.dataset.resume : motionButton.dataset.pause;
      if (label) {
        const span = $('span', motionButton);
        if (span) span.textContent = label;
        motionButton.setAttribute('aria-label', label);
      }
    }
    if (off || document.hidden) {
      clearPointer();
      context?.clearRect(0, 0, width, height);
      if (frame !== null) cancelAnimationFrame(frame);
      frame = null;
      lastPaint = 0;
      if (off) revealEverything();
    }
    scrollDirty = true;
    scheduleFrame();
  }
  motionButton?.addEventListener('click', () => {
    preference = effectsAllowed() ? 'off' : 'on';
    for (const kind of ['localStorage', 'sessionStorage']) {
      try { window[kind].setItem(storageKey, preference); } catch (_) {}
    }
    syncMotion();
  });
  window.addEventListener('storage', event => {
    if (event.key !== storageKey) return;
    preference = event.newValue === 'on' || event.newValue === 'off' ? event.newValue : null;
    syncMotion();
  });
  watchMedia(reduce, syncMotion);
  connection?.addEventListener?.('change', syncMotion);
  document.addEventListener('visibilitychange', () => { syncMotion(); updateClock(); });
  syncMotion();
  updateClock();
})();
