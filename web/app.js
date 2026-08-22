const arrivals = [
  { tail: 'N100SP', station: 'LHR-H1', arrival: 'Today, 14:20', part: 'PUMP-100', compliance: 'Verified', constraint: 'Clear', status: 'green', label: 'Ready' },
  { tail: 'N200SP', station: 'JFK-H2', arrival: 'Today, 15:05', part: 'VALVE-200', compliance: 'Quarantined', constraint: 'Clear', status: 'red', label: 'Blocked' },
  { tail: 'N318SP', station: 'DXB-H3', arrival: 'Today, 16:40', part: 'FILTER-318', compliance: 'Verified', constraint: 'Vehicle wait', status: 'yellow', label: 'At risk' },
  { tail: 'N442SP', station: 'SIN-H1', arrival: 'Today, 18:15', part: 'ACTUATOR-442', compliance: 'Verified', constraint: 'Clear', status: 'green', label: 'Ready' },
];

const monthlyFlights = [
  { flight: 'SPM 101', tail: 'N100SP', route: 'LHR → JFK', departure: '01 Aug · 06:20', arrival: '01 Aug · 09:05', station: 'LHR-H1', status: 'On time', tone: 'green' },
  { flight: 'SPM 102', tail: 'N200SP', route: 'JFK → LHR', departure: '03 Aug · 11:40', arrival: '03 Aug · 23:10', station: 'JFK-H2', status: 'Parts watch', tone: 'red' },
  { flight: 'SPM 103', tail: 'N318SP', route: 'DXB → SIN', departure: '05 Aug · 02:15', arrival: '05 Aug · 12:40', station: 'DXB-H3', status: 'On time', tone: 'green' },
  { flight: 'SPM 104', tail: 'N442SP', route: 'SIN → SYD', departure: '07 Aug · 18:00', arrival: '08 Aug · 03:15', station: 'SIN-H1', status: 'On time', tone: 'green' },
  { flight: 'SPM 105', tail: 'N100SP', route: 'JFK → LHR', departure: '10 Aug · 14:10', arrival: '11 Aug · 01:40', station: 'JFK-H2', status: 'MEL monitored', tone: 'yellow' },
  { flight: 'SPM 106', tail: 'N200SP', route: 'LHR → DXB', departure: '12 Aug · 20:35', arrival: '13 Aug · 06:55', station: 'LHR-H1', status: 'On time', tone: 'green' },
  { flight: 'SPM 107', tail: 'N318SP', route: 'DXB → LHR', departure: '15 Aug · 09:25', arrival: '15 Aug · 14:10', station: 'DXB-H3', status: 'Ground watch', tone: 'yellow' },
  { flight: 'SPM 108', tail: 'N442SP', route: 'SYD → SIN', departure: '18 Aug · 05:50', arrival: '18 Aug · 12:20', station: 'SIN-H1', status: 'On time', tone: 'green' },
  { flight: 'SPM 109', tail: 'N100SP', route: 'LHR → JFK', departure: '21 Aug · 06:20', arrival: '21 Aug · 09:05', station: 'LHR-H1', status: 'Parts watch', tone: 'red' },
  { flight: 'SPM 110', tail: 'N200SP', route: 'JFK → SIN', departure: '24 Aug · 16:45', arrival: '26 Aug · 06:30', station: 'JFK-H2', status: 'On time', tone: 'green' },
  { flight: 'SPM 111', tail: 'N318SP', route: 'SIN → DXB', departure: '27 Aug · 21:10', arrival: '28 Aug · 04:50', station: 'SIN-H1', status: 'MEL monitored', tone: 'yellow' },
  { flight: 'SPM 112', tail: 'N442SP', route: 'DXB → LHR', departure: '30 Aug · 03:40', arrival: '30 Aug · 08:25', station: 'DXB-H3', status: 'On time', tone: 'green' },
];

