from textwrap import dedent
from verified_cogen.runners.languages import LanguageDatabase, register_basic_languages

register_basic_languages()


def test_nagini_generate():
    nagini_lang = LanguageDatabase().get("nagini")
    code = dedent(
        """\
        def main(value: int) -> int:
            Requires(value >= 10)
            Ensures(Result() >= 20)
            # impl-start
            Assert(value * 2 >= 20) # assert-line
            return value * 2
            # impl-end"""
    )
    assert nagini_lang.generate_validators(code) == dedent(
        """\
        def main_valid(value: int) -> int:
            Requires(value >= 10)
            Ensures(Result() >= 20)
            ret = main(value)
            return ret"""
    )


def test_nagini_with_comments():
    nagini_lang = LanguageDatabase().get("nagini")
    code = dedent(
        """\
        def main(value: int) -> int:
            # pre-conditions-start
            Requires(value >= 10)
            # pre-conditions-end
            # post-conditions-start
            Ensures(Result() >= 20)
            # post-conditions-end
            # impl-start
            Assert(value * 2 >= 20) # assert-line
            return value * 2
            # impl-end"""
    )
    assert nagini_lang.generate_validators(code) == dedent(
        """\
        def main_valid(value: int) -> int:
            # pre-conditions-start
            Requires(value >= 10)
            # pre-conditions-end
            # post-conditions-start
            Ensures(Result() >= 20)
            # post-conditions-end
            ret = main(value)
            return ret"""
    )


def test_remove_line():
    nagini_lang = LanguageDatabase().get("nagini")
    code = dedent(
        """\
        def main():
            Assert(a == 1) # assert-line
        """
    )
    assert nagini_lang.remove_asserts_and_invariants(code) == dedent(
        """\
        def main():"""
    )


def test_remove_multiline_assert():
    nagini_lang = LanguageDatabase().get("nagini")

    code = dedent(
        """\
        def main():
            # assert-start
            Assert(
                a == 1
            )
            # assert-end"""
    )
    assert nagini_lang.remove_asserts_and_invariants(code) == dedent(
        """\
        def main():"""
    )


def test_remove_invariants():
    nagini_lang = LanguageDatabase().get("nagini")

    code = dedent(
        """\
        def main():
            while True:
                # invariants-start
                Invariant(false)
                Invariant(true)
                # invariants-end"""
    )
    assert nagini_lang.remove_asserts_and_invariants(code) == dedent(
        """\
        def main():
            while True:"""
    )


def test_remove_all():
    nagini_lang = LanguageDatabase().get("nagini")

    code = dedent(
        """\
        def is_prime(k : int) -> bool:
            # pre-conditions-start
            Requires((k) >= (2))
            # pre-conditions-end
            # post-conditions-start
            Ensures(not (Result()) or (Forall(int, lambda d_0_i_:
                not (((2) <= (d_0_i_)) and ((d_0_i_) < (k))) or ((k % d_0_i_) != (0)))))
            Ensures(not (not(Result())) or (Exists(int, lambda d_1_j_:
                (((2) <= (d_1_j_)) and ((d_1_j_) < (k))) and (((k % d_1_j_)) == (0)))))
            # post-conditions-end
            result = False # type : bool
            d_2_i_ = int(0) # type : int
            d_2_i_ = 2
            result = True
            while (d_2_i_) < (k):
                # invariants-start
                Invariant(((2) <= (d_2_i_)) and ((d_2_i_) <= (k)))
                Invariant(not (not(result)) or (Exists(int, lambda d_3_j_:
                    (((2) <= (d_3_j_)) and ((d_3_j_) < (d_2_i_))) and (((k % d_3_j_)) == (0)))))
                Invariant(not (result) or (Forall(int, lambda d_4_j_:
                    not (((2) <= (d_4_j_)) and ((d_4_j_) < (d_2_i_))) or (((k % d_4_j_)) != (0)))))
                # invariants-end
                if ((k % d_2_i_)) == (0):
                    result = False
                Assert((not result) or Forall(int, lambda j : 2 <= j < i ==> k % j != 0)) # assert-line
                # assert-start
                Assert(result
                    or Exists(int,
                        lamdbda j : 2 <= j < i && k % j == 0)
                # assert-end
                d_2_i_ = (d_2_i_) + (1)
            return result"""
    )
    assert nagini_lang.remove_asserts_and_invariants(code) == dedent(
        """\
        def is_prime(k : int) -> bool:
            # pre-conditions-start
            Requires((k) >= (2))
            # pre-conditions-end
            # post-conditions-start
            Ensures(not (Result()) or (Forall(int, lambda d_0_i_:
                not (((2) <= (d_0_i_)) and ((d_0_i_) < (k))) or ((k % d_0_i_) != (0)))))
            Ensures(not (not(Result())) or (Exists(int, lambda d_1_j_:
                (((2) <= (d_1_j_)) and ((d_1_j_) < (k))) and (((k % d_1_j_)) == (0)))))
            # post-conditions-end
            result = False # type : bool
            d_2_i_ = int(0) # type : int
            d_2_i_ = 2
            result = True
            while (d_2_i_) < (k):
                if ((k % d_2_i_)) == (0):
                    result = False
                d_2_i_ = (d_2_i_) + (1)
            return result"""
    )


