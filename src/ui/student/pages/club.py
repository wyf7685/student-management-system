from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import (
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from database import DBManager
from ui.common.page import BasePage, PageTitle


class ClubPage(BasePage):
    button_name = "社团信息"

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 设置全局字体大小
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        # 添加标题
        layout.addWidget(PageTitle("社团信息查询"))

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

        # 添加社团信息表格
        self.clubs_table = QTableWidget()
        self.clubs_table.setColumnCount(3)
        self.clubs_table.setHorizontalHeaderLabels(["社团名称", "描述", "报名状态"])
        self.clubs_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.clubs_table.customContextMenuRequested.connect(
            self.handle_list_context_menu
        )
        header = self.clubs_table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.clubs_table)

        # 添加报名信息框
        self.enrollment_frame = QFrame()
        self.enrollment_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.enrollment_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.enrollment_frame.setFixedHeight(200)  # 设置固定高度
        enrollment_layout = QVBoxLayout()
        self.enrollment_label = QLabel("请选择一个社团以查看报名信息")
        self.enrollment_label.setAlignment(Qt.AlignmentFlag.AlignTop)  # 文本对齐方式
        enrollment_layout.addWidget(self.enrollment_label)

        # 添加提示信息
        self.hint_label = QLabel("右键选择是否加入社团，再次右键退出社团")
        self.hint_label.setStyleSheet("color: gray; font-size: 10px;")
        enrollment_layout.addWidget(self.hint_label)

        self.enrollment_frame.setLayout(enrollment_layout)
        layout.addWidget(self.enrollment_frame)

        self.search_button.clicked.connect(self.update_clubs_table)
        self.clubs_table.cellClicked.connect(self.update_enrollment_info)
        self.update_clubs_table()

    def update_clubs_table(self) -> None:
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

        self.clubs_table.setRowCount(len(clubs))
        for row, club in enumerate(clubs):
            status = "报名中..." if club.club_id in joined else "未报名..."
            self.clubs_table.setItem(row, 0, QTableWidgetItem(club.name))
            self.clubs_table.setItem(row, 1, QTableWidgetItem(club.description))
            self.clubs_table.setItem(row, 2, QTableWidgetItem(status))

        self.joined = joined
        self.clubs = [c.club_id for c in clubs]

    def handle_list_context_menu(self, pos: QPoint):
        current_item = self.clubs_table.itemAt(pos)
        if not current_item:
            return

        row = current_item.row()
        cid = self.clubs[row]
        if cid not in self.joined:
            menu = self.create_join_ctx_menu(cid)
        else:
            menu = self.create_quit_ctx_menu(cid)
        menu.exec(self.clubs_table.mapToGlobal(pos))
        self.update_clubs_table()

    def create_join_ctx_menu(self, club_id: int):
        menu = QMenu(self)
        join_action = QAction("报名", self)
        join_action.triggered.connect(lambda: self.handle_join_action(club_id))
        menu.addAction(join_action)
        return menu

    def create_quit_ctx_menu(self, club_id: int):
        menu = QMenu(self)
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(lambda: self.handle_quit_action(club_id))
        menu.addAction(quit_action)
        return menu

    def handle_join_action(self, club_id: int):
        DBManager.student_club().add_student_club(
            int(self.get_user_id()), club_id, "member"
        )
        self.update_clubs_table()

    def handle_quit_action(self, club_id: int):
        DBManager.student_club().delete_student_club(int(self.get_user_id()), club_id)
        self.update_clubs_table()

    def update_enrollment_info(self, row: int, column: int):  
    # 确保 clubs 列表是最新的
     if not hasattr(self, "clubs") or not self.clubs:
        self.update_clubs_table()

     cid = self.clubs[row]
     status = "报名中..." if cid in self.joined else "未报名..."
     # 从原始的 clubs 数据中查找描述信息
     club_data = next((club for club in DBManager.club().get_all_clubs() if club.club_id == cid), None) 
     description = club_data.description if club_data else "无描述信息"

     self.enrollment_label.setText(
        f"社团ID: {cid}\n状态: {status}\n描述: {description}"
    )
