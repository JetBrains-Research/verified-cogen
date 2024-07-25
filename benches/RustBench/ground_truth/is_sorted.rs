use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn is_sorted(lst: &[i32]) -> (result: bool)
    requires
        lst.len() >= 1,
    ensures
        result <== forall|i: int, j: int| 0 <= i && i < j && j < lst.len() ==> lst[i] <= lst[j],
        !result ==> exists|i: int, j: int| 0 <= i && i < j && j < lst.len() && lst[i] > lst[j],
{
    let mut result = true;
    let mut i = 0;
    while i + 1 < lst.len()
        invariant
            0 <= i && i < lst.len(),
            result <== forall|k: int, l: int| 0 <= k < l < i ==> lst[k] <= lst[l],
            !result ==> exists|k: int, l: int| 0 <= k < l < i && lst[k] > lst[l],
    {
        if lst[i] > lst[i + 1] {
            result = false;
            break;
        }
        i = i + 1;
    }
    result
}

fn main() {}
}