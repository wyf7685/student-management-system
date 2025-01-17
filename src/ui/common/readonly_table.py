from collections.abc import Sequence

from PyQt6.QtWidgets import QTableWidget


class ReadonlyTableWidget(QTableWidget):
    def __init__(self, labels: Sequence[str]) -> None:
        super().__init__()
        self.setColumnCount(len(labels))
        self.setHorizontalHeaderLabels(labels)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
