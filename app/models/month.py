"""Month model module."""

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.models.base import table_registry


@table_registry.mapped_as_dataclass
class Month:
    """Month model."""

    __tablename__ = "month"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=now()
    )

    user_months: Mapped[list["UserMonth"]] = relationship(
        "UserMonth", back_populates="month"
    )
    user_incomes: Mapped[list["UserIncome"]] = relationship(
        "UserIncome", back_populates="month"
    )
    user_essential_expenses: Mapped[list["UserEssentialExpense"]] = (
        relationship("UserEssentialExpense", back_populates="month")
    )
    user_non_essential_expenses: Mapped[list["UserNonEssentialExpense"]] = (
        relationship("UserNonEssentialExpense", back_populates="month")
    )
