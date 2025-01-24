from textwrap import dedent

from verified_cogen.runners.rewriters.nagini_rewriter import NaginiRewriter
from verified_cogen.runners.rewriters.nagini_rewriter_fixing import NaginiRewriterFixing
from verified_cogen.runners.rewriters.nagini_rewriter_fixing_ast import (
    NaginiRewriterFixingAST,
)
from verified_cogen.tools import rewrite_error


def test_nagini_rewriter():
    code = dedent(
        """\
from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *

def Compare(scores: List[int], guesses: List[int]) -> List[int]:
    Requires(Acc(list_pred(guesses)))
    Requires(Acc(list_pred(scores)))
    Requires(len(scores) == len(guesses))
    Ensures(Acc(list_pred(guesses)))
    Ensures(Acc(list_pred(scores)))
    Ensures(Acc(list_pred(Result())))
    Ensures(len(Result()) == len(scores))
    Ensures(len(scores) == len(guesses))
    Ensures(Forall(int, lambda d_0_i_:
    not (0 <= d_0_i_ and d_0_i_ < len(Result())) or (Result()[d_0_i_] == abs(scores[d_0_i_] - guesses[d_0_i_]))))

    result = [int(0)] * 0
    nw0_ = [int(0)] * len(scores)
    result = nw0_
    d_1_i_ = int(0)
    d_1_i_ = 0
    while d_1_i_ < len(scores):
        Invariant(Acc(list_pred(scores)))
        Invariant(Acc(list_pred(guesses)))
        Invariant(Acc(list_pred(result)))
        Invariant(0 <= d_1_i_ and d_1_i_ <= len(scores))
        Invariant(len(result) == len(scores))
        Invariant(len(scores) == len(guesses))
        Invariant(Forall(int, lambda k: (0 <= k and k < d_1_i_) ==> (result[k] == abs(scores[k] - guesses[k]))))
        Invariant(Forall(int, lambda k: (0 <= k and k < len(scores)) ==> (scores[k] == Old(scores[k]))))
        Invariant(Forall(int, lambda k: (0 <= k and k < len(guesses)) ==> (guesses[k] == Old(guesses[k]))))
        result[d_1_i_] = abs(scores[d_1_i_] - guesses[d_1_i_])
        d_1_i_ = d_1_i_ + 1
    return result
    """
    )

    error = dedent(
        """\
Manual inspection revealed occurrences of `==>` operator for implication on the following positions:
(28, 65), (29, 70), (30, 71)
`==>` operator does not exist in Nagini. All occurrences of `==>` operator should be replaced with `Implies(a, b)` operator, that is used to express implication in Nagini
    """
    )

    _, prompt = NaginiRewriter().rewrite(code)
    assert prompt == error


