from typing import ClassVar, Literal

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base
from .student import Student
from .teacher import Teacher


class SystemAccount(Base):
    __table_args__: ClassVar = (
        CheckConstraint("role != 'Student' OR student_id IS NOT NULL"),
        CheckConstraint("role != 'Teacher' OR teacher_id IS NOT NULL"),
        CheckConstraint("role != 'Admin' OR admin_id IS NOT NULL"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    role: Mapped[Literal["Student", "Teacher", "Admin"]] = mapped_column(
        String(256),
        CheckConstraint("role IN ('Student', 'Teacher', 'Admin')"),
        nullable=False,
    )
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    salt: Mapped[str] = mapped_column(String(256), nullable=False)
    student_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(Student.student_id),
        nullable=True,
    )
    teacher_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(Teacher.teacher_id),
        nullable=True,
    )
    admin_id: Mapped[str | None] = mapped_column(
        String(256),
        nullable=True,
    )

    @property
    def user_id(self) -> str:
        match self.role:
            case "Student":
                return str(self.student_id)
            case "Teacher":
                return str(self.teacher_id)
            case "Admin":
                return str(self.admin_id)
            case _:
                raise ValueError("Invalid role")

    @user_id.setter
    def user_id(self, value: str):
        match self.role:
            case "Student":
                self.student_id = int(value)
            case "Teacher":
                self.teacher_id = int(value)
            case "Admin":
                self.admin_id = value
            case _:
                raise ValueError("Invalid role")
