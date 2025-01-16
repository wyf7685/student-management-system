from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpacerItem,
    QVBoxLayout,
)

from database import DBManager
from ui.common.page import BasePage
from utils import check


class InfoPage(BasePage):
    button_name = "个人信息"

    def init_ui(self):
        group_box = QGroupBox("个人信息")
        group_layout = QVBoxLayout()
        group_box.setLayout(group_layout)

        self.id_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.gender_edit = QLineEdit()
        self.birth_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.college_edit = QLineEdit()
        self.major_edit = QLineEdit()
        self.class_edit = QLineEdit()
        self.enrollment_date_edit = QLineEdit()
        for label, edit, readonly in [
            ("学号:", self.id_edit, True),
            ("姓名:", self.name_edit, True),
            ("性别:", self.gender_edit, True),
            ("出生日期:", self.birth_edit, True),
            ("电话:", self.phone_edit, False),
            ("电子邮件:", self.email_edit, False),
            ("学院:", self.college_edit, True),
            ("专业:", self.major_edit, True),
            ("班级:", self.class_edit, True),
            ("入学日期:", self.enrollment_date_edit, True),
        ]:
            edit.setReadOnly(readonly)
            row = QHBoxLayout()
            label = QLabel(label)
            label.setFixedWidth(80)
            row.addWidget(label)
            row.addWidget(edit)
            group_layout.addLayout(row)

        self.phone_edit.textChanged.connect(self.on_line_edit_updated)
        self.email_edit.textChanged.connect(self.on_line_edit_updated)

        central_layout = QVBoxLayout()
        central_layout.addWidget(group_box)

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

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.confirm_btn = btn("确认修改")
        self.confirm_btn.clicked.connect(self.on_confirm_modify)
        self.cancel_btn = btn("取消修改")
        self.cancel_btn.clicked.connect(self.load_student_info)
        central_layout.addLayout(button_layout)

        layout = QHBoxLayout()
        spacer = QSpacerItem(90, 20)
        layout.addSpacerItem(spacer)
        layout.addLayout(central_layout)
        layout.addSpacerItem(spacer)
        self.setLayout(layout)

        # 初始化学生信息
        self.load_student_info()
        self.on_line_edit_updated()

    def on_line_edit_updated(self):
        enabled = (
            self.phone_edit.text().strip() != self.phone
            or self.email_edit.text().strip() != self.email
        )
        self.confirm_btn.setEnabled(enabled)
        self.cancel_btn.setEnabled(enabled)

    def on_confirm_modify(self):
        phone = self.phone_edit.text().strip()
        email = self.email_edit.text().strip()

        db = DBManager.student()
        try:
            db.update_student(
            int(self.get_user_id()),
            phone=phone,
            email=email,
        )
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
            db.rollback()
        else:
            QMessageBox.information(self, "成功", "修改成功")
            self.phone = phone
            self.email = email

    def load_student_info(self):
        # 查询学生信息
        student = check(DBManager.student().get_student(int(self.get_user_id())))
        college = check(DBManager.college().get_college(student.college_id))
        major = check(DBManager.major().get_major(student.major_id))
        class_ = check(DBManager.class_().get_class(student.class_id))

        self.phone = student.phone
        self.email = student.email

        self.id_edit.setText(str(student.student_id))
        self.name_edit.setText(student.name)
        self.gender_edit.setText("男" if student.gender == "M" else "女")
        self.birth_edit.setText(student.birth.strftime("%Y-%m-%d"))
        self.phone_edit.setText(student.phone)
        self.email_edit.setText(student.email)
        self.college_edit.setText(college.name)
        self.major_edit.setText(major.name)
        self.class_edit.setText(class_.name)
        self.enrollment_date_edit.setText(student.enrollment_date.strftime("%Y-%m-%d"))
