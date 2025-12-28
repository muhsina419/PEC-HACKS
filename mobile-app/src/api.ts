import Constants from 'expo-constants';

export type AuthResponse = { token: string; user: { id: number; phone_number: string; name?: string; city?: string; avatar_url?: string } };
export type CarbonSnapshot = { eco_score: number; total_emissions: number; breakdown: Record<string, number>; tips?: string[] };
export type LeaderboardEntry = { rank: number; name: string; city: string; eco_score: number; headline: string };
export type Circle = { id: number; name: string; city: string; members: number; upcoming_events?: string[] };
export type Alert = { id: number; title: string; status: string; reward: number };
export type Badge = { id: number; title: string; description: string; awarded_at: string };
export type Reminder = { id: number; title: string; next_trigger_at: string };
export type Recommendation = { id: number; title: string; savings: string; partner?: string };

const API_URL = Constants.expoConfig?.extra?.apiUrl || process.env.EXPO_PUBLIC_API_URL || 'https://api.ecosphere.local';

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });
  if (!res.ok) {
    const message = await res.text();
    throw new Error(message || `Request failed: ${res.status}`);
  }
  return res.json();
}

export async function login(phone_number: string, password: string): Promise<AuthResponse> {
  return request<AuthResponse>('/api/auth/login/', { method: 'POST', body: JSON.stringify({ phone_number, password }) });
}

export async function register(phone_number: string, password: string, name?: string): Promise<AuthResponse> {
  return request<AuthResponse>('/api/auth/register/', { method: 'POST', body: JSON.stringify({ phone_number, password, name }) });
}

export async function getProfile(token: string) {
  return request<AuthResponse>('/api/auth/profile/', { headers: { Authorization: `Bearer ${token}` } });
}

export async function updateProfile(token: string, payload: Partial<{ name: string; city: string; avatar_url: string }>) {
  return request<AuthResponse>('/api/auth/profile/', { method: 'PATCH', body: JSON.stringify(payload), headers: { Authorization: `Bearer ${token}` } });
}

export async function getCarbonSnapshot(token: string) {
  return request<CarbonSnapshot>('/api/dashboard/carbon/', { headers: { Authorization: `Bearer ${token}` } });
}

export async function getLeaderboard(token: string) {
  return request<{ global: LeaderboardEntry[]; city: LeaderboardEntry[] }>('/api/engagement/rank/', { headers: { Authorization: `Bearer ${token}` } });
}

export async function getCircles(token: string) {
  return request<{ circles: Circle[] }>('/api/engagement/circles/', { headers: { Authorization: `Bearer ${token}` } });
}

export async function getAlerts(token: string) {
  return request<{ alerts: Alert[] }>('/api/engagement/alerts/', { headers: { Authorization: `Bearer ${token}` } });
}

export async function submitAlert(token: string, title: string, photo_url?: string) {
  return request<Alert>('/api/engagement/alerts/', { method: 'POST', body: JSON.stringify({ title, photo_url }), headers: { Authorization: `Bearer ${token}` } });
}

export async function getBadges(token: string) {
  return request<{ badges: Badge[] }>('/api/engagement/badges/', { headers: { Authorization: `Bearer ${token}` } });
}

export async function getReminders(token: string) {
  return request<{ reminders: Reminder[] }>('/api/engagement/reminders/', { headers: { Authorization: `Bearer ${token}` } });
}

export async function getRecommendations(token: string) {
  return request<{ recommendations: Recommendation[] }>('/api/engagement/shop/', { headers: { Authorization: `Bearer ${token}` } });
}

export function formatDate(value: string) {
  return new Date(value).toLocaleDateString();
}
