import { useTranslation } from "react-i18next";

import { SUPPORTED_LANGS, type AppLang } from "../i18n/config";

const LANG_CODES: AppLang[] = [...SUPPORTED_LANGS];

export function LanguageSwitcher({ className = "" }: { className?: string }) {
  const { t, i18n } = useTranslation();
  const current = (i18n.resolvedLanguage ?? i18n.language ?? "en").split("-")[0]!.toLowerCase();

  return (
    <label className={`inline-flex items-center gap-2 text-sm text-slate-400 ${className}`}>
      <span className="sr-only">{t("lang.label")}</span>
      <select
        value={LANG_CODES.includes(current as AppLang) ? current : "en"}
        onChange={(e) => void i18n.changeLanguage(e.target.value)}
        className="rounded-lg border border-surface-600 bg-surface-800 px-2 py-1.5 text-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-500/40"
        aria-label={t("lang.label")}
      >
        {LANG_CODES.map((code) => (
          <option key={code} value={code}>
            {t(`lang.${code}`)}
          </option>
        ))}
      </select>
    </label>
  );
}
