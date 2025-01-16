import datetime
from typing import Literal

from sqlalchemy import CheckConstraint, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base


class Tearcher(Base):
    tearcher_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[Literal["F", "M"]] = mapped_column(
        String(1),
        CheckConstraint("gender IN ('F', 'M')"),
        nullable=False,
    )
    birth: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
