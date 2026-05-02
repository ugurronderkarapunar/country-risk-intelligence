import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Organization, User
from app.schemas import LoginIn, RegisterIn, TokenOut, UserOut
from app.services.auth_tokens import create_access_token
from app.services.passwords import hash_password, verify_password
from app.services.tiers import normalize_tier

log = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenOut)
def register(body: RegisterIn, session: Session = Depends(get_db)):
    try:
        email_norm = str(body.email).lower().strip()
        exists = session.execute(select(User).where(User.email == email_norm)).scalar_one_or_none()
        if exists:
            raise HTTPException(status_code=409, detail="Bu e-posta zaten kayıtlı")
        org = Organization(name=body.company_name.strip(), subscription_tier="starter")
        session.add(org)
        session.flush()
        user = User(
            email=email_norm,
            hashed_password=hash_password(body.password),
            org_id=org.id,
            is_admin=True,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        token = create_access_token(subject=user.email, user_id=user.id, org_id=user.org_id)
        return TokenOut(access_token=token)
    except HTTPException:
        session.rollback()
        raise
    except IntegrityError as e:
        session.rollback()
        log.warning("register integrity: %s", e)
        raise HTTPException(status_code=409, detail="Kayıt çakışması — e-posta veya veri tekrarını kontrol edin.") from e
    except Exception as e:
        session.rollback()
        log.exception("register failed")
        raise HTTPException(
            status_code=500,
            detail="Kayıt tamamlanamadı. Şifre en az 8 karakter olmalı; sorun sürerse daha sonra deneyin.",
        ) from e


@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, session: Session = Depends(get_db)):
    user = session.execute(select(User).where(User.email == str(body.email).lower().strip())).scalar_one_or_none()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="E-posta veya şifre hatalı")
    token = create_access_token(subject=user.email, user_id=user.id, org_id=user.org_id)
    return TokenOut(access_token=token)


@router.get("/me", response_model=UserOut)
def me(user: Annotated[User, Depends(get_current_user)], session: Session = Depends(get_db)):
    org = session.get(Organization, user.org_id)
    if not org:
        raise HTTPException(status_code=400, detail="Organizasyon yok")
    return UserOut(
        id=user.id,
        email=user.email,
        org_id=user.org_id,
        org_name=org.name,
        subscription_tier=normalize_tier(org.subscription_tier),
        is_admin=user.is_admin,
    )
