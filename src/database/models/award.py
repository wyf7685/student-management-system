import datetime

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base
from .student import Student


class Award(Base):
    award_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Student.student_id),
        nullable=False,
    )
    award_name: Mapped[str] = mapped_column(String, nullable=False)
    award_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
