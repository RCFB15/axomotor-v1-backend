from uuid import UUID
from datetime import datetime, date, timedelta
from typing import Optional

from pydantic import Field, computed_field
from sqlmodel import SQLModel

from core.config import settings
from models.enums import LicenseClass

class DriverCreate(SQLModel):
    user_id: UUID
    license_number: str = Field(max_length=20)
    license_class: LicenseClass
    license_iss_date: date
    license_exp_date: date

class DriverUpdate(SQLModel):
    license_number: Optional[str] = Field(default=None, max_length=20)
    license_class: Optional[LicenseClass] = Field(default=None)
    license_iss_date: Optional[date] = Field(default=None)
    license_exp_date: Optional[date] = Field(default=None)
    is_enabled: Optional[bool] = None

class DriverResponse(SQLModel):
    driver_id: UUID
    user_id: UUID
    telegram_user_id: Optional[int]
    license_number: str = Field(max_length=20)
    license_class: LicenseClass
    license_iss_date: date
    license_exp_date: date
    is_active: bool
    is_enabled: bool
    registered_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class LinkCreateResponse(SQLModel):
    token: str = Field(max_length=60)
    created_at: datetime

    @computed_field
    @property
    def expires_on(self) -> datetime:
        return self.created_at + timedelta(minutes=settings.LINKING_TOKEN_EXPIRE_MINUTES)

    @computed_field
    @property
    def url(self) -> str:
        return f"https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start={self.token}"

class DriverLink(SQLModel):
    token: str = Field(max_length=60)
    telegram_user_id: int
