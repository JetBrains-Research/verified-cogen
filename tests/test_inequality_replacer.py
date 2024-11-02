from textwrap import dedent
from verified_cogen.tools.inequality_replacer import replace_inequalities, contains_double_inequality

def test_simple_contains1():
    code = dedent(
        """\
        def test():
            if a >= b >= c > d:
                print('Chained')
        """
    )

    assert contains_double_inequality(code)

def test_simple_contains2():
    code = dedent(
        """\
Implies(1 <= k < d_6_i_, xs[k - 1] <= xs[k])
d_4_increasing_ == Forall(int, lambda k: Implies(1 <= k < d_6_i_, xs[k - 1] <= xs[k]))
Invariant(d_4_increasing_ == Forall(int, lambda k: Implies(1 <= k < d_6_i_, xs[k - 1] <= xs[k])))
        """
    )

    new_code = replace_inequalities(code)
    compare_code = dedent(
        """\
Implies(1 <= k and k < d_6_i_, xs[k - 1] <= xs[k])
d_4_increasing_ == Forall(int, lambda k: Implies(1 <= k and k < d_6_i_, xs[k - 1] <= xs[k]))
Invariant(d_4_increasing_ == Forall(int, lambda k: Implies(1 <= k and k < d_6_i_, xs[k - 1] <= xs[k])))"""
    )

    assert contains_double_inequality(code)
    assert new_code == compare_code

def test_simple_contains3():
    code = dedent(
        """\
        def test():
            if a < b and b < c and c <= d:
                print('Chained')
        """
    )

    assert not contains_double_inequality(code)

def test_simple():
    code = dedent(
        """\
        def test():
            if a < b < c < d:
                print('Chained')
        """
    )

    new_code = replace_inequalities(code)

    compare_code = dedent(
        """\
        def test():
            if a < b and b < c and (c < d):
                print('Chained')"""
    )

    assert new_code == compare_code

def test_simple1():
    code = dedent(
        """\
        def test():
            if a < b <= c < d:
                print('Chained')
        """
    )

    new_code = replace_inequalities(code)

    compare_code = dedent(
        """\
        def test():
            if a < b and b <= c and (c < d):
                print('Chained')"""
    )

    assert new_code == compare_code

def test_complicated():
    code = dedent(
        """\
from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *

@Pure
def factorial__spec(n : int) -> int :
    Requires(n >= -1)
    Ensures(Result() >= 0)
    if n == -1:
        return 1
    else:
        return (n + 1) * factorial__spec(n - 1)

@Pure
def sum__spec(n : int) -> int :
    Requires(n >= -1)
    Ensures(Result() >= 0)
    if 0 > n:
        return 0
    else:
        return n + 1 + sum__spec(n - 1)

def f(n : int) -> List[int]:
    Requires((n) >= (1))
    Ensures(Acc(list_pred(Result())))
    Ensures((len(Result())) == (n))
    Ensures(Forall(int, lambda d_2_i_:
        not ((((d_2_i_) >= (0)) and ((d_2_i_) < (len(Result())))) and (((d_2_i_ % 2)) == (0))) or (((Result())[d_2_i_]) == (factorial__spec(d_2_i_ - 1)))))
    Ensures(Forall(int, lambda d_3_i_:
        not ((((d_3_i_) >= (0)) and ((d_3_i_) < (len(Result())))) and (((d_3_i_ % 2)) != (0))) or (((Result())[d_3_i_]) == (sum__spec(d_3_i_ - 1)))))

    result: List[int] = []
    d_4_i_ = 0
    while (d_4_i_) < (n):
        Invariant(0 <= d_4_i_ <= n)
        Invariant(len(result) == d_4_i_)
        Invariant(Acc(list_pred(result)))
        Invariant(Forall(int, lambda i:Implies( (0 <= i < d_4_i_ and i % 2 == 0) , result[i] == factorial__spec(i - 1))))
        Invariant(Forall(int, lambda i:Implies( (0 <= i < d_4_i_ and i % 2 != 0) , result[i] == sum__spec(i - 1))))

        if ((d_4_i_ % 2)) == (0):
            d_7_x_ = 1
            d_8_j_ = 0
            while (d_8_j_) < (d_4_i_):
                Invariant(0 <= d_8_j_ <= d_4_i_)
                Invariant(d_7_x_ == factorial__spec(d_8_j_ - 1))
                d_7_x_ = (d_7_x_) * (d_8_j_ + 1)
                d_8_j_ = (d_8_j_) + (1)
            result = (result) + [d_7_x_]
        else:
            d_9_x_ = 0
            d_10_j_ = 0
            while (d_10_j_) < (d_4_i_):
                Invariant(0 <= d_10_j_ <= d_4_i_)
                Invariant(d_9_x_ == sum__spec(d_10_j_ - 1))
                d_9_x_ = (d_9_x_) + (d_10_j_ + 1)
                d_10_j_ = (d_10_j_) + (1)
            result = (result) + [d_9_x_]
        d_4_i_ = (d_4_i_) + (1)
    return result
        """
    )

    new_code = replace_inequalities(code)

    compare_code = dedent(
        """\
from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *

@Pure
def factorial__spec(n: int) -> int:
    Requires(n >= -1)
    Ensures(Result() >= 0)
    if n == -1:
        return 1
    else:
        return (n + 1) * factorial__spec(n - 1)

@Pure
def sum__spec(n: int) -> int:
    Requires(n >= -1)
    Ensures(Result() >= 0)
    if 0 > n:
        return 0
    else:
        return n + 1 + sum__spec(n - 1)

def f(n: int) -> List[int]:
    Requires(n >= 1)
    Ensures(Acc(list_pred(Result())))
    Ensures(len(Result()) == n)
    Ensures(Forall(int, lambda d_2_i_: not ((d_2_i_ >= 0 and d_2_i_ < len(Result())) and d_2_i_ % 2 == 0) or Result()[d_2_i_] == factorial__spec(d_2_i_ - 1)))
    Ensures(Forall(int, lambda d_3_i_: not ((d_3_i_ >= 0 and d_3_i_ < len(Result())) and d_3_i_ % 2 != 0) or Result()[d_3_i_] == sum__spec(d_3_i_ - 1)))
    result: List[int] = []
    d_4_i_ = 0
    while d_4_i_ < n:
        Invariant(0 <= d_4_i_ and d_4_i_ <= n)
        Invariant(len(result) == d_4_i_)
        Invariant(Acc(list_pred(result)))
        Invariant(Forall(int, lambda i: Implies((0 <= i and i < d_4_i_) and i % 2 == 0, result[i] == factorial__spec(i - 1))))
        Invariant(Forall(int, lambda i: Implies((0 <= i and i < d_4_i_) and i % 2 != 0, result[i] == sum__spec(i - 1))))
        if d_4_i_ % 2 == 0:
            d_7_x_ = 1
            d_8_j_ = 0
            while d_8_j_ < d_4_i_:
                Invariant(0 <= d_8_j_ and d_8_j_ <= d_4_i_)
                Invariant(d_7_x_ == factorial__spec(d_8_j_ - 1))
                d_7_x_ = d_7_x_ * (d_8_j_ + 1)
                d_8_j_ = d_8_j_ + 1
            result = result + [d_7_x_]
        else:
            d_9_x_ = 0
            d_10_j_ = 0
            while d_10_j_ < d_4_i_:
                Invariant(0 <= d_10_j_ and d_10_j_ <= d_4_i_)
                Invariant(d_9_x_ == sum__spec(d_10_j_ - 1))
                d_9_x_ = d_9_x_ + (d_10_j_ + 1)
                d_10_j_ = d_10_j_ + 1
            result = result + [d_9_x_]
        d_4_i_ = d_4_i_ + 1
    return result"""
    )

    assert new_code == compare_code

