import { useCallback, useEffect, useState } from "react";
import { api } from "../lib/api";
import { useAuth } from "../context/AuthContext";

export function SettingsPage() {
  const { user } = useAuth();
  const [usage, setUsage] = useState<{
    tier: string;
    corridor_used_this_month: number;
    corridor_limit_per_month: number;
  } | null>(null);
  const [keys, setKeys] = useState<Array<{ id: number; label: string; prefix: string }>>([]);
  const [label, setLabel] = useState("TMS prod");
  const [newKey, setNewKey] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);

  const load = useCallback(async () => {
    setErr(null);
    try {
      const u = await api.orgUsage();
      setUsage({
        tier: u.tier,
        corridor_used_this_month: u.corridor_used_this_month,
        corridor_limit_per_month: u.corridor_limit_per_month,
      });
      if (user?.is_admin) {
        setKeys(await api.listApiKeys());
      } else {
        setKeys([]);
      }
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Yükleme hatası");
    }
  }, [user?.is_admin]);

  useEffect(() => {
    void load();
  }, [load]);

  const tier = user?.subscription_tier ?? "starter";
  const canApi = tier === "pro" || tier === "enterprise";

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 md:px-8">
      <h1 className="text-2xl font-semibold text-white">API &amp; kota</h1>
      <p className="mt-2 text-sm text-slate-400">
        Pro ve Enterprise planlarda REST API ile TMS entegrasyonu. Uçlar:{" "}
        <code className="rounded bg-surface-800 px-1 text-xs">POST /api/v1/corridor</code>,{" "}
        <code className="rounded bg-surface-800 px-1 text-xs">GET /api/v1/countries</code> — başlık:{" "}
        <code className="text-xs">X-API-Key: crik_…</code>
      </p>

      {err ? <p className="mt-4 text-sm text-rose-300">{err}</p> : null}

      {usage ? (
        <div className="mt-6 rounded-2xl border border-surface-600/60 bg-surface-800/40 p-4">
          <p className="text-sm text-slate-400">
            Plan: <span className="text-accent-amber">{usage.tier}</span>
          </p>
          <p className="mt-2 font-mono text-slate-200">
            Koridor analizi bu ay: {usage.corridor_used_this_month} / {usage.corridor_limit_per_month}
          </p>
        </div>
      ) : null}

      <section className="mt-8">
        <h2 className="text-sm font-semibold text-slate-200">API anahtarları</h2>
        {!canApi ? (
          <p className="mt-2 text-sm text-amber-200">
            Starter planda API yok. Müşteriye Pro satışı veya sunucuda demo yükseltme (DEMO_UPGRADE_SECRET) ile test
            edin.
          </p>
        ) : (
          <>
            <div className="mt-3 flex flex-wrap gap-2">
              <input
                value={label}
                onChange={(e) => setLabel(e.target.value)}
                className="rounded-xl border border-surface-600 bg-surface-800 px-3 py-2 text-sm text-slate-100"
              />
              <button
                type="button"
                onClick={async () => {
                  setErr(null);
                  setNewKey(null);
                  try {
                    const r = await api.createApiKey(label);
                    setNewKey(r.api_key);
                    await load();
                  } catch (e) {
                    setErr(e instanceof Error ? e.message : "Oluşturulamadı");
                  }
                }}
                className="rounded-xl bg-violet-500/90 px-4 py-2 text-sm font-medium text-white"
              >
                Yeni anahtar
              </button>
            </div>
            {newKey ? (
              <p className="mt-3 break-all rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-3 font-mono text-xs text-emerald-100">
                Bir kez gösterilir: {newKey}
              </p>
            ) : null}
            <ul className="mt-4 space-y-2">
              {keys.map((k) => (
                <li
                  key={k.id}
                  className="flex items-center justify-between rounded-xl border border-surface-600/50 bg-surface-900/40 px-3 py-2 text-sm"
                >
                  <span>
                    {k.label} — <code className="text-slate-400">{k.prefix}…</code>
                  </span>
                  <button
                    type="button"
                    className="text-rose-300 hover:underline"
                    onClick={async () => {
                      await api.revokeApiKey(k.id);
                      await load();
                    }}
                  >
                    İptal
                  </button>
                </li>
              ))}
            </ul>
          </>
        )}
      </section>
    </div>
  );
}
