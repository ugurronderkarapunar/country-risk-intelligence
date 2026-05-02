import { useState } from "react";
import type { RecommendationPlaybook } from "../lib/api";
import { api } from "../lib/api";

const PLAYBOOK_TITLES: Record<string, string> = {
  guvenlik: "Güvenlik",
  lojistik_operasyon: "Lojistik",
  gumruk_uyum: "Gümrük & uyum",
  finans_sigorta: "Finans & sigorta",
  kurumsal_sureklilik: "Kurumsal süreklilik",
};

export function CorridorPage() {
  const [raw, setRaw] = useState("DE, PL, UA");
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const run = async () => {
    setErr(null);
    setBusy(true);
    setResult(null);
    try {
      const legs = raw
        .split(/[\s,;]+/)
        .map((s) => s.trim().toUpperCase())
        .filter(Boolean);
      const data = await api.corridor(legs);
      setResult(data);
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Hata");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 md:px-8">
      <h1 className="text-2xl font-semibold text-white">Koridor (rota) analizi</h1>
      <p className="mt-2 text-sm text-slate-400">
        Transit ülkeleri sırayla girin (ISO2, virgül veya boşluk ile). Darboğaz ülke ve birleşik öneriler üretilir.
        Her çalıştırma aylık kotanızdan düşer.
      </p>
      <div className="mt-6 flex flex-col gap-3 md:flex-row md:items-end">
        <div className="flex-1">
          <label className="block text-xs font-medium text-slate-400">Ülke zinciri</label>
          <input
            value={raw}
            onChange={(e) => setRaw(e.target.value)}
            className="mt-1 w-full rounded-xl border border-surface-600 bg-surface-800 px-3 py-2 font-mono text-sm text-slate-100"
            placeholder="ör. TR, BG, RO, HU, DE"
          />
        </div>
        <button
          type="button"
          onClick={() => void run()}
          disabled={busy}
          className="rounded-xl bg-cyan-500 px-5 py-2.5 text-sm font-semibold text-surface-900 disabled:opacity-50"
        >
          {busy ? "Hesaplanıyor…" : "Analiz et"}
        </button>
      </div>
      {err ? <p className="mt-4 text-sm text-rose-300">{err}</p> : null}
      {result?.valid === false ? (
        <p className="mt-4 text-sm text-amber-200">{String(result.message)}</p>
      ) : null}
      {result?.valid === true ? (
        <div className="mt-6 space-y-4 rounded-2xl border border-surface-600/60 bg-surface-800/40 p-4">
          <p className="font-mono text-lg text-white">
            Koridor skoru: {String(result.corridor_risk_score)} ({String(result.corridor_risk_level)})
          </p>
          <p className="text-sm text-slate-300">
            Darboğaz: <strong>{String((result.bottleneck as { name_en?: string })?.name_en)}</strong> (
            {(result.bottleneck as { iso2?: string })?.iso2})
          </p>
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm text-slate-300">
              <thead className="text-xs uppercase text-slate-500">
                <tr>
                  <th className="py-2">Ülke</th>
                  <th className="py-2">Skor</th>
                  <th className="py-2">Seviye</th>
                  <th className="py-2">Lojistik</th>
                </tr>
              </thead>
              <tbody>
                {(result.legs as Array<Record<string, unknown>>).map((row) => (
                  <tr key={String(row.iso2)} className="border-t border-surface-600/40">
                    <td className="py-2">
                      {String(row.name_en)} ({String(row.iso2)})
                    </td>
                    <td className="py-2 font-mono">{String(row.risk_score)}</td>
                    <td className="py-2">{String(row.risk_level)}</td>
                    <td className="py-2">{String(row.logistics_friction)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <ul className="list-disc space-y-2 pl-5 text-sm text-slate-300">
            {(result.recommendations as string[]).map((r) => (
              <li key={r.slice(0, 60)}>{r}</li>
            ))}
          </ul>
          {result.recommendation_playbook &&
          typeof result.recommendation_playbook === "object" &&
          Object.keys(result.recommendation_playbook as object).length > 0 ? (
            <div className="mt-6 border-t border-surface-600/50 pt-4">
              <h3 className="text-sm font-semibold text-slate-200">Playbook (darboğaz ülke bazlı)</h3>
              <div className="mt-3 grid gap-3 md:grid-cols-2">
                {Object.entries(result.recommendation_playbook as RecommendationPlaybook).map(([k, lines]) =>
                  lines?.length ? (
                    <div key={k} className="rounded-lg border border-surface-600/40 bg-surface-900/30 p-3">
                      <p className="text-[11px] font-semibold uppercase text-cyan-300/90">
                        {PLAYBOOK_TITLES[k] ?? k}
                      </p>
                      <ul className="mt-2 list-disc space-y-1 pl-4 text-xs text-slate-300">
                        {lines.map((line) => (
                          <li key={line.slice(0, 72)}>{line}</li>
                        ))}
                      </ul>
                    </div>
                  ) : null,
                )}
              </div>
            </div>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
