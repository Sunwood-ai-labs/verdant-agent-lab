const sources = [
  ['furniture', 'assets/manifests/furniture.v1.json'],
  ['technology', 'assets/manifests/technology.v1.json'],
  ['props', 'assets/manifests/props.v1.json'],
];
const [manifests, layout, boundsReport] = await Promise.all([
  Promise.all(sources.map(async ([kind, path]) => ({ kind, ...(await fetch(path).then((r) => r.json())) }))),
  fetch('assets/layouts/starter.v1.json').then((r) => r.json()),
  fetch('proof/runtime-asset-bounds-v1.json').then((r) => r.json()),
]);
const bounds = new Map(boundsReport.assets.map((item) => [item.id, item]));
const placedIds = new Set(layout.objects.map((item) => item.assetId));
const assets = manifests.flatMap(({ kind, items }) => items.map((item) => ({ ...item, kind, placed: placedIds.has(item.id), bounds: bounds.get(item.id) })));
const humanize = (value = 'not declared') => value.replaceAll('-', ' ');
const parts = (item) => item.contentCount?.decomposedParts ? `${item.contentCount.decomposedParts} cells` : item.decompositionManifest ? 'composite' : 'single sprite';
const catalog = document.querySelector('#catalog');
const template = document.querySelector('#card-template');
const filter = document.querySelector('#filter');
const pageSize = 24;
const requestedPage = Math.max(1, Number(new URLSearchParams(location.search).get('page')) || 1);
document.querySelector('#total').textContent = assets.length;
document.querySelector('#active').textContent = assets.filter((item) => item.placed).length;
document.querySelector('#decomposed').textContent = assets.filter((item) => item.decompositionManifest).length;
function draw() {
  const type = filter.value;
  const shown = assets.filter((item) => type === 'all' || (type === 'active' && item.placed) || (type === 'decomposed' && item.decompositionManifest) || item.kind === type);
  const pageCount = Math.max(1, Math.ceil(shown.length / pageSize));
  const currentPage = Math.min(requestedPage, pageCount);
  const pageAssets = shown.slice((currentPage - 1) * pageSize, currentPage * pageSize);
  const cards = pageAssets.map((item) => {
    const node = template.content.cloneNode(true);
    const image = node.querySelector('img');
    image.src = `assets/${item.sprite.replace('../', '')}`;
    image.alt = item.id;
    node.querySelector('.kind').textContent = item.kind.toUpperCase();
    node.querySelector('.placed').textContent = item.placed ? 'PLACED NOW' : 'CATALOG ONLY';
    const risk = node.querySelector('.bounds');
    risk.textContent = item.bounds?.touchesCanvasEdge ? `EDGE-CUT RISK: ${item.bounds.hitEdges.join(', ')}` : item.bounds?.trimmedFrom ? 'TIGHT-TRIMMED / 8PX PAD' : 'FULL ALPHA BOUNDS';
    risk.classList.toggle('risk', Boolean(item.bounds?.touchesCanvasEdge));
    node.querySelector('h2').textContent = humanize(item.id);
    node.querySelector('.orientation').textContent = humanize(item.orientation);
    node.querySelector('.parts').textContent = parts(item);
    node.querySelector('code').textContent = item.sprite;
    return node;
  });
  catalog.replaceChildren(...cards);
  document.querySelector('#resultCount').textContent = `${pageAssets.length} shown · ${shown.length} filtered / ${assets.length} runtime`;
  const previous = document.querySelector('#previousPage');
  const next = document.querySelector('#nextPage');
  previous.href = `?page=${Math.max(1, currentPage - 1)}`;
  next.href = `?page=${Math.min(pageCount, currentPage + 1)}`;
  previous.setAttribute('aria-disabled', String(currentPage === 1));
  next.setAttribute('aria-disabled', String(currentPage === pageCount));
  document.querySelector('#pageLabel').textContent = `PAGE ${currentPage} / ${pageCount}`;
}
filter.addEventListener('change', draw);
draw();
