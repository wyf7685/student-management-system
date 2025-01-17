# course.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from database.manager import DBManager
from ui.common.page import BasePage, PageTitle
from utils import check


class CoursePage(BasePage):
    button_name = "课程信息查询"

    def init_ui(self):
        layout = QVBoxLayout()

        # 添加标题
        layout.addWidget(PageTitle("课程信息查询"))

        # 添加课表信息列表
        self.courses_list = QListWidget()
        self.courses_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: 1px solid palette(mid);
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                background-color: palette(base);
                border: 1px solid palette(midlight);
                border-radius: 5px;
                margin: 5px;
                padding: 10px;
            }
            QListWidget::item:hover {
                background-color: palette(highlight);
            }
            QListWidget::item:selected {
                background-color: palette(highlight);
                font-weight: bold;
                color: palette(text);  /* 使用系统默认字体颜色 */
            }
        """)
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
                item = QListWidgetItem(QIcon("path/to/icon.png"), item_text)  # 添加图标
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                font = QFont(self.courses_list.font())
                font.setPointSize(int(font.pointSize() * 1.5))  # 放大字体并转换为整数
                item.setFont(font)
                self.courses_list.addItem(item)
        else:
            item = QListWidgetItem("没有找到相关课程")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            font = QFont(self.courses_list.font())
            font.setPointSize(int(font.pointSize() * 1.5))  # 放大字体并转换为整数
            item.setFont(font)
            self.courses_list.addItem(item)
