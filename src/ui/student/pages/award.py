from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout

from database.manager import DBManager
from ui.common.page import BasePage, PageTitle

AWARD_LIST_STYLESHEET = """
QListWidget {
    background-color: transparent;
    border: 1px solid palette(mid);
    border-radius: 5px;
    padding: 5px;
}
QListWidget::item {
    background-color: palette(base);
    border: 1px solid palette(midlight);
    border-radius: 5px;
    margin: 5px;
    padding: 10px;
}
QListWidget::item:hover {
    background-color: palette(highlight);
}
QListWidget::item:selected {
    background-color: palette(highlight);
    font-weight: bold;
    color: palette(text);  /* 使用系统默认字体颜色 */
}
"""


class AwardPage(BasePage):
    button_name = "获奖查询"

    def init_ui(self):
        layout = QVBoxLayout()

        # 添加标题
        layout.addWidget(PageTitle("获奖查询"))

        # 添加获奖信息列表
        self.awards_list = QListWidget()
        self.awards_list.setStyleSheet(AWARD_LIST_STYLESHEET)
        layout.addWidget(self.awards_list)

        self.setLayout(layout)
        self.update_awards()

    def create_list_item(self, text: str) -> QListWidgetItem:
        item = QListWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont(self.awards_list.font())
        font.setPointSize(int(font.pointSize() * 1.5))
        item.setFont(font)
        return item

    def update_awards(self):
        award_manager = DBManager.award()
        awards = award_manager.get_awards_by_student(int(self.get_user_id()))

        self.awards_list.clear()
        if awards:
            for award in awards:
                text = f"奖项名称: {award.award_name}, 获奖日期: {award.award_date}"
                self.awards_list.addItem(self.create_list_item(text))
        else:
            self.awards_list.addItem(self.create_list_item("没有找到相关奖项"))
