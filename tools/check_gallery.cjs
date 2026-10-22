// Deterministic DOM fixture for the gallery's timer and interaction lifecycle.
// This checks state transitions; it does not replace a real-browser layout check.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

class Element {
  constructor(tag = 'div') {
    this.tagName = tag.toUpperCase(); this.attrs = {}; this.dataset = {}; this.style = {};
    this.events = {}; this.children = []; this.hidden = false; this.open = false;
    this.isConnected = true; this.classList = {add() {}, remove() {}, toggle() {}};
    this.textContent = ''; this.playCount = 0; this.pauseCount = 0;
  }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  getAttribute(k) { return this.attrs[k] ?? null; }
  hasAttribute(k) { return k in this.attrs; }
  removeAttribute(k) { delete this.attrs[k]; }
  addEventListener(k, fn) { (this.events[k] ??= []).push(fn); }
  emit(k, event = {}) { (this.events[k] || []).forEach(fn => fn({type: k, target: this, preventDefault() {}, ...event})); }
  append(el) { this.children.push(el); el.parent = this; }
  contains(el) { return el === this || this.children.some(child => child.contains(el)); }
  matches() { return false; }
  closest() { return null; }
  getClientRects() { return this.hidden ? [] : [{}]; }
  getBoundingClientRect() { return {left: 0, top: 0, right: 100, bottom: 100}; }
  focus() {}
  play() { this.playCount++; return Promise.resolve(); }
  pause() { this.pauseCount++; }
  load() {}
  showModal() { this.open = true; }
  close() { this.open = false; }
  querySelector(s) { return this.map?.[s] || null; }
  querySelectorAll(s) { return this.lists?.[s] || []; }
}

function fixture({videoSlide = false, reducedMotion = false} = {}) {
  const timers = new Map(); let id = 0;
  const doc = new Element(); doc.documentElement = new Element(); doc.body = new Element();
  doc.activeElement = null; doc.hidden = false; doc.getElementById = () => null;
  const root = new Element(); const count = new Element('output'); const controls = new Element();
  const prev = new Element('button'); const next = new Element('button');
  const slides = []; const thumbs = []; const anchors = [];
  for (let i = 0; i < 3; i++) {
    const slide = new Element('figure'); const media = new Element(videoSlide && i === 0 ? 'video' : 'img');
    media.setAttribute('src', `image-${i}`); media.duration = 5;
    const caption = new Element('figcaption'); caption.textContent = `Caption ${i}`;
    const anchor = new Element('a'); anchor.append(media); slide.append(anchor);
    slide.map = {'img, video': media, 'video': media.tagName === 'VIDEO' ? media : null, 'figcaption': caption, '[data-lightbox]': anchor};
    root.append(slide); slides.push(slide); anchors.push(anchor); thumbs.push(new Element('a'));
  }
  root.append(controls); [prev, count, next, ...thumbs].forEach(el => controls.append(el));
  root.map = {'.gallery-controls': controls, '[data-gallery-count]': count, '[data-gallery-prev]': prev, '[data-gallery-next]': next};
  root.lists = {'.gallery-slide': slides, '[data-slide]': thumbs, '[data-lightbox]': anchors, '[data-gallery-control]': [prev, next]};
  const dialog = new Element('dialog'); const keys = ['img','video','.lightbox-viewport','[data-position]','[data-zoom]','.lightbox-caption','.lightbox-loading','.lightbox-original','#lightbox-title','[data-prev]','[data-next]','[data-close]'];
  dialog.map = Object.fromEntries(keys.map(k => [k, new Element(k === 'video' ? 'video' : 'div')]));
  doc.createElement = tag => tag === 'dialog' ? dialog : new Element(tag);
  doc.lists = {'[data-gallery]': [root]};
  const win = new Element(); let observer;
  class Observer {
    constructor(fn) { this.callback = fn; observer = this; }
    observe() {}
    report(visible) { this.callback([{target: root, isIntersecting: visible}]); }
  }
  win.IntersectionObserver = Observer;
  const reduced = new Element(); reduced.matches = reducedMotion;
  const sandbox = {document: doc, window: win, matchMedia: () => reduced, IntersectionObserver: Observer,
    setTimeout(fn, delay) { timers.set(++id, {fn, delay}); return id; }, clearTimeout(key) { timers.delete(key); }};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../gallery.js'), 'utf8'), sandbox);
  const fire = () => { assert.equal(timers.size, 1); const [key, timer] = [...timers][0]; timers.delete(key); timer.fn(); };
  return {doc, root, count, slides, thumbs, anchors, controls, dialog, reduced, timers, win, observer, fire, next,
    rotation: controls.children.find(el => el.hasAttribute('data-gallery-rotation'))};
}

