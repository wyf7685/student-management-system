from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base
from .course import Course
from .student import Student


class Grade(Base):
    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Student.student_id),
        nullable=False,
        primary_key=True,
    )
    course_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Course.course_id),
        nullable=False,
        primary_key=True,
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    term: Mapped[str] = mapped_column(String(256), nullable=False)
