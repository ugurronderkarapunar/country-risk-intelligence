import type { CountryBrief } from "./api";

export function riskBadgeClass(level: string): string {
  switch (level) {
    case "LOW":
      return "bg-emerald-500/15 text-emerald-300 ring-1 ring-emerald-500/30";
    case "MEDIUM":
      return "bg-amber-500/15 text-amber-200 ring-1 ring-amber-500/30";
    case "HIGH":
      return "bg-orange-500/15 text-orange-200 ring-1 ring-orange-500/35";
    case "EXTREME":
      return "bg-rose-600/20 text-rose-200 ring-1 ring-rose-500/40";
    default:
      return "bg-slate-500/15 text-slate-300 ring-1 ring-slate-500/30";
  }
}

export function riskFill(score: number): string {
  if (score < 3) return "#34d399";
  if (score < 5.5) return "#fbbf24";
  if (score < 7.5) return "#fb923c";
  return "#f43f5e";
}

export type MapPoint = CountryBrief & { z: number };

export function toMapPoints(rows: CountryBrief[]): MapPoint[] {
  return rows.map((r) => ({ ...r, z: Math.max(2, r.risk_score * 3) }));
}
