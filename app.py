
from flask import Flask, jsonify, render_template_string
import os
from datetime import datetime, timezone

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_NAME = "DevOps CI/CD Dashboard"
STARTED_AT = datetime.now(timezone.utc)


@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DevOps CI/CD Dashboard</title>
<style>
:root {
    --bg: #07111f;
    --panel: #0c1b2e;
    --border: #193453;
    --text: #e5efff;
    --muted: #91a9c9;
    --blue: #1685ff;
    --green: #00d49a;
}
* { box-sizing: border-box; }
body {
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: Inter, "Segoe UI", Arial, sans-serif;
}
header {
    min-height: 70px;
    padding: 18px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
    border-bottom: 1px solid var(--border);
    background: #091629;
}
.brand { font-size: 22px; font-weight: 750; }
.brand span { color: #32a4ff; }
.header-right { color: var(--muted); font-size: 13px; }
.pill {
    display: inline-block;
    padding: 7px 11px;
    border-radius: 20px;
    background: #063d34;
    color: #4fffc7;
    margin-right: 12px;
}
.layout { display: flex; min-height: calc(100vh - 70px); }
.sidebar {
    width: 205px;
    flex-shrink: 0;
    padding: 25px 14px;
    border-right: 1px solid var(--border);
    background: #091629;
}
.nav {
    display: block;
    color: #a8bdd9;
    padding: 14px;
    margin-bottom: 7px;
    border-radius: 8px;
    text-decoration: none;
}
.nav.active, .nav:hover {
    background: #10315b;
    color: #53b4ff;
}
main { padding: 30px; min-width: 0; flex: 1; }
.eyebrow { color: #43aaff; font-size: 13px; font-weight: 700; }
h1 { font-size: clamp(25px, 3vw, 34px); margin: 9px 0; }
.subtitle { color: var(--muted); line-height: 1.6; }
.grid { display: grid; gap: 16px; margin-top: 24px; }
.stats { grid-template-columns: repeat(5, minmax(0, 1fr)); }
.columns { grid-template-columns: 1.5fr 1fr; }
.bottom { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.card {
    min-width: 0;
    background: linear-gradient(145deg, #0d2037, #0a1729);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 20px;
}
.stat { border-top: 3px solid var(--blue); }
.stat.green { border-top-color: var(--green); }
.stat.purple { border-top-color: #9664ff; }
.stat.orange { border-top-color: #ff9e43; }
.stat.cyan { border-top-color: #18c9e8; }
.label { color: var(--muted); font-size: 13px; }
.value { font-size: 25px; font-weight: 750; margin: 13px 0 8px; }
.good { color: #3af0b4; }
.small { color: var(--muted); font-size: 12px; line-height: 1.6; }
.section-title {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    align-items: center;
    margin: 0 0 20px;
    font-size: 17px;
}
.stages {
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    gap: 8px;
}
.stage { text-align: center; font-size: 12px; }
.dot {
    width: 31px; height: 31px; margin: 0 auto 10px;
    display: grid; place-items: center;
    background: #063d34; color: #3af0b4;
    border: 1px solid #087e65; border-radius: 50%;
}
.bar {
    height: 8px; background: #193453;
    border-radius: 10px; overflow: hidden; margin: 12px 0 6px;
}
.bar span { display: block; height: 100%; background: var(--blue); }
.run {
    display: flex; align-items: flex-start; gap: 12px;
    padding: 14px 0; border-bottom: 1px solid var(--border);
}
.run:last-child { border-bottom: 0; }
.check {
    width: 30px; height: 30px; flex-shrink: 0;
    border-radius: 50%; background: #064436; color: #3af0b4;
    display: grid; place-items: center;
}
table { width: 100%; border-collapse: collapse; font-size: 13px; }
td { padding: 12px 4px; border-bottom: 1px solid var(--border); }
td:first-child { color: var(--muted); }
td:last-child { text-align: right; overflow-wrap: anywhere; }
.metric { margin: 17px 0; }
.metric-head { display: flex; justify-content: space-between; font-size: 13px; }
button {
    background: var(--blue); color: white; border: 0;
    padding: 11px 16px; border-radius: 7px;
    cursor: pointer; font-weight: 650;
}
button:hover { background: #006cda; }
#health-result { color: var(--green); font-size: 13px; margin-top: 12px; }
footer { color: var(--muted); text-align: center; padding: 25px; font-size: 12px; }
@media(max-width: 1100px) {
    .stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .columns, .bottom { grid-template-columns: 1fr; }
}
@media(max-width: 650px) {
    .sidebar { display: none; }
    main { padding: 18px 12px; }
    header { padding: 17px; }
    .stats { grid-template-columns: 1fr 1fr; }
    .stages { grid-template-columns: repeat(4, minmax(0, 1fr)); row-gap: 20px; }
    .card { padding: 15px; }
}
</style>
</head>
<body>
<header>
  <div class="brand"><span>◈</span> DevOps CI/CD Dashboard</div>
  <div class="header-right">
    <span class="pill">● Application Healthy</span>
    Version {{ version }}
  </div>
</header>

<div class="layout">
<aside class="sidebar">
  <a class="nav active" href="#overview">⌂ &nbsp; Overview</a>
  <a class="nav" href="#pipeline">⛓ &nbsp; Pipeline</a>
  <a class="nav" href="#deployments">⇧ &nbsp; Deployments</a>
  <a class="nav" href="#health">♥ &nbsp; Health Check</a>
  <a class="nav" href="#monitoring">▥ &nbsp; Monitoring</a>
  <div class="small" style="margin:35px 12px 0">POWERED BY<br><br>Python · Flask<br>Docker · Kubernetes</div>
</aside>

<main id="overview">
  <div class="eyebrow">YOUR DEVOPS CONTROL CENTER</div>
  <h1>DevOps CI/CD Pipeline</h1>
  <p class="subtitle">Build. Test. Scan. Deploy. Verify.</p>

  <div class="grid stats">
    <div class="card stat green">
      <div class="label">Application Status</div>
      <div class="value good">● Healthy</div>
      <div class="small">Flask application running</div>
    </div>
    <div class="card stat">
      <div class="label">Application Version</div>
      <div class="value">v{{ version }}</div>
      <div class="small">Configured version</div>
    </div>
    <div class="card stat purple">
      <div class="label">Pipeline</div>
      <div class="value">Ready</div>
      <div class="small">Awaiting CI workflow</div>
    </div>
    <div class="card stat cyan">
      <div class="label">Health Endpoint</div>
      <div class="value">/health</div>
      <div class="small">HTTP health check</div>
    </div>
    <div class="card stat orange">
      <div class="label">Deployment</div>
      <div class="value">Local</div>
      <div class="small">Development environment</div>
    </div>
  </div>

  <div class="grid columns" id="pipeline">
    <section class="card">
      <h2 class="section-title">⚡ Pipeline Overview
        <span class="small">Planned workflow</span>
      </h2>
      <div class="stages">
        {% for stage in stages %}
        <div class="stage">
          <div class="dot">{{ loop.index }}</div>
          <div>{{ stage }}</div>
        </div>
        {% endfor %}
      </div>
      <div style="margin-top:28px">
        <h3 class="section-title">CI/CD Workflow Progress</h3>
        {% for label, width in progress %}
        <div class="metric">
          <div class="metric-head"><span>{{ label }}</span><span>{{ width }}%</span></div>
          <div class="bar"><span style="width:{{ width }}%"></span></div>
        </div>
        {% endfor %}
        <p class="small">Illustrative workflow progress, not live GitHub Actions data.</p>
      </div>
    </section>

    <section class="card" id="deployments">
      <h2 class="section-title">Deployment Activity</h2>
      <div class="run">
        <div class="check">✓</div>
        <div><strong>Application started</strong><div class="small">Current local session</div></div>
      </div>
      <div class="run">
        <div class="check">✓</div>
        <div><strong>Health endpoint available</strong><div class="small">GET /health</div></div>
      </div>
      <div class="run">
        <div class="check">○</div>
        <div><strong>Automated CI pipeline</strong><div class="small">To be configured</div></div>
      </div>
      <div class="run">
        <div class="check">○</div>
        <div><strong>Kubernetes deployment</strong><div class="small">Upcoming project stage</div></div>
      </div>
    </section>
  </div>

  <div class="grid bottom">
    <section class="card">
      <h2 class="section-title">▤ Application Details</h2>
      <table>
        <tr><td>Application</td><td>DevOps Dashboard</td></tr>
        <tr><td>Framework</td><td>Python / Flask</td></tr>
        <tr><td>Version</td><td>{{ version }}</td></tr>
        <tr><td>Environment</td><td>{{ environment }}</td></tr>
        <tr><td>Health route</td><td>/health</td></tr>
      </table>
    </section>

    <section class="card" id="health">
      <h2 class="section-title">♥ Health Check</h2>
      <p class="subtitle">Check whether the Flask service responds.</p>
      <div class="metric-head"><span>Service</span><span class="good">● Available</span></div>
      <div class="metric-head" style="margin-top:16px"><span>Endpoint</span><span>/health</span></div>
      <div class="metric-head" style="margin-top:16px"><span>HTTP status</span><span id="http-status">Not checked</span></div>
      <button style="margin-top:22px;width:100%" onclick="checkHealth()">↻ Check Now</button>
      <div id="health-result" role="status" aria-live="polite"></div>
    </section>

    <section class="card" id="monitoring">
      <h2 class="section-title">▥ System Metrics</h2>
      <p class="subtitle">Demo values for dashboard layout only.</p>
      {% for label, value in demo_metrics %}
      <div class="metric">
        <div class="metric-head"><span>{{ label }}</span><span>{{ value }}%</span></div>
        <div class="bar"><span style="width:{{ value }}%"></span></div>
      </div>
      {% endfor %}
      <p class="small">Connect Prometheus or CloudWatch for real metrics.</p>
    </section>
  </div>
  <footer>DevOps CI/CD Portfolio Project · Flask · Docker · GitHub Actions · Kubernetes</footer>
</main>
</div>
<script>
async function checkHealth() {
    const result = document.getElementById("health-result");
    const status = document.getElementById("http-status");
    result.textContent = "Checking service...";
    try {
        const response = await fetch("/health", {cache: "no-store"});
        const data = await response.json();
        status.textContent = response.status;
        result.textContent = response.ok
            ? "✓ " + data.status + " · Version " + data.version
            : "Service returned an error";
    } catch (error) {
        status.textContent = "Unavailable";
        result.textContent = "✕ Health check failed";
    }
}
</script>
</body>
</html>
    """, version=APP_VERSION,
       environment=os.getenv("APP_ENV", "development"),
       stages=["Code Push", "Build", "Test", "Scan", "Publish", "Deploy", "Verify"],
       progress=[("Code & configuration", 100),
                 ("Automated tests", 0),
                 ("Docker image", 0),
                 ("Deployment", 0)],
       demo_metrics=[("CPU (demo)", 32),
                     ("Memory (demo)", 58),
                     ("Disk (demo)", 41)])


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION,
        "application": APP_NAME
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