def test_nagini_rewriter1():
    code = dedent(
        """\
from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *

def get__positive(l : List[int]) -> List[int]:
    Requires(Acc(list_pred(l)))
    Ensures(Acc(list_pred(l)))
    Ensures(Acc(list_pred(Result())))
    Ensures(Forall(int, lambda d_0_i_:
        not (((d_0_i_) >= (0)) and ((d_0_i_) < (len(Result())))) or (((Result())[d_0_i_]) > (0))))
    Ensures((len(Result())) <= (len(l)))
    Ensures(Forall(int, lambda d_1_i1_:
        not (((d_1_i1_) >= (0)) and ((d_1_i1_) < (len(l)))) or (not (((l)[d_1_i1_]) > (0)) or (Exists(int, lambda d_2_i2_:
            (((d_2_i2_) >= (0)) and ((d_2_i2_) < (len(Result())))) and (((Result())[d_2_i2_]) == ((l)[d_1_i1_])))))))
    Ensures(((len(Result())) == (0)) or (Forall(int, lambda d_3_i1_:
        not (((d_3_i1_) >= (0)) and ((d_3_i1_) < (len(Result())))) or (Exists(int, lambda d_4_i2_:
            (((d_4_i2_) >= (0)) and ((d_4_i2_) < (len(l)))) and (((l)[d_4_i2_]) == ((Result())[d_3_i1_])))))))
    result = list([0] * 0)
    d_5_i_ = int(0)
    d_5_i_ = 0
    while (d_5_i_) < (len(l)):
        Invariant(Acc(list_pred(l)))
        Invariant(Acc(list_pred(result)))
        Invariant(0 <= d_5_i_ and d_5_i_ <= len(l))
        Invariant(len(result) <= d_5_i_)
        Invariant(Forall(int, lambda j: (0 <= j and j < len(result)) ==> (result[j] > 0)))
        Invariant(Forall(int, lambda j: (0 <= j and j < d_5_i_) ==>
                  (l[j] > 0 ==> Exists(int, lambda k: (0 <= k and k < len(result) and result[k] == l[j])))))
        Invariant(Forall(int, lambda j: (0 <= j and j < len(result)) ==>
                  Exists(int, lambda k: (0 <= k and k < d_5_i_ and l[k] == result[j]))))
        Invariant(Forall(int, lambda j1, j2: (0 <= j1 and j1 < j2 and j2 < len(result)) ==>
                  Exists(int, lambda k1, k2: (0 <= k1 and k1 < k2 and k2 < d_5_i_ and
                                              l[k1] == result[j1] and l[k2] == result[j2]))))
        d_13_n_ = int(0)
        d_13_n_ = (l)[d_5_i_]
        if (d_13_n_) > (0):
            d_17_res__prev_ = result
            result = (result) + ([d_13_n_])
        d_5_i_ = (d_5_i_) + (1)
    return result
    """
    )

    res = dedent(
        """\
from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *

def get__positive(l : List[int]) -> List[int]:
    Requires(Acc(list_pred(l)))
    Ensures(Acc(list_pred(l)))
    Ensures(Acc(list_pred(Result())))
    Ensures(Forall(int, lambda d_0_i_:
        not (((d_0_i_) >= (0)) and ((d_0_i_) < (len(Result())))) or (((Result())[d_0_i_]) > (0))))
    Ensures((len(Result())) <= (len(l)))
    Ensures(Forall(int, lambda d_1_i1_:
        not (((d_1_i1_) >= (0)) and ((d_1_i1_) < (len(l)))) or (not (((l)[d_1_i1_]) > (0)) or (Exists(int, lambda d_2_i2_:
            (((d_2_i2_) >= (0)) and ((d_2_i2_) < (len(Result())))) and (((Result())[d_2_i2_]) == ((l)[d_1_i1_])))))))
    Ensures(((len(Result())) == (0)) or (Forall(int, lambda d_3_i1_:
        not (((d_3_i1_) >= (0)) and ((d_3_i1_) < (len(Result())))) or (Exists(int, lambda d_4_i2_:
            (((d_4_i2_) >= (0)) and ((d_4_i2_) < (len(l)))) and (((l)[d_4_i2_]) == ((Result())[d_3_i1_])))))))
    result = list([0] * 0)
    d_5_i_ = int(0)
    d_5_i_ = 0
    while (d_5_i_) < (len(l)):
        Invariant(Acc(list_pred(l)))
        Invariant(Acc(list_pred(result)))
        Invariant(0 <= d_5_i_ and d_5_i_ <= len(l))
        Invariant(len(result) <= d_5_i_)
        Invariant(Forall(int, lambda j:Implies( (0 <= j and j < len(result)) , (result[j] > 0))))
        Invariant(Forall(int, lambda j:Implies( (0 <= j and j < d_5_i_) ,
                  (Implies(l[j] > 0 , Exists(int, lambda k: (0 <= k and k < len(result) and result[k] == l[j])))))))
        Invariant(Forall(int, lambda j:Implies( (0 <= j and j < len(result)) ,
                  Exists(int, lambda k: (0 <= k and k < d_5_i_ and l[k] == result[j])))))
        Invariant(Forall(int, lambda j1, j2:Implies( (0 <= j1 and j1 < j2 and j2 < len(result)) ,
                  Exists(int, lambda k1, k2: (0 <= k1 and k1 < k2 and k2 < d_5_i_ and
                                              l[k1] == result[j1] and l[k2] == result[j2])))))
        d_13_n_ = int(0)
        d_13_n_ = (l)[d_5_i_]
        if (d_13_n_) > (0):
            d_17_res__prev_ = result
            result = (result) + ([d_13_n_])
        d_5_i_ = (d_5_i_) + (1)
    return result
    """
    )

    prg = NaginiRewriterFixing().replace_impl(code)
    assert prg == res


def test_nagini_rewriter2():
    code = dedent(
        """\
def fizz__buzz(n : int) -> int:
    Requires(n >= 0)
    Ensures(Result() >= 0)
    Ensures((Result()) == fizz_buzz_fun(n))
    result = int(0)
    result = 0
    d_1_i_ = int(0)
    d_1_i_ = 0
    while (d_1_i_) < (n):
        Invariant(0 <= d_1_i_)
        Invariant(d_1_i_ <= n)
        Invariant(result >= 0)
        Invariant(result == fizz_buzz_fun(d_1_i_))
        Invariant(Forall(int, lambda k: (0 <= k and k < d_1_i_) ==>
                         (((k % 11 == 0) or (k % 13 == 0)) ==>
                          (fizz_buzz_fun(k+1) == fizz_buzz_fun(k) + count7__r(k)))))
        if (((d_1_i_ % 11)) == (0)) or (((d_1_i_ % 13)) == (0)):
            d_4_cnt_ = int(0)
            d_4_cnt_ = count7(d_1_i_)
            result = (result) + (d_4_cnt_)
        d_1_i_ = (d_1_i_) + (1)
    return result
    """
    )

    res = dedent(
        """\
def fizz__buzz(n : int) -> int:
    Requires(n >= 0)
    Ensures(Result() >= 0)
    Ensures((Result()) == fizz_buzz_fun(n))
    result = int(0)
    result = 0
    d_1_i_ = int(0)
    d_1_i_ = 0
    while (d_1_i_) < (n):
        Invariant(0 <= d_1_i_)
        Invariant(d_1_i_ <= n)
        Invariant(result >= 0)
        Invariant(result == fizz_buzz_fun(d_1_i_))
        Invariant(Forall(int, lambda k:Implies( (0 <= k and k < d_1_i_) ,
                         (Implies(((k % 11 == 0) or (k % 13 == 0)) ,
                          (fizz_buzz_fun(k+1) == fizz_buzz_fun(k) + count7__r(k)))))))
        if (((d_1_i_ % 11)) == (0)) or (((d_1_i_ % 13)) == (0)):
            d_4_cnt_ = int(0)
            d_4_cnt_ = count7(d_1_i_)
            result = (result) + (d_4_cnt_)
        d_1_i_ = (d_1_i_) + (1)
    return result
    """
    )

    prg = NaginiRewriterFixing().replace_impl(code)
    assert prg == res


