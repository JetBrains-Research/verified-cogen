from typing import List


def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    return [x for x in strings if substring in x]

def check(filter_by_substring):
    assert filter_by_substring([], 'a') == []
    assert filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a') == ['abc', 'bacd', 'array']
check(filter_by_substring)
