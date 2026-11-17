from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from api.v1.dependencies import get_current_user
from db.database import get_session
from models import Driver, User, UserRole
from schemas.driver import DriverCreate, DriverUpdate, DriverResponse, DriverLink, LinkCreateResponse

router = APIRouter()

@router.post(
    "/",
    response_model=DriverResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_driver(
    driver_data: DriverCreate,
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> Driver:
    user = session.get(User, driver_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    elif user.role != UserRole.driver:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User must be registered as driver",
        )

    existing_driver = session.exec(
        select(Driver).where(Driver.user_id == driver_data.user_id)
    ).first()

    if existing_driver:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered as driver",
        )

    driver = Driver(
        user_id = driver_data.user_id,
        license_number = driver_data.license_number,
        license_class = driver_data.license_class,
        license_iss_date = driver_data.license_iss_date,
        license_exp_date = driver_data.license_exp_date
    )

    session.add(driver)

    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already another driver registered with the same information",
        ) from None

    session.refresh(driver)
    return driver

@router.get("/", response_model=list[DriverResponse])
def get_drivers(
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> list[Driver]:
    return list(session.exec(select(Driver)).all())

@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(
    driver_id: UUID,
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> Driver:
    driver = session.get(Driver, driver_id)

    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found",
        )
    return driver

@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(
    driver_id: UUID,
    driver_data: DriverUpdate,
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> Driver:
    driver = session.get(Driver, driver_id)
    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found",
        )

    update_data = driver_data.model_dump(exclude_unset=True)
    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="All fields cannot be null or empty",
        )

    for field, value in update_data.items():
        setattr(driver, field, value)

    session.add(driver)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already another driver registered with the same information",
        ) from None

    session.refresh(driver)
    return driver
