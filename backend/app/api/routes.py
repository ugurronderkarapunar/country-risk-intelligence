from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, nulls_last, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import ConflictEvent, Country, SyncRun, User
from app.schemas import BreakingNewsOut, ConflictZoneItem, CountryBrief, CountryDetail, SyncStatus
from app.services.conflict_sync import event_counts_last_days, run_conflict_sync
from app.services.breaking_news import list_breaking_news
from app.services.recommendations import trade_logistics_recommendations
from app.services.recommendations_playbook import build_playbook, playbook_to_flat_summary
from app.services.risk import conflict_boost_from_events, effective_conflict, risk_level, risk_score

router = APIRouter(prefix="/api", dependencies=[Depends(get_current_user)])


def _country_brief_list(session: Session) -> list[CountryBrief]:
    counts = event_counts_last_days(session, 14)
    countries = session.execute(select(Country).order_by(Country.name_en)).scalars().all()
    out: list[CountryBrief] = []
    for c in countries:
        boost = conflict_boost_from_events(counts.get(c.iso2, 0))
        ce = effective_conflict(c.conflict_base, boost)
        rs = risk_score(ce, c.political_stability, c.economic_risk, c.logistics_friction)
        out.append(
            CountryBrief(
                iso2=c.iso2,
                name_en=c.name_en,
                risk_score=rs,
                risk_level=risk_level(rs),
                conflict_effective=ce,
                political_stability=c.political_stability,
                economic_risk=c.economic_risk,
                logistics_friction=c.logistics_friction,
                latitude=c.latitude,
                longitude=c.longitude,
            )
        )
    out.sort(key=lambda x: x.risk_score, reverse=True)
    return out


@router.get("/countries", response_model=list[CountryBrief])
def list_countries(session: Session = Depends(get_db)):
    return _country_brief_list(session)


@router.get("/countries/{iso2}", response_model=CountryDetail)
def country_detail(iso2: str, session: Session = Depends(get_db)):
    iso2 = iso2.upper()
    c = session.get(Country, iso2)
    if not c:
        raise HTTPException(status_code=404, detail="Country not found")
    counts = event_counts_last_days(session, 14)
    boost = conflict_boost_from_events(counts.get(c.iso2, 0))
    ce = effective_conflict(c.conflict_base, boost)
    rs = risk_score(ce, c.political_stability, c.economic_risk, c.logistics_friction)
    lvl = risk_level(rs)
    headlines_q = (
        select(ConflictEvent.title)
        .where(ConflictEvent.country_iso2 == iso2)
        .order_by(nulls_last(desc(ConflictEvent.published_at)), desc(ConflictEvent.id))
        .limit(8)
    )
    headlines = [row[0] for row in session.execute(headlines_q).all()]
    hc = counts.get(c.iso2, 0)
    playbook = build_playbook(
        iso2=c.iso2,
        name_en=c.name_en,
        risk_level=lvl,
        conflict_effective=ce,
        political_stability=c.political_stability,
        economic_risk=c.economic_risk,
        logistics_friction=c.logistics_friction,
        recent_headline_count=hc,
    )
    base_recs = trade_logistics_recommendations(
        risk_level=lvl,
        conflict_effective=ce,
        political_stability=c.political_stability,
        economic_risk=c.economic_risk,
        logistics_friction=c.logistics_friction,
    )
    merged = list(dict.fromkeys([*base_recs, *playbook_to_flat_summary(playbook)]))
    return CountryDetail(
        iso2=c.iso2,
        name_en=c.name_en,
        risk_score=rs,
        risk_level=lvl,
        conflict_effective=ce,
        political_stability=c.political_stability,
        economic_risk=c.economic_risk,
        logistics_friction=c.logistics_friction,
        latitude=c.latitude,
        longitude=c.longitude,
        recommendations=merged,
        recommendation_playbook=playbook,
        recent_conflict_headlines=headlines,
    )


@router.get("/news/breaking", response_model=list[BreakingNewsOut])
def breaking_news(session: Session = Depends(get_db), limit: int = 35):
    rows = list_breaking_news(session, limit=limit)
    return [
        BreakingNewsOut(
            source=r.source,
            title=r.title,
            link=r.link,
            summary=r.summary,
            published_at=r.published_at,
        )
        for r in rows
    ]


@router.get("/conflict-zones", response_model=list[ConflictZoneItem])
def conflict_zones(session: Session = Depends(get_db), limit: int = 40):
    q = (
        select(ConflictEvent, Country.name_en)
        .join(Country, Country.iso2 == ConflictEvent.country_iso2)
        .order_by(nulls_last(desc(ConflictEvent.published_at)), desc(ConflictEvent.id))
        .limit(min(limit, 100))
    )
    rows = session.execute(q).all()
    return [
        ConflictZoneItem(
            country_iso2=ev.country_iso2,
            country_name=name_en,
            title=ev.title,
            link=ev.link,
            published_at=ev.published_at,
        )
        for ev, name_en in rows
    ]


@router.get("/meta/sync", response_model=SyncStatus)
def sync_meta(session: Session = Depends(get_db)):
    last = session.execute(select(SyncRun).order_by(SyncRun.id.desc()).limit(1)).scalar_one_or_none()
    if not last:
        return SyncStatus(
            last_run_started=None,
            last_run_finished=None,
            last_status=None,
            last_message=None,
            items_ingested=None,
        )
    return SyncStatus(
        last_run_started=last.started_at,
        last_run_finished=last.finished_at,
        last_status=last.status,
        last_message=last.message,
        items_ingested=last.items_ingested,
    )


@router.post("/sync")
def trigger_sync(
    user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_db),
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Haber senkronu yalnızca organizasyon yöneticisi tarafından tetiklenebilir")
    run = run_conflict_sync(session)
    return {
        "status": run.status,
        "message": run.message,
        "items_ingested": run.items_ingested,
        "finished_at": run.finished_at.isoformat() if run.finished_at else None,
    }
