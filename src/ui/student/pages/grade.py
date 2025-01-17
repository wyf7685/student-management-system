from PyQt6.QtWidgets import (
    QHeaderView,
    QSizePolicy,
    QTableWidgetItem,
    QVBoxLayout,
)

from database.manager import DBManager
from ui.common.page import BasePage, PageTitle
from ui.common.readonly_table import ReadonlyTableWidget
from utils import check


class GradePage(BasePage):
    button_name = "成绩查询"

    def init_ui(self):
        # 创建一个垂直布局
        layout = QVBoxLayout()
        layout.addWidget(PageTitle("成绩查询"))

        self.table_widget = ReadonlyTableWidget(["课程名称", "成绩", "学期"])
        self.table_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        if header := self.table_widget.horizontalHeader():
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # 获取成绩信息
        grades = DBManager.grade().get_all_grades()

        # 设置表格的行数
        self.table_widget.setRowCount(len(grades))

        # 填充表格数据
        for row, grade in enumerate(grades):
            course = check(DBManager.course().get_course(grade.course_id))
            self.table_widget.setItem(row, 0, QTableWidgetItem(course.name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(grade.score)))
            self.table_widget.setItem(row, 2, QTableWidgetItem(grade.term))

        # 将表格添加到布局中
        layout.addWidget(self.table_widget)

        # 设置布局的边距为0
        layout.setContentsMargins(0, 0, 0, 0)

        # 设置布局
        self.setLayout(layout)
