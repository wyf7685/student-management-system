import datetime
import hashlib
import uuid
from typing import Literal

from .db_config import get_session, validate_token
from .models import (
    Award,
    Class,
    Club,
    College,
    Course,
    CourseEnrollment,
    CourseTeacher,
    EnrollmentsStatusCode,
    Exam,
    Grade,
    Major,
    Scholarship,
    Student,
    StudentClub,
    SystemAccount,
    Teacher,
)


class DBManager:
    def __init__(self) -> None:
        self._session, self._token = get_session()

    @property
    def session(self):
        if not validate_token(self._token):
            self._session, self._token = get_session()
        return self._session

    def rollback(self):
        self.session.rollback()

    def __del__(self):
        self._session.close()

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

    @classmethod
    def award(cls):
        return AwardDBManager()

    @classmethod
    def exam(cls):
        return ExamDBManager()

    @classmethod
    def club(cls):
        return ClubDBManager()

    @classmethod
    def student_club(cls):
        return StudentClubDBManager()

    @classmethod
    def scholarship(cls):
        return ScholarshipDBManager()

    @classmethod
    def teacher(cls):
        return TeacherDBManager()

    @classmethod
    def course_teacher(cls):
        return CourseTeacherDBManager()

    @classmethod
    def course_enrollment(cls):
        return CourseEnrollmentDBManager()


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

    def get_major_by_college(self, college_id: int) -> list[Major]:
        return self.session.query(Major).filter_by(college_id=college_id).all()

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

    def get_class_by_major(self, major_id: int) -> list[Class]:
        return self.session.query(Class).filter_by(major_id=major_id).all()

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

    def get_courses_by_teacher(self, teacher_id: int):
        return (
            self.session.query(Course)
            .join(CourseTeacher, Course.course_id == CourseTeacher.course_id)
            .filter(CourseTeacher.tearcher_id == teacher_id)
            .all()
        )

    def exists_course(self, course_id: int):
        return self.session.query(Course).filter_by(course_id=course_id).count() > 0

    def search_course(self, keyword: str):
        like = f"%{keyword}%"
        return self.session.query(Course).filter(Course.name.like(like)).all()

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

    def find_grade_by_student(self, student_id: int) -> list[Grade]:
        return self.session.query(Grade).filter_by(student_id=student_id).all()

    def find_grade_by_course(self, course_id: int) -> list[Grade]:
        return self.session.query(Grade).filter_by(course_id=course_id).all()

    def exists_grade(self, student_id: int, course_id: int) -> bool:
        return (
            self.session.query(Grade).filter_by(student_id=student_id, course_id=course_id).count()
            > 0
        )

    def add_grade(self, student_id: int, course_id: int, score: int, term: str):
        if self.exists_grade(student_id, course_id):
            raise ValueError("成绩记录已存在")
        grade = Grade(
            student_id=student_id,
            course_id=course_id,
            score=score,
            term=term,
        )
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


class ExamDBManager(DBManager):
    def get_exam(self, exam_id: int) -> Exam | None:
        return self.session.query(Exam).get(exam_id)

    def get_exam_by_student_id(self, student_id: int) -> list[Exam]:
        return (
            self.session.query(Exam)
            .join(Course, Exam.course_id == Course.course_id)
            .join(CourseEnrollment, Course.course_id == CourseEnrollment.course_id)
            .filter(CourseEnrollment.student_id == student_id)
            .all()
        )

    def get_all_exams(self):
        return self.session.query(Exam).all()

    def exists_exam(self, exam_id: int) -> bool:
        return self.session.query(Exam).filter_by(exam_id=exam_id).count() > 0

    def add_exam(self, exam: Exam):
        if self.exists_exam(exam.exam_id):
            raise ValueError("考试记录已存在")
        self.session.add(exam)
        self.session.commit()

    def update_exam(
        self,
        exam_id: int,
        *,
        course_id: int | None = None,
        time: datetime.datetime | None = None,
        duration: int | None = None,
        name: str | None = None,
        description: str | None = None,
        location: str | None = None,
    ):
        exam = self.get_exam(exam_id)
        if not exam:
            raise ValueError("考试记录不存在")

        if course_id is not None:
            exam.course_id = course_id
        if time is not None:
            exam.time = time
        if duration is not None:
            exam.duration = duration
        if name is not None:
            exam.name = name
        if description is not None:
            exam.description = description
        if location is not None:
            exam.location = location

        self.session.commit()
        return exam

    def delete_exam(self, exam_id: int):
        exam = self.get_exam(exam_id)
        if not exam:
            raise ValueError("考试记录不存在")
        self.session.delete(exam)
        self.session.commit()


