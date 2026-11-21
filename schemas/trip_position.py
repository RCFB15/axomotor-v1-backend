from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime
from pydantic import Field
from sqlmodel import SQLModel

class TripPositionCreate(SQLModel):
    trip_id: UUID
    
    position: Dict[str, Any]
    
    speed: float

class TripPositionUpdate(SQLModel):
    trip_id: Optional[UUID] = Field(default=None)
    position: Optional[Dict[str, Any]] = Field(default=None)
    speed: Optional[float] = Field(default=None)

class TripPositionResponse(SQLModel):
    position_id: UUID
    trip_id: UUID
    position: Any
    speed: float
    registered_at: datetime
    
    model_config = {"from_attributes": True}