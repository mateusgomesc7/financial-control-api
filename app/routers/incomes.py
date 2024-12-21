"""Income router."""

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models.income import Income
from app.models.member import Member
from app.models.user import User
from app.schemas.incomes import IncomePublic, IncomeSchema
from app.security import get_current_user

router = APIRouter(prefix="/incomes", tags=["incomes"])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=IncomePublic)
def create_income(
    income: IncomeSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Create a new income."""
    member = session.execute(
        select(Member).filter(Member.id == income.id_member_fk)
    ).scalar()

    if not member:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Member not found",
        )

    if member.id_user_fk != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Member not found",
        )

    db_income = Income(
        name=income.name,
        amount=income.amount,
        id_member_fk=income.id_member_fk,
    )

    session.add(db_income)
    session.commit()
    session.refresh(db_income)

    return db_income
