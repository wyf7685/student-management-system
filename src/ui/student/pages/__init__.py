from ui.common.page import BasePage

from .award import AwardPage
from .course import CoursePage
from .exam import ExamPage
from .grade import GradePage
from .info import InfoPage

PAGES: tuple[type[BasePage], ...] = (
    InfoPage,
    CoursePage,
    ExamPage,
    GradePage,
    AwardPage,
)

"""
个人信息
课表查询
考试查询
成绩查询
奖项查询
"""
