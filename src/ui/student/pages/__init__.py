from ui.common.page import BasePage

from .award import AwardPage
from .course import CoursePage
from .grade import GradePage
from .info import InfoPage
from .scholarship import ScholarshipPage

PAGES: tuple[type[BasePage], ...] = (
    InfoPage,
    CoursePage,
    GradePage,
    AwardPage,
    ScholarshipPage,
)
