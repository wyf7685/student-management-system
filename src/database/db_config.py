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


DEFAULT_ADMIN_SQL = """
INSERT INTO system_account (
    role, password, salt, student_id, teacher_id, admin_id
)
SELECT
    'Admin',
    '697d423a3558f0ab2e71cea50014029628ee62cd154e1e81d5cd960932cce9b6',
    'default',
    NULL,
    NULL,
    'admin'
WHERE NOT EXISTS (
    SELECT 1 FROM system_account
    WHERE role = 'Admin' AND admin_id = 'admin'
);
"""


def setup_default_admin():
    from sqlalchemy import text

    with get_engine().begin() as conn:
        conn.execute(text(DEFAULT_ADMIN_SQL))


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

    setup_default_admin()
