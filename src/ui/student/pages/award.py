from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from database.manager import DBManager
from ui.common.page import BasePage, PageTitle


class AwardPage(BasePage):
    button_name = "获奖查询"

    def init_ui(self):
        layout = QVBoxLayout()

        # 添加标题
        layout.addWidget(PageTitle("获奖查询"))

        # 添加输入框和查询按钮
        input_group_box = QGroupBox()
        input_group_layout = QHBoxLayout()
        input_group_box.setLayout(input_group_layout)

        self.student_id_label = QLabel("请输入学号:")
        self.student_id_input = QLineEdit()
        self.search_button = QPushButton("查询")

        input_group_layout.addWidget(self.student_id_label)
        input_group_layout.addWidget(self.student_id_input)
        input_group_layout.addWidget(self.search_button)

        layout.addWidget(input_group_box)

        # 添加获奖信息列表
        self.awards_list = QListWidget()
        layout.addWidget(self.awards_list)

        # 连接查询按钮的点击事件
        self.search_button.clicked.connect(self.search_awards)

        self.setLayout(layout)

    def search_awards(self):
        student_id = self.student_id_input.text()
        if not student_id:
            self.awards_list.clear()
            self.awards_list.addItem("请输入学号")
            return

        try:
            student_id = int(student_id)
        except ValueError:
            self.awards_list.clear()
            self.awards_list.addItem("学号必须是数字")
            return

        award_manager = DBManager.award()
        awards = award_manager.get_awards_by_student(student_id)

        self.awards_list.clear()
        if awards:
            for award in awards:
                item_text = (
                    f"奖项名称: {award.award_name}, 获奖日期: {award.award_date}"
                )
                item = QListWidgetItem(item_text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.awards_list.addItem(item)
        else:
            self.awards_list.addItem("没有找到相关奖项")
