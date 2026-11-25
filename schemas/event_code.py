from pydantic import Field
from sqlmodel import SQLModel

from models.enums import SeverityLevel, EventCategory

class EventCodeResponse(SQLModel):
    code: str = Field(max_length=12)
    description: str = Field(max_length=40)
    severity: SeverityLevel
    category: EventCategory
    severity: SeverityLevel
    is_enabled: bool

    model_config = {"from_attributes": True}
