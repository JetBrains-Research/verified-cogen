from textwrap import dedent
from verified_cogen.runners.languages import LanguageDatabase, register_basic_languages
from verified_cogen.runners.languages.language import AnnotationType

register_basic_languages(
    with_removed=[
        AnnotationType.INVARIANTS,
        AnnotationType.ASSERTS,
    ]
)


def test_verus_generate():
    verus_lang = LanguageDatabase().get("verus")
    code = dedent(
        """\
        fn main(value: i32) -> (result: i32)
            requires
                value >= 10,
            ensures
                result >= 20,
        {
            assert(value * 2 >= 20); // assert-line
            value * 2
        }

        spec fn test(val: i32) -> (result: i32) 
        {
            val
        }

        fn is_prime(num: u32) -> (result: bool)
            requires
                num >= 2,
            ensures
                result <==> spec_prime(num as int),
        {
            let mut i = 2;
            let mut result = true;
            while i < num
                // invariants-start
                invariant
                    2 <= i <= num,
                    result <==> spec_prime_helper(num as int, i as int),
                // invariants-end
            {
                if num % i == 0 {
                    result = false;
                    assert(result <==> spec_prime_helper(num as int, i as int)); // assert-line
                }
                // assert-start
                assert(result <==> spec_prime_helper(num as int, i as int)) by {
                    assert(true);
                }
                // assert-end
                i += 1;
            }
            result
        }"""
    )
    assert verus_lang.generate_validators(code, True) == dedent(
        """\
        verus!{
        spec fn test_valid_pure(val: i32) -> (result: i32) 
        { let ret = test(val); ret }
        
        fn main_valid(value: i32) -> (result: i32)
            requires
                value >= 10,
            ensures
                result >= 20,
        { let ret = main(value); ret }

        fn is_prime_valid(num: u32) -> (result: bool)
            requires
                num >= 2,
            ensures
                result <==> spec_prime(num as int),
        { let ret = is_prime(num); ret }
        }"""
    )


def test_remove_line():
    verus_lang = LanguageDatabase().get("verus")
    code = dedent(
        """\
        fn main() {
            assert a == 1; // assert-line
        }"""
    )
    assert verus_lang.remove_conditions(code) == dedent(
        """\
        fn main() {
        }"""
    )


def test_remove_multiline_assert():
    verus_lang = LanguageDatabase().get("verus")

    code = dedent(
        """\
        fn main() {
            // assert-start
            assert a == 1 by {

            }
            // assert-end
        }"""
    )
    assert verus_lang.remove_conditions(code) == dedent(
        """\
        fn main() {
        }"""
    )


def test_remove_invariants():
    verus_lang = LanguageDatabase().get("verus")

    code = dedent(
        """\
        fn main() {
            while true
                // invariants-start
                invariant false
                invariant true
                // invariants-end
            {
            }
        }"""
    )
    assert verus_lang.remove_conditions(code) == dedent(
        """\
        fn main() {
            while true
            {
            }
        }"""
    )


def test_remove_all():
    verus_lang = LanguageDatabase().get("verus")

    code = dedent(
        """\
        fn is_prime(num: u32) -> (result: bool)
            requires
                num >= 2,
            ensures
                result <==> spec_prime(num as int),
        {
            let mut i = 2;
            let mut result = true;
            while i < num
                // invariants-start
                invariant
                    2 <= i <= num,
                    result <==> spec_prime_helper(num as int, i as int),
                // invariants-end
            {
                if num % i == 0 {
                    result = false;
                    assert(result <==> spec_prime_helper(num as int, i as int)); // assert-line
                }
                // assert-start
                assert(result <==> spec_prime_helper(num as int, i as int)) by {
                    assert(true);
                }
                // assert-end
                i += 1;
            }
            result
        }"""
    )
    assert verus_lang.remove_conditions(code) == dedent(
        """\
        fn is_prime(num: u32) -> (result: bool)
            requires
                num >= 2,
            ensures
                result <==> spec_prime(num as int),
        {
            let mut i = 2;
            let mut result = true;
            while i < num
            {
                if num % i == 0 {
                    result = false;
                }
                i += 1;
            }
            result
        }"""
    )
