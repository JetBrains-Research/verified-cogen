from textwrap import dedent

from verified_cogen.smart_search.scoring_functions.nagini_simple import NaginiSimpleScoringFunction


def test_nagini_scoring():
    code = dedent(
    """\
from typing import List, Tuple
from nagini_contracts.contracts import *
def even__odd__count(n : int) -> Tuple[int, int]:
    Requires((n) > (0))
    Ensures((Result()[0]) == (even__count(n)))
    Ensures((Result()[1]) == (odd__count(n)))
    even : int = int(0)
    odd : int = int(0)
    num : int = n
    while (num) > (0):
        Invariant(num >= 0)
        Invariant(even >= 0)
        Invariant(odd >= 0)
        Invariant(even + odd == len(str(n)) - len(str(num)))
        Invariant(even == even__count(n) - even__count(num))
        Invariant(odd == odd__count(n) - odd__count(num))
        even = (even) + ((num % 2) == 0)
        odd = (odd) + (num % 2)
        num = (num // 10)
    return (even, odd)

@Pure
def odd__count(n : int) -> int :
    Requires(n >= 0)
    if n == 0:
        return 0
    else:
        return (n % 2) + odd__count(n // 10)

@Pure
def even__count(n : int) -> int :
    Requires(n >= 0)
    if n == 0:
        return 0
    else:
        return ((n % 2) == 0) + even__count(n // 10)
    """
    )

    error = dedent(
    """\
Verification failed
Errors:
Loop invariant might not be preserved. Assertion ((even + odd) == (len(str(n)) - len(str(num)))) might not hold. (155_even_odd_count.2.py@14.18--14.59)
Verification took 8.39 seconds."""
    )

    sc = NaginiSimpleScoringFunction(0.5, -10).score(code, error)
    assert sc == 0.5


def test_nagini_scoring1():
    code = dedent(
    """\
from typing import cast, List, Dict, Set, Optional, Union, Tuple
from nagini_contracts.contracts import *
def sort__array(s : List[int]) -> List[int]:
    Requires(Acc(list_pred(s)))
    Ensures(Acc(list_pred(s)))
    Ensures(Acc(list_pred(Result())))
    Ensures((len(Result())) == (len(s)))
    Ensures(not (((len(s)) > (0)) and ((((((s)[0]) + ((s)[(len(s)) - (1)])) % 2)) == (0))) or (Forall(int, lambda i:
        Forall(int, lambda j:
            not ((((0) <= (i)) and ((i) < (j))) and ((j) < (len(Result())))) or (((Result())[i]) >= ((Result())[j]))))))
    Ensures(not (((len(s)) > (0)) and ((((((s)[0]) + ((s)[(len(s)) - (1)])) % 2)) != (0))) or (Forall(int, lambda i:
        Forall(int, lambda j:
            not ((((0) <= (i)) and ((i) < (j))) and ((j) < (len(Result())))) or (((Result())[i]) <= ((Result())[j]))))))
    sorted : List[int] = []
    if (len(s)) == (0):
        sorted = list([])
        return sorted
    elif (((((s)[0]) + ((s)[(len(s)) - (1)])) % 2)) == (0):
        t : List[int] = BubbleSort(s)
        sorted = reverse(t) 
        return sorted
    else:
        sorted = BubbleSort(s)
        return sorted
def reverse(str : List[int]) -> List[int]:
    Requires(Acc(list_pred(str), 1/2))
    Requires(Forall(int, lambda x: Forall(int, lambda y: not (((0) <= (x)) and ((x) < (y)) and ((y) < (len(str)))) or ((str)[x] <= (str)[y]))))
    Ensures(Acc(list_pred(str), 1/2))
    Ensures(Acc(list_pred(Result())))
    Ensures(Forall(int, lambda x: Forall(int, lambda y: not (((0) <= (x)) and ((x) < (y)) and ((y) < (len(Result())))) or ((Result())[x] >= (Result())[y]))))
    Ensures(str == Old(str))
    Ensures((len(Result())) == (len(str)))
    Ensures(Forall(int, lambda k:
        not (((0) <= (k)) and ((k) < (len(str)))) or (((Result())[k]) == ((str)[((len(str)) - (1)) - (k)]))))
    rev : List[int] = []
    i : int = 0
    while (i) < (len(str)):
        Invariant(Acc(list_pred(str)))
        Invariant(Acc(list_pred(rev)))
        Invariant(0 <= i and i <= len(str))
        Invariant(len(rev) == i)
        Invariant(Forall(int, lambda k: not (0 <= k and k < i) or (rev[k] == str[len(str) - 1 - k])))
        Invariant(Forall(int, lambda x: Forall(int, lambda y: not (0 <= x and x < y and y < len(str)) or (str[x] <= str[y]))))
        rev = (rev) + [(str)[(len(str) - (i)) - (1)]]
        i = (i) + (1)
    return rev
def BubbleSort(a1 : List[int]) -> List[int]:
    Requires(Acc(list_pred(a1), 1/2))
    Ensures(Acc(list_pred(a1), 1/2))
    Ensures(Acc(list_pred(Result())))
    Ensures((len(a1)) == (len(Result())))
    Ensures(Forall(int, lambda i:
        Forall(int, lambda j:
            Implies((((0) <= (i)) and ((i) < (j))) and ((j) < (len((Result())))), ((Result())[i]) <= ((Result())[j])))))
    a : List[int] = list(a1)
    i : int = (len((a))) - (1)
    while (i) > (0):
        Invariant(Acc(list_pred(a)))
        Invariant(0 < i and i < len(a))
        Invariant(len(a) == len(a1))
        Invariant(Forall(int, lambda k: Forall(int, lambda m: not (i < k and k < m and m < len(a)) or (a[k] <= a[m]))))
        j : int = 0
        while (j) < (i):
            Invariant(Acc(list_pred(a)))
            Invariant(0 <= j and j < i)
            Invariant(len(a) == len(a1))
            Invariant(Forall(int, lambda k: Forall(int, lambda m: not (i < k and k < m and m < len(a)) or (a[k] <= a[m]))))
            Invariant(Forall(int, lambda k: not (0 <= k and k < j) or a[k] <= a[k + 1]))
            if ((a)[j]) > ((a)[(j) + (1)]):
                rhs0_ : int = (a)[(j) + (1)]
                (a)[(j) + (1)] = (a)[j]
                (a)[j] = rhs0_
            j = (j) + (1)
        i = (i) - (1)
    return a
    """
    )

    error = dedent(
        """\
Verification failed
Errors:
Loop invariant might not hold on entry. There might be insufficient permission to access list_pred(str). (088-sort_array.2.py@38.22--38.36)
The precondition of function len might not hold. There might be insufficient permission. (088-sort_array.2.py@60.28--60.35)
Verification took 10.38 seconds."""
    )

    sc = NaginiSimpleScoringFunction(0.5, -10).score(code, error)
    assert sc == 0


def test_nagini_scoring2():

    sc = NaginiSimpleScoringFunction(0.5, -10).score("", "Verification timed out")
    assert sc == -10

def test_nagini_scoring3():

    error = dedent(
    """\
    Translation failed
    Invalid program: purity.violated (/home/aleksandr/verified-cogen/log_tries/humaneval-nagini-several/mode1/run_4/000-has-close-elements.2.py@35.17)
    """
    )
    sc = NaginiSimpleScoringFunction(0.5, -10).score("", error)
    assert sc == -1e9