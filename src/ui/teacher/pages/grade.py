from PyQt6.QtWidgets import QVBoxLayout

from ui.common.page import BasePage


class GradePage(BasePage):
    button_name = "学生评分"

    def init_ui(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)
