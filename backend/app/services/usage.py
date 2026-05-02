from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Organization
from app.services.tiers import corridor_monthly_limit, normalize_tier


def reset_month_if_needed(org: Organization) -> None:
    ym = datetime.now(UTC).strftime("%Y-%m")
    if org.corridor_usage_month != ym:
        org.corridor_usage_month = ym
        org.corridor_usage_count = 0


def check_and_increment_corridor(session: Session, org: Organization) -> tuple[int, int]:
    """Koridor kotasını kontrol eder, geçerse sayacı artırır. (used, limit) döner."""
    reset_month_if_needed(org)
    tier = normalize_tier(org.subscription_tier)
    limit = corridor_monthly_limit(tier)
    if org.corridor_usage_count >= limit:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "corridor_quota_exceeded",
                "message": "Aylık koridor analizi limitine ulaşıldı. Plan yükseltin.",
                "used": org.corridor_usage_count,
                "limit": limit,
                "tier": tier,
            },
        )
    org.corridor_usage_count += 1
    session.add(org)
    session.commit()
    session.refresh(org)
    return org.corridor_usage_count, limit
