from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum
from pydantic import Field
from sqlmodel import SQLModel

class VehicleType(str, Enum):
    PASSENGER_CAR = "PASSENGER_CAR"
    PICKUP = "PICKUP"
    PANEL = "PANEL"
    VAN = "VAN"
    BUS = "BUS"
    TRUCK = "TRUCK"

class VehicleStatus(str, Enum):
    OPERATIVE = "OPERATIVE"
    IN_USE = "IN_USE"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"
    DOCUMENTS_EXPIRED = "DOCUMENTS_EXPIRED"
    HELD_BY_AUTHORITIES = "HELD_BY_AUTHORITIES"

class VehicleCreate(SQLModel):
    plate_number: str = Field(max_length=12)
    reg_number: str = Field(max_length=22)
    series_vin: str = Field(max_length=17)
    brand: str = Field(max_length=60)
    model: str = Field(max_length=60)
    year: int
    type: VehicleType
    
    axes: int = Field(default=2)
    status: VehicleStatus = Field(default=VehicleStatus.OPERATIVE)

class VehicleUpdate(SQLModel):
    plate_number: Optional[str] = Field(default=None, max_length=12)
    reg_number: Optional[str] = Field(default=None, max_length=22)
    series_vin: Optional[str] = Field(default=None, max_length=17)
    brand: Optional[str] = Field(default=None, max_length=60)
    model: Optional[str] = Field(default=None, max_length=60)
    year: Optional[int] = Field(default=None)
    type: Optional[VehicleType] = Field(default=None)
    axes: Optional[int] = Field(default=None)
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
    axes: int
    status: VehicleStatus
    registered_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}