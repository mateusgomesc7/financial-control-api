"""Month Non Essential Expense model module."""

from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import table_registry


@table_registry.mapped_as_dataclass
class MonthNonEssentialExpense:
    """Month Non Essential Expense model."""

    __tablename__ = "month_non_essential_expense"

    id_month_fk: Mapped[int] = mapped_column(ForeignKey("month.id"))
    id_non_essential_expense_fk: Mapped[int] = mapped_column(
        ForeignKey("non_essential_expense.id"), primary_key=True
    )
    expected: Mapped[float] = mapped_column(DECIMAL(10, 2))
    paid: Mapped[float] = mapped_column(DECIMAL(10, 2))
