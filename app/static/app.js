<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Hasti Launch Sentinel</title>
    <link rel="stylesheet" href="/static/styles.css" />
  </head>
  <body>
    <div class="app-shell">
      <header class="topbar">
        <div>
          <p class="eyebrow">Launch intelligence</p>
          <h1>Hasti Launch Sentinel</h1>
        </div>
        <button id="refreshBtn" class="secondary-btn">Refresh</button>
      </header>

      <main class="dashboard">
        <section class="panel hero-panel">
          <div>
            <p class="eyebrow">Portfolio overview</p>
            <h2>AI-powered launch risk detection</h2>
          </div>
          <div class="hero-metrics">
            <div class="metric-card">
              <span>Active launches</span>
              <strong id="activeLaunches">0</strong>
            </div>
            <div class="metric-card">
              <span>Average readiness</span>
              <strong id="avgReadiness">0%</strong>
            </div>
            <div class="metric-card danger">
              <span>Critical alerts</span>
              <strong id="criticalAlerts">0</strong>
            </div>
          </div>
        </section>

        <section class="panel">
          <h3>Create launch</h3>
          <form id="launchForm" class="launch-form">
            <input type="text" name="product_name" placeholder="Product name" required />
            <input type="date" name="launch_date" />
            <input type="text" name="market" placeholder="Market" value="US Enterprise" />
            <input type="text" name="team" placeholder="Team" value="Product + Growth" />
            <select name="status">
              <option value="planned">Planned</option>
              <option value="active">Active</option>
              <option value="at_risk">At risk</option>
              <option value="launched">Launched</option>
            </select>
            <button type="submit">Add launch</button>
          </form>
        </section>

        <section class="panel">
          <h3>Launch portfolio</h3>
          <div id="launchList" class="launch-list"></div>
        </section>
      </main>
    </div>

    <script src="/static/app.js"></script>
  </body>
</html>
