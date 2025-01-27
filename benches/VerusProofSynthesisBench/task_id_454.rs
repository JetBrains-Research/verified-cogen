use vstd::prelude::*;

verus! {

fn contains_z(text: &Vec<char>) -> (result: bool)
    // post-conditions-start
    ensures
        result == (exists|i: int| 0 <= i < text.len() && (text[i] == 'Z' || text[i] == 'z')),
    // post-conditions-end
{
    // impl-start
    let mut index = 0;
    while index < text.len()
        // invariants-start
        invariant
            0 <= index <= text.len(),
            forall|k: int| 0 <= k < index ==> (text[k] != 'Z' && text[k] != 'z'),
        // invariants-end
    {
        if text[index] == 'Z' || text[index] == 'z' {
            return true;
        }
        index += 1;
    }
    false
    // impl-end
}

} // verus!

fn main() {}
