use vstd::prelude::*;


verus! {

fn contains_k(arr: &Vec<i32>, k: i32) -> (result: bool)
    // post-conditions-start
    ensures
        result == (exists|i: int| 0 <= i < arr.len() && (arr[i] == k)),
    // post-conditions-end
{
    // impl-start
    let mut index = 0;
    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            forall|m: int| 0 <= m < index ==> (arr[m] != k),
        // invariants-end
    {
        if (arr[index] == k) {
            return true;
        }
        index += 1;
    }
    false
    // impl-end
}

} // verus!

fn main() {}