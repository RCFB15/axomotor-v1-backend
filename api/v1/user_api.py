from datetime import timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from api.v1.dependencies import get_current_user
from core.config import settings
from core.security import create_access_token, get_password_hash, verify_password
from db.database import get_session
from models.user import User
from schemas.token import Token
from schemas.user import UserCreate, UserResponse, UserUpdate, UserUpdatePassword

router = APIRouter()

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> Token:
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if user is None or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_enabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User disabled",
        )

    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
    )
    return Token(access_token=access_token)

@router.get("/me", response_model=UserResponse)
def get_logged_user(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
) -> User:
    existing_user = session.exec(
        select(User).where(
            (User.username == user_data.username) |
            (User.email == user_data.email) |
            (User.phone_number == user_data.phone_number)
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email or phone number already registered",
        )

    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        username=user_data.username,
        phone_number=user_data.phone_number,
        role=user_data.role,
        hashed_password=get_password_hash(user_data.password),
    )

    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already another user registered with the same information",
        ) from None

    session.refresh(user)
    return user

@router.get("/", response_model=list[UserResponse])
def get_users(
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> list[User]:
    return list(session.exec(select(User)).all())

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> User:
    user = session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user),
) -> User:
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    update_data = user_update.model_dump(exclude_unset=True)
    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="All fields cannot be null or empty",
        )

    if "username" in update_data or "email" in update_data or "phone_number" in update_data:
        duplicate = session.exec(
            select(User).where(
                User.user_id != user_id,
                (User.username == update_data.get("username", user.username)) |
                (User.email == update_data.get("email", user.email)) |
                (User.phone_number == update_data.get("phone_number", user.phone_number))
            )
        ).first()

        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email or phone number already registered",
            )

    for field, value in update_data.items():
        setattr(user, field, value)

    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already another user registered with the same information",
        ) from None

    session.refresh(user)
    return user

@router.put("/{user_id}/change_password", status_code=status.HTTP_204_NO_CONTENT)
def update_password(
    user_id: UUID,
    form_data: UserUpdatePassword,
    session: Session = Depends(get_session),
    _current_user: User = Depends(get_current_user)
):
    user = session.get(User, user_id)
    if user is None or not verify_password(
        form_data.current_password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid username or password",
        )

    if not user.is_enabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User disabled",
        )

    user.hashed_password = get_password_hash(form_data.new_password)
    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot update password",
        ) from None
