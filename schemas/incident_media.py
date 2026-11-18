from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime
from pydantic import Field
from sqlmodel import SQLModel

from models.enums import MediaType

class IncidentMediaCreate(SQLModel):
    incident_id: UUID
    
    file_url: str = Field(max_length=240)
    
    type: MediaType
    
    file_metadata: Dict[str, Any]
    
    captured_at: datetime
    uploaded_at: Optional[datetime] = Field(default=None)

class IncidentMediaUpdate(SQLModel):
    incident_id: Optional[UUID] = Field(default=None)
    file_url: Optional[str] = Field(default=None, max_length=240)
    type: Optional[MediaType] = Field(default=None)
    file_metadata: Optional[Dict[str, Any]] = Field(default=None)
    captured_at: Optional[datetime] = Field(default=None)
    uploaded_at: Optional[datetime] = Field(default=None)

class IncidentMediaResponse(SQLModel):
    media_id: UUID
    incident_id: UUID
    file_url: str = Field(max_length=240)
    type: MediaType
    file_metadata: Dict[str, Any]
    captured_at: datetime
    uploaded_at: Optional[datetime] = None

    model_config = {"from_attributes": True}