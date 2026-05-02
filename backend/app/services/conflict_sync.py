from __future__ import annotations

import re
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime

import feedparser
import httpx
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import ConflictEvent, Country, SyncRun

KEYWORD_ISO: list[tuple[str, str]] = [
    ("democratic republic of the congo", "CD"),
    ("dr congo", "CD"),
    ("drc", "CD"),
    ("south sudan", "SS"),
    ("sudan", "SD"),
    ("somalia", "SO"),
    ("ethiopia", "ET"),
    ("eritrea", "ER"),
    ("yemen", "YE"),
    ("syria", "SY"),
    ("gaza", "PS"),
    ("west bank", "PS"),
    ("palestin", "PS"),
    ("israel", "IL"),
    ("lebanon", "LB"),
    ("iraq", "IQ"),
    ("iran", "IR"),
    ("afghanistan", "AF"),
    ("pakistan", "PK"),
    ("ukraine", "UA"),
    ("russia", "RU"),
    ("myanmar", "MM"),
    ("burma", "MM"),
    ("mali", "ML"),
    ("burkina faso", "BF"),
    ("niger", "NE"),
    ("nigeria", "NG"),
    ("cameroon", "CM"),
    ("chad", "TD"),
    ("mozambique", "MZ"),
    ("haiti", "HT"),
    ("venezuela", "VE"),
    ("colombia", "CO"),
    ("libya", "LY"),
    ("turkey", "TR"),
    ("türkiye", "TR"),
    ("syrian", "SY"),
    ("ukrainian", "UA"),
    ("german", "DE"),
    ("france", "FR"),
    ("china", "CN"),
    ("india", "IN"),
    ("egypt", "EG"),
    ("saudi", "SA"),
    ("congo", "CD"),
]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def _extract_isos(text: str) -> set[str]:
    hay = _normalize(text)
    found: set[str] = set()
    for key, iso in sorted(KEYWORD_ISO, key=lambda x: -len(x[0])):
        if key in hay:
            found.add(iso)
    return found


def _parse_published(entry) -> datetime | None:
    raw = getattr(entry, "published", None) or getattr(entry, "updated", None)
    if not raw:
        return None
    try:
        dt = parsedate_to_datetime(raw)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=UTC)
        return dt.astimezone(UTC)
    except (TypeError, ValueError, OverflowError):
        return None


def run_conflict_sync(session: Session) -> SyncRun:
    run = SyncRun(status="running", message=None, items_ingested=0)
    session.add(run)
    session.commit()
    session.refresh(run)

    try:
        with httpx.Client(timeout=45.0, headers={"User-Agent": "CountryRiskIntel/1.0"}) as client:
            r = client.get(settings.reliefweb_rss_url)
            r.raise_for_status()
            parsed = feedparser.parse(r.text)

        existing_links = {row[0] for row in session.execute(select(ConflictEvent.link)).all()}
        valid_isos = {row[0] for row in session.execute(select(Country.iso2)).all()}

        inserted = 0
        for entry in getattr(parsed, "entries", [])[:120]:
            title = getattr(entry, "title", "") or ""
            summary = ""
            if getattr(entry, "summary", None):
                summary = re.sub("<[^>]+>", "", entry.summary)
            link = getattr(entry, "link", "") or ""
            if not link or link in existing_links:
                continue
            isos = _extract_isos(title + " " + summary)
            isos &= valid_isos
            if not isos:
                continue
            pub = _parse_published(entry)
            for iso in isos:
                session.add(
                    ConflictEvent(
                        country_iso2=iso,
                        title=title[:500],
                        link=link,
                        summary=(summary[:2000] if summary else None),
                        published_at=pub,
                        source="reliefweb",
                    )
                )
                inserted += 1
            existing_links.add(link)

        cutoff = datetime.now(UTC) - timedelta(days=45)
        session.execute(delete(ConflictEvent).where(ConflictEvent.created_at < cutoff))

        run.status = "ok"
        run.message = f"ReliefWeb RSS işlendi; {inserted} ülke-olay kaydı eklendi."
        run.items_ingested = inserted
    except Exception as e:  # noqa: BLE001
        run.status = "error"
        run.message = str(e)[:2000]
        run.items_ingested = 0

    run.finished_at = datetime.now(UTC)
    session.commit()
    session.refresh(run)
    return run


def event_counts_last_days(session: Session, days: int = 14) -> dict[str, int]:
    since = datetime.now(UTC) - timedelta(days=days)
    ts = func.coalesce(ConflictEvent.published_at, ConflictEvent.created_at)
    q = select(ConflictEvent.country_iso2, func.count()).where(ts >= since).group_by(ConflictEvent.country_iso2)
    rows = session.execute(q).all()
    return {iso: int(n) for iso, n in rows}
