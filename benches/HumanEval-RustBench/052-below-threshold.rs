use vstd::prelude::*;

verus! {

fn below_threshold(l: &[i32], t: i32) -> (result: bool)
    // post-conditions-start
    ensures
        result == forall|i: int| 0 <= i < l.len() ==> l[i] < t,
    // post-conditions-end
{
    // impl-start
    for i in 0..l.len()
        // invariants-start
        invariant
            forall|j: int| 0 <= j < i ==> l[j] < t,
        // invariants-end
    {
        if l[i] >= t {
            return false;
        }
    }
    true
    // impl-end
}

}
fn main() {}
