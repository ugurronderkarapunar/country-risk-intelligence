/** BCP 47 tag for Date/toLocaleString */
const MAP: Record<string, string> = {
  tr: "tr-TR",
  en: "en-US",
  ar: "ar-SA",
  zh: "zh-CN",
  de: "de-DE",
  fr: "fr-FR",
  es: "es-ES",
  ja: "ja-JP",
};

export function localeTagFor(i18nLanguage: string | undefined): string {
  const code = (i18nLanguage ?? "en").split("-")[0]?.toLowerCase() ?? "en";
  return MAP[code] ?? "en-US";
}
