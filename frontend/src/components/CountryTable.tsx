import { ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import type { CountryBrief } from "../lib/api";
import { riskBadgeClass } from "../lib/riskUi";

export function CountryTable({ rows }: { rows: CountryBrief[] }) {
  const { t } = useTranslation();

  return (
    <div className="overflow-hidden rounded-2xl border border-surface-600/60 bg-surface-800/30">
      <div className="border-b border-surface-600/60 px-4 py-3">
        <h2 className="text-sm font-semibold text-slate-200">{t("table.title")}</h2>
        <p className="text-xs text-slate-500">{t("table.subtitle")}</p>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-surface-900/50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-3 font-medium">{t("table.country")}</th>
              <th className="px-4 py-3 font-medium">{t("table.score")}</th>
              <th className="px-4 py-3 font-medium">{t("table.level")}</th>
              <th className="px-4 py-3 font-medium">{t("table.conflict")}</th>
              <th className="px-4 py-3 font-medium">{t("table.political")}</th>
              <th className="px-4 py-3 font-medium">{t("table.economy")}</th>
              <th className="px-4 py-3 font-medium">{t("table.logistics")}</th>
              <th className="px-4 py-3" />
            </tr>
          </thead>
          <tbody className="divide-y divide-surface-600/40">
            {rows.map((c) => (
              <tr key={c.iso2} className="hover:bg-surface-700/20">
                <td className="px-4 py-3">
                  <div className="font-medium text-slate-100">{c.name_en}</div>
                  <div className="font-mono text-xs text-slate-500">{c.iso2}</div>
                </td>
                <td className="px-4 py-3 font-mono text-slate-200">{c.risk_score.toFixed(2)}</td>
                <td className="px-4 py-3">
                  <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${riskBadgeClass(c.risk_level)}`}>
                    {c.risk_level}
                  </span>
                </td>
                <td className="px-4 py-3 text-slate-300">{c.conflict_effective.toFixed(1)}</td>
                <td className="px-4 py-3 text-slate-300">{c.political_stability.toFixed(1)}</td>
                <td className="px-4 py-3 text-slate-300">{c.economic_risk.toFixed(1)}</td>
                <td className="px-4 py-3 text-slate-300">{c.logistics_friction.toFixed(1)}</td>
                <td className="px-4 py-3 text-right">
                  <Link
                    to={`/country/${c.iso2}`}
                    className="inline-flex items-center gap-1 text-accent-cyan hover:text-cyan-200"
                  >
                    {t("table.detail")}
                    <ChevronRight className="h-4 w-4" />
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
