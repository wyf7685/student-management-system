from ui.common.user_window import BaseUserWindow

from .pages import PAGES


class TeacherMainWindow(BaseUserWindow):
    title = "学生信息管理系统 - 教师端"
    page_cls = PAGES
