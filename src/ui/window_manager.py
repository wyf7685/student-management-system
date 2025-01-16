from PyQt6.QtCore import QObject


class WindowManager(QObject):
    def __init__(self):
        super().__init__()
        self.current_window = None

    def show_login(self):
        from .login_window import LoginWindow

        if self.current_window:
            self.current_window.close()

        self.login_window = LoginWindow()
        self.login_window.switch_window = self.show_main_window  # wtf
        self.login_window.show()
        self.current_window = self.login_window

    def show_main_window(self, role, user_id):
        if self.current_window:
            self.current_window.close()

        if role == "Student":
            from .student.window import StudentMainWindow

            self.main_window = StudentMainWindow(user_id)

        elif role == "Admin":
            from .admin.window import AdminMainWindow

            self.main_window = AdminMainWindow(user_id)

        elif role == "Teacher":
            from .teacher.window import TeacherMainWindow

            self.main_window = TeacherMainWindow(user_id)

        self.main_window.logout_signal.connect(self.show_login)
        self.main_window.show()
        self.current_window = self.main_window
