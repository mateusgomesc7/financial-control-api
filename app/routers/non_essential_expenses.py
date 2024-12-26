"""Non Essential Expense router."""

from http import HTTPStatus
from math import ceil
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.database import get_session
from app.models.member import Member
from app.models.non_essential_expense import NonEssentialExpense
from app.models.user import User
from app.schemas.non_essential_expenses import (
    NonEssentialExpensePaginated,
    NonEssentialExpensePublic,
    NonEssentialExpenseSchema,
)
from app.schemas.utils import Message
from app.security import get_current_user

router = APIRouter(
    prefix="/non-essential-expenses", tags=["non essential expenses"]
)

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    response_model=NonEssentialExpensePublic,
)
def create_non_essential_expense(
    non_essential_expense: NonEssentialExpenseSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Create a new non essential expense."""
    member = session.execute(
        select(Member).filter(Member.id == non_essential_expense.id_member_fk)
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

    db_non_essential_expense = NonEssentialExpense(
        name=non_essential_expense.name,
        expected=non_essential_expense.expected,
        id_user_fk=current_user.id,
        id_member_fk=non_essential_expense.id_member_fk,
        member=member,
    )

    session.add(db_non_essential_expense)
    session.commit()
    session.refresh(db_non_essential_expense)

    db_non_essential_expense.member = member

    return db_non_essential_expense


@router.get("/", response_model=NonEssentialExpensePaginated)
def get_non_essential_expenses_paginated(
    session: T_Session,
    current_user: T_CurrentUser,
    page: int = 1,
    per_page: int = 10,
    name: str = None,
):
    """Get all non essential expenses."""
    query = select(NonEssentialExpense).filter(
        NonEssentialExpense.id_user_fk == current_user.id
    )

    if name:
        query = query.filter(NonEssentialExpense.name.ilike(f"%{name}%"))

    total = session.scalar(select(func.count()).select_from(query.subquery()))

    offset = (page - 1) * per_page

    items = (
        session.execute(
            query.options(selectinload(NonEssentialExpense.member))
            .order_by(NonEssentialExpense.updated_at.desc())
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


@router.get(
    "/{non_essential_expense_id}", response_model=NonEssentialExpenseSchema
)
def get_non_essential_expense(
    non_essential_expense_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Get a single non essential expense."""
    non_essential_expense = session.execute(
        select(NonEssentialExpense)
        .filter(NonEssentialExpense.id == non_essential_expense_id)
        .filter(NonEssentialExpense.id_user_fk == current_user.id)
    ).scalar()

    if not non_essential_expense:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Non essential expense not found",
        )

    return non_essential_expense


@router.put(
    "/{non_essential_expense_id}", response_model=NonEssentialExpensePublic
)
def update_non_essential_expense(
    non_essential_expense_id: int,
    non_essential_expense: NonEssentialExpenseSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Update an non essential expense."""
    db_non_essential_expense = session.execute(
        select(NonEssentialExpense)
        .where(NonEssentialExpense.id == non_essential_expense_id)
        .options(joinedload(NonEssentialExpense.member))
    ).scalar()

    if not db_non_essential_expense:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Non Essential expense not found",
        )

    if db_non_essential_expense.id_user_fk != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You don't have permission to update this non essential expense",
        )

    db_non_essential_expense.name = non_essential_expense.name
    db_non_essential_expense.expected = non_essential_expense.expected
    db_non_essential_expense.id_member_fk = non_essential_expense.id_member_fk

    session.commit()
    session.refresh(db_non_essential_expense)

    return db_non_essential_expense


@router.delete("/{non_essential_expense_id}", response_model=Message)
def delete_non_essential_expense(
    non_essential_expense_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    """Delete an non essential expense."""
    db_non_essential_expense = session.get(
        NonEssentialExpense, non_essential_expense_id
    )

    if not db_non_essential_expense:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Non essential expense not found",
        )

    if db_non_essential_expense.id_user_fk != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You don't have permission to delete this non essential expense",
        )

    session.delete(db_non_essential_expense)
    session.commit()

    return {"message": "Non essential expense deleted successfully"}
