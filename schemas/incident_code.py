from pydantic import Field
from sqlmodel import SQLModel

from models.enums import SeverityLevel

class IncidentCodeResponse(SQLModel):
    code: str = Field(max_length=12)
    description: str = Field(max_length=40)
    severity: SeverityLevel

    model_config = {"from_attributes": True}
