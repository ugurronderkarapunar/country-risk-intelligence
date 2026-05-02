from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.deps import get_current_org, get_current_user, hash_api_key, new_api_key_plain
from app.models import ApiKey, Organization, User
from app.schemas import ApiKeyCreateIn, ApiKeyCreateOut, CorridorIn, DemoTierIn
from app.services.corridor_risk import analyze_corridor
from app.services.tiers import corridor_monthly_limit, normalize_tier, tier_at_least
from app.services.usage import check_and_increment_corridor, reset_month_if_needed

router = APIRouter(prefix="/api", tags=["organization"])


@router.get("/org/usage")
def org_usage(
    org: Annotated[Organization, Depends(get_current_org)],
    session: Session = Depends(get_db),
):
    reset_month_if_needed(org)
    session.add(org)
    session.commit()
    session.refresh(org)
    tier = normalize_tier(org.subscription_tier)
    return {
        "tier": tier,
        "corridor_used_this_month": org.corridor_usage_count,
        "corridor_limit_per_month": corridor_monthly_limit(tier),
        "month": org.corridor_usage_month or None,
        "stripe": {
            "status": "not_connected",
            "message": "Ödeme: Stripe Customer + Checkout entegrasyonu bir sonraki adım.",
        },
    }


@router.post("/org/demo-upgrade")
def demo_upgrade(
    body: DemoTierIn,
    org: Annotated[Organization, Depends(get_current_org)],
    session: Session = Depends(get_db),
    x_demo_secret: Annotated[str | None, Header(alias="X-Demo-Upgrade-Secret")] = None,
):
    if not settings.demo_upgrade_secret or x_demo_secret != settings.demo_upgrade_secret:
        raise HTTPException(status_code=403, detail="Demo plan yükseltme kapalı veya gizli anahtar hatalı")
    org.subscription_tier = body.tier
    session.add(org)
    session.commit()
    return {"ok": True, "subscription_tier": normalize_tier(org.subscription_tier)}


@router.post("/logistics/corridor")
def corridor_analysis(
    body: CorridorIn,
    org: Annotated[Organization, Depends(get_current_org)],
    session: Session = Depends(get_db),
):
    check_and_increment_corridor(session, org)
    return analyze_corridor(session, body.legs)


@router.post("/api-keys", response_model=ApiKeyCreateOut)
def create_api_key(
    body: ApiKeyCreateIn,
    user: Annotated[User, Depends(get_current_user)],
    org: Annotated[Organization, Depends(get_current_org)],
    session: Session = Depends(get_db),
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Yalnızca org yöneticisi API anahtarı oluşturabilir")
    if not tier_at_least(org.subscription_tier, "pro"):
        raise HTTPException(status_code=403, detail="API anahtarı için Pro veya Enterprise plan gerekli")
    plain = new_api_key_plain()
    row = ApiKey(
        org_id=org.id,
        label=body.label.strip(),
        key_prefix=plain[:12],
        key_hash=hash_api_key(plain),
    )
    session.add(row)
    session.commit()
    return ApiKeyCreateOut(api_key=plain, label=row.label, prefix=row.key_prefix)


@router.get("/api-keys")
def list_api_keys(
    user: Annotated[User, Depends(get_current_user)],
    org: Annotated[Organization, Depends(get_current_org)],
    session: Session = Depends(get_db),
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Yalnızca org yöneticisi listeleyebilir")
    rows = session.execute(select(ApiKey).where(ApiKey.org_id == org.id).order_by(ApiKey.id.desc())).scalars().all()
    return [
        {
            "id": r.id,
            "label": r.label,
            "prefix": r.key_prefix,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


@router.delete("/api-keys/{key_id}")
def revoke_api_key(
    key_id: int,
    user: Annotated[User, Depends(get_current_user)],
    org: Annotated[Organization, Depends(get_current_org)],
    session: Session = Depends(get_db),
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Yalnızca org yöneticisi iptal edebilir")
    row = session.get(ApiKey, key_id)
    if not row or row.org_id != org.id:
        raise HTTPException(status_code=404, detail="Anahtar bulunamadı")
    session.delete(row)
    session.commit()
    return {"ok": True}
