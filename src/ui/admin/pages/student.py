# ruff: noqa: DTZ007

from datetime import datetime

from PyQt6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from ui.common.selection import SelectionCombo

from ..common import (
    BaseConfirmDialog,
    BaseContextMenuHandler,
    ClassSelectionCombo,
    CollegeSelectionCombo,
    MajorSelectionCombo,
    check,
)
from ..controllers.student import StudentController
from ..page import BasePage


class AddDialog(BaseConfirmDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent, "添加学生")

    def setup_content(self, layout: QVBoxLayout):
        form_layout = QFormLayout()

        # 创建输入控件
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.gender_selection = SelectionCombo(self, ["男", "女"])
        self.birth_input = QDateEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.college_selection = CollegeSelectionCombo(self)
        self.major_selection = MajorSelectionCombo(self, self.college_selection)
        self.class_selection = ClassSelectionCombo(self, self.major_selection)
        self.enrollment_input = QDateEdit()

        # 设置宽度
        for widget in [self.name_input, self.phone_input, self.email_input]:
            widget.setFixedWidth(200)

        # 添加到表单
        form_layout.addRow("学号:", self.id_input)
        form_layout.addRow("姓名:", self.name_input)
        form_layout.addRow("性别:", self.gender_selection)
        form_layout.addRow("出生日期:", self.birth_input)
        form_layout.addRow("手机:", self.phone_input)
        form_layout.addRow("邮箱:", self.email_input)
        form_layout.addRow("学院:", self.college_selection)
        form_layout.addRow("专业:", self.major_selection)
        form_layout.addRow("班级:", self.class_selection)
        form_layout.addRow("入学日期:", self.enrollment_input)

        layout.addLayout(form_layout)

    def get_values(self) -> tuple:
        return (
            self.id_input.text().strip(),
            self.name_input.text().strip(),
            "M" if self.gender_selection.get_selected() == "男" else "F",
            self.birth_input.date().toPyDate().strftime("%Y-%m-%d"),
            self.phone_input.text().strip(),
            self.email_input.text().strip(),
            self.college_selection.get_selected()[0],
            self.major_selection.get_selected()[0],
            self.class_selection.get_selected()[0],
            self.enrollment_input.date().toPyDate().strftime("%Y-%m-%d"),
        )


class EditDialog(BaseConfirmDialog):
    def __init__(self, parent: QWidget, student_data: tuple[str, ...]):
        super().__init__(parent, "编辑学生")
        self.student_data = student_data

    def setup_content(self, layout: QVBoxLayout):
        form_layout = QFormLayout()

        # ID显示
        self.id_label = QLabel(self.student_data[0])

        # 其他输入控件
        self.name_input = QLineEdit(self.student_data[1])
        self.gender_input = QComboBox()
        self.gender_input.addItems(["男", "女"])
        self.gender_input.setCurrentText(self.student_data[2])
        self.birth_input = QDateEdit()
        self.birth_input.setDate(datetime.strptime(self.student_data[3], "%Y-%m-%d").date())

        self.phone_input = QLineEdit(self.student_data[4])
        self.email_input = QLineEdit(self.student_data[5])
        self.college_selection = CollegeSelectionCombo(self, int(self.student_data[6]))
        self.major_selection = MajorSelectionCombo(
            self,
            self.college_selection,
            int(self.student_data[7]),
        )
        self.class_selection = ClassSelectionCombo(
            self,
            self.major_selection,
            int(self.student_data[8]),
        )

        self.enrollment_input = QDateEdit()
        self.enrollment_input.setDate(datetime.strptime(self.student_data[9], "%Y-%m-%d").date())

        # 添加到表单
        form_layout.addRow("学号:", self.id_label)
        form_layout.addRow("姓名:", self.name_input)
        form_layout.addRow("性别:", self.gender_input)
        form_layout.addRow("出生日期:", self.birth_input)
        form_layout.addRow("手机:", self.phone_input)
        form_layout.addRow("邮箱:", self.email_input)
        form_layout.addRow("学院代码:", self.college_selection)
        form_layout.addRow("专业代码:", self.major_selection)
        form_layout.addRow("班级代码:", self.class_selection)
        form_layout.addRow("入学日期:", self.enrollment_input)

        layout.addLayout(form_layout)

    def get_values(self) -> tuple:
        return (
            self.name_input.text().strip(),
            "M" if self.gender_input.currentText() == "男" else "F",
            self.birth_input.date().toPyDate().strftime("%Y-%m-%d"),
            self.phone_input.text().strip(),
            self.email_input.text().strip(),
            self.college_selection.get_selected()[0],
            self.major_selection.get_selected()[0],
            self.class_selection.get_selected()[0],
            self.enrollment_input.date().toPyDate().strftime("%Y-%m-%d"),
        )


class ContextMenuHandler(BaseContextMenuHandler[StudentController]):
    def handle_add(self):
        dialog = AddDialog(self.parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.controller.add(*dialog.get_values())

    def handle_edit(self):
        values = tuple(self.get_item_value(i) for i in range(10))
        dialog = EditDialog(self.parent, values)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.controller.update(values[0], *dialog.get_values())

    def handle_delete(self):
        reply = QMessageBox.question(
            self.parent,
            "确认删除",
            f"确定要删除学生 {self.get_item_value(1)} 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.delete(self.get_item_value(0))

    def setup_menu(self) -> None:
        self.handlers[check(self.menu.addAction("添加"))] = self.handle_add
        if self.item is not None:
            self.handlers[check(self.menu.addAction("编辑"))] = self.handle_edit
            self.handlers[check(self.menu.addAction("删除"))] = self.handle_delete


class StudentPage(BasePage[StudentController]):
    button_name = "学生"
    handler_cls = ContextMenuHandler
    columns = (
        "学号",
        "姓名",
        "性别",
        "出生日期",
        "手机",
        "邮箱",
        "学院代码",
        "专业代码",
        "班级代码",
        "入学日期",
    )
    controller_cls = StudentController

    def iterate_table_data(self):
        for item in self.controller.get_all():
            yield (
                item.student_id,
                item.name,
                "男" if item.gender == "M" else "女",
                item.birth.strftime("%Y-%m-%d"),
                item.phone,
                item.email,
                item.college_id,
                item.major_id,
                item.class_id,
                item.enrollment_date.strftime("%Y-%m-%d"),
            )
