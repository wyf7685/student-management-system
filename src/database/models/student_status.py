import datetime
from enum import Enum
from typing import Literal

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base
from .student import Student


class StudentStatusCode(int, Enum):
    ACTIVE = 1
    RETAIN = 2
    TRANSFER = 3
    GRADUATED = 4
    DROPPED = 5


type StudentStatusName = Literal["在读", "留级", "转专业", "毕业", "退学"]

STUDENT_STATUS_NAME: dict[StudentStatusCode, StudentStatusName] = {
    StudentStatusCode.ACTIVE: "在读",
    StudentStatusCode.RETAIN: "留级",
    StudentStatusCode.TRANSFER: "转专业",
    StudentStatusCode.GRADUATED: "毕业",
    StudentStatusCode.DROPPED: "退学",
}

class StudentStatus(Base):
    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Student.student_id),
        primary_key=True,
    )
    status_code: Mapped[StudentStatusCode] = mapped_column(
        Integer,
        CheckConstraint("status_code IN (1, 2, 3, 4, 5)"),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(String, nullable=True)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    @property
    def status_name(self) -> StudentStatusName:
        return STUDENT_STATUS_NAME[self.status_code]
