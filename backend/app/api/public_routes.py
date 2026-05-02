from fastapi import APIRouter

from app.services.tiers import CORRIDOR_MONTHLY_LIMIT, TIER_RANK

router = APIRouter(prefix="/api", tags=["public"])


@router.get("/health")
def health():
    return {"status": "ok", "service": "country-risk-intelligence"}


@router.get("/pricing-tiers")
def pricing_tiers():
    """Arayüz / satış sayfası için limit özeti (kimlik gerektirmez)."""
    return {
        "tiers": [
            {
                "id": "starter",
                "name": "Starter",
                "price_hint_try": "Ücretsiz deneme / düşük sabit ücret",
                "corridor_analyses_per_month": CORRIDOR_MONTHLY_LIMIT["starter"],
                "api_access": False,
                "features": [
                    "Ülke ve koridor risk paneli",
                    "ReliefWeb çatışma akışı",
                    "Türkçe operasyonel öneriler",
                ],
            },
            {
                "id": "pro",
                "name": "Pro",
                "price_hint_try": "Koltuk başı aylık (ör. 2.500–8.000 ₺ aralığı — siz belirlersiniz)",
                "corridor_analyses_per_month": CORRIDOR_MONTHLY_LIMIT["pro"],
                "api_access": True,
                "features": [
                    "Tüm Starter özellikleri",
                    "REST API + API anahtarı (TMS entegrasyonu)",
                    "Yüksek koridor analiz kotası",
                ],
            },
            {
                "id": "enterprise",
                "name": "Enterprise",
                "price_hint_try": "Yıllık lisans + SLA",
                "corridor_analyses_per_month": CORRIDOR_MONTHLY_LIMIT["enterprise"],
                "api_access": True,
                "features": [
                    "Özel veri kaynakları ve raporlama",
                    "SOC2 / sözleşme uyumu için ayrı koşullar",
                    "Öncelikli destek",
                ],
            },
        ],
        "tier_order": list(TIER_RANK.keys()),
    }
