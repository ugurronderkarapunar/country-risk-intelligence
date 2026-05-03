import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useAuth } from "../context/AuthContext";
import { BreakingNewsFeed } from "../components/BreakingNewsFeed";
import { ConflictFeed } from "../components/ConflictFeed";
import { CountryTable } from "../components/CountryTable";
import { DashboardHeader } from "../components/DashboardHeader";
import { RiskScatter } from "../components/RiskScatter";
import { StatCards } from "../components/StatCards";
import { TopRisksBar } from "../components/TopRisksBar";
import type { ConflictZoneItem, CountryBrief, SyncStatus } from "../lib/api";
import { api } from "../lib/api";

export function Dashboard() {
  const { t } = useTranslation();
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
      setErr(e instanceof Error ? e.message : t("dashboard.loadError"));
    }
  }, [t]);

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
          ? t("dashboard.syncOkWithMsg", { status: res.status, message: res.message })
          : t("dashboard.syncOk", { status: res.status }),
      );
    } catch (e) {
      setErr(e instanceof Error ? e.message : t("dashboard.syncError"));
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

        <div className="grid gap-6 lg:grid-cols-4">
          <div className="space-y-6 lg:col-span-2">
            <RiskScatter data={countries} />
            <TopRisksBar data={countries} />
          </div>
          <ConflictFeed items={zones} />
          <BreakingNewsFeed />
        </div>

        <CountryTable rows={countries} />
      </div>

      <footer className="mt-12 border-t border-surface-600/50 pt-6 text-center text-xs text-slate-500">
        {t("dashboard.footer")}
      </footer>
    </div>
  );
}
