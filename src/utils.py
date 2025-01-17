import sys
from pathlib import Path


def check[T](value: T | None, /) -> T:
    assert value is not None
    return value


def get_resource_path(relative_path: str):
    """获取资源的绝对路径"""
    root = getattr(sys, "_MEIPASS", Path(__file__).parent.parent)
    return (Path(root) / relative_path).absolute()
