import secrets
from typing import Annotated

from fastapi import Depends, Header, Security, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import JWTError, jwt
from sqlmodel import Session, select

from core.config import settings
from db.database import get_session
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")
bot_key_header = APIKeyHeader(name="X-MQTT-CONSUMER-API-KEY", auto_error=False)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Cannot verify credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM],
        )
        username = payload.get("sub")
        if not isinstance(username, str) or not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception from None

    user = session.exec(
        select(User).where(User.username == username)
    ).first()

    if user is None:
        raise credentials_exception
    if not user.is_enabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User disabled",
        )

    return user

def verify_mqtt_consumer(
    api_key: Annotated[str | None, Security(bot_key_header)]
) -> bool:
    if not api_key or not secrets.compare_digest(api_key, settings.X_MQTT_CONSUMER_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )

    return True
