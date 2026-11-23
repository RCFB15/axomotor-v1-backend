from uuid import UUID

from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy import func, cast
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select, col
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement

from api.v1.dependencies import get_current_user, verify_mqtt_consumer
from db.database import get_session
from models import Vehicle, User, Position, VehicleEvent, VehicleEventCode
from schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from schemas.position import PositionResponse
from schemas.vehicle_event import VehicleEventCreate, VehicleEventResponse

router = APIRouter()

@router.post(
    "/",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_vehicle(
    vehicle_data: VehicleCreate,
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> Vehicle:
    existing_vehicle = session.exec(
        select(Vehicle).where(
            (Vehicle.plate_number == vehicle_data.plate_number) |
            (Vehicle.reg_number == vehicle_data.reg_number) |
            (Vehicle.series_vin == vehicle_data.series_vin)
        )
    ).first()

    if existing_vehicle:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already another vehicle registered with the same information",
        )

    vehicle = Vehicle(
        plate_number = vehicle_data.plate_number,
        reg_number = vehicle_data.reg_number,
        series_vin = vehicle_data.series_vin,
        brand = vehicle_data.brand,
        model = vehicle_data.model,
        year = vehicle_data.year,
        type = vehicle_data.type,
        status = vehicle_data.status
    )

    session.add(vehicle)

    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already another vehicle registered with the same information",
        ) from None

    session.refresh(vehicle)
    return vehicle

@router.get("/", response_model=list[VehicleResponse])
def get_vehicles(
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> list[Vehicle]:
    return list(session.exec(select(Vehicle)).all())

@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(
    vehicle_id: UUID,
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> Vehicle:
    vehicle = session.exec(
        select(Vehicle).where(Vehicle.vehicle_id == vehicle_id)
    ).first()

    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )
    return vehicle

@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: UUID,
    vehicle_data: VehicleUpdate,
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> Vehicle:
    vehicle = session.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )

    update_data = vehicle_data.model_dump(exclude_unset=True)
    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="All fields cannot be null or empty",
        )

    if any(key in update_data for key in ['plate_number', 'reg_number', 'series_vin']):
        duplicate = session.exec(
            select(Vehicle).where(
                Vehicle.vehicle_id != vehicle_id,
                (Vehicle.plate_number == update_data.get('plate_number', vehicle.plate_number)) |
                (Vehicle.reg_number == update_data.get('reg_number', vehicle.reg_number)) |
                (Vehicle.series_vin == update_data.get('series_vin', vehicle.series_vin))
            )
        ).first()

        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="There is already another vehicle registered with the same information"
            )

    for field, value in update_data.items():
        setattr(vehicle, field, value)

    session.add(vehicle)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already another vehicle registered with the same information",
        ) from None

    session.refresh(vehicle)
    return vehicle

@router.get("/{vehicle_id}/positions", response_model=list[PositionResponse])
def get_positions(
    vehicle_id: UUID,
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
):
    return session.exec(
        select(
            Position.position_id,
            Position.vehicle_id,
            Position.trip_id,
            func.ST_AsGeoJSON(Position.position).label("geojson"),
            Position.speed,
            Position.registered_at
        ) # type: ignore
        .where(Position.vehicle_id == vehicle_id)
        .order_by(col(Position.registered_at).desc())
    ).all()

@router.get("/{vehicle_id}/events", response_model=list[VehicleEventResponse])
def get_events(
    vehicle_id: UUID,
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> list[VehicleEvent]:
    return list(session.exec(
        select(VehicleEvent)
            .where(VehicleEvent.vehicle_id == vehicle_id)
            .options(joinedload(VehicleEvent.info)) # type: ignore
            .order_by(col(VehicleEvent.registered_at).desc())
    ).all())

@router.post(
    "/{vehicle_id}/events",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_mqtt_consumer)]
)
def create_event(
    vehicle_id: UUID,
    event_data: VehicleEventCreate,
    session: Session = Depends(get_session),
):
    vehicle = session.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )

    info = session.get(VehicleEventCode, event_data.code)
    if info is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid event code"
        )

    event = VehicleEvent(
        code = event_data.code,
        vehicle_id = vehicle_id,
        additional_data=event_data.additional_data
    )

    if event_data.has_position:
        position_wkt = f"POINT({event_data.longitude} {event_data.latitude})"
        event.position=WKTElement(position_wkt, srid=4326)

    session.add(event)

    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Failed to register the event",
        ) from None

    return Response(status_code=status.HTTP_204_NO_CONTENT)
