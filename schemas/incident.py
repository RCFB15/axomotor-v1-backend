from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime
from pydantic import Field
from sqlmodel import SQLModel

from models.enums import IncidentStatus

class IncidentCreate(SQLModel):
    related_incident_id: UUID
    trip_id: UUID
    code: str = Field(max_length=12)
    
    created_by_id: Optional[UUID] = Field(default=None)
    reviewed_by_id: Optional[UUID] = Field(default=None)
    
    status: IncidentStatus = Field(default=IncidentStatus.open)
    
    position: Dict[str, Any]
    description: str = Field(max_length=500)
    comments: Optional[str] = Field(default=None, max_length=500)
    
    reviewed_at: Optional[datetime] = Field(default=None)
    closed_at: Optional[datetime] = Field(default=None)

class IncidentUpdate(SQLModel):
    related_incident_id: Optional[UUID] = Field(default=None)
    trip_id: Optional[UUID] = Field(default=None)
    code: Optional[str] = Field(default=None, max_length=12)
    created_by_id: Optional[UUID] = Field(default=None)
    reviewed_by_id: Optional[UUID] = Field(default=None)
    status: Optional[IncidentStatus] = Field(default=None)
    position: Optional[Dict[str, Any]] = Field(default=None)
    description: Optional[str] = Field(default=None, max_length=500)
    comments: Optional[str] = Field(default=None, max_length=500)
    reviewed_at: Optional[datetime] = Field(default=None)
    closed_at: Optional[datetime] = Field(default=None)

class IncidentResponse(SQLModel):
    incident_id: UUID
    related_incident_id: UUID
    created_by_id: Optional[UUID] = None
    reviewed_by_id: Optional[UUID] = None
    trip_id: UUID
    code: str = Field(max_length=12)
    status: IncidentStatus
    position: Any
    description: str = Field(max_length=500)
    comments: Optional[str] = Field(default=None, max_length=500)
    registered_at: datetime
    reviewed_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}