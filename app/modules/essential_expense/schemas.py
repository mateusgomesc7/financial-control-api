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


class EssentialExpenseSchema(BaseModel):
    name: str
    expected: float
    id_member_fk: int


class EssentialExpensePublic(BaseModel):
    id: int
    name: str
    expected: float
    id_user_fk: int
    member: Optional[MemberPublic]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EssentialExpensePaginated(BaseModel):
    items: list[EssentialExpensePublic]
    pagination: Pagination


class EssentialExpenseList(BaseModel):
    essential_expenses: list[EssentialExpensePublic]
