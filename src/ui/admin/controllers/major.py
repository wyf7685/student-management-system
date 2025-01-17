from database import Major
from database.manager import MajorDBManager

from ._base import BaseController, check_major_id


class MajorController(BaseController[MajorDBManager]):
    dbm_factory = MajorDBManager

    def add(self, major_id: str, name: str, college_id: int) -> bool:
        try:
            # 验证数据
            if not name:
                return self.error("专业名称不能为空")
            mid = check_major_id(major_id)

            # 检查是否已存在
            if self.db.exists_major(mid):
                return self.error("专业代码已存在")

            # 创建并保存
            major = Major(name=name, major_id=mid, college_id=college_id)
            self.db.add_major(major)

            # 发送信号
            self.added.emit(major)
            return self.success("专业添加成功")
        except Exception as err:
            return self.error(str(err))

    def update(self, major_id: str, name: str, college_id: int) -> bool:
        major = None
        try:
            mid = check_major_id(major_id)
            if name:
                major = self.db.update_major(mid, name=name)
            if college_id:
                major = self.db.update_major(mid, college_id=college_id)
            if major is None:
                return self.error("专业信息未更新")

            self.updated.emit(major)
            return self.success("专业信息更新成功")
        except Exception as err:
            return self.error(str(err))

    def delete(self, major_id: str) -> bool:
        try:
            mid = check_major_id(major_id)
            self.db.delete_major(mid)
            self.deleted.emit(major_id)
            return self.success("专业删除成功")
        except Exception as err:
            return self.error(str(err))

    def get(self, major_id: str) -> Major | None:
        """获取单个专业信息"""
        try:
            mid = check_major_id(major_id)
            return self.db.get_major(mid)
        except Exception as err:
            self.error(str(err))
            return None

    def get_all(self) -> list[Major]:
        """获取所有专业信息"""
        return self.db.get_all_majors()
