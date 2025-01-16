from sqlalchemy import URL, Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, declared_attr, sessionmaker
from sqlalchemy.util import immutabledict

from config import config

__token = object()
__engine: Engine | None = None
__session_maker: sessionmaker | None = None


def get_engine() -> Engine:
    global __engine

    if __engine is None:
        if config.db.type == "SQLite":
            url = f"sqlite:///{config.db.path}"
            __engine = create_engine(url)
            # SQLite 数据库默认不启用外键约束，需要手动开启
            event.listen(
                __engine,
                "connect",
                lambda con, _: con.execute("pragma foreign_keys=ON"),
            )
        else:
            url = URL(
                drivername=config.db.type.lower(),
                username=config.db.username,
                password=config.db.password,
                host=config.db.host,
                port=config.db.port,
                database=config.db.database,
                query=immutabledict(),
            )
            __engine = create_engine(url)

    return __engine


def get_session() -> Session:
    global __session_maker

    if __session_maker is None:
        __session_maker = sessionmaker(bind=get_engine())

    return __session_maker()


def reload_engine():
    global __engine, __session_maker, __token
    __engine = __session_maker = None
    create_all()
    __token = object()


def get_token():
    return __token


class Base(DeclarativeBase):
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        # 将 CamelCase 类名转换为 snake_case 表名
        # 例如: StudentInfo -> student_info
        name = cls.__name__
        return "".join(
            f"_{c.lower()}" if c.isupper() else c.lower() for c in name
        ).lstrip("_")


def setup_default_data():
    from pathlib import Path

    from sqlalchemy import text

    stmts = [
        s.strip()
        for s in (Path(__file__).parent / "default.sql").read_text("utf-8").split(";")
        if s.strip()
    ]

    with get_engine().begin() as conn:
        for stmt in stmts:
            conn.execute(text(stmt))


def create_all():
    Base.metadata.create_all(get_engine())

    setup_default_data()
