from datetime import datetime

from pydantic import BaseModel, Field


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
