from datetime import datetime, timezone
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, field_validator

class EventBase(BaseModel):
    latitude: float = Field(ge=-90.0, le=90.0)
    longitude: float = Field(ge=-180.0, le=180.0)
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("longitude")
    @classmethod
    def reject_invalid_coordinates(cls, long: float, info) -> float:
        lat = info.data.get("latitude")
        if lat == 0.0 and long == 0.0:
            raise ValueError("Invalid GPS Coordinates (0.0, 0.0)")
        return long

class VehicleEventRegister(EventBase):
    code: str = Field(max_length=12)
    additional_data: Optional[dict] = Field(default=None)

class TripPositionRegister(EventBase):
    speed: Decimal = Field(default=Decimal(0), ge=0.0, le=300.0)
