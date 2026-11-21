from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional, Any, Dict

from pydantic import Field
from sqlmodel import SQLModel

class TripPositionResponse(SQLModel):
    position_id: UUID
    trip_id: UUID
    position: Any
    speed: Decimal
    registered_at: datetime

    model_config = {"from_attributes": True}
