from ..page import BasePage
from .class_ import ClassPage
from .college import CollegePage
from .course import CoursePage
from .major import MajorPage
from .student import StudentPage

PAGES: tuple[type[BasePage], ...] = (
    CollegePage,
    MajorPage,
    ClassPage,
    StudentPage,
    CoursePage,
)
