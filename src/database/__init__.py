from .manager import DBManager as DBManager
from .models import Award as Award
from .models import Class as Class
from .models import Club as Club
from .models import College as College
from .models import Course as Course
from .models import CourseEnrollment as CourseEnrollment
from .models import CourseTeacher as CourseTeacher
from .models import EnrollmentsStatusCode as EnrollmentsStatusCode
from .models import Exam as Exam
from .models import Grade as Grade
from .models import Major as Major
from .models import Scholarship as Scholarship
from .models import Student as Student
from .models import StudentClub as StudentClub
from .models import StudentStatus as StudentStatus
from .models import SystemAccount as SystemAccount
from .models import Teacher as Teacher


def __init():
    from .db_config import create_all

    create_all()


__init()