const inventory = [
  { part: 'PUMP-100', serial: 'SN-001', station: 'LHR-H1', state: 'Verified', tone: 'green' },
  { part: 'VALVE-200', serial: 'SN-002', station: 'JFK-H2', state: 'Quarantined', tone: 'red' },
  { part: 'FILTER-318', serial: 'SN-318', station: 'DXB-H3', state: 'Verified', tone: 'green' },
];
const orders = [
  { part: 'VALVE-200', reason: 'No compliant stock', due: 'MEL · 36h', tone: 'red' },
  { part: 'ACTUATOR-442', reason: 'Network stockout', due: 'Demand · 7d', tone: 'yellow' },
];
const transfers = [
  { part: 'PUMP-100', route: 'LHR-H1 → JFK-H2', eta: 'ETA 14:30', tone: 'green' },
  { part: 'FILTER-318', route: 'DXB-H3 → SIN-H1', eta: 'In transit', tone: 'yellow' },
  { part: 'ACTUATOR-442', route: 'SIN-H1 → LHR-H1', eta: 'ETA 22 Aug', tone: 'blue' },
];
const hangars = [
  { city: 'Dallas', airport: 'DFW', hangar: 'DFW-H1', capacity: '12 aircraft', status: 'Ready', tone: 'green', focus: 'Rotable staging' },
  { city: 'Atlanta', airport: 'ATL', hangar: 'ATL-H2', capacity: '10 aircraft', status: 'Ready', tone: 'green', focus: 'MEL support' },
  { city: 'Chicago', airport: 'ORD', hangar: 'ORD-H1', capacity: '8 aircraft', status: 'At risk', tone: 'yellow', focus: 'Vehicle shortage' },
  { city: 'Houston', airport: 'IAH', hangar: 'IAH-H3', capacity: '9 aircraft', status: 'Ready', tone: 'green', focus: 'Engine components' },
  { city: 'Denver', airport: 'DEN', hangar: 'DEN-H1', capacity: '7 aircraft', status: 'At risk', tone: 'yellow', focus: 'Weather watch' },
  { city: 'Florida', airport: 'MIA', hangar: 'MIA-H2', capacity: '11 aircraft', status: 'Ready', tone: 'green', focus: 'Line maintenance' },
];
const demandReport = [
  { date: '01 Aug', required: 18, consumed: 17 }, { date: '07 Aug', required: 22, consumed: 24 },
  { date: '14 Aug', required: 20, consumed: 19 }, { date: '18 Aug', required: 28, consumed: 30 },
  { date: '21 Aug', required: 26, consumed: 25 }, { date: '26 Aug', required: 32, consumed: 34 },
  { date: '31 Aug', required: 30, consumed: 33 },
];

const detailViews = {
  staging: {
    title: 'Staging board', subtitle: 'Live-style readiness view using local mock visits',
    columns: ['Aircraft', 'Station', 'Required parts', 'Documentation', 'MEL window', 'Action'],
    rows: [
      ['N100SP', 'LHR-H1', 'PUMP-100', 'Verified', '36 hours', 'Ready to kit'],
      ['N200SP', 'JFK-H2', 'VALVE-200', 'Quarantined', 'No MEL', 'Resolve certificate'],
      ['N318SP', 'DXB-H3', 'FILTER-318', 'Verified', '72 hours', 'Vehicle wait'],
      ['N442SP', 'SIN-H1', 'ACTUATOR-442', 'Verified', 'No MEL', 'Ready to kit'],
    ],
  },
  forecast: {
    title: 'Demand forecast', subtitle: 'Mock demand outlook based on historical consumption',
    columns: ['Part number', 'Current stock', '30-day demand', 'Forecast confidence', 'Signal', 'Recommendation'],
    rows: [
      ['PUMP-100', '4 verified', '6 units', '91%', 'Rising', 'Rebalance 2 units'],
      ['VALVE-200', '0 compliant', '3 units', '88%', 'Critical', 'Create PO now'],
      ['FILTER-318', '8 verified', '5 units', '86%', 'Stable', 'Maintain buffer'],
      ['ACTUATOR-442', '0 compliant', '2 units', '82%', 'Rising', 'Create PO now'],
    ],
  },
  procurement: {
    title: 'Procurement details', subtitle: 'Mock purchase queue and approval status',
    columns: ['PO reference', 'Part number', 'Quantity', 'Priority', 'Approval', 'Next step'],
    rows: [
      ['MOCK-PO-001', 'VALVE-200', '1', 'Critical · MEL', 'Pending approval', 'Review certificate'],
      ['MOCK-PO-002', 'ACTUATOR-442', '1', 'High · demand', 'Draft', 'Route for approval'],
      ['MOCK-PO-003', 'PUMP-100', '2', 'Medium · buffer', 'Approved', 'Mock transfer'],
    ],
  },
};

const rows = document.querySelector('#arrival-rows');
const search = document.querySelector('#search-input');
const filter = document.querySelector('#status-filter');
const toast = document.querySelector('#toast');
const monthlySearch = document.querySelector('#monthly-search');

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

