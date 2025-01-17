from database import SystemAccount
from database.manager import SystemAccountDBManager

from ._base import (
    BaseController,
    check_student_id,
    make_checker,
)

check_teacher_id = make_checker("教师 ID")


def _check_user_id(role: str, user_id: str):
    match role:
        case "Student":
            return str(check_student_id(user_id))
        case "Teacher":
            return str(check_teacher_id(user_id))
        case "Admin":
            return user_id
        case _:
            raise ValueError("Invalid role")


class SystemAccountController(BaseController[SystemAccountDBManager]):
    dbm_factory = SystemAccountDBManager

    def add(self, role: str, user_id: str, password: str):
        try:
            u = _check_user_id(role, user_id)
            account = self.db.find_account(role, u)
            if account:
                return self.error("账号已存在")
            new_account = self.db.add_account(role, u, password)
            self.added.emit(new_account)
            return self.success("账号创建成功")
        except Exception as err:
            return self.error(str(err))

    def update_password(self, role: str, user_id: str, password: str):
        try:
            account = self.db.find_account(role, _check_user_id(role, user_id))
            if not account:
                return self.error("未找到账号信息")
            account = self.db.update_account(account.id, password=password)
            self.updated.emit(account)
            return self.success("密码更新成功")
        except Exception as err:
            return self.error(str(err))

    def delete(self, role: str, user_id: str):
        try:
            account = self.db.find_account(role, _check_user_id(role, user_id))
            if not account:
                return self.error("未找到账号信息")
            self.db.delete_account(account.id)
            self.deleted.emit(account)
            return self.success("账号删除成功")
        except Exception as err:
            return self.error(str(err))

    def get_all(self) -> list[SystemAccount]:
        return self.db.get_all_accounts()
