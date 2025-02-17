from PyQt6.QtCore import QObject

from .admin.window import AdminMainWindow
from .common.user_window import BaseUserWindow
from .login_window import LoginWindow
from .student.window import StudentMainWindow
from .teacher.window import TeacherMainWindow

WINDOW_CLS: dict[str, type[BaseUserWindow]] = {
    "Admin": AdminMainWindow,
    "Student": StudentMainWindow,
    "Teacher": TeacherMainWindow,
}


class WindowManager(QObject):
    def __init__(self):
        super().__init__()
        self.current_window = None

    def show_login(self):
        if self.current_window:
            self.current_window.close()

        self.login_window = LoginWindow()
        self.login_window.switch_window = self.show_main_window  # wtf
        self.login_window.show()
        self.current_window = self.login_window

    def show_main_window(self, role: str, user_id: str):
        if self.current_window:
            self.current_window.close()

        self.main_window = WINDOW_CLS[role](user_id)
        self.main_window.logout_signal.connect(self.show_login)
        self.main_window.show()
        self.current_window = self.main_window
