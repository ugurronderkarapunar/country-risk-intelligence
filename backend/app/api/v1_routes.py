from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_org_from_api_key
from app.models import Organization
from app.schemas import CorridorIn, CountryDetail
from app.api.routes import _country_brief_list, country_detail
from app.services.corridor_risk import analyze_corridor
from app.services.usage import check_and_increment_corridor

router = APIRouter(prefix="/api/v1", tags=["api-v1"])


@router.post("/corridor")
def v1_corridor(
    body: CorridorIn,
    org: Annotated[Organization, Depends(get_org_from_api_key)],
    session: Session = Depends(get_db),
):
    check_and_increment_corridor(session, org)
    return analyze_corridor(session, body.legs)


@router.get("/countries")
def v1_countries(
    org: Annotated[Organization, Depends(get_org_from_api_key)],
    session: Session = Depends(get_db),
):
    _ = org
    return _country_brief_list(session)


@router.get("/countries/{iso2}", response_model=CountryDetail)
def v1_country_detail(
    iso2: str,
    org: Annotated[Organization, Depends(get_org_from_api_key)],
    session: Session = Depends(get_db),
):
    _ = org
    return country_detail(iso2, session)
