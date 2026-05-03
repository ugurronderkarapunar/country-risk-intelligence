import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useTranslation } from "react-i18next";
import type { CountryBrief } from "../lib/api";

export function TopRisksBar({ data }: { data: CountryBrief[] }) {
  const { t } = useTranslation();
  const top = [...data].sort((a, b) => b.risk_score - a.risk_score).slice(0, 8);
  const rows = top.map((c) => ({ name: c.iso2, skor: c.risk_score }));

  return (
    <div className="rounded-2xl border border-surface-600/60 bg-surface-800/30 p-4">
      <h2 className="mb-2 text-sm font-semibold text-slate-200">{t("topRisks.title")}</h2>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={rows} layout="vertical" margin={{ left: 8, right: 16 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#243047" horizontal={false} />
          <XAxis type="number" domain={[0, 10]} stroke="#64748b" tick={{ fill: "#94a3b8", fontSize: 10 }} />
          <YAxis type="category" dataKey="name" width={32} stroke="#64748b" tick={{ fill: "#94a3b8", fontSize: 10 }} />
          <Tooltip
            contentStyle={{ background: "#111822", border: "1px solid #243047", borderRadius: "8px" }}
            labelStyle={{ color: "#e2e8f0" }}
          />
          <Bar dataKey="skor" fill="url(#barGrad)" radius={[0, 6, 6, 0]} />
          <defs>
            <linearGradient id="barGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#22d3ee" stopOpacity={0.2} />
              <stop offset="100%" stopColor="#a78bfa" stopOpacity={0.9} />
            </linearGradient>
          </defs>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