def test_nagini_rewriter3():
    code = dedent(
        """\
from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *

def Compare(scores: List[int], guesses: List[int]) -> List[int]:
    Requires(Acc(list_pred(guesses)))
    Requires(Acc(list_pred(scores)))
    Requires(len(scores) == len(guesses))
    Ensures(Acc(list_pred(guesses)))
    Ensures(Acc(list_pred(scores)))
    Ensures(Acc(list_pred(Result())))
    Ensures(len(Result()) == len(scores))
    Ensures(len(scores) == len(guesses))
    Ensures(Forall(int, lambda d_0_i_:
    not (0 <= d_0_i_ and d_0_i_ < len(Result())) or (Result()[d_0_i_] == abs(scores[d_0_i_] - guesses[d_0_i_]))))

    result = [int(0)] * 0
    nw0_ = [int(0)] * len(scores)
    result = nw0_
    d_1_i_ = int(0)
    d_1_i_ = 0
    while d_1_i_ < len(scores):
        Invariant(Acc(list_pred(scores)))
        Invariant(Acc(list_pred(guesses)))
        Invariant(Acc(list_pred(result)))
        Invariant(0 <= d_1_i_ and d_1_i_ <= len(scores))
        Invariant(len(result) == len(scores))
        Invariant(len(scores) == len(guesses))
        Invariant(Forall(int, lambda k: (0 <= k and k < d_1_i_) ==> (result[k] == abs(scores[k] - guesses[k]))))
        Invariant(Forall(int, lambda k: (0 <= k and k < len(scores)) ==> (scores[k] == Old(scores[k]))))
        Invariant(Forall(int, lambda k: (0 <= k and k < len(guesses)) ==> (guesses[k] == Old(guesses[k]))))
        result[d_1_i_] = abs(scores[d_1_i_] - guesses[d_1_i_])
        d_1_i_ = d_1_i_ + 1
    return result
    """
    )

    error = dedent(
        """\
Manual inspection revealed occurrences of `==>` operator for implication on the following positions:
(28, 65), (29, 70), (30, 71)
`==>` operator does not exist in Nagini. All occurrences of `==>` operator should be replaced with `Implies(a, b)` operator, that is used to express implication in Nagini
We fixed errors with `==>` occurrences for you, and got the following program:
from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *

def Compare(scores: List[int], guesses: List[int]) -> List[int]:
    Requires(Acc(list_pred(guesses)))
    Requires(Acc(list_pred(scores)))
    Requires(len(scores) == len(guesses))
    Ensures(Acc(list_pred(guesses)))
    Ensures(Acc(list_pred(scores)))
    Ensures(Acc(list_pred(Result())))
    Ensures(len(Result()) == len(scores))
    Ensures(len(scores) == len(guesses))
    Ensures(Forall(int, lambda d_0_i_:
    not (0 <= d_0_i_ and d_0_i_ < len(Result())) or (Result()[d_0_i_] == abs(scores[d_0_i_] - guesses[d_0_i_]))))

    result = [int(0)] * 0
    nw0_ = [int(0)] * len(scores)
    result = nw0_
    d_1_i_ = int(0)
    d_1_i_ = 0
    while d_1_i_ < len(scores):
        Invariant(Acc(list_pred(scores)))
        Invariant(Acc(list_pred(guesses)))
        Invariant(Acc(list_pred(result)))
        Invariant(0 <= d_1_i_ and d_1_i_ <= len(scores))
        Invariant(len(result) == len(scores))
        Invariant(len(scores) == len(guesses))
        Invariant(Forall(int, lambda k:Implies( (0 <= k and k < d_1_i_) , (result[k] == abs(scores[k] - guesses[k])))))
        Invariant(Forall(int, lambda k:Implies( (0 <= k and k < len(scores)) , (scores[k] == Old(scores[k])))))
        Invariant(Forall(int, lambda k:Implies( (0 <= k and k < len(guesses)) , (guesses[k] == Old(guesses[k])))))
        result[d_1_i_] = abs(scores[d_1_i_] - guesses[d_1_i_])
        d_1_i_ = d_1_i_ + 1
    return result

Next, we run verifier on this program. Using the following verdict, you should possibly modify this program.
    """
    )

    _, prompt = NaginiRewriterFixing(NaginiRewriter()).rewrite(code)
    assert prompt == error


