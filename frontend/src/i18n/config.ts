import i18n from "i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import { initReactI18next } from "react-i18next";

import ar from "./locales/ar.json";
import de from "./locales/de.json";
import en from "./locales/en.json";
import es from "./locales/es.json";
import fr from "./locales/fr.json";
import ja from "./locales/ja.json";
import tr from "./locales/tr.json";
import zh from "./locales/zh.json";

export const SUPPORTED_LANGS = ["tr", "en", "ar", "zh", "de", "fr", "es", "ja"] as const;
export type AppLang = (typeof SUPPORTED_LANGS)[number];

void i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      tr: { translation: tr },
      en: { translation: en },
      ar: { translation: ar },
      zh: { translation: zh },
      de: { translation: de },
      fr: { translation: fr },
      es: { translation: es },
      ja: { translation: ja },
    },
    fallbackLng: "en",
    supportedLngs: [...SUPPORTED_LANGS],
    interpolation: { escapeValue: false },
    detection: {
      order: ["localStorage", "navigator"],
      caches: ["localStorage"],
      lookupLocalStorage: "cri_lang",
    },
  });

export default i18n;
