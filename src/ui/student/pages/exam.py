from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from database.manager import DBManager
from database.models import Exam
from ui.common.page import BasePage


class ExamPage(BasePage):
    button_name = "考试查询"

    def init_ui(self):
        # 创建一个垂直布局
        layout = QVBoxLayout()

        title_label = QLabel("考试查询")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # 创建一个 QTableWidget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(
            ["考试ID", "课程ID", "时间", "持续时间", "名称", "描述", "地点"]
        )

        # 获取考试信息
        exams = DBManager.exam().get_all_exams()

        # 设置表格的行数
        self.table_widget.setRowCount(len(exams))

        # 填充表格数据
        for row, exam in enumerate(exams):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(exam.exam_id)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(exam.course_id)))
            self.table_widget.setItem(
                row, 2, QTableWidgetItem(exam.time.strftime("%Y-%m-%d %H:%M:%S"))
            )
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(exam.duration)))
            self.table_widget.setItem(row, 4, QTableWidgetItem(exam.name))
            self.table_widget.setItem(row, 5, QTableWidgetItem(exam.description))
            self.table_widget.setItem(row, 6, QTableWidgetItem(exam.location))

        # 将表格添加到布局中
        layout.addWidget(self.table_widget)

        # 设置布局
        self.setLayout(layout)
