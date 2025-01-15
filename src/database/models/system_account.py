from typing import Literal

from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base


class SystemAccount(Base):
    id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    role: Mapped[Literal["Student", "Teacher", "Admin"]] = mapped_column(
        String,
        CheckConstraint("role IN ('Student', 'Teacher', 'Admin')"),
        nullable=False,
    )
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
