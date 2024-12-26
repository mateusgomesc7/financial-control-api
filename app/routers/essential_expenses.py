"""Essential Expense router."""

from http import HTTPStatus
from math import ceil
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.database import get_session
from app.models.essential_expense import EssentialExpense
from app.models.member import Member
from app.models.user import User
from app.schemas.essential_expenses import (
    EssentialExpensePaginated,
    EssentialExpensePublic,
    EssentialExpenseSchema,
)
from app.schemas.utils import Message
from app.security import get_current_user

router = APIRouter(prefix="/essential-expenses", tags=["essential expenses"])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    "/", status_code=HTTPStatus.CREATED, response_model=EssentialExpensePublic
)
def create_essential_expense(
    essential_expense: EssentialExpenseSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Create a new essential expense."""
    member = session.execute(
        select(Member).filter(Member.id == essential_expense.id_member_fk)
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

    db_essential_expense = EssentialExpense(
        name=essential_expense.name,
        expected=essential_expense.expected,
        id_user_fk=current_user.id,
        id_member_fk=essential_expense.id_member_fk,
        member=member,
    )

    session.add(db_essential_expense)
    session.commit()
    session.refresh(db_essential_expense)

    db_essential_expense.member = member

    return db_essential_expense


@router.get("/", response_model=EssentialExpensePaginated)
def get_essential_expenses_paginated(
    session: T_Session,
    current_user: T_CurrentUser,
    page: int = 1,
    per_page: int = 10,
    name: str = None,
):
    """Get all essential expenses."""
    query = select(EssentialExpense).filter(
        EssentialExpense.id_user_fk == current_user.id
    )

    if name:
        query = query.filter(EssentialExpense.name.ilike(f"%{name}%"))

    total = session.scalar(select(func.count()).select_from(query.subquery()))

    offset = (page - 1) * per_page

    items = (
        session.execute(
            query.options(selectinload(EssentialExpense.member))
            .order_by(EssentialExpense.updated_at.desc())
            .limit(per_page)
            .offset(offset)
        )
        .scalars()
        .all()
    )

    total_pages = ceil(total / per_page) if total > 0 else 1

    return {
        "items": items,
        "pagination": {
            "count": len(items),
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        },
    }


@router.get("/{essential_expense_id}", response_model=EssentialExpenseSchema)
def get_essential_expense(
    essential_expense_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Get a single essential expense."""
    essential_expense = session.execute(
        select(EssentialExpense)
        .filter(EssentialExpense.id == essential_expense_id)
        .filter(EssentialExpense.id_user_fk == current_user.id)
    ).scalar()

    if not essential_expense:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Essential expense not found",
        )

    return essential_expense


@router.put("/{essential_expense_id}", response_model=EssentialExpensePublic)
def update_essential_expense(
    essential_expense_id: int,
    essential_expense: EssentialExpenseSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Update an essential expense."""
    db_essential_expense = session.execute(
        select(EssentialExpense)
        .where(EssentialExpense.id == essential_expense_id)
        .options(joinedload(EssentialExpense.member))
    ).scalar()

    if not db_essential_expense:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Essential expense not found",
        )

    if db_essential_expense.id_user_fk != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You don't have permission to update this essential expense",
        )

    db_essential_expense.name = essential_expense.name
    db_essential_expense.expected = essential_expense.expected
    db_essential_expense.id_member_fk = essential_expense.id_member_fk

    session.commit()
    session.refresh(db_essential_expense)

    return db_essential_expense


@router.delete("/{essential_expense_id}", response_model=Message)
def delete_essential_expense(
    essential_expense_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Delete an essential expense."""
    db_essential_expense = session.get(EssentialExpense, essential_expense_id)

    if not db_essential_expense:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Essential expense not found",
        )

    if db_essential_expense.id_user_fk != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You don't have permission to delete this essential expense",
        )

    session.delete(db_essential_expense)
    session.commit()

    return {"message": "Essential expense deleted successfully"}
