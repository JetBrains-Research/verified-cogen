use vstd::prelude::*;

verus! {

#[verifier::loop_isolation(false)]
fn smallest_missing_number(s: &[i32]) -> (v: i32)
    // pre-conditions-start
    requires
        forall|i: int, j: int| 0 <= i < j < s.len() ==> s[i] <= s[j],
        forall|i: int| 0 <= i < s.len() ==> s[i] >= 0,
        s.len() <= 100_000,
    // pre-conditions-end
    // post-conditions-start
    ensures
        0 <= v,
        forall|i: int| 0 <= i < s.len() ==> s[i] != v,
        forall|k: int| 0 <= k < v && s[k] != v ==> exists|j: int| 0 <= j < s.len() && s[j] == k,
    // post-conditions-end
{
    // impl-start
    let mut v = 0;
    let mut i = 0;
    while i < s.len()
        // invariants-start
        invariant
            0 <= i <= s.len(),
            0 <= v <= i,
            forall|k: int| 0 <= k < i ==> s[k] != v,
            forall|k: int| 0 <= k < v && s[k] != v ==> exists|j: int| 0 <= j < i && s[j] == k,
        // invariants-end
    {
        if s[i] > v {
            break;
        } else {
            if s[i] == v {
                v = v + 1;
            }
        }
        i = i + 1;
    }
    v
    // impl-end
}

fn main() {}
}
