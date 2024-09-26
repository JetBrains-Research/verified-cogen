use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn is_sorted(lst: &[i32]) -> (result: bool)
    // pre-conditions-start
    requires
        lst.len() >= 1,
    // pre-conditions-end
    // post-conditions-start
    ensures
        result <== forall|i: int, j: int| 0 <= i && i < j && j < lst.len() ==> lst[i] <= lst[j],
        !result ==> exists|i: int, j: int| 0 <= i && i < j && j < lst.len() && lst[i] > lst[j],
    // post-conditions-end
{
    // impl-start
    let mut result = true;
    let mut i = 0;
    while i + 1 < lst.len()
        // invariants-start
        invariant
            0 <= i && i < lst.len(),
            result <== forall|k: int, l: int| 0 <= k < l < i ==> lst[k] <= lst[l],
            !result ==> exists|k: int, l: int| 0 <= k < l < i && lst[k] > lst[l],
        // invariants-end
    {
        if lst[i] > lst[i + 1] {
            result = false;
            break;
        }
        i = i + 1;
    }
    result
    // impl-end
}

fn main() {}
}
