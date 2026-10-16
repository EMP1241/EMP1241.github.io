(() => {
  'use strict';
  const root = document.documentElement;
  const toggle = document.getElementById('theme-toggle');
  const label = document.getElementById('theme-label');
  function setTheme(theme, persist = false) {
    const dark = theme !== 'light';
    root.dataset.theme = dark ? 'dark' : 'light';
    if (toggle) toggle.setAttribute('aria-pressed', String(dark));
    if (label) label.textContent = dark ? 'Dark' : 'Light';
    if (persist) {
      try { localStorage.setItem('portfolio-theme', root.dataset.theme); } catch {}
    }
  }
  setTheme(root.dataset.theme);
  if (toggle) {
    toggle.hidden = false;
    toggle.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark', true));
  }
  window.addEventListener('storage', event => {
    if (event.key === 'portfolio-theme' || event.key === null) setTheme(event.newValue === 'light' ? 'light' : 'dark');
  });

  // Preserve links shared while the portfolio was a single page.
  if (document.body.dataset.page === 'index.html') {
    const legacyPages = {
      about: 'about.html', projects: 'projects.html', resume: 'resume.html',
      nwsw: 'project-nwsw.html', trae: 'project-trae.html', tvae: 'project-tvae.html',
      'research-architect': 'project-research-architect.html', gnss: 'project-gnss.html'
    };
    function followLegacyLink() {
      let id;
      try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
      if (Object.hasOwn(legacyPages, id)) location.replace(legacyPages[id]);
    }
    followLegacyLink();
    window.addEventListener('hashchange', followLegacyLink);
  }

  const printButton = document.getElementById('print-resume');
  if (printButton) {
    printButton.hidden = false;
    printButton.addEventListener('click', () => {
      try { window.print(); } catch {
        const status = document.getElementById('action-status');
        if (status) status.textContent = 'The print dialog could not open. Download the PDF or use your browser’s Print command.';
      }
    });
  }
})();
