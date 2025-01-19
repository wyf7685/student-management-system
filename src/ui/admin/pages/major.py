from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from ..common import (
    BaseConfirmDialog,
    BaseContextMenuHandler,
    CollegeSelectionCombo,
    check,
)
from ..controllers.major import MajorController
from ..page import BasePage


class AddDialog(BaseConfirmDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent, "添加专业")

    def setup_content(self, layout: QVBoxLayout):
        form_layout = QFormLayout()

        # 创建控件
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.college_selection = CollegeSelectionCombo(self)
        self.name_input.setFixedWidth(200)

        # 添加到表单
        form_layout.addRow("专业代码:", self.id_input)
        form_layout.addRow("专业名称:", self.name_input)
        form_layout.addRow("学院代码:", self.college_selection)
        layout.addLayout(form_layout)

    def get_major_id(self) -> str:
        return self.id_input.text().strip()

    def get_major_name(self) -> str:
        return self.name_input.text().strip()

    def get_college_id(self) -> int:
        return self.college_selection.get_selected()[0]


class EditDialog(BaseConfirmDialog):
    def __init__(
        self,
        parent: QWidget,
        major_id: str,
        major_name: str,
        college_id: str,
    ):
        super().__init__(parent, "编辑专业")
        self.major_id = major_id
        self.major_name = major_name
        self.college_id = college_id

    def setup_content(self, layout: QVBoxLayout):
        form_layout = QFormLayout()
        self.id_label = QLabel(self.major_id)
        self.name_input = QLineEdit()
        self.college_selection = CollegeSelectionCombo(self, int(self.college_id))
        self.name_input.setFixedWidth(200)

        # 设置默认值
        self.name_input.setText(self.major_name)

        # 添加到表单
        form_layout.addRow("专业名称:", self.name_input)
        form_layout.addRow("学院代码:", self.college_selection)
        layout.addLayout(form_layout)

    def get_new_name(self) -> str:
        return self.name_input.text().strip()

    def get_new_college_id(self) -> int:
        return self.college_selection.get_selected()[0]


class ContextMenuHandler(BaseContextMenuHandler[MajorController]):
    def handle_add(self):
        dialog = AddDialog(self.parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.controller.add(
                dialog.get_major_id(),
                dialog.get_major_name(),
                dialog.get_college_id(),
            )

    def handle_edit(self):
        dialog = EditDialog(
            self.parent,
            mid := self.get_item_value(0),
            self.get_item_value(1),
            self.get_item_value(2),
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.controller.update(
                mid,
                dialog.get_new_name(),
                dialog.get_new_college_id(),
            )

    def handle_delete(self):
        reply = QMessageBox.question(
            self.parent,
            "确认删除",
            f"确定要删除专业 {self.get_item_value(1)} 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.delete(self.get_item_value(0))

    def setup_menu(self) -> None:
        self.handlers[check(self.menu.addAction("添加"))] = self.handle_add
        if self.item is not None:
            self.handlers[check(self.menu.addAction("编辑"))] = self.handle_edit
            self.handlers[check(self.menu.addAction("删除"))] = self.handle_delete


class MajorPage(BasePage[MajorController]):
    button_name = "专业"
    handler_cls = ContextMenuHandler
    columns = "专业代码", "专业名称", "学院代码"
    controller_cls = MajorController

    def iterate_table_data(self):
        for item in self.controller.get_all():
            yield (item.major_id, item.name, item.college_id)