def test_nagini_large():
    nagini_lang = LanguageDatabase().get("nagini")

    code = dedent(
        """\
        from typing import cast, List, Dict, Set, Optional, Union
        from nagini_contracts.contracts import *

        @Pure
        def lower(c : int) -> bool :
            # impl-start
            return ((0) <= (c)) and ((c) <= (25))
            # impl-end

        @Pure
        def upper(c : int) -> bool :
            # impl-start
            return ((26) <= (c)) and ((c) <= (51))
            # impl-end

        @Pure
        def alpha(c : int) -> bool :
            # impl-start
            return (lower(c)) or (upper(c))
            # impl-end

        @Pure
        def flip__char(c : int) -> int :
            # pre-conditions-start
            Ensures(lower(c) == upper(Result()))
            Ensures(upper(c) == lower(Result()))
            # pre-conditions-end

            # impl-start
            if lower(c):
                return ((c) - (0)) + (26)
            elif upper(c):
                return ((c) + (0)) - (26)
            elif True:
                return c
            # impl-end

        def flip__case(s : List[int]) -> List[int] :
            # pre-conditions-start
            Requires(Acc(list_pred(s)))
            # pre-conditions-end
            # post-conditions-start
            Ensures(Acc(list_pred(s)))
            Ensures(Acc(list_pred(Result())))
            Ensures((len(Result())) == (len(s)))
            Ensures(Forall(int, lambda d_0_i_: (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(s))), lower((s)[d_0_i_]) == upper((Result())[d_0_i_])))))
            Ensures(Forall(int, lambda d_0_i_: (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(s))), upper((s)[d_0_i_]) == lower((Result())[d_0_i_])))))
            # post-conditions-end

            # impl-start
            res = list([int(0)] * len(s)) # type : List[int]
            i = int(0) # type : int
            while i < len(s):
                # invariants-start
                Invariant(Acc(list_pred(s)))
                Invariant(Acc(list_pred(res)))
                Invariant(((0) <= (i)) and ((i) <= (len(s))))
                Invariant((len(res)) == (len(s)))
                Invariant(Forall(int, lambda d_0_i_: (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (i)), lower((s)[d_0_i_]) == upper((res)[d_0_i_])))))
                Invariant(Forall(int, lambda d_0_i_: (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (i)), upper((s)[d_0_i_]) == lower((res)[d_0_i_])))))
                # invariants-end
                res[i] = flip__char(s[i])
                i = i + 1
            return res
            # impl-end"""
    )
    # print(nagini_lang.generate_validators(code))
    assert nagini_lang.generate_validators(code) == dedent(
        """\
        def lower_valid(c : int) -> bool :
            ret = lower(c)
            return ret
        def upper_valid(c : int) -> bool :
            ret = upper(c)
            return ret
        def alpha_valid(c : int) -> bool :
            ret = alpha(c)
            return ret
        def flip__char_valid(c : int) -> int :
            # pre-conditions-start
            Ensures(lower(c) == upper(Result()))
            Ensures(upper(c) == lower(Result()))
            # pre-conditions-end
            ret = flip__char(c)
            return ret
        def flip__case_valid(s : List[int]) -> List[int] :
            # pre-conditions-start
            Requires(Acc(list_pred(s)))
            # pre-conditions-end
            # post-conditions-start
            Ensures(Acc(list_pred(s)))
            Ensures(Acc(list_pred(Result())))
            Ensures((len(Result())) == (len(s)))
            Ensures(Forall(int, lambda d_0_i_: (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(s))), lower((s)[d_0_i_]) == upper((Result())[d_0_i_])))))
            Ensures(Forall(int, lambda d_0_i_: (Implies(((0) <= (d_0_i_)) and ((d_0_i_) < (len(s))), upper((s)[d_0_i_]) == lower((Result())[d_0_i_])))))
            # post-conditions-end
            ret = flip__case(s)
            return ret"""
    )


def test_nagini_small():
    nagini_lang = LanguageDatabase().get("nagini")

    code = dedent(
        """\
        @Pure
        def flip__char(c : int) -> int :
            # pre-conditions-start
            Ensures(lower(c) == upper(Result()))
            Ensures(upper(c) == lower(Result()))
            # pre-conditions-end

            # impl-start
            if lower(c):
                return ((c) - (0)) + (26)
            elif upper(c):
                return ((c) + (0)) - (26)
            elif True:
                return c
            # impl-end"""
    )
    assert nagini_lang.generate_validators(code) == dedent(
        """\
        def flip__char_valid(c : int) -> int :
            # pre-conditions-start
            Ensures(lower(c) == upper(Result()))
            Ensures(upper(c) == lower(Result()))
            # pre-conditions-end
            ret = flip__char(c)
            return ret"""
    )
