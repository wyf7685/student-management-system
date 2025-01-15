from .manager import DBManager as DBManager
from .models import Award as Award
from .models import Class as Class
from .models import Club as Club
from .models import College as College
from .models import Course as Course
from .models import Grade as Grade
from .models import Major as Major
from .models import Student as Student
from .models import StudentClub as StudentClub
from .models import StudentStatus as StudentStatus


def __init():
    from .db_config import create_all

    create_all()


__init()
