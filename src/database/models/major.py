from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base
from .college import College


class Major(Base):
    major_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    college_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(College.college_id),
        nullable=False,
    )
