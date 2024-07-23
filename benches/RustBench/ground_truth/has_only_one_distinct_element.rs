use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn has_only_one_distinct_element(a: &[i32]) -> (result: bool)
    ensures
        result ==> forall|i: int, j: int| 0 <= i < a.len() && 0 <= j < a.len() ==> a[i] == a[j],
        !result ==> exists|i: int, j: int| 0 <= i < a.len() && 0 <= j < a.len() && a[i] != a[j],
{
    if a.len() == 0 {
        return true;
    }

    let first = a[0];
    let mut i = 1;
    while i < a.len()
        invariant
            0 <= i <= a.len(),
            forall|k: int, l: int| 0 <= k < i && 0 <= l < i ==> a[k] == a[l],
    {
        if a[i] != first {
            return false;
        }
        i = i + 1;
    }
    true
}

fn main() {}
}
