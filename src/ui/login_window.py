from collections.abc import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from config import LastLogin, config
from const import BUTTON_STYLESHEET
from database import DBManager
from database.db_config import setup_default_data
from utils import check

from .dialog.about import AboutDialog
from .dialog.settings import SettingsDialog

ROLE_CONVERT = {
    "管理员": "Admin",
    "教师": "Teacher",
    "学生": "Student",
    "Admin": "管理员",
    "Teacher": "教师",
    "Student": "学生",
}


class LoginWindow(QMainWindow):
    switch_window: Callable[[str, str], object]

    def __init__(self):
        super().__init__()

        self.about_dialog = None
        self.init_ui()

    def init_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle("学生信息管理系统")
        self.setFixedSize(400, 300)

        # 创建中央部件和主布局
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        layout_h = QHBoxLayout()
        layout_h.addSpacing(40)
        layout_h.addLayout(central_layout)
        layout_h.addSpacing(40)
        central_widget.setLayout(layout_h)
        self.setCentralWidget(central_widget)

        # 创建标题标签
        title_label = QLabel("学生信息管理系统")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central_layout.addWidget(title_label)

        # 创建表单布局
        form_layout = QFormLayout()
        central_layout.addLayout(form_layout)
        # 创建身份选择下拉框
        self.role_combo = QComboBox()
        self.role_combo.addItems(["学生", "教师", "管理员"])
        form_layout.addRow("选择身份:", self.role_combo)
        # 创建用户名输入框
        self.username_input = QLineEdit()
        form_layout.addRow("用户名:", self.username_input)
        # 创建密码输入框
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("密码:", self.password_input)

        # 创建登录按钮
        login_button = QPushButton("登录")
        login_button.setMinimumWidth(100)
        login_button.setMaximumWidth(250)
        login_button.setStyleSheet(BUTTON_STYLESHEET)
        login_button.clicked.connect(self.handle_login)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(login_button)
        button_layout.addStretch()
        central_layout.addLayout(button_layout)

        # 加载上次登录信息
        self.load_last_login()

        # 创建菜单栏
        self.create_menu_bar()

    def load_last_login(self):
        if config.last_login is not None:
            role = ROLE_CONVERT[config.last_login.role]
            self.role_combo.setCurrentText(role)
            self.username_input.setText(config.last_login.username)

    def save_last_login(self, role: str, username: str):
        config.last_login = LastLogin(role=role, username=username)  # type:ignore[]
        config.save()

    def create_menu_bar(self) -> None:
        self.menubar = check(self.menuBar())

        # 文件菜单
        file_menu = check(self.menubar.addMenu("文件"))
        setup_default_action = check(file_menu.addAction("导入默认数据"))
        setup_default_action.triggered.connect(self.handle_setup_default_data)
        settings_action = check(file_menu.addAction("设置"))
        settings_action.triggered.connect(lambda: SettingsDialog(self).exec())
        exit_action = check(file_menu.addAction("退出"))
        exit_action.triggered.connect(self.close)

        # 帮助菜单
        help_menu = check(self.menubar.addMenu("帮助"))
        about_action = check(help_menu.addAction("关于"))
        about_action.triggered.connect(lambda: AboutDialog(self).exec())

    def handle_login(self):
        role = ROLE_CONVERT[self.role_combo.currentText()]
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "警告", "用户名和密码不能为空！")
            return

        if not DBManager.system_account().check_login(role, username, password):
            QMessageBox.warning(self, "错误", "用户名或密码错误！")
            return

        self.save_last_login(role, username)
        self.switch_window(role, username)

    def handle_setup_default_data(self):
        try:
            setup_default_data()
        except Exception as err:
            QMessageBox.critical(self, "错误", f"导入默认数据失败：{err}")
        else:
            QMessageBox.information(self, "成功", "导入默认数据成功！")
