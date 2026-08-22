const arrivals = [
  { tail: 'N100SP', station: 'LHR-H1', arrival: 'Today, 14:20', part: 'PUMP-100', compliance: 'Verified', constraint: 'Clear', status: 'green', label: 'Ready' },
  { tail: 'N200SP', station: 'JFK-H2', arrival: 'Today, 15:05', part: 'VALVE-200', compliance: 'Quarantined', constraint: 'Clear', status: 'red', label: 'Blocked' },
  { tail: 'N318SP', station: 'DXB-H3', arrival: 'Today, 16:40', part: 'FILTER-318', compliance: 'Verified', constraint: 'Vehicle wait', status: 'yellow', label: 'At risk' },
  { tail: 'N442SP', station: 'SIN-H1', arrival: 'Today, 18:15', part: 'ACTUATOR-442', compliance: 'Verified', constraint: 'Clear', status: 'green', label: 'Ready' },
];

const rows = document.querySelector('#arrival-rows');
const search = document.querySelector('#search-input');
const filter = document.querySelector('#status-filter');
const toast = document.querySelector('#toast');

function renderRows() {
  const query = search.value.trim().toLowerCase();
  const filtered = arrivals.filter((item) => {
    const matchesText = `${item.tail} ${item.station} ${item.part}`.toLowerCase().includes(query);
    return matchesText && (filter.value === 'all' || item.status === filter.value);
  });
  rows.innerHTML = filtered.map((item) => `
    <tr>
      <td><div class="aircraft"><span class="plane-icon">✈</span><span><strong>${item.tail}</strong><small>${item.station}</small></span></div></td>
      <td>${item.arrival}</td>
      <td><span class="part-tag">${item.part}</span></td>
      <td class="${item.compliance === 'Verified' ? 'verified' : 'unverified'}">${item.compliance === 'Verified' ? '✓' : '!'} ${item.compliance}</td>
      <td>${item.constraint}</td>
      <td><span class="status-pill status-${item.status}">${item.label}</span></td>
      <td><button class="row-action" aria-label="Open ${item.tail}">›</button></td>
    </tr>`).join('');
  document.querySelector('#row-count').textContent = filtered.length;
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add('show');
  window.setTimeout(() => toast.classList.remove('show'), 2400);
}

document.querySelectorAll('[data-view], [data-view-link]').forEach((control) => {
  control.addEventListener('click', () => {
    const view = control.dataset.view || control.dataset.viewLink;
    const labels = { overview: 'Overview', staging: 'Staging board', forecast: 'Demand forecast', procurement: 'Procurement' };
    document.querySelectorAll('.nav-item').forEach((item) => item.classList.toggle('active', item.dataset.view === view));
    document.querySelector('#page-title').textContent = labels[view];
    showToast(`${labels[view]} view is available in the mock workspace`);
  });
});

search.addEventListener('input', renderRows);
filter.addEventListener('change', renderRows);
document.querySelector('#refresh-button').addEventListener('click', () => showToast('Mock data refreshed locally'));
document.querySelector('#export-button').addEventListener('click', () => showToast('Briefing prepared locally; no file was uploaded'));
renderRows();