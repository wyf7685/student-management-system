from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base
from .major import Major


class Class(Base):
    class_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    major_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Major.major_id),
        nullable=False,
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False)
