const RTL_LOCALES = new Set(["ar"]);

export function isRtlLocale(lang: string): boolean {
  const code = lang.split("-")[0]?.toLowerCase() ?? "";
  return RTL_LOCALES.has(code);
}
