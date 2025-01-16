from collections.abc import Callable
from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

from database.manager import DBManager

if TYPE_CHECKING:
    from ..page import BasePage


class BaseController[D: DBManager](QObject):
    added = pyqtSignal(object)
    updated = pyqtSignal(object)
    deleted = pyqtSignal(int)
    operation_error = pyqtSignal(str)
    status_update = pyqtSignal(str)

    dbm_factory: Callable[[], D]
    db: D

    def __init__(self, parent: "BasePage") -> None:
        super().__init__(parent)
        self.db = self.dbm_factory()
        self.operation_error.connect(parent.status_update.emit)
        self.status_update.connect(parent.status_update.emit)

    def error(self, error: str):
        self.db.rollback()

        if "FOREIGN KEY" in error:
            error = f"外键约束错误，请检查数据是否存在关联\n{error}"

        self.operation_error.emit(error)
        return False

    def success(self, status: str):
        self.status_update.emit(status)
        return True

    def init_db(self) -> None:
        pass


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
