use vstd::prelude::*;

fn main() {}

verus! {

fn contains(arr: &Vec<i32>, key: i32) -> (result: bool)
    // post-conditions-start
    ensures
        result == (exists|i: int| 0 <= i < arr.len() && (arr[i] == key)),
    // post-conditions-end
{
    // impl-start
    let mut i = 0;
    while i < arr.len()
        // invariants-start
        invariant
            0 <= i <= arr.len(),
            forall|m: int| 0 <= m < i ==> (arr[m] != key),
        // invariants-end
    {
        if (arr[i] == key) {
            return true;
        }
        i += 1;
    }
    false
    // impl-end
}

fn any_value_exists(arr1: &Vec<i32>, arr2: &Vec<i32>) -> (result: bool)
    // post-conditions-start
    ensures
        result == exists|k: int| 0 <= k < arr1.len() && arr2@.contains(#[trigger] arr1[k]),
    // post-conditions-end
{
    // impl-start
    let mut index = 0;
    while index < arr1.len()
        // invariants-start
        invariant
            0 <= index <= arr1.len(),
            forall|k: int| 0 <= k < index ==> !arr2@.contains(#[trigger] arr1[k]),
        // invariants-end
    {
        if (contains(arr2, arr1[index])) {
            return true;
        }
        index += 1;
    }
    false
    // impl-end
}

} // verus!
