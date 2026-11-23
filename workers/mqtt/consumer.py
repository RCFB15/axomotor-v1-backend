import asyncio
import logging
import uuid
from aiohttp import ClientSession

from aiomqtt import Client, Message
from geoalchemy2.elements import WKTElement
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

import models
from db.database import get_session
from models import Position

from .schemas import PositionCreate
from .utils import parse_uuid
from .config import settings

# Constantes

BASE_TOPIC = "axomotor/v1/vehicles"

# Configuración de logger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

client_headers = {
    "X-MQTT-CONSUMER-API-KEY": settings.X_MQTT_CONSUMER_API_KEY,
    "content-type": "application/json"
}

def new_db_session():
    return next(get_session())

# Procesadores de mensajes recibidos

async def process_position(vehicle_id: uuid.UUID, payload_bytes: bytes):
    try:
        data = PositionCreate.model_validate_json(payload_bytes)
    except ValidationError as e:
        logger.warning(f"Failed to serialize trip position received from {vehicle_id}")
        return

    point_wkt = f"POINT({data.longitude} {data.latitude})"
    new_entry = Position(
        vehicle_id=vehicle_id,
        trip_id=data.trip_id,
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
        logger.warning(f"Failed to register position received from {vehicle_id}")

async def process_event(vehicle_id: str, payload_bytes: bytes, http: ClientSession):
    async with http.post(
        f"{settings.X_MQTT_CONSUMER_HOST}/api/v1/vehicles/{vehicle_id}/events",
        data=payload_bytes,
    ) as response:
        if not response.ok:
            body = await response.json()
            reason = body.get("detail")
            logger.warning(f"Failed to register event received from {vehicle_id}: {reason}")

async def process_incident(vehicle_id: uuid.UUID, payload_bytes: bytes, http: ClientSession):
    async with http.post(
        f"{settings.X_MQTT_CONSUMER_HOST}/api/v1/incidents/",
        data=payload_bytes,
    ) as response:
        if not response.ok:
            body = await response.json()
            reason = body.get("detail")
            logger.warning(f"Failed to register incident received from {vehicle_id}: {reason}")

async def process_message(message: Message, http: ClientSession):
    topic = message.topic.value.removeprefix(BASE_TOPIC)
    _, vehicle_id, level = topic.split("/")
    vehicle_uuid = parse_uuid(vehicle_id)

    if vehicle_uuid is None:
        logger.warning("Invalid Vehicle Identifier")
        return

    match level:
        case "position":
            await process_position(vehicle_uuid, message.payload)
        case "event":
            await process_event(vehicle_id, message.payload, http)
        case "incident":
            await process_incident(vehicle_uuid, message.payload, http)
        case "ack":
            pass

# Bucle principal que recibe mensajes en los tópicos suscritos

async def main():
    async with Client(
        settings.MQTT_CONSUMER_HOST,
        username=settings.MQTT_CONSUMER_USER,
        password=settings.MQTT_CONSUMER_PASSWORD
    ) as mqtt:
        await mqtt.subscribe(f"{BASE_TOPIC}/+/incident")
        await mqtt.subscribe(f"{BASE_TOPIC}/+/position")
        await mqtt.subscribe(f"{BASE_TOPIC}/+/event")
        #await client.subscribe(f"{BASE_TOPIC}/+/ack")

        async with ClientSession(headers=client_headers) as http:
            async for message in mqtt.messages:
                await process_message(message, http)

# Punto de entrada principal

if __name__ == "__main__":
    logger.info("MQTT Consumer started!")
    asyncio.run(main())
