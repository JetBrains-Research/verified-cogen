def add(x: int, y: int):
    return x + y
def check(add):
    import random
    assert add(2, 3) == 5
    assert add(5, 7) == 12
check(add)
