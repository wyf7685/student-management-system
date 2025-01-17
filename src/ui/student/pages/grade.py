from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout

from database.manager import DBManager
from ui.common.page import BasePage, PageTitle
from utils import check


class GradePage(BasePage):
    button_name = "成绩查询"

    def init_ui(self):
        # 创建一个垂直布局
        layout = QVBoxLayout()
        layout.addWidget(PageTitle("成绩查询"))

        # 创建一个 QTableWidget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["课程名称", "成绩", "学期"])

        # 获取成绩信息
        grades = DBManager.grade().get_all_grades()

        # 设置表格的行数
        self.table_widget.setRowCount(len(grades))

        # 填充表格数据
        for row, grade in enumerate(grades):
            course = check(DBManager.course().get_course(grade.course_id))
            # self.table_widget.setItem(row, 0, QTableWidgetItem(str(grade.student_id)))
            self.table_widget.setItem(row, 0, QTableWidgetItem(course.name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(grade.score)))
            self.table_widget.setItem(row, 2, QTableWidgetItem(grade.term))

        # 将表格添加到布局中
        layout.addWidget(self.table_widget)

        # 设置布局
        self.setLayout(layout)
