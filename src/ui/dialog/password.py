from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from database.manager import DBManager
from utils import check


class PasswordDialog(QDialog):
    def __init__(self, parent: QWidget, role: str, user_id: str) -> None:
        super().__init__(parent)
        self.role = role
        self.user_id = user_id

        self.setWindowTitle("修改密码")
        self.setFixedSize(200, 150)
        self.init_ui()

    def init_ui(self) -> None:
        layout = QVBoxLayout()
        box = QGroupBox("账号管理")
        form = QFormLayout()
        box.setLayout(form)
        layout.addWidget(box)
        self.setLayout(layout)

        role_name = {
            "Admin": "管理员",
            "Teacher": "教师",
            "Student": "学生",
        }[self.role]

        form.addRow("身份:", QLabel(role_name))
        form.addRow("学号:", QLabel(self.user_id))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("密码:", self.password_edit)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.confirm_btn = QPushButton("确认修改")
        self.confirm_btn.clicked.connect(self.confirm_edit_password)
        btn_layout.addWidget(self.confirm_btn)
        layout.addLayout(btn_layout)

    def confirm_edit_password(self):
        password = self.password_edit.text()
        if not password:
            QMessageBox.warning(self, "错误", "密码不能为空")
            return

        try:
            db = DBManager.system_account()
            account = check(db.find_account(self.role, self.user_id))
            db.update_account(account.id, password=password)
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
        else:
            QMessageBox.information(self, "成功", "密码修改成功")
            self.close()
        finally:
            self.password_edit.clear()

    @classmethod
    def as_slot(cls, parent: QWidget, role: str, user_id: str):
        return lambda: cls(parent, role, user_id).exec()
