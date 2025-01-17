from pathlib import Path

VERSION = "0.1.0"
AUTHORS = (
    ("wyf7685", "wyf7685@163.com"),
    ("lcj", "1613603747@qq.com"),
    ("wxy", "xxx@qq.com"),
)
COPYRIGHT = "© 2025 All Rights Reserved"

CONFIG_FILE = Path("settings.json")

BUTTON_STYLESHEET = """\
QPushButton {
    padding: 8px 16px;
    background-color: #2196F3;
    color: white;
    border-radius: 4px;
    border: none;
    font-size: 14px;
    font-weight: bold;
    min-width: 80px;
}
QPushButton:hover {
    background-color: #1976D2;
}
QPushButton:pressed {
    background-color: #0D47A1;
}
QPushButton:disabled {
    background-color: #E0E0E0;
    color: #9E9E9E;
}
"""
