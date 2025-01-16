from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base
from .tearcher import Tearcher


class CourseTeacher(Base):
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tearcher_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Tearcher.tearcher_id),
        primary_key=True,
    )
    semester: Mapped[str] = mapped_column(String(50), nullable=False)
