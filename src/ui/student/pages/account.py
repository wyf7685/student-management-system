from PyQt6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from database.manager import DBManager
from ui.common.page import BasePage
from utils import check


class AccountPage(BasePage):
    button_name = "账号管理"

    def init_ui(self) -> None:
        layout_h = QHBoxLayout()
        layout_v = QVBoxLayout()
        central_box = QGroupBox("账号管理")
        layout_v.addSpacing(60)
        layout_v.addWidget(central_box)
        layout_v.addSpacing(60)
        layout_h.addSpacing(90)
        layout_h.addLayout(layout_v)
        layout_h.addSpacing(90)
        self.setLayout(layout_h)

        box_layout = QVBoxLayout()
        central_box.setLayout(box_layout)
        form = QFormLayout()
        box_layout.addLayout(form)

        student_id = int(self.get_user_id())
        form.addRow("身份:", QLabel("学生"))
        form.addRow("学号:", QLabel(str(student_id)))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("密码:", self.password_edit)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.confirm_btn = QPushButton("确认修改")
        self.confirm_btn.clicked.connect(self.confirm_edit_password)
        btn_layout.addWidget(self.confirm_btn)
        box_layout.addLayout(btn_layout)

    def confirm_edit_password(self):
        password = self.password_edit.text()
        if not password:
            QMessageBox.warning(self, "错误", "密码不能为空")
            return

        try:
            db = DBManager.system_account()
            account = check(db.find_account("Student", self.get_user_id()))
            db.update_account(account.id, password=password)
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
        else:
            QMessageBox.information(self, "成功", "密码修改成功")
        finally:
            self.password_edit.clear()
