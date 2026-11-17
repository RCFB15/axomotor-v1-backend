import asyncio
import logging
import uuid

from aiomqtt import Client, Message
from geoalchemy2.elements import WKTElement
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from db.database import get_session
import models
from models import TripPosition, VehicleEvent
from .schemas import TripPositionRegister, VehicleEventRegister

# Configuración de logger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# Funciones auxiliares

def parse_uuid(value: str):
    try:
        return uuid.UUID(value)
    except ValueError:
        return None

def new_db_session():
    return next(get_session())

# Procesadores de mensajes recibidos

async def process_position(trip_id: uuid.UUID, payload_bytes: bytes):
    try:
        data = TripPositionRegister.model_validate_json(payload_bytes)
    except ValidationError as e:
        logger.warning(f"Invalid trip position received from {trip_id}")
        return

    point_wkt = f"POINT({data.longitude} {data.latitude})"
    new_entry = TripPosition(
        trip_id=trip_id,
        position=WKTElement(point_wkt, srid=4326),
        speed=data.speed,
        registered_at=data.registered_at
    )

    session = new_db_session()
    session.add(new_entry)

    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        logger.warning(f"Failed to register position received from {trip_id}")

async def process_event(vehicle_id: uuid.UUID, payload_bytes: bytes):
    try:
        data = VehicleEventRegister.model_validate_json(payload_bytes)
    except ValidationError as e:
        logger.warning(f"Invalid event from {vehicle_id}")
        return

    point_wkt = f"POINT({data.longitude} {data.latitude})"
    new_entry = VehicleEvent(
        vehicle_id=vehicle_id,
        position=WKTElement(point_wkt, srid=4326),
        code=data.code,
        additional_data=data.additional_data,
        registered_at=data.registered_at
    )

    session = new_db_session()
    session.add(new_entry)

    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        logger.warning(f"Failed to register event received from {vehicle_id}")

async def process_message(message: Message):
    topic = message.topic.value
    if topic.startswith("trips/"):
        trip_id = parse_uuid(topic.split("/")[1])
        if trip_id is None:
            logger.warning("Invalid Trip Id")
            return

        if topic.endswith("/position"):
            await process_position(trip_id, message.payload)
    elif topic.startswith("vehicles/"):
        vehicle_id = parse_uuid(topic.split("/")[1])
        if vehicle_id is None:
            logger.warning("Invalid Vehicle Id")
            return

        if topic.endswith("/event"):
            await process_event(vehicle_id, message.payload)

# Bucle principal que recibe mensajes en los tópicos suscritos

async def main():
    async with Client("127.0.0.1") as client:
        await client.subscribe("trips/+/position")
        await client.subscribe("trips/+/incident")
        await client.subscribe("vehicles/+/event")
        await client.subscribe("vehicles/+/ack")

        async for message in client.messages:
            await process_message(message)

# Punto de entrada principal

if __name__ == "__main__":
    logger.info("MQTT Consumer started!")
    asyncio.run(main())
