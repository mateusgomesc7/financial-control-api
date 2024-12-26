from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.members import MemberPublic


class Pagination(BaseModel):
    count: int
    page: int
    per_page: int
    total: int
    total_pages: int


class NonEssentialExpenseSchema(BaseModel):
    name: str
    expected: float
    id_member_fk: int


class NonEssentialExpensePublic(BaseModel):
    id: int
    name: str
    expected: float
    id_user_fk: int
    member: Optional[MemberPublic]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NonEssentialExpensePaginated(BaseModel):
    items: list[NonEssentialExpensePublic]
    pagination: Pagination


class NonEssentialExpenseList(BaseModel):
    non_essential_expenses: list[NonEssentialExpensePublic]
