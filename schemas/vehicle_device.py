from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum
from pydantic import Field
from sqlmodel import SQLModel

class DeviceType(str, Enum):
    HUB = "HUB"
    NODE = "NODE"

class VehicleDeviceCreate(SQLModel):
    vehicle_id: UUID
    serial_number: str = Field(max_length=12)
    tag: str = Field(max_length=16)
    type: DeviceType
    
    battery_level: int = Field(ge=0, le=100)
    
    is_active: bool = Field(default=False)
    is_enabled: bool = Field(default=True)

class VehicleDeviceUpdate(SQLModel):
    vehicle_id: Optional[UUID] = Field(default=None)
    serial_number: Optional[str] = Field(default=None, max_length=12)
    tag: Optional[str] = Field(default=None, max_length=16)
    type: Optional[DeviceType] = Field(default=None)
    battery_level: Optional[int] = Field(default=None, ge=0, le=100)
    is_active: Optional[bool] = Field(default=None)
    is_enabled: Optional[bool] = Field(default=None)

class VehicleDeviceResponse(SQLModel):
    device_id: UUID
    vehicle_id: UUID
    serial_number: str = Field(max_length=12)
    tag: str = Field(max_length=16)
    type: DeviceType
    battery_level: int
    is_active: bool
    is_enabled: bool
    registered_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}