import { ExternalLink, Radio } from "lucide-react";
import { useTranslation } from "react-i18next";
import type { ConflictZoneItem } from "../lib/api";
import { localeTagFor } from "../i18n/locale";

export function ConflictFeed({ items }: { items: ConflictZoneItem[] }) {
  const { t, i18n } = useTranslation();
  const loc = localeTagFor(i18n.language);

  return (
    <div className="flex h-full min-h-[320px] flex-col rounded-2xl border border-surface-600/60 bg-surface-800/30">
      <div className="flex items-center gap-2 border-b border-surface-600/60 px-4 py-3">
        <Radio className="h-4 w-4 text-accent-violet" aria-hidden />
        <div>
          <h2 className="text-sm font-semibold text-slate-200">{t("conflict.title")}</h2>
          <p className="text-xs text-slate-500">{t("conflict.subtitle")}</p>
        </div>
      </div>
      <div className="flex-1 space-y-3 overflow-y-auto p-4 pr-2" style={{ maxHeight: 560 }}>
        {items.length === 0 ? (
          <p className="text-sm text-slate-500">{t("conflict.empty")}</p>
        ) : (
          items.map((it, i) => (
            <article
              key={`${it.link}-${i}`}
              className="rounded-xl border border-surface-600/50 bg-surface-900/40 p-3 transition hover:border-cyan-500/25"
            >
              <div className="flex items-center justify-between gap-2">
                <span className="rounded-md bg-violet-500/10 px-2 py-0.5 font-mono text-[11px] text-violet-200">
                  {it.country_iso2}
                </span>
                <span className="text-[11px] text-slate-500">
                  {it.published_at ? new Date(it.published_at).toLocaleDateString(loc) : "—"}
                </span>
              </div>
              <p className="mt-2 line-clamp-3 text-sm text-slate-200">{it.title}</p>
              <a
                href={it.link}
                target="_blank"
                rel="noreferrer"
                className="mt-2 inline-flex items-center gap-1 text-xs font-medium text-accent-cyan hover:underline"
              >
                {t("conflict.openSource")}
                <ExternalLink className="h-3 w-3" />
              </a>
            </article>
          ))
        )}
      </div>
    </div>
  );
}
