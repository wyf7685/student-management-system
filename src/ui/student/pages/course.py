# course.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from database.manager import DBManager
from ui.common.page import BasePage
from utils import check


class CoursePage(BasePage):
    button_name = "课表查询"

    def init_ui(self):
        layout = QVBoxLayout()

        # 添加标题
        title_label = QLabel("课表查询")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # 添加课表信息列表
        self.courses_list = QListWidget()
        layout.addWidget(self.courses_list)

        self.setLayout(layout)

        # 加载课程信息
        self.load_courses()

    def load_courses(self):
        student_id = self.get_user_id()  # 假设 self.user_id 存储了当前学生的学号

        # 确保 student_id 是整数
        if not isinstance(student_id, int):
            try:
                student_id = int(student_id)
            except ValueError:
                self.courses_list.clear()
                self.courses_list.addItem("学号格式不正确")
                return

        # 查询学生信息
        student = check(DBManager.student().get_student(student_id))
        if not student:
            self.courses_list.clear()
            self.courses_list.addItem("学生不存在")
            return

        # 查询班级信息
        class_ = check(DBManager.class_().get_class(student.class_id))
        if not class_:
            self.courses_list.clear()
            self.courses_list.addItem("班级不存在")
            return

        # 假设我们有一个方法来获取班级的课程列表
        # 这里为了简化示例，直接查询所有课程
        courses = check(DBManager.course().get_all_courses())

        self.courses_list.clear()
        if courses:
            for course in courses:
                item_text = f"课程名称: {course.name}, 学分: {course.credits}"
                item = QListWidgetItem(item_text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                font = QFont(self.courses_list.font())
                font.setPointSize(int(font.pointSize() * 1.5))  # 放大字体并转换为整数
                item.setFont(font)
                self.courses_list.addItem(item)
        else:
            self.courses_list.addItem("没有找到相关课程")
