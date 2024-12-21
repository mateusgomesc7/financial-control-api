"""Essential Expense model module."""

from datetime import datetime

from sqlalchemy import DECIMAL, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.models.base import table_registry


@table_registry.mapped_as_dataclass
class EssentialExpense:
    """Essential Expense model."""

    __tablename__ = "essential_expense"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    id_member_fk: Mapped[int] = mapped_column(
        ForeignKey("member.id", ondelete="SET NULL"), nullable=True
    )
    expected: Mapped[float] = mapped_column(DECIMAL(10, 2))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=now(), onupdate=now()
    )

    user_essential_expenses: Mapped[list["UserEssentialExpense"]] = (
        relationship(
            "UserEssentialExpense", back_populates="essential_expense"
        )
    )
