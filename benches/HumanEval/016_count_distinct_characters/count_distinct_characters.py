def count_distinct_characters(string: str) -> int:
    return len(set(string.lower()))
def check(count_distinct_characters):
    assert count_distinct_characters('xyzXYZ') == 3
    assert count_distinct_characters('Jerry') == 4
check(count_distinct_characters)
