from pathlib import Path

VERSION = "0.1.0"
AUTHORS = (
    ("wyf7685", "wyf7685@163.com"),
    ("lcj", "xxx@qq.com"),
    ("wxy", "xxx@qq.com"),
)
COPYRIGHT = "© 2025 All Rights Reserved"

CONFIG_DIR = Path("config")
CONFIG_FILE = CONFIG_DIR / "config.json"

BUTTON_STYLESHEET = """\
QPushButton {
  padding: 8px;
  background-color: #59a5fb;
  color: white;
  border-radius: 4px;
}
QPushButton:hover {
  background-color: #337ec9;
}
QPushButton:disabled {
    background-color: #cccccc;
    color: #666666;
    opacity: 0.6;
}
"""
