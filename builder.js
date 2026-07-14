const MANIFESTS = [
  'assets/manifests/furniture.v1.json',
  'assets/manifests/technology.v1.json',
  'assets/manifests/props.v1.json',
];
const STARTER_LAYOUT = 'assets/layouts/starter.v1.json';

const WORLD = { cols: 40, rows: 30 };
const STORAGE_KEY = 'verdant-agent-lab-layout-v1';

const catalogGrid = document.querySelector('#catalogGrid');
const assetCount = document.querySelector('#assetCount');
const assetSearch = document.querySelector('#assetSearch');
const categoryFilters = document.querySelector('#categoryFilters');
const stage = document.querySelector('#stage');
const placedObjects = document.querySelector('#placedObjects');
const tileCursor = document.querySelector('#tileCursor');
const placementCount = document.querySelector('#placementCount');
const builderHint = document.querySelector('#builderHint');
const inspectorEmpty = document.querySelector('#inspectorEmpty');
const inspectorPanel = document.querySelector('#inspectorPanel');
const inspectorSprite = document.querySelector('#inspectorSprite');
const inspectorName = document.querySelector('#inspectorName');
const inspectorUid = document.querySelector('#inspectorUid');
const inspectorType = document.querySelector('#inspectorType');
const inspectorGrid = document.querySelector('#inspectorGrid');
const inspectorZ = document.querySelector('#inspectorZ');
const deleteButton = document.querySelector('#deleteButton');
const referenceToggle = document.querySelector('#referenceToggle');
const resetButton = document.querySelector('#resetButton');
const exportButton = document.querySelector('#exportButton');

let assets = [];
let layout = { version: 1, world: WORLD, objects: [] };
let selectedAssetId = null;
let selectedUid = null;
let activeCategory = 'all';
let dragging = null;
let dragMoved = false;
let starterTemplate = { version: 1, world: WORLD, objects: [] };

function titleFromId(id) {
  return id.replaceAll('-', ' ');
}

function showHint(message) {
  builderHint.textContent = message;
}

function resolveSprite(manifestPath, spritePath) {
  return new URL(spritePath, new URL(manifestPath, location.href)).href;
}

async function loadCatalog() {
  const packs = await Promise.all(MANIFESTS.map(async (manifestPath) => {
    const response = await fetch(manifestPath);
    if (!response.ok) throw new Error(`Could not load ${manifestPath}`);
    const manifest = await response.json();
    return manifest.items.map((item) => ({
      ...item,
      packId: manifest.packId,
      spriteUrl: resolveSprite(manifestPath, item.sprite),
    }));
  }));

  assets = packs.flat();
  const starterResponse = await fetch(STARTER_LAYOUT);
  if (!starterResponse.ok) throw new Error(`Could not load ${STARTER_LAYOUT}`);
  starterTemplate = await starterResponse.json();
  assetCount.textContent = `${assets.length} OBJECTS`;
  renderFilters();
  renderCatalog();
  restoreLayout();
}

function renderFilters() {
  const categories = ['all', ...new Set(assets.map((asset) => asset.category))];
  categoryFilters.replaceChildren(...categories.map((category) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `filter-chip${category === activeCategory ? ' is-active' : ''}`;
    button.dataset.category = category;
    button.setAttribute('aria-pressed', String(category === activeCategory));
    button.textContent = category;
    button.addEventListener('click', () => {
      activeCategory = category;
      renderFilters();
      renderCatalog();
      requestAnimationFrame(() => categoryFilters.querySelector(`[data-category="${category}"]`)?.focus());
    });
    return button;
  }));
}

function renderCatalog() {
  const query = assetSearch.value.trim().toLowerCase();
  const visible = assets.filter((asset) => {
    const categoryMatch = activeCategory === 'all' || asset.category === activeCategory;
    const searchMatch = !query || `${asset.id} ${asset.category}`.includes(query);
    return categoryMatch && searchMatch;
  });
  assetCount.textContent = `${visible.length} / ${assets.length} OBJECTS`;

  catalogGrid.replaceChildren(...visible.map((asset) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `asset-card${asset.id === selectedAssetId ? ' is-selected' : ''}`;
    button.dataset.assetId = asset.id;
    button.title = titleFromId(asset.id);
    button.setAttribute('aria-pressed', String(asset.id === selectedAssetId));
    button.innerHTML = `<img src="${asset.spriteUrl}" alt="" /><strong>${titleFromId(asset.id)}</strong><span>${asset.category}</span>`;
    button.addEventListener('click', () => {
      selectedAssetId = selectedAssetId === asset.id ? null : asset.id;
      selectedUid = null;
      stage.classList.toggle('is-placing', Boolean(selectedAssetId));
      renderCatalog();
      renderInspector();
      requestAnimationFrame(() => catalogGrid.querySelector(`[data-asset-id="${asset.id}"]`)?.focus());
      showHint(selectedAssetId ? `${titleFromId(asset.id)} を選択。床をクリック、またはTabで床へ移動しEnter/Spaceで中央へ配置。` : '配置ツールを解除しました。');
    });
    return button;
  }));
}

