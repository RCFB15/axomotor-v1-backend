import uuid
from datetime import datetime, date, timezone
from typing import Optional, List, TYPE_CHECKING

import sqlalchemy as sa
from sqlmodel import SQLModel, Field, Relationship
from models.enums import LicenseClass

if TYPE_CHECKING:
    from models.user import User
    from models.trip import Trip
    from models.linking_token import LinkingToken

class Driver(SQLModel, table=True):
    __tablename__ = 'drivers'

    driver_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key='users.user_id', index=True, unique=True)
    telegram_user_id: Optional[int] = Field(default=None)
    license_number: str = Field(index=True, max_length=20)
    license_class: LicenseClass
    license_iss_date: date
    license_exp_date: date
    is_active: bool = Field(default=False)
    is_enabled: bool = Field(default=True)
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            'onupdate': sa.func.now(),
            'server_default': sa.func.now(),
        }
    )

    user: Optional['User'] = Relationship(back_populates='driver')
    trips: List['Trip'] = Relationship(
        back_populates='driver',
        sa_relationship_kwargs={'cascade': 'all, delete-orphan'}
    )
    linking_tokens: List['LinkingToken'] = Relationship(
        back_populates='driver',
        sa_relationship_kwargs={'cascade': 'all, delete-orphan'}
    )
