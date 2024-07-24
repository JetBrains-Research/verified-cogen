from typing import Any, List


def filter_integers(values: List[Any]) -> List[int]:
    return [x for x in values if isinstance(x, int)]
def check(filter_integers):
    assert filter_integers(['a', 3.14, 5]) == [5]
    assert filter_integers([1, 2, 3, 'abc', {}, []]) == [1,2,3]
check(filter_integers)
