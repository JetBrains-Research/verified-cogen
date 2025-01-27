from textwrap import dedent

import pytest

from verified_cogen.runners.languages import LanguageDatabase, register_basic_languages
from verified_cogen.runners.languages.language import AnnotationType


@pytest.fixture()
def language_database():
    LanguageDatabase().reset()
    register_basic_languages(
        with_removed=[
            AnnotationType.INVARIANTS,
            AnnotationType.ASSERTS,
            AnnotationType.IMPLS,
            AnnotationType.PRE_CONDITIONS,
            AnnotationType.POST_CONDITIONS,
        ]
    )
    return LanguageDatabase()


def test_verus_wo_prepost_validators(language_database: LanguageDatabase):
    verus_lang = language_database.get("verus")
    code = dedent(
        """\
use vstd::assert_seqs_equal;
use vstd::prelude::*;

verus! {
spec fn intersperse_spec(numbers: Seq<u64>, delimiter: u64) -> (result:Seq<u64>)
    decreases numbers.len(),
{
    if numbers.len() <= 1 {
        numbers
    } else {
        intersperse_spec(numbers.drop_last(), delimiter) + seq![delimiter, numbers.last()]
    }
}
// pure-end

spec fn even(i: int) -> (result:int) {
    2 * i
}
// pure-end

spec fn odd(i: int) -> (result:int) {
    2 * i + 1
}
// pure-end

spec fn intersperse_quantified(numbers: Seq<u64>, delimiter: u64, interspersed: Seq<u64>) -> (result:bool) {
    (if numbers.len() == 0 {
        interspersed.len() == 0
    } else {
        interspersed.len() == 2 * numbers.len() - 1
    }) && (forall|i: int| 0 <= i < numbers.len() ==> #[trigger] interspersed[even(i)] == numbers[i])
        && (forall|i: int|
        0 <= i < numbers.len() - 1 ==> #[trigger] interspersed[odd(i)] == delimiter)
}
// pure-end

proof fn intersperse_spec_len(numbers: Seq<u64>, delimiter: u64)
    // post-conditions-start
    ensures
        numbers.len() > 0 ==> intersperse_spec(numbers, delimiter).len() == 2 * numbers.len() - 1,
    decreases numbers.len(),
    // post-conditions-end
{
    // impl-start
    if numbers.len() > 0 {
        intersperse_spec_len(numbers.drop_last(), delimiter);
    }
    // impl-end
}
// pure-end

proof fn intersperse_quantified_is_spec(numbers: Seq<u64>, delimiter: u64, interspersed: Seq<u64>)
    // pre-conditions-start
    requires
        intersperse_quantified(numbers, delimiter, interspersed),
    // pre-conditions-end
    // post-conditions-start
    ensures
        interspersed == intersperse_spec(numbers, delimiter),
    decreases numbers.len(),
    // post-conditions-end
{
    // impl-start
    let is = intersperse_spec(numbers, delimiter);
    if numbers.len() == 0 {
    } else if numbers.len() == 1 {
        assert(interspersed.len() == 1); // assert-line
        assert(interspersed[even(0)] == numbers[0]); // assert-line
    } else {
        intersperse_quantified_is_spec(
            numbers.drop_last(),
            delimiter,
            interspersed.take(interspersed.len() - 2),
        );
        intersperse_spec_len(numbers, delimiter);
        // assert-start
        assert_seqs_equal!(is == interspersed, i => {
            if i < is.len() - 2 {
            } else {
                if i % 2 == 0 {
                    assert(is[i] == numbers.last());
                    assert(interspersed[even(i/2)] == numbers[i / 2]);
                    assert(i / 2 == numbers.len() - 1);
                } else {
                    assert(is[i] == delimiter);
                    assert(interspersed[odd((i-1)/2)] == delimiter);
                }
            }
        });
        // assert-end
    }
    assert(interspersed =~= intersperse_spec(numbers, delimiter)); // assert-line
    // impl-end
}
// pure-end

fn intersperse(numbers: Vec<u64>, delimiter: u64) -> (result: Vec<u64>)
    // post-conditions-start
    ensures
        result@ == intersperse_spec(numbers@, delimiter),
    // post-conditions-end
{
    // impl-start
    if numbers.len() <= 1 {
        numbers
    } else {
        let mut result = Vec::new();
        let mut index = 0;
        while index < numbers.len() - 1
            // invariants-start
            invariant
                numbers.len() > 1,
                0 <= index < numbers.len(),
                result.len() == 2 * index,
                forall|i: int| 0 <= i < index ==> #[trigger] result[even(i)] == numbers[i],
                forall|i: int| 0 <= i < index ==> #[trigger] result[odd(i)] == delimiter,
            // invariants-end
        {
            result.push(numbers[index]);
            result.push(delimiter);
            index += 1;
        }
        result.push(numbers[numbers.len() - 1]);
        // assert-start
        proof {
            intersperse_quantified_is_spec(numbers@, delimiter, result@);
        }
        // assert-end
        result
    }
    // impl-end
}

} // verus!"""
    )
    assert verus_lang.generate_validators(code, True) == dedent(
        """\
        verus!{
        spec fn intersperse_spec_valid_pure(numbers: Seq<u64>, delimiter: u64) -> (result:Seq<u64>)
            decreases numbers.len(),
        { let ret = intersperse_spec(numbers, delimiter); ret }

        spec fn even_valid_pure(i: int) -> (result:int) { let ret = even(i); ret }

        spec fn odd_valid_pure(i: int) -> (result:int) { let ret = odd(i); ret }

        spec fn intersperse_quantified_valid_pure(numbers: Seq<u64>, delimiter: u64, interspersed: Seq<u64>) -> (result:bool) { let ret = intersperse_quantified(numbers, delimiter, interspersed); ret }

        fn intersperse_valid(numbers: Vec<u64>, delimiter: u64) -> (result: Vec<u64>)
            // post-conditions-start
            ensures
                result@ == intersperse_spec(numbers@, delimiter),
            // post-conditions-end
        { let ret = intersperse(numbers, delimiter); ret }
        }"""
    )


