from typing import Optional
from enum import Enum
from pydantic import Field
from sqlmodel import SQLModel

class IncidentSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class IncidentCodeCreate(SQLModel):
    code: str = Field(max_length=12)
    description: str = Field(max_length=40)
    severity: IncidentSeverity

class IncidentCodeUpdate(SQLModel):
    description: Optional[str] = Field(default=None, max_length=40)
    severity: Optional[IncidentSeverity] = Field(default=None)

class IncidentCodeResponse(SQLModel):
    code: str = Field(max_length=12)
    description: str = Field(max_length=40)
    severity: IncidentSeverity
    
    model_config = {"from_attributes": True}