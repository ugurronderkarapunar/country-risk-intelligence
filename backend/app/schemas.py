from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class CountryBrief(BaseModel):
    iso2: str
    name_en: str
    risk_score: float
    risk_level: str
    conflict_effective: float
    political_stability: float
    economic_risk: float
    logistics_friction: float
    latitude: float
    longitude: float


class CountryDetail(CountryBrief):
    recommendations: list[str]
    recent_conflict_headlines: list[str] = Field(default_factory=list)


class ConflictZoneItem(BaseModel):
    country_iso2: str
    country_name: str
    title: str
    link: str
    published_at: datetime | None


class SyncStatus(BaseModel):
    last_run_started: datetime | None
    last_run_finished: datetime | None
    last_status: str | None
    last_message: str | None
    items_ingested: int | None
    next_scheduled_tr: str = "Her gün 12:00 Türkiye saati (Europe/Istanbul)"


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    company_name: str = Field(min_length=2, max_length=256)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str
    org_id: int
    org_name: str
    subscription_tier: str
    is_admin: bool


class CorridorIn(BaseModel):
    legs: list[str] = Field(..., min_length=2, description="ISO2 ülke kodları sırasıyla, örn. [\"DE\",\"PL\",\"UA\"]")


class DemoTierIn(BaseModel):
    tier: Literal["starter", "pro", "enterprise"]


class ApiKeyCreateIn(BaseModel):
    label: str = Field(min_length=1, max_length=128)


class ApiKeyCreateOut(BaseModel):
    api_key: str
    label: str
    prefix: str
    message: str = "Bu anahtarı yalnızca bir kez gösteriyoruz; güvenli saklayın."