function assetById(id) {
  return assets.find((asset) => asset.id === id);
}

function uidFor(assetId) {
  return `${assetId}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`;
}

function gridPoint(event) {
  const rect = stage.getBoundingClientRect();
  return {
    col: Math.max(0, Math.min(WORLD.cols - 1, Math.round((event.clientX - rect.left) / rect.width * WORLD.cols))),
    row: Math.max(0, Math.min(WORLD.rows - 1, Math.round((event.clientY - rect.top) / rect.height * WORLD.rows))),
  };
}

function visualBounds(asset) {
  return {
    width: Math.max(2.5, Math.min(100, (asset.footprint?.w ?? 1) / WORLD.cols * 100)),
    height: Math.max(3.333, Math.min(100, (asset.footprint?.h ?? 1) / WORLD.rows * 100)),
  };
}

function updatePlacedSelection() {
  document.querySelectorAll('.placed-object').forEach((element) => {
    element.classList.toggle('is-selected', element.dataset.uid === selectedUid);
    element.setAttribute('aria-pressed', String(element.dataset.uid === selectedUid));
  });
}

function applyObjectPosition(button, instance, asset) {
  button.style.left = `${instance.col / WORLD.cols * 100}%`;
  button.style.top = `${instance.row / WORLD.rows * 100}%`;
  button.style.zIndex = String(instance.row * 10 + (asset.zBias ?? 0));
  button.style.setProperty('--rotation', `${instance.rotation ?? 0}deg`);
  button.setAttribute('aria-label', `${titleFromId(asset.id)}、列${instance.col}、行${instance.row}、回転${instance.rotation ?? 0}度`);
}

function selectInstance(instance) {
  selectedUid = instance.uid;
  selectedAssetId = null;
  stage.classList.remove('is-placing');
  renderCatalog();
  renderInspector();
  updatePlacedSelection();
}

function objectElement(instance) {
  const asset = assetById(instance.assetId);
  const button = document.createElement('button');
  button.type = 'button';
  button.className = `placed-object${instance.uid === selectedUid ? ' is-selected' : ''}`;
  button.dataset.uid = instance.uid;
  const bounds = visualBounds(asset);
  button.style.width = `${bounds.width}%`;
  button.style.height = `${bounds.height}%`;
  button.setAttribute('aria-pressed', String(instance.uid === selectedUid));
  button.innerHTML = `<img src="${asset.spriteUrl}" alt="" draggable="false" />`;
  applyObjectPosition(button, instance, asset);

  button.addEventListener('pointerdown', (event) => {
    selectInstance(instance);
    dragMoved = false;
    dragging = { uid: instance.uid, pointerId: event.pointerId };
    button.setPointerCapture(event.pointerId);
  });

  button.addEventListener('pointermove', (event) => {
    if (!dragging || dragging.uid !== instance.uid) return;
    dragMoved = true;
    const point = gridPoint(event);
    instance.col = point.col;
    instance.row = point.row;
    applyObjectPosition(button, instance, asset);
    renderInspector();
  });

  button.addEventListener('pointerup', () => {
    if (!dragging || dragging.uid !== instance.uid) return;
    dragging = null;
    saveLayout();
    showHint(dragMoved ? 'オブジェクトをグリッドへ移動しました。' : 'オブジェクトを選択しました。');
  });

  const cancelDrag = () => {
    if (!dragging || dragging.uid !== instance.uid) return;
    dragging = null;
    dragMoved = false;
    saveLayout();
    showHint('ドラッグを終了しました。');
  };

  button.addEventListener('pointercancel', cancelDrag);
  button.addEventListener('lostpointercapture', cancelDrag);

  button.addEventListener('click', () => {
    if (!dragMoved) {
      selectInstance(instance);
      button.focus();
      showHint(`${titleFromId(asset.id)} を選択しました。矢印キーで移動できます。`);
    }
    dragMoved = false;
  });

  button.addEventListener('keydown', (event) => {
    const deltas = {
      ArrowLeft: [-1, 0],
      ArrowRight: [1, 0],
      ArrowUp: [0, -1],
      ArrowDown: [0, 1],
    };
    const delta = deltas[event.key];
    if (!delta) return;
    event.preventDefault();
    const step = event.shiftKey ? 5 : 1;
    instance.col = Math.max(0, Math.min(WORLD.cols - 1, instance.col + delta[0] * step));
    instance.row = Math.max(0, Math.min(WORLD.rows - 1, instance.row + delta[1] * step));
    applyObjectPosition(button, instance, asset);
    selectInstance(instance);
    saveLayout();
    button.focus();
    showHint(`${titleFromId(asset.id)} を ${instance.col}, ${instance.row} へ移動しました。`);
  });

  return button;
}

