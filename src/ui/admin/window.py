from ui.common.user_window import BaseUserWindow

from .pages import PAGES


class AdminMainWindow(BaseUserWindow):
    title = "学生信息管理系统 - 管理员端"
    page_cls = PAGES
