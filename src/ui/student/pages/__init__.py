from ui.common.page import BasePage

from .account import AccountPage
from .award import AwardPage
from .club import ClubPage
from .course import CoursePage
from .exam import ExamPage
from .grade import GradePage
from .info import InfoPage
from .scholarship import ScholarshipPage

PAGES: tuple[type[BasePage], ...] = (
    InfoPage,
    CoursePage,
    ExamPage,
    GradePage,
    AwardPage,
    ScholarshipPage,
    ClubPage,
    AccountPage,
)
