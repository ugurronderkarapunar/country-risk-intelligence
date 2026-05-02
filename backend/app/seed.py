from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Country

SEED_COUNTRIES: list[dict] = [
    {"iso2": "TR", "name_en": "Türkiye", "conflict_base": 4.2, "political_stability": 5.8, "economic_risk": 6.0, "logistics_friction": 4.5, "latitude": 38.9637, "longitude": 35.2433},
    {"iso2": "DE", "name_en": "Germany", "conflict_base": 1.2, "political_stability": 8.2, "economic_risk": 3.0, "logistics_friction": 2.0, "latitude": 51.1657, "longitude": 10.4515},
    {"iso2": "NL", "name_en": "Netherlands", "conflict_base": 0.8, "political_stability": 8.5, "economic_risk": 2.8, "logistics_friction": 2.2, "latitude": 52.1326, "longitude": 5.2913},
    {"iso2": "CN", "name_en": "China", "conflict_base": 2.8, "political_stability": 6.5, "economic_risk": 5.8, "logistics_friction": 5.5, "latitude": 35.8617, "longitude": 104.1954},
    {"iso2": "US", "name_en": "United States", "conflict_base": 2.5, "political_stability": 6.8, "economic_risk": 4.2, "logistics_friction": 3.0, "latitude": 37.0902, "longitude": -95.7129},
    {"iso2": "AE", "name_en": "United Arab Emirates", "conflict_base": 1.5, "political_stability": 7.8, "economic_risk": 3.5, "logistics_friction": 3.2, "latitude": 23.4241, "longitude": 53.8478},
    {"iso2": "IR", "name_en": "Iran", "conflict_base": 6.5, "political_stability": 4.0, "economic_risk": 7.8, "logistics_friction": 7.5, "latitude": 32.4279, "longitude": 53.6880},
    {"iso2": "IQ", "name_en": "Iraq", "conflict_base": 7.8, "political_stability": 3.5, "economic_risk": 7.2, "logistics_friction": 8.0, "latitude": 33.2232, "longitude": 43.6793},
    {"iso2": "IL", "name_en": "Israel", "conflict_base": 7.0, "political_stability": 5.5, "economic_risk": 4.8, "logistics_friction": 5.5, "latitude": 31.0461, "longitude": 34.8516},
    {"iso2": "PS", "name_en": "Palestinian Territories", "conflict_base": 8.5, "political_stability": 3.0, "economic_risk": 8.0, "logistics_friction": 8.5, "latitude": 31.9522, "longitude": 35.2332},
    {"iso2": "SY", "name_en": "Syria", "conflict_base": 9.2, "political_stability": 2.0, "economic_risk": 9.0, "logistics_friction": 9.5, "latitude": 34.8021, "longitude": 38.9968},
    {"iso2": "UA", "name_en": "Ukraine", "conflict_base": 8.8, "political_stability": 3.2, "economic_risk": 7.8, "logistics_friction": 8.8, "latitude": 48.3794, "longitude": 31.1656},
    {"iso2": "RU", "name_en": "Russia", "conflict_base": 6.2, "political_stability": 4.2, "economic_risk": 6.8, "logistics_friction": 7.0, "latitude": 61.5240, "longitude": 105.3188},
    {"iso2": "SD", "name_en": "Sudan", "conflict_base": 8.5, "political_stability": 2.5, "economic_risk": 8.2, "logistics_friction": 9.0, "latitude": 12.8628, "longitude": 30.2176},
    {"iso2": "YE", "name_en": "Yemen", "conflict_base": 8.9, "political_stability": 2.2, "economic_risk": 8.8, "logistics_friction": 9.2, "latitude": 15.5527, "longitude": 48.5164},
    {"iso2": "AF", "name_en": "Afghanistan", "conflict_base": 8.7, "political_stability": 2.0, "economic_risk": 8.5, "logistics_friction": 9.3, "latitude": 33.9391, "longitude": 67.7100},
    {"iso2": "MM", "name_en": "Myanmar", "conflict_base": 7.5, "political_stability": 3.0, "economic_risk": 7.0, "logistics_friction": 8.0, "latitude": 21.9162, "longitude": 95.9560},
    {"iso2": "ET", "name_en": "Ethiopia", "conflict_base": 7.2, "political_stability": 3.8, "economic_risk": 7.5, "logistics_friction": 8.2, "latitude": 9.1450, "longitude": 40.4897},
    {"iso2": "NG", "name_en": "Nigeria", "conflict_base": 6.8, "political_stability": 4.0, "economic_risk": 7.2, "logistics_friction": 7.8, "latitude": 9.0820, "longitude": 8.6753},
    {"iso2": "IN", "name_en": "India", "conflict_base": 4.0, "political_stability": 6.0, "economic_risk": 5.5, "logistics_friction": 6.0, "latitude": 20.5937, "longitude": 78.9629},
    {"iso2": "EG", "name_en": "Egypt", "conflict_base": 5.0, "political_stability": 5.0, "economic_risk": 6.5, "logistics_friction": 6.2, "latitude": 26.8206, "longitude": 30.8025},
    {"iso2": "SA", "name_en": "Saudi Arabia", "conflict_base": 3.5, "political_stability": 6.5, "economic_risk": 5.0, "logistics_friction": 4.8, "latitude": 23.8859, "longitude": 45.0792},
    {"iso2": "PL", "name_en": "Poland", "conflict_base": 2.0, "political_stability": 7.5, "economic_risk": 3.8, "logistics_friction": 3.5, "latitude": 51.9194, "longitude": 19.1451},
    {"iso2": "IT", "name_en": "Italy", "conflict_base": 1.8, "political_stability": 7.0, "economic_risk": 5.5, "logistics_friction": 4.0, "latitude": 41.8719, "longitude": 12.5674},
    {"iso2": "GB", "name_en": "United Kingdom", "conflict_base": 1.5, "political_stability": 7.5, "economic_risk": 4.0, "logistics_friction": 3.2, "latitude": 55.3781, "longitude": -3.4360},
    {"iso2": "FR", "name_en": "France", "conflict_base": 2.0, "political_stability": 7.0, "economic_risk": 4.5, "logistics_friction": 3.0, "latitude": 46.2276, "longitude": 2.2137},
    {"iso2": "BR", "name_en": "Brazil", "conflict_base": 3.2, "political_stability": 5.5, "economic_risk": 6.2, "logistics_friction": 6.5, "latitude": -14.2350, "longitude": -51.9253},
    {"iso2": "CD", "name_en": "DR Congo", "conflict_base": 7.8, "political_stability": 2.8, "economic_risk": 8.0, "logistics_friction": 8.8, "latitude": -4.0383, "longitude": 21.7587},
    {"iso2": "HT", "name_en": "Haiti", "conflict_base": 7.0, "political_stability": 2.5, "economic_risk": 8.5, "logistics_friction": 8.0, "latitude": 18.9712, "longitude": -72.2852},
    {"iso2": "VE", "name_en": "Venezuela", "conflict_base": 5.5, "political_stability": 3.5, "economic_risk": 8.8, "logistics_friction": 7.5, "latitude": 6.4238, "longitude": -66.5897},
]


def ensure_seed(session: Session) -> None:
    if session.execute(select(Country.iso2).limit(1)).scalar_one_or_none() is not None:
        return
    for row in SEED_COUNTRIES:
        session.add(Country(**row))
    session.commit()
