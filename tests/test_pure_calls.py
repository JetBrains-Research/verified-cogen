from textwrap import dedent

import pytest

from verified_cogen.runners.languages import (
    AnnotationType,
    LanguageDatabase,
    register_basic_languages,
)
from verified_cogen.tools.pureCallsDetectors import detect_and_replace_pure_calls_nagini


@pytest.fixture()
def language_database():
    LanguageDatabase().reset()
    register_basic_languages(
        with_removed=[
            AnnotationType.INVARIANTS,
            AnnotationType.ASSERTS,
            AnnotationType.IMPLS,
        ]
    )
    return LanguageDatabase()


def test_simple():
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

    result = [0] * n
    i = 0
    while sum__spec(i - 1) < n:
        Invariant(Acc(list_pred(result)))
        Invariant(0 <= i and i <= n)
        Invariant(len(result) == n)
        Invariant(sum__spec(i - 1) >= 0)
        Invariant(Forall(int, lambda j: Implies(0 <= j and j < i, result[j] == (factorial__spec(j - 1) if j % 2 == 0 else sum__spec(j - 1)))))
        Invariant(Forall(int, lambda j: Implies(i <= j and j < n, result[j] == 0)))
        if i % 2 == 0:
            result[i] = factorial__spec(i - 1)
        else:
            result[i] = sum__spec(i - 1)
        i += 1
    return result
"""
    )

    calls, new_code = detect_and_replace_pure_calls_nagini(code, [])

    assert calls == ["factorial__spec", "sum__spec"]
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
    result = [0] * n
    i = 0
    while sum__spec(i - 1) < n:
        Invariant(Acc(list_pred(result)))
        Invariant(0 <= i and i <= n)
        Invariant(len(result) == n)
        Invariant(sum__spec(i - 1) >= 0)
        Invariant(Forall(int, lambda j: Implies(0 <= j and j < i, result[j] == (factorial__spec(j - 1) if j % 2 == 0 else sum__spec(j - 1)))))
        Invariant(Forall(int, lambda j: Implies(i <= j and j < n, result[j] == 0)))
        if i % 2 == 0:
            result[i] = invalid_call()
        else:
            result[i] = invalid_call()
        i += 1
    return result"""
    )

    assert new_code == compare_code


def test_simple1():
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

    result = [0] * n
    i = 0
    while sum__spec(i - 1) < n:
        Invariant(Acc(list_pred(result)))
        Invariant(0 <= i and i <= n)
        Invariant(len(result) == n)
        Invariant(sum__spec(i - 1) >= 0)
        Invariant(Forall(int, lambda j: Implies(0 <= j and j < i, result[j] == (factorial__spec(j - 1) if j % 2 == 0 else sum__spec(j - 1)))))
        Invariant(Forall(int, lambda j: Implies(i <= j and j < n, result[j] == 0)))
        if i % 2 == 0:
            result[i] = factorial__spec(i - 1)
        else:
            result[i] = sum__spec(i - 1)
        i += 1
    return result
"""
    )

    calls, new_code = detect_and_replace_pure_calls_nagini(code, ["sum__spec"])

    assert calls == ["factorial__spec"]
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
    result = [0] * n
    i = 0
    while sum__spec(i - 1) < n:
        Invariant(Acc(list_pred(result)))
        Invariant(0 <= i and i <= n)
        Invariant(len(result) == n)
        Invariant(sum__spec(i - 1) >= 0)
        Invariant(Forall(int, lambda j: Implies(0 <= j and j < i, result[j] == (factorial__spec(j - 1) if j % 2 == 0 else sum__spec(j - 1)))))
        Invariant(Forall(int, lambda j: Implies(i <= j and j < n, result[j] == 0)))
        if i % 2 == 0:
            result[i] = invalid_call()
        else:
            result[i] = sum__spec(i - 1)
        i += 1
    return result"""
    )

    assert new_code == compare_code


def test_find_pure_non_helpers(language_database: LanguageDatabase):
    code = dedent(
        """\
from typing import cast, List, Dict, Set, Optional, Union
from nagini_contracts.contracts import *

#use-as-unpure
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

    result = [0] * n
    i = 0
    while sum__spec(i - 1) < n:
        Invariant(Acc(list_pred(result)))
        Invariant(0 <= i and i <= n)
        Invariant(len(result) == n)
        Invariant(sum__spec(i - 1) >= 0)
        Invariant(Forall(int, lambda j: Implies(0 <= j and j < i, result[j] == (factorial__spec(j - 1) if j % 2 == 0 else sum__spec(j - 1)))))
        Invariant(Forall(int, lambda j: Implies(i <= j and j < n, result[j] == 0)))
        if i % 2 == 0:
            result[i] = factorial__spec(i - 1)
        else:
            result[i] = sum__spec(i - 1)
        i += 1
    return result"""
    )

    nagini_lang = language_database.get("nagini")

    result: list[str] = ["factorial__spec"]

    assert nagini_lang.find_pure_non_helpers(code) == result
