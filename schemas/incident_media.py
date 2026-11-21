from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime

from pydantic import Field
from sqlmodel import SQLModel

from models.enums import MediaType

class IncidentMediaCreate(SQLModel):
    incident_id: UUID
    type: MediaType
    file_metadata: Dict[str, Any]
    captured_at: datetime

class IncidentMediaResponse(SQLModel):
    media_id: UUID
    incident_id: UUID
    file_url: str = Field(max_length=240)
    type: MediaType
    file_metadata: Dict[str, Any]
    captured_at: datetime
    uploaded_at: datetime

    model_config = {"from_attributes": True}
