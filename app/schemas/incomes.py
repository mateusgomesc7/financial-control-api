from datetime import datetime
from pydantic import BaseModel, ConfigDict


class IncomeSchema(BaseModel):
    name: str
    amount: float
    id_member_fk: int


class IncomePublic(BaseModel):
    id: int
    name: str
    amount: float
    id_user_fk: int
    id_member_fk: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IncomeList(BaseModel):
    incomes: list[IncomePublic]
