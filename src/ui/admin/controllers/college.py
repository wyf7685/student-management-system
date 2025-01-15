from database import College, DBManager

from ._base import BaseController, DBRollbackMixin, check_college_id


class CollegeController(DBRollbackMixin, BaseController):
    def __init__(self) -> None:
        super().__init__()
        self.db = DBManager.college()

    def add(self, college_id: str, name: str) -> bool:
        """添加新学院"""
        try:
            # 验证数据
            if not name:
                return self.error("学院名称不能为空")
            cid = check_college_id(college_id)

            # 检查是否已存在
            if self.db.exists_college(cid):
                return self.error("学院代码已存在")

            # 创建并保存
            college = College(name=name, college_id=cid)
            self.db.add_college(college)

            # 发送信号
            self.added.emit(college)
            return self.success("学院添加成功")
        except Exception as err:
            return self.error(str(err))

    def update(self, college_id: str, name: str) -> bool:
        """更新学院信息"""
        try:
            cid = check_college_id(college_id)
            college = self.db.update_college(cid, name)
            self.updated.emit(college)
            return self.success("学院信息更新成功")
        except Exception as err:
            return self.error(str(err))

    def delete(self, college_id: str) -> bool:
        """删除学院"""
        try:
            cid = check_college_id(college_id)
            self.db.delete_college(cid)
            self.deleted.emit(college_id)
            return self.success("学院删除成功")
        except Exception as err:
            return self.error(str(err))

    def get(self, college_id: str) -> College | None:
        """获取单个学院信息"""
        try:
            cid = check_college_id(college_id)
            return self.db.get_college(cid)
        except Exception as e:
            self.error(str(e))
            return None

    def get_all(self) -> list[College]:
        """获取所有学院列表"""
        try:
            return self.db.get_all_colleges()
        except Exception as e:
            self.error(str(e))
            return []
