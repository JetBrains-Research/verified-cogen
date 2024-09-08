from textwrap import dedent
from verified_cogen.runners.languages import LanguageDatabase, init_basic_languages

init_basic_languages()


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
