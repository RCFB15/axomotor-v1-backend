from uuid import UUID
from datetime import datetime, date
from typing import Optional

from pydantic import Field
from sqlmodel import SQLModel

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
