from typing import TYPE_CHECKING, ClassVar

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from utils import check

from ..dialog.about import AboutDialog
from ..dialog.settings import SettingsDialog

if TYPE_CHECKING:
    from .page import BasePage


class BaseUserWindow(QMainWindow):
    logout_signal = pyqtSignal()
    status_update = pyqtSignal(str)

    title: ClassVar[str]
    page_cls: ClassVar[tuple[type["BasePage"], ...]]

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
        settings_action.triggered.connect(lambda: SettingsDialog(self).exec())
        action = check(file_menu.addAction("退出登录"))
        action.triggered.connect(self.handle_logout)

        # 帮助菜单
        help_menu = check(self.menubar.addMenu("帮助"))
        about_action = check(help_menu.addAction("关于"))
        about_action.triggered.connect(lambda: AboutDialog(self).exec())

    def create_status_bar(self) -> None:
        self.status_bar = check(self.statusBar())
        self.status_bar.showMessage("就绪")
        self.status_update.connect(self.status_bar.showMessage)

    def handle_logout(self):
        reply = QMessageBox.question(
            self,
            "确认",
            "确定要退出登录吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.logout_signal.emit()

    def init_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle(self.title)
        self.setMinimumSize(800, 600)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)

        # 添加标题栏
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("padding: 10px;")
        main_layout.addWidget(title_label)

        # 创建堆叠窗口部件用于切换不同页面
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # 创建底部按钮区域
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setSpacing(10)
        self.button_layout = button_layout
        main_layout.addWidget(button_widget)

        # 添加各功能页面
        self.init_pages()

        # 创建状态栏
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage(f"当前用户: {self.user_id}")

    def init_pages(self):
        def slot(i):
            return lambda *_: self.switch_page(i)

        def btn(text: str):
            btn = QPushButton(text)
            btn.setMinimumWidth(100)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 8px;
                    background-color: #4a90e2;
                    color: white;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #357abd;
                }
            """)
            self.button_layout.addWidget(btn)
            return btn

        for idx, page in enumerate(self.page_cls):
            p = page(self)
            btn(p.button_name).clicked.connect(slot(idx))
            self.stack.addWidget(p)

        btn("退出登录").clicked.connect(self.handle_logout)

        self.switch_page(0)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
