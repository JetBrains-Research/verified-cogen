use vstd::prelude::*;

verus! {

fn min_sublist(seq: &Vec<Vec<i32>>) -> (min_list: &Vec<i32>)
    // pre-conditions-start
    requires
        seq.len() > 0,
    // pre-conditions-end
    // post-conditions-start
    ensures
        forall|k: int| 0 <= k < seq.len() ==> min_list.len() <= #[trigger] (seq[k]).len(),
        exists|k: int| 0 <= k < seq.len() && min_list@ =~= #[trigger] (seq[k]@),
    // post-conditions-end
{
    // impl-start
    let mut min_list = &seq[0];
    assert(min_list@ =~= seq[0]@);
    let mut index = 1;

    while index < seq.len()
        // invariants-start
        invariant
            0 <= index <= seq.len(),
            forall|k: int| 0 <= k < index ==> min_list.len() <= #[trigger] (seq[k]).len(),
            exists|k: int| 0 <= k < index && min_list@ =~= #[trigger] (seq[k]@),
        // invariants-end
    {
        if ((seq[index]).len() < min_list.len()) {
            min_list = &seq[index];
        }
        index += 1;
    }
    min_list
    // impl-end
}

} // verus!

fn main() {}
