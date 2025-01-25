use vstd::prelude::*;

verus! {

spec fn count_boolean(seq: Seq<bool>) -> (result: int)
    decreases seq.len(),
{
    if seq.len() == 0 {
        0
    } else {
        count_boolean(seq.drop_last()) + if (seq.last()) {
            1 as int
        } else {
            0 as int
        }
    }
}
// pure-end

fn count_true(arr: &Vec<bool>) -> (count: u64)
    // pre-conditions-start
    ensures
        0 <= count <= arr.len(),
        count_boolean(arr@) == count,
    // pre-conditions-end
{
    // impl-start
    let mut index = 0;
    let mut counter = 0;

    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            0 <= counter <= index,
            count_boolean(arr@.subrange(0, index as int)) == counter,
        // invariants-end
    {
        if (arr[index]) {
            counter += 1;
        }
        index += 1;
        // assert-start
        assert(arr@.subrange(0, index - 1 as int) == arr@.subrange(0, index as int).drop_last());
        // assert-end
    }
    // assert-start
    assert(arr@ == arr@.subrange(0, index as int));
    // assert-end
    counter
    // impl-end
}

} // verus!

fn main() {}