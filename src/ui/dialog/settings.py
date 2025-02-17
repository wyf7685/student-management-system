from pathlib import Path

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from config import ServerConfig, SqliteConfig, config
from database.db_config import reload_engine


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setFixedSize(400, 300)
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout()

        # 数据库设置组
        db_group = QGroupBox("数据库设置")
        db_layout = QVBoxLayout()

        # 数据库类型选择
        db_type_layout = QHBoxLayout()
        db_type_layout.addWidget(QLabel("数据库类型:"))
        self.db_type_combo = QComboBox()
        self.db_type_combo.addItems(["SQLite", "SQL Server", "MySQL", "PostgreSQL"])
        self.db_type_combo.setCurrentText(config.db.type)
        self.db_type_combo.currentTextChanged.connect(self.on_db_type_changed)
        db_type_layout.addWidget(self.db_type_combo)
        db_layout.addLayout(db_type_layout)

        # SQLite配置
        self.sqlite_config = QWidget()
        self.sqlite_layout = QHBoxLayout()
        self.sqlite_layout.addWidget(QLabel("数据库文件:"))
        self.sqlite_path = QLineEdit()
        self.sqlite_browse = QPushButton("浏览...")
        self.sqlite_browse.clicked.connect(self.browse_sqlite_file)
        self.sqlite_layout.addWidget(self.sqlite_path)
        self.sqlite_layout.addWidget(self.sqlite_browse)
        self.sqlite_config.setLayout(self.sqlite_layout)
        db_layout.addWidget(self.sqlite_config)

        # MySQL/PostgreSQL配置
        self.server_config = QWidget()
        server_layout = QFormLayout()
        self.host_edit = QLineEdit()
        self.port_edit = QLineEdit()
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.database_edit = QLineEdit()
        server_layout.addRow("主机:", self.host_edit)
        server_layout.addRow("端口:", self.port_edit)
        server_layout.addRow("用户名:", self.username_edit)
        server_layout.addRow("密码:", self.password_edit)
        server_layout.addRow("数据库:", self.database_edit)
        self.server_config.setLayout(server_layout)
        db_layout.addWidget(self.server_config)

        db_group.setLayout(db_layout)

        # 按钮
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("保存")
        cancel_btn = QPushButton("取消")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addWidget(db_group)
        layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # default setting
        self.on_db_type_changed("SQLite")

    def switch_sqlite_visible(self, *, visible: bool):
        self.sqlite_config.setVisible(visible)
        self.server_config.setVisible(not visible)

        is_sql_server = self.db_type_combo.currentText() == "SQL Server"
        self.host_edit.setDisabled(is_sql_server)
        self.port_edit.setDisabled(is_sql_server)
        self.username_edit.setDisabled(is_sql_server)
        self.password_edit.setDisabled(is_sql_server)

    def on_db_type_changed(self, db_type):
        """处理数据库类型变更"""
        if db_type == "SQLite":
            self.sqlite_path.setText("db.sqlite")
        else:
            self.host_edit.setText("localhost")
            default_port = {
                "SQL Server": "",
                "MySQL": "3306",
                "PostgreSQL": "5432",
            }[db_type]
            self.port_edit.setText(default_port)

        self.load_settings()
        self.switch_sqlite_visible(visible=db_type == "SQLite")

    def browse_sqlite_file(self):
        """选择SQLite数据库文件"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "选择数据库文件",
            "",
            "SQLite数据库文件 (*.db *.sqlite);;所有文件 (*.*)",
        )
        if filename:
            self.sqlite_path.setText(filename)

    def load_settings(self):
        if config.db.type == "SQLite":
            self.sqlite_path.setText(str(config.db.path))
            self.switch_sqlite_visible(visible=True)
        elif self.db_type_combo.currentText() == config.db.type:
            self.host_edit.setText(config.db.host)
            self.port_edit.setText(str(config.db.port or ""))
            self.username_edit.setText(config.db.username)
            self.password_edit.setText(config.db.password)
            self.database_edit.setText(config.db.database)
            self.switch_sqlite_visible(visible=False)

    def save_settings(self):
        original = config.db

        if self.db_type_combo.currentText() == "SQLite":
            config.db = SqliteConfig(path=Path(self.sqlite_path.text()))
        else:
            config.db = ServerConfig(
                type=self.db_type_combo.currentText(),  # type:ignore[]
                host=self.host_edit.text(),
                port=int(port) if (port := self.port_edit.text()) else None,
                username=self.username_edit.text(),
                password=self.password_edit.text(),
                database=self.database_edit.text(),
            )

        try:
            reload_engine()
        except Exception as err:
            config.db = original
            reload_engine()
            QMessageBox.critical(self, "错误", f"保存配置失败: {err}")
        else:
            config.save()
            self.accept()
