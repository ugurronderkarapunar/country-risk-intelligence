from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models import Country
from app.services.conflict_sync import event_counts_last_days
from app.services.recommendations import trade_logistics_recommendations
from app.services.risk import conflict_boost_from_events, effective_conflict, risk_level, risk_score


@dataclass
class LegBrief:
    iso2: str
    name_en: str
    risk_score: float
    risk_level: str
    logistics_friction: float


def analyze_corridor(session: Session, legs_iso2: list[str]) -> dict:
    """Transit ülke zinciri için darboğaz ve birleşik öneriler."""
    seen: set[str] = set()
    legs_clean: list[str] = []
    for raw in legs_iso2:
        code = raw.strip().upper()
        if len(code) != 2 or code in seen:
            continue
        seen.add(code)
        legs_clean.append(code)

    if len(legs_clean) < 2:
        return {
            "valid": False,
            "message": "En az iki farklı ülke ISO2 kodu girin (ör. DE,PL,UA).",
            "legs": [],
            "bottleneck": None,
            "corridor_risk_score": None,
            "recommendations": [],
        }

    counts = event_counts_last_days(session, 14)
    leg_rows: list[LegBrief] = []
    for iso in legs_clean:
        c = session.get(Country, iso)
        if not c:
            return {
                "valid": False,
                "message": f"Bilinmeyen ülke kodu: {iso}",
                "legs": [],
                "bottleneck": None,
                "corridor_risk_score": None,
                "recommendations": [],
            }
        boost = conflict_boost_from_events(counts.get(c.iso2, 0))
        ce = effective_conflict(c.conflict_base, boost)
        rs = risk_score(ce, c.political_stability, c.economic_risk, c.logistics_friction)
        lvl = risk_level(rs)
        leg_rows.append(
            LegBrief(
                iso2=c.iso2,
                name_en=c.name_en,
                risk_score=rs,
                risk_level=lvl,
                logistics_friction=c.logistics_friction,
            )
        )

    bottleneck = max(leg_rows, key=lambda x: x.risk_score)
    avg_log = sum(x.logistics_friction for x in leg_rows) / len(leg_rows)
    corridor_score = round(
        max(x.risk_score for x in leg_rows) * 0.65 + (sum(x.risk_score for x in leg_rows) / len(leg_rows)) * 0.35,
        2,
    )
    worst = session.get(Country, bottleneck.iso2)
    assert worst is not None
    boost_b = conflict_boost_from_events(counts.get(worst.iso2, 0))
    ce_b = effective_conflict(worst.conflict_base, boost_b)
    recs = trade_logistics_recommendations(
        risk_level=risk_level(corridor_score if corridor_score <= 10 else 10),
        conflict_effective=ce_b,
        political_stability=worst.political_stability,
        economic_risk=worst.economic_risk,
        logistics_friction=max(x.logistics_friction for x in leg_rows),
    )
    recs.insert(
        0,
        f"Koridor ({len(leg_rows)} bacak): darboğaz ülke {bottleneck.name_en} ({bottleneck.iso2}), "
        f"ortalama lojistik sürtünme {avg_log:.1f}/10.",
    )

    return {
        "valid": True,
        "message": None,
        "legs": [
            {
                "iso2": x.iso2,
                "name_en": x.name_en,
                "risk_score": x.risk_score,
                "risk_level": x.risk_level,
                "logistics_friction": x.logistics_friction,
            }
            for x in leg_rows
        ],
        "bottleneck": {
            "iso2": bottleneck.iso2,
            "name_en": bottleneck.name_en,
            "risk_score": bottleneck.risk_score,
            "risk_level": bottleneck.risk_level,
        },
        "corridor_risk_score": corridor_score,
        "corridor_risk_level": risk_level(corridor_score),
        "recommendations": recs,
    }
