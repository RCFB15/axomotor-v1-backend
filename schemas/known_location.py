from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime
from pydantic import Field
from sqlmodel import SQLModel

class KnownLocationCreate(SQLModel):
    name: str = Field(min_length=1, max_length=60)
    type: Optional[str] = Field(default=None, max_length=40)
    address: str = Field(max_length=240)
    location_area: Dict[str, Any]

class KnownLocationUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=60)
    type: Optional[str] = Field(default=None, max_length=40)
    address: Optional[str] = Field(default=None, max_length=240)
    location_area: Optional[Dict[str, Any]] = Field(default=None)

class KnownLocationResponse(SQLModel):
    location_id: UUID
    name: str = Field(max_length=60)
    type: Optional[str] = Field(default=None, max_length=40)
    address: str = Field(max_length=240)
    location_area: Any
    registered_at: datetime

    model_config = {"from_attributes": True}
