from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from ..user_window import BaseUserWindow
from .pages import PAGES


class StudentMainWindow(BaseUserWindow):
    def init_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle("学生信息管理系统 - 学生端")
        self.setMinimumSize(800, 600)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)

        # 添加标题栏
        title_label = QLabel("学生信息管理系统 - 学生端")
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

        for idx, page in enumerate(PAGES):
            p = page(self)
            btn(p.button_name).clicked.connect(slot(idx))
            self.stack.addWidget(p)

        btn("退出登录").clicked.connect(self.handle_logout)

        self.switch_page(0)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
