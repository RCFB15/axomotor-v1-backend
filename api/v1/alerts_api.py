from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlmodel import Session, col, select

from api.v1.common import PaginationDep, apply_update, commit_or_409, paginate
from api.v1.dependencies import get_current_user
from db.database import get_session
from models import User, UserAlert
from models.enums import AlertType
from schemas.user_alert import UserAlertResponse, UserAlertUpdate

router = APIRouter()


def _get_own_alert(session: Session, alert_id: UUID, user: User) -> UserAlert:
    alert = session.get(UserAlert, alert_id)
    if alert is None or alert.user_id != user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )
    return alert


@router.get("/", response_model=list[UserAlertResponse])
def get_alerts(
    response: Response,
    page: PaginationDep,
    is_read: Optional[bool] = None,
    alert_type: Optional[AlertType] = Query(default=None, alias="type"),
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[UserAlert]:
    statement = select(UserAlert).where(UserAlert.user_id == current_user.user_id)

    if is_read is not None:
        statement = statement.where(UserAlert.is_read == is_read)
    if alert_type is not None:
        statement = statement.where(UserAlert.type == alert_type)
    if from_date is not None:
        statement = statement.where(UserAlert.created_at >= from_date)
    if to_date is not None:
        statement = statement.where(UserAlert.created_at <= to_date)

    statement = statement.order_by(col(UserAlert.created_at).desc())
    return paginate(session, statement, page, response)


@router.put("/{alert_id}", response_model=UserAlertResponse)
def update_alert(
    alert_id: UUID,
    alert_data: UserAlertUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> UserAlert:
    alert = _get_own_alert(session, alert_id, current_user)
    apply_update(alert, alert_data)
    session.add(alert)
    commit_or_409(session, "The alert could not be updated")
    session.refresh(alert)
    return alert


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_alerts(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> None:
    alerts = session.exec(
        select(UserAlert).where(UserAlert.user_id == current_user.user_id)
    ).all()
    for alert in alerts:
        session.delete(alert)
    session.commit()


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(
    alert_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> None:
    alert = _get_own_alert(session, alert_id, current_user)
    session.delete(alert)
    session.commit()