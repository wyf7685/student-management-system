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
from ..controllers.college import CollegeController
from ._base import BaseTab


class AddDialog(BaseConfirmDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent, "添加学院")

    def setup_content(self, layout: QVBoxLayout):
        form_layout = QFormLayout()

        # 创建控件
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.name_input.setFixedWidth(200)

        # 添加到表单
        form_layout.addRow("学院代码:", self.id_input)
        form_layout.addRow("学院名称:", self.name_input)
        layout.addLayout(form_layout)

    def get_college_id(self) -> str:
        return self.id_input.text().strip()

    def get_college_name(self) -> str:
        return self.name_input.text().strip()


class EditDialog(BaseConfirmDialog):
    def __init__(
        self,
        parent: QWidget,
        college_id: str,
        college_name: str,
    ):
        super().__init__(parent, "编辑学院")
        self.college_id = college_id
        self.college_name = college_name

    def setup_content(self, layout: QVBoxLayout):
        form_layout = QFormLayout()
        self.id_label = QLabel(self.college_id)
        self.name_input = QLineEdit(self.college_name)
        self.name_input.setFixedWidth(200)

        # 添加到表单
        form_layout.addRow("学院代码:", self.id_label)
        form_layout.addRow("学院名称:", self.name_input)
        layout.addLayout(form_layout)

    def get_new_name(self) -> str:
        return self.name_input.text().strip()


class ContextMenuHandler(BaseContextMenuHandler[CollegeController]):
    def handle_add(self):
        dialog = AddDialog(self.parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.controller.add(dialog.get_college_id(), dialog.get_college_name())

    def handle_edit(self):
        dialog = EditDialog(
            self.parent,
            cid := self.get_item_value(0),
            self.get_item_value(1),
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.controller.update(cid, dialog.get_new_name())

    def handle_delete(self):
        reply = QMessageBox.question(
            self.parent,
            "确认删除",
            f"确定要删除学院 {self.get_item_value(1)} 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.delete(self.get_item_value(0))

    def setup_menu(self) -> None:
        self.handlers[check(self.menu.addAction("添加"))] = self.handle_add
        if self.item is not None:
            self.handlers[check(self.menu.addAction("编辑"))] = self.handle_edit
            self.handlers[check(self.menu.addAction("删除"))] = self.handle_delete


class CollegeTab(BaseTab[CollegeController]):
    tab_name = "学院"
    handler_cls = ContextMenuHandler
    columns = "学院代码", "学院名称"
    controller_cls = CollegeController

    def iterate_table_data(self):
        for item in self.controller.get_all():
            yield (item.college_id, item.name)
