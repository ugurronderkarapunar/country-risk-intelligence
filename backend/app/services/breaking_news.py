from __future__ import annotations

import re
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime

import feedparser
import httpx
from sqlalchemy import delete, desc, func, nulls_last, select
from sqlalchemy.orm import Session

from app.models import BreakingNewsItem

DEFAULT_FEEDS: list[tuple[str, str]] = [
    ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("Google News TR", "https://news.google.com/rss?hl=tr&gl=TR&ceid=TR:tr"),
]

_CACHE_SEC = 15 * 60


def _parse_pub(entry) -> datetime | None:
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


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)[:500] if s else ""


def should_refresh(session: Session) -> bool:
    latest = session.execute(select(func.max(BreakingNewsItem.created_at))).scalar_one_or_none()
    if latest is None:
        return True
    if isinstance(latest, datetime):
        if latest.tzinfo is None:
            latest = latest.replace(tzinfo=UTC)
        return (datetime.now(UTC) - latest).total_seconds() > _CACHE_SEC
    return True


def ingest_breaking_news(session: Session, feeds: list[tuple[str, str]] | None = None) -> int:
    feeds = feeds or DEFAULT_FEEDS
    cutoff_item = datetime.now(UTC) - timedelta(hours=72)
    session.execute(delete(BreakingNewsItem).where(BreakingNewsItem.created_at < cutoff_item))

    added = 0
    with httpx.Client(timeout=30.0, headers={"User-Agent": "CountryRiskIntel-News/1.0"}) as client:
        for source_name, url in feeds:
            try:
                r = client.get(url)
                r.raise_for_status()
                parsed = feedparser.parse(r.text)
            except Exception:
                continue
            for entry in getattr(parsed, "entries", [])[:35]:
                title = (getattr(entry, "title", None) or "").strip()
                link = (getattr(entry, "link", None) or "").strip()
                if not title or not link:
                    continue
                if len(link) > 2000:
                    link = link[:2000]
                exists = session.execute(select(BreakingNewsItem.id).where(BreakingNewsItem.link == link)).first()
                if exists:
                    continue
                summary = ""
                if getattr(entry, "summary", None):
                    summary = _strip_html(entry.summary)
                session.add(
                    BreakingNewsItem(
                        source=source_name,
                        title=title[:500],
                        link=link,
                        summary=summary or None,
                        published_at=_parse_pub(entry),
                    )
                )
                added += 1
    session.commit()
    return added


def list_breaking_news(session: Session, limit: int = 40) -> list[BreakingNewsItem]:
    if should_refresh(session):
        try:
            ingest_breaking_news(session)
        except Exception:
            session.rollback()
    q = select(BreakingNewsItem).order_by(
        nulls_last(desc(BreakingNewsItem.published_at)),
        desc(BreakingNewsItem.id),
    )
    return list(session.execute(q.limit(min(limit, 80))).scalars().all())
