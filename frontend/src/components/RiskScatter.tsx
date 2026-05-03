import {
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from "recharts";
import { useTranslation } from "react-i18next";
import type { CountryBrief } from "../lib/api";
import { riskFill } from "../lib/riskUi";

type Pt = CountryBrief & { z: number };

function Tip({ active, payload }: { active?: boolean; payload?: Array<{ payload: Pt }> }) {
  const { t } = useTranslation();
  if (!active || !payload?.length) return null;
  const p = payload[0].payload;
  return (
    <div className="rounded-lg border border-surface-600 bg-surface-800/95 px-3 py-2 text-sm shadow-xl backdrop-blur">
      <div className="font-semibold text-white">{p.name_en}</div>
      <div className="text-slate-400">
        {p.iso2} · {t("scatter.tooltipScore")} {p.risk_score} · {p.risk_level}
      </div>
    </div>
  );
}

export function RiskScatter({ data }: { data: CountryBrief[] }) {
  const { t } = useTranslation();
  const pts: Pt[] = data.map((d) => ({
    ...d,
    z: 40 + d.risk_score * 90,
  }));

  return (
    <div className="rounded-2xl border border-surface-600/60 bg-surface-800/30 p-4">
      <div className="mb-2 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-slate-200">{t("scatter.title")}</h2>
        <span className="text-xs text-slate-500">{t("scatter.bubbleHint")}</span>
      </div>
      <ResponsiveContainer width="100%" height={340}>
        <ScatterChart margin={{ top: 8, right: 8, bottom: 8, left: 8 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#243047" />
          <XAxis
            type="number"
            dataKey="longitude"
            domain={[-180, 180]}
            stroke="#64748b"
            tick={{ fill: "#94a3b8", fontSize: 10 }}
          />
          <YAxis
            type="number"
            dataKey="latitude"
            domain={[-55, 72]}
            stroke="#64748b"
            tick={{ fill: "#94a3b8", fontSize: 10 }}
          />
          <ZAxis type="number" dataKey="z" range={[70, 420]} />
          <Tooltip content={<Tip />} cursor={{ strokeDasharray: "3 3" }} />
          <Scatter data={pts} fill="#22d3ee">
            {pts.map((e, i) => (
              <Cell key={`${e.iso2}-${i}`} fill={riskFill(e.risk_score)} stroke="#0b0f14" strokeWidth={0.5} />
            ))}
          </Scatter>
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
