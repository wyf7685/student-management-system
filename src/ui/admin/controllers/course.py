from database.manager import DBManager
from database.models import Course

from ._base import BaseController, check_course_id


def check_credits(course_id: str) -> int:
    if not course_id.isdigit():
        raise ValueError("学分必须为数字")
    credits = int(course_id)
    if credits <= 0:
        raise ValueError("学分必须大于 0")
    return credits


class CourseController(BaseController):
    def __init__(self):
        super().__init__()
        self.manager = DBManager.course()

    def get_all(self):
        return self.manager.get_all_courses()

    def add(self, course_id: str, name: str, credits: str):
        try:
            cid = check_course_id(course_id)
            c = check_credits(credits)
            course = Course(course_id=cid, name=name, credits=c)
            self.manager.add_course(course)
            self.added.emit(course)
            return self.success("课程添加成功")
        except Exception as e:
            return self.error(str(e))

    def update(self, course_id: str, name: str, credits: str):
        course = None
        try:
            cid = check_course_id(course_id)
            if name:
                course = self.manager.update_course(cid, name=name)
            if credits:
                c = check_credits(credits)
                course = self.manager.update_course(cid, name=name, credits=c)
            if course is None:
                return self.error("课程信息未更新")

            self.updated.emit(course)
            return self.success("课程信息更新成功")
        except Exception as e:
            return self.error(str(e))

    def delete(self, course_id: str):
        try:
            cid = check_course_id(course_id)
            self.manager.delete_course(cid)
            self.deleted.emit(cid)
            return self.success("课程删除成功")
        except Exception as e:
            return self.error(str(e))
