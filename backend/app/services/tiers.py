from __future__ import annotations

TIER_RANK: dict[str, int] = {"starter": 0, "pro": 1, "enterprise": 2}

# Aylık koridor analizi (rota ülke zinciri) üst sınırı
CORRIDOR_MONTHLY_LIMIT: dict[str, int] = {
    "starter": 40,
    "pro": 2500,
    "enterprise": 999_999,
}


def normalize_tier(tier: str | None) -> str:
    t = (tier or "starter").lower().strip()
    return t if t in TIER_RANK else "starter"


def tier_at_least(current: str, minimum: str) -> bool:
    return TIER_RANK.get(normalize_tier(current), 0) >= TIER_RANK.get(normalize_tier(minimum), 0)


def corridor_monthly_limit(tier: str) -> int:
    return CORRIDOR_MONTHLY_LIMIT.get(normalize_tier(tier), CORRIDOR_MONTHLY_LIMIT["starter"])
