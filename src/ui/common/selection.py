from collections.abc import Callable

from PyQt6.QtWidgets import QComboBox, QWidget


class SelectionCombo[T](QComboBox):
    def __init__(
        self,
        parent: QWidget,
        inner_data: list[T],
        formatter: Callable[[T], str] = str,
        default_pred: Callable[[T], bool] | None = None,
    ) -> None:
        super().__init__(parent)

        self.inner_data = inner_data
        self.formatter = formatter

        for data in inner_data:
            self.addItem(formatter(data))
            if default_pred is not None and default_pred(data):
                self.setCurrentIndex(self.count() - 1)

    def get_selected(self) -> T:
        return self.inner_data[self.currentIndex()]

    def update_data(self, inner_data: list[T]) -> None:
        self.clear()

        self.inner_data = inner_data
        for data in inner_data:
            self.addItem(self.formatter(data))

        self.setCurrentIndex(0)
