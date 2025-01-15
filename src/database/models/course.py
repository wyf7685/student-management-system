from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base


class Course(Base):
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    credits: Mapped[int] = mapped_column(Integer, nullable=False)
