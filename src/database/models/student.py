import datetime
from typing import Literal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base
from .class_ import Class
from .college import College
from .major import Major

PHONE_CHECK = "1" + "_" * 10


class Student(Base):
    student_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[Literal["F", "M"]] = mapped_column(
        String(1),
        CheckConstraint("gender IN ('F', 'M')"),
        nullable=False,
    )
    birth: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    phone: Mapped[str] = mapped_column(
        String(20),
        CheckConstraint(f"phone LIKE '{PHONE_CHECK}'"),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(100),
        CheckConstraint("email LIKE '%@%.%'"),
        nullable=False,
    )
    college_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(College.college_id),
        nullable=False,
    )
    major_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Major.major_id),
        nullable=False,
    )
    class_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Class.class_id),
        nullable=False,
    )
    enrollment_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