function renderObjects() {
  placedObjects.replaceChildren(...layout.objects.map(objectElement));
  placementCount.textContent = `${layout.objects.length} PLACED`;
}

function renderInspector() {
  const instance = layout.objects.find((object) => object.uid === selectedUid);
  const asset = instance && assetById(instance.assetId);
  inspectorEmpty.hidden = Boolean(instance && asset);
  inspectorPanel.hidden = !instance || !asset;
  if (!instance || !asset) return;

  inspectorSprite.src = asset.spriteUrl;
  inspectorSprite.alt = titleFromId(asset.id);
  inspectorName.textContent = titleFromId(asset.id);
  inspectorUid.textContent = instance.uid;
  inspectorType.textContent = `${asset.category} / ${asset.packId}`;
  inspectorGrid.textContent = `${instance.col}, ${instance.row}`;
  inspectorZ.textContent = String(asset.zBias ?? 0);
}

function placeSelected(event) {
  if (!selectedAssetId || event.target.closest('.placed-object')) return;
  placeAssetAt(gridPoint(event));
}

function placeAssetAt(point) {
  if (!selectedAssetId) return;
  const instance = { uid: uidFor(selectedAssetId), assetId: selectedAssetId, ...point, rotation: 0, state: 'default' };
  layout.objects.push(instance);
  selectedUid = instance.uid;
  renderObjects();
  renderInspector();
  saveLayout();
  showHint(`${titleFromId(selectedAssetId)} を ${point.col}, ${point.row} に配置しました。`);
}

function saveLayout() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(layout));
}

function starterLayout() {
  return structuredClone(starterTemplate);
}

function restoreLayout() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    layout = saved?.version === 1 ? saved : starterLayout();
  } catch {
    layout = starterLayout();
  }
  renderObjects();
  renderInspector();
}

stage.addEventListener('pointermove', (event) => {
  const point = gridPoint(event);
  tileCursor.style.left = `${point.col / WORLD.cols * 100}%`;
  tileCursor.style.top = `${point.row / WORLD.rows * 100}%`;
});

stage.addEventListener('click', (event) => {
  if (!dragMoved) placeSelected(event);
  dragMoved = false;
});

stage.addEventListener('keydown', (event) => {
  if (!selectedAssetId || !['Enter', ' '].includes(event.key)) return;
  event.preventDefault();
  placeAssetAt({ col: Math.floor(WORLD.cols / 2), row: Math.floor(WORLD.rows / 2) });
});

assetSearch.addEventListener('input', renderCatalog);

deleteButton.addEventListener('click', () => {
  if (!selectedUid) return;
  layout.objects = layout.objects.filter((object) => object.uid !== selectedUid);
  selectedUid = null;
  renderObjects();
  renderInspector();
  saveLayout();
  showHint('オブジェクトを削除しました。');
});

document.addEventListener('keydown', (event) => {
  if ((event.key === 'Delete' || event.key === 'Backspace') && selectedUid && document.activeElement?.tagName !== 'INPUT') {
    deleteButton.click();
  }
  if (event.key === 'Escape') {
    selectedAssetId = null;
    selectedUid = null;
    stage.classList.remove('is-placing');
    renderCatalog();
    renderObjects();
    renderInspector();
    showHint('選択を解除しました。');
  }
});

referenceToggle.addEventListener('click', () => {
  const active = stage.classList.toggle('is-reference');
  referenceToggle.setAttribute('aria-pressed', String(active));
});

resetButton.addEventListener('click', () => {
  layout = starterLayout();
  selectedUid = null;
  selectedAssetId = null;
  saveLayout();
  renderCatalog();
  renderObjects();
  renderInspector();
  showHint('スターターレイアウトへ戻しました。');
});

exportButton.addEventListener('click', () => {
  const blob = new Blob([JSON.stringify(layout, null, 2)], { type: 'application/json' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `verdant-layout-${new Date().toISOString().slice(0, 10)}.json`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(link.href), 0);
  showHint('レイアウトJSONを書き出しました。');
});

loadCatalog().catch((error) => {
  catalogGrid.textContent = error.message;
  showHint('カタログの読み込みに失敗しました。');
});