function renderMonthlyFlights() {
  const query = monthlySearch.value.trim().toLowerCase();
  const filtered = monthlyFlights.filter((item) => `${item.flight} ${item.tail} ${item.route} ${item.station}`.toLowerCase().includes(query));
  document.querySelector('#monthly-flight-rows').innerHTML = filtered.map((item) => `
    <tr><td><div class="aircraft"><span class="plane-icon">✈</span><span><strong>${item.flight}</strong><small>${item.tail}</small></span></div></td><td>${item.route}</td><td>${item.departure}</td><td>${item.arrival}</td><td>${item.station}</td><td><span class="status-pill status-${item.tone}">${item.status}</span></td></tr>`).join('');
  document.querySelector('#monthly-row-count').textContent = filtered.length;
}

function renderPartsOperations() {
  document.querySelector('#inventory-list').innerHTML = inventory.map((item) => `<div class="part-row"><span class="part-symbol">▣</span><span class="part-info"><strong>${item.part}</strong><small>${item.serial} · ${item.station}</small></span><span class="status-pill status-${item.tone}">${item.state}</span></div>`).join('');
  document.querySelector('#order-list').innerHTML = orders.map((item) => `<div class="part-row"><span class="part-symbol order-symbol">!</span><span class="part-info"><strong>${item.part}</strong><small>${item.reason}</small></span><span class="part-due">${item.due}</span></div>`).join('');
  document.querySelector('#transfer-list').innerHTML = transfers.map((item) => `<div class="part-row"><span class="part-symbol transfer-symbol">↗</span><span class="part-info"><strong>${item.part}</strong><small>${item.route}</small></span><span class="status-pill status-${item.tone === 'blue' ? 'green' : item.tone}">${item.eta}</span></div>`).join('');
}

function renderDemandReport() {
  document.querySelector('#actual-report-rows').innerHTML = demandReport.map((item) => {
    const variance = item.consumed - item.required;
    return `<tr><td>${item.date}</td><td>${item.required}</td><td>${item.consumed}</td><td class="${variance > 0 ? 'variance-high' : 'variance-low'}">${variance > 0 ? '+' : ''}${variance}</td></tr>`;
  }).join('');
}

function renderHangars() {
  document.querySelector('#hangar-list').innerHTML = hangars.map((item) => `<div class="hangar-card"><div class="hangar-code">${item.airport}</div><div class="hangar-info"><strong>${item.city} · ${item.hangar}</strong><small>${item.capacity} · ${item.focus}</small></div><span class="status-pill status-${item.tone}">${item.status}</span></div>`).join('');
}

function renderDetailView(view) {
  const panel = document.querySelector('#detail-view');
  const detail = detailViews[view];
  if (!detail) {
    panel.hidden = true;
    return;
  }
  panel.hidden = false;
  panel.innerHTML = `<div class="panel-heading"><div><h2>${detail.title}</h2><p class="muted">${detail.subtitle}</p></div><span class="mock-tag">LOCAL MOCK VIEW</span></div><div class="table-scroll detail-table"><table><thead><tr>${detail.columns.map((column) => `<th>${column}</th>`).join('')}</tr></thead><tbody>${detail.rows.map((row) => `<tr>${row.map((cell, index) => `<td class="${index === row.length - 1 ? 'detail-action' : ''}">${cell}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
}

document.querySelectorAll('[data-view], [data-view-link]').forEach((control) => {
  control.addEventListener('click', () => {
    const view = control.dataset.view || control.dataset.viewLink;
    const labels = { overview: 'Overview', staging: 'Staging board', forecast: 'Demand forecast', procurement: 'Procurement' };
    document.querySelectorAll('.nav-item').forEach((item) => item.classList.toggle('active', item.dataset.view === view));
    document.querySelector('#page-title').textContent = labels[view];
    renderDetailView(view);
    showToast(`${labels[view]} view is available in the mock workspace`);
  });
});

search.addEventListener('input', renderRows);
filter.addEventListener('change', renderRows);
monthlySearch.addEventListener('input', renderMonthlyFlights);
document.querySelector('#refresh-button').addEventListener('click', () => showToast('Mock data refreshed locally'));
document.querySelector('#export-button').addEventListener('click', () => showToast('Briefing prepared locally; no file was uploaded'));
renderRows();
renderMonthlyFlights();
renderPartsOperations();
renderDemandReport();
renderHangars();