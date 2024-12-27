from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.modules.member.schemas import MemberPublic


class Pagination(BaseModel):
    count: int
    page: int
    per_page: int
    total: int
    total_pages: int


class IncomeSchema(BaseModel):
    name: str
    amount: float
    id_member_fk: int


class IncomePublic(BaseModel):
    id: int
    name: str
    amount: float
    id_user_fk: int
    member: Optional[MemberPublic]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IncomePaginated(BaseModel):
    items: list[IncomePublic]
    pagination: Pagination


class IncomeList(BaseModel):
    incomes: list[IncomePublic]