def test_nagini_rewriter4():
    code = dedent(
        """\
from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *

def Compare(scores: List[int], guesses: List[int]) -> List[int]:
    Requires(Acc(list_pred(guesses)))
    Requires(Acc(list_pred(scores)))
    Requires(len(scores) == len(guesses))
    Ensures(Acc(list_pred(guesses)))
    Ensures(Acc(list_pred(scores)))
    Ensures(Acc(list_pred(Result())))
    Ensures(len(Result()) == len(scores))
    Ensures(len(scores) == len(guesses))
    Ensures(Forall(int, lambda d_0_i_:
    not (0 <= d_0_i_ and d_0_i_ < len(Result())) or (Result()[d_0_i_] == abs(scores[d_0_i_] - guesses[d_0_i_]))))

    result = [int(0)] * 0
    nw0_ = [int(0)] * len(scores)
    result = nw0_
    d_1_i_ = int(0)
    d_1_i_ = 0
    while d_1_i_ < len(scores):
        Invariant(Acc(list_pred(scores)))
        Invariant(Acc(list_pred(guesses)))
        Invariant(Acc(list_pred(result)))
        Invariant(0 <= d_1_i_ and d_1_i_ <= len(scores))
        Invariant(len(result) == len(scores))
        Invariant(len(scores) == len(guesses))
        Invariant(Forall(int, lambda k:Implies( (0 <= k and k < d_1_i_) , (result[k] == abs(scores[k] - guesses[k])))))
        Invariant(Forall(int, lambda k:Implies( (0 <= k and k < len(scores)) , (scores[k] == Old(scores[k])))))
        Invariant(Forall(int, lambda k:Implies( (0 <= k and k < len(guesses)) , (guesses[k] == Old(guesses[k])))))
        result[d_1_i_] = abs(scores[d_1_i_] - guesses[d_1_i_])
        d_1_i_ = d_1_i_ + 1
    return result
    """
    )

    error = ""

    _, prompt = NaginiRewriterFixing(NaginiRewriter()).rewrite(code)
    assert prompt == error


def test_nagini_rewriter5():
    code = dedent(
        """\
from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *

def Compare(scores: List[int], guesses: List[int]) -> List[int]:
    result = [int(0)] * 0
    nw0_ = [int(0)] * len(scores)
    result = nw0_
    d_1_i_ = int(0)
    d_1_i_ = 0
    while d_1_i_ < len(scores):
        Invariant(0 <= d_1_i_ <= len(scores))
        result[d_1_i_] = abs(scores[d_1_i_] - guesses[d_1_i_])
        d_1_i_ = d_1_i_ + 1
    return result
    """
    )

    error = dedent(
        """\
We replaced all double (triple and so on) inequalities with their equivalents (as they are prohibited) and got the following program:
from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *

def Compare(scores: List[int], guesses: List[int]) -> List[int]:
    result = [int(0)] * 0
    nw0_ = [int(0)] * len(scores)
    result = nw0_
    d_1_i_ = int(0)
    d_1_i_ = 0
    while d_1_i_ < len(scores):
        Invariant(0 <= d_1_i_ and d_1_i_ <= len(scores))
        result[d_1_i_] = abs(scores[d_1_i_] - guesses[d_1_i_])
        d_1_i_ = d_1_i_ + 1
    return result
Next, we run verifier on this program. Using the following verdict, you should possibly modify this program.
    """
    )

    _, prompt = NaginiRewriterFixingAST(NaginiRewriterFixing(NaginiRewriter())).rewrite(
        code
    )
    assert prompt == error


def test_rewriter6():
    code = dedent(
        """\
        Invariant(0 <= k and k < d_1_i_ ==> s[k] != s[len(s) - 1 - k] ==> c > smallest__change__fun(s, 0, k))
        """
    )

    prg, prompt = NaginiRewriterFixing(NaginiRewriter()).rewrite(code)

    assert prompt != ""
    assert prg == dedent(
        """\
        Invariant(Implies(0 <= k and k < d_1_i_ ,Implies( s[k] != s[len(s) - 1 - k] , c > smallest__change__fun(s, 0, k))))
        """
    )


