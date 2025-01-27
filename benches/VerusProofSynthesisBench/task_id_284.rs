use vstd::prelude::*;

fn main() {}

verus! {

fn all_elements_equals(arr: &Vec<i32>, element: i32) -> (result: bool)
    // post-conditions-start
    ensures
        result == (forall|i: int| 0 <= i < arr.len() ==> (arr[i] == element)),
    // post-conditions-end
{
    // impl-start
    let mut index = 0;
    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            forall|k: int| 0 <= k < index ==> (arr[k] == element),
        // invariants-end
    {
        if arr[index] != element {
            return false;
        }
        index += 1;
    }
    true
    // impl-end
}

} // verus!
