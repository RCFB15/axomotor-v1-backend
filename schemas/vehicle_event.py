from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime

from pydantic import Field
from sqlmodel import SQLModel

from schemas.vehicle_event_code import VehicleEventCodeResponse

class VehicleEventCreate(SQLModel):
    code: str = Field(max_length=12)
    vehicle_id: UUID
    position: Dict[str, Any]
    additional_data: Optional[Dict[str, Any]] = Field(default=None)

class VehicleEventResponse(SQLModel):
    event_id: UUID
    code: str = Field(max_length=12)
    vehicle_id: UUID
    position: Any
    additional_data: Optional[Dict[str, Any]] = None
    registered_at: datetime

    info: VehicleEventCodeResponse

    model_config = {"from_attributes": True}
