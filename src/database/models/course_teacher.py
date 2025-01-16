from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base
from .teacher import Teacher


class CourseTeacher(Base):
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tearcher_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Teacher.teacher_id),
        primary_key=True,
    )
    semester: Mapped[str] = mapped_column(String(50), nullable=False)
