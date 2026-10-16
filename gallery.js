(() => {
  'use strict';
  const galleries = [...document.querySelectorAll('[data-gallery]')];
  if (!galleries.length || document.getElementById('media-lightbox')) return;

  const dialog = document.createElement('dialog');
  dialog.id = 'media-lightbox';
  dialog.className = 'media-lightbox';
  dialog.setAttribute('aria-labelledby', 'lightbox-title');
  dialog.setAttribute('aria-describedby', 'lightbox-caption');
  dialog.innerHTML = `<div class="lightbox-header"><div><span class="eyebrow">Project gallery</span><h2 id="lightbox-title"></h2></div><button type="button" class="gallery-button" data-close aria-label="Close image viewer">Close <span aria-hidden="true">×</span></button></div><div class="lightbox-toolbar"><button type="button" class="gallery-button" data-prev aria-label="Previous image">← Previous</button><span data-position aria-live="polite"></span><button type="button" class="gallery-button" data-next aria-label="Next image">Next →</button><button type="button" class="gallery-button" data-zoom aria-pressed="false">Full resolution</button></div><div class="lightbox-viewport" tabindex="0" aria-label="Image viewport. At full resolution, scroll to inspect the image."><img class="lightbox-image" alt=""><p class="lightbox-loading" role="status"></p></div><p class="lightbox-caption" id="lightbox-caption"></p><a class="lightbox-original" href="#" target="_blank" rel="noopener">Open original image in a new tab ↗</a>`;
  const supportsDialog = typeof dialog.showModal === 'function';
  if (supportsDialog) document.body.append(dialog);
  const image = dialog.querySelector('img');
  const viewport = dialog.querySelector('.lightbox-viewport');
  const position = dialog.querySelector('[data-position]');
  const caption = dialog.querySelector('.lightbox-caption');
  const loading = dialog.querySelector('.lightbox-loading');
  const zoomButton = dialog.querySelector('[data-zoom]');
  let activeGallery = null;
  let returnFocus = null;
  let zoomed = false;
  let imageRequest = 0;

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
    const source = slide.querySelector('img');
    const text = slide.querySelector('figcaption').textContent.trim();
    const token = ++imageRequest;
    setZoom(false);
    image.hidden = true;
    loading.textContent = 'Loading image…';
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
    dialog.querySelector('#lightbox-title').textContent = activeGallery.title;
    position.textContent = `${activeGallery.index + 1} / ${activeGallery.slides.length}`;
    caption.textContent = text;
    dialog.querySelector('.lightbox-original').href = source.getAttribute('src');
    dialog.querySelector('[data-prev]').disabled = activeGallery.slides.length < 2;
    dialog.querySelector('[data-next]').disabled = activeGallery.slides.length < 2;
  }

  function showLightbox(gallery, opener) {
    if (!supportsDialog) return false;
    activeGallery = gallery;
    returnFocus = opener;
    renderLightbox();
    dialog.showModal();
    document.body.classList.add('lightbox-open');
    dialog.querySelector('[data-close]').focus();
    return true;
  }

  galleries.forEach(element => {
    const slides = [...element.querySelectorAll('.gallery-slide')];
    const thumbnails = [...element.querySelectorAll('[data-slide]')];
    if (!slides.length) return;
    const state = {element, slides, index: 0, title: element.dataset.galleryTitle || 'Project images'};
    const count = element.querySelector('[data-gallery-count]');
    function select(index) {
      state.index = (index + slides.length) % slides.length;
      slides.forEach((slide, n) => { slide.hidden = n !== state.index; });
      thumbnails.forEach((thumb, n) => {
        if (n === state.index) thumb.setAttribute('aria-current', 'true');
        else thumb.removeAttribute('aria-current');
      });
      if (count) count.textContent = `${state.index + 1} / ${slides.length}`;
      if (dialog.open && activeGallery === state) renderLightbox();
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
      if (event.altKey || event.ctrlKey || event.metaKey || !['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      if (event.key === 'Home') select(0);
      else if (event.key === 'End') select(slides.length - 1);
      else state.step(event.key === 'ArrowLeft' ? -1 : 1);
    });
    element.querySelectorAll('[data-gallery-control]').forEach(control => { control.hidden = slides.length < 2; });
    select(0);
  });

  if (supportsDialog) {
    dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
    dialog.querySelector('[data-prev]').addEventListener('click', () => activeGallery?.step(-1));
    dialog.querySelector('[data-next]').addEventListener('click', () => activeGallery?.step(1));
    zoomButton.addEventListener('click', () => { if (image.complete && image.naturalWidth) setZoom(!zoomed); });
    dialog.addEventListener('keydown', event => {
      if (event.altKey || event.ctrlKey || event.metaKey) return;
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
      if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
    });
    dialog.addEventListener('close', () => {
      const visibleOpener = activeGallery?.slides[activeGallery.index].querySelector('[data-lightbox]');
      ++imageRequest;
      image.onload = null;
      image.onerror = null;
      image.removeAttribute('src');
      image.hidden = true;
      setZoom(false);
      activeGallery = null;
      document.body.classList.remove('lightbox-open');
      const focusTarget = returnFocus?.isConnected && returnFocus.getClientRects().length ? returnFocus : visibleOpener;
      focusTarget?.focus({preventScroll: true});
      returnFocus = null;
    });
  }
  // A manually played project clip should stop when its page is hidden.
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) document.querySelectorAll('video').forEach(video => video.pause());
  });
})();
