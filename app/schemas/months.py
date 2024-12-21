from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MonthSchema(BaseModel):
    created_at: datetime


class MonthPublic(BaseModel):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MonthList(BaseModel):
    months: list[MonthPublic]
