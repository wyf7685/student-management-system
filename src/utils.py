import sys
from pathlib import Path


def check[T](value: T | None, /) -> T:
    if value is not None:
        return value

    frame = sys._getframe(1)  # noqa: SLF001
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    raise ValueError(f"Value is None at {filename}:{lineno}")


def get_resource_path(relative_path: str):
    """获取资源的绝对路径"""
    root = getattr(sys, "_MEIPASS", Path(__file__).parent.parent)
    return (Path(root) / relative_path).absolute()
