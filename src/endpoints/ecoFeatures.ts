import { Bool, Num, OpenAPIRoute, Str } from "chanfana";
import { z } from "zod";
import { type AppContext } from "../types";

const breakdownSchema = z.object({
        area: Str({ example: "transport" }),
        kgCO2e: Num({ example: 12.5 }),
        change: Num({ description: "Percent delta vs prior period", example: -14 }),
});

const leaderboardEntry = z.object({
        name: Str({ example: "You" }),
        score: Num({ example: 82 }),
        rank: Num({ example: 12 }),
        city: Str({ example: "Bengaluru" }),
});

const communityEvent = z.object({
        title: Str({ example: "Beach cleanup" }),
        location: Str({ example: "Marina" }),
        date: Str({ example: "2025-02-18" }),
        spotsLeft: Num({ example: 24 }),
        rsvp: Bool({ example: true }),
});

const badgeSchema = z.object({
        name: Str({ example: "Local Shopper" }),
        description: Str({ example: "72% local purchases" }),
        month: Str({ example: "2025-01" }),
        unlocked: Bool({ example: true }),
});

const reminderSchema = z.object({
        title: Str({ example: "Expiry approaching" }),
        next_trigger_at: Str({ example: "2025-01-08T08:00:00Z" }),
        channel: Str({ example: "push" }),
        actionable: Bool({ example: true }),
});

const recommendationSchema = z.object({
        title: Str({ example: "Switch to refill packs" }),
        savingsKg: Num({ example: 1.1 }),
        partner: Str({ example: "Refill Co" }),
        link: Str({ example: "https://refill.example" }),
});

export class CarbonDashboard extends OpenAPIRoute {
        schema = {
                tags: ["Eco"],
                summary: "Carbon footprint snapshot",
                responses: {
                        "200": {
                                description: "Latest carbon score with breakdowns",
                                content: {
                                        "application/json": {
                                                schema: z.object({
                                                        score: Num({ example: 74 }),
                                                        headline: Str({ example: "Travel footprint decreased by 14% this week" }),
                                                        breakdown: breakdownSchema.array(),
                                                        weeklyTrend: z.array(
                                                                z.object({
                                                                        label: Str({ example: "Week 1" }),
                                                                        kgCO2e: Num({ example: 22.4 }),
                                                                }),
                                                        ),
                                                }),
                                        },
                                },
                        },
                },
        };

        async handle(c: AppContext) {
                return {
                        score: 78,
                        headline: "Travel footprint decreased by 14% this week",
                        breakdown: [
                                { area: "travel", kgCO2e: 8.6, change: -14 },
                                { area: "home_energy", kgCO2e: 12.2, change: -3 },
                                { area: "shopping", kgCO2e: 5.1, change: 4 },
                                { area: "waste", kgCO2e: 2.2, change: -8 },
                        ],
                        weeklyTrend: [
                                { label: "Week 1", kgCO2e: 26.4 },
                                { label: "Week 2", kgCO2e: 24.0 },
                                { label: "Week 3", kgCO2e: 21.3 },
                                { label: "Week 4", kgCO2e: 18.9 },
                        ],
                };
        }
}

export class Leaderboard extends OpenAPIRoute {
        schema = {
                tags: ["Eco"],
                summary: "Leaderboard & rewards",
                request: {
                        query: z.object({
                                city: Str({ required: false, example: "Delhi" }),
                        }),
                },
                responses: {
                        "200": {
                                description: "Leaderboard ranks and tips",
                                content: {
                                        "application/json": {
                                                schema: z.object({
                                                        percentile: Num({ example: 12 }),
                                                        city: Str({ example: "Delhi" }),
                                                        globalRank: Num({ example: 120 }),
                                                        cityRank: Num({ example: 24 }),
                                                        rewards: z.array(Str()),
                                                        leaders: leaderboardEntry.array(),
                                                }),
                                        },
                                },
                        },
                },
        };

        async handle(c: AppContext) {
                const city = (await this.getValidatedData<typeof this.schema>()).query.city ?? "Global";
                return {
                        percentile: 12,
                        city,
                        globalRank: 120,
                        cityRank: 24,
                        rewards: ["Weekly streak bonus", "City top-25% badge"],
                        leaders: [
                                { name: "You", score: 82, rank: 24, city },
                                { name: "Aditi", score: 90, rank: 1, city },
                                { name: "Rahul", score: 86, rank: 2, city },
                        ],
                };
        }
}

