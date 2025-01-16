from typing import TYPE_CHECKING, ClassVar, cast

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

if TYPE_CHECKING:
    from .user_window import BaseUserWindow


class BasePage(QWidget):
    button_name: ClassVar[str]
    status_update = pyqtSignal(str)

    def __init__(self, parent: "BaseUserWindow") -> None:
        super().__init__(parent)
        self.status_update.connect(parent.status_update.emit)
        self.init_ui()

    def parent(self) -> "BaseUserWindow":
        return cast("BaseUserWindow", super().parent())

    @property
    def user_id(self) -> str:
        return self.parent().user_id

    def init_ui(self) -> None:
        raise NotImplementedError
