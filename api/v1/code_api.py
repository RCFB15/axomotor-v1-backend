from typing import Optional

from fastapi import APIRouter, Depends
from sqlmodel import Session, col, select

from api.v1.dependencies import get_current_user
from db.database import get_session
from models import IncidentCode, User, VehicleEventCode
from models.enums import SeverityLevel
from schemas.incident_code import IncidentCodeResponse
from schemas.vehicle_event_code import VehicleEventCodeResponse

router = APIRouter()


@router.get("/incidents", response_model=list[IncidentCodeResponse])
def get_incident_codes(
    severity: Optional[SeverityLevel] = None,
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> list[IncidentCode]:
    statement = select(IncidentCode)
    if severity is not None:
        statement = statement.where(IncidentCode.severity == severity)
    statement = statement.order_by(col(IncidentCode.code))
    return list(session.exec(statement).all())


@router.get("/events", response_model=list[VehicleEventCodeResponse])
def get_event_codes(
    severity: Optional[SeverityLevel] = None,
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> list[VehicleEventCode]:
    statement = select(VehicleEventCode)
    if severity is not None:
        statement = statement.where(VehicleEventCode.severity == severity)
    statement = statement.order_by(col(VehicleEventCode.code))
    return list(session.exec(statement).all())