from pydantic import BaseModel, ConfigDict


class IncomeSchema(BaseModel):
    name: str
    amount: float
    id_member_fk: int


class IncomePublic(BaseModel):
    id: int
    name: str
    amount: float
    id_member_fk: int

    model_config = ConfigDict(from_attributes=True)


class IncomeList(BaseModel):
    incomes: list[IncomePublic]
