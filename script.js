const scene = document.querySelector('#scene');
const shell = document.querySelector('.scene-shell');
const zones = document.querySelector('.zones');
const zoneToggle = document.querySelector('#zoneToggle');
const zoomToggle = document.querySelector('#zoomToggle');
const hint = document.querySelector('#hint');
const zoneButtons = [...document.querySelectorAll('.zone')];

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let hintTimer;
let panning = false;
let zoomLevel = 1;
let panX = 0;
let panY = 0;
let pointerStart = { x: 0, y: 0, panX: 0, panY: 0 };

function resetTilt() {
  scene.style.setProperty('--rx', '0deg');
  scene.style.setProperty('--ry', '0deg');
}

function showHint(message, persistent = false) {
  clearTimeout(hintTimer);
  hint.textContent = message;
  hint.classList.add('is-visible');
  if (!persistent) hintTimer = setTimeout(() => hint.classList.remove('is-visible'), 2200);
}

function clearSelection() {
  zoneButtons.forEach((zone) => zone.classList.remove('is-selected'));
}

function applyPan(x, y) {
  const maxX = shell.clientWidth * (zoomLevel - 1) / 2;
  const maxY = shell.clientHeight * (zoomLevel - 1) / 2;
  panX = Math.max(-maxX, Math.min(maxX, x));
  panY = Math.max(-maxY, Math.min(maxY, y));
  scene.style.setProperty('--px', `${panX}px`);
  scene.style.setProperty('--py', `${panY}px`);
}

function setExplore(active, announce = true) {
  zones.classList.toggle('is-active', active);
  zones.toggleAttribute('inert', !active);
  zones.setAttribute('aria-hidden', String(!active));
  zoneButtons.forEach((zone) => { zone.tabIndex = active ? 0 : -1; });
  zoneToggle.setAttribute('aria-expanded', String(active));
  zoneToggle.setAttribute('aria-pressed', String(active));
  zoneToggle.setAttribute('aria-label', active ? '探索エリアを非表示' : '探索エリアを表示');
  if (!active) clearSelection();
  if (announce) showHint(active ? 'エリアを選ぶとパーツを確認できます' : '探索表示を終了しました');
}

shell.addEventListener('pointermove', (event) => {
  if (panning) {
    applyPan(pointerStart.panX + event.clientX - pointerStart.x, pointerStart.panY + event.clientY - pointerStart.y);
    return;
  }
  if (shell.classList.contains('is-zoomed') || reducedMotion.matches || event.pointerType === 'touch') return;
  const rect = shell.getBoundingClientRect();
  const x = (event.clientX - rect.left) / rect.width - 0.5;
  const y = (event.clientY - rect.top) / rect.height - 0.5;
  scene.style.setProperty('--rx', `${(-y * 1.1).toFixed(2)}deg`);
  scene.style.setProperty('--ry', `${(x * 1.1).toFixed(2)}deg`);
});

shell.addEventListener('pointerleave', resetTilt);

scene.addEventListener('pointerdown', (event) => {
  if (!shell.classList.contains('is-zoomed') || event.target.closest('.zone')) return;
  panning = true;
  pointerStart = { x: event.clientX, y: event.clientY, panX, panY };
  shell.classList.add('is-panning');
  scene.setPointerCapture(event.pointerId);
});

scene.addEventListener('pointerup', (event) => {
  if (!panning) return;
  panning = false;
  shell.classList.remove('is-panning');
  scene.releasePointerCapture(event.pointerId);
});

scene.addEventListener('pointercancel', () => {
  panning = false;
  shell.classList.remove('is-panning');
});

zoneToggle.addEventListener('click', () => {
  setExplore(!zones.classList.contains('is-active'));
});

zoomToggle.addEventListener('click', () => {
  const zoomed = shell.classList.toggle('is-zoomed');
  resetTilt();
  zoomLevel = zoomed ? (matchMedia('(max-aspect-ratio: 3 / 4)').matches ? 1.85 : 1.3) : 1;
  scene.style.setProperty('--zoom', String(zoomLevel));
  if (!zoomed) {
    panX = 0;
    panY = 0;
    scene.style.setProperty('--px', '0px');
    scene.style.setProperty('--py', '0px');
  }
  zoomToggle.setAttribute('aria-pressed', String(zoomed));
  zoomToggle.setAttribute('aria-label', zoomed ? 'マップを全景表示に戻す' : 'マップを拡大');
  zoomToggle.textContent = zoomed ? 'FIT' : 'ZOOM';
  showHint(zoomed ? 'マップをドラッグして移動できます' : '全景表示に戻りました', zoomed);
});

zoneButtons.forEach((zone) => {
  zone.addEventListener('click', () => {
    const wasSelected = zone.classList.contains('is-selected');
    clearSelection();
    if (!wasSelected) zone.classList.add('is-selected');
    showHint(wasSelected ? '選択を解除しました' : zone.dataset.zone, !wasSelected);
  });
});

document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') return;
  clearSelection();
  showHint('選択を解除しました');
});

const demoParams = new URLSearchParams(window.location.search);
if (demoParams.has('explore')) {
  setExplore(true);
  if (demoParams.get('explore') === 'solar') {
    const solar = document.querySelector('.zone--solar');
    solar.classList.add('is-selected');
    solar.focus();
  }
} else {
  setExplore(false, false);
}

if (demoParams.has('zoom')) zoomToggle.click();

if (demoParams.get('pan') === 'se' && shell.classList.contains('is-zoomed')) {
  applyPan(-shell.clientWidth * (zoomLevel - 1) / 2, -shell.clientHeight * (zoomLevel - 1) / 2);
}
