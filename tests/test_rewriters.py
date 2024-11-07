from textwrap import dedent

from verified_cogen.runners.rewriters.nagini_rewriter import NaginiRewriter
from verified_cogen.runners.rewriters.nagini_rewriter_fixing import NaginiRewriterFixing
from verified_cogen.runners.rewriters.nagini_rewriter_fixing_ast import NaginiRewriterFixingAST


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

    prg, prompt = NaginiRewriter().rewrite(code)
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

    prg, prompt = NaginiRewriterFixing(NaginiRewriter()).rewrite(code)
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

    prg, prompt = NaginiRewriterFixing(NaginiRewriter()).rewrite(code)
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

    prg, prompt = NaginiRewriterFixingAST(NaginiRewriterFixing(NaginiRewriter())).rewrite(code)
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

    prg, prompt = NaginiRewriterFixingAST(NaginiRewriterFixing(NaginiRewriter())).rewrite(code)

    assert prompt == ""
    assert prg == dedent(
        """\
        Invariant(Forall(int, lambda i: Forall(int, lambda j: Implies(0 <= i and i < j and j < len(result), result[i] < result[j]))))
        """
    )