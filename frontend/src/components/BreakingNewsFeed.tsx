import { Newspaper } from "lucide-react";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { api, type BreakingNewsItem } from "../lib/api";
import { localeTagFor } from "../i18n/locale";

export function BreakingNewsFeed() {
  const { t, i18n } = useTranslation();
  const loc = localeTagFor(i18n.language);
  const [items, setItems] = useState<BreakingNewsItem[]>([]);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      try {
        setItems(await api.breakingNews());
      } catch (e) {
        setErr(e instanceof Error ? e.message : t("breaking.loadError"));
      }
    })();
  }, [t]);

  return (
    <div className="flex h-full min-h-[320px] flex-col rounded-2xl border border-surface-600/60 bg-surface-800/30">
      <div className="flex items-center gap-2 border-b border-surface-600/60 px-4 py-3">
        <Newspaper className="h-4 w-4 text-cyan-400" aria-hidden />
        <div>
          <h2 className="text-sm font-semibold text-slate-200">{t("breaking.title")}</h2>
          <p className="text-xs text-slate-500">{t("breaking.subtitle")}</p>
        </div>
      </div>
      <div className="flex-1 space-y-2 overflow-y-auto p-4 pr-2" style={{ maxHeight: 560 }}>
        {err ? <p className="text-sm text-rose-300">{err}</p> : null}
        {!err && items.length === 0 ? (
          <p className="text-sm text-slate-500">{t("breaking.loading")}</p>
        ) : null}
        {items.map((it, i) => (
          <article
            key={`${it.link}-${i}`}
            className="rounded-xl border border-surface-600/50 bg-surface-900/40 p-3 transition hover:border-cyan-500/20"
          >
            <div className="flex items-center justify-between gap-2">
              <span className="rounded-md bg-cyan-500/10 px-2 py-0.5 text-[11px] text-cyan-200">{it.source}</span>
              <span className="text-[11px] text-slate-500">
                {it.published_at ? new Date(it.published_at).toLocaleString(loc) : "—"}
              </span>
            </div>
            <p className="mt-2 line-clamp-3 text-sm text-slate-200">{it.title}</p>
            {it.summary ? <p className="mt-1 line-clamp-2 text-xs text-slate-500">{it.summary}</p> : null}
            <a
              href={it.link}
              target="_blank"
              rel="noreferrer"
              className="mt-2 inline-block text-xs font-medium text-accent-cyan hover:underline"
            >
              {t("breaking.openArticle")}
            </a>
          </article>
        ))}
      </div>
    </div>
  );
}