class ClubDBManager(DBManager):
    def get_club(self, club_id: int) -> Club | None:
        return self.session.query(Club).get(club_id)

    def get_all_clubs(self):
        return self.session.query(Club).all()

    def exists_club(self, club_id: int) -> bool:
        return self.session.query(Club).filter_by(club_id=club_id).count() > 0

    def search_club(self, keyword: str):
        like = f"%{keyword}%"
        return (
            self.session.query(Club)
            .filter((Club.name.like(like)) | (Club.description.like(like)))
            .all()
        )

    def add_club(self, club: Club):
        if self.exists_club(club.club_id):
            raise ValueError("社团已存在")
        self.session.add(club)
        self.session.commit()

    def update_club(
        self,
        club_id: int,
        *,
        name: str | None = None,
        description: str | None = None,
    ):
        club = self.get_club(club_id)
        if not club:
            raise ValueError("社团不存在")

        if name is not None:
            club.name = name
        if description is not None:
            club.description = description

        self.session.commit()
        return club

    def delete_club(self, club_id: int):
        club = self.get_club(club_id)
        if not club:
            raise ValueError("社团不存在")
        self.session.delete(club)
        self.session.commit()


class StudentClubDBManager(DBManager):
    def get_student_club(self, student_id: int, club_id: int) -> StudentClub | None:
        return self.session.query(StudentClub).get((student_id, club_id))

    def get_all_student_clubs(self):
        return self.session.query(StudentClub).all()

    def get_clubs_by_student(self, student_id: int):
        return self.session.query(StudentClub).filter_by(student_id=student_id).all()

    def get_students_by_club(self, club_id: int):
        return self.session.query(StudentClub).filter_by(club_id=club_id).all()

    def exists_student_club(self, student_id: int, club_id: int) -> bool:
        return (
            self.session.query(StudentClub)
            .filter_by(student_id=student_id, club_id=club_id)
            .count()
            > 0
        )

    def add_student_club(self, student_id: int, club_id: int, role: str):
        if self.exists_student_club(student_id, club_id):
            raise ValueError("学生社团关系已存在")
        student_club = StudentClub(student_id=student_id, club_id=club_id, role=role)
        self.session.add(student_club)
        self.session.commit()

    def delete_student_club(self, student_id: int, club_id: int):
        student_club = self.get_student_club(student_id, club_id)
        if not student_club:
            raise ValueError("学生社团关系不存在")
        self.session.delete(student_club)
        self.session.commit()


class ScholarshipDBManager(DBManager):
    def get_scholarship(self, scholarship_id: int) -> Scholarship | None:
        return self.session.query(Scholarship).get(scholarship_id)

    def get_all_scholarships(self):
        return self.session.query(Scholarship).all()

    def get_scholarships_by_student(self, student_id: int):
        return self.session.query(Scholarship).filter_by(student_id=student_id).all()

    def exists_scholarship(self, scholarship_id: int) -> bool:
        return self.session.query(Scholarship).filter_by(scholarship_id=scholarship_id).count() > 0

    def add_scholarship(self, scholarship: Scholarship):
        if self.exists_scholarship(scholarship.scholarship_id):
            raise ValueError("奖学金记录已存在")
        self.session.add(scholarship)
        self.session.commit()

    def update_scholarship(
        self,
        scholarship_id: int,
        *,
        student_id: int | None = None,
        scholarship_name: str | None = None,
        amount: int | None = None,  # 保持为 int 类型，根据你的模型定义
        date_awarded: str | None = None,
        description: str | None = None,
    ):
        scholarship = self.get_scholarship(scholarship_id)
        if not scholarship:
            raise ValueError("奖学金记录不存在")

        if student_id is not None:
            scholarship.student_id = student_id
        if scholarship_name is not None:
            scholarship.scholarship_name = scholarship_name
        if amount is not None:
            scholarship.amount = amount
        if date_awarded is not None:
            scholarship.date_awarded = date_awarded
        if description is not None:
            scholarship.description = description

        self.session.commit()
        return scholarship

    def delete_scholarship(self, scholarship_id: int):
        scholarship = self.get_scholarship(scholarship_id)
        if not scholarship:
            raise ValueError("奖学金记录不存在")
        self.session.delete(scholarship)
        self.session.commit()


class TeacherDBManager(DBManager):
    def get_teacher(self, teacher_id: int) -> Teacher | None:
        return self.session.query(Teacher).get(teacher_id)

    def get_all_teachers(self):
        return self.session.query(Teacher).all()

    def exists_teacher(self, teacher_id: int) -> bool:
        return self.session.query(Teacher).filter_by(teacher_id=teacher_id).count() > 0

    def add_teacher(self, teacher: Teacher):
        if self.exists_teacher(teacher.teacher_id):
            raise ValueError("教师已存在")
        self.session.add(teacher)
        self.session.commit()

    def update_teacher(
        self,
        teacher_id: int,
        *,
        name: str | None = None,
        gender: Literal["F", "M"] | None = None,
        birth: datetime.datetime | None = None,
        phone: str | None = None,
        email: str | None = None,
    ):
        teacher = self.get_teacher(teacher_id)
        if not teacher:
            raise ValueError("教师不存在")

        if name is not None:
            teacher.name = name
        if gender is not None:
            teacher.gender = gender
        if birth is not None:
            teacher.birth = birth
        if phone is not None:
            teacher.phone = phone
        if email is not None:
            teacher.email = email

        self.session.commit()
        return teacher

    def delete_teacher(self, teacher_id: int):
        teacher = self.get_teacher(teacher_id)
        if not teacher:
            raise ValueError("教师不存在")
        self.session.delete(teacher)
        self.session.commit()


