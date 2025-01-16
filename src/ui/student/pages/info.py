from PyQt6.QtWidgets import QFormLayout, QLineEdit, QVBoxLayout

from database.manager import StudentDBManager
from ui.common.page import BasePage


class InfoPage(BasePage):
    button_name = "个人信息"

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # 创建只读文本框
        self.id_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.gender_edit = QLineEdit()
        self.age_edit = QLineEdit()
        self.class_edit = QLineEdit()
        self.dept_edit = QLineEdit()
        self.major_edit = QLineEdit()

        # 设置只读
        for edit in [
            self.id_edit,
            self.name_edit,
            self.gender_edit,
            self.age_edit,
            self.class_edit,
            self.dept_edit,
            self.major_edit,
        ]:
            edit.setReadOnly(True)

        # 添加到表单布局
        form_layout.addRow("学号:", self.id_edit)
        form_layout.addRow("姓名:", self.name_edit)
        form_layout.addRow("性别:", self.gender_edit)
        # form_layout.addRow("年龄:", self.age_edit)
        # form_layout.addRow("班级:", self.class_edit)
        # form_layout.addRow("院系:", self.dept_edit)
        # form_layout.addRow("专业:", self.major_edit)

        layout.addLayout(form_layout)
        self.setLayout(layout)

        # 加载学生信息
        self.load_student_info()

    def load_student_info(self):
        # 查询学生信息
        db_manager = StudentDBManager()
        student = db_manager.get_student(int(self.user_id))

        if student:
            self.id_edit.setText(str(student.student_id))
            self.name_edit.setText(student.name)
            self.gender_edit.setText("男" if student.gender == "M" else "女")
            # self.age_edit.setText(str(student.age))
            # self.class_edit.setText(student.class_name)
            # self.dept_edit.setText(student.department)
            # self.major_edit.setText(student.major)
