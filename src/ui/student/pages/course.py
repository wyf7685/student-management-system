from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from database.manager import DBManager
from ui.common.page import BasePage, PageTitle
from utils import check

COURSE_LIST_STYLESHEET = """
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
"""


class CoursePage(BasePage):
    button_name = "课程信息查询"

    def init_ui(self):
        layout = QVBoxLayout()

        # 添加标题
        layout.addWidget(PageTitle("课程信息查询"))

        # 添加课表信息列表
        self.courses_list = QListWidget()
        self.courses_list.setStyleSheet(COURSE_LIST_STYLESHEET)
        layout.addWidget(self.courses_list)

        self.setLayout(layout)

        # 加载课程信息
        self.load_courses()

    def create_list_item(self, text: str) -> QListWidgetItem:
        item = QListWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont(self.courses_list.font())
        font.setPointSize(int(font.pointSize() * 1.5))  # 放大字体并转换为整数
        item.setFont(font)
        return item

    def load_courses(self):
        self.courses_list.clear()

        student_id = int(self.get_user_id())
        enrollments = DBManager.course_enrollment().get_student_enrollments(student_id)

        if not enrollments:
            item = self.create_list_item("没有找到相关课程")
            self.courses_list.addItem(item)
            return

        cdb = DBManager.course()
        for enrollment in enrollments:
            course = check(cdb.get_course(enrollment.course_id))
            item_text = f"课程名称: {course.name}, 学分: {course.credits}"
            item = self.create_list_item(item_text)
            self.courses_list.addItem(item)
