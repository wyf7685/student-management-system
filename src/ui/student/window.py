from PyQt6.QtWidgets import QHBoxLayout, QSpacerItem, QVBoxLayout, QWidget

from ui.common.user_window import BaseUserWindow

from .pages import PAGES


class StudentMainWindow(BaseUserWindow):
    title = "学生信息管理系统 - 学生端"
    page_cls = PAGES

    def add_stack_widget(self, widget: QWidget):
        w = QWidget()
        layout = QHBoxLayout()
        w.setLayout(layout)
        spacer = QSpacerItem(70, 20)
        layout.addSpacerItem(spacer)
        layout.addWidget(widget)
        layout.addSpacerItem(spacer)
        return super().add_stack_widget(w)

    def init_pages(self):
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row1.setSpacing(15)
        row2.setSpacing(15)
        button_layout.addLayout(row1)
        button_layout.addLayout(row2)
        self.button_widget.setLayout(button_layout)

        for idx, page in enumerate(self.page_cls):
            p = page(self)
            self.add_stack_widget(p)
            btn = self._create_btn(p.button_name)
            btn.clicked.connect(self._page_btn_slot(idx))
            (row1 if idx < 4 else row2).addWidget(btn)

        btn = self._create_btn("退出登录")
        btn.clicked.connect(self.handle_logout)
        row2.addWidget(btn)

        self.switch_page(0)
