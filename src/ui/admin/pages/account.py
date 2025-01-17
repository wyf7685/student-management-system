from collections.abc import Generator

from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from database.manager import DBManager
from ui.common.selection import SelectionCombo
from utils import check

from ..common import BaseConfirmDialog, BaseContextMenuHandler
from ..controllers.account import SystemAccountController
from ..page import BasePage

ROLE_CONVERT = {
    "管理员": "Admin",
    "教师": "Teacher",
    "学生": "Student",
    "Admin": "管理员",
    "Teacher": "教师",
    "Student": "学生",
}


class AddDialog(BaseConfirmDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent, "添加系统账号")

    def setup_content(self, layout: QVBoxLayout):
        self.form_layout = form = QFormLayout()
        layout.addLayout(form)

        # 账号类型选择
        self.role_selection = SelectionCombo(self, ["学生", "教师", "管理员"])
        self.role_selection.currentTextChanged.connect(self.on_role_changed)
        form.addRow("账号类型:", self.role_selection)

        self.student_select = SelectionCombo(
            self,
            inner_data=[
                (student.student_id, student.name)
                for student in DBManager.student().get_all_students()
            ],
            formatter=lambda student: f"{student[0]} - {student[1]}",
        )
        form.addRow("选择学生:", self.student_select)

        self.teacher_select = SelectionCombo(
            self,
            inner_data=[
                (teacher.teacher_id, teacher.name)
                for teacher in DBManager.teacher().get_all_teachers()
            ],
            formatter=lambda teacher: f"{teacher[0]} - {teacher[1]}",
        )
        form.addRow("选择教师:", self.teacher_select)

        self.admin_id_edit = QLineEdit()
        form.addRow("输入管理员ID:", self.admin_id_edit)

        form.setRowVisible(2, False)
        form.setRowVisible(3, False)

    def on_role_changed(self, role: str):
        rows = {"学生": 1, "教师": 2, "管理员": 3}
        for i in rows.values():
            self.form_layout.setRowVisible(i, False)
        self.form_layout.setRowVisible(rows[role], True)

    def get_role(self) -> str:
        return ROLE_CONVERT[self.role_selection.currentText()]

    def get_user_id(self) -> str:
        match self.role_selection.get_selected():
            case "学生":
                return str(self.student_select.get_selected()[0])
            case "教师":
                return str(self.teacher_select.get_selected()[0])
            case "管理员":
                return self.admin_id_edit.text()
        return ""


class EditDialog(BaseConfirmDialog):
    def __init__(self, parent: QWidget, role: str, user_id: str) -> None:
        super().__init__(parent, "修改系统账号")
        self.role = role
        self.user_id = user_id

    def setup_content(self, layout: QVBoxLayout):
        form = QFormLayout()
        layout.addLayout(form)
        form.addRow("账号类型:", QLabel(self.role))
        form.addRow(f"{self.role} ID:", QLabel(self.user_id))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("新密码:", self.password_edit)

    def get_password(self) -> str:
        return self.password_edit.text()


class ContextMenuHandler(BaseContextMenuHandler[SystemAccountController]):
    def handle_add(self):
        dialog = AddDialog(self.parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            role = dialog.get_role()
            user_id = dialog.get_user_id()
            if DBManager.system_account().exists_account(role, user_id):
                QMessageBox.warning(
                    self.parent,
                    "警告",
                    f"{ROLE_CONVERT[role]}账号 {user_id} 已存在",
                )
                return

            self.controller.add(
                dialog.get_role(),
                dialog.get_user_id(),
                "123456",
            )

    def handle_edit(self):
        role = self.get_item_value(1)
        user_id = self.get_item_value(2)
        dialog = EditDialog(self.parent, role, user_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            password = dialog.get_password()
            if not password:
                QMessageBox.warning(self.parent, "警告", "密码不能为空")
                return

            self.controller.update_password(ROLE_CONVERT[role], user_id, password)

    def handle_delete(self):
        role = self.get_item_value(1)
        user_id = self.get_item_value(2)
        name = self.get_item_value(3)
        reply = QMessageBox.question(
            self.parent,
            "确认删除",
            f"确定要删除 {role} 账号 {name} 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.delete(role, user_id)

    def setup_menu(self) -> None:
        self.handlers[check(self.menu.addAction("添加账号"))] = self.handle_add
        if self.item is not None:
            self.handlers[check(self.menu.addAction("修改密码"))] = self.handle_edit
            self.handlers[check(self.menu.addAction("删除账号"))] = self.handle_delete


class AccountPage(BasePage[SystemAccountController]):
    button_name = "系统账号"
    handler_cls = ContextMenuHandler
    columns = "账号 ID", "身份", "用户 ID", "名称"
    controller_cls = SystemAccountController

    def iterate_table_data(self) -> Generator[tuple[object, ...]]:
        for item in sorted(
            self.controller.get_all(),
            key=lambda x: (x.role, x.id),
        ):
            name = item.user_id
            if item.role == "Student":
                stu = DBManager.student().get_student(int(name))
                name = check(stu).name
            elif item.role == "Teacher":
                tea = DBManager.teacher().get_teacher(int(name))
                name = check(tea).name
            yield (item.id, ROLE_CONVERT[item.role], item.user_id, name)
