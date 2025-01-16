from typing import TYPE_CHECKING, Protocol, cast

from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QMenu,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from utils import check as check

if TYPE_CHECKING:
    from collections.abc import Callable

    from PyQt6.QtGui import QAction


class _ContextMenuHandlerParentTab[C](Protocol):
    table: QTableWidget
    controller: C


class BaseContextMenuHandler[C]:
    def __init__(
        self,
        parent: QWidget,
        item: QTableWidgetItem | None,
        table: QTableWidget,
        controller: C,
    ) -> None:
        self.parent = parent
        self.menu = QMenu(parent)
        self.item = item
        self.table = table
        self.controller = controller
        self.handlers: dict[QAction | None, Callable[[], object]] = {}
        self.setup_menu()

    def get_item_value(self, column: int):
        return check(self.table.item(check(self.item).row(), column)).text()

    def setup_menu(self) -> None:
        pass

    def exec(self, pos: QPoint) -> None:
        if handler := self.handlers.get(self.menu.exec(pos)):
            handler()

    @classmethod
    def as_slot(cls, tab: _ContextMenuHandlerParentTab[C]):
        def slot(pos: QPoint) -> None:
            cls(
                cast(QWidget, tab),
                tab.table.itemAt(pos),
                tab.table,
                tab.controller,
            ).exec(check(tab.table.viewport()).mapToGlobal(pos))

        return slot


class BaseConfirmDialog(QDialog):
    def __init__(self, parent: QWidget, title: str) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.content_layout = QVBoxLayout()
        layout.addLayout(self.content_layout)
        btn_layout = QHBoxLayout()
        self.yes_btn = QPushButton("确定")
        self.no_btn = QPushButton("取消")
        btn_layout.addStretch()
        btn_layout.addWidget(self.yes_btn)
        btn_layout.addWidget(self.no_btn)
        layout.addLayout(btn_layout)
        self.yes_btn.clicked.connect(self.accept)
        self.no_btn.clicked.connect(self.reject)

    def exec(self) -> int:
        self.setup_content(self.content_layout)
        return super().exec()

    def setup_content(self, layout: QVBoxLayout):
        pass
