use vstd::prelude::*;

fn main() {}

verus! {

fn is_greater(arr: &Vec<i32>, number: i32) -> (result: bool)
    // post-conditions-start
    ensures
        result == (forall|i: int| 0 <= i < arr.len() ==> number > arr[i]),
    // post-conditions-end
{
    // impl-start
    let mut i = 0;
    while i < arr.len()
        // invariants-start
        invariant
            0 <= i <= arr.len(),
            forall|k: int| 0 <= k < i ==> number > arr[k],
        // invariants-end
    {
        if number <= arr[i] {
            return false;
        }
        i += 1;
    }
    true
    // impl-end
}

} // verus!
