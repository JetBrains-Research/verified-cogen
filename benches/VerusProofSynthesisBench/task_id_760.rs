use vstd::prelude::*;

fn main() {}

verus! {

fn has_only_one_distinct_element(arr: &Vec<i32>) -> (result: bool)
    // pre-conditions-start
    ensures
        result == (forall|i: int| 1 <= i < arr@.len() ==> arr[0] == #[trigger] arr[i]),
    // pre-conditions-end
{
    // impl-start
    if arr.len() <= 1 {
        return true;
    }
    let mut index = 1;
    while index < arr.len()
        // invariants-start
        invariant
            1 <= index <= arr.len(),
            forall|k: int| 0 <= k < index ==> arr[0] == #[trigger] arr[k],
        // invariants-end
    {
        if arr[0] != arr[index] {
            // assert-start
            assert(exists|i: int| 1 <= i < arr@.len() && arr[0] != #[trigger] arr[i]);
            // assert-end
            return false;
        }
        index += 1;
    }
    true
    // impl-end
}

} // verus!
