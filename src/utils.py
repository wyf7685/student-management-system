def check[T](value: T | None, /) -> T:
    assert value is not None
    return value
