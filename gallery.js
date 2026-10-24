(() => {
  'use strict';
  const galleries = [...document.querySelectorAll('[data-gallery]')];
  const imageSets = [...document.querySelectorAll('[data-image-set]')];
  if ((!galleries.length && !imageSets.length) || document.getElementById('media-lightbox')) return;

  const dialog = document.createElement('dialog');
  dialog.id = 'media-lightbox';
  dialog.className = 'media-lightbox';
  dialog.setAttribute('aria-labelledby', 'lightbox-title');
  dialog.setAttribute('aria-describedby', 'lightbox-caption');
  dialog.innerHTML = `<div class="lightbox-header"><div><span class="eyebrow">Project gallery</span><h2 id="lightbox-title"></h2></div><button type="button" class="gallery-button" data-close aria-label="Close gallery">Close <span aria-hidden="true">×</span></button></div><div class="lightbox-toolbar"><button type="button" class="gallery-button" data-prev aria-label="Previous item">← Previous</button><span data-position aria-live="polite"></span><button type="button" class="gallery-button" data-next aria-label="Next item">Next →</button><button type="button" class="gallery-button" data-zoom aria-pressed="false">Full resolution</button></div><div class="lightbox-viewport" tabindex="0" aria-label="Image viewport. At full resolution, scroll to inspect the image."><img class="lightbox-image" alt=""><video class="lightbox-video" controls muted loop playsinline preload="metadata" tabindex="0" hidden></video><p class="lightbox-loading" role="status"></p></div><p class="lightbox-caption" id="lightbox-caption"></p><a class="lightbox-original" href="#" target="_blank" rel="noopener">Open original image in a new tab ↗</a>`;
  const supportsDialog = typeof dialog.showModal === 'function';
  if (supportsDialog) document.body.append(dialog);
  const image = dialog.querySelector('img');
  const video = dialog.querySelector('video');
  const viewport = dialog.querySelector('.lightbox-viewport');
  const position = dialog.querySelector('[data-position]');
  const caption = dialog.querySelector('.lightbox-caption');
  const loading = dialog.querySelector('.lightbox-loading');
  const zoomButton = dialog.querySelector('[data-zoom]');
  let activeGallery = null;
  let returnFocus = null;
  let zoomed = false;
  let imageRequest = 0;
  const states = [];
  const manualPlayback = new WeakSet();
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let away = false;
  const canAutoplay = () => !away && !document.hidden && !reduced.matches && document.documentElement.dataset.motion !== 'paused';

  function syncSlideshow(state) {
    clearTimeout(state.timer);
    state.timer = null;
    const enabled = canAutoplay();
    const clip = state.slides[state.index].querySelector('video');
    // A resting pointer should not strand a completed demo. Image reading and
    // keyboard/native-player interaction still suspend automatic navigation.
    const running = enabled && !state.paused && state.visible && (!state.hover || clip) && !state.focus && !dialog.open && state.slides.length > 1;
    if (state.count) state.count.setAttribute('aria-live', running ? 'off' : 'polite');
    if (state.rotation) {
      state.rotation.disabled = !enabled;
      state.rotation.textContent = reduced.matches ? 'Reduced motion' : !enabled ? 'Effects paused' : state.paused ? 'Resume slideshow' : 'Pause slideshow';
    }
    if (!running) return;
    const remaining = clip && Number.isFinite(clip.duration) ? Math.max(0, clip.duration - (clip.currentTime || 0)) * 1000 : 0;
    // Ended is the normal trigger. The fallback also releases an unavailable
    // or stalled preview rather than freezing the entire gallery.
    const delay = clip ? clip.ended ? 500 : Math.max(15000, remaining + 5000) : 7000;
    state.timer = setTimeout(() => {
      state.timer = null;
      state.step(1);
    }, delay);
  }

  function playMuted(clip) {
    if (manualPlayback.has(clip)) return;
    clip.muted = true;
    clip.play()?.catch(() => {}); // Native controls remain available if autoplay is blocked.
  }

  function syncGalleryPlayback() {
    states.forEach(state => {
      syncSlideshow(state);
      state.slides.forEach((slide, index) => {
        const clip = slide.querySelector('video');
        if (!clip) return;
        if (index === state.index && state.visible && !dialog.open && canAutoplay()) { if (!clip.ended) playMuted(clip); }
        else clip.pause();
      });
    });
    if (dialog.open && !video.hidden && video.hasAttribute('src')) {
      if (canAutoplay()) playMuted(video);
      else video.pause();
    }
  }

  function clearLightboxVideo() {
    video.pause();
    manualPlayback.delete(video);
    video.onloadeddata = null;
    video.onerror = null;
    video.removeAttribute('src');
    video.removeAttribute('poster');
    video.hidden = true;
    video.load();
  }

  function setZoom(next) {
    zoomed = next;
    viewport.classList.toggle('is-zoomed', next);
    image.style.width = next && image.naturalWidth ? `${image.naturalWidth}px` : '';
    zoomButton.setAttribute('aria-pressed', String(next));
    zoomButton.textContent = next ? 'Fit image' : 'Full resolution';
    viewport.scrollTop = 0;
    viewport.scrollLeft = 0;
  }

  function renderLightbox() {
    if (!activeGallery) return;
    const slide = activeGallery.slides[activeGallery.index];
    const source = slide.querySelector('img, video');
    const text = slide.querySelector('figcaption').textContent.trim();
    const token = ++imageRequest;
    setZoom(false);
    clearLightboxVideo();
    image.onload = null;
    image.onerror = null;
    image.removeAttribute('src');
    image.hidden = true;
    const isVideo = source.tagName === 'VIDEO';
    viewport.classList.toggle('is-video', isVideo);
    viewport.style.aspectRatio = isVideo ? `${source.width || 16} / ${source.height || 9}` : '';
    zoomButton.hidden = isVideo;
    viewport.setAttribute('aria-label', isVideo ? 'Video player. Use the controls to play or pause the clip.' : 'Image viewport. At full resolution, scroll to inspect the image.');
    const original = dialog.querySelector('.lightbox-original');
    original.href = source.getAttribute('src');
    original.textContent = `Open original ${isVideo ? 'video' : 'image'} in a new tab ↗`;
    dialog.querySelector('#lightbox-title').textContent = activeGallery.title;
    position.textContent = `${activeGallery.index + 1} / ${activeGallery.slides.length}`;
    caption.textContent = text;
    dialog.querySelector('[data-prev]').disabled = activeGallery.slides.length < 2;
    dialog.querySelector('[data-next]').disabled = activeGallery.slides.length < 2;
    loading.textContent = isVideo ? 'Loading video…' : 'Loading image…';
    if (isVideo) {
      video.setAttribute('aria-label', source.getAttribute('aria-label') || 'Project demonstration');
      if (source.getAttribute('poster')) video.poster = source.getAttribute('poster');
      video.onloadeddata = () => { if (token === imageRequest) loading.textContent = ''; };
      video.onerror = () => {
        if (token !== imageRequest) return;
        video.pause();
        loading.textContent = 'The video could not load. Try another item or open the original below.';
      };
      video.src = source.getAttribute('src');
      video.hidden = false;
      if (canAutoplay()) playMuted(video);
      return;
    }
    image.onload = () => {
      if (token !== imageRequest) return;
      image.hidden = false;
      loading.textContent = '';
    };
    image.onerror = () => {
      if (token !== imageRequest) return;
      image.hidden = true;
      loading.textContent = 'The image could not load. Try another image or open the original below.';
    };
    image.alt = source.alt;
    image.src = source.getAttribute('src');
  }

  function showLightbox(gallery, opener) {
    if (!supportsDialog) return false;
    activeGallery = gallery;
    returnFocus = opener;
    dialog.showModal();
    syncGalleryPlayback();
    renderLightbox();
    document.body.classList.add('lightbox-open');
    dialog.querySelector('[data-close]').focus();
    return true;
  }

  function cleanupLightbox() {
    const visibleOpener = activeGallery?.slides[activeGallery.index].querySelector('[data-lightbox]');
    ++imageRequest;
    image.onload = null;
    image.onerror = null;
    image.removeAttribute('src');
    image.hidden = true;
    clearLightboxVideo();
    loading.textContent = '';
    setZoom(false);
    activeGallery = null;
    syncGalleryPlayback();
    document.body.classList.remove('lightbox-open');
    const focusTarget = returnFocus?.isConnected && returnFocus.getClientRects().length && !returnFocus.closest('.gallery-slide')?.hidden ? returnFocus : visibleOpener;
    focusTarget?.focus({preventScroll: true});
    returnFocus = null;
  }

  function closeLightbox() {
    if (dialog.open) dialog.close();
    // Native close events are queued. Restore now so a quick reopen is independent.
    cleanupLightbox();
  }

  galleries.forEach(element => {
    const slides = [...element.querySelectorAll('.gallery-slide')];
    const thumbnails = [...element.querySelectorAll('[data-slide]')];
    if (!slides.length) return;
    const state = {element, slides, index: 0, visible: !('IntersectionObserver' in window), hover: element.matches(':hover'), focus: element.contains(document.activeElement), paused: false, timer: null, title: element.dataset.galleryTitle || 'Project gallery'};
    states.push(state);
    element.classList.add('gallery-ready');
    slides.forEach(slide => {
      const clip = slide.querySelector('video');
      const status = slide.querySelector('[data-video-status]');
      if (!clip) return;
      clip.loop = false;
      clip.addEventListener('loadedmetadata', () => syncSlideshow(state));
      clip.addEventListener('ended', () => { if (slide === state.slides[state.index]) syncSlideshow(state); });
      function takePlaybackControl(event) {
        if (event.type === 'keydown' && (event.key === 'Tab' || event.altKey || event.ctrlKey || event.metaKey)) return;
        manualPlayback.add(clip);
        state.paused = true;
        syncSlideshow(state);
      }
      clip.addEventListener('pointerdown', takePlaybackControl);
      clip.addEventListener('keydown', takePlaybackControl);
      if (status) {
        clip.addEventListener('error', () => { status.textContent = ' Video unavailable. Try Watch larger to open the original.'; });
        clip.addEventListener('loadeddata', () => { status.textContent = ''; });
      }
    });
    const count = element.querySelector('[data-gallery-count]');
    state.count = count;
    const controls = element.querySelector('.gallery-controls');
    if (controls && slides.length > 1) {
      const rotation = document.createElement('button');
      rotation.type = 'button';
      rotation.className = 'gallery-button gallery-rotation';
      rotation.setAttribute('data-gallery-rotation', '');
      rotation.textContent = 'Pause slideshow';
      rotation.addEventListener('click', () => { state.paused = !state.paused; syncSlideshow(state); });
      controls.append(rotation);
      state.rotation = rotation;
    }
    function select(index) {
      const previous = state.index;
      state.index = (index + slides.length) % slides.length;
      const selectedClip = slides[state.index].querySelector('video');
      if (previous !== state.index && selectedClip?.ended && !manualPlayback.has(selectedClip)) selectedClip.currentTime = 0;
      slides.forEach((slide, n) => { slide.hidden = n !== state.index; });
      thumbnails.forEach((thumb, n) => {
        if (n === state.index) thumb.setAttribute('aria-current', 'true');
        else thumb.removeAttribute('aria-current');
      });
      if (count) count.textContent = `${state.index + 1} / ${slides.length}`;
      const upcomingImage = slides[(state.index + 1) % slides.length].querySelector('img');
      if (upcomingImage) upcomingImage.loading = 'eager';
      if (dialog.open && activeGallery === state) renderLightbox();
      syncGalleryPlayback();
    }
    state.select = select;
    state.step = amount => select(state.index + amount);
    thumbnails.forEach((thumb, index) => thumb.addEventListener('click', event => {
      event.preventDefault();
      select(index);
    }));
    element.querySelector('[data-gallery-prev]')?.addEventListener('click', () => state.step(-1));
    element.querySelector('[data-gallery-next]')?.addEventListener('click', () => state.step(1));
    element.querySelectorAll('[data-lightbox]').forEach(anchor => anchor.addEventListener('click', event => {
      if (showLightbox(state, anchor)) event.preventDefault();
    }));
    element.addEventListener('keydown', event => {
      if (event.target.closest('video, input, select, textarea, [contenteditable="true"]')) return;
      if (event.altKey || event.ctrlKey || event.metaKey || !['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      if (event.key === 'Home') select(0);
      else if (event.key === 'End') select(slides.length - 1);
      else state.step(event.key === 'ArrowLeft' ? -1 : 1);
    });
    element.addEventListener('mouseenter', () => { state.hover = true; syncSlideshow(state); });
    element.addEventListener('mouseleave', () => { state.hover = false; syncSlideshow(state); });
    element.addEventListener('focusin', () => { state.focus = true; syncSlideshow(state); });
    element.addEventListener('focusout', event => {
      if (!element.contains(event.relatedTarget)) { state.focus = false; syncSlideshow(state); }
    });
    element.querySelectorAll('[data-gallery-control]').forEach(control => { control.hidden = slides.length < 2; });
    select(0);
  });

  // Static walkthroughs share the modal without becoming rotating galleries.
  imageSets.forEach(element => {
    const slides = [...element.querySelectorAll('[data-image-frame]')];
    if (!slides.length) return;
    const state = {
      element, slides, index: 0,
      title: element.dataset.galleryTitle || 'Image walkthrough',
      step(amount) {
        this.index = (this.index + amount + slides.length) % slides.length;
        renderLightbox();
      }
    };
    slides.forEach((slide, index) => {
      const anchor = slide.querySelector('[data-lightbox]');
      anchor?.addEventListener('click', event => {
        if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
        state.index = index;
        if (showLightbox(state, anchor)) event.preventDefault();
      });
    });
  });

  if (supportsDialog) {
    function takeLightboxControl(event) {
      if (event.type === 'keydown' && (event.key === 'Tab' || event.altKey || event.ctrlKey || event.metaKey)) return;
      manualPlayback.add(video);
    }
    video.addEventListener('pointerdown', takeLightboxControl);
    video.addEventListener('keydown', takeLightboxControl);
    dialog.querySelector('[data-close]').addEventListener('click', closeLightbox);
    dialog.addEventListener('cancel', event => { event.preventDefault(); closeLightbox(); });
    dialog.querySelector('[data-prev]').addEventListener('click', () => activeGallery?.step(-1));
    dialog.querySelector('[data-next]').addEventListener('click', () => activeGallery?.step(1));
    zoomButton.addEventListener('click', () => { if (image.complete && image.naturalWidth) setZoom(!zoomed); });
    dialog.addEventListener('keydown', event => {
      if (event.altKey || event.ctrlKey || event.metaKey) return;
      if (event.target === video && event.key !== 'Tab') return;
      if (event.key === 'Tab') {
        const stops = [...dialog.querySelectorAll('button:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])')].filter(element => element.getClientRects().length);
        const first = stops[0];
        const last = stops[stops.length - 1];
        if (first && (event.shiftKey && document.activeElement === first || !event.shiftKey && document.activeElement === last || !dialog.contains(document.activeElement))) {
          event.preventDefault();
          (event.shiftKey ? last : first).focus();
        }
      }
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        // Preserve arrow-key panning when the full-resolution viewport has focus.
        if (zoomed && event.target === viewport) return;
        event.preventDefault();
        activeGallery?.step(event.key === 'ArrowLeft' ? -1 : 1);
      }
    });
    dialog.addEventListener('click', event => {
      const bounds = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) closeLightbox();
    });
    dialog.addEventListener('close', () => {
      if (!dialog.open && activeGallery) cleanupLightbox();
    });
  }
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        const state = states.find(item => item.element === entry.target);
        if (state) state.visible = entry.isIntersecting;
      });
      syncGalleryPlayback();
    });
    states.forEach(state => observer.observe(state.element));
  }
  document.documentElement.addEventListener('portfolio:motion-change', syncGalleryPlayback);
  reduced.addEventListener('change', syncGalleryPlayback);
  document.addEventListener('visibilitychange', () => {
    syncGalleryPlayback();
    if (document.hidden) document.querySelectorAll('video').forEach(clip => clip.pause());
  });
  window.addEventListener('pagehide', () => {
    away = true;
    syncGalleryPlayback();
    document.querySelectorAll('video').forEach(clip => clip.pause());
  });
  window.addEventListener('pageshow', () => { away = false; syncGalleryPlayback(); });
})();
