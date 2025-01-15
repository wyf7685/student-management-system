from PyQt6.QtWidgets import QApplication

from ui import WindowManager

if __name__ == "__main__":
    app = QApplication([])
    WindowManager().show_login()
    app.exec()
