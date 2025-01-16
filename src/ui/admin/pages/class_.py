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
from ..controllers.class_ import ClassController
from ..page import BasePage


class AddDialog(BaseConfirmDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent, "添加班级")

    def setup_content(self, layout: QVBoxLayout):
        form_layout = QFormLayout()

        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.major_id_input = QLineEdit()
        self.year_input = QLineEdit()
        self.name_input.setFixedWidth(200)

        form_layout.addRow("班级代码:", self.id_input)
        form_layout.addRow("班级名称:", self.name_input)
        form_layout.addRow("专业代码:", self.major_id_input)
        form_layout.addRow("年级:", self.year_input)
        layout.addLayout(form_layout)

    def get_class_id(self) -> str:
        return self.id_input.text().strip()

    def get_class_name(self) -> str:
        return self.name_input.text().strip()

    def get_major_id(self) -> str:
        return self.major_id_input.text().strip()

    def get_year(self) -> str:
        return self.year_input.text().strip()


class EditDialog(BaseConfirmDialog):
    def __init__(
        self,
        parent: QWidget,
        class_id: str,
        name: str,
        major_id: str,
        year: str,
    ):
        super().__init__(parent, "编辑班级")
        self.class_id = class_id
        self.name = name
        self.major_id = major_id
        self.year = year

    def setup_content(self, layout: QVBoxLayout):
        form_layout = QFormLayout()

        self.id_label = QLabel(self.class_id)
        self.name_input = QLineEdit(self.name)
        self.major_id_input = QLineEdit(self.major_id)
        self.year_input = QLineEdit(self.year)
        self.name_input.setFixedWidth(200)

        form_layout.addRow("班级代码:", self.id_label)
        form_layout.addRow("班级名称:", self.name_input)
        form_layout.addRow("专业代码:", self.major_id_input)
        form_layout.addRow("年级:", self.year_input)
        layout.addLayout(form_layout)

    def get_new_name(self) -> str:
        return self.name_input.text().strip()

    def get_new_major_id(self) -> str:
        return self.major_id_input.text().strip()

    def get_new_year(self) -> str:
        return self.year_input.text().strip()


class ContextMenuHandler(BaseContextMenuHandler[ClassController]):
    def handle_add(self):
        dialog = AddDialog(self.parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.controller.add(
                dialog.get_class_id(),
                dialog.get_class_name(),
                dialog.get_major_id(),
                dialog.get_year(),
            )

    def handle_edit(self):
        dialog = EditDialog(
            self.parent,
            cid := self.get_item_value(0),
            self.get_item_value(1),
            self.get_item_value(2),
            self.get_item_value(3),
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.controller.update(
                cid,
                dialog.get_new_name(),
                dialog.get_new_major_id(),
                dialog.get_new_year(),
            )

    def handle_delete(self):
        reply = QMessageBox.question(
            self.parent,
            "确认删除",
            f"确定要删除班级 {self.get_item_value(1)} 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.delete(self.get_item_value(0))

    def setup_menu(self) -> None:
        self.handlers[check(self.menu.addAction("添加"))] = self.handle_add
        if self.item is not None:
            self.handlers[check(self.menu.addAction("编辑"))] = self.handle_edit
            self.handlers[check(self.menu.addAction("删除"))] = self.handle_delete


class ClassPage(BasePage[ClassController]):
    button_name = "班级"
    handler_cls = ContextMenuHandler
    columns = "班级代码", "班级名称", "专业代码", "年级"
    controller_cls = ClassController

    def iterate_table_data(self):
        for item in self.controller.get_all():
            yield (item.class_id, item.name, item.major_id, item.year)
