from typing import Optional
from enum import Enum
from pydantic import Field
from sqlmodel import SQLModel

class EventSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class VehicleEventCodeCreate(SQLModel):
    code: str = Field(max_length=12)
    description: str = Field(max_length=40)
    # La severidad no puede ser nula y debe ser una de las opciones del Enum
    severity: EventSeverity

class VehicleEventCodeUpdate(SQLModel):
    description: Optional[str] = Field(default=None, max_length=40)
    severity: Optional[EventSeverity] = Field(default=None)

class VehicleEventCodeResponse(SQLModel):
    code: str = Field(max_length=12)
    description: str = Field(max_length=40)
    severity: EventSeverity
    
    model_config = {"from_attributes": True}