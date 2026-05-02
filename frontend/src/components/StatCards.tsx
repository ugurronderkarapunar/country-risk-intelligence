import { AlertTriangle, BarChart3, Clock } from "lucide-react";
import type { CountryBrief } from "../lib/api";
import type { SyncStatus } from "../lib/api";

type Props = {
  countries: CountryBrief[];
  sync: SyncStatus | null;
};

export function StatCards({ countries, sync }: Props) {
  const avg = countries.length ? countries.reduce((a, c) => a + c.risk_score, 0) / countries.length : 0;
  const high = countries.filter((c) => c.risk_level === "HIGH" || c.risk_level === "EXTREME").length;
  const last = sync?.last_run_finished ? new Date(sync.last_run_finished).toLocaleString("tr-TR") : "—";

  const items = [
    {
      label: "Ortalama risk skoru",
      value: avg.toFixed(2),
      sub: "0–10 bileşik gösterge",
      icon: BarChart3,
    },
    {
      label: "Yüksek / ekstrem ülke",
      value: String(high),
      sub: `${countries.length} ülke içinde`,
      icon: AlertTriangle,
    },
    {
      label: "Son çatışma senkronu",
      value: last,
      sub: sync?.next_scheduled_tr ?? "",
      icon: Clock,
    },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-3">
      {items.map((it) => (
        <div
          key={it.label}
          className="rounded-2xl border border-surface-600/60 bg-surface-800/40 p-4 shadow-glow backdrop-blur"
        >
          <div className="flex items-center justify-between gap-2">
            <p className="text-xs font-medium uppercase tracking-wider text-slate-500">{it.label}</p>
            <it.icon className="h-4 w-4 text-accent-cyan/80" aria-hidden />
          </div>
          <p className="mt-2 font-mono text-2xl font-semibold text-white">{it.value}</p>
          <p className="mt-1 text-xs text-slate-500">{it.sub}</p>
        </div>
      ))}
    </div>
  );
}
