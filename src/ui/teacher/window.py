from PyQt6.QtCore import pyqtSignal

from ui.common.user_window import BaseUserWindow


class TeacherMainWindow(BaseUserWindow):
    logout_signal = pyqtSignal()

    def init_ui(self):
        pass
