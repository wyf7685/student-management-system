from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout

from database.manager import DBManager
from ui.common.page import BasePage
from utils import check


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
        labels = ["考试ID", "课程名称", "时间", "持续时间", "名称", "描述", "地点"]
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(labels))
        self.table_widget.setHorizontalHeaderLabels(labels)

        # 获取考试信息
        exams = DBManager.exam().get_exam_by_student_id(int(self.get_user_id()))
        cdb = DBManager.course()
        courses = {
            exam.course_id: check(cdb.get_course(exam.course_id)).name for exam in exams
        }

        # 设置表格的行数
        self.table_widget.setRowCount(len(exams))

        # 填充表格数据
        for row, exam in enumerate(exams):
            data = (
                exam.exam_id,
                courses[exam.course_id],
                exam.time.strftime("%Y-%m-%d %H:%M:%S"),
                exam.duration,
                exam.name,
                exam.description,
                exam.location,
            )
            for col, item in enumerate(data):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(item)))

        # 将表格添加到布局中
        layout.addWidget(self.table_widget)

        # 设置布局
        self.setLayout(layout)
