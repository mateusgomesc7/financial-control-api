"""Member model module."""

from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

from app.models.base import table_registry


@table_registry.mapped_as_dataclass
class Member:
    """Member model."""

    __tablename__ = "member"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    id_user_fk: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=now(), onupdate=now()
    )
