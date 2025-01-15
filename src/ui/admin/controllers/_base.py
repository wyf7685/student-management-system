from PyQt6.QtCore import QObject, pyqtSignal

from ..common import get_admin_main


class BaseController(QObject):
    added = pyqtSignal(object)
    updated = pyqtSignal(object)
    deleted = pyqtSignal(int)
    operation_error = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.__error_connected = False

    def error(self, error: str):
        if not self.__error_connected:
            self.operation_error.connect(get_admin_main().status_update.emit)
            self.__error_connected = True

        if "FOREIGN KEY" in error:
            error = f"外键约束错误，请检查数据是否存在关联\n{error}"

        self.operation_error.emit(error)
        return False

    def success(self, status: str):
        get_admin_main().status_update.emit(status)
        return True


class DBRollbackMixin:
    def error(self, error: str):
        self.db.rollback()  # type:ignore[]
        return super().error(error)  # type:ignore[]


def make_checker(name: str):
    def checker(id: str):
        if not id:
            raise ValueError(f"{name}不能为空")

        if not id.isdigit():
            raise ValueError(f"{name}必须为数字")

        return int(id)

    return checker


check_college_id = make_checker("学院代码")
check_major_id = make_checker("专业代码")
check_class_id = make_checker("班级代码")
check_student_id = make_checker("学生学号")
check_course_id = make_checker("课程代码")
