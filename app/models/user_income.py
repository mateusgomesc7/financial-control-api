"""User Income model module."""

from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import table_registry


@table_registry.mapped_as_dataclass
class UserIncome:
    """User Income model."""

    __tablename__ = "user_income"

    id_user_fk: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True
    )
    id_income_fk: Mapped[int] = mapped_column(
        ForeignKey("income.id"), primary_key=True
    )
    id_month_fk: Mapped[int] = mapped_column(ForeignKey("month.id"))
    amount: Mapped[float] = mapped_column(DECIMAL(10, 2))

    user: Mapped["User"] = relationship("User", back_populates="user_incomes")
    income: Mapped["Income"] = relationship(
        "Income", back_populates="user_incomes"
    )
    month: Mapped["Month"] = relationship(
        "Month", back_populates="user_incomes"
    )
