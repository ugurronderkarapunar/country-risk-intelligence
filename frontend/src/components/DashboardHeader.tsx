import { Globe2, RefreshCw } from "lucide-react";

type Props = {
  onSync: () => void;
  syncing: boolean;
};

export function DashboardHeader({ onSync, syncing }: Props) {
  return (
    <header className="flex flex-col gap-4 border-b border-surface-600/60 pb-6 md:flex-row md:items-center md:justify-between">
      <div className="flex items-start gap-3">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-400/20 to-violet-500/20 ring-1 ring-cyan-400/25">
          <Globe2 className="h-6 w-6 text-accent-cyan" aria-hidden />
        </div>
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-white md:text-3xl">Country Risk Intelligence</h1>
          <p className="mt-1 max-w-2xl text-sm text-slate-400">
            Lojistik ve dış ticaret ekipleri için ülke riski, çatışma sinyalleri ve operasyonel öneriler — tek panelde.
          </p>
        </div>
      </div>
      <button
        type="button"
        onClick={onSync}
        disabled={syncing}
        className="inline-flex items-center justify-center gap-2 rounded-xl bg-surface-700 px-4 py-2.5 text-sm font-medium text-slate-100 ring-1 ring-surface-600 transition hover:bg-surface-600 disabled:opacity-50"
      >
        <RefreshCw className={`h-4 w-4 ${syncing ? "animate-spin" : ""}`} />
        Çatışma akışını şimdi güncelle
      </button>
    </header>
  );
}
