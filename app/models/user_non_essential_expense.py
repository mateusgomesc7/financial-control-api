"""User Non Essential Expense model module."""

from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import table_registry


@table_registry.mapped_as_dataclass
class UserNonEssentialExpense:
    """User Non Essential Expense model."""

    __tablename__ = "user_non_essential_expense"

    id_user_fk: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True
    )
    id_non_essential_expense_fk: Mapped[int] = mapped_column(
        ForeignKey("non_essential_expense.id"), primary_key=True
    )
    id_month_fk: Mapped[int] = mapped_column(ForeignKey("month.id"))
    expected: Mapped[float] = mapped_column(DECIMAL(10, 2))
    paid: Mapped[float] = mapped_column(DECIMAL(10, 2))

    user: Mapped["User"] = relationship(
        "User", back_populates="user_non_essential_expenses"
    )
    non_essential_expense: Mapped["NonEssentialExpense"] = relationship(
        "NonEssentialExpense", back_populates="user_non_essential_expenses"
    )
    month: Mapped["Month"] = relationship(
        "Month", back_populates="user_non_essential_expenses"
    )
