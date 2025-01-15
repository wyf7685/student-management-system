from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base
from .club import Club
from .student import Student


class StudentClub(Base):
    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Student.student_id),
        primary_key=True,
    )
    club_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Club.club_id),
        primary_key=True,
    )
    role: Mapped[str] = mapped_column(String, nullable=False)
