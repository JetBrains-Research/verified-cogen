def greatest_common_divisor(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a
def check(greatest_common_divisor):
    assert greatest_common_divisor(3, 5) == 1
    assert greatest_common_divisor(25, 15) == 5
check(greatest_common_divisor)
