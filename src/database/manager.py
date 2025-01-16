import datetime
import hashlib
import uuid
from typing import Literal

from .db_config import get_session, get_token
from .models import Class, College, Course, Grade, Major, Student, SystemAccount, Award


class DBManager:
    def __init__(self) -> None:
        self._session = get_session()
        self._token = get_token()

    @property
    def session(self):
        if self._token is not get_token():
            self._session = get_session()
        return self._session

    def rollback(self):
        self.session.rollback()

    @classmethod
    def college(cls):
        return CollegeDBManager()

    @classmethod
    def major(cls):
        return MajorDBManager()

    @classmethod
    def class_(cls):
        return ClassDBManager()

    @classmethod
    def student(cls):
        return StudentDBManager()

    @classmethod
    def course(cls):
        return CourseDBManager()

    @classmethod
    def system_account(cls):
        return SystemAccountDBManager()

    @classmethod
    def grade(cls):
        return GradeDBManager()


class CollegeDBManager(DBManager):
    def get_college(self, college_id: int) -> College | None:
        return self.session.query(College).get(college_id)

    def get_all_colleges(self):
        return self.session.query(College).all()

    def exists_college(self, college_id: int):
        return self.session.query(College).filter_by(college_id=college_id).count() > 0

    def add_college(self, college: College):
        self.session.add(college)
        self.session.commit()

    def update_college(self, college_id: int, name: str):
        college = self.get_college(college_id)
        if not college:
            raise ValueError("学院不存在")
        college.name = name
        self.session.commit()
        return college

    def delete_college(self, college_id: int):
        college = self.get_college(college_id)
        if not college:
            raise ValueError("学院不存在")
        self.session.delete(college)
        self.session.commit()


class MajorDBManager(DBManager):
    def get_major(self, major_id: int) -> Major | None:
        return self.session.query(Major).get(major_id)

    def get_all_majors(self):
        return self.session.query(Major).all()

    def exists_major(self, major_id: int):
        return self.session.query(Major).filter_by(major_id=major_id).count() > 0

    def add_major(self, major: Major):
        self.session.add(major)
        self.session.commit()

    def update_major(
        self,
        major_id: int,
        *,
        name: str | None = None,
        college_id: int | None = None,
    ):
        major = self.get_major(major_id)
        if not major:
            raise ValueError("专业不存在")
        if name is not None:
            major.name = name
        if college_id is not None:
            major.college_id = college_id
        self.session.commit()
        return major

    def delete_major(self, major_id: int):
        major = self.get_major(major_id)
        if not major:
            raise ValueError("专业不存在")
        self.session.delete(major)
        self.session.commit()


class ClassDBManager(DBManager):
    def get_class(self, class_id: int) -> Class | None:
        return self.session.query(Class).get(class_id)

    def get_all_classes(self):
        return self.session.query(Class).all()

    def exists_class(self, class_id: int):
        return self.session.query(Class).filter_by(class_id=class_id).count() > 0

    def add_class(self, class_: Class):
        self.session.add(class_)
        self.session.commit()

    def update_class(
        self,
        class_id: int,
        *,
        name: str | None = None,
        major_id: int | None = None,
        year: int | None = None,
    ):
        class_ = self.get_class(class_id)
        if not class_:
            raise ValueError("班级不存在")
        if name is not None:
            class_.name = name
        if major_id is not None:
            class_.major_id = major_id
        if year is not None:
            class_.year = year
        self.session.commit()
        return class_

    def delete_class(self, class_id: int):
        class_ = self.get_class(class_id)
        if not class_:
            raise ValueError("班级不存在")
        self.session.delete(class_)
        self.session.commit()


class StudentDBManager(DBManager):
    def get_student(self, student_id: int) -> Student | None:
        return self.session.query(Student).get(student_id)

    def get_all_students(self):
        return self.session.query(Student).all()

    def exists_student(self, student_id: int):
        return self.session.query(Student).filter_by(student_id=student_id).count() > 0

    def add_student(self, student: Student):
        self.session.add(student)
        self.session.commit()

    def update_student(
        self,
        student_id: int,
        *,
        name: str | None = None,
        gender: Literal["F", "M"] | None = None,
        birth: datetime.datetime | None = None,
        phone: str | None = None,
        email: str | None = None,
        college_id: int | None = None,
        major_id: int | None = None,
        class_id: int | None = None,
        enrollment_date: datetime.date | None = None,
    ):
        student = self.get_student(student_id)
        if not student:
            raise ValueError("学生不存在")

        if name is not None:
            student.name = name
        if gender is not None:
            student.gender = gender
        if birth is not None:
            student.birth = birth
        if phone is not None:
            student.phone = phone
        if email is not None:
            student.email = email
        if college_id is not None:
            student.college_id = college_id
        if major_id is not None:
            student.major_id = major_id
        if class_id is not None:
            student.class_id = class_id
        if enrollment_date is not None:
            student.enrollment_date = enrollment_date

        self.session.commit()
        return student

    def delete_student(self, student_id: int):
        student = self.get_student(student_id)
        if not student:
            raise ValueError("学生不存在")
        self.session.delete(student)
        self.session.commit()

    def get_by_class(self, class_id: int):
        """按班级查询学生"""
        return self.session.query(Student).filter_by(class_id=class_id).all()

    def get_by_major(self, major_id: int):
        """按专业查询学生"""
        return self.session.query(Student).filter_by(major_id=major_id).all()

    def get_by_college(self, college_id: int):
        """按学院查询学生"""
        return self.session.query(Student).filter_by(college_id=college_id).all()


