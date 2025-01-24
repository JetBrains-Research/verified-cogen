from textwrap import dedent
from verified_cogen.runners.languages import LanguageDatabase, register_basic_languages
from verified_cogen.runners.languages.language import AnnotationType

import pytest


@pytest.fixture()
def language_database():
    LanguageDatabase().reset()
    register_basic_languages(
        with_removed=[
            AnnotationType.INVARIANTS,
            AnnotationType.ASSERTS,
        ]
    )
    return LanguageDatabase()


def test_dafny_generate(language_database: LanguageDatabase):
    dafny_lang = language_database.get("dafny")
    code = dedent(
        """\
        method main(value: int) returns (result: int)
            requires value >= 10
            ensures result >= 20
        {
            assert value * 2 >= 20; // assert-line
            result := value * 2;
        }"""
    )
    assert dafny_lang.generate_validators(code, True) == dedent(
        """\
        method main_valid(value: int) returns (result: int)
            requires value >= 10
            ensures result >= 20
        { var ret0 := main(value); return ret0; }
        """
    )


def test_dafny_generate_with_helper(language_database: LanguageDatabase):
    dafny_lang = language_database.get("dafny")
    code = dedent(
        """\
        function abs(n: int) : nat { if n > 0 then n else -n }

        method main(value: int) returns (result: int)
            requires value >= 10
            ensures result >= 20
        {
            assert value * 2 >= 20; // assert-line
            result := value * 2;
        }"""
    )
    assert dafny_lang.generate_validators(code, True) == dedent(
        """\
        function abs_valid_pure(n: int): nat { abs(n) }

        method main_valid(value: int) returns (result: int)
            requires value >= 10
            ensures result >= 20
        { var ret0 := main(value); return ret0; }
        """
    )


def test_dafny_generate_multiple_returns(language_database: LanguageDatabase):
    dafny_lang = language_database.get("dafny")
    code = dedent(
        """\
        method main(value: int) returns (result: int, result2: int)
            requires value >= 10
            ensures result >= 20
            ensures result2 >= 30
        {
            assert value * 2 >= 20; // assert-line
            result := value * 2;
            result2 := value * 3;
        }"""
    )
    assert dafny_lang.generate_validators(code, True) == dedent(
        """\
        method main_valid(value: int) returns (result: int, result2: int)
            requires value >= 10
            ensures result >= 20
            ensures result2 >= 30
        { var ret0, ret1 := main(value); return ret0, ret1; }
        """
    )


def test_remove_line(language_database: LanguageDatabase):
    dafny_lang = language_database.get("dafny")
    code = dedent(
        """\
        method main() {
            assert a == 1; // assert-line
        }"""
    )
    assert dafny_lang.remove_conditions(code) == dedent(
        """\
        method main() {
        }"""
    )


def test_remove_multiline_assert(language_database: LanguageDatabase):
    dafny_lang = language_database.get("dafny")

    code = dedent(
        """\
        method main() {
            // assert-start
            assert a == 1 by {

            }
            // assert-end
        }"""
    )
    assert dafny_lang.remove_conditions(code) == dedent(
        """\
        method main() {
        }"""
    )


def test_remove_invariants(language_database: LanguageDatabase):
    dafny_lang = language_database.get("dafny")

    code = dedent(
        """\
        method main() {
            while true
                // invariants-start
                invariant false
                invariant true
                // invariants-end
            {
            }
        }"""
    )
    assert dafny_lang.remove_conditions(code) == dedent(
        """\
        method main() {
            while true
            {
            }
        }"""
    )


def test_remove_all(language_database: LanguageDatabase):
    dafny_lang = language_database.get("dafny")

    code = dedent(
        """\
        method is_prime(k: int) returns (result: bool)
          requires k >= 2
          ensures result ==> forall i :: 2 <= i < k ==> k % i != 0
          ensures !result ==> exists j :: 2 <= j < k && k % j == 0
        {
          var i := 2;
          result := true;
          while i < k
            // invariants-start
            invariant 2 <= i <= k
            invariant !result ==> exists j :: 2 <= j < i && k % j == 0
            invariant result ==> forall j :: 2 <= j < i ==> k % j != 0
            // invariants-end
          {
            if k % i == 0 {
              result := false;
            }
            assert result ==> forall j :: 2 <= j < i ==> k % j != 0; // assert-line
            // assert-start
            assert !result ==> exists j :: 2 <= j < i && k % j == 0 by {
                assert true;
            }
            // assert-end
            i := i + 1;
          }
        }"""
    )
    assert dafny_lang.remove_conditions(code) == dedent(
        """\
        method is_prime(k: int) returns (result: bool)
          requires k >= 2
          ensures result ==> forall i :: 2 <= i < k ==> k % i != 0
          ensures !result ==> exists j :: 2 <= j < k && k % j == 0
        {
          var i := 2;
          result := true;
          while i < k
          {
            if k % i == 0 {
              result := false;
            }
            i := i + 1;
          }
        }"""
    )
