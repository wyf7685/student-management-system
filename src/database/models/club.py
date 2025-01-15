from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base


class Club(Base):
    club_id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
