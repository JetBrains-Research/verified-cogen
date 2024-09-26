use vstd::assert_seqs_equal;
use vstd::prelude::*;

verus! {
pub open spec fn intersperse_spec(numbers: Seq<u64>, delimiter: u64) -> Seq<u64>
    decreases numbers.len(),
{
    // impl-start
    if numbers.len() <= 1 {
        numbers
    } else {
        intersperse_spec(numbers.drop_last(), delimiter) + seq![delimiter, numbers.last()]
    }
    // impl-end
}
spec fn even(i: int) -> int {
    2 * i
}

spec fn odd(i: int) -> int {
    2 * i + 1
}
spec fn intersperse_quantified(numbers: Seq<u64>, delimiter: u64, interspersed: Seq<u64>) -> bool {
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
    // post-conditions-end
    decreases numbers.len(),
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
    // post-conditions-end
    decreases numbers.len(),
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

}
fn main() {}
