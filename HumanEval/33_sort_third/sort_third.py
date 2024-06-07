def sort_third(l: list):
    l = list(l)
    l[::3] = sorted(l[::3])
    return l
def check(sort_third):
    assert sort_third([1, 2, 3]) == [1, 2, 3]
    assert sort_third([5, 6, 3, 4, 8, 9, 2]) == [2, 6, 3, 4, 8, 9, 5]
check(sort_third)
