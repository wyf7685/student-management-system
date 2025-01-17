from ui.common.page import BasePage

from .course import CoursePage
from .grade import GradePage

PAGES: tuple[type[BasePage], ...] = (
    CoursePage,
    GradePage,
)
