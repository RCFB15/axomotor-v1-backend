from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import Field
from sqlmodel import SQLModel

from models.enums import VehicleDeviceType

class VehicleDeviceCreate(SQLModel):
    vehicle_id: UUID
    serial_number: str = Field(min_length=12, max_length=12)
    tag: str = Field(max_length=16)
    type: VehicleDeviceType
    is_enabled: bool = Field(default=True)

class VehicleDeviceUpdate(SQLModel):
    vehicle_id: Optional[UUID] = Field(default=None)
    serial_number: Optional[str] = Field(default=None, min_length=12, max_length=12)
    tag: Optional[str] = Field(default=None, max_length=16)
    type: Optional[VehicleDeviceType] = Field(default=None)
    is_enabled: Optional[bool] = None

class VehicleDeviceResponse(SQLModel):
    device_id: UUID
    vehicle_id: UUID
    serial_number: str = Field(max_length=12)
    tag: str = Field(max_length=16)
    type: VehicleDeviceType
    battery_level: int
    is_active: bool
    is_enabled: bool
    registered_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
