export const mobileAppPage = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>EcoSphere X Mobile Preview</title>
    <style>
      :root {
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #f3f7f2;
        color: #0b1c17;
      }
      body {
        margin: 0;
        padding: 16px;
        display: flex;
        justify-content: center;
      }
      .app-shell {
        max-width: 480px;
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }
      .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 14px;
        background: linear-gradient(135deg, #1b5e20, #43a047);
        border-radius: 16px;
        color: #f1f8e9;
        box-shadow: 0 8px 24px rgba(27, 94, 32, 0.25);
      }
      .header h1 {
        margin: 0;
        font-size: 20px;
        letter-spacing: -0.02em;
      }
      .pill {
        padding: 6px 10px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 999px;
        font-size: 12px;
      }
      .card {
        background: #ffffff;
        border-radius: 14px;
        padding: 14px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
        border: 1px solid #e3f2e1;
      }
      .card h2 {
        margin: 0 0 6px;
        font-size: 16px;
        color: #184d2e;
      }
      .score {
        font-size: 36px;
        font-weight: 700;
        margin: 8px 0 2px;
      }
      .muted {
        color: #4f6f65;
        font-size: 13px;
      }
      .row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
      }
      .chip {
        background: #e8f5e9;
        color: #1b5e20;
        padding: 6px 10px;
        border-radius: 12px;
        font-size: 12px;
        border: 1px solid #c8e6c9;
      }
      .list {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 6px;
      }
      .list-item {
        padding: 10px 12px;
        background: #f9fcf8;
        border-radius: 12px;
        border: 1px solid #e6f2e4;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
      }
      .btn {
        background: #2e7d32;
        color: #ffffff;
        border: none;
        border-radius: 12px;
        padding: 10px 14px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.25);
      }
      .btn.secondary {
        background: #ffffff;
        color: #2e7d32;
        border: 1px solid #c8e6c9;
        box-shadow: none;
      }
      .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 10px;
      }
      form {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 8px;
      }
      input, select, textarea {
        padding: 10px 12px;
        border-radius: 10px;
        border: 1px solid #dfe8dd;
        font-size: 14px;
      }
      textarea {
        min-height: 72px;
        resize: vertical;
      }
      .status {
        margin-top: 6px;
        font-size: 13px;
        color: #1b5e20;
      }
    </style>
  </head>
  <body>
    <div class="app-shell">
      <div class="header">
        <div>
          <div class="pill">EcoSphere X</div>
          <h1>Mobile Experience</h1>
        </div>
        <button class="btn secondary" id="refresh">Refresh</button>
      </div>

      <div class="card" id="carbon-card">
        <h2>Carbon Wallet</h2>
        <div class="score" id="score">--</div>
        <div class="muted" id="headline">Loading footprint...</div>
        <div class="list" id="breakdown"></div>
      </div>

      <div class="card" id="leaderboard-card">
        <h2>EcoRank</h2>
        <div class="muted" id="rank-meta"></div>
        <div class="list" id="leaders"></div>
      </div>

      <div class="card" id="community-card">
        <h2>EcoCircle</h2>
        <div class="list" id="groups"></div>
        <div class="list" id="events"></div>
      </div>

      <div class="card" id="badges-card">
        <h2>EcoBadge</h2>
        <div class="grid" id="badges"></div>
      </div>

      <div class="card" id="nudges-card">
        <h2>EcoNudge</h2>
        <div class="list" id="reminders"></div>
      </div>

      <div class="card" id="shop-card">
        <h2>EcoShop</h2>
        <div class="list" id="recommendations"></div>
      </div>

      <div class="card" id="alert-card">
        <h2>EcoAlert</h2>
        <p class="muted">Report illegal dumping or unusual waste.</p>
        <form id="alert-form">
          <input type="text" name="description" placeholder="Description" required />
          <input type="text" name="location" placeholder="Location (lat,long)" required />
          <input type="url" name="photoUrl" placeholder="Photo URL (optional)" />
          <button class="btn" type="submit">Submit report</button>
          <div class="status" id="alert-status"></div>
        </form>
      </div>
    </div>

    <script>
      const endpoints = {
        carbon: '/api/dashboard/carbon',
        leaderboard: '/api/leaderboard',
        community: '/api/community',
        badges: '/api/badges',
        reminders: '/api/reminders',
        recommendations: '/api/recommendations',
        alerts: '/api/alerts'
      };

      const fallback = {
        carbon: {
          score: 72,
          headline: 'Travel footprint decreased by 14% this week',
          breakdown: [
            { area: 'travel', kgCO2e: 8.6, change: -14 },
            { area: 'home_energy', kgCO2e: 12.2, change: -3 },
            { area: 'shopping', kgCO2e: 5.1, change: 4 },
            { area: 'waste', kgCO2e: 2.2, change: -8 },
          ]
        },
        leaderboard: {
          percentile: 12,
          city: 'Global',
          globalRank: 120,
          cityRank: 24,
          rewards: ['Weekly streak bonus', 'City top-25% badge'],
          leaders: [
            { name: 'You', score: 82, rank: 24, city: 'Global' },
            { name: 'Aditi', score: 90, rank: 1, city: 'Global' },
            { name: 'Rahul', score: 86, rank: 2, city: 'Global' },
          ],
        },
        community: {
          groups: [
            { name: 'Campus Green Circle', members: 120, invitesOpen: true },
            { name: 'Neighborhood Composters', members: 58, invitesOpen: false },
          ],
          events: [
            { title: 'Beach cleanup', location: 'Marina', date: '2025-02-18', spotsLeft: 24, rsvp: true },
            { title: 'Clothes swap', location: 'Community Hall', date: '2025-02-22', spotsLeft: 12, rsvp: false },
          ],
        },
        badges: [
          { name: 'Local Shopper', description: '72% local purchases', month: '2025-01', unlocked: true },
          { name: 'Reuse Hero', description: '5 items refilled', month: '2025-01', unlocked: true },
        ],
        reminders: [
          { title: 'Expiry approaching', next_trigger_at: '2025-01-08T08:00:00Z', channel: 'push', actionable: true },
          { title: 'Log commute', next_trigger_at: '2025-01-09T07:00:00Z', channel: 'push', actionable: false },
        ],
        recommendations: [
          { title: 'Switch to refill packs', savingsKg: 1.1, partner: 'Refill Co', link: 'https://example.com/refill' },
          { title: 'Bike to work twice a week', savingsKg: 2.4, partner: 'EcoMiles Boost', link: 'https://example.com/ecomiles' },
        ],
      };

      async function fetchJson(url) {
        try {
          const response = await fetch(url);
          if (!response.ok) throw new Error('bad status');
          return await response.json();
        } catch (err) {
          console.warn('Falling back for', url, err);
          return null;
        }
      }

      function renderCarbon(data) {
        document.getElementById('score').textContent = data.score;
        document.getElementById('headline').textContent = data.headline;
        const wrap = document.getElementById('breakdown');
        wrap.innerHTML = data.breakdown
          .map((b) => `<div class="list-item"><div><strong>${b.area}</strong><div class="muted">${b.kgCO2e} kg CO₂e</div></div><span class="chip">${b.change}%</span></div>`)
          .join('');
      }

      function renderLeaderboard(data) {
        document.getElementById('rank-meta').textContent = `Top ${data.percentile}% · City rank ${data.cityRank}`;
        const wrap = document.getElementById('leaders');
        wrap.innerHTML = data.leaders
          .map((l) => `<div class="list-item"><div><strong>#${l.rank} ${l.name}</strong><div class="muted">${l.city}</div></div><span class="chip">${l.score} pts</span></div>`)
          .join('');
      }

      function renderCommunity(data) {
        const groupWrap = document.getElementById('groups');
        groupWrap.innerHTML = data.groups
          .map((g) => `<div class="list-item"><div><strong>${g.name}</strong><div class="muted">${g.members} members</div></div><span class="chip">${g.invitesOpen ? 'Open' : 'Closed'}</span></div>`)
          .join('');
        const eventWrap = document.getElementById('events');
        eventWrap.innerHTML = data.events
          .map((e) => `<div class="list-item"><div><strong>${e.title}</strong><div class="muted">${e.location} · ${e.date}</div></div><span class="chip">${e.spotsLeft} spots</span></div>`)
          .join('');
      }

      function renderBadges(data) {
        const wrap = document.getElementById('badges');
        wrap.innerHTML = data
          .map((b) => `<div class="list-item"><div><strong>${b.name}</strong><div class="muted">${b.description}</div></div><span class="chip">${b.unlocked ? 'Unlocked' : 'Locked'}</span></div>`)
          .join('');
      }

      function renderReminders(data) {
        const wrap = document.getElementById('reminders');
        wrap.innerHTML = data
          .map((r) => `<div class="list-item"><div><strong>${r.title}</strong><div class="muted">${new Date(r.next_trigger_at).toLocaleString()}</div></div><span class="chip">${r.channel}</span></div>`)
          .join('');
      }

      function renderRecommendations(data) {
        const wrap = document.getElementById('recommendations');
        wrap.innerHTML = data
          .map((rec) => `<div class="list-item"><div><strong>${rec.title}</strong><div class="muted">Save ${rec.savingsKg} kg CO₂e/mo</div></div><a class="chip" href="${rec.link}" target="_blank" rel="noreferrer">${rec.partner}</a></div>`)
          .join('');
      }

      async function hydrate() {
        const [carbon, leaderboard, community, badges, reminders, recommendations] = await Promise.all([
          fetchJson(endpoints.carbon),
          fetchJson(endpoints.leaderboard),
          fetchJson(endpoints.community),
          fetchJson(endpoints.badges),
          fetchJson(endpoints.reminders),
          fetchJson(endpoints.recommendations),
        ]);

        renderCarbon(carbon || fallback.carbon);
        renderLeaderboard(leaderboard || fallback.leaderboard);
        renderCommunity(community || fallback.community);
        renderBadges(badges || fallback.badges);
        renderReminders(reminders || fallback.reminders);
        renderRecommendations(recommendations || fallback.recommendations);
      }

      document.getElementById('refresh').addEventListener('click', hydrate);

      document.getElementById('alert-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = e.target;
        const payload = Object.fromEntries(new FormData(form).entries());
        const statusNode = document.getElementById('alert-status');
        statusNode.textContent = 'Submitting...';
        try {
          const res = await fetch(endpoints.alerts, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          });
          if (!res.ok) throw new Error('Failed');
          const json = await res.json();
          statusNode.textContent = 'Report submitted: ' + (json.status || 'submitted');
          form.reset();
        } catch (err) {
          statusNode.textContent = 'Offline mode: saved locally';
        }
      });

      hydrate();
    </script>
  </body>
</html>`;
