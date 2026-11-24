'use strict';

const briefingViewers = [...document.querySelectorAll('[data-briefing-viewer]')];
const assessmentSummary = document.querySelector('#briefing-assessment');
const assessmentViewer = assessmentSummary.closest('details');
const assessmentMount = assessmentViewer.querySelector('[data-briefing-frame]');
const assessmentPageHash = /^#briefing-assessment-page-([1-9]\d*)$/;
let requestedPage = 1;
let assessmentApp = null;

function updatePreview(viewer) {
  const mount = viewer.querySelector('[data-briefing-frame]');
  if (!viewer.open) {
    mount.replaceChildren();
    if (viewer === assessmentViewer) assessmentApp = null;
    return;
  }
  if (mount.firstElementChild) return;

  const preview = viewer.querySelector('template').content.cloneNode(true);
  if (viewer === assessmentViewer) {
    const frame = preview.querySelector('iframe');
    const url = new URL(frame.getAttribute('src'), document.baseURI);
    url.hash = `page=${requestedPage}&zoom=page-width`;
    frame.src = url.href;
  }
  mount.append(preview);
}

for (const viewer of briefingViewers) {
  viewer.addEventListener('toggle', () => updatePreview(viewer));
  updatePreview(viewer);
}

document.addEventListener('webviewerloaded', event => {
  const frame = assessmentMount.firstElementChild;
  const source = event.detail?.source;
  if (!frame || source !== frame.contentWindow) return;

  // Keep the portfolio's citations in the browser history, separate from scrolling the PDF.
  source.PDFViewerApplicationOptions.set('disableHistory', true);
  source.PDFViewerApplicationOptions.set('enableScripting', false);
  source.PDFViewerApplicationOptions.set('annotationEditorMode', -1);

  const app = source.PDFViewerApplication;
  app.initializedPromise.then(() => {
    app.eventBus.on('documentinit', () => {
      if (frame !== assessmentMount.firstElementChild) return;
      assessmentApp = app;
      if (app.page !== requestedPage) app.page = requestedPage;
    });
  });
});

function openAssessmentPage(page) {
  requestedPage = page;
  assessmentViewer.open = true;
  updatePreview(assessmentViewer);
  if (assessmentApp) assessmentApp.page = page;
  assessmentSummary.focus({ preventScroll: true });
  assessmentSummary.scrollIntoView({ block: 'start', behavior: 'instant' });
}

function openBriefingViewer(hash) {
  const page = Number(hash.match(assessmentPageHash)?.[1]);
  if (Number.isSafeInteger(page)) {
    openAssessmentPage(page);
    return;
  }
  const viewer = briefingViewers.find(item => `#${item.querySelector('summary').id}` === hash);
  if (viewer) viewer.open = true;
}

document.addEventListener('click', event => {
  if (event.defaultPrevented || event.button !== 0 || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
  const link = event.target.closest('a[href]');
  if (!link) return;

  if (link.hasAttribute('data-assessment-link')) {
    const page = Number(new URLSearchParams(link.hash.slice(1)).get('page'));
    if (!Number.isSafeInteger(page) || page < 1) return;
    event.preventDefault();
    link.closest('dialog.media-lightbox[open]')?.querySelector('[data-close]')?.click();
    const hash = `#briefing-assessment-page-${page}`;
    if (window.location.hash !== hash) window.history.pushState(null, '', hash);
    openAssessmentPage(page);
  } else if (link.closest('#briefing') && link.hash) {
    openBriefingViewer(link.hash);
  }
});

window.addEventListener('hashchange', () => openBriefingViewer(window.location.hash));
openBriefingViewer(window.location.hash);
