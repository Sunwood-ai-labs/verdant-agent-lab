const report = await fetch('proof/similarity/modular-office-direct-ssim-v2.json').then((response) => response.json());
const percent = (value) => `${Number(value).toFixed(2)}%`;
document.querySelector('#score').textContent = percent(report.scores.maskedSsimPercent);
document.querySelector('#ssim').textContent = percent(report.scores.maskedSsimPercent);
document.querySelector('#edge').textContent = percent(report.scores.edgeF1Percent);
document.querySelector('#composite').textContent = percent(report.scores.pixelCompositePercent);
document.querySelector('#meterFill').style.width = `${Math.min(100, report.scores.maskedSsimPercent)}%`;
document.querySelector('#status').textContent = report.pass
  ? 'DIRECT MASKED SSIM PASS · LEDGER VERIFIED'
  : 'DIRECT MASKED SSIM < 60% · NOT VERIFIED';
document.querySelector('#zoneRows').replaceChildren(...report.zones.map((zone) => {
  const row = document.createElement('tr');
  row.innerHTML = `<td>${zone.id}</td><td>${percent(zone.ssimPercent)}</td><td class="${zone.ledgerStatus === 'verified' ? '' : 'bad'}">${zone.ledgerStatus}</td><td>${zone.orientation}</td>`;
  return row;
}));
const lighttable = document.querySelector('#lighttable');
document.querySelectorAll('[data-mode]').forEach((button) => button.addEventListener('click', () => {
  document.querySelectorAll('[data-mode]').forEach((item) => item.classList.toggle('active', item === button));
  document.querySelectorAll('[data-mode]').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
  lighttable.className = `lighttable mode-${button.dataset.mode}`;
}));
const opacity = document.querySelector('#opacity');
const setOpacity = (value) => {
  opacity.value = value;
  document.querySelector('.overlay-original').style.opacity = Number(value) / 100;
  document.querySelector('#opacityValue').textContent = `${value}%`;
};
opacity.addEventListener('input', () => setOpacity(opacity.value));
document.querySelectorAll('[data-opacity]').forEach((button) => button.addEventListener('click', () => setOpacity(button.dataset.opacity)));
