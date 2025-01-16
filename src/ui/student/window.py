from PyQt6.QtWidgets import QHBoxLayout, QSpacerItem, QWidget

from ui.common.user_window import BaseUserWindow

from .pages import PAGES


class StudentMainWindow(BaseUserWindow):
    title = "学生信息管理系统 - 学生端"
    page_cls = PAGES

    def add_stack_widget(self, widget: QWidget):
        w = QWidget()
        layout = QHBoxLayout()
        w.setLayout(layout)
        spacer = QSpacerItem(90, 20)
        layout.addSpacerItem(spacer)
        layout.addWidget(widget)
        layout.addSpacerItem(spacer)
        return super().add_stack_widget(w)
