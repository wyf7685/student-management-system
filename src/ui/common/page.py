from typing import TYPE_CHECKING, ClassVar

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QWidget

if TYPE_CHECKING:
    from .user_window import BaseUserWindow


class BasePage(QWidget):
    button_name: ClassVar[str]
    status_update = pyqtSignal(str)

    def __init__(self, parent: "BaseUserWindow") -> None:
        super().__init__(parent)
        self._parent = parent
        self.status_update.connect(parent.status_update.emit)
        self.init_ui()

    def get_user_id(self) -> str:
        return self._parent.user_id

    def update_status(self, status: str) -> None:
        self.status_update.emit(status)

    def on_error(self, message: str) -> None:
        self.update_status(f"错误: {message}")
        QMessageBox.warning(self, "错误", message)

    def init_ui(self) -> None:
        raise NotImplementedError
