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

from database.manager import DBManager
from ui.common.selection import SelectionCombo
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


class CollegeSelectionCombo(SelectionCombo):
    def __init__(self, parent: QWidget, default: int | None = None) -> None:
        super().__init__(
            parent,
            [(c.college_id, c.name) for c in DBManager.college().get_all_colleges()],
            lambda x: f"{x[0]} - {x[1]}",
            (lambda x: x[0] == default) if default is not None else None,
        )


class MajorSelectionCombo(SelectionCombo):
    def __init__(self, parent: QWidget, default: int | None = None) -> None:
        super().__init__(
            parent,
            [(m.major_id, m.name) for m in DBManager.major().get_all_majors()],
            lambda x: f"{x[0]} - {x[1]}",
            (lambda x: x[0] == default) if default is not None else None,
        )


class ClassSelectionCombo(SelectionCombo):
    def __init__(self, parent: QWidget, default: int | None = None) -> None:
        super().__init__(
            parent,
            [(c.class_id, c.name) for c in DBManager.class_().get_all_classes()],
            lambda x: f"{x[0]} - {x[1]}",
            (lambda x: x[0] == default) if default is not None else None,
        )
