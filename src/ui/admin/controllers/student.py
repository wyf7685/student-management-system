# ruff: noqa: DTZ007

from datetime import datetime
from typing import Literal

from database import DBManager, Student

from ._base import BaseController, DBRollbackMixin, check_student_id


class StudentController(DBRollbackMixin, BaseController):
    def __init__(self) -> None:
        super().__init__()
        self.db = DBManager.student()

    def add(
        self,
        student_id: str,
        name: str,
        gender: Literal["F", "M"],
        birth: str,
        phone: str,
        email: str,
        college_id: str,
        major_id: str,
        class_id: str,
        enrollment_date: str,
    ) -> bool:
        try:
            # 验证数据
            if not all([name, gender, birth, phone, email]):
                return self.error("学生信息不完整")

            sid = check_student_id(student_id)

            # 检查是否已存在
            if self.db.exists_student(sid):
                return self.error("学号已存在")

            # 创建并保存
            student = Student(
                student_id=sid,
                name=name,
                gender=gender,
                birth=datetime.strptime(birth, "%Y-%m-%d"),
                phone=phone,
                email=email,
                college_id=int(college_id),
                major_id=int(major_id),
                class_id=int(class_id),
                enrollment_date=datetime.strptime(enrollment_date, "%Y-%m-%d").date(),
            )
            self.db.add_student(student)

            # 发送信号
            self.added.emit(student)
            return self.success("学生添加成功")
        except Exception as err:
            return self.error(str(err))

    def update(
        self,
        student_id: str,
        name: str | None = None,
        gender: Literal["F", "M"] | None = None,
        birth: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        college_id: str | None = None,
        major_id: str | None = None,
        class_id: str | None = None,
        enrollment_date: str | None = None,
    ) -> bool:
        try:
            sid = check_student_id(student_id)

            # 转换日期格式
            birth_dt = datetime.strptime(birth, "%Y-%m-%d") if birth else None
            enroll_dt = (
                datetime.strptime(enrollment_date, "%Y-%m-%d").date()
                if enrollment_date
                else None
            )

            # 更新数据
            student = self.db.update_student(
                sid,
                name=name,
                gender=gender,
                birth=birth_dt,
                phone=phone,
                email=email,
                college_id=int(college_id) if college_id else None,
                major_id=int(major_id) if major_id else None,
                class_id=int(class_id) if class_id else None,
                enrollment_date=enroll_dt,
            )

            self.updated.emit(student)
            return self.success("学生信息更新成功")
        except Exception as err:
            return self.error(str(err))

    def delete(self, student_id: str) -> bool:
        try:
            sid = check_student_id(student_id)
            self.db.delete_student(sid)
            self.deleted.emit(student_id)
            return self.success("学生删除成功")
        except Exception as err:
            return self.error(str(err))

    def get(self, student_id: str) -> Student | None:
        """获取单个学生信息"""
        try:
            sid = check_student_id(student_id)
            return self.db.get_student(sid)
        except Exception as err:
            self.error(str(err))
            return None

    def get_all(self) -> list[Student]:
        """获取所有学生信息"""
        return self.db.get_all_students()

    def get_by_class(self, class_id: str) -> list[Student]:
        """按班级查询学生"""
        return self.db.get_by_class(int(class_id))

    def get_by_major(self, major_id: str) -> list[Student]:
        """按专业查询学生"""
        return self.db.get_by_major(int(major_id))

    def get_by_college(self, college_id: str) -> list[Student]:
        """按学院查询学生"""
        return self.db.get_by_college(int(college_id))