def test_complicated1():

    code = dedent("""\
def BubbleSort(a1 : List[int]) -> List[int]:
    Requires(Acc(list_pred(a1), 1/2))
    Requires(Forall(int, lambda i : Implies(i >= 0 and i < len(a1), a1[i] >= 0)))
    Ensures(Acc(list_pred(a1), 1/2))
    Ensures(Acc(list_pred(Result())))
    Ensures((len(a1)) == (len(Result())))
    Ensures(Forall(int, lambda i : Implies(i >= 0 and i < len(Result()), Result()[i] >= 0)))
    Ensures(Forall(int, lambda d_0_i_:
        Forall(int, lambda d_1_j_:
            Implies((((0) <= (d_0_i_)) and ((d_0_i_) < (d_1_j_))) and ((d_1_j_) < (len((Result())))), popcount((Result())[d_0_i_]) <= popcount((Result())[d_1_j_])))))

    a = list(a1)
    d_2_i_ = int(0)
    d_2_i_ = (len((a))) - (1)
    while (d_2_i_) > (0):
        Invariant(Acc(list_pred(a)))
        Invariant(0 <= d_2_i_ < len(a))
        Invariant(Forall(int, lambda k: Implies(d_2_i_ < k and k < len(a), Forall(int, lambda m: Implies(0 <= m and m < k, popcount(a[m]) <= popcount(a[k]))))))
        Invariant(Forall(int, lambda i: Implies(0 <= i and i < len(a), a[i] >= 0)))
        Invariant(len(a) == len(a1))
        Invariant(Forall(int, lambda i: Implies(0 <= i and i < len(a), Exists(int, lambda j: (0 <= j and j < len(a1) and a[i] == a1[j])))))
        Invariant(Forall(int, lambda i: Implies(0 <= i and i < len(a1), Exists(int, lambda j: (0 <= j and j < len(a) and a1[i] == a[j])))))

        d_7_j_ = int(0)
        d_7_j_ = 0
        while (d_7_j_) < (d_2_i_):
            Invariant(Acc(list_pred(a)))
            Invariant(0 <= d_7_j_ <= d_2_i_ < len(a))
            Invariant(Forall(int, lambda k: Implies(0 <= k and k < d_7_j_, popcount(a[k]) <= popcount(a[d_7_j_]))))
            Invariant(Forall(int, lambda i: Implies(0 <= i and i < len(a), a[i] >= 0)))
            Invariant(len(a) == len(a1))
            Invariant(Forall(int, lambda i: Implies(0 <= i and i < len(a), Exists(int, lambda j: (0 <= j and j < len(a1) and a[i] == a1[j])))))
            Invariant(Forall(int, lambda i: Implies(0 <= i and i < len(a1), Exists(int, lambda j: (0 <= j and j < len(a) and a1[i] == a[j])))))

            if popcount((a)[d_7_j_]) > popcount((a)[(d_7_j_) + (1)]):
                rhs0_ = (a)[(d_7_j_) + (1)]
                (a)[(d_7_j_) + (1)] = (a)[d_7_j_]
                (a)[d_7_j_] = rhs0_
            d_7_j_ = (d_7_j_) + (1)
        d_2_i_ = (d_2_i_) - (1)
    return a
    """)

    new_code = replace_inequalities(code)

    print(new_code)