def test_rewriter7():
    code = dedent(
        """\
        Invariant(Forall(int, lambda i: Forall(int, lambda j: Implies(0 <= i and i < j and j < len(result), result[i] < result[j]))))
        """
    )

    prg, prompt = NaginiRewriterFixingAST(
        NaginiRewriterFixing(NaginiRewriter())
    ).rewrite(code)

    assert prompt == ""
    assert prg == dedent(
        """\
        Invariant(Forall(int, lambda i: Forall(int, lambda j: Implies(0 <= i and i < j and j < len(result), result[i] < result[j]))))
        """
    )


def test_rewrite_error():
    error = dedent(
        """\
Errors:
The precondition of function count_chars_inter might not hold. Assertion Forall(int, (lambda d_0_i_: ((not ((0 <= d_0_i_) and (d_0_i_ < len(s)))) or ((97 <= s[d_0_i_]) and (s[d_0_i_] <= 122))))) might not hold. (016-count_distinct_characters.2.py@43.23--43.51)
Verification took 9.10 seconds.
"""
    )

    code = dedent(
        """\
from typing import cast, List, Dict, Set, Optional, Union, Tuple
from nagini_contracts.contracts import *

@Pure
def contains_char(s : List[int], c : int, i : int, j : int) -> bool:
    Requires(Acc(list_pred(s)))
    Requires(Forall(int, lambda d_0_i_:
        not (((0) <= (d_0_i_)) and ((d_0_i_) < (len(s)))) or (((97) <= ((s)[d_0_i_])) and (((s)[d_0_i_]) <= (122)))))
    Requires(0 <= i and i <= j and j <= len(s))
    Requires(((97) <= (c)) and ((c) <= (122)))

    if i == j:
        return False
    else:
        return s[j - 1] == c or contains_char(s, c, i, j - 1)

@Pure
def count_chars_inter(s : List[int], c : int) -> int:
    Requires(Acc(list_pred(s)))
    Requires(Forall(int, lambda d_0_i_:
        not (((0) <= (d_0_i_)) and ((d_0_i_) < (len(s)))) or (((97) <= ((s)[d_0_i_])) and (((s)[d_0_i_]) <= (122)))))
    Requires(((97) <= (c)) and ((c) <= (123)))

    if c == 97:
        return 0
    else:
        return count_chars_inter(s, c - 1) + (1 if contains_char(s, c - 1, 0, len(s)) else 0)

def count_distinct_characters(s : List[int]) -> int:
    Requires(Acc(list_pred(s)))
    Requires(Forall(int, lambda d_1_i_:
        not (((0) <= (d_1_i_)) and ((d_1_i_) < (len(s)))) or (((97) <= ((s)[d_1_i_])) and (((s)[d_1_i_]) <= (122)))))
    Ensures(Acc(list_pred(s)))
    Ensures(Forall(int, lambda d_1_i_:
        not (((0) <= (d_1_i_)) and ((d_1_i_) < (len(s)))) or (((97) <= ((s)[d_1_i_])) and (((s)[d_1_i_]) <= (122)))))
    Ensures((Result()) == count_chars_inter(s, 123))

    c : int = int(0)
    d_2_i_ : int = int(97)
    while (d_2_i_) <= (122):
        Invariant(Acc(list_pred(s)))
        Invariant(97 <= d_2_i_ and d_2_i_ <= 123)
        Invariant(c == count_chars_inter(s, d_2_i_))
        Invariant(Forall(int, lambda i: Implies((0 <= i and i < len(s)), (97 <= s[i] and s[i] <= 122))))
        Invariant(0 <= c and c <= d_2_i_ - 97)
        Invariant(Forall(int, lambda x: Implies((97 <= x and x < d_2_i_), (contains_char(s, x, 0, len(s)) == (count_chars_inter(s, x + 1) > count_chars_inter(s, x))))))
        if contains_char(s, d_2_i_, 0, len(s)):
            c = c + 1
        d_2_i_ = d_2_i_ + 1
    return c
# ==== verifiers ====
def contains_char_valid(s : List[int], c : int, i : int, j : int) -> bool:
    # pre-conditions-start
    Requires(Acc(list_pred(s)))
    Requires(Forall(int, lambda d_0_i_:
        not (((0) <= (d_0_i_)) and ((d_0_i_) < (len(s)))) or (((97) <= ((s)[d_0_i_])) and (((s)[d_0_i_]) <= (122)))))
    Requires(0 <= i and i <= j and j <= len(s))
    Requires(((97) <= (c)) and ((c) <= (122)))
    # pre-conditions-end
    ret = contains_char(s, c, i, j)
    return ret
def count_chars_inter_valid(s : List[int], c : int) -> int:
    # pre-conditions-start
    Requires(Acc(list_pred(s)))
    Requires(Forall(int, lambda d_0_i_:
        not (((0) <= (d_0_i_)) and ((d_0_i_) < (len(s)))) or (((97) <= ((s)[d_0_i_])) and (((s)[d_0_i_]) <= (122)))))
    Requires(((97) <= (c)) and ((c) <= (123)))
    # pre-conditions-end
    ret = count_chars_inter(s, c)
    return ret
def count_distinct_characters_valid(s : List[int]) -> int:
    # pre-conditions-start
    Requires(Acc(list_pred(s)))
    Requires(Forall(int, lambda d_1_i_:
        not (((0) <= (d_1_i_)) and ((d_1_i_) < (len(s)))) or (((97) <= ((s)[d_1_i_])) and (((s)[d_1_i_]) <= (122)))))
    # pre-conditions-end
    # post-conditions-start
    Ensures(Acc(list_pred(s)))
    Ensures(Forall(int, lambda d_1_i_:
        not (((0) <= (d_1_i_)) and ((d_1_i_) < (len(s)))) or (((97) <= ((s)[d_1_i_])) and (((s)[d_1_i_]) <= (122)))))
    Ensures((Result()) == count_chars_inter(s, 123))
    # post-conditions-end
    ret = count_distinct_characters(s)
    return ret
"""
    )

    assert dedent(
        """\
Errors:
The precondition of function count_chars_inter might not hold. Assertion Forall(int, (lambda d_0_i_: ((not ((0 <= d_0_i_) and (d_0_i_ < len(s)))) or ((97 <= s[d_0_i_]) and (s[d_0_i_] <= 122))))) might not hold. (016-count_distinct_characters.2.py@43.23--43.51)
Error occurred on the following line(s)
        Invariant(c == count_chars_inter(s, d_2_i_))
Verification took 9.10 seconds.
"""
    ) == rewrite_error(code, error)


