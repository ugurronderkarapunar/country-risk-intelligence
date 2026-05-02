import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Check, Globe2 } from "lucide-react";
import { api, type PricingTiersResponse } from "../lib/api";

export function Landing() {
  const [data, setData] = useState<PricingTiersResponse | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      try {
        setData(await api.pricingTiers());
      } catch (e) {
        setErr(e instanceof Error ? e.message : "Yükleme hatası");
      }
    })();
  }, []);

  return (
    <div className="min-h-screen px-4 py-12 md:px-8">
      <header className="mx-auto flex max-w-5xl flex-col items-center text-center">
        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-400/20 to-violet-500/20 ring-1 ring-cyan-400/25">
          <Globe2 className="h-8 w-8 text-accent-cyan" />
        </div>
        <h1 className="mt-6 text-4xl font-semibold tracking-tight text-white md:text-5xl">
          Lojistik için ülke riski &amp; koridor analizi
        </h1>
        <p className="mt-4 max-w-2xl text-lg text-slate-400">
          Taşıma güzergâhınızdaki ülkeleri tek panelde skorlayın; çatışma sinyalleri ve Türkçe operasyon önerileriyle
          operasyon ve finans ekiplerini hizalayın. <strong className="text-slate-300">SaaS panel</strong> ana gelir
          kanalı; <strong className="text-slate-300">REST API</strong> TMS / WMS entegrasyonu için Pro+.
        </p>
        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link
            to="/register"
            className="inline-flex items-center gap-2 rounded-xl bg-cyan-500 px-5 py-3 text-sm font-semibold text-surface-900 hover:bg-cyan-400"
          >
            Ücretsiz dene
            <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            to="/login"
            className="rounded-xl border border-surface-600 bg-surface-800/50 px-5 py-3 text-sm font-medium text-slate-200 hover:bg-surface-700"
          >
            Giriş
          </Link>
        </div>
      </header>

      {err ? (
        <p className="mx-auto mt-8 max-w-2xl text-center text-sm text-rose-300">{err}</p>
      ) : null}

      <section className="mx-auto mt-16 grid max-w-5xl gap-6 md:grid-cols-3">
        {(data?.tiers ?? []).map((t) => (
          <div
            key={t.id}
            className={`rounded-2xl border p-6 ${
              t.id === "pro"
                ? "border-cyan-500/40 bg-cyan-500/5 shadow-glow"
                : "border-surface-600/60 bg-surface-800/40"
            }`}
          >
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">{t.name}</p>
            <p className="mt-2 text-sm text-slate-300">{t.price_hint_try}</p>
            <ul className="mt-4 space-y-2 text-sm text-slate-400">
              <li className="flex gap-2">
                <Check className="h-4 w-4 shrink-0 text-emerald-400" />
                Aylık koridor analizi: <strong className="text-slate-200">{t.corridor_analyses_per_month}</strong>
              </li>
              <li className="flex gap-2">
                <Check className="h-4 w-4 shrink-0 text-emerald-400" />
                API: {t.api_access ? "Evet (Pro+)" : "Hayır (panel only)"}
              </li>
              {t.features.map((f) => (
                <li key={f} className="flex gap-2">
                  <Check className="h-4 w-4 shrink-0 text-emerald-400" />
                  {f}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </section>

      <footer className="mx-auto mt-20 max-w-3xl text-center text-xs text-slate-500">
        Gelir modeli özeti: <strong className="text-slate-400">Starter</strong> (düşük bilet / deneme) →{" "}
        <strong className="text-slate-400">Pro</strong> (koltuk + API) → <strong className="text-slate-400">Enterprise</strong>{" "}
        (yıllık lisans, SLA). Ayrıntı için repodaki <code className="text-slate-400">docs/IS_MODELI.md</code>.
      </footer>
    </div>
  );
}
