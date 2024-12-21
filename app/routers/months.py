"""Mounth router."""

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_session
from app.models.month import Month
from app.models.user import User
from app.models.user_month import UserMonth
from app.schemas.months import MonthPublic, MonthSchema

router = APIRouter(prefix="/months", tags=["months"])

T_Session = Annotated[Session, Depends(get_session)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=MonthPublic)
def create_month(month: MonthSchema, session: T_Session):
    db_month = Month(
        created_at=month.created_at,
    )

    session.add(db_month)
    session.flush()

    users = session.query(User).all()

    user_month_relations = [
        UserMonth(id_user_fk=user.id, id_month_fk=db_month.id)
        for user in users
    ]
    session.add_all(user_month_relations)

    session.commit()
    session.refresh(db_month)

    return db_month
