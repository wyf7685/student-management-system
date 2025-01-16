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
    from .manager import DBManager
    from .models import Student

    student = {
        "student_id": 2021010101,
        "name": "张三",
        "gender": "M",
        "birth": "2003-01-01",
        "phone": "13800138000",
        "email": "zhangsan@xxx.edu.cn",
        "college_id": 1,
        "major_id": 1,
        "class_id": 1,
        "enrollment_date": "2021-09-01",
    }

    db = DBManager.student()
    if not db.get_student(111):
        db.add_student(Student(**student))

    db = DBManager.system_account()
    if not db.find_account("Admin", "admin"):
        db.add_account("Admin", "admin", "admin")
    if not db.find_account("Student", "111"):
        db.add_account("Student", "111", "pswd")
    if not db.find_account("Teacher", "222"):
        db.add_account("Teacher", "222", "pswd")


def create_all():
    Base.metadata.create_all(get_engine())

    # setup_default_data()
