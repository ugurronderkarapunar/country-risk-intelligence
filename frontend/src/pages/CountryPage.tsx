import { ArrowLeft } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import type { CountryDetail } from "../lib/api";
import { api } from "../lib/api";
import { riskBadgeClass } from "../lib/riskUi";

export function CountryPage() {
  const { iso2 } = useParams();
  const [data, setData] = useState<CountryDetail | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    if (!iso2) return;
    void (async () => {
      setErr(null);
      try {
        setData(await api.country(iso2));
      } catch (e) {
        setErr(e instanceof Error ? e.message : "Hata");
      }
    })();
  }, [iso2]);

  if (err) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16">
        <Link to="/dashboard" className="text-accent-cyan hover:underline">
          ← Panele dön
        </Link>
        <p className="mt-6 text-rose-200">{err}</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16 text-slate-400">
        <Link to="/dashboard" className="inline-flex items-center gap-2 text-accent-cyan hover:underline">
          <ArrowLeft className="h-4 w-4" />
          Panele dön
        </Link>
        <p className="mt-8">Yükleniyor…</p>
      </div>
    );
  }

  const politicalRisk = Math.max(0, 10 - data.political_stability);
  const radarRows = [
    { boyut: "Çatışma", deger: data.conflict_effective },
    { boyut: "Politik risk", deger: politicalRisk },
    { boyut: "Ekonomi", deger: data.economic_risk },
    { boyut: "Lojistik", deger: data.logistics_friction },
  ];

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 md:px-8">
      <Link to="/dashboard" className="inline-flex items-center gap-2 text-sm text-accent-cyan hover:underline">
        <ArrowLeft className="h-4 w-4" />
        Panele dön
      </Link>

      <div className="mt-6 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 className="text-3xl font-semibold text-white">{data.name_en}</h1>
          <p className="mt-1 font-mono text-slate-400">{data.iso2}</p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <span className="font-mono text-3xl font-semibold text-white">{data.risk_score.toFixed(2)}</span>
          <span className={`rounded-full px-3 py-1 text-sm font-medium ${riskBadgeClass(data.risk_level)}`}>
            {data.risk_level}
          </span>
        </div>
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-surface-600/60 bg-surface-800/30 p-4">
          <h2 className="text-sm font-semibold text-slate-200">Risk bileşenleri</h2>
          <ResponsiveContainer width="100%" height={320}>
            <RadarChart data={radarRows} cx="50%" cy="50%" outerRadius="75%">
              <PolarGrid stroke="#243047" />
              <PolarAngleAxis dataKey="boyut" tick={{ fill: "#94a3b8", fontSize: 11 }} />
              <Radar name="Skor" dataKey="deger" stroke="#22d3ee" fill="#22d3ee" fillOpacity={0.25} />
              <Tooltip
                contentStyle={{ background: "#111822", border: "1px solid #243047", borderRadius: "8px" }}
                labelStyle={{ color: "#e2e8f0" }}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        <div className="space-y-4 rounded-2xl border border-surface-600/60 bg-surface-800/30 p-4">
          <h2 className="text-sm font-semibold text-slate-200">Lojistik &amp; ticaret önerileri</h2>
          <ul className="space-y-3">
            {data.recommendations.map((r) => (
              <li key={r.slice(0, 48)} className="rounded-xl border border-surface-600/50 bg-surface-900/40 p-3 text-sm text-slate-200">
                {r}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="mt-6 rounded-2xl border border-surface-600/60 bg-surface-800/30 p-4">
        <h2 className="text-sm font-semibold text-slate-200">Son çatışma / kriz başlıkları</h2>
        {data.recent_conflict_headlines.length === 0 ? (
          <p className="mt-2 text-sm text-slate-500">Bu ülke için eşleşen başlık yok.</p>
        ) : (
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-slate-300">
            {data.recent_conflict_headlines.map((h) => (
              <li key={h}>{h}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
