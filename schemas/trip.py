from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import Field
from sqlmodel import SQLModel

from models.enums import TripStatus

class TripCreate(SQLModel):
    vehicle_id: UUID
    driver_id: UUID
    origin_id: UUID
    destination_id: UUID
    
    departure_date: datetime
    arrive_date: Optional[datetime] = Field(default=None)
    
    status: TripStatus = Field(default=TripStatus.planned)
    
    distance: Optional[float] = Field(default=None)
    average_speed: Optional[float] = Field(default=None)
    
    started_at: Optional[datetime] = Field(default=None)
    finished_at: Optional[datetime] = Field(default=None)

class TripUpdate(SQLModel):
    vehicle_id: Optional[UUID] = Field(default=None)
    driver_id: Optional[UUID] = Field(default=None)
    origin_id: Optional[UUID] = Field(default=None)
    destination_id: Optional[UUID] = Field(default=None)
    
    departure_date: Optional[datetime] = Field(default=None)
    arrive_date: Optional[datetime] = Field(default=None)
    
    status: Optional[TripStatus] = Field(default=None)
    distance: Optional[float] = Field(default=None)
    average_speed: Optional[float] = Field(default=None)
    
    started_at: Optional[datetime] = Field(default=None)
    finished_at: Optional[datetime] = Field(default=None)

class TripResponse(SQLModel):
    trip_id: UUID
    vehicle_id: UUID
    driver_id: UUID
    origin_id: UUID
    destination_id: UUID
    departure_date: datetime
    arrive_date: Optional[datetime] = None
    status: TripStatus
    distance: Optional[float] = None
    average_speed: Optional[float] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    model_config = {"from_attributes": True}