import { fromHono } from "chanfana";
import { Hono } from "hono";
import { CarbonDashboard, Leaderboard, Community, AlertReport, BadgeList, ReminderList, RecommendationList } from "./endpoints/ecoFeatures";
import { TaskCreate } from "./endpoints/taskCreate";
import { TaskDelete } from "./endpoints/taskDelete";
import { TaskFetch } from "./endpoints/taskFetch";
import { TaskList } from "./endpoints/taskList";
import { mobileAppPage } from "./frontend/mobile";

// Start a Hono app
const app = new Hono<{ Bindings: Env }>();

// Setup OpenAPI registry
const openapi = fromHono(app, {
        docs_url: "/",
});

// Register OpenAPI endpoints
openapi.get("/api/tasks", TaskList);
openapi.post("/api/tasks", TaskCreate);
openapi.get("/api/tasks/:taskSlug", TaskFetch);
openapi.delete("/api/tasks/:taskSlug", TaskDelete);

openapi.get("/api/dashboard/carbon", CarbonDashboard);
openapi.get("/api/leaderboard", Leaderboard);
openapi.get("/api/community", Community);
openapi.post("/api/alerts", AlertReport);
openapi.get("/api/badges", BadgeList);
openapi.get("/api/reminders", ReminderList);
openapi.get("/api/recommendations", RecommendationList);

// Lightweight frontend overview for mobile team
app.get("/frontend", (c) =>
        c.html(`
                <html>
                        <head>
                                <title>EcoSphere X Frontend Mock</title>
                                <style>
                                        body { font-family: Arial, sans-serif; margin: 2rem; line-height: 1.6; }
                                        h1 { color: #1b5e20; }
                                        section { margin-bottom: 1.5rem; }
                                        .card { border: 1px solid #c8e6c9; padding: 1rem; border-radius: 8px; background: #f1f8e9; }
                                </style>
                        </head>
                        <body>
                                <h1>EcoSphere X Feature Mock</h1>
                                <p>This lightweight screen mirrors the mobile endpoints for leaderboard, badges, nudges, and recommendations.</p>
                                <section class="card">
                                        <h2>EcoRank</h2>
                                        <p>Top 12% in your city this week. Rewards: streak bonus, top-25% badge.</p>
                                </section>
                                <section class="card">
                                        <h2>EcoCircle</h2>
                                        <p>Upcoming: Beach cleanup (RSVP yes), Clothes swap (RSVP open).</p>
                                </section>
                                <section class="card">
                                        <h2>EcoAlerts & Badges</h2>
                                        <p>Submit waste reports for +35 EcoPoints. Badges unlocked: Local Shopper, Reuse Hero.</p>
                                </section>
                                <section class="card">
                                        <h2>EcoNudge</h2>
                                        <p>2 items expire in 2 days — update disposal plan?</p>
                                </section>
                                <section class="card">
                                        <h2>EcoShop</h2>
                                        <p>Switch to refill packs to save 1.1kg CO₂e/month. Partner offers available.</p>
                                </section>
                        </body>
                </html>
        `),
);

// Mobile-style UI that hydrates against the eco feature endpoints
app.get("/mobile", (c) => c.html(mobileAppPage));

// Export the Hono app
export default app;
