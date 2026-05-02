import { useCallback, useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { ConflictFeed } from "../components/ConflictFeed";
import { CountryTable } from "../components/CountryTable";
import { DashboardHeader } from "../components/DashboardHeader";
import { RiskScatter } from "../components/RiskScatter";
import { StatCards } from "../components/StatCards";
import { TopRisksBar } from "../components/TopRisksBar";
import type { ConflictZoneItem, CountryBrief, SyncStatus } from "../lib/api";
import { api } from "../lib/api";

export function Dashboard() {
  const { user } = useAuth();
  const [countries, setCountries] = useState<CountryBrief[]>([]);
  const [zones, setZones] = useState<ConflictZoneItem[]>([]);
  const [sync, setSync] = useState<SyncStatus | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);
  const [syncing, setSyncing] = useState(false);

  const load = useCallback(async () => {
    setErr(null);
    setInfo(null);
    try {
      const [c, z, m] = await Promise.all([api.countries(), api.conflictZones(), api.syncMeta()]);
      setCountries(c);
      setZones(z);
      setSync(m);
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Yükleme hatası");
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const onSync = async () => {
    setSyncing(true);
    setErr(null);
    setInfo(null);
    try {
      const res = await api.triggerSync();
      await load();
      setInfo(
        res.message
          ? `Senkron tamam: ${res.status} — ${res.message}`
          : `Senkron tamam: ${res.status}`,
      );
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Senkron hatası");
    } finally {
      setSyncing(false);
    }
  };

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-8">
      <DashboardHeader onSync={onSync} syncing={syncing} showSync={user?.is_admin ?? false} />

      {err ? (
        <div className="mt-6 rounded-xl border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-sm text-rose-100">
          {err}
        </div>
      ) : null}
      {info ? (
        <div className="mt-6 rounded-xl border border-emerald-500/35 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-100">
          {info}
        </div>
      ) : null}

      <div className="mt-8 space-y-8">
        <StatCards countries={countries} sync={sync} />

        <div className="grid gap-6 lg:grid-cols-3">
          <div className="space-y-6 lg:col-span-2">
            <RiskScatter data={countries} />
            <TopRisksBar data={countries} />
          </div>
          <ConflictFeed items={zones} />
        </div>

        <CountryTable rows={countries} />
      </div>

      <footer className="mt-12 border-t border-surface-600/50 pt-6 text-center text-xs text-slate-500">
        Veriler bilgilendirme amaçlıdır; ticari kararlar için uzman görüşü gereklidir. ReliefWeb RSS ile otomatik akış;
        her gün 12:00 Türkiye saatinde senkron önerilir (sunucu zamanı Europe/Istanbul).
      </footer>
    </div>
  );
}
