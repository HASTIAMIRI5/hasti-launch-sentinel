# hasti-launch-sentinel

AI product launch tracker and risk detector for product, growth, and GTM teams.

## Why this project matters

Product launches fail because teams track the wrong signals: vague launch readiness, hidden dependency risk, inconsistent milestone visibility, and no single place to spot launch threats early. This project turns that into a clear operational system:

- launch readiness scorecards
- risk detection by task and dependency health
- milestone tracking across product, marketing, and sales
- decision-oriented recommendations for launch owners

## Features

- Launch dashboard with KPIs and risk status
- Automatic risk analysis for product launch health
- Milestone tracking with deadline and dependency awareness
- REST API for integrations and dashboards
- FastAPI backend with static web UI
- Built-in tests for risk scoring logic

## Tech stack

- Python 3.12+
- FastAPI
- Pydantic
- Uvicorn
- Pytest

## Quick start

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Open the dashboard:

   ```text
   http://localhost:8000
   ```

5. API base URL:

   ```text
   http://localhost:8000/api
   ```

## Example API calls

Create a launch:

```bash
curl -X POST http://localhost:8000/api/launches \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Nimbus AI",
    "launch_date": "2026-11-15",
    "market": "US Enterprise",
    "team": "Growth + Product",
    "status": "planned",
    "milestones": [
      {"id": "m1", "name": "Alpha validation", "owner": "PM", "status": "done", "priority": "critical"},
      {"id": "m2", "name": "Pricing finalization", "owner": "Revenue", "status": "in_progress", "priority": "high"},
      {"id": "m3", "name": "Partner enablement", "owner": "BD", "status": "blocked", "priority": "critical"}
    ]
  }'
```

List launches:

```bash
curl http://localhost:8000/api/launches
```

## Project structure

```text
app/
  __init__.py
  main.py
  models.py
  api/
    __init__.py
    routes.py
  services/
    __init__.py
    data_store.py
    risk_engine.py
  static/
    index.html
    app.js
    styles.css

data/
  launches.json

tests/
  test_risk_engine.py
```

## Risk model

The application scores launch readiness using factors such as:

- milestone completion rate
- unresolved blocked work
- critical tasks remaining close to launch date
- dependency coverage and bottlenecks
- overall launch confidence

Generated output includes:

- readiness score (0-100)
- risk level
- findings with recommendations
- launch summary

## License

MIT
