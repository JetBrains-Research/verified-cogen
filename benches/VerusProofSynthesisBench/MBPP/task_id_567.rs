use vstd::prelude::*;

verus! {

fn is_sorted(arr: &Vec<i32>) -> (is_sorted: bool)
    // pre-conditions-start
    requires
        arr.len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        is_sorted == (forall|i: int, j: int| 0 <= i < j < arr.len() ==> (arr[i] <= arr[j])),
    // post-conditions-end
{
    // impl-start
    let mut index = 0;
    while index < arr.len() - 1
        // invariants-start
        invariant
            0 <= index <= arr.len() - 1,
            forall|k: int, l: int| 0 <= k < l <= index ==> arr[k] <= arr[l],
        // invariants-end
    {
        if arr[index] > arr[index + 1] {
            return false;
        }
        index += 1;
    }
    true
    // impl-end
}

} // verus!

fn main() {}
