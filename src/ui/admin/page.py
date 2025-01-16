from collections.abc import Generator
from typing import ClassVar, cast

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ui.common.page import BasePage as _BasePage

from .common import BaseContextMenuHandler
from .controllers._base import BaseController


class BasePage[C: BaseController](_BasePage):
    handler_cls: ClassVar[type[BaseContextMenuHandler]]
    columns: ClassVar[tuple[str, ...]]
    controller_cls: ClassVar[type[BaseController]]

    def init_ui(self) -> None:
        self.controller = cast(C, self.controller_cls(self))

        self.controller.added.connect(self.update_table)
        self.controller.deleted.connect(self.update_table)
        self.controller.updated.connect(self.update_table)
        self.controller.operation_error.connect(self.on_error)

        widget = QWidget()
        layout = QVBoxLayout(widget)
        title_layout = QHBoxLayout()
        title_label = QLabel(f"{self.button_name}列表")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; margin-bottom: 10px;"
        )
        refresh_btn = QPushButton()
        refresh_btn.setText("刷新")
        refresh_btn.setFixedSize(72, 24)
        refresh_btn.setToolTip("刷新列表")
        refresh_btn.clicked.connect(self.update_table)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(refresh_btn)
        layout.addLayout(title_layout)
        self.setup_table()
        layout.addWidget(self.table)

        self._layout = QVBoxLayout()
        self._layout.addWidget(widget)
        self.setLayout(self._layout)

    def setup_table(self):
        table = QTableWidget()
        table.setColumnCount(len(self.columns))
        table.setHorizontalHeaderLabels(self.columns)
        table.setMinimumWidth(400)
        table.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        table.customContextMenuRequested.connect(self.handler_cls.as_slot(self))
        self.table = table
        self.update_table()

    def update_table(self) -> None:
        self.table.setRowCount(0)
        for data in self.iterate_table_data():
            row = self.table.rowCount()
            self.table.insertRow(row)

            for col, value in enumerate(data):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def iterate_table_data(self) -> Generator[tuple[object, ...]]:
        yield NotImplemented
