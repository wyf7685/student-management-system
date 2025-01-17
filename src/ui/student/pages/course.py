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
    button_name = "课程信息查询"

    def init_ui(self):
        layout = QVBoxLayout()

        # 添加标题
        title_label = QLabel("课程信息查询")
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
        student_id = int(self.get_user_id())
        enrollments = DBManager.course_enrollment().get_student_enrollments(student_id)
        cdb = DBManager.course()

        self.courses_list.clear()
        if enrollments:
            for enrollment in enrollments:
                course = check(cdb.get_course(enrollment.course_id))
                item_text = f"课程名称: {course.name}, 学分: {course.credits}"
                item = QListWidgetItem(item_text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                font = QFont(self.courses_list.font())
                font.setPointSize(int(font.pointSize() * 1.5))  # 放大字体并转换为整数
                item.setFont(font)
                self.courses_list.addItem(item)
        else:
            self.courses_list.addItem("没有找到相关课程")
