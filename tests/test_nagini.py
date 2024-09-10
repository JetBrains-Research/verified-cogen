import re
from textwrap import dedent
from verified_cogen.runners.languages import LanguageDatabase, init_basic_languages

init_basic_languages()


def test_nagini_generate():
    nagini_lang = LanguageDatabase().get("nagini")
    code = dedent(
        """\
        def main(value: int) -> int:
            Requires(value >= 10)
            Ensures(Result() >= 20)
            Assert(value * 2 >= 20) # assert-line
            return value * 2"""
    )
    assert nagini_lang.generate_validators(code) == dedent(
        """\
        def main_valid(value: int) -> int:
            Requires(value >= 10)
            Ensures(Result() >= 20)
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
