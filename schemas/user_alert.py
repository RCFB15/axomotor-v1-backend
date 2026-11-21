from typing import Optional, Any, Dict
from uuid import UUID
from datetime import datetime

from pydantic import Field
from sqlmodel import SQLModel

from models.enums import AlertType

class UserAlertUpdate(SQLModel):
    is_read: bool

class UserAlertResponse(SQLModel):
    alert_id: UUID
    user_id: UUID
    title: str = Field(max_length=80)
    content: Optional[str] = Field(max_length=240)
    type: AlertType
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}
