use vstd::prelude::*;

verus! {

spec fn sum_to(arr: Seq<i64>) -> (result: int)
    decreases arr.len(),
{
    if arr.len() == 0 {
        0
    } else {
        sum_to(arr.drop_last()) + arr.last()
    }
}
// pure-end

fn sum(arr: &Vec<i64>) -> (sum: i128)
    // post-conditions-start
    ensures
        sum_to(arr@) == sum,
    // post-conditions-end
{
    // impl-start
    let mut index = 0;
    let mut sum = 0i128;

    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            sum == sum_to(arr@.subrange(0, index as int)),
            forall|j: int|
                0 <= j <= index ==> (i64::MIN * index <= (sum_to(#[trigger] arr@.subrange(0, j)))
                    <= i64::MAX * index),
        // invariants-end
    {
        // assert-start
        assert(arr@.subrange(0, index as int) =~= arr@.subrange(0, (index + 1) as int).drop_last());
        // assert-end
        sum = sum + arr[index] as i128;
        index += 1;
    }
    // assert-start
    assert(arr@ == arr@.subrange(0, index as int));
    // assert-end
    sum
    // impl-end
}

} // verus!

fn main() {}
