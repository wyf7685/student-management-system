from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base


class College(Base):
    college_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
