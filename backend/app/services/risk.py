def conflict_boost_from_events(event_count_14d: int) -> float:
    """RSS kaynaklı olay sayısına göre çatışma bileşenine üst sınırı 3 puan olacak şekilde ekleme."""
    if event_count_14d <= 0:
        return 0.0
    return min(3.0, 0.45 + (event_count_14d - 1) * 0.35)


def effective_conflict(conflict_base: float, boost: float) -> float:
    return round(min(10.0, conflict_base + boost), 2)


def risk_score(
    conflict_effective: float,
    political_stability: float,
    economic_risk: float,
    logistics_friction: float,
) -> float:
    """0–10 bileşik risk. Yüksek = daha riskli."""
    political_instability = 10.0 - political_stability
    raw = (
        conflict_effective * 0.38
        + political_instability * 0.27
        + economic_risk * 0.25
        + logistics_friction * 0.10
    )
    return round(min(10.0, max(0.0, raw)), 2)


def risk_level(score: float) -> str:
    if score < 3.0:
        return "LOW"
    if score < 5.5:
        return "MEDIUM"
    if score < 7.5:
        return "HIGH"
    return "EXTREME"
