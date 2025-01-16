from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from ..common import BaseConfirmDialog, BaseContextMenuHandler, check
from ..controllers.course import CourseController
from ..page import BasePage


class AddDialog(BaseConfirmDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent, "添加课程")

    def setup_content(self, layout: QVBoxLayout):
        form_layout = QFormLayout()

        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.credits_input = QLineEdit()
        self.name_input.setFixedWidth(200)

        form_layout.addRow("课程代码:", self.id_input)
        form_layout.addRow("课程名称:", self.name_input)
        form_layout.addRow("学分:", self.credits_input)
        layout.addLayout(form_layout)

    def get_course_id(self) -> str:
        return self.id_input.text().strip()

    def get_course_name(self) -> str:
        return self.name_input.text().strip()

    def get_credits(self) -> str:
        return self.credits_input.text().strip()


class EditDialog(BaseConfirmDialog):
    def __init__(self, parent: QWidget, course_id: str, name: str, credits: str):
        super().__init__(parent, "编辑课程")
        self.course_id = course_id
        self.name = name
        self.credits = credits

    def setup_content(self, layout: QVBoxLayout):
        form_layout = QFormLayout()
        self.id_label = QLabel(self.course_id)
        self.name_input = QLineEdit(self.name)
        self.credits_input = QLineEdit(self.credits)
        self.name_input.setFixedWidth(200)

        form_layout.addRow("课程代码:", self.id_label)
        form_layout.addRow("课程名称:", self.name_input)
        form_layout.addRow("学分:", self.credits_input)
        layout.addLayout(form_layout)

    def get_new_name(self) -> str:
        return self.name_input.text().strip()

    def get_new_credits(self) -> str:
        return self.credits_input.text().strip()


class ContextMenuHandler(BaseContextMenuHandler[CourseController]):
    def handle_add(self):
        dialog = AddDialog(self.parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.controller.add(
                dialog.get_course_id(), dialog.get_course_name(), dialog.get_credits()
            )

    def handle_edit(self):
        dialog = EditDialog(
            self.parent,
            cid := self.get_item_value(0),
            self.get_item_value(1),
            self.get_item_value(2),
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.controller.update(cid, dialog.get_new_name(), dialog.get_new_credits())

    def handle_delete(self):
        reply = QMessageBox.question(
            self.parent,
            "确认删除",
            f"确定要删除课程 {self.get_item_value(1)} 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.delete(self.get_item_value(0))

    def setup_menu(self) -> None:
        self.handlers[check(self.menu.addAction("添加"))] = self.handle_add
        if self.item is not None:
            self.handlers[check(self.menu.addAction("编辑"))] = self.handle_edit
            self.handlers[check(self.menu.addAction("删除"))] = self.handle_delete


class CoursePage(BasePage[CourseController]):
    button_name = "课程"
    handler_cls = ContextMenuHandler
    columns = "课程代码", "课程名称", "学分"
    controller_cls = CourseController

    def iterate_table_data(self):
        for item in self.controller.get_all():
            yield (item.course_id, item.name, item.credits)
