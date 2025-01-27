use vstd::prelude::*;

fn main() {}

verus! {

spec fn sum_negative_to(seq: Seq<i64>) -> (res: int)
    decreases seq.len(),
{
    if seq.len() == 0 {
        0
    } else {
        sum_negative_to(seq.drop_last()) + if (seq.last() < 0) {
            seq.last() as int
        } else {
            0 as int
        }
    }
}
// pure-end

fn sum_negatives(arr: &Vec<i64>) -> (sum_neg: i128)
    // post-conditions-start
    ensures
        sum_negative_to(arr@) == sum_neg,
    // post-conditions-end
{
    // impl-start
    let mut index = 0;
    let mut sum_neg = 0i128;

    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            forall|j: int|
                0 <= j <= index ==> (i64::MIN * index <= (sum_negative_to(
                    #[trigger] arr@.subrange(0, j),
                )) <= 0),
            sum_negative_to(arr@.subrange(0, index as int)) == sum_neg,
        // invariants-end
    {
        if (arr[index] < 0) {
            sum_neg = sum_neg + (arr[index] as i128);
        }
        index += 1;
        // assert-start
        assert(arr@.subrange(0, index - 1 as int) == arr@.subrange(0, index as int).drop_last());
        // assert-end
    }
    // assert-start
    assert(arr@ == arr@.subrange(0, index as int));
    // assert-end
    sum_neg
    // impl-end
}

} // verus!