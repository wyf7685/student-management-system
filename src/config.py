from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from const import CONFIG_FILE


class SqliteConfig(BaseModel):
    type: Literal["SQLite"] = "SQLite"
    path: Path


class ServerConfig(BaseModel):
    type: Literal["MySQL", "PostgreSQL"]
    host: str
    port: int
    username: str
    password: str
    database: str


class Config(BaseModel):
    db: SqliteConfig | ServerConfig = SqliteConfig(path=Path("db.sqlite"))

    def save(self):
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(self.model_dump_json(), "utf-8")


def load_config() -> Config:
    return Config.model_validate_json(CONFIG_FILE.read_text("utf-8"))


if not CONFIG_FILE.exists():
    Config().save()

config = load_config()
