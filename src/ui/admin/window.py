from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from ..user_window import BaseUserWindow
from .common import setup_admin_main
from .tabs import TABS


class AdminMainWindow(BaseUserWindow):
    def init_ui(self) -> None:
        self.setWindowTitle("学生信息管理系统 - 管理员端")
        self.setMinimumSize(800, 600)

        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self._layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget()
        self._layout.addWidget(self.tab_widget)

        for tab in TABS:
            tab(self.tab_widget).put_into(self.tab_widget)

        setup_admin_main(self)
