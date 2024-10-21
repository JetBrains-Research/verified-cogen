def circular_shift(x, shift):
    s = str(x)
    if shift > len(s):
        return s[::-1]
    else:
        return s[len(s) - shift:] + s[:len(s) - shift]
def check(circular_shift):
    # Check some simple cases
    assert circular_shift(12, 2) == "12"
    assert circular_shift(12, 1) == "21", "This prints if this assert fails 1 (good for debugging!)"
    # Check some edge cases that are easy to work out by hand.
check(circular_shift)
