import uuid
from datetime import datetime, timezone
from typing import Optional, Any, TYPE_CHECKING
from decimal import Decimal

from sqlmodel import SQLModel, Field, Relationship, Column
from geoalchemy2 import Geography

if TYPE_CHECKING:
    from models.trip import Trip
    from models.vehicle import Vehicle

class Position(SQLModel, table=True):
    __tablename__ = 'positions'

    position_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    vehicle_id: uuid.UUID = Field(foreign_key='vehicles.vehicle_id', index=True)
    trip_id: Optional[uuid.UUID] = Field(default=None, foreign_key='trips.trip_id', index=True)
    # Se usa sa_column para definir el tipo espacial de PostGIS
    position: Any = Field(sa_column=Column(Geography('POINT', srid=4326)))
    speed: Decimal = Field(max_digits=5, decimal_places=2)
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    vehicle: Optional['Vehicle'] = Relationship(back_populates='positions')
    trip: Optional['Trip'] = Relationship(back_populates='positions')
