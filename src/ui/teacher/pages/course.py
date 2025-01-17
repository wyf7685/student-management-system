from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QSpinBox,
    QTableWidgetItem,
    QVBoxLayout,
)

from database import DBManager
from ui.common.page import BasePage, PageTitle
from ui.common.readonly_table import ReadonlyTableWidget


class SemesterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择学期")
        layout = QFormLayout(self)

        # 起止年份
        self.year_start = QSpinBox()
        self.year_start.setRange(2020, 2030)
        self.year_start.setValue(2023)
        layout.addRow("起始年份:", self.year_start)

        # 学期选择
        self.semester = QComboBox()
        self.semester.addItems(["1", "2"])
        layout.addRow("学期:", self.semester)

        # 确认取消按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_semester(self) -> str:
        year = self.year_start.value()
        sem = self.semester.currentText()
        return f"{year}-{year + 1}-{sem}"


class CoursePage(BasePage):
    button_name = "课程管理"

    def init_ui(self) -> None:
        self.teacher_id = int(self.get_user_id())
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 添加标题
        layout.addWidget(PageTitle("课程管理"))

        # 添加输入框和查询按钮
        input_group_box = QGroupBox()
        input_group_layout = QHBoxLayout()
        input_group_box.setLayout(input_group_layout)
        input_group_layout.addWidget(QLabel("请输入搜索关键词:"))
        self.keyword_edit = QLineEdit()
        input_group_layout.addWidget(self.keyword_edit)
        self.search_button = QPushButton("查询")
        input_group_layout.addWidget(self.search_button)
        layout.addWidget(input_group_box)

        # 添加课程信息表格
        self.course_table = ReadonlyTableWidget(["课程ID", "课程名称", "学期", "状态"])
        self.course_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.course_table.customContextMenuRequested.connect(self.handle_list_context_menu)
        header = self.course_table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.course_table)

        # 添加提示信息
        self.hint_label = QLabel("右键开设课程，再次右键取消授课")
        self.hint_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(self.hint_label)

        self.search_button.clicked.connect(self.update_course_list)
        self.update_course_list()

    def update_course_list(self) -> None:
        keyword = self.keyword_edit.text().strip()

        db = DBManager.course()
        courses = db.search_course(keyword) if keyword else db.get_all_courses()
        teaching = {
            course.course_id: course.semester
            for course in DBManager.course_teacher().get_courses_by_teacher(self.teacher_id)
        }
        courses.sort(key=lambda c: (c.course_id not in teaching, c.course_id))

        self.course_table.setRowCount(len(courses))
        for row, course in enumerate(courses):
            status = "正在授课" if course.course_id in teaching else "未授课"
            semester_info = teaching.get(course.course_id, "")

            item_id = QTableWidgetItem(str(course.course_id))
            item_id.setFont(QFont("Arial", 12))
            self.course_table.setItem(row, 0, item_id)

            item_name = QTableWidgetItem(course.name)
            item_name.setFont(QFont("Arial", 12))
            self.course_table.setItem(row, 1, item_name)

            item_semester = QTableWidgetItem(semester_info)
            item_semester.setFont(QFont("Arial", 12))
            self.course_table.setItem(row, 2, item_semester)

            item_status = QTableWidgetItem(status)
            item_status.setFont(QFont("Arial", 12))
            self.course_table.setItem(row, 3, item_status)

        self.teaching = teaching
        self.courses = [c.course_id for c in courses]

    def handle_list_context_menu(self, pos: QPoint):
        current_item = self.course_table.itemAt(pos)
        if not current_item:
            return

        row = current_item.row()
        course_id = self.courses[row]
        if course_id not in self.teaching:
            menu = self.create_teach_ctx_menu(course_id)
        else:
            menu = self.create_stop_ctx_menu(course_id)
        menu.exec(self.course_table.mapToGlobal(pos))
        self.update_course_list()

    def create_teach_ctx_menu(self, course_id: int):
        menu = QMenu(self)
        teach_action = QAction("开设课程", self)

        def on_teach():
            dialog = SemesterDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                semester = dialog.get_semester()
                DBManager.course_teacher().add_course_teacher(course_id, self.teacher_id, semester)

        teach_action.triggered.connect(on_teach)
        menu.addAction(teach_action)
        return menu

    def create_stop_ctx_menu(self, course_id: int):
        menu = QMenu(self)
        stop_action = QAction("停止授课", self)
        stop_action.triggered.connect(
            lambda: DBManager.course_teacher().delete_course_teacher(course_id, self.teacher_id)
        )
        menu.addAction(stop_action)
        return menu
