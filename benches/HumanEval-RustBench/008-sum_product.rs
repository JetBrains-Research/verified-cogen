use vstd::prelude::*;

verus! {
spec fn sum(numbers: Seq<u32>) -> (result:int) {
    numbers.fold_left(0, |acc: int, x| acc + x)
}
// pure-end

spec fn product(numbers: Seq<u32>) -> (result:int) {
    numbers.fold_left(1, |acc: int, x| acc * x)
}
// pure-end

proof fn sum_bound(numbers: Seq<u32>)
    // post-conditions-start
    ensures
        sum(numbers) <= numbers.len() * u32::MAX,
    decreases numbers.len(),
    // post-conditions-end
{
    // impl-start
    if numbers.len() == 0 {
    } else {
        sum_bound(numbers.drop_last());
    }
    // impl-end
}
// pure-end

fn sum_product(numbers: Vec<u32>) -> (result: (u64, Option<u32>))
    // pre-conditions-start
    requires
        numbers.len() < u32::MAX,
    // pre-conditions-end
    // post-conditions-start
    ensures
        result.0 == sum(numbers@),
        result.1 matches Some(v) ==> v == product(numbers@),
    // post-conditions-end
{
    // impl-start
    let mut sum_value: u64 = 0;
    let mut prod_value: Option<u32> = Some(1);
    for index in 0..numbers.len()
        // invariants-start
        invariant
            numbers.len() < u32::MAX,
            sum_value == sum(numbers@.take(index as int)),
            prod_value matches Some(v) ==> v == product(numbers@.take(index as int)),
            index <= numbers.len(),
            index >= 0,
        // invariants-end
    {
        // assert-start
        proof {
            sum_bound(numbers@.take(index as int));
            assert(sum_value <= index * u32::MAX);
        }
        // assert-end
        assert(numbers@.take(index as int + 1).drop_last() =~= numbers@.take(index as int)); // assert-line
        assert(numbers[index as int] == numbers@.take(index as int + 1).last()); // assert-line
        sum_value += numbers[index] as u64;
        prod_value =
        match prod_value {
            Some(v) => v.checked_mul(numbers[index]),
            None => None,
        };
    }
    assert(numbers@.take(numbers@.len() as int) =~= numbers@); // assert-line
    (sum_value, prod_value)
    // impl-end
}

}
fn main() {}
