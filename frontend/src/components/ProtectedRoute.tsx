import { Navigate, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuth } from "../context/AuthContext";
import { getToken } from "../lib/api";

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { t } = useTranslation();
  const { loading, user } = useAuth();
  const loc = useLocation();

  if (!getToken()) {
    return <Navigate to="/login" replace state={{ from: loc.pathname }} />;
  }
  if (loading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center text-slate-400">
        {t("protected.verifying")}
      </div>
    );
  }
  if (!user) {
    return <Navigate to="/login" replace state={{ from: loc.pathname }} />;
  }
  return <>{children}</>;
}
