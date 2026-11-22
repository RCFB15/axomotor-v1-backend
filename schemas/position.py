from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional, Any

from sqlmodel import SQLModel
from pydantic import Field, computed_field
from geoalchemy2.shape import to_shape

class PositionResponse(SQLModel):
    position_id: UUID
    vehicle_id: UUID
    trip_id: Optional[UUID]
    latitude: Decimal
    longitude: Decimal
    speed: Decimal
    registered_at: datetime

    position: Any = Field(exclude=True)

    model_config = {"from_attributes": True}