export class Community extends OpenAPIRoute {
        schema = {
                tags: ["Eco"],
                summary: "Community groups & events",
                responses: {
                        "200": {
                                description: "Returns EcoCircle data",
                                content: {
                                        "application/json": {
                                                schema: z.object({
                                                        groups: z.array(
                                                                z.object({
                                                                        name: Str({ example: "Campus Green Circle" }),
                                                                        members: Num({ example: 120 }),
                                                                        invitesOpen: Bool({ example: true }),
                                                                }),
                                                        ),
                                                        events: communityEvent.array(),
                                                }),
                                        },
                                },
                        },
                },
        };

        async handle(c: AppContext) {
                return {
                        groups: [
                                { name: "Campus Green Circle", members: 120, invitesOpen: true },
                                { name: "Neighborhood Composters", members: 58, invitesOpen: false },
                        ],
                        events: [
                                { title: "Beach cleanup", location: "Marina", date: "2025-02-18", spotsLeft: 24, rsvp: true },
                                { title: "Clothes swap", location: "Community Hall", date: "2025-02-22", spotsLeft: 12, rsvp: false },
                        ],
                };
        }
}

export class AlertReport extends OpenAPIRoute {
        schema = {
                tags: ["Eco"],
                summary: "Report unusual waste",
                request: {
                        body: {
                                content: {
                                        "application/json": {
                                                schema: z.object({
                                                        description: Str({ example: "Illegal dumping near river" }),
                                                        location: Str({ example: "12.9716,77.5946" }),
                                                        photoUrl: Str({ required: false }),
                                                }),
                                        },
                                },
                        },
                },
                responses: {
                        "201": {
                                description: "Report recorded",
                                content: {
                                        "application/json": {
                                                schema: z.object({
                                                        status: Str({ example: "submitted" }),
                                                        pointsAwarded: Num({ example: 35 }),
                                                        guidance: Str({ example: "We verify within 24h" }),
                                                }),
                                        },
                                },
                        },
                },
        };

        async handle(c: AppContext) {
                return c.json(
                        {
                                status: "submitted",
                                pointsAwarded: 35,
                                guidance: "Verification pending — expect an update within 24h.",
                        },
                        201,
                );
        }
}

export class BadgeList extends OpenAPIRoute {
        schema = {
                tags: ["Eco"],
                summary: "Monthly achievement badges",
                responses: {
                        "200": {
                                description: "Badges and progress",
                                content: {
                                        "application/json": {
                                                schema: z.object({
                                                        badges: badgeSchema.array(),
                                                }),
                                        },
                                },
                        },
                },
        };

        async handle(c: AppContext) {
                return {
                        badges: [
                                { name: "Local Shopper", description: "72% local purchases", month: "2025-01", unlocked: true },
                                { name: "Zero Waste Week", description: "7 days no landfill", month: "2025-01", unlocked: false },
                                { name: "Reuse Hero", description: "5 refill actions", month: "2025-01", unlocked: true },
                        ],
                };
        }
}

export class ReminderList extends OpenAPIRoute {
        schema = {
                tags: ["Eco"],
                summary: "Daily habit reminders",
                responses: {
                        "200": {
                                description: "Scheduled reminders",
                                content: {
                                        "application/json": {
                                                schema: z.object({
                                                        reminders: reminderSchema.array(),
                                                }),
                                        },
                                },
                        },
                },
        };

        async handle(c: AppContext) {
                return {
                        reminders: [
                                { title: "2 items expire in 2 days", next_trigger_at: "2025-01-08T08:00:00Z", channel: "push", actionable: true },
                                { title: "Log your commute for today", next_trigger_at: "2025-01-08T18:00:00Z", channel: "sms", actionable: false },
                        ],
                };
        }
}

export class RecommendationList extends OpenAPIRoute {
        schema = {
                tags: ["Eco"],
                summary: "Eco-friendly product recommendations",
                responses: {
                        "200": {
                                description: "Partner offers and carbon savings",
                                content: {
                                        "application/json": {
                                                schema: z.object({
                                                        recommendations: recommendationSchema.array(),
                                                }),
                                        },
                                },
                        },
                },
        };

        async handle(c: AppContext) {
                return {
                        recommendations: [
                                { title: "Switch to refill packs", savingsKg: 1.1, partner: "Refill Co", link: "https://refill.example" },
                                { title: "Metro over cab for office commute", savingsKg: 2.4, partner: "City Metro", link: "https://metro.example" },
                                { title: "LED upgrade", savingsKg: 0.8, partner: "SolarHome", link: "https://solar.example" },
                        ],
                };
        }
}
