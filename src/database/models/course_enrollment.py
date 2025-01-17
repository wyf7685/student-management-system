from enum import Enum
from typing import Literal

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db_config import Base
from .course import Course
from .student import Student


class EnrollmentsStatusCode(int, Enum):
    Enrolled = 1
    Completed = 2
    Dropped = 3
    InProgress = 4
    NotEnrolled = 5
    Pending = 6
    Withdrawn = 7
    Failed = 8


type EnrollmentsStatusName = Literal[
    "已选修",
    "已完成",
    "已放弃",
    "选修中",
    "未选修",
    "待选修",
    "已退课",
    "选课失败",
]

COURSE_STATUS_NAME: dict[EnrollmentsStatusCode, EnrollmentsStatusName] = {
    EnrollmentsStatusCode.Enrolled: "已选修",
    EnrollmentsStatusCode.Completed: "已完成",
    EnrollmentsStatusCode.Dropped: "已放弃",
    EnrollmentsStatusCode.InProgress: "选修中",
    EnrollmentsStatusCode.NotEnrolled: "未选修",
    EnrollmentsStatusCode.Pending: "待选修",
    EnrollmentsStatusCode.Withdrawn: "已退课",
    EnrollmentsStatusCode.Failed: "选课失败",
}


class CourseEnrollment(Base):
    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Student.student_id),
        primary_key=True,
    )
    course_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Course.course_id),
        primary_key=True,
    )
    semester: Mapped[str] = mapped_column(String(50), nullable=False)
    course_status: Mapped[EnrollmentsStatusCode] = mapped_column(
        Integer,
        CheckConstraint("course_status IN (1, 2, 3, 4, 5, 6, 7, 8)"),
        nullable=False,
    )

    @property
    def course_status_name(self) -> EnrollmentsStatusName:
        return COURSE_STATUS_NAME[self.course_status]