class CourseTeacherDBManager(DBManager):
    def get_course_teacher(self, course_id: int, teacher_id: int) -> CourseTeacher | None:
        return (
            self.session.query(CourseTeacher)
            .filter_by(course_id=course_id, tearcher_id=teacher_id)
            .first()
        )

    def get_all_course_teachers(self):
        return self.session.query(CourseTeacher).all()

    def get_courses_by_teacher(self, teacher_id: int):
        return self.session.query(CourseTeacher).filter_by(tearcher_id=teacher_id).all()

    def get_teachers_by_course(self, course_id: int):
        return self.session.query(CourseTeacher).filter_by(course_id=course_id).all()

    def get_by_semester(self, semester: str):
        return self.session.query(CourseTeacher).filter_by(semester=semester).all()

    def exists_course_teacher(self, course_id: int, teacher_id: int) -> bool:
        return (
            self.session.query(CourseTeacher)
            .filter_by(course_id=course_id, tearcher_id=teacher_id)
            .count()
            > 0
        )

    def add_course_teacher(self, course_id: int, teacher_id: int, semester: str):
        if self.exists_course_teacher(course_id, teacher_id):
            raise ValueError("课程教师关系已存在")
        course_teacher = CourseTeacher(
            course_id=course_id, tearcher_id=teacher_id, semester=semester
        )
        self.session.add(course_teacher)
        self.session.commit()

    def update_course_teacher(
        self,
        course_id: int,
        teacher_id: int,
        *,
        semester: str | None = None,
    ):
        course_teacher = self.get_course_teacher(course_id, teacher_id)
        if not course_teacher:
            raise ValueError("课程教师关系不存在")

        if semester is not None:
            course_teacher.semester = semester

        self.session.commit()
        return course_teacher

    def delete_course_teacher(self, course_id: int, teacher_id: int):
        course_teacher = self.get_course_teacher(course_id, teacher_id)
        if not course_teacher:
            raise ValueError("课程教师关系不存在")
        self.session.delete(course_teacher)
        self.session.commit()


class CourseEnrollmentDBManager(DBManager):
    def get_enrollment(self, student_id: int, course_id: int) -> CourseEnrollment | None:
        return (
            self.session.query(CourseEnrollment)
            .filter_by(student_id=student_id, course_id=course_id)
            .first()
        )

    def get_all_enrollments(self):
        return self.session.query(CourseEnrollment).all()

    def get_student_enrollments(self, student_id: int):
        return self.session.query(CourseEnrollment).filter_by(student_id=student_id).all()

    def get_course_enrollments(self, course_id: int):
        return self.session.query(CourseEnrollment).filter_by(course_id=course_id).all()

    def get_by_semester(self, semester: str):
        return self.session.query(CourseEnrollment).filter_by(semester=semester).all()

    def get_by_status(self, status: EnrollmentsStatusCode):
        return self.session.query(CourseEnrollment).filter_by(course_status=status).all()

    def get_detail(self, enrollment: CourseEnrollment):
        data = (
            self.session.query(
                CourseEnrollment.student_id,
                Student.name,
                CourseEnrollment.course_id,
                Course.name,
            )
            .join(Student, Student.student_id == CourseEnrollment.student_id)
            .join(Course, Course.course_id == CourseEnrollment.course_id)
            .filter(CourseEnrollment.student_id == enrollment.student_id)
            .filter(CourseEnrollment.course_id == enrollment.course_id)
            .first()
        )
        if data is None:
            return data

        score = (
            self.session.query(Grade.score)
            .filter_by(
                student_id=enrollment.student_id,
                course_id=enrollment.course_id,
            )
            .first()
        )
        return (*data.t, score.t[0] if score else None)

    def exists_enrollment(self, student_id: int, course_id: int) -> bool:
        return (
            self.session.query(CourseEnrollment)
            .filter_by(student_id=student_id, course_id=course_id)
            .count()
            > 0
        )

    def add_enrollment(self, enrollment: CourseEnrollment):
        if self.exists_enrollment(enrollment.student_id, enrollment.course_id):
            raise ValueError("选课记录已存在")
        self.session.add(enrollment)
        self.session.commit()

    def update_enrollment(
        self,
        student_id: int,
        course_id: int,
        *,
        semester: str | None = None,
        course_status: EnrollmentsStatusCode | None = None,
    ):
        enrollment = self.get_enrollment(student_id, course_id)
        if not enrollment:
            raise ValueError("选课记录不存在")

        if semester is not None:
            enrollment.semester = semester
        if course_status is not None:
            enrollment.course_status = course_status

        self.session.commit()
        return enrollment

    def delete_enrollment(self, student_id: int, course_id: int):
        enrollment = self.get_enrollment(student_id, course_id)
        if not enrollment:
            raise ValueError("选课记录不存在")
        self.session.delete(enrollment)
        self.session.commit()
