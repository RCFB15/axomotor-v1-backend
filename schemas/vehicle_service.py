from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum
from pydantic import Field
from sqlmodel import SQLModel

class ServiceStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    DISCARDED = "DISCARDED"

class VehicleServiceCreate(SQLModel):
    vehicle_id: UUID
    
    status: ServiceStatus = Field(default=ServiceStatus.PENDING)
    
    date: datetime
    next_service_date: Optional[datetime] = Field(default=None)
    
    created_by_id: UUID
    authorized_by_id: Optional[UUID] = Field(default=None)

class VehicleServiceUpdate(SQLModel):
    vehicle_id: Optional[UUID] = Field(default=None)
    status: Optional[ServiceStatus] = Field(default=None)
    date: Optional[datetime] = Field(default=None)
    next_service_date: Optional[datetime] = Field(default=None)
    authorized_by_id: Optional[UUID] = Field(default=None)

class VehicleServiceResponse(SQLModel):
    service_id: UUID
    vehicle_id: UUID
    status: ServiceStatus
    date: datetime
    next_service_date: Optional[datetime] = None
    created_by_id: UUID
    authorized_by_id: Optional[UUID] = None
    registered_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}