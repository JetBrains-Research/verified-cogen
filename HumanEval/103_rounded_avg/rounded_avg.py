def rounded_avg(n, m):
    if m < n:
        return -1
    summation = 0
    for i in range(n, m+1):
        summation += i
    return bin(round(summation/(m - n + 1)))
def check(rounded_avg):
    # Check some simple cases
    assert rounded_avg(1, 5) == "0b11"
    # Check some edge cases that are easy to work out by hand.
    assert rounded_avg(7, 5) == -1
    assert rounded_avg(10,20) == "0b1111"
    assert rounded_avg(20, 33) == "0b11010"
check(rounded_avg)
