from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)

from database import DBManager
from ui.common.page import BasePage
from utils import check


class InfoPage(BasePage):
    button_name = "个人信息"

    def init_ui(self):
        layout = QVBoxLayout()

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
        for label, edit in [
            ("学号:", self.id_edit),
            ("姓名:", self.name_edit),
            ("性别:", self.gender_edit),
            ("出生日期:", self.birth_edit),
            ("电话:", self.phone_edit),
            ("电子邮件:", self.email_edit),
            ("学院:", self.college_edit),
            ("专业:", self.major_edit),
            ("班级:", self.class_edit),
            ("入学日期:", self.enrollment_date_edit),
        ]:
            edit.setReadOnly(True)
            row = QHBoxLayout()
            label = QLabel(label)
            label.setFixedWidth(80)
            row.addWidget(label)
            row.addWidget(edit)
            group_layout.addLayout(row)

        layout.addWidget(group_box)
        self.setLayout(layout)

        # 加载学生信息
        self.load_student_info()

    def load_student_info(self):
        # 查询学生信息
        student = check(DBManager.student().get_student(int(self.user_id)))
        college = check(DBManager.college().get_college(student.college_id))
        major = check(DBManager.major().get_major(student.major_id))
        class_ = check(DBManager.class_().get_class(student.class_id))

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