def test_rewrite_error1():
    error = dedent(
        """\
Errors:
The precondition of function len might not hold. There might be insufficient permission. (029-filter_by_prefix.2.py@39.44--39.51)
The precondition of function len might not hold. There might be insufficient permission. (029-filter_by_prefix.2.py@59.20--59.26)
The precondition of function starts__with might not hold. There might be insufficient permission to access list_pred(s). (029-filter_by_prefix.2.py@71.24--71.45)
Verification took 10.88 seconds.
"""
    )

    code = dedent(
        """\
from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *
@Pure
def starts__with(s : List[int], p : List[int], i : int) -> bool :
    Requires(Acc(list_pred(s), 1/2))
    Requires(Acc(list_pred(p), 1/2))
    Requires(i >= 0 and i <= len(p) and i <= len(s))
    Ensures(Implies(len(p) == i and len(s) >= len(p), Result()))
    Ensures(Implies(len(s) < len(p), not Result()))
    return len(s) >= len(p) and Forall(int, lambda x: Implies(x >= i and x < len(p), s[x] == p[x]))

@Pure
def starts__with__fun(s : List[int], p : List[int], i : int) -> bool :
    Requires(Acc(list_pred(s), 1/2))
    Requires(Acc(list_pred(p), 1/2))
    Requires(0 <= i and i <= len(p) and i <= len(s))
    Ensures(Result() == starts__with(s, p, i))
    if (len(p) == i):
        return True
    if (len(s) > i and len(s) >= len(p) and s[i] == p[i]):
        return starts__with(s, p, i + 1)
    return False

def filter__by__prefix(xs : List[List[int]], p : List[int]) -> List[int]:
    Requires(Acc(list_pred(xs)))
    Requires(Acc(list_pred(p)))
    Requires(Forall(xs, lambda x : Acc(list_pred(x))))
    Ensures(Acc(list_pred(p)))
    Ensures(Acc(list_pred(xs)))
    Ensures(Forall(xs, lambda x : Acc(list_pred(x))))
    Ensures(Acc(list_pred(Result())))
    Ensures(Forall(int, lambda d_2_j_:
        Implies(d_2_j_ >= 0 and d_2_j_ < len(Result()), Result()[d_2_j_] >= 0 and Result()[d_2_j_] < len(xs))))
    Ensures(Forall(int, lambda d_0_i_:
        not (((0) <= (d_0_i_)) and ((d_0_i_) < (len(Result())))) or (starts__with(xs[Result()[d_0_i_]], p, 0))))
    filtered : List[int] = []
    d_1_i_ : int = 0
    while (d_1_i_) < (len(xs)):
        Invariant(0 <= d_1_i_ and d_1_i_ <= len(xs))
        Invariant(Acc(list_pred(xs)))
        Invariant(Acc(list_pred(p)))
        Invariant(Forall(xs, lambda x: Acc(list_pred(x), 1/2)))
        Invariant(Acc(list_pred(filtered)))
        Invariant(Forall(int, lambda j: Implies(0 <= j and j < len(filtered), 0 <= filtered[j] and filtered[j] < d_1_i_)))
        Invariant(Forall(int, lambda j: Implies(0 <= j and j < len(filtered), starts__with(xs[filtered[j]], p, 0))))
        Invariant(Forall(int, lambda k: Implies(0 <= k and k < d_1_i_ and starts__with(xs[k], p, 0), k in filtered)))
        if starts__with__fun((xs)[d_1_i_], p, 0):
            filtered = (filtered) + [d_1_i_]
        d_1_i_ = (d_1_i_) + (1)
    return filtered
# ==== verifiers ====
def starts__with_valid(s : List[int], p : List[int], i : int) -> bool :
    # pre-conditions-start
    Requires(Acc(list_pred(s), 1/2))
    Requires(Acc(list_pred(p), 1/2))
    Requires(i >= 0 and i <= len(p) and i <= len(s))
    # pre-conditions-end
    # post-conditions-start
    Ensures(Implies(len(p) == i and len(s) >= len(p), Result()))
    Ensures(Implies(len(s) < len(p), not Result()))
    # post-conditions-end
    ret = starts__with(s, p, i)
    return ret
def starts__with__fun_valid(s : List[int], p : List[int], i : int) -> bool :
    # pre-conditions-start
    Requires(Acc(list_pred(s), 1/2))
    Requires(Acc(list_pred(p), 1/2))
    Requires(0 <= i and i <= len(p) and i <= len(s))
    # pre-conditions-end
    # post-conditions-start
    Ensures(Result() == starts__with(s, p, i))
    # post-conditions-end
    ret = starts__with__fun(s, p, i)
    return ret
def filter__by__prefix_valid(xs : List[List[int]], p : List[int]) -> List[int]:
    # pre-conditions-start
    Requires(Acc(list_pred(xs)))
    Requires(Acc(list_pred(p)))
    Requires(Forall(xs, lambda x : Acc(list_pred(x))))
    # pre-conditions-end
    # post-conditions-start
    Ensures(Acc(list_pred(p)))
    Ensures(Acc(list_pred(xs)))
    Ensures(Forall(xs, lambda x : Acc(list_pred(x))))
    Ensures(Acc(list_pred(Result())))
    Ensures(Forall(int, lambda d_2_j_:
        Implies(d_2_j_ >= 0 and d_2_j_ < len(Result()), Result()[d_2_j_] >= 0 and Result()[d_2_j_] < len(xs))))
    Ensures(Forall(int, lambda d_0_i_:
        not (((0) <= (d_0_i_)) and ((d_0_i_) < (len(Result())))) or (starts__with(xs[Result()[d_0_i_]], p, 0))))
    # post-conditions-end
    ret = filter__by__prefix(xs, p)
    return ret
"""
    )

    assert dedent(
        """\
Errors:
The precondition of function len might not hold. There might be insufficient permission. (029-filter_by_prefix.2.py@39.44--39.51)
Error occurred on the following line(s)
        Invariant(0 <= d_1_i_ and d_1_i_ <= len(xs))
The precondition of function len might not hold. There might be insufficient permission. (029-filter_by_prefix.2.py@59.20--59.26)
Error occurred on the following line(s)
    Ensures(Implies(len(p) == i and len(s) >= len(p), Result()))
The precondition of function starts__with might not hold. There might be insufficient permission to access list_pred(s). (029-filter_by_prefix.2.py@71.24--71.45)
Error occurred on the following line(s)
    Ensures(Result() == starts__with(s, p, i))
Verification took 10.88 seconds.
"""
    ) == rewrite_error(code, error)


