import { useEffect } from "react";
import { useTranslation } from "react-i18next";

import { isRtlLocale } from "../i18n/rtl";

/** Keeps document lang/dir in sync (Arabic RTL). */
export function I18nDirection() {
  const { i18n } = useTranslation();

  useEffect(() => {
    const code = (i18n.resolvedLanguage ?? i18n.language ?? "en").split("-")[0]!.toLowerCase();
    document.documentElement.lang = code;
    document.documentElement.dir = isRtlLocale(code) ? "rtl" : "ltr";
  }, [i18n.language, i18n.resolvedLanguage]);

  return null;
}
