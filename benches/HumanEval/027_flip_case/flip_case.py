def flip_case(string: str) -> str:
    return string.swapcase()
def check(flip_case):
    assert flip_case('Hello') == 'hELLO'
check(flip_case)
