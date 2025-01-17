from database import Class
from database.manager import ClassDBManager
from utils import check

from ._base import (
    BaseController,
    check_class_id,
    make_checker,
)

check_year = make_checker("年级")


class ClassController(BaseController[ClassDBManager]):
    dbm_factory = ClassDBManager

    def add(
        self,
        class_id: str,
        name: str,
        major_id: int,
        year: str,
    ) -> bool:
        try:
            # 验证数据
            if not name:
                return self.error("班级名称不能为空")
            cid = check_class_id(class_id)
            y = check_year(year)

            # 检查是否已存在
            if self.db.exists_class(cid):
                return self.error("班级代码已存在")

            # 创建并保存
            class_ = Class(name=name, class_id=cid, major_id=major_id, year=y)
            self.db.add_class(class_)

            # 发送信号
            self.added.emit(class_)
            return self.success("班级添加成功")
        except Exception as err:
            return self.error(str(err))

    def update(
        self,
        class_id: str,
        name: str,
        major_id: int,
        year: str,
    ) -> bool:
        class_ = None
        try:
            cid = check_class_id(class_id)
            kwds = {}
            if name:
                kwds["name"] = name
            if major_id:
                kwds["major_id"] = major_id
            if year:
                kwds["year"] = check_year(year)
            if not kwds:
                return self.error("班级信息未更新")

            class_ = self.db.update_class(cid, **kwds)
            self.updated.emit(class_)
            return self.success("班级信息更新成功")
        except Exception as err:
            return self.error(str(err))

    def delete(self, class_id: str) -> bool:
        try:
            cid = check_class_id(class_id)
            self.db.delete_class(cid)
            self.deleted.emit(class_id)
            return self.success("班级删除成功")
        except Exception as err:
            return self.error(str(err))

    def get(self, class_id: str) -> Class | None:
        """获取单个班级信息"""
        try:
            cid = check_class_id(class_id)
            return self.db.get_class(cid)
        except Exception as err:
            self.error(str(err))
            return None

    def get_all(self):
        """获取所有班级信息"""
        mdb = self.db.major()
        for c in self.db.get_all_classes():
            m = check(mdb.get_major(c.major_id))
            yield (c.class_id, c.name, c.major_id, m.name, c.year)
