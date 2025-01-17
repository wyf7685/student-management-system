from sqlalchemy import URL, Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, declared_attr, sessionmaker
from sqlalchemy.util import immutabledict

from config import config, SqliteConfig, ServerConfig

__token: object = None
__engine: Engine | None = None
__session_maker: sessionmaker | None = None


def get_token() -> object:
    return __token


def _create_sqlite_engine(config: SqliteConfig) -> Engine:
    url = f"sqlite:///{config.path}"
    engine = create_engine(url)

    def fn(con, _):
        con.execute("pragma foreign_keys=ON")

    event.listen(engine, "connect", fn)

    return engine


def _create_server_engine(config: ServerConfig) -> Engine:
    url = URL(
        drivername=config.type.lower(),
        username=config.username,
        password=config.password,
        host=config.host,
        port=config.port,
        database=config.database,
        query=immutabledict(),
    )
    return create_engine(url)


def get_engine() -> Engine:
    global __engine, __token

    if __engine is None:
        if config.db.type == "SQLite":
            __engine = _create_sqlite_engine(config.db)
        else:
            __engine = _create_server_engine(config.db)

        if __token is None:
            create_all()

        __token = object()

    return __engine


def get_session() -> tuple[Session, object]:
    global __session_maker

    if __session_maker is None:
        __session_maker = sessionmaker(bind=get_engine())

    return __session_maker(), get_token()


def validate_token(token: object) -> bool:
    return token is get_token()


def reload_engine() -> Engine:
    global __engine, __session_maker, __token

    if __session_maker is not None:
        __session_maker.close_all()

    if __engine is not None:
        __engine.dispose()

    __engine = __session_maker = __token = None
    return get_engine()


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


def create_all():
    Base.metadata.create_all(get_engine())

    setup_default_admin()
