from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional, Any, Dict
import json

from sqlmodel import SQLModel
from pydantic import Field, field_validator, model_validator, computed_field

class PositionCreateBase(SQLModel):
    latitude: Optional[Decimal] = Field(default=None, ge=-90.0, le=90.0)
    longitude: Optional[Decimal] = Field(default=None, ge=-180.0, le=180.0)

    @model_validator(mode="after")
    def validate_coordinates(self) -> "PositionCreateBase":
        if ([self.latitude, self.longitude].count(None) == 1) or \
            (self.latitude == 0.0 and self.longitude == 0.0):
            raise ValueError("Invalid GPS coordinates")
        return self

    @computed_field
    @property
    def has_position(self) -> bool:
        return self.latitude is not None and self.longitude is not None

class PositionResponse(SQLModel):
    position_id: UUID
    vehicle_id: UUID
    trip_id: Optional[UUID]
    geojson: Dict[str, Any]
    speed: Decimal
    registered_at: datetime

    @field_validator("geojson", mode="before")
    @classmethod
    def parse_geojson(cls, v: Any) -> Dict[str, Any]:
        return json.loads(v) if isinstance(v, str) else v
