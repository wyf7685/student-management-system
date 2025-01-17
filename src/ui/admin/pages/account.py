from collections.abc import Generator

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from database.manager import DBManager
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


def create_student_select(widget: QWidget):
    layout = QHBoxLayout()
    widget.setLayout(layout)
    layout.addWidget(QLabel("选择学生:"))
    combo = QComboBox()
    layout.addWidget(combo)

    students = [
        (student.student_id, student.name)
        for student in DBManager.student().get_all_students()
    ]
    combo.addItems([f"{id} - {name}" for id, name in students])

    return students, combo


def create_teacher_select(widget: QWidget):
    layout = QHBoxLayout()
    widget.setLayout(layout)
    layout.addWidget(QLabel("选择教师:"))
    combo = QComboBox()
    layout.addWidget(combo)

    teachers = [
        (teacher.teacher_id, teacher.name)
        for teacher in DBManager.teacher().get_all_teachers()
    ]
    combo.addItems([f"{id} - {name}" for id, name in teachers])

    return teachers, combo


class AddDialog(BaseConfirmDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent, "添加系统账号")

    def setup_content(self, layout: QVBoxLayout):
        # 账号类型选择
        role_layout = QHBoxLayout()
        role_layout.addWidget(QLabel("账号类型:"))
        self.role_combo = QComboBox()
        self.role_combo.addItems(["学生", "教师", "管理员"])
        self.role_combo.setCurrentText("学生")
        self.role_combo.currentTextChanged.connect(self.on_role_changed)
        role_layout.addWidget(self.role_combo)
        layout.addLayout(role_layout)

        self.student_id_widget = QWidget()
        self.student_id_widget.setVisible(True)
        layout.addWidget(self.student_id_widget)
        self.students, self.student_id_combo = create_student_select(
            self.student_id_widget
        )

        self.teacher_id_widget = QWidget()
        self.teacher_id_widget.setVisible(False)
        layout.addWidget(self.teacher_id_widget)
        self.teachers, self.teacher_id_combo = create_teacher_select(
            self.teacher_id_widget
        )

        self.admin_widget = QWidget()
        self.admin_widget.setVisible(False)
        layout.addWidget(self.admin_widget)
        admin_layout = QHBoxLayout()
        self.admin_widget.setLayout(admin_layout)
        admin_layout.addWidget(QLabel("输入管理员ID:"))
        self.admin_id_edit = QLineEdit()
        admin_layout.addWidget(self.admin_id_edit)

    def on_role_changed(self, role: str):
        self.student_id_widget.setVisible(False)
        self.teacher_id_widget.setVisible(False)
        self.admin_widget.setVisible(False)

        match role:
            case "学生":
                self.student_id_widget.setVisible(True)
            case "教师":
                self.teacher_id_widget.setVisible(True)
            case "管理员":
                self.admin_widget.setVisible(True)

    def get_role(self) -> str:
        return ROLE_CONVERT[self.role_combo.currentText()]

    def get_user_id(self) -> str:
        match self.role_combo.currentText():
            case "学生":
                idx = self.student_id_combo.currentIndex()
                return str(self.students[idx][0])
            case "教师":
                idx = self.teacher_id_combo.currentIndex()
                return str(self.teachers[idx][0])
            case "管理员":
                return self.admin_id_edit.text()
        return ""


class EditDialog(BaseConfirmDialog):
    def __init__(self, parent: QWidget, role: str, user_id: str) -> None:
        super().__init__(parent, "修改系统账号")
        self.role = role
        self.user_id = user_id

    def setup_content(self, layout: QVBoxLayout):
        role_layout = QHBoxLayout()
        role_layout.addWidget(QLabel("账号类型:"))
        role_layout.addWidget(QLabel(self.role))
        layout.addLayout(role_layout)

        user_id_layout = QHBoxLayout()
        user_id_layout.addWidget(QLabel(f"{self.role} ID:"))
        user_id_layout.addWidget(QLabel(self.user_id))
        layout.addLayout(user_id_layout)

        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("新密码:"))
        self.password_edit = QLineEdit()
        password_layout.addWidget(self.password_edit)
        layout.addLayout(password_layout)

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
                    f"{role} 账号 {user_id} 已存在",
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
        self.handlers[check(self.menu.addAction("添加"))] = self.handle_add
        if self.item is not None:
            self.handlers[check(self.menu.addAction("编辑"))] = self.handle_edit
            self.handlers[check(self.menu.addAction("删除"))] = self.handle_delete


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
