def add(lst):
    return sum([lst[i] for i in range(1, len(lst), 2) if lst[i]%2 == 0])
def check(add):
    # Check some simple cases
    assert add([4, 2, 6, 7]) == 2
    # Check some edge cases that are easy to work out by hand.
check(add)