def test_rewrite_errors2():
    error = dedent(
        """\
Verification failed
Errors:
The precondition of function len might not hold. There might be insufficient permission. (029-filter_by_prefix.4.py@40.44--40.51)
The precondition of function len might not hold. There might be insufficient permission. (029-filter_by_prefix.4.py@61.20--61.26)
The precondition of function starts__with might not hold. There might be insufficient permission to access list_pred(s). (029-filter_by_prefix.4.py@73.24--73.45)
Verification took 11.41 seconds.
"""
    )

    code = dedent(
        """\

from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *
@Pure
def starts__with(s : List[int], p : List[int], i : int) -> bool :
    Requires(Acc(list_pred(s), 1/2))
    Requires(Acc(list_pred(p), 1/2))
    Requires(i >= 0 and i <= len(p) and i <= len(s))
    Ensures(Implies(len(p) == i and len(s) >= len(p), Result()))
    Ensures(Implies(len(s) < len(p), not Result()))
    return len(s) >= len(p) and Forall(int, lambda x: Implies(x >= i and x < len(p), s[x] == p[x]))

@Pure
def starts__with__fun(s : List[int], p : List[int], i : int) -> bool :
    Requires(Acc(list_pred(s), 1/2))
    Requires(Acc(list_pred(p), 1/2))
    Requires(0 <= i and i <= len(p) and i <= len(s))
    Ensures(Result() == starts__with(s, p, i))
    if (len(p) == i):
        return True
    if (len(s) > i and len(s) >= len(p) and s[i] == p[i]):
        return starts__with(s, p, i + 1)
    return False

def filter__by__prefix(xs : List[List[int]], p : List[int]) -> List[int]:
    Requires(Acc(list_pred(xs)))
    Requires(Acc(list_pred(p)))
    Requires(Forall(xs, lambda x : Acc(list_pred(x))))
    Ensures(Acc(list_pred(p)))
    Ensures(Acc(list_pred(xs)))
    Ensures(Forall(xs, lambda x : Acc(list_pred(x))))
    Ensures(Acc(list_pred(Result())))
    Ensures(Forall(int, lambda d_2_j_:
        Implies(d_2_j_ >= 0 and d_2_j_ < len(Result()), Result()[d_2_j_] >= 0 and Result()[d_2_j_] < len(xs))))
    Ensures(Forall(int, lambda d_0_i_:
        not (((0) <= (d_0_i_)) and ((d_0_i_) < (len(Result())))) or (starts__with(xs[Result()[d_0_i_]], p, 0))))
    filtered : List[int] = []
    d_1_i_ : int = 0
    while (d_1_i_) < (len(xs)):
        Invariant(0 <= d_1_i_ and d_1_i_ <= len(xs))
        Invariant(Acc(list_pred(xs)))
        Invariant(Forall(xs, lambda x : Acc(list_pred(x))))
        Invariant(Acc(list_pred(p)))
        Invariant(Acc(list_pred(filtered)))
        Invariant(Forall(int, lambda j: Implies(0 <= j and j < len(filtered), 0 <= filtered[j] and filtered[j] < d_1_i_)))
        Invariant(Forall(int, lambda j: Implies(0 <= j and j < len(filtered), starts__with(xs[filtered[j]], p, 0))))
        Invariant(Forall(int, lambda k: Implies(0 <= k and k < d_1_i_ and starts__with(xs[k], p, 0), k in filtered)))
        if starts__with__fun((xs)[d_1_i_], p, 0):
            filtered = (filtered) + [d_1_i_]
        d_1_i_ = (d_1_i_) + (1)
    return filtered

# ==== verifiers ====
def starts__with_valid(s : List[int], p : List[int], i : int) -> bool :
    # pre-conditions-start
    Requires(Acc(list_pred(s), 1/2))
    Requires(Acc(list_pred(p), 1/2))
    Requires(i >= 0 and i <= len(p) and i <= len(s))
    # pre-conditions-end
    # post-conditions-start
    Ensures(Implies(len(p) == i and len(s) >= len(p), Result()))
    Ensures(Implies(len(s) < len(p), not Result()))
    # post-conditions-end
    ret = starts__with(s, p, i)
    return ret
def starts__with__fun_valid(s : List[int], p : List[int], i : int) -> bool :
    # pre-conditions-start
    Requires(Acc(list_pred(s), 1/2))
    Requires(Acc(list_pred(p), 1/2))
    Requires(0 <= i and i <= len(p) and i <= len(s))
    # pre-conditions-end
    # post-conditions-start
    Ensures(Result() == starts__with(s, p, i))
    # post-conditions-end
    ret = starts__with__fun(s, p, i)
    return ret
def filter__by__prefix_valid(xs : List[List[int]], p : List[int]) -> List[int]:
    # pre-conditions-start
    Requires(Acc(list_pred(xs)))
    Requires(Acc(list_pred(p)))
    Requires(Forall(xs, lambda x : Acc(list_pred(x))))
    # pre-conditions-end
    # post-conditions-start
    Ensures(Acc(list_pred(p)))
    Ensures(Acc(list_pred(xs)))
    Ensures(Forall(xs, lambda x : Acc(list_pred(x))))
    Ensures(Acc(list_pred(Result())))
    Ensures(Forall(int, lambda d_2_j_:
        Implies(d_2_j_ >= 0 and d_2_j_ < len(Result()), Result()[d_2_j_] >= 0 and Result()[d_2_j_] < len(xs))))
    Ensures(Forall(int, lambda d_0_i_:
        not (((0) <= (d_0_i_)) and ((d_0_i_) < (len(Result())))) or (starts__with(xs[Result()[d_0_i_]], p, 0))))
    # post-conditions-end
    ret = filter__by__prefix(xs, p)
    return ret
"""
    )

    assert dedent(
        """\
Verification failed
Errors:
The precondition of function len might not hold. There might be insufficient permission. (029-filter_by_prefix.4.py@40.44--40.51)
Error occurred on the following line(s)
        Invariant(0 <= d_1_i_ and d_1_i_ <= len(xs))
The precondition of function len might not hold. There might be insufficient permission. (029-filter_by_prefix.4.py@61.20--61.26)
Error occurred on the following line(s)
    Ensures(Implies(len(p) == i and len(s) >= len(p), Result()))
The precondition of function starts__with might not hold. There might be insufficient permission to access list_pred(s). (029-filter_by_prefix.4.py@73.24--73.45)
Error occurred on the following line(s)
    Ensures(Result() == starts__with(s, p, i))
Verification took 11.41 seconds.
"""
    ) == rewrite_error(code, error)
