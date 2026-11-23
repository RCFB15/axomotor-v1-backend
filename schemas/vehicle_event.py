from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from pydantic import Field, model_validator, computed_field, field_validator
from sqlmodel import SQLModel

from schemas.vehicle_event_code import VehicleEventCodeResponse

class VehicleEventCreate(SQLModel):
    code: str = Field(max_length=12)
    latitude: Optional[Decimal] = Field(default=None, ge=-90.0, le=90.0)
    longitude: Optional[Decimal] = Field(default=None, ge=-180.0, le=180.0)
    additional_data: Optional[Dict[str, Any]] = Field(default=None)

    @model_validator(mode="after")
    def validate_coordinates(self) -> "VehicleEventCreate":
        if ([self.latitude, self.longitude].count(None) == 1) or \
            (self.latitude == 0.0 and self.longitude == 0.0):
            raise ValueError("Invalid GPS coordinates")
        return self

    @computed_field
    @property
    def has_position(self) -> bool:
        return self.latitude is not None and self.longitude is not None

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
