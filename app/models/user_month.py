"""User Month model module."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import table_registry


@table_registry.mapped_as_dataclass
class UserMonth:
    """User Month model."""

    __tablename__ = "user_month"

    id_user_fk: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True
    )
    id_month_fk: Mapped[int] = mapped_column(
        ForeignKey("month.id"), primary_key=True
    )

    user: Mapped["User"] = relationship("User", back_populates="user_months")
    month: Mapped["Month"] = relationship(
        "Month", back_populates="user_months"
    )
