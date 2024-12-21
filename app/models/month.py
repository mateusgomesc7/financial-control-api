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
    created_at: Mapped[datetime] = mapped_column()
