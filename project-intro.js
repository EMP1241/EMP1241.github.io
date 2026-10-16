(() => {
  'use strict';
  const video = document.getElementById('project-intro-video');
  const replay = document.getElementById('replay-intro');
  if (!video || !replay || document.getElementById('project-intro-dialog')) return;

  const dialog = document.createElement('dialog');
  if (typeof dialog.showModal !== 'function') return;
  dialog.id = 'project-intro-dialog';
  dialog.className = 'project-intro-dialog';
  dialog.setAttribute('aria-labelledby', 'intro-dialog-title');
  dialog.innerHTML = '<div class="intro-toolbar"><div><span class="eyebrow">Brandon Santor · Independent software</span><h2 id="intro-dialog-title">Phal<span class="ai-emphasis">AI</span>nx</h2></div><button type="button" class="gallery-button" data-skip-intro>Skip intro · View project →</button></div><div class="intro-screen"></div><p class="intro-status" role="status"></p>';
  document.body.append(dialog);
  const screen = dialog.querySelector('.intro-screen');
  const skip = dialog.querySelector('[data-skip-intro]');
  const status = dialog.querySelector('.intro-status');
  const placeholder = document.createComment('Project introduction video position');
  video.before(placeholder);
  let returnFocus = null;
  let request = 0;

  function closeIntro() {
    ++request;
    video.pause();
    if (dialog.open) dialog.close();
    // Restore immediately; native dialog close events are queued asynchronously.
    placeholder.after(video);
    document.body.classList.remove('intro-open');
    const target = returnFocus?.isConnected ? returnFocus : document.getElementById('main');
    target?.focus({preventScroll: true});
    returnFocus = null;
  }

  async function openIntro(automatic) {
    if (dialog.open) return;
    returnFocus = automatic ? document.getElementById('main') : replay;
    const token = ++request;
    screen.append(video);
    video.pause();
    video.currentTime = 0;
    video.muted = true;
    status.textContent = 'Starts muted. Use the video controls for sound, or skip to the project.';
    dialog.showModal();
    document.body.classList.add('intro-open');
    skip.focus();
    if (automatic && matchMedia('(prefers-reduced-motion: reduce)').matches) {
      status.textContent = 'Reduced motion is enabled. Select Play to watch, or skip to the project.';
      return;
    }
    try {
      await video.play();
    } catch {
      if (token === request && dialog.open) status.textContent = 'Select Play to watch the introduction, or skip to the project.';
    }
  }

  replay.hidden = false;
  replay.addEventListener('click', () => openIntro(false));
  skip.addEventListener('click', closeIntro);
  dialog.addEventListener('cancel', event => { event.preventDefault(); closeIntro(); });
  dialog.addEventListener('close', () => {
    if (!dialog.open && video.parentElement === screen) closeIntro();
  });
  video.addEventListener('ended', () => { if (dialog.open) closeIntro(); });
  function mediaError() {
    if (dialog.open) {
      ++request;
      status.textContent = 'The introduction could not load. Skip to the project to continue.';
    }
  }
  video.addEventListener('error', mediaError);
  // Source-element failures do not bubble to the video element.
  video.querySelectorAll('source').forEach(source => source.addEventListener('error', mediaError));
  document.addEventListener('visibilitychange', () => { if (document.hidden) video.pause(); });
  window.addEventListener('pagehide', () => video.pause());

  const url = new URL(location.href);
  if (url.searchParams.get('intro') === '1') {
    url.searchParams.delete('intro');
    history.replaceState(history.state, '', url.pathname + url.search + url.hash);
    openIntro(true);
  }
})();
