from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from app.config import settings


def create_access_token(*, subject: str, user_id: int, org_id: int) -> str:
    """exp Unix zaman damgası (int) — tüm python-jose sürümleriyle uyumlu."""
    expire = datetime.now(UTC) + timedelta(minutes=settings.jwt_expire_minutes)
    exp_ts = int(expire.timestamp())
    payload = {"sub": subject, "uid": user_id, "oid": org_id, "exp": exp_ts}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])


def safe_decode(token: str) -> dict | None:
    try:
        return decode_token(token)
    except JWTError:
        return None
