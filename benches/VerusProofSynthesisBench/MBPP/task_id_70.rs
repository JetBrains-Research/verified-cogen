use vstd::prelude::*;

verus! {

fn all_sequence_equal_length(seq: &Vec<Vec<i32>>) -> (result: bool)
    // pre-conditions-start
    requires
        seq.len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        result == (forall|i: int, j: int|
            (0 <= i < seq.len() && 0 <= j < seq.len()) ==> (#[trigger] seq[i].len()
                == #[trigger] seq[j].len())),
    // post-conditions-end
{
    // impl-start
    let mut index = 1;
    while index < seq.len()
        // invariants-start
        invariant
            1 <= index <= seq.len(),
            forall|k: int| 0 <= k < index ==> (#[trigger] seq[k].len() == (&seq[0]).len()),
        // invariants-end
    {
        if ((&seq[index]).len() != (&seq[0]).len()) {
            return false;
        }
        index += 1;
    }
    true
    // impl-end
}

} // verus!


fn main() {}