def test_verus_wo_prepost_remove(language_database: LanguageDatabase):
    verus_lang = language_database.get("verus")
    code = dedent(
        """\
use vstd::assert_seqs_equal;
use vstd::prelude::*;

verus! {
spec fn intersperse_spec(numbers: Seq<u64>, delimiter: u64) -> (result:Seq<u64>)
    decreases numbers.len(),
{
    if numbers.len() <= 1 {
        numbers
    } else {
        intersperse_spec(numbers.drop_last(), delimiter) + seq![delimiter, numbers.last()]
    }
}
spec fn even(i: int) -> (result:int) {
    2 * i
}

spec fn odd(i: int) -> (result:int) {
    2 * i + 1
}
spec fn intersperse_quantified(numbers: Seq<u64>, delimiter: u64, interspersed: Seq<u64>) -> (result:bool) {
    (if numbers.len() == 0 {
        interspersed.len() == 0
    } else {
        interspersed.len() == 2 * numbers.len() - 1
    }) && (forall|i: int| 0 <= i < numbers.len() ==> #[trigger] interspersed[even(i)] == numbers[i])
        && (forall|i: int|
        0 <= i < numbers.len() - 1 ==> #[trigger] interspersed[odd(i)] == delimiter)
}

proof fn intersperse_spec_len(numbers: Seq<u64>, delimiter: u64)
    // post-conditions-start
    ensures
        numbers.len() > 0 ==> intersperse_spec(numbers, delimiter).len() == 2 * numbers.len() - 1,
    decreases numbers.len(),
    // post-conditions-end
{
    // impl-start
    if numbers.len() > 0 {
        intersperse_spec_len(numbers.drop_last(), delimiter);
    }
    // impl-end
}

proof fn intersperse_quantified_is_spec(numbers: Seq<u64>, delimiter: u64, interspersed: Seq<u64>)
    // pre-conditions-start
    requires
        intersperse_quantified(numbers, delimiter, interspersed),
    // pre-conditions-end
    // post-conditions-start
    ensures
        interspersed == intersperse_spec(numbers, delimiter),
    decreases numbers.len(),
    // post-conditions-end
{
    // impl-start
    let is = intersperse_spec(numbers, delimiter);
    if numbers.len() == 0 {
    } else if numbers.len() == 1 {
        assert(interspersed.len() == 1); // assert-line
        assert(interspersed[even(0)] == numbers[0]); // assert-line
    } else {
        intersperse_quantified_is_spec(
            numbers.drop_last(),
            delimiter,
            interspersed.take(interspersed.len() - 2),
        );
        intersperse_spec_len(numbers, delimiter);
        // assert-start
        assert_seqs_equal!(is == interspersed, i => {
            if i < is.len() - 2 {
            } else {
                if i % 2 == 0 {
                    assert(is[i] == numbers.last());
                    assert(interspersed[even(i/2)] == numbers[i / 2]);
                    assert(i / 2 == numbers.len() - 1);
                } else {
                    assert(is[i] == delimiter);
                    assert(interspersed[odd((i-1)/2)] == delimiter);
                }
            }
        });
        // assert-end
    }
    assert(interspersed =~= intersperse_spec(numbers, delimiter)); // assert-line
    // impl-end
}

fn intersperse(numbers: Vec<u64>, delimiter: u64) -> (result: Vec<u64>)
    // post-conditions-start
    ensures
        result@ == intersperse_spec(numbers@, delimiter),
    // post-conditions-end
{
    // impl-start
    if numbers.len() <= 1 {
        numbers
    } else {
        let mut result = Vec::new();
        let mut index = 0;
        while index < numbers.len() - 1
            // invariants-start
            invariant
                numbers.len() > 1,
                0 <= index < numbers.len(),
                result.len() == 2 * index,
                forall|i: int| 0 <= i < index ==> #[trigger] result[even(i)] == numbers[i],
                forall|i: int| 0 <= i < index ==> #[trigger] result[odd(i)] == delimiter,
            // invariants-end
        {
            result.push(numbers[index]);
            result.push(delimiter);
            index += 1;
        }
        result.push(numbers[numbers.len() - 1]);
        // assert-start
        proof {
            intersperse_quantified_is_spec(numbers@, delimiter, result@);
        }
        // assert-end
        result
    }
    // impl-end
}

} // verus!"""
    )
    assert verus_lang.remove_conditions(code) == dedent(
        """\
use vstd::assert_seqs_equal;
use vstd::prelude::*;
verus! {
spec fn intersperse_spec(numbers: Seq<u64>, delimiter: u64) -> (result:Seq<u64>)
    decreases numbers.len(),
{
    if numbers.len() <= 1 {
        numbers
    } else {
        intersperse_spec(numbers.drop_last(), delimiter) + seq![delimiter, numbers.last()]
    }
}
spec fn even(i: int) -> (result:int) {
    2 * i
}
spec fn odd(i: int) -> (result:int) {
    2 * i + 1
}
spec fn intersperse_quantified(numbers: Seq<u64>, delimiter: u64, interspersed: Seq<u64>) -> (result:bool) {
    (if numbers.len() == 0 {
        interspersed.len() == 0
    } else {
        interspersed.len() == 2 * numbers.len() - 1
    }) && (forall|i: int| 0 <= i < numbers.len() ==> #[trigger] interspersed[even(i)] == numbers[i])
        && (forall|i: int|
        0 <= i < numbers.len() - 1 ==> #[trigger] interspersed[odd(i)] == delimiter)
}
proof fn intersperse_spec_len(numbers: Seq<u64>, delimiter: u64)
{
}
proof fn intersperse_quantified_is_spec(numbers: Seq<u64>, delimiter: u64, interspersed: Seq<u64>)
{
}
fn intersperse(numbers: Vec<u64>, delimiter: u64) -> (result: Vec<u64>)
{
}
} // verus!"""
    )
