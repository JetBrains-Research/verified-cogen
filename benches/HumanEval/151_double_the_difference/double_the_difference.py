def double_the_difference(lst):
    return sum([i**2 for i in lst if i > 0 and i%2!=0 and "." not in str(i)])
def check(double_the_difference):
    # Check some simple cases
    assert double_the_difference([1,3,2,0]) == 10 , "This prints if this assert fails 1 (good for debugging!)"
    assert double_the_difference([-1,-2,0]) == 0 , "This prints if this assert fails 2 (good for debugging!)"
    assert double_the_difference([9,-2]) == 81 , "This prints if this assert fails 3 (good for debugging!)"
    assert double_the_difference([0]) == 0 , "This prints if this assert fails 4 (good for debugging!)"
check(double_the_difference)