const f = fixture();
assert.equal(f.timers.size, 0, 'Do not start before visibility is known');
f.observer.report(true);
assert.equal(f.timers.size, 1);
assert.equal([...f.timers.values()][0].delay, 7000);
assert.equal(f.count.getAttribute('aria-live'), 'off', 'Automatic changes should not generate live announcements');
f.fire(); assert.equal(f.slides[1].hidden, false);
f.fire(); f.fire(); assert.equal(f.slides[0].hidden, false, 'Wrap after the final slide');
for (let i = 0; i < 5; i++) {
  f.root.emit('mouseenter'); assert.equal(f.timers.size, 0);
  f.root.emit('mouseleave'); assert.equal(f.timers.size, 1);
  f.root.emit('focusin'); assert.equal(f.timers.size, 0);
  f.root.emit('focusout', {relatedTarget: f.thumbs[0]}); assert.equal(f.timers.size, 0);
  f.root.emit('focusout', {relatedTarget: null}); assert.equal(f.timers.size, 1);
  f.rotation.emit('click'); assert.equal(f.timers.size, 0);
  f.rotation.emit('click'); assert.equal(f.timers.size, 1);
}
f.observer.report(false); assert.equal(f.timers.size, 0);
f.observer.report(true); assert.equal(f.timers.size, 1);
f.doc.hidden = true; f.doc.emit('visibilitychange'); assert.equal(f.timers.size, 0);
f.doc.hidden = false; f.doc.emit('visibilitychange'); assert.equal(f.timers.size, 1);
f.doc.documentElement.dataset.motion = 'paused';
f.doc.documentElement.emit('portfolio:motion-change'); assert.equal(f.timers.size, 0); assert.equal(f.rotation.disabled, true);
f.doc.documentElement.dataset.motion = 'playing';
f.doc.documentElement.emit('portfolio:motion-change'); assert.equal(f.timers.size, 1);
for (let i = 0; i < 3; i++) {
  f.anchors[0].emit('click'); assert.equal(f.dialog.open, true); assert.equal(f.timers.size, 0);
  f.dialog.map['[data-close]'].emit('click'); assert.equal(f.dialog.open, false); assert.equal(f.timers.size, 1);
  f.dialog.emit('close'); assert.equal(f.timers.size, 1, 'Queued close must not create another timer');
}
f.win.emit('pagehide'); assert.equal(f.timers.size, 0);
f.win.emit('pageshow'); assert.equal(f.timers.size, 1);
f.reduced.matches = true; f.reduced.emit('change'); assert.equal(f.timers.size, 0);
f.next.emit('click'); assert.equal(f.count.textContent, '2 / 3', 'Manual navigation works with reduced motion');
const quiet = fixture({reducedMotion: true}); quiet.observer.report(true);
assert.equal(quiet.timers.size, 0); assert.equal(quiet.rotation.disabled, true);
const v = fixture({videoSlide: true}); v.observer.report(true);
assert.ok(v.slides[0].map.video.playCount > 0);
v.slides[0].map.video.emit('pointerdown'); assert.equal(v.timers.size, 0, 'Native video interaction stops slide rotation');
v.rotation.emit('click'); assert.equal(v.timers.size, 1);
v.slides[0].map.video.duration = 12; v.slides[0].map.video.emit('loadedmetadata');
assert.equal([...v.timers.values()][0].delay, 12750, 'Allow the short clip to finish');
v.win.emit('pagehide'); assert.equal(v.timers.size, 0); assert.ok(v.slides[0].map.video.pauseCount > 0);
const manual = fixture({videoSlide: true}); manual.observer.report(true);
const manualClip = manual.slides[0].map.video;
manualClip.emit('keydown', {key: 'Tab'});
assert.equal(manual.timers.size, 1, 'Tab navigation alone must not take over playback');
manualClip.emit('keydown', {key: ' '});
assert.equal(manual.timers.size, 0, 'Keyboard video controls must stop slide rotation');
const manualPlayCount = manualClip.playCount;
manualClip.muted = false;
manual.observer.report(false); manual.observer.report(true);
manual.doc.hidden = true; manual.doc.emit('visibilitychange');
manual.doc.hidden = false; manual.doc.emit('visibilitychange');
assert.equal(manualClip.playCount, manualPlayCount, 'Scrolling or returning to the tab must not override manual playback');
assert.equal(manualClip.muted, false, 'Lifecycle updates must preserve the user\'s sound setting');
const pointer = fixture({videoSlide: true}); pointer.observer.report(true);
const pointerClip = pointer.slides[0].map.video;
pointerClip.emit('pointerdown');
const pointerPlayCount = pointerClip.playCount;
pointer.observer.report(false); pointer.observer.report(true);
assert.equal(pointerClip.playCount, pointerPlayCount, 'Mouse/touch video interaction must also take ownership of playback');
const modal = fixture({videoSlide: true}); modal.observer.report(true);
modal.anchors[0].emit('click');
const modalClip = modal.dialog.map.video;
modalClip.emit('keydown', {key: ' '});
const modalPlayCount = modalClip.playCount;
modal.doc.hidden = true; modal.doc.emit('visibilitychange');
modal.doc.hidden = false; modal.doc.emit('visibilitychange');
assert.equal(modalClip.playCount, modalPlayCount, 'The lightbox must retain a manual pause after returning to the tab');
console.log('PASS: gallery rotation, lifecycle, reduced motion, lightbox cleanup, and mouse/touch/keyboard ownership of playback and sound.');
