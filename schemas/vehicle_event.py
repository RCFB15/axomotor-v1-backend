from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime

from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from pydantic import Field, computed_field
from sqlmodel import SQLModel

from schemas.position import PositionCreateBase
from schemas.vehicle_event_code import VehicleEventCodeResponse

class VehicleEventCreate(PositionCreateBase):
    code: str = Field(max_length=12)
    additional_data: Optional[Dict[str, Any]] = Field(default=None)

class VehicleEventResponse(SQLModel):
    event_id: UUID
    vehicle_id: UUID
    code: str = Field(exclude=True)
    info: VehicleEventCodeResponse
    position: Any = Field(exclude=True)
    additional_data: Optional[Dict[str, Any]] = None
    registered_at: datetime

    @computed_field
    @property
    def geojson(self) -> Optional[Dict[str, Any]]:
        if self.position:
            point = to_shape(self.position)
            return mapping(point)
        else:
            return None
