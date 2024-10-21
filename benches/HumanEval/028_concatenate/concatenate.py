from typing import List


def concatenate(strings: List[str]) -> str:
    return ''.join(strings)
def check(concatenate):
    assert concatenate([]) == ''
    assert concatenate(['a', 'b', 'c']) == 'abc'
check(concatenate)
