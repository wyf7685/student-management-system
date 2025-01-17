from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from ui import WindowManager
from utils import get_resource_path

if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon(str(get_resource_path("app.ico"))))
    WindowManager().show_login()
    app.exec()
