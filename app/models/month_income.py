"""Month Income model module."""

from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import table_registry


@table_registry.mapped_as_dataclass
class MonthIncome:
    """Month Income model."""

    __tablename__ = "month_income"

    id_month_fk: Mapped[int] = mapped_column(ForeignKey("month.id"))
    id_income_fk: Mapped[int] = mapped_column(
        ForeignKey("income.id"), primary_key=True
    )
    amount: Mapped[float] = mapped_column(DECIMAL(10, 2))
