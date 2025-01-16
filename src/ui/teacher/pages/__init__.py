from ui.common.page import BasePage

from .grade import GradePage

PAGES: tuple[type[BasePage], ...] = (GradePage,)
