from PyQt6.QtWidgets import QApplication

from ui import WindowManager

# from ui import LoginWindow as MainWindow
# from ui.admin.window import AdminMainWindow as MainWindow
# from ui.student.window import StudentMainWindow as MainWindow

if __name__ == "__main__":
    app = QApplication([])
    WindowManager().show_login()
    app.exec()
