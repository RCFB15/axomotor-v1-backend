from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from models.enums import SeverityLevel, EventCategory, EventType

if TYPE_CHECKING:
    from models.vehicle_event import VehicleEvent
    from models.incident import Incident

class EventCode(SQLModel, table=True):
    __tablename__ = 'event_codes'

    code: str = Field(primary_key=True, max_length=12)
    description: str = Field(index=True, unique=True, max_length=40)
    type: EventType
    category: EventCategory
    severity: SeverityLevel
    is_enabled: bool = Field(default=True)

    events: List['VehicleEvent'] = Relationship(
        back_populates='info',
        sa_relationship_kwargs={'cascade': 'all, delete-orphan'}
    )

    incidents: List['Incident'] = Relationship(
        back_populates='info',
        sa_relationship_kwargs={'cascade': 'all, delete-orphan'}
    )
