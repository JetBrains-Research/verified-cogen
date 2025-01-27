use vstd::prelude::*;

fn main() {}

verus! {

fn is_smaller(arr1: &Vec<i32>, arr2: &Vec<i32>) -> (result: bool)
    // pre-conditions-start
    requires
        arr1.len() == arr2.len(),
    // pre-conditions-end
    // post-conditions-start
    ensures
        result == (forall|i: int| 0 <= i < arr1.len() ==> arr1[i] > arr2[i]),
    // post-conditions-end
{
    // impl-start
    let mut index = 0;
    while index < arr1.len()
        // invariants-start
        invariant
            0 <= index <= arr1.len(),
            arr1.len() == arr2.len(),
            0 <= index <= arr2.len(),
            forall|k: int| 0 <= k < index ==> arr1[k] > arr2[k],
        // invariants-end
    {
        if arr1[index] <= arr2[index] {
            return false;
        }
        index += 1;
    }
    true
    // impl-end
}

} // verus!
