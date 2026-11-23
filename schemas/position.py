from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional, Any, Dict
import json

from sqlmodel import SQLModel
from pydantic import field_validator

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
