from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from const import CONFIG_FILE


class SqliteConfig(BaseModel):
    type: Literal["SQLite"] = "SQLite"
    path: Path = Path("db.sqlite")


class ServerConfig(BaseModel):
    type: Literal["SQL Server", "MySQL", "PostgreSQL"]
    host: str
    port: int | None
    username: str
    password: str
    database: str


class LastLogin(BaseModel):
    role: Literal["Admin", "Teacher", "Student"]
    username: str


class Config(BaseModel):
    db: SqliteConfig | ServerConfig = SqliteConfig()
    last_login: LastLogin | None = None

    def save(self):
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(self.model_dump_json(), "utf-8")


def load_config() -> Config:
    return (
        Config.model_validate_json(CONFIG_FILE.read_text("utf-8"))
        if CONFIG_FILE.exists()
        else Config()
    )


config = load_config()
