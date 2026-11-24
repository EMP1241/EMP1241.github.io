'use strict';

const briefingViewers = [...document.querySelectorAll('[data-briefing-viewer]')];

for (const viewer of briefingViewers) {
  const mount = viewer.querySelector('[data-briefing-frame]');
  const preview = viewer.querySelector('template');

  const updatePreview = () => {
    if (!viewer.open) {
      mount.replaceChildren();
    } else if (!mount.firstElementChild) {
      mount.append(preview.content.cloneNode(true));
    }
  };

  viewer.addEventListener('toggle', updatePreview);
  updatePreview();
}

function openBriefingViewer(hash) {
  const viewer = briefingViewers.find(item => `#${item.querySelector('summary').id}` === hash);
  if (viewer) viewer.open = true;
}

document.querySelector('#briefing').addEventListener('click', event => {
  if (event.defaultPrevented || event.button !== 0 || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
  const link = event.target.closest('a[href^="#"]');
  if (link) openBriefingViewer(link.hash);
});

window.addEventListener('hashchange', () => openBriefingViewer(window.location.hash));
openBriefingViewer(window.location.hash);
