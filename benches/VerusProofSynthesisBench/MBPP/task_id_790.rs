use vstd::prelude::*;

fn main() {}

verus! {

fn is_even_at_even_index(arr: &Vec<usize>) -> (result: bool)
    // post-conditions-start
    ensures
        result == forall|i: int| 0 <= i < arr.len() ==> ((i % 2) == (arr[i] % 2)),
    // post-conditions-end
{
    // impl-start
    let mut index = 0;
    while index < arr.len()
        // invariants-start
        invariant
            0 <= index <= arr.len(),
            forall|i: int| 0 <= i < index ==> ((i % 2) == (arr[i] % 2)),
        // invariants-end
    {
        if ((index % 2) != (arr[index] % 2)) {
            // assert-start
            assert(((index as int) % 2) != (arr[index as int] % 2));
            // assert-end
            return false;
        }
        index += 1;
    }
    true
    // impl-end
}

} // verus!
