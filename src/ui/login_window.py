from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from database import DBManager


class LoginWindow(QMainWindow):
    switch_window = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle("学生信息管理系统")
        self.setFixedSize(400, 300)

        # 创建中央部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 创建标题标签
        title_label = QLabel("学生信息管理系统")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # 创建表单布局
        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)

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
        login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(login_button)

    def handle_login(self):
        role = self.role_combo.currentText()
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "警告", "用户名和密码不能为空！")
            return

        role = {"管理员": "Admin", "教师": "Teacher", "学生": "Student"}[role]
        if not DBManager.system_account().check_login(role, username, password):
            QMessageBox.warning(self, "错误", "用户名或密码错误！")
            return

        self.switch_window.emit(role, username)