class CourseDBManager(DBManager):
    def get_course(self, course_id: int) -> Course | None:
        return self.session.query(Course).get(course_id)

    def get_all_courses(self):
        return self.session.query(Course).all()

    def exists_course(self, course_id: int):
        return self.session.query(Course).filter_by(course_id=course_id).count() > 0

    def add_course(self, course: Course):
        if self.exists_course(course.course_id):
            raise ValueError("课程代码已存在")
        if not (1 <= course.credits <= 10):
            raise ValueError("学分必须在1-10之间")
        self.session.add(course)
        self.session.commit()

    def update_course(
        self,
        course_id: int,
        *,
        name: str | None = None,
        credits: int | None = None,
    ):
        course = self.get_course(course_id)
        if not course:
            raise ValueError("课程不存在")

        if name is not None:
            course.name = name
        if credits is not None:
            if credits <= 0:
                raise ValueError("学分必须大于 0")
            course.credits = credits

        self.session.commit()
        return course

    def delete_course(self, course_id: int):
        course = self.get_course(course_id)
        if not course:
            raise ValueError("课程不存在")
        self.session.delete(course)
        self.session.commit()


class SystemAccountDBManager(DBManager):
    @staticmethod
    def encode_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def convert_user_id(role: str, user_id: str) -> dict[str, str | int]:
        if role == "Student":
            return {"student_id": int(user_id)}
        if role == "Teacher":
            return {"teacher_id": int(user_id)}
        if role == "Admin":
            return {"admin_id": user_id}
        raise ValueError("Invalid role")

    def get_account(self, account_id: int) -> SystemAccount | None:
        return self.session.query(SystemAccount).get(account_id)

    def get_all_accounts(self):
        return self.session.query(SystemAccount).all()

    def find_account(self, role: str, username: str) -> SystemAccount | None:
        kwds = {"role": role} | self.convert_user_id(role, username)
        return self.session.query(SystemAccount).filter_by(**kwds).first()

    def exists_account(self, role: str, username: str):
        return self.find_account(role, username) is not None

    def add_account(self, role: str, username: str, password: str):
        salt = str(uuid.uuid4())
        kwds: dict[str, str | int] = {
            "role": role,
            "password": self.encode_password(password + salt),
            "salt": salt,
            **self.convert_user_id(role, username),
        }
        self.session.add(SystemAccount(**kwds))
        self.session.commit()

    def update_account(
        self,
        account_id: int,
        *,
        role: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ):
        account = self.get_account(account_id)
        if not account:
            raise ValueError("账户不存在")

        if role is not None:
            if role not in ("Student", "Teacher", "Admin"):
                raise ValueError("角色必须为 Student, Teacher, Admin 中的一个")
            account.role = role
        if username is not None:
            account.user_id = username
        if password is not None:
            account.salt = str(uuid.uuid4())
            account.password = self.encode_password(password + account.salt)

        self.session.commit()
        return account

    def delete_account(self, account_id: int):
        account = self.get_account(account_id)
        if not account:
            raise ValueError("账户不存在")
        self.session.delete(account)
        self.session.commit()

    def check_login(self, role: str, username: str, password: str):
        kwds = {"role": role} | self.convert_user_id(role, username)
        account = self.session.query(SystemAccount).filter_by(**kwds).first()
        return (
            account is not None
            and self.encode_password(password + account.salt) == account.password
        )


class GradeDBManager(DBManager):
    def get_grade(self, student_id: int, course_id: int) -> Grade | None:
        return self.session.query(Grade).get((student_id, course_id))

    def get_all_grades(self):
        return self.session.query(Grade).all()

    def exists_grade(self, student_id: int, course_id: int) -> bool:
        return (
            self.session.query(Grade)
            .filter_by(student_id=student_id, course_id=course_id)
            .count()
            > 0
        )

    def add_grade(self, grade: Grade):
        if self.exists_grade(grade.student_id, grade.course_id):
            raise ValueError("成绩记录已存在")
        self.session.add(grade)
        self.session.commit()

    def update_grade(
        self,
        student_id: int,
        course_id: int,
        *,
        score: int | None = None,
        term: str | None = None,
    ):
        grade = self.get_grade(student_id, course_id)
        if not grade:
            raise ValueError("成绩记录不存在")

        if score is not None:
            grade.score = score
        if term is not None:
            grade.term = term

        self.session.commit()
        return grade

    def delete_grade(self, student_id: int, course_id: int):
        grade = self.get_grade(student_id, course_id)
        if not grade:
            raise ValueError("成绩记录不存在")
        self.session.delete(grade)
        self.session.commit()


class AwardDBManager(DBManager):
    def get_award(self, award_id: int) -> Award | None:
        return self.session.query(Award).get(award_id)

    def get_all_awards(self):
        return self.session.query(Award).all()

    def get_awards_by_student(self, student_id: int):
        return self.session.query(Award).filter_by(student_id=student_id).all()

    def exists_award(self, award_id: int) -> bool:
        return self.session.query(Award).filter_by(award_id=award_id).count() > 0

    def add_award(self, award: Award):
        if self.exists_award(award.award_id):
            raise ValueError("奖项已存在")
        self.session.add(award)
        self.session.commit()

    def update_award(
        self,
        award_id: int,
        *,
        student_id: int | None = None,
        award_name: str | None = None,
        award_date: datetime.date | None = None,
    ):
        award = self.get_award(award_id)
        if not award:
            raise ValueError("奖项不存在")

        if student_id is not None:
            award.student_id = student_id
        if award_name is not None:
            award.award_name = award_name
        if award_date is not None:
            award.award_date = award_date

        self.session.commit()
        return award

    def delete_award(self, award_id: int):
        award = self.get_award(award_id)
        if not award:
            raise ValueError("奖项不存在")
        self.session.delete(award)
        self.session.commit()
