from textwrap import dedent
from verified_cogen.runners.languages import LanguageDatabase, register_basic_languages

register_basic_languages()


def test_dafny_generate():
    dafny_lang = LanguageDatabase().get("dafny")
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
    assert dafny_lang.generate_validators(code) == dedent(
        """\
        method main_valid(value: int) returns (result: int)
            requires value >= 10
            ensures result >= 20
        { var ret := main(value); return ret; }
        """
    )


def test_remove_line():
    dafny_lang = LanguageDatabase().get("dafny")
    code = dedent(
        """\
        method main() {
            assert a == 1; // assert-line
        }"""
    )
    assert dafny_lang.remove_asserts_and_invariants(code) == dedent(
        """\
        method main() {
        }"""
    )


def test_remove_multiline_assert():
    dafny_lang = LanguageDatabase().get("dafny")

    code = dedent(
        """\
        method main() {
            // assert-start
            assert a == 1 by {

            }
            // assert-end
        }"""
    )
    assert dafny_lang.remove_asserts_and_invariants(code) == dedent(
        """\
        method main() {
        }"""
    )


def test_remove_invariants():
    dafny_lang = LanguageDatabase().get("dafny")

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
    assert dafny_lang.remove_asserts_and_invariants(code) == dedent(
        """\
        method main() {
            while true
            {
            }
        }"""
    )


def test_remove_all():
    dafny_lang = LanguageDatabase().get("dafny")

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
    assert dafny_lang.remove_asserts_and_invariants(code) == dedent(
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
