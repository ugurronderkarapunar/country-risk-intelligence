const base = "";

const TOKEN_KEY = "cri_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string | null): void {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

function authHeaders(): HeadersInit {
  const t = getToken();
  const h: Record<string, string> = {};
  if (t) h.Authorization = `Bearer ${t}`;
  return h;
}

export type CountryBrief = {
  iso2: string;
  name_en: string;
  risk_score: number;
  risk_level: string;
  conflict_effective: number;
  political_stability: number;
  economic_risk: number;
  logistics_friction: number;
  latitude: number;
  longitude: number;
};

export type CountryDetail = CountryBrief & {
  recommendations: string[];
  recent_conflict_headlines: string[];
};

export type ConflictZoneItem = {
  country_iso2: string;
  country_name: string;
  title: string;
  link: string;
  published_at: string | null;
};

export type SyncStatus = {
  last_run_started: string | null;
  last_run_finished: string | null;
  last_status: string | null;
  last_message: string | null;
  items_ingested: number | null;
  next_scheduled_tr: string;
};

export type UserMe = {
  id: number;
  email: string;
  org_id: number;
  org_name: string;
  subscription_tier: string;
  is_admin: boolean;
};

export type PricingTiersResponse = {
  tiers: Array<{
    id: string;
    name: string;
    price_hint_try: string;
    corridor_analyses_per_month: number;
    api_access: boolean;
    features: string[];
  }>;
};

async function j<T>(p: Promise<Response>): Promise<T> {
  const r = await p;
  const text = await r.text();
  if (!r.ok) {
    let msg = text || r.statusText;
    try {
      const data = JSON.parse(text) as { detail?: unknown };
      if (typeof data?.detail === "string") msg = data.detail;
      else if (data?.detail != null) msg = JSON.stringify(data.detail);
    } catch {
      /* use msg */
    }
    throw new Error(msg);
  }
  if (!text) return {} as T;
  return JSON.parse(text) as T;
}

export const api = {
  pricingTiers: () => j<PricingTiersResponse>(fetch(`${base}/api/pricing-tiers`)),

  register: (body: { email: string; password: string; company_name: string }) =>
    j<{ access_token: string }>(
      fetch(`${base}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }),
    ),

  login: (body: { email: string; password: string }) =>
    j<{ access_token: string }>(
      fetch(`${base}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }),
    ),

  me: () => j<UserMe>(fetch(`${base}/auth/me`, { headers: authHeaders() })),

  orgUsage: () =>
    j<{
      tier: string;
      corridor_used_this_month: number;
      corridor_limit_per_month: number;
      month: string | null;
    }>(fetch(`${base}/api/org/usage`, { headers: authHeaders() })),

  corridor: (legs: string[]) =>
    j<Record<string, unknown>>(
      fetch(`${base}/api/logistics/corridor`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ legs }),
      }),
    ),

  countries: () => j<CountryBrief[]>(fetch(`${base}/api/countries`, { headers: authHeaders() })),

  country: (iso2: string) =>
    j<CountryDetail>(fetch(`${base}/api/countries/${iso2}`, { headers: authHeaders() })),

  conflictZones: () =>
    j<ConflictZoneItem[]>(fetch(`${base}/api/conflict-zones?limit=50`, { headers: authHeaders() })),

  syncMeta: () => j<SyncStatus>(fetch(`${base}/api/meta/sync`, { headers: authHeaders() })),

  triggerSync: () =>
    j<{ status: string; message: string | null; items_ingested: number }>(
      fetch(`${base}/api/sync`, { method: "POST", headers: authHeaders() }),
    ),

  createApiKey: (label: string) =>
    j<{ api_key: string; label: string; prefix: string }>(
      fetch(`${base}/api/api-keys`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ label }),
      }),
    ),

  listApiKeys: () =>
    j<Array<{ id: number; label: string; prefix: string; created_at: string | null }>>(
      fetch(`${base}/api/api-keys`, { headers: authHeaders() }),
    ),

  revokeApiKey: (id: number) =>
    j<{ ok: boolean }>(
      fetch(`${base}/api/api-keys/${id}`, { method: "DELETE", headers: authHeaders() }),
    ),
};
