from ui.common.user_window import BaseUserWindow

from .pages import PAGES


class StudentMainWindow(BaseUserWindow):
    title = "学生信息管理系统 - 学生端"
    page_cls = PAGES
