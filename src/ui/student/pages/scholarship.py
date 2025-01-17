from functools import partial

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from database.manager import DBManager
from ui.common.page import BasePage


class ScholarshipPage(BasePage):
    button_name = "奖学金申请"

    def init_ui(self):
        # 创建一个垂直布局
        layout = QVBoxLayout()

        # 添加标题标签
        title_label = QLabel("奖学金申请")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # 创建一个 QTableWidget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)  # 减少一列用于描述
        self.table_widget.setHorizontalHeaderLabels(
            ["奖学金ID", "奖学金名称", "金额", "日期", "操作"]
        )

        # 设置表格的大小策略，使其填充可用空间
        self.table_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # 动态调整表格列宽，使每个列均匀分布
        header = self.table_widget.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # 获取奖学金信息
        scholarships = DBManager.scholarship().get_all_scholarships()

        # 设置表格的行数
        self.table_widget.setRowCount(len(scholarships))

        # 填充表格数据
        for row, scholarship in enumerate(scholarships):
            self.table_widget.setItem(
                row, 0, QTableWidgetItem(str(scholarship.scholarship_id))
            )
            self.table_widget.setItem(
                row, 1, QTableWidgetItem(scholarship.scholarship_name)
            )
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(scholarship.amount)))
            self.table_widget.setItem(
                row, 3, QTableWidgetItem(scholarship.date_awarded)
            )

            # 添加申请按钮，并使用 partial 捕获当前行号
            apply_button = QPushButton("申请")
            apply_button.clicked.connect(partial(self.apply_scholarship, row))
            self.table_widget.setCellWidget(row, 4, apply_button)  # 更新列索引

        # 将表格添加到布局中
        layout.addWidget(self.table_widget)

        # 设置布局的边距为0
        layout.setContentsMargins(0, 0, 0, 0)

        # 设置布局
        self.setLayout(layout)

    def apply_scholarship(self, row):
        # 获取当前行的奖学金ID
        item = self.table_widget.item(row, 0)
        if item is None:
            QMessageBox.critical(self, "错误", "无法获取奖学金ID，请刷新页面并重试。")
            return
        if not item.text().isdigit():
            QMessageBox.critical(self, "错误", "奖学金ID无效，请联系管理员。")
            return

        # 获取奖学金名称
        scholarship_name_item = self.table_widget.item(row, 1)
        if scholarship_name_item is None:
            QMessageBox.critical(self, "错误", "无法获取奖学金名称，请刷新页面并重试。")
            return

        scholarship_name = scholarship_name_item.text()

        # 更新按钮文本为“奖学金名称 申请中”
        apply_button = self.table_widget.cellWidget(row, 4)  # 更新列索引
        if isinstance(apply_button, QPushButton):  # 确保按钮是 QPushButton 类型
            apply_button.setText(f"{scholarship_name} 申请中...")  # 使用 setText 方法
            apply_button.setEnabled(False)  # 禁用按钮，防止重复点击
        else:
            QMessageBox.critical(self, "错误", "无法找到申请按钮，请刷新页面并重试。")
            return

        # 使用 QTimer 单次触发延迟显示消息框，确保按钮文本更新完成
        QTimer.singleShot(
            0,
            lambda: QMessageBox.information(
                self, "申请奖学金", f"{scholarship_name} 申请中..."
            ),
        )

        # 模拟申请成功后的处理
        # 例如：更新数据库、刷新表格等
        # ...
