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

from utils import check

from ..user_window import BaseUserWindow


class StudentMainWindow(BaseUserWindow):
    def init_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle("学生信息管理系统 - 学生端")
        self.setMinimumSize(800, 600)

        # 创建菜单栏
        menubar = check(self.menuBar())

        # 信息查询菜单
        info_menu = check(menubar.addMenu("信息查询"))
        personal_info_action = check(info_menu.addAction("个人信息"))
        personal_info_action.triggered.connect(lambda: self.switch_page(0))

        # 教学管理菜单
        teaching_menu = check(menubar.addMenu("教学管理"))
        schedule_action = check(teaching_menu.addAction("课表查询"))
        schedule_action.triggered.connect(lambda: self.switch_page(1))
        exam_action = check(teaching_menu.addAction("考试查询"))
        exam_action.triggered.connect(lambda: self.switch_page(2))
        grade_action = check(teaching_menu.addAction("成绩查询"))
        grade_action.triggered.connect(lambda: self.switch_page(3))

        # 奖项管理菜单
        award_menu = check(menubar.addMenu("奖项管理"))
        award_action = check(award_menu.addAction("奖项查询"))
        award_action.triggered.connect(lambda: self.switch_page(4))

        # 系统菜单
        system_menu = check(menubar.addMenu("系统"))
        logout_action = check(system_menu.addAction("退出登录"))
        logout_action.triggered.connect(self.handle_logout)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)

        # 添加标题栏
        title_label = QLabel("学生信息管理系统 - 学生端")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("background-color: #f0f0f0; padding: 10px;")
        main_layout.addWidget(title_label)

        # 创建堆叠窗口部件用于切换不同页面
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # 添加各功能页面
        self.init_pages()

        # 创建底部按钮区域
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setSpacing(10)

        # 定义按钮列表
        buttons = [
            ("个人信息", 0),
            ("课表查询", 1),
            ("考试查询", 2),
            ("成绩查询", 3),
            ("奖项查询", 4),
        ]

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
            button_layout.addWidget(btn)
            return btn

        # 创建按钮
        for text, page_index in buttons:
            btn(text).clicked.connect(slot(page_index))

        btn("退出登录").clicked.connect(self.handle_logout)

        main_layout.addWidget(button_widget)

        # 创建状态栏
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage(f"当前用户: {self.user_id}")

    def init_pages(self):
        # 个人信息页面
        personal_page = QWidget()
        self.stack.addWidget(personal_page)

        # 课表查询页面
        schedule_page = QWidget()
        self.stack.addWidget(schedule_page)

        # 考试查询页面
        exam_page = QWidget()
        self.stack.addWidget(exam_page)

        # 成绩查询页面
        grade_page = QWidget()
        self.stack.addWidget(grade_page)

        # 奖项查询页面
        award_page = QWidget()
        self.stack.addWidget(award_page)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
