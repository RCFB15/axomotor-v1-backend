from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional, Any, Dict

from pydantic import BaseModel, Field, model_validator, computed_field

class EventBase(BaseModel):
    latitude: Optional[float] = Field(default=None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(default=None, ge=-180.0, le=180.0)
    registered_at: datetime

    @model_validator(mode="after")
    def validate_coordinates(self) -> "EventBase":
        if ([self.latitude, self.longitude].count(None) == 1) or \
            (self.latitude == 0.0 and self.longitude == 0.0):
            raise ValueError("Invalid GPS coordinates")
        return self

    @computed_field
    @property
    def has_position(self) -> bool:
        return self.latitude is not None and self.longitude is not None

class VehicleEventCreate(EventBase):
    code: str = Field(max_length=12)
    additional_data: Optional[Dict[str, Any]] = Field(default=None)

class PositionCreate(EventBase):
    trip_id: Optional[UUID]
    speed: Decimal = Field(default=Decimal(0), ge=0.0, le=300.0)

class IncidentCreate(EventBase):
    trip_id: UUID
    code: str = Field(max_length=12)
    description: str = Field(min_length=2, max_length=500)
