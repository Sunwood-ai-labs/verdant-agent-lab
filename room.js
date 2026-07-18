const LAYOUT_URL = 'assets/layouts/current-room-composite.v2.json';
const stage = document.querySelector('#roomStage');
const layersRoot = document.querySelector('#roomLayers');
const layerToggle = document.querySelector('#layerToggle');
const assetCount = document.querySelector('#assetCount');
const selectionStatus = document.querySelector('#selectionStatus');

if (new URLSearchParams(location.search).get('clean') === '1') {
  document.body.classList.add('clean');
}

const response = await fetch(LAYOUT_URL);
if (!response.ok) throw new Error(`Could not load ${LAYOUT_URL}`);
const layout = await response.json();
document.querySelector('#foundation').src = layout.foundation;

const totalParts = layout.layers.reduce((sum, layer) => sum + layer.parts, 0);
assetCount.textContent = `${layout.layers.length} LAYERS / ${totalParts} PARTS`;

function percent(value, axis) {
  return `${value / layout.world[axis] * 100}%`;
}

function selectLayer(button, layer) {
  document.querySelectorAll('.room-layer').forEach((item) => item.classList.toggle('is-selected', item === button));
  selectionStatus.textContent = `${layer.label} · ${layer.parts} parts · ${layer.state}`;
}

layersRoot.replaceChildren(...layout.layers.map((layer, index) => {
  const [x1, y1, x2, y2] = layer.bbox;
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'room-layer';
  button.dataset.layerId = layer.id;
  button.dataset.label = layer.label;
  button.style.left = percent(x1, 'width');
  button.style.top = percent(y1, 'height');
  button.style.width = percent(x2 - x1, 'width');
  button.style.height = percent(y2 - y1, 'height');
  button.style.zIndex = String(10 + index);
  button.setAttribute('aria-label', `${layer.label}、${layer.parts}パーツ、${layer.state}`);
  button.innerHTML = `<img src="${layer.sprite}" alt="" draggable="false" />`;
  button.addEventListener('click', () => selectLayer(button, layer));
  return button;
}));

layerToggle.addEventListener('click', () => {
  const active = stage.classList.toggle('show-layers');
  layerToggle.setAttribute('aria-pressed', String(active));
});
