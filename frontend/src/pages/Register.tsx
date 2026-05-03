import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { api, setToken } from "../lib/api";
import { useAuth } from "../context/AuthContext";
import { LanguageSwitcher } from "../components/LanguageSwitcher";

export function Register() {
  const { t } = useTranslation();
  const nav = useNavigate();
  const { refresh } = useAuth();
  const [company_name, setCompanyName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    setBusy(true);
    try {
      const { access_token } = await api.register({ email, password, company_name });
      setToken(access_token);
      await refresh();
      nav("/dashboard", { replace: true });
    } catch (e2) {
      setErr(e2 instanceof Error ? e2.message : t("register.error"));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-4">
      <div className="mb-6 flex justify-end">
        <LanguageSwitcher />
      </div>
      <h1 className="text-2xl font-semibold text-white">{t("register.title")}</h1>
      <p className="mt-1 text-sm text-slate-500">
        {t("register.haveAccount")}{" "}
        <Link to="/login" className="text-accent-cyan hover:underline">
          {t("register.loginLink")}
        </Link>
      </p>
      <form onSubmit={submit} className="mt-6 space-y-4">
        <div>
          <label className="block text-xs font-medium text-slate-400">{t("register.company")}</label>
          <input
            required
            minLength={2}
            value={company_name}
            onChange={(e) => setCompanyName(e.target.value)}
            className="mt-1 w-full rounded-xl border border-surface-600 bg-surface-800 px-3 py-2 text-slate-100"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-400">{t("register.email")}</label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 w-full rounded-xl border border-surface-600 bg-surface-800 px-3 py-2 text-slate-100"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-400">{t("register.password")}</label>
          <input
            type="password"
            required
            minLength={8}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 w-full rounded-xl border border-surface-600 bg-surface-800 px-3 py-2 text-slate-100"
          />
        </div>
        {err ? <p className="text-sm text-rose-300">{err}</p> : null}
        <button
          type="submit"
          disabled={busy}
          className="w-full rounded-xl bg-cyan-500 py-2.5 text-sm font-semibold text-surface-900 disabled:opacity-50"
        >
          {busy ? t("register.submitBusy") : t("register.submit")}
        </button>
      </form>
      <Link to="/" className="mt-6 text-center text-sm text-slate-500 hover:text-slate-300">
        {t("register.home")}
      </Link>
    </div>
  );
}
