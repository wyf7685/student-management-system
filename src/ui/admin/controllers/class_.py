from database import Class
from database.manager import ClassDBManager

from ._base import (
    BaseController,
    check_class_id,
    check_major_id,
    make_checker,
)

check_year = make_checker("年级")


class ClassController(BaseController[ClassDBManager]):
    dbm_factory = ClassDBManager

    def add(
        self,
        class_id: str,
        name: str,
        major_id: str,
        year: str,
    ) -> bool:
        try:
            # 验证数据
            if not name:
                return self.error("班级名称不能为空")
            cid = check_class_id(class_id)
            mid = check_major_id(major_id)
            y = check_year(year)

            # 检查是否已存在
            if self.db.exists_class(cid):
                return self.error("班级代码已存在")

            # 创建并保存
            class_ = Class(
                name=name,
                class_id=cid,
                major_id=mid,
                year=y,
            )
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
        major_id: str,
        year: str,
    ) -> bool:
        class_ = None
        try:
            cid = check_class_id(class_id)
            if name:
                class_ = self.db.update_class(cid, name=name)
            if major_id:
                mid = check_major_id(major_id)
                class_ = self.db.update_class(cid, major_id=mid)
            if year:
                y = check_year(year)
                class_ = self.db.update_class(cid, year=y)
            if class_ is None:
                return self.error("班级信息未更新")

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

    def get_all(self) -> list[Class]:
        """获取所有班级信息"""
        return self.db.get_all_classes()
