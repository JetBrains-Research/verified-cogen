use vstd::prelude::*;


verus! {

fn all_characters_same(char_arr: &Vec<char>) -> (result: bool)
    // post-conditions-start
    ensures
        result == (forall|i: int|
            1 <= i < char_arr@.len() ==> char_arr[0] == #[trigger] char_arr[i]),
    // post-conditions-end
{
    // impl-start
    if char_arr.len() <= 1 {
        return true;
    }
    let mut index = 1;
    while index < char_arr.len()
        // invariants-start
        invariant
            1 <= index <= char_arr.len(),
            forall|k: int| 0 <= k < index ==> char_arr[0] == #[trigger] char_arr[k],
        // invariants-end
    {
        if char_arr[0] != char_arr[index] {
            // assert-start
            assert(exists|i: int|
                1 <= i < char_arr@.len() && char_arr[0] != #[trigger] char_arr[i]);
            // assert-end
            return false;
        }
        index += 1;
    }
    true
    // impl-end
}

} // verus!

fn main() {}
