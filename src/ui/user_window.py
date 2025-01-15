from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from utils import check

from .dialog.about import AboutWindow
from .dialog.settings import SettingsWindow


class BaseUserWindow(QMainWindow):
    logout_signal = pyqtSignal()
    status_update = pyqtSignal(str)

    def __init__(self, user_id: str) -> None:
        super().__init__()
        self.user_id = user_id

        self.about_dialog = None
        self.create_menu_bar()
        self.create_status_bar()
        self.init_ui()

    def create_menu_bar(self) -> None:
        self.menubar = check(self.menuBar())

        # 文件菜单
        file_menu = check(self.menubar.addMenu("文件"))
        settings_action = check(file_menu.addAction("设置"))
        settings_action.triggered.connect(lambda: SettingsWindow(self).exec())
        action = check(file_menu.addAction("退出登录"))
        action.triggered.connect(self.handle_logout)

        # 帮助菜单
        help_menu = check(self.menubar.addMenu("帮助"))
        about_action = check(help_menu.addAction("关于"))
        about_action.triggered.connect(lambda: AboutWindow(self).exec())

    def create_status_bar(self) -> None:
        self.status_bar = check(self.statusBar())
        self.status_bar.showMessage("就绪")
        self.status_update.connect(self.status_bar.showMessage)

    def init_ui(self) -> None:
        raise NotImplementedError

    def handle_logout(self):
        reply = QMessageBox.question(
            self,
            "确认",
            "确定要退出登录吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.logout_signal.emit()
