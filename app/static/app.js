const form = document.getElementById('launch-form');
const list = document.getElementById('launch-list');
const refreshBtn = document.getElementById('refresh-btn');
const activeLaunches = document.getElementById('active-launches');
const avgReadiness = document.getElementById('avg-readiness');
const criticalAlerts = document.getElementById('critical-alerts');

const defaultMilestones = [
  {
    id: 'm1',
    name: 'Core feature validation',
    owner: 'PM',
    status: 'done',
    priority: 'critical',
    dependency_ids: [],
  },
  {
    id: 'm2',
    name: 'Pricing lock',
    owner: 'Finance',
    status: 'in_progress',
    priority: 'high',
    dependency_ids: ['m1'],
  },
  {
    id: 'm3',
    name: 'Launch comms readiness',
    owner: 'Marketing',
    status: 'blocked',
    priority: 'critical',
    dependency_ids: ['m2'],
  },
];

async function fetchDashboard() {
  const res = await fetch('/api/dashboard');
  const data = await res.json();
  renderLaunches(data.launches || []);
  renderSummary(data.summary || {});
}

function renderSummary(summary) {
  activeLaunches.textContent = String(summary.active_launches ?? 0);
  avgReadiness.textContent = `${summary.average_readiness ?? 0}%`;
  criticalAlerts.textContent = String(summary.critical_alerts ?? 0);
}

function renderLaunches(launches) {
  if (!launches.length) {
    list.innerHTML = '<div class="empty-state">No launches tracked yet.</div>';
    return;
  }

  list.innerHTML = launches
    .map((launch) => {
      const assessment = launch.assessment || {};
      const readiness = assessment.readiness_score ?? 0;
      const riskLevel = assessment.risk_level || 'monitor';
      const summary = assessment.summary || 'Assessment pending';

      return `
        <article class="launch-card ${riskLevel}">
          <div class="launch-header">
            <div>
              <h4>${launch.product_name}</h4>
              <p>${launch.market} • ${launch.team}</p>
            </div>
            <span class="badge ${riskLevel}">${riskLevel}</span>
          </div>
          <div class="score-row">
            <div>
              <span>Readiness</span>
              <strong>${readiness}%</strong>
            </div>
            <div>
              <span>Launch date</span>
              <strong>${launch.launch_date || 'TBD'}</strong>
            </div>
          </div>
          <p class="summary">${summary}</p>
          <ul class="milestone-summary">
            ${(launch.milestones || []).slice(0, 4).map((item) => `<li>${item.name} • ${item.status}</li>`).join('') || '<li>No milestones yet</li>'}
          </ul>
        </article>
      `;
    })
    .join('');
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const payload = {
    product_name: formData.get('product_name'),
    launch_date: formData.get('launch_date') || null,
    market: formData.get('market'),
    team: formData.get('team'),
    status: formData.get('status'),
    milestones: defaultMilestones,
  };

  const res = await fetch('/api/launches', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (res.ok) {
    form.reset();
    fetchDashboard();
  }
});

refreshBtn.addEventListener('click', fetchDashboard);
fetchDashboard();
