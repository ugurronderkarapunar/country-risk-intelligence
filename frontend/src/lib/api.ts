const base = "";

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

async function j<T>(r: Response): Promise<T> {
  if (!r.ok) {
    const t = await r.text();
    throw new Error(t || r.statusText);
  }
  return r.json() as Promise<T>;
}

export const api = {
  countries: () => j<CountryBrief[]>(fetch(`${base}/api/countries`)),
  country: (iso2: string) => j<CountryDetail>(fetch(`${base}/api/countries/${iso2}`)),
  conflictZones: () => j<ConflictZoneItem[]>(fetch(`${base}/api/conflict-zones?limit=50`)),
  syncMeta: () => j<SyncStatus>(fetch(`${base}/api/meta/sync`)),
  triggerSync: () =>
    j<{ status: string; message: string | null; items_ingested: number }>(
      fetch(`${base}/api/sync`, { method: "POST" }),
    ),
};
