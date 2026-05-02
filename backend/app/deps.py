from __future__ import annotations

import hashlib
import secrets
from typing import Annotated

from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ApiKey, Organization, User
from app.services.auth_tokens import safe_decode
from app.services.tiers import normalize_tier, tier_at_least

_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    session: Annotated[Session, Depends(get_db)],
    cred: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> User:
    if cred is None or cred.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Oturum gerekli: Authorization: Bearer <token>")
    payload = safe_decode(cred.credentials)
    if not payload or "uid" not in payload:
        raise HTTPException(status_code=401, detail="Geçersiz veya süresi dolmuş token")
    uid = int(payload["uid"])
    user = session.get(User, uid)
    if not user:
        raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")
    return user


def get_current_org(
    session: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Organization:
    org = session.get(Organization, user.org_id)
    if not org:
        raise HTTPException(status_code=400, detail="Organizasyon bulunamadı")
    return org


def get_org_from_api_key(
    session: Annotated[Session, Depends(get_db)],
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> Organization:
    if not x_api_key or not x_api_key.strip():
        raise HTTPException(status_code=401, detail="X-API-Key başlığı gerekli")
    raw = x_api_key.strip()
    h = hashlib.sha256(raw.encode()).hexdigest()
    row = session.execute(select(ApiKey).where(ApiKey.key_hash == h)).scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=401, detail="Geçersiz API anahtarı")
    org = session.get(Organization, row.org_id)
    if not org:
        raise HTTPException(status_code=401, detail="Organizasyon bulunamadı")
    if not tier_at_least(org.subscription_tier, "pro"):
        raise HTTPException(status_code=403, detail="API erişimi için Pro veya Enterprise plan gerekli")
    return org


def new_api_key_plain() -> str:
    return f"crik_{secrets.token_urlsafe(32)}"


def hash_api_key(plain: str) -> str:
    return hashlib.sha256(plain.encode()).hexdigest()
