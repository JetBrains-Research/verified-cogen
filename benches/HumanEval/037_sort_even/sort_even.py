def sort_even(l: list):
    evens = l[::2]
    odds = l[1::2]
    evens.sort()
    ans = []
    for e, o in zip(evens, odds):
        ans.extend([e, o])
    if len(evens) > len(odds):
        ans.append(evens[-1])
    return ans
def check(sort_even):
    assert tuple(sort_even([1, 2, 3])) == tuple([1, 2, 3])
    assert tuple(sort_even([5, 6,3,4])) == tuple([3,6,5,4])
check(sort_even)
