from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from const import AUTHORS, COPYRIGHT, VERSION


class AboutWindow(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setWindowTitle("关于")
        self.setFixedSize(400, 300)

        # 创建主布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 添加标题
        title = QLabel("学生信息管理系统")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        # 添加版本信息
        version = QLabel(f"版本: {VERSION}")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)

        # 添加分割线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # 添加作者信息标题
        authors_title = QLabel("作者信息")
        authors_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        authors_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(authors_title)

        # 添加作者信息容器
        authors_container = QWidget()
        authors_layout = QHBoxLayout(authors_container)
        authors_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(authors_container)

        for idx, (name, email) in enumerate(AUTHORS):
            author_label = QLabel(f"{name}\n{email}")
            author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            authors_layout.addWidget(author_label)
            # 在作者之间添加分隔符，最后一个作者除外
            if idx < len(AUTHORS) - 1:
                separator = QLabel("|")
                separator.setStyleSheet("color: #999;")
                authors_layout.addWidget(separator)

        # 添加分割线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # 添加版权信息
        copyright = QLabel(COPYRIGHT)  # noqa: A001
        copyright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright)

        # 添加关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        # 设置窗口样式
        self.setStyleSheet("""
            QLabel {
                padding: 5px;
            }
            QPushButton {
                padding: 5px 15px;
                margin: 10px;
            }
        """)
