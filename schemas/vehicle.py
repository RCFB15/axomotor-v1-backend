from typing import Optional
from uuid import UUID
from datetime import datetime, timezone

from pydantic import Field
from sqlmodel import SQLModel

from models.enums import VehicleType, VehicleStatus

class VehicleCreate(SQLModel):
    plate_number: str = Field(min_length=8, max_length=12)
    reg_number: str = Field(min_length=16, max_length=22)
    series_vin: str = Field(min_length=17, max_length=17)
    brand: str = Field(min_length=1, max_length=60)
    model: str = Field(min_length=1, max_length=60)
    year: int = Field(gt=1900, le=datetime.now(timezone.utc).year + 2)
    type: VehicleType
    status: VehicleStatus = Field(default=VehicleStatus.operative)

class VehicleUpdate(SQLModel):
    plate_number: Optional[str] = Field(default=None, min_length=8, max_length=12)
    reg_number: Optional[str] = Field(default=None, min_length=16, max_length=22)
    series_vin: Optional[str] = Field(default=None, min_length=17, max_length=17)
    brand: Optional[str] = Field(default=None, min_length=1, max_length=60)
    model: Optional[str] = Field(default=None, min_length=1, max_length=60)
    year: Optional[int] = Field(default=None, gt=1900, le=datetime.now(timezone.utc).year + 2)
    type: Optional[VehicleType] = Field(default=None)
    status: Optional[VehicleStatus] = Field(default=None)

class VehicleResponse(SQLModel):
    vehicle_id: UUID
    plate_number: str = Field(max_length=12)
    reg_number: str = Field(max_length=22)
    series_vin: str = Field(max_length=17)
    brand: str = Field(max_length=60)
    model: str = Field(max_length=60)
    year: int
    type: VehicleType
    status: VehicleStatus
    registered_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
