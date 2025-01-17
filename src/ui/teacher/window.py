from PyQt6.QtWidgets import QHBoxLayout, QSpacerItem, QWidget

from ui.common.user_window import BaseUserWindow
from ui.dialog.password import PasswordDialog

from .pages import PAGES


class TeacherMainWindow(BaseUserWindow):
    title = "学生信息管理系统 - 教师端"
    page_cls = PAGES

    def add_stack_widget(self, widget: QWidget):
        w = QWidget()
        layout = QHBoxLayout()
        w.setLayout(layout)
        spacer = QSpacerItem(50, 20)
        layout.addSpacerItem(spacer)
        layout.addWidget(widget)
        layout.addSpacerItem(spacer)
        return super().add_stack_widget(w)

    def init_pages(self):
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        self.button_widget.setLayout(button_layout)

        for idx, page in enumerate(self.page_cls):
            p = page(self)
            self.add_stack_widget(p)
            btn = self._create_btn(p.button_name)
            btn.clicked.connect(self._page_btn_slot(idx))
            button_layout.addWidget(btn)

        btn = self._create_btn("修改密码")
        btn.clicked.connect(PasswordDialog.as_slot(self, "Teacher", self.user_id))
        button_layout.addWidget(btn)

        btn = self._create_btn("退出登录")
        btn.clicked.connect(self.handle_logout)
        button_layout.addWidget(btn)

        self.switch_page(0)
