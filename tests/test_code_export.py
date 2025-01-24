from textwrap import dedent

from verified_cogen.tools import extract_code_from_llm_output


def test_extract_code():
    code = dedent(
        """\
        ```rust
        fn main() {

        }
        ```"""
    )
    assert extract_code_from_llm_output(code) == dedent(
        """\
        fn main() {

        }"""
    )


def test_extract_code_no_block():
    code = dedent(
        """\
        fn main() {

        }"""
    )
    assert extract_code_from_llm_output(code) == dedent(
        """\
        fn main() {

        }"""
    )
