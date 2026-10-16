(() => {
  'use strict';
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const toggle = document.querySelector('[data-motion-toggle]');
  const sections = [...document.querySelectorAll('.hero, .project-hero, .project-content')];
  const visible = new Set();
  const highlights = [...document.querySelectorAll('[data-highlights]')].map(el => ({
    el, panels: [...el.querySelectorAll('[data-hero-highlight]')], buttons: [...el.querySelectorAll('[data-highlight-select]')],
    current: 0, visible: true, hover: false, focus: false, timer: null, animations: [], request: 0
  }));
  let paused = false;
  let away = false;
  let frame = null;
  try { paused = localStorage.getItem('portfolio-motion') === 'paused'; } catch {}
  const enabled = () => !paused && !reduced.matches && !away && !document.hidden;
  function cancelTimer(item) { clearTimeout(item.timer); item.timer = null; }
  function schedule(item) {
    cancelTimer(item);
    if (!enabled() || !item.visible || item.hover || item.focus || item.panels.length < 2) return;
    item.timer = setTimeout(() => { show(item, (item.current + 1) % item.panels.length, true); }, 8500);
  }
  async function show(item, index, automatic = false) {
    if (index < 0 || index >= item.panels.length) return;
    const request = ++item.request;
    cancelTimer(item);
    item.animations.forEach(a => a.cancel()); item.animations = [];
    if (automatic && enabled() && item.panels[item.current].animate) {
      const outgoing = item.panels[item.current].animate([{opacity: 1}, {opacity: 0}], {duration: 1000, easing: 'ease-in-out'});
      item.animations.push(outgoing);
      try { await outgoing.finished; } catch {}
      if (request !== item.request || !enabled() || item.hover || item.focus || !item.visible) return;
    }
    item.current = index;
    item.panels.forEach((panel, i) => { panel.hidden = i !== index; });
    item.buttons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
    const panel = item.panels[index];
    if (enabled() && panel.animate) item.animations.push(panel.animate([{opacity: 0}, {opacity: 1}], {duration: 1600, easing: 'ease-in-out'}));
    schedule(item);
  }
  function draw() {
    frame = null;
    if (!enabled()) return;
    visible.forEach(el => {
      const box = el.getBoundingClientRect();
      const offset = Math.max(-34, Math.min(34, (innerHeight / 2 - box.top - box.height / 2) * .055));
      el.style.setProperty('--parallax-y', `${offset.toFixed(1)}px`);
    });
  }
  function queue() { if (enabled() && frame === null && visible.size) frame = requestAnimationFrame(draw); }
  function sync() {
    root.dataset.motion = paused || reduced.matches ? 'paused' : 'playing';
    if (toggle) {
      toggle.textContent = reduced.matches ? 'Reduced motion' : paused ? 'Resume effects' : 'Pause effects';
      toggle.setAttribute('aria-label', toggle.textContent);
      toggle.title = toggle.textContent;
      toggle.setAttribute('aria-pressed', String(paused || reduced.matches));
      toggle.disabled = reduced.matches;
      toggle.hidden = false;
    }
    if (!enabled()) {
      if (frame !== null) cancelAnimationFrame(frame); frame = null;
      sections.forEach(el => el.style.setProperty('--parallax-y', '0px'));
      highlights.forEach(item => { ++item.request; cancelTimer(item); item.animations.forEach(a => a.cancel()); });
    } else { highlights.forEach(schedule); queue(); }
    root.dispatchEvent(new CustomEvent('portfolio:motion-change'));
  }
  highlights.forEach(item => {
    item.buttons.forEach((button, i) => button.addEventListener('click', () => show(item, i)));
    item.el.querySelector('[data-highlight-controls]').hidden = false;
    item.el.classList.add('highlights-ready');
    item.el.addEventListener('mouseenter', () => { item.hover = true; cancelTimer(item); });
    item.el.addEventListener('mouseleave', () => { item.hover = false; schedule(item); });
    item.el.addEventListener('focusin', () => { item.focus = true; cancelTimer(item); });
    item.el.addEventListener('focusout', event => { if (!item.el.contains(event.relatedTarget)) { item.focus = false; schedule(item); } });
  });
  let observer;
  if ('IntersectionObserver' in window) {
    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (sections.includes(entry.target)) {
          if (entry.isIntersecting) visible.add(entry.target); else visible.delete(entry.target);
        }
        const item = highlights.find(x => x.el === entry.target);
        if (item) { item.visible = entry.isIntersecting; schedule(item); }
      });
      queue();
    });
    sections.forEach(el => observer.observe(el)); highlights.forEach(item => observer.observe(item.el));
  } else sections.forEach(el => visible.add(el));
  toggle?.addEventListener('click', () => {
    paused = !paused;
    try { localStorage.setItem('portfolio-motion', paused ? 'paused' : 'playing'); } catch {}
    sync();
  });
  reduced.addEventListener('change', sync);
  window.addEventListener('storage', event => {
    if (event.key === 'portfolio-motion' || event.key === null) { paused = event.newValue === 'paused'; sync(); }
  });
  window.addEventListener('scroll', queue, {passive: true});
  window.addEventListener('resize', queue, {passive: true});
  document.addEventListener('visibilitychange', sync);
  window.addEventListener('pagehide', () => { away = true; sync(); observer?.disconnect(); });
  window.addEventListener('pageshow', () => {
    away = false;
    sections.forEach(el => observer?.observe(el)); highlights.forEach(item => observer?.observe(item.el));
    sync();
  });
  sync();
})();
