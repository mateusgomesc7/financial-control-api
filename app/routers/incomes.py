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
from app.schemas.incomes import IncomeList, IncomePublic, IncomeSchema
from app.schemas.utils import Message
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
        id_user_fk=current_user.id,
        id_member_fk=income.id_member_fk,
    )

    session.add(db_income)
    session.commit()
    session.refresh(db_income)

    return db_income


@router.get("/", response_model=IncomeList)
def get_incomes(
    session: T_Session,
    current_user: T_CurrentUser,
    limit: int = 10,
    offset: int = 0,
):
    """Get all incomes."""
    incomes = session.execute(
        select(Income)
        .filter(Income.id_user_fk == current_user.id)
        .order_by(Income.updated_at.desc())
        .limit(limit)
        .offset(offset)
    ).scalars()

    return {"incomes": incomes}


@router.get("/{income_id}", response_model=IncomePublic)
def get_income(
    income_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Get a single income."""
    income = session.execute(
        select(Income)
        .filter(Income.id == income_id)
        .filter(Income.id_user_fk == current_user.id)
    ).scalar()

    if not income:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Income not found",
        )

    return income


@router.put("/{income_id}", response_model=IncomePublic)
def update_income(
    income_id: int,
    income: IncomeSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Update an income."""
    db_income = session.get(Income, income_id)

    if not db_income:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Income not found",
        )

    if db_income.id_user_fk != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You don't have permission to update this income",
        )

    db_income.name = income.name
    db_income.amount = income.amount
    db_income.id_member_fk = income.id_member_fk

    session.commit()
    session.refresh(db_income)

    return db_income


@router.delete("/{income_id}", response_model=Message)
def delete_income(
    income_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Delete an income."""
    db_income = session.get(Income, income_id)

    if not db_income:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Income not found",
        )

    if db_income.id_user_fk != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You don't have permission to delete this income",
        )

    session.delete(db_income)
    session.commit()

    return {"message": "Income deleted successfully"}
