from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime

from pydantic import Field
from sqlmodel import SQLModel

from models.enums import IncidentStatus, PriorityLevel
from schemas.incident_code import IncidentCodeResponse
from schemas.user import UserResponse
from schemas.trip import TripResponse

class IncidentCreate(SQLModel):
    trip_id: UUID
    code: str = Field(max_length=12)
    status: Optional[IncidentStatus] = Field(default=IncidentStatus.open)
    description: str = Field(min_length=2, max_length=500)
    comments: Optional[str] = Field(default=None, min_length=2, max_length=500)
    related_incident_id: Optional[UUID] = Field(default=None)

class IncidentUpdate(SQLModel):
    code: Optional[str] = Field(default=None, max_length=12)
    priority: Optional[PriorityLevel] = Field(default=None)
    status: Optional[IncidentStatus] = Field(default=None)
    description: Optional[str] = Field(default=None, min_length=2, max_length=500)
    comments: Optional[str] = Field(default=None, min_length=2, max_length=500)
    related_incident_id: Optional[UUID] = Field(default=None)

class IncidentResponse(SQLModel):
    incident_id: UUID
    trip_id: UUID
    code: str = Field(max_length=12)
    priority: PriorityLevel
    status: IncidentStatus
    position: Any
    description: str = Field(max_length=500)
    comments: Optional[str] = Field(default=None, max_length=500)
    related_incident_id: Optional[UUID]
    registered_at: datetime
    reviewed_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    created_by_id: Optional[UUID] = None
    reviewed_by_id: Optional[UUID] = None

    info: IncidentCodeResponse

    model_config = {"from_attributes": True}

class IncidentResponseExtended(IncidentResponse):
    trip: TripResponse
    created_by: Optional[UserResponse]
    reviewed_by: Optional[UserResponse]
