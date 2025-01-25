use vstd::prelude::*;

fn main() {}

verus! {

fn list_deep_clone(arr: &Vec<u64>) -> (copied: Vec<u64>)
    // post-conditions-start
    ensures
        arr@.len() == copied@.len(),
        forall|i: int| (0 <= i < arr.len()) ==> arr[i] == copied[i],
    // post-conditions-end
{
    // impl-start
    let mut copied_array = Vec::with_capacity(arr.len());
    let mut index = 0;
    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            copied_array.len() == index,
            forall|i: int| (0 <= i < index) ==> arr[i] == copied_array[i],
        // invariants-end
    {
        copied_array.push(arr[index]);
        index += 1;
    }
    copied_array
    // impl-end
}

} // verus!
