use vstd::prelude::*;


verus! {

fn max_length_list(seq: &Vec<Vec<i32>>) -> (max_list: &Vec<i32>)
    // pre-conditions-start
    requires
        seq.len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        forall|k: int| 0 <= k < seq.len() ==> max_list.len() >= #[trigger] (seq[k]).len(),
        exists|k: int| 0 <= k < seq.len() && max_list@ =~= #[trigger] (seq[k]@),
    // post-conditions-end
{
    // impl-start
    let mut max_list = &seq[0];
    assert(max_list@ =~= seq[0]@);
    let mut index = 1;

    while index < seq.len()
        // invariants-start
        invariant
            0 <= index <= seq.len(),
            forall|k: int| 0 <= k < index ==> max_list.len() >= #[trigger] (seq[k]).len(),
            exists|k: int| 0 <= k < index && max_list@ =~= #[trigger] (seq[k]@),
        // invariants-end
    {
        if ((seq[index]).len() > max_list.len()) {
            max_list = &seq[index];
        }
        index += 1;
    }
    max_list
    // impl-end
}

} // verus!

fn main() {}
