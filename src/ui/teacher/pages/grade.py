from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from database.manager import DBManager
from ui.admin.common import BaseConfirmDialog
from ui.common.page import BasePage, PageTitle
from ui.common.selection import SelectionCombo


class ScoreDialog(BaseConfirmDialog):
    def __init__(
        self,
        parent: QWidget,
        student_name: str,
        course_name: str,
        current_score: int | None = None,
    ):
        super().__init__(parent, "学生评分")
        self.student_name = student_name
        self.course_name = course_name
        self.current_grade = current_score

    def setup_content(self, layout: QVBoxLayout) -> None:
        form = QFormLayout()
        layout.addLayout(form)

        form.addRow("学生姓名:", QLabel(self.student_name))
        form.addRow("课程名:", QLabel(self.course_name))
        self.score_input = QLineEdit()
        if self.current_grade is not None:
            self.score_input.setText(str(self.current_grade))
        form.addRow("成绩:", self.score_input)

    def get_score(self):
        return int(self.score_input.text())


class GradePage(BasePage):
    button_name = "学生评分"

    def init_ui(self) -> None:
        layout = QVBoxLayout()

        # 添加标题
        layout.addWidget(PageTitle("学生评分"))

        # 课程选择
        course_box = QHBoxLayout()
        course_box.addStretch()
        course_label = QLabel("选择课程：")
        course_box.addWidget(course_label)
        self.course_combo_layout = QHBoxLayout()
        self.course_combo = self.create_course_combo()
        self.course_combo_layout.addWidget(self.course_combo)
        course_box.addLayout(self.course_combo_layout)
        refresh_course_button = QPushButton("刷新")
        refresh_course_button.clicked.connect(self.refresh_course_combo)
        course_box.addWidget(refresh_course_button)
        layout.addLayout(course_box)

        # 成绩表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["学生ID", "学生姓名", "课程ID", "课程名", "成绩", "操作"]
        )
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.update_table()

    def create_course_combo(self):
        teacher_id = int(self.get_user_id())
        combo = SelectionCombo(
            self,
            [
                (c.course_id, c.name)
                for c in DBManager.course().get_courses_by_teacher(teacher_id)
            ],
            formatter=lambda c: f"{c[0]} - {c[1]}",
        )
        combo.currentIndexChanged.connect(self.update_table)
        return combo

    def refresh_course_combo(self):
        self.course_combo_layout.removeWidget(self.course_combo)
        self.course_combo = self.create_course_combo()
        self.course_combo_layout.addWidget(self.course_combo)

    def update_table(self):
        course_id = self.course_combo.get_selected()[0]
        if course_id is None:
            return

        edb = DBManager.course_enrollment()
        details = [
            detail
            for enrollment in edb.get_course_enrollments(course_id)
            if (detail := edb.get_detail(enrollment))
        ]
        self.table.setRowCount(len(details))

        # slot 闭包
        def slot(detail: tuple[int, str, int, str, int | None]):
            return lambda: self.edit_grade(*detail)

        for row, detail in enumerate(details):
            for col, data in enumerate(detail):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))
            btn = QPushButton("修改成绩")
            btn.clicked.connect(slot(detail))
            self.table.setCellWidget(row, 5, btn)

    def edit_grade(
        self,
        student_id: int,
        student_name: str,
        course_id: int,
        course_name: str,
        current_score: int | None,
    ):
        dialog = ScoreDialog(self, student_name, course_name, current_score)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        score = dialog.get_score()
        if not (0 <= score <= 100):
            QMessageBox.critical(self, "错误", "成绩必须在0-100之间")
            return

        gdb = DBManager.grade()
        try:
            if current_score is None:
                gdb.add_grade(student_id, course_id, score, "2024")
            else:
                gdb.update_grade(student_id, course_id, score=score)
            self.update_table()
        except Exception as err:
            QMessageBox.critical(self, "错误", str(err))
            gdb.rollback()
