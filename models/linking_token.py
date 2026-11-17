import uuid
import secrets
from datetime import datetime, timezone, timedelta
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from core.config import settings

if TYPE_CHECKING:
    from models.driver import Driver

class LinkingToken(SQLModel, table=True):
    __tablename__ = 'linking_tokens'

    token: str = Field(primary_key=True, default_factory=lambda: secrets.token_urlsafe(32), max_length=60)
    driver_id: uuid.UUID = Field(foreign_key='drivers.driver_id', index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    driver: Optional['Driver'] = Relationship(back_populates='linking_tokens')

    @property
    def is_valid(self):
        return datetime.now(timezone.utc) < (
            self.created_at + timedelta(minutes=settings.LINKING_TOKEN_EXPIRE_MINUTES)
        )
