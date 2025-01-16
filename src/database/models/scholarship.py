from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base
from .student import Student


class Scholarship(Base):
    scholarship_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    scholarship_name: Mapped[str] = mapped_column(String, nullable=False)
    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Student.student_id),
        nullable=False,
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    date_awarded: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
