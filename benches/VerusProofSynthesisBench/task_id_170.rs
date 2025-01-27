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

fn sum_range_list(arr: &Vec<i64>, start: usize, end: usize) -> (sum: i128)
    // pre-conditions-start
    requires
        0 <= start <= end,
        start <= end < arr.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        sum_to(arr@.subrange(start as int, end + 1 as int)) == sum,
    // post-conditions-end
{
    // impl-start
    let mut index = start;
    let mut sum = 0i128;
    let _end = end + 1;

    while index < _end
        // invariants-start
        invariant
            start <= _end <= arr.len(),
            start <= index <= _end,
            sum == sum_to(arr@.subrange(start as int, index as int)),
            forall|j: int|
                start <= j <= index ==> (i64::MIN * index <= (sum_to(
                    #[trigger] arr@.subrange(start as int, j),
                )) <= i64::MAX * index),
        // invariants-end
    {
        // assert-start
        assert(arr@.subrange(start as int, index as int) =~= arr@.subrange(
            start as int,
            (index + 1) as int,
        ).drop_last());
        // assert-end
        sum = sum + arr[index] as i128;
        index += 1;
    }
    sum
    // impl-end
}

} // verus!

fn main() {}