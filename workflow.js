(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('[data-workflow]').forEach(root => {
    const controls = root.querySelector('[data-flow-controls]');
    const buttons = [...root.querySelectorAll('[data-flow-step]')];
    const panels = [...root.querySelectorAll('[data-flow-panel]')];
    const title = root.querySelector('[data-flow-title]');
    if (!controls || !title || buttons.length !== panels.length || !panels.length) return;
    let current = -1;
    let animation;
    function select(index, focus = false) {
      if (index < 0 || index >= panels.length) return;
      if (focus) buttons[index].focus();
      if (index === current) return;
      current = index;
      panels.forEach((panel, i) => { panel.hidden = i !== index; });
      buttons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
      title.textContent = panels[index].dataset.title;
      animation?.cancel();
      if (!reduced.matches && document.documentElement.dataset.motion !== 'paused' && title.animate) {
        animation = title.animate([{opacity: .2, transform: 'translateY(8px)'}, {opacity: 1, transform: 'translateY(0)'}], {duration: 450, easing: 'ease-out'});
      }
    }
    buttons.forEach((button, i) => {
      button.addEventListener('click', () => select(i));
      button.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (i + 1) % buttons.length;
        if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (i + buttons.length - 1) % buttons.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = buttons.length - 1;
        if (next !== undefined) { event.preventDefault(); select(next, true); }
      });
    });
    root.classList.add('workflow-ready');
    select(0);
    controls.hidden = false;
    document.documentElement.addEventListener('portfolio:motion-change', () => {
      if (document.documentElement.dataset.motion === 'paused') animation?.cancel();
    });
    reduced.addEventListener('change', () => { if (reduced.matches) animation?.cancel(); });
    window.addEventListener('pagehide', () => animation?.cancel());
  });
})();
