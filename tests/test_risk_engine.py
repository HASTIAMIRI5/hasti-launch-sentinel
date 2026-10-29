* {
  box-sizing: border-box;
}

:root {
  --bg: #07111f;
  --panel: #101d30;
  --panel-strong: #0d1728;
  --border: rgba(148, 163, 184, 0.2);
  --text: #e5eefb;
  --muted: #9ab0d1;
  --accent: #5eead4;
  --warning: #fbbf24;
  --danger: #f87171;
  --success: #34d399;
}

body {
  margin: 0;
  background: linear-gradient(135deg, #07111f 0%, #0d1728 100%);
  color: var(--text);
  font-family: Inter, Arial, sans-serif;
}

.app-shell {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 20px 60px;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.eyebrow {
  margin: 0 0 8px;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 11px;
  color: var(--muted);
}

h1, h2, h3, h4, p {
  margin-top: 0;
}

h1 {
  margin-bottom: 0;
  font-size: clamp(2rem, 4vw, 3rem);
}

.dashboard {
  display: grid;
  gap: 24px;
}

.panel {
  background: rgba(16, 29, 48, 0.9);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 14px 40px rgba(2, 6, 23, 0.25);
}

.hero-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.hero-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(120px, 1fr));
  gap: 16px;
  width: min(100%, 520px);
}

.metric-card {
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 16px 18px;
}

.metric-card span {
  display: block;
  color: var(--muted);
  font-size: 12px;
  margin-bottom: 8px;
}

.metric-card strong {
  font-size: 2rem;
}

.metric-card.danger strong {
  color: var(--danger);
}

.launch-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
}

input, select, button {
  border-radius: 12px;
  border: 1px solid var(--border);
  padding: 12px 14px;
  font: inherit;
}

input, select {
  background: rgba(15, 23, 42, 0.8);
  color: var(--text);
}

button {
  background: linear-gradient(135deg, #2dd4bf, #22c55e);
  color: #03221d;
  font-weight: 700;
  border: none;
  cursor: pointer;
}

.secondary-btn {
  background: rgba(15, 23, 42, 0.8);
  color: var(--text);
  border: 1px solid var(--border);
}

.launch-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
}

.launch-card {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 18px;
}

.launch-card.critical {
  border-color: rgba(248, 113, 113, 0.5);
}

.launch-card.watch {
  border-color: rgba(251, 191, 36, 0.5);
}

.launch-card.healthy {
  border-color: rgba(52, 211, 153, 0.5);
}

.launch-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.launch-header h4 {
  margin-bottom: 6px;
  font-size: 1.2rem;
}

.launch-header p,
.summary,
.milestone-summary {
  color: var(--muted);
}

.badge {
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-top: 4px;
}

.badge.healthy {
  background: rgba(52, 211, 153, 0.15);
  color: var(--success);
}

.badge.monitor,
.badge.watch {
  background: rgba(251, 191, 36, 0.15);
  color: var(--warning);
}

.badge.critical {
  background: rgba(248, 113, 113, 0.15);
  color: var(--danger);
}

.score-row {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
}

.score-row span {
  display: block;
  color: var(--muted);
  font-size: 12px;
}

.score-row strong {
  font-size: 1.1rem;
}

.milestone-summary {
  padding-left: 18px;
  margin: 0;
}

.empty-state {
  color: var(--muted);
  padding: 18px;
  border: 1px dashed var(--border);
  border-radius: 12px;
}

@media (max-width: 720px) {
  .hero-panel {
    flex-direction: column;
    align-items: flex-start;
  }

  .hero-metrics {
    width: 100%;
  }
}
