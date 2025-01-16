from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QVBoxLayout,
)

from database import DBManager
from ui.common.page import BasePage


class ClubPage(BasePage):
    button_name = "社团信息"

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 添加标题
        title_label = QLabel("社团信息查询")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # 添加输入框和查询按钮
        input_group_box = QGroupBox()
        input_group_layout = QHBoxLayout()
        input_group_box.setLayout(input_group_layout)
        input_group_layout.addWidget(QLabel("请输入搜索关键词:"))
        self.keyword_edit = QLineEdit()
        input_group_layout.addWidget(self.keyword_edit)
        self.search_button = QPushButton("查询")
        input_group_layout.addWidget(self.search_button)
        layout.addWidget(input_group_box)

        # 添加社团信息列表
        self.clubs_list = QListWidget()
        self.clubs_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.clubs_list.customContextMenuRequested.connect(
            self.handle_list_context_menu
        )
        layout.addWidget(self.clubs_list)

        self.search_button.clicked.connect(self.update_clubs_list)
        self.update_clubs_list()

    def update_clubs_list(self) -> None:
        keyword = self.keyword_edit.text().strip()

        db = DBManager.club()
        clubs = db.search_club(keyword) if keyword else db.get_all_clubs()

        joined = [
            club.club_id
            for club in DBManager.student_club().get_clubs_by_student(
                int(self.get_user_id())
            )
        ]
        clubs.sort(key=lambda c: (c.club_id not in joined, c.club_id))

        self.clubs_list.clear()
        for club in clubs:
            sign = "◆" if club.club_id in joined else "◇"
            item = QListWidgetItem(f"{sign} {club.name}  -  {club.description}")
            item.setFont(QFont("Arial", 12))
            self.clubs_list.addItem(item)

        self.joined = joined
        self.clubs = [c.club_id for c in clubs]

    def handle_list_context_menu(self, pos: QPoint):
        if not self.clubs_list.currentItem():
            return

        cid = self.clubs[self.clubs_list.currentRow()]
        if cid not in self.joined:
            menu = self.create_join_ctx_menu(cid)
        else:
            menu = self.create_quit_ctx_menu(cid)
        menu.exec(self.clubs_list.mapToGlobal(pos))
        self.update_clubs_list()

    def create_join_ctx_menu(self, club_id: int):
        menu = QMenu(self)
        join_action = QAction("加入", self)
        join_action.triggered.connect(
            lambda: DBManager.student_club().add_student_club(
                int(self.get_user_id()), club_id, "member"
            )
        )
        menu.addAction(join_action)
        return menu

    def create_quit_ctx_menu(self, club_id: int):
        menu = QMenu(self)
        join_action = QAction("退出", self)
        join_action.triggered.connect(
            lambda: DBManager.student_club().delete_student_club(
                int(self.get_user_id()), club_id
            )
        )
        menu.addAction(join_action)
        return menu
