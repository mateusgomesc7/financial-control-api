"""Member router."""

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models.member import Member
from app.models.user import User
from app.schemas.members import MemberList, MemberPublic, MemberSchema
from app.schemas.utils import Message
from app.security import get_current_user

router = APIRouter(prefix="/members", tags=["members"])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=MemberPublic)
def create_member(
    member: MemberSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != member.id_user_fk:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You don't have permission to create a member for another user",
        )

    db_member = Member(
        name=member.name,
        id_user_fk=member.id_user_fk,
    )

    session.add(db_member)
    session.commit()
    session.refresh(db_member)

    return db_member


@router.get("/", response_model=MemberList)
def read_members(
    session: T_Session,
    limit: int = 10,
    offset: int = 0,
):
    members = session.scalars(select(Member).limit(limit).offset(offset))

    return {"members": members}


@router.put("/{member_id}", response_model=MemberPublic)
def update_member(
    member_id: int,
    member: MemberSchema,
    session: T_Session,
    current_user: User = Depends(get_current_user),
):
    db_member = session.get(Member, member_id)

    if not db_member:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Member not found",
        )

    if db_member.id_user_fk != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You don't have permission to update this member",
        )

    db_member.name = member.name
    db_member.id_user_fk = member.id_user_fk

    session.commit()
    session.refresh(db_member)

    return db_member


@router.delete("/{member_id}", response_model=Message)
def delete_member(
    member_id: int,
    session: T_Session,
    current_user: User = Depends(get_current_user),
):
    db_member = session.get(Member, member_id)

    if not db_member:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Member not found",
        )

    if db_member.id_user_fk != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You don't have permission to delete this member",
        )

    session.delete(db_member)
    session.commit()

    return {"message": "Member deleted successfully"}
