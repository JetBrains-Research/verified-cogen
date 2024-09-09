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
            Assert(value * 2 >= 20) // assert-line
